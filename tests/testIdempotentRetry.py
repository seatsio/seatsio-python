import unittest
import uuid

import requests
from parameterized import parameterized

from seatsio import Client, Region
from seatsio.exceptions import SeatsioException, RateLimitExceededException
from seatsio.httpClient import HttpClient, Delivery
from tests.util.asserts import assert_that
from tests.util.fakeServer import FakeServer, FakeClock, LOST_RESPONSE, status, key_status, json_reply, error, \
    free_port

BOOK = "/events/{key}/actions/book"


class IdempotentRetryTest(unittest.TestCase):

    def setUp(self):
        self.server = FakeServer().start()
        self.clock = FakeClock()

    def tearDown(self):
        self.server.close()

    # guide test 1
    @parameterized.expand([("POST",), ("DELETE",)])
    def test_a_lost_response_is_retried_with_the_same_key_on_a_route_that_honors_keys(self, method):
        client = self.client()
        self.server.enqueue(key_status(200, "executed"), LOST_RESPONSE,
                            key_status(json_reply(200, '{"replayed": true}'), "replayed"))

        self.send(client, method)
        response = self.send(client, method)

        assert_that(response.text).is_equal_to('{"replayed": true}')
        keys = self.server.sent_idempotency_keys()
        assert_that(keys).has_size(3)
        assert_that(None in keys).is_false()
        assert_that(keys[2]).is_equal_to(keys[1])
        assert_that(keys[1]).is_not_equal_to(keys[0])

    # guide test 2
    def test_a_lost_response_is_not_retried_on_a_route_that_ignores_keys(self):
        client = self.client()
        self.server.enqueue(key_status(200, "ignored"), LOST_RESPONSE)

        self.send(client, "POST")
        e = self.fails(lambda: self.send(client, "POST"))

        assert_that(self.server.request_count).is_equal_to(2)
        assert_that(e.outcome_is_unknown()).is_true()
        assert_that(e.is_safe_to_retry_with_same_key()).is_false()
        assert_that(e.idempotency_key).is_equal_to(self.server.sent_idempotency_keys()[1])

    # guide test 3
    def test_a_lost_response_is_not_retried_on_a_route_that_never_sent_a_status(self):
        client = self.client()
        self.server.enqueue(status(200), LOST_RESPONSE)

        self.send(client, "POST")
        self.fails(lambda: self.send(client, "POST"))

        assert_that(self.server.request_count).is_equal_to(2)

    # guide test 4
    @parameterized.expand([("POST",), ("PUT",), ("DELETE",)])
    def test_the_first_request_to_a_route_is_not_retried_after_a_lost_response(self, method):
        self.server.enqueue(LOST_RESPONSE, status(200))

        e = self.fails(lambda: self.send(self.client(), method))

        assert_that(self.server.request_count).is_equal_to(1)
        assert_that(e.outcome_is_unknown()).is_true()
        assert_that(e.is_safe_to_retry_with_same_key()).is_false()
        assert_that(e.idempotency_key).is_equal_to(self.server.sent_idempotency_keys()[0])

    # guide test 5
    def test_a_request_that_was_never_sent_is_retried_with_the_same_key(self):
        port = free_port()
        with FakeServer() as late:
            late.enqueue(status(200))
            self.clock.on_sleep = lambda: late.start(port)

            HttpClient("http://127.0.0.1:%d" % port, "secretKey", None, 5, clock=self.clock).url("/").post({})

            assert_that(self.clock.sleeps).is_equal_to(1)
            assert_that(late.request_count).is_equal_to(1)
            assert_that(uuid.UUID(late.sent_idempotency_keys()[0]).version).is_equal_to(4)

    # guide test 6
    def test_routes_are_remembered_separately(self):
        client = self.client()
        self.server.enqueue(key_status(200, "executed"), LOST_RESPONSE)

        client.url("/a").post({})
        self.fails(lambda: client.url("/b").post({}))

        assert_that(self.server.request_count).is_equal_to(2)

    def test_methods_are_remembered_separately(self):
        client = self.client()
        self.server.enqueue(key_status(200, "executed"), LOST_RESPONSE)

        self.send(client, "POST")
        self.fails(lambda: self.send(client, "DELETE"))

        assert_that(self.server.request_count).is_equal_to(2)

    # guide test 7
    @parameterized.expand([(200,), (400,), (500,)])
    def test_the_latest_known_status_of_a_route_wins(self, ignored_status):
        client = self.client()
        self.server.enqueue(key_status(200, "executed"), key_status(ignored_status, "ignored"), LOST_RESPONSE)

        self.send(client, "POST")
        try:
            self.send(client, "POST")
        except SeatsioException:
            pass
        self.fails(lambda: self.send(client, "POST"))

        assert_that(self.server.request_count).is_equal_to(3)

    # guide test 8
    @parameterized.expand([(401,), (429,)])
    def test_a_response_without_a_status_leaves_the_memory_alone(self, code):
        client = self.client()
        self.server.enqueue(key_status(200, "executed"), error(code, "SOME_ERROR"), LOST_RESPONSE,
                            key_status(200, "replayed"))

        self.send(client, "POST")
        client.max_retries = 0
        self.fails(lambda: self.send(client, "POST"))
        client.max_retries = 1
        self.send(client, "POST")

        assert_that(self.server.request_count).is_equal_to(4)

    # guide test 9
    def test_concrete_paths_of_the_same_template_share_the_memory(self):
        client = self.client()
        self.server.enqueue(key_status(200, "executed"), LOST_RESPONSE, key_status(200, "replayed"))

        client.url(BOOK, key="event1").post({})
        client.url(BOOK, key="event2").post({})

        assert_that(self.server.request_count).is_equal_to(3)

    # guide test 10
    def test_copies_with_a_key_share_the_memory(self):
        client = self.client()
        self.server.enqueue(key_status(200, "executed"), LOST_RESPONSE, key_status(200, "replayed"))

        self.send(client, "POST")
        self.send(client.with_idempotency_key(str(uuid.uuid4())), "POST")

        assert_that(self.server.request_count).is_equal_to(3)

    def test_the_original_client_shares_the_memory_of_its_copies(self):
        client = self.client()
        self.server.enqueue(key_status(200, "executed"), LOST_RESPONSE, key_status(200, "replayed"))

        self.send(client.with_idempotency_key(str(uuid.uuid4())), "POST")
        self.send(client, "POST")

        assert_that(self.server.request_count).is_equal_to(3)

    def test_other_clients_dont_share_the_memory(self):
        self.server.enqueue(key_status(200, "executed"), LOST_RESPONSE)

        self.send(HttpClient(self.server.url(), "aSecretKey", None, 5, clock=self.clock), "POST")
        self.fails(lambda: self.send(HttpClient(self.server.url(), "anotherSecretKey", None, 5, clock=self.clock), "POST"))

        assert_that(self.server.request_count).is_equal_to(2)

    # guide test 11
    def test_a_retry_sends_the_same_request(self):
        client = HttpClient(self.server.url(), "secretKey", "aWorkspaceKey", 5, clock=self.clock)
        self.server.enqueue(key_status(200, "executed"), LOST_RESPONSE, key_status(200, "replayed"))

        client.url(BOOK, key="event1").post({})
        client.url(BOOK, query_params={"expand": "x"}, key="event2").post({"objects": ["A-1"]})

        lost, retry = self.server.requests[1], self.server.requests[2]
        assert_that(retry.method).is_equal_to(lost.method)
        assert_that(retry.method).is_equal_to("POST")
        assert_that(retry.target).is_equal_to(lost.target)
        assert_that(retry.target).is_equal_to("/events/event2/actions/book?expand=x")
        assert_that(retry.body).is_equal_to(lost.body)
        assert_that(retry.body).is_equal_to(b'{"objects": ["A-1"]}')
        for header in ["Idempotency-Key", "X-Workspace-Key", "Authorization"]:
            assert_that(retry.header_values(header)).has_size(1)
            assert_that(retry.header_values(header)).is_equal_to(lost.header_values(header))

    # guide test 12
    def test_an_unknown_status_leaves_the_memory_alone(self):
        client = self.client()
        self.server.enqueue(key_status(200, "executed"), key_status(200, "maybe"), LOST_RESPONSE,
                            key_status(200, "replayed"))

        self.send(client, "POST")
        self.send(client, "POST")
        self.send(client, "POST")

        assert_that(self.server.request_count).is_equal_to(4)

    def test_an_unknown_status_does_not_mark_a_route_as_honoring_keys(self):
        client = self.client()
        self.server.enqueue(key_status(200, "maybe"), LOST_RESPONSE)

        self.send(client, "POST")
        self.fails(lambda: self.send(client, "POST"))

        assert_that(self.server.request_count).is_equal_to(2)

    def test_the_status_is_case_insensitive(self):
        client = self.client()
        self.server.enqueue(key_status(200, " Executed "), LOST_RESPONSE, key_status(200, "replayed"))

        self.send(client, "POST")
        self.send(client, "POST")

        assert_that(self.server.request_count).is_equal_to(3)

    # guide test 13
    def test_in_use_marks_a_route_as_honoring_keys(self):
        client = self.client()
        self.server.enqueue(key_status(error(409, "IDEMPOTENCY_KEY_IN_USE"), "in-use"), LOST_RESPONSE,
                            key_status(200, "replayed"))

        client.max_retries = 0
        e = self.fails(lambda: self.send(client, "POST"))
        client.max_retries = 1
        self.send(client, "POST")

        assert_that(self.server.request_count).is_equal_to(3)
        assert_that(e.idempotency_key_honored).is_true()
        assert_that(e.replayed).is_false()

    def test_reused_marks_a_route_as_honoring_keys(self):
        client = self.client()
        self.server.enqueue(key_status(error(422, "IDEMPOTENCY_KEY_REUSED"), "reused"), LOST_RESPONSE,
                            key_status(200, "replayed"))

        e = self.fails(lambda: self.send(client, "POST"))
        self.send(client, "POST")

        assert_that(self.server.request_count).is_equal_to(3)
        assert_that(e.idempotency_key_honored).is_true()
        assert_that(e.replayed).is_false()
        assert_that(e.outcome_is_unknown()).is_false()
        assert_that(e.is_safe_to_retry_with_same_key()).is_false()

    def test_replayed_marks_a_route_as_honoring_keys(self):
        client = self.client()
        self.server.enqueue(key_status(200, "replayed"), LOST_RESPONSE, key_status(200, "replayed"))

        self.send(client, "POST")
        self.send(client, "POST")

        assert_that(self.server.request_count).is_equal_to(3)

    def test_a_replayed_error_is_reported_as_replayed(self):
        self.server.enqueue(key_status(error(400, "SOME_ERROR"), "replayed"))

        e = self.fails(lambda: self.send(self.client(), "POST"))

        assert_that(e.replayed).is_true()
        assert_that(e.idempotency_key_honored).is_true()
        assert_that(e.outcome_is_unknown()).is_false()
        assert_that(e.is_safe_to_retry_with_same_key()).is_false()

    def test_an_error_without_a_status_says_nothing_about_the_key(self):
        self.server.enqueue(error(400, "SOME_ERROR"))

        e = self.fails(lambda: self.send(self.client(), "POST"))

        assert_that(e.idempotency_key_honored).is_none()
        assert_that(e.replayed).is_false()

    def test_reused_is_not_retried(self):
        self.server.enqueue(key_status(error(422, "IDEMPOTENCY_KEY_REUSED"), "reused"), status(200))

        self.fails(lambda: self.send(self.client(), "POST"))

        assert_that(self.server.request_count).is_equal_to(1)

    def test_an_invalid_key_is_not_retried(self):
        self.server.enqueue(error(400, "INVALID_IDEMPOTENCY_KEY"), status(200))

        self.fails(lambda: self.send(self.client(), "POST"))

        assert_that(self.server.request_count).is_equal_to(1)

    # guide test 14
    def test_lost_responses_count_against_max_retries(self):
        client = self.client()
        self.server.enqueue(key_status(200, "executed"))
        self.server.enqueue_times(3, LOST_RESPONSE)

        self.send(client, "POST")
        client.max_retries = 2
        e = self.fails(lambda: self.send(client, "POST"))

        assert_that(self.server.request_count).is_equal_to(1 + 3)
        assert_that(e.outcome_is_unknown()).is_true()
        assert_that(e.is_safe_to_retry_with_same_key()).is_true()
        assert_that(set(self.server.sent_idempotency_keys()[1:])).is_equal_to({e.idempotency_key})

    def test_all_kinds_of_failure_share_one_retry_count(self):
        port = free_port()
        with FakeServer() as late:
            late.enqueue(error(429, "RATE_LIMIT_EXCEEDED"),
                         key_status(error(409, "IDEMPOTENCY_KEY_IN_USE"), "in-use"),
                         LOST_RESPONSE,
                         status(200))

            def on_sleep():
                if self.clock.sleeps == 1:
                    late.start(port)

            self.clock.on_sleep = on_sleep
            client = HttpClient("http://127.0.0.1:%d" % port, "secretKey", None, 3, clock=self.clock)

            e = self.fails(lambda: client.url(BOOK, key="event1").post({}))

            assert_that(self.clock.sleeps).is_equal_to(3)
            assert_that(late.request_count).is_equal_to(3)
            assert_that(e.cause).is_not_none()
            assert_that(e.outcome_is_unknown()).is_true()
            assert_that(e.is_safe_to_retry_with_same_key()).is_true()

    # guide test 15
    def test_set_default_workspace_is_retried_after_a_lost_response(self):
        client = Client(Region(self.server.url()), "secretKey")
        client.http_client._state.clock = self.clock
        self.server.enqueue(key_status(204, "executed"), LOST_RESPONSE, key_status(204, "replayed"))

        client.workspaces.set_default("workspace1")
        client.workspaces.set_default("workspace2")

        keys = self.server.sent_idempotency_keys()
        assert_that(keys).has_size(3)
        assert_that(keys[2]).is_equal_to(keys[1])

    # guide test 16
    def test_a_request_that_was_never_sent_is_safe_to_retry_with_the_same_key(self):
        url = self.server.url()
        self.server.close()

        e = self.fails(lambda: HttpClient(url, "secretKey", None, 0, clock=self.clock).url("/").post({}))

        assert_that(e.outcome_is_unknown()).is_false()
        assert_that(e.is_safe_to_retry_with_same_key()).is_true()
        assert_that(e.idempotency_key).is_not_none()

    def test_a_get_that_was_never_sent_has_a_known_outcome(self):
        url = self.server.url()
        self.server.close()

        e = self.fails(lambda: HttpClient(url, "secretKey", None, 5, clock=self.clock).url("/").get())

        assert_that(e.outcome_is_unknown()).is_false()
        assert_that(e.is_safe_to_retry_with_same_key()).is_false()
        assert_that(self.clock.sleeps).is_equal_to(0)

    def test_a_get_with_a_lost_response_has_an_unknown_outcome(self):
        self.server.enqueue(LOST_RESPONSE)

        e = self.fails(lambda: self.send(self.client(), "GET"))

        assert_that(e.outcome_is_unknown()).is_true()

    def test_a_write_to_an_unknown_host_is_retried_with_the_same_key(self):
        e = self.fails(lambda: HttpClient("http://seatsio.invalid", "secretKey", None, 1, clock=self.clock).url("/").post({}))

        assert_that(self.clock.sleeps).is_equal_to(1)
        assert_that(e.outcome_is_unknown()).is_false()
        assert_that(e.is_safe_to_retry_with_same_key()).is_true()

    def test_a_write_that_fails_the_tls_handshake_is_retried_with_the_same_key(self):
        url = self.server.url().replace("http://", "https://")

        e = self.fails(lambda: HttpClient(url, "secretKey", None, 1, clock=self.clock).url("/").post({}))

        assert_that(e.cause).is_instance(requests.exceptions.SSLError)
        assert_that(self.clock.sleeps).is_equal_to(1)
        assert_that(e.outcome_is_unknown()).is_false()
        assert_that(e.is_safe_to_retry_with_same_key()).is_true()

    @parameterized.expand([
        ("connect timeout", requests.exceptions.ConnectTimeout(), Delivery.NEVER_SENT),
        ("read timeout", requests.exceptions.ReadTimeout(), Delivery.RESPONSE_LOST),
        ("truncated body", requests.exceptions.ChunkedEncodingError(), Delivery.RESPONSE_LOST),
        ("ssl error after the handshake", requests.exceptions.SSLError(), Delivery.RESPONSE_LOST),
        ("other connection error", requests.exceptions.ConnectionError(), Delivery.RESPONSE_LOST),
        ("invalid url", requests.exceptions.InvalidURL(), Delivery.NOT_RETRYABLE),
        ("not a requests error", ValueError(), Delivery.NOT_RETRYABLE),
    ])
    def test_failures_are_classified(self, _, cause, delivery):
        assert_that(Delivery.of(cause)).is_equal_to(delivery)

    def test_a_lost_response_is_safe_to_retry_with_the_same_key_on_a_route_that_honors_keys(self):
        client = self.client()
        self.server.enqueue(key_status(200, "executed"), LOST_RESPONSE)

        self.send(client, "POST")
        client.max_retries = 0
        e = self.fails(lambda: self.send(client, "POST"))

        assert_that(e.outcome_is_unknown()).is_true()
        assert_that(e.is_safe_to_retry_with_same_key()).is_true()

    # guide test 17
    def test_a_request_that_was_never_sent_is_not_retried_once_the_key_may_have_expired(self):
        self.server.enqueue(error(429, "RATE_LIMIT_EXCEEDED"))

        def on_sleep():
            self.server.close()
            self.clock.current += 6 * 60

        self.clock.on_sleep = on_sleep

        e = self.fails(lambda: self.send(self.client(), "POST"))

        assert_that(self.server.request_count).is_equal_to(1)
        assert_that(self.clock.sleeps).is_equal_to(1)
        assert_that(e.cause).is_not_none()
        assert_that(e.outcome_is_unknown()).is_false()

    def test_a_request_that_was_never_sent_is_retried_whatever_the_time_if_no_attempt_was_sent(self):
        url = self.server.url()
        self.server.close()

        def on_sleep():
            self.clock.current += 10 * 60

        self.clock.on_sleep = on_sleep

        self.fails(lambda: HttpClient(url, "secretKey", None, 3, clock=self.clock).url("/").post({}))

        assert_that(self.clock.sleeps).is_equal_to(3)

    def test_lost_responses_are_not_retried_once_the_key_may_have_expired(self):
        client = self.client()
        self.server.enqueue(key_status(200, "executed"))
        self.server.enqueue_times(4, LOST_RESPONSE)

        def on_sleep():
            self.clock.current += 2 * 60

        self.clock.on_sleep = on_sleep

        self.send(client, "POST")
        e = self.fails(lambda: self.send(client, "POST"))

        assert_that(self.server.request_count).is_equal_to(1 + 4)
        assert_that(e.outcome_is_unknown()).is_true()
        assert_that(e.is_safe_to_retry_with_same_key()).is_false()

    def test_retries_on_429_stop_once_the_key_may_have_expired(self):
        self.server.enqueue_times(2, error(429, "RATE_LIMIT_EXCEEDED"))

        def on_sleep():
            self.clock.current += 6 * 60

        self.clock.on_sleep = on_sleep

        with self.assertRaises(RateLimitExceededException):
            self.send(self.client(), "POST")

        assert_that(self.server.request_count).is_equal_to(2)

    def test_gets_are_not_retried_after_a_lost_response(self):
        self.server.enqueue(LOST_RESPONSE, status(200))

        e = self.fails(lambda: self.send(self.client(), "GET"))

        assert_that(self.server.request_count).is_equal_to(1)
        assert_that(e.idempotency_key).is_none()
        assert_that(e.is_safe_to_retry_with_same_key()).is_false()

    def test_gets_are_retried_on_429(self):
        self.server.enqueue(error(429, "RATE_LIMIT_EXCEEDED"), json_reply(200, "{}"))

        self.send(self.client(), "GET")

        assert_that(self.server.request_count).is_equal_to(2)
        assert_that(self.server.sent_idempotency_keys()).is_equal_to([None, None])

    def test_request_construction_errors_are_not_retried(self):
        self.fails(lambda: HttpClient("unknownProtocol://", "secretKey", None, 5, clock=self.clock).url("/x").post({}))

        assert_that(self.clock.sleeps).is_equal_to(0)

    def test_writes_are_retried_on_429_with_the_same_key(self):
        self.server.enqueue(error(429, "RATE_LIMIT_EXCEEDED"), status(200))

        self.send(self.client(), "POST")

        keys = self.server.sent_idempotency_keys()
        assert_that(keys).has_size(2)
        assert_that(keys[1]).is_equal_to(keys[0])

    def test_writes_are_retried_on_key_in_use_with_the_same_key(self):
        self.server.enqueue(error(409, "IDEMPOTENCY_KEY_IN_USE"), status(200))

        self.send(self.client(), "POST")

        keys = self.server.sent_idempotency_keys()
        assert_that(keys).has_size(2)
        assert_that(keys[1]).is_equal_to(keys[0])

    def test_caller_key_survives_a_retry(self):
        key = str(uuid.uuid4())
        self.server.enqueue(error(409, "IDEMPOTENCY_KEY_IN_USE"), status(200))

        self.send(self.client().with_idempotency_key(key), "POST")

        assert_that(self.server.sent_idempotency_keys()).is_equal_to([key, key])

    def test_key_in_use_error_is_thrown_when_retries_run_out(self):
        self.server.enqueue_times(3, error(409, "IDEMPOTENCY_KEY_IN_USE"))
        client = self.client()
        client.max_retries = 2

        e = self.fails(lambda: self.send(client, "POST"))

        assert_that(self.server.request_count).is_equal_to(3)
        assert_that(e.errors[0]["code"]).is_equal_to("IDEMPOTENCY_KEY_IN_USE")
        assert_that(set(self.server.sent_idempotency_keys())).is_equal_to({e.idempotency_key})

    @parameterized.expand([
        ('{"errors": [{"code": "SOME_OTHER_CONFLICT", "message": "conflict"}]}',),
        ('{"errors": []}',),
        ('{}',),
        ('null',),
        ('[]',),
        ('not json',),
        ('',),
    ])
    def test_other_conflicts_are_not_retried(self, body):
        self.server.enqueue(json_reply(409, body), status(200))

        e = self.fails(lambda: self.send(self.client(), "POST"))

        assert_that(self.server.request_count).is_equal_to(1)
        assert_that(e.idempotency_key).is_not_none()

    def test_a_keyboard_interrupt_stops_the_retries(self):
        self.server.enqueue(error(429, "RATE_LIMIT_EXCEEDED"), status(200))

        def on_sleep():
            raise KeyboardInterrupt()

        self.clock.on_sleep = on_sleep

        with self.assertRaises(KeyboardInterrupt):
            self.send(self.client(), "POST")

        assert_that(self.server.request_count).is_equal_to(1)

    def test_headers_are_sent_once_per_attempt(self):
        self.server.enqueue(error(429, "RATE_LIMIT_EXCEEDED"), status(200))

        self.send(self.client(), "POST")

        assert_that(self.server.request_count).is_equal_to(2)
        for request in self.server.requests:
            assert_that(request.header_values("X-Client-Lib")).has_size(1)
            assert_that(request.header_values("Authorization")).has_size(1)
            assert_that(request.header_values("Idempotency-Key")).has_size(1)

    def test_max_retries_is_shared_with_clients_that_have_a_key(self):
        self.server.enqueue_times(3, error(429, "RATE_LIMIT_EXCEEDED"))
        client = Client(Region(self.server.url()), "secretKey")
        client.http_client._state.clock = self.clock
        copy = client.with_idempotency_key(str(uuid.uuid4()))

        client.http_client.max_retries = 2
        with self.assertRaises(RateLimitExceededException):
            copy.events.update("anEvent", event_key="anotherEvent")

        assert_that(self.server.request_count).is_equal_to(3)

    def test_max_retries_0_gives_one_attempt_for_every_kind_of_failure(self):
        client = self.client()
        self.server.enqueue(key_status(200, "executed"))
        self.send(client, "POST")
        client.max_retries = 0

        self.server.enqueue(error(429, "RATE_LIMIT_EXCEEDED"))
        self.fails(lambda: self.send(client, "POST"))
        self.server.enqueue(error(409, "IDEMPOTENCY_KEY_IN_USE"))
        self.fails(lambda: self.send(client, "POST"))
        self.server.enqueue(LOST_RESPONSE)
        self.fails(lambda: self.send(client, "POST"))
        self.server.close()
        self.fails(lambda: client.url("/").post({}))

        assert_that(self.server.request_count).is_equal_to(1 + 3)
        assert_that(self.clock.sleeps).is_equal_to(0)

    @parameterized.expand([(500,), (502,), (503,)])
    def test_outcome_is_unknown_after_a_5xx(self, code):
        self.server.enqueue(error(code, "SOME_ERROR"))

        e = self.fails(lambda: self.send(self.client(), "POST"))

        assert_that(e.outcome_is_unknown()).is_true()
        assert_that(e.is_safe_to_retry_with_same_key()).is_false()

    def test_a_5xx_is_safe_to_retry_with_the_same_key_when_the_key_was_honored(self):
        self.server.enqueue(key_status(error(500, "SOME_ERROR"), "executed"))

        e = self.fails(lambda: self.send(self.client(), "POST"))

        assert_that(e.idempotency_key_honored).is_true()
        assert_that(e.is_safe_to_retry_with_same_key()).is_true()

    def test_a_5xx_without_a_status_is_safe_to_retry_with_the_same_key_on_a_route_that_honors_keys(self):
        client = self.client()
        self.server.enqueue(key_status(200, "executed"), error(502, "BAD_GATEWAY"))

        self.send(client, "POST")
        e = self.fails(lambda: self.send(client, "POST"))

        assert_that(e.idempotency_key_honored).is_none()
        assert_that(e.is_safe_to_retry_with_same_key()).is_true()

    def test_a_5xx_is_not_safe_to_retry_with_the_same_key_when_the_key_was_ignored(self):
        self.server.enqueue(key_status(error(500, "SOME_ERROR"), "ignored"))

        e = self.fails(lambda: self.send(self.client(), "POST"))

        assert_that(e.idempotency_key_honored).is_false()
        assert_that(e.is_safe_to_retry_with_same_key()).is_false()

    def test_outcome_is_unknown_when_the_key_is_still_in_use_after_all_retries(self):
        self.server.enqueue(key_status(error(409, "IDEMPOTENCY_KEY_IN_USE"), "in-use"))
        client = self.client()
        client.max_retries = 0

        e = self.fails(lambda: self.send(client, "POST"))

        assert_that(e.outcome_is_unknown()).is_true()
        assert_that(e.is_safe_to_retry_with_same_key()).is_true()

    @parameterized.expand([(400,), (404,), (409,), (422,)])
    def test_outcome_is_known_after_a_4xx(self, code):
        self.server.enqueue(key_status(error(code, "SOME_ERROR"), "executed"))

        e = self.fails(lambda: self.send(self.client(), "POST"))

        assert_that(e.outcome_is_unknown()).is_false()
        assert_that(e.is_safe_to_retry_with_same_key()).is_false()

    def test_an_operation_with_unknown_outcome_can_be_retried_with_the_key_of_the_exception(self):
        self.server.enqueue(key_status(error(500, "SOME_ERROR"), "executed"), json_reply(200, "{}"))
        client = Client(Region(self.server.url()), "secretKey")

        e = self.fails(lambda: client.events.update("anEvent", event_key="anotherEvent"))

        assert_that(e.is_safe_to_retry_with_same_key()).is_true()
        client.with_idempotency_key(e.idempotency_key).events.update("anEvent", event_key="anotherEvent")

        assert_that(self.server.sent_idempotency_keys()).is_equal_to([e.idempotency_key, e.idempotency_key])

    def client(self):
        return HttpClient(self.server.url(), "secretKey", None, 5, clock=self.clock)

    def send(self, client, method):
        resource = client.url("/")
        if method == "GET":
            return resource.get()
        return getattr(resource, method.lower())({})

    def fails(self, call):
        with self.assertRaises(SeatsioException) as context:
            call()
        return context.exception
