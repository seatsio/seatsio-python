import contextlib
import unittest
import unittest.mock
import uuid
import requests

from seatsio import Client, Region
from seatsio.exceptions import SeatsioException, RateLimitExceededException
from seatsio.httpClient import HttpClient
from tests.httpbin import httpbin_url
from tests.util.asserts import assert_that


class IdempotencyKeyTest(unittest.TestCase):

    def test_posts_get_an_idempotency_key(self):
        client = HttpClient(httpbin_url(), "secretKey", None, 5)
        response = client.url("/anything").post("{}")
        key = self.sent_idempotency_key(response)

        assert_that(uuid.UUID(key).version).is_equal_to(4)

    def test_deletes_get_an_idempotency_key(self):
        client = HttpClient(httpbin_url(), "secretKey", None, 5)
        response = client.url("/anything").delete()
        key = self.sent_idempotency_key(response)

        assert_that(uuid.UUID(key).version).is_equal_to(4)

    def test_puts_get_an_idempotency_key(self):
        client = HttpClient(httpbin_url(), "secretKey", None, 5)
        response = client.url("/anything").put("{}")
        key = self.sent_idempotency_key(response)

        assert_that(uuid.UUID(key).version).is_equal_to(4)

    def test_gets_do_not_get_an_idempotency_key(self):
        client = HttpClient(httpbin_url(), "secretKey", None, 5)
        response = client.url("/anything").get()

        assert_that("Idempotency-Key" in response.get("headers", {})).is_false()

    def test_each_request_gets_its_own_key(self):
        client = HttpClient(httpbin_url(), "secretKey", None, 5)

        first = self.sent_idempotency_key(client.url("/anything").post("{}"))
        second = self.sent_idempotency_key(client.url("/anything").post("{}"))

        assert_that(first).is_not_equal_to(second)

    def test_failed_requests_expose_their_idempotency_key(self):
        with self.spy_on_post() as sent_keys:
            try:
                HttpClient(httpbin_url(), "secretKey", None, 5).url("/status/500").post("{}")
                self.fail("expected exception")
            except SeatsioException as e:
                assert_that(sent_keys).has_size(1)
                assert_that(e.idempotency_key).is_equal_to(sent_keys[0])
                assert_that(e.idempotencyKey).is_equal_to(sent_keys[0])

    def test_connection_failures_expose_their_idempotency_key(self):
        with self.spy_on_post() as sent_keys:
            try:
                HttpClient("http://localhost:1", "secretKey", None, 5).url("/anything").post("{}")
                self.fail("expected exception")
            except SeatsioException as e:
                assert_that(sent_keys).has_size(1)
                assert_that(e.idempotency_key).is_equal_to(sent_keys[0])
                assert_that(e.idempotencyKey).is_equal_to(sent_keys[0])

    def test_rejects_idempotency_keys_that_are_not_v4_uuids(self):
        for key in ["", "not-a-uuid", str(uuid.uuid1()), uuid.uuid4(), None]:
            with self.assertRaises(ValueError):
                HttpClient(httpbin_url(), "secretKey", None, 5).with_idempotency_key(key)
            with self.assertRaises(ValueError):
                Client(Region(httpbin_url()), "secretKey").with_idempotency_key(key)

    def test_accepts_uppercase_v4_uuids(self):
        key = str(uuid.uuid4()).upper()
        client = HttpClient(httpbin_url(), "secretKey", None, 5).with_idempotency_key(key)

        assert_that(self.sent_idempotency_key(client.url("/anything").post("{}"))).is_equal_to(key)

    def test_retries_409_idempotency_key_in_use_with_the_same_key(self):
        responses = [self.json_response(409, "IDEMPOTENCY_KEY_IN_USE"), self.json_response(200)]
        with unittest.mock.patch("requests.post", side_effect=responses) as post, \
                unittest.mock.patch("time.sleep"):
            response = HttpClient(httpbin_url(), "secretKey", None, 5).url("/anything").post("{}")

        assert_that(response.status_code).is_equal_to(200)
        assert_that(post.call_count).is_equal_to(2)
        keys = [call.kwargs["headers"]["Idempotency-Key"] for call in post.call_args_list]
        assert_that(keys[0]).is_equal_to(keys[1])

    def test_does_not_retry_other_409s(self):
        responses = [self.json_response(409, "SOMETHING_ELSE"), self.json_response(200)]
        with unittest.mock.patch("requests.post", side_effect=responses) as post, \
                unittest.mock.patch("time.sleep"):
            with self.assertRaises(SeatsioException):
                HttpClient(httpbin_url(), "secretKey", None, 5).url("/anything").post("{}")

        assert_that(post.call_count).is_equal_to(1)

    def test_a_client_can_retry_with_the_same_idempotency_key(self):
        key = str(uuid.uuid4())
        client = HttpClient(httpbin_url(), "secretKey", None, 5).with_idempotency_key(key)

        assert_that(self.sent_idempotency_key(client.url("/anything").post("{}"))).is_equal_to(key)
        assert_that(self.sent_idempotency_key(client.url("/anything").post("{}"))).is_equal_to(key)

    def test_seatsio_client_can_retry_with_the_same_idempotency_key(self):
        key = str(uuid.uuid4())
        client = Client(Region(httpbin_url()), "secretKey").with_idempotency_key(key)

        res1 = client.http_client.url("/anything").post("{}")
        res2 = client.http_client.url("/anything").post("{}")

        assert_that(self.sent_idempotency_key(res1)).is_equal_to(key)
        assert_that(self.sent_idempotency_key(res2)).is_equal_to(key)

    def test_seatsio_client_can_retry_with_the_same_idempotency_key_camel_case(self):
        key = str(uuid.uuid4())
        client = Client(Region(httpbin_url()), "secretKey").withIdempotencyKey(key)

        res = client.http_client.url("/anything").post("{}")
        assert_that(self.sent_idempotency_key(res)).is_equal_to(key)

    def test_retries_reuse_same_idempotency_key(self):
        captured_keys = []
        original_post = requests.post

        def mock_post(*args, **kwargs):
            headers = kwargs.get("headers", {})
            if "Idempotency-Key" in headers:
                captured_keys.append(headers["Idempotency-Key"])
            return original_post(*args, **kwargs)

        with unittest.mock.patch("requests.post", side_effect=mock_post):
            try:
                HttpClient(httpbin_url(), "secretKey", None, 2, timeout=5).url("/status/429").post("{}")
            except RateLimitExceededException:
                pass

        assert len(captured_keys) > 1
        assert_that(set(captured_keys)).has_size(1)
        assert_that(uuid.UUID(captured_keys[0]).version).is_equal_to(4)

    @staticmethod
    @contextlib.contextmanager
    def spy_on_post():
        sent_keys = []
        original_post = requests.post

        def spy(*args, **kwargs):
            sent_keys.append(kwargs.get("headers", {}).get("Idempotency-Key"))
            return original_post(*args, **kwargs)

        with unittest.mock.patch("requests.post", side_effect=spy):
            yield sent_keys

    @staticmethod
    def json_response(status_code, error_code=None):
        response = unittest.mock.Mock()
        response.status_code = status_code
        response.headers = {"content-type": "application/json"}
        errors = [{"code": error_code, "message": error_code}] if error_code else []
        response.json.return_value = {"errors": errors, "requestId": "123"}
        return response

    @staticmethod
    def sent_idempotency_key(response):
        data = response.json() if hasattr(response, "json") else response
        header = data.get("headers", {}).get("Idempotency-Key")
        # httpbingo returns header values as arrays, httpbin as strings
        return header[0] if isinstance(header, list) else header
