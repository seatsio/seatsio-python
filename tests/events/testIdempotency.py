import uuid

import requests

from seatsio import Client, Region
from seatsio.exceptions import SeatsioException
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that
from tests.util.fakeServer import FakeServer, Reply, LOST_RESPONSE


class IdempotencyTest(SeatsioClientTest):

    def test_same_key_replays_the_response(self):
        self.use_test_company_with_idempotency_enabled()
        chart_key = self.create_test_chart()
        client_with_key = self.client.with_idempotency_key(str(uuid.uuid4()))

        first = client_with_key.events.create(chart_key)
        second = client_with_key.events.create(chart_key)

        assert_that(second.id).is_equal_to(first.id)
        assert_that(second.key).is_equal_to(first.key)

    def test_same_key_with_a_different_request_is_rejected(self):
        self.use_test_company_with_idempotency_enabled()
        chart_key = self.create_test_chart()
        client_with_key = self.client.with_idempotency_key(str(uuid.uuid4()))
        client_with_key.events.create(chart_key)

        with self.assertRaises(SeatsioException) as context:
            client_with_key.events.create(chart_key, event_key="anotherEvent")

        assert_that(context.exception.errors[0]["code"]).is_equal_to("IDEMPOTENCY_KEY_REUSED")
        assert_that(context.exception.idempotency_key_honored).is_true()
        assert_that(context.exception.is_safe_to_retry_with_same_key()).is_false()

    def test_key_is_ignored_when_idempotency_is_not_enabled_for_the_company(self):
        chart_key = self.create_test_chart()
        client_with_key = self.client.with_idempotency_key(str(uuid.uuid4()))

        first = client_with_key.events.create(chart_key)
        second = client_with_key.events.create(chart_key)

        assert_that(second.id).is_not_equal_to(first.id)

    def test_supplied_key_is_available_on_a_failed_request(self):
        self.use_test_company_with_idempotency_enabled()
        key = str(uuid.uuid4())

        with self.assertRaises(SeatsioException) as context:
            self.client.with_idempotency_key(key).events.create("unknownChart")

        assert_that(context.exception.idempotency_key).is_equal_to(key)

    def test_generated_key_is_available_on_a_failed_request(self):
        self.use_test_company_with_idempotency_enabled()

        with self.assertRaises(SeatsioException) as context:
            self.client.events.create("unknownChart")

        assert_that(uuid.UUID(context.exception.idempotency_key).version).is_equal_to(4)

    def test_retry_after_a_lost_response_creates_one_event(self):
        self.use_test_company_with_idempotency_enabled()
        chart_key = self.create_test_chart()
        with FakeServer() as proxy:
            proxy.dispatcher = self.forwarding_but_dropping_the_response_of_request(2)
            proxy.start()
            client_via_proxy = Client(Region(proxy.url()), self.user["secretKey"])

            first = client_via_proxy.events.create(chart_key)  # the client learns that the route honors keys
            second = client_via_proxy.events.create(chart_key)  # response lost, retried with the same key, replayed

            assert_that(proxy.request_count).is_equal_to(3)
            assert_that(sorted(e.id for e in self.client.events.list())).is_equal_to(sorted([first.id, second.id]))

    def forwarding_but_dropping_the_response_of_request(self, request_to_drop):
        forwarded = [0]

        def dispatch(request):
            headers = {name: value for (name, value) in request.headers
                       if name.lower() not in ("host", "content-length")}
            response = requests.request(request.method, self.base_url() + request.target, headers=headers,
                                        data=request.body)
            forwarded[0] += 1
            if forwarded[0] == request_to_drop:
                return LOST_RESPONSE
            reply_headers = {name: response.headers[name] for name in ("Content-Type", "Idempotency-Key-Status")
                             if response.headers.get(name)}
            return Reply(response.status_code, reply_headers, response.content)

        return dispatch
