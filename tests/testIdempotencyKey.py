import unittest
import uuid

from parameterized import parameterized

from seatsio import Client, Region
from seatsio.exceptions import SeatsioException, RateLimitExceededException, BestAvailableObjectsNotFoundException
from seatsio.httpClient import HttpClient
from tests.util.asserts import assert_that
from tests.util.fakeServer import FakeServer, FakeClock, Reply, status, json_reply, error


class IdempotencyKeyTest(unittest.TestCase):

    def setUp(self):
        self.server = FakeServer().start()
        self.clock = FakeClock()

    def tearDown(self):
        self.server.close()

    @parameterized.expand([("post",), ("put",), ("delete",)])
    def test_writes_get_an_idempotency_key(self, method):
        self.server.enqueue(status(200))

        getattr(self.client().url("/anything"), method)({})

        assert_that(uuid.UUID(self.server.sent_idempotency_keys()[0]).version).is_equal_to(4)

    def test_gets_do_not_get_an_idempotency_key(self):
        self.server.enqueue(json_reply(200, "{}"))

        self.client().url("/anything").get()

        assert_that(self.server.sent_idempotency_keys()).is_equal_to([None])

    def test_each_request_gets_its_own_key(self):
        self.server.enqueue(status(200), status(200))
        client = self.client()

        client.url("/anything").post({})
        client.url("/anything").post({})

        keys = self.server.sent_idempotency_keys()
        assert_that(keys[0]).is_not_equal_to(keys[1])

    def test_failed_requests_expose_their_idempotency_key(self):
        self.server.enqueue(error(500, "SOME_ERROR"))

        with self.assertRaises(SeatsioException) as context:
            self.client().url("/anything").post({})

        assert_that(context.exception.idempotency_key).is_equal_to(self.server.sent_idempotency_keys()[0])
        assert_that(context.exception.idempotencyKey).is_equal_to(self.server.sent_idempotency_keys()[0])

    def test_connection_failures_expose_their_idempotency_key(self):
        url = self.server.url()
        self.server.close()

        with self.assertRaises(SeatsioException) as context:
            HttpClient(url, "secretKey", None, 0, clock=self.clock).url("/anything").post({})

        assert_that(uuid.UUID(context.exception.idempotency_key).version).is_equal_to(4)
        assert_that(context.exception.idempotencyKey).is_equal_to(context.exception.idempotency_key)

    def test_rejects_idempotency_keys_that_are_not_v4_uuids(self):
        for key in ["", "not-a-uuid", str(uuid.uuid1()), " " + str(uuid.uuid4()), uuid.uuid4(), None]:
            with self.assertRaises(ValueError):
                self.client().with_idempotency_key(key)
            with self.assertRaises(ValueError):
                Client(Region(self.server.url()), "secretKey").with_idempotency_key(key)

    def test_accepts_uppercase_v4_uuids(self):
        key = str(uuid.uuid4()).upper()
        self.server.enqueue(status(200))

        self.client().with_idempotency_key(key).url("/anything").post({})

        assert_that(self.server.sent_idempotency_keys()).is_equal_to([key])

    def test_a_client_with_a_key_sends_it_with_every_write(self):
        key = str(uuid.uuid4())
        self.server.enqueue(status(200), status(200))
        client = self.client().with_idempotency_key(key)

        client.url("/anything").post({})
        client.url("/anything").delete()

        assert_that(self.server.sent_idempotency_keys()).is_equal_to([key, key])

    def test_a_client_with_a_key_doesnt_send_it_with_a_get(self):
        self.server.enqueue(json_reply(200, "{}"))

        self.client().with_idempotency_key(str(uuid.uuid4())).url("/anything").get()

        assert_that(self.server.sent_idempotency_keys()).is_equal_to([None])

    def test_the_original_client_keeps_generating_keys(self):
        key = str(uuid.uuid4())
        self.server.enqueue(status(200))
        client = self.client()
        client.with_idempotency_key(key)

        client.url("/anything").post({})

        assert_that(self.server.sent_idempotency_keys()[0]).is_not_equal_to(key)

    def test_seatsio_client_can_retry_with_the_same_idempotency_key(self):
        key = str(uuid.uuid4())
        self.server.enqueue(status(200), status(200))
        client = Client(Region(self.server.url()), "secretKey").with_idempotency_key(key)

        client.events.update("event1", event_key="event2")
        client.events.update("event1", event_key="event2")

        assert_that(self.server.sent_idempotency_keys()).is_equal_to([key, key])

    def test_the_copy_keeps_the_workspace_key(self):
        self.server.enqueue(status(200))
        client = Client(Region(self.server.url()), "secretKey", "aWorkspaceKey")

        client.with_idempotency_key(str(uuid.uuid4())).events.update("event1", event_key="event2")

        assert_that(self.server.requests[0].header("X-Workspace-Key")).is_equal_to("aWorkspaceKey")

    def test_a_client_for_another_workspace_uses_that_workspace_and_generates_its_own_keys(self):
        self.server.enqueue(status(200), status(200))
        client = Client(Region(self.server.url()), "secretKey", "workspace1")

        client.with_idempotency_key(str(uuid.uuid4())).events.update("event1", event_key="event2")
        client.with_workspace_key("workspace2").events.update("event1", event_key="event2")

        assert_that(self.server.requests[1].header("X-Workspace-Key")).is_equal_to("workspace2")
        keys = self.server.sent_idempotency_keys()
        assert_that(keys[1]).is_not_equal_to(keys[0])

    @parameterized.expand([
        ('{}',),
        ('{"errors": []}',),
        ('{"errors": null}',),
        ('{"errors": [null, "x", {"code": 1}]}',),
        ('null',),
        ('[]',),
        ('"a string"',),
        ('not json',),
        ('',),
    ])
    def test_unusual_error_bodies_give_a_seatsio_exception(self, body):
        self.server.enqueue(json_reply(400, body))

        with self.assertRaises(SeatsioException) as context:
            self.client().url("/anything").post({})

        assert_that(context.exception.message).is_equal_to("Error while executing POST " + self.server.url("/anything"))
        assert_that(context.exception.requestId).is_none()

    def test_an_error_body_without_content_type_is_not_parsed(self):
        self.server.enqueue(Reply(400, {}, '{"errors": [{"code": "X", "message": "m"}]}'))

        with self.assertRaises(SeatsioException) as context:
            self.client().url("/anything").post({})

        assert_that(context.exception.errors).is_none()

    def test_an_error_body_gives_the_errors_and_message(self):
        self.server.enqueue(error(400, "SOME_ERROR"))

        with self.assertRaises(SeatsioException) as context:
            self.client().url("/anything").post({})

        assert_that(context.exception.message).is_equal_to("SOME_ERROR.")
        assert_that(context.exception.errors).is_equal_to([{"code": "SOME_ERROR", "message": "SOME_ERROR"}])
        assert_that(context.exception.requestId).is_equal_to("aRequestId")

    def test_a_429_without_an_error_code_is_a_rate_limit_exception(self):
        self.server.enqueue(status(429))
        client = self.client()
        client.max_retries = 0

        with self.assertRaises(RateLimitExceededException):
            client.url("/anything").post({})

    def test_best_available_objects_not_found(self):
        self.server.enqueue(error(400, "BEST_AVAILABLE_OBJECTS_NOT_FOUND"))

        with self.assertRaises(BestAvailableObjectsNotFoundException):
            self.client().url("/anything").post({})

    def client(self):
        return HttpClient(self.server.url(), "secretKey", None, 5, clock=self.clock)
