import time

from seatsio.exceptions import SeatsioException, RateLimitExceededException
from seatsio.httpClient import HttpClient
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ExponentialBackoffTest(SeatsioClientTest):

    def test_aborts_eventually_if_server_keeps_returning_429_get(self):
        start = time.time()
        try:
            client = HttpClient("https://mockbin.org", "aSecretKey", None, 5)
            client.url("/bin/0381d6f4-0155-4b8c-937b-73d3d88b2a3f").get()
            raise Exception("Should have failed")
        except RateLimitExceededException as e:
            assert_that(e.errors[0]['code']).is_equal_to("RATE_LIMIT_EXCEEDED")
            wait_time = int(time.time() - start)
            assert_that(wait_time).is_between(10, 20)

    def test_aborts_eventually_if_server_keeps_returning_429_post(self):
        start = time.time()
        try:
            client = HttpClient("https://mockbin.org", "aSecretKey", None, 5)
            client.url("/bin/0381d6f4-0155-4b8c-937b-73d3d88b2a3f").post()
            raise Exception("Should have failed")
        except RateLimitExceededException as e:
            assert_that(e.errors[0]['code']).is_equal_to("RATE_LIMIT_EXCEEDED")
            wait_time = int(time.time() - start)
            assert_that(wait_time).is_between(10, 20)

    def test_aborts_eventually_if_server_keeps_returning_429_delete(self):
        start = time.time()
        try:
            client = HttpClient("https://mockbin.org", "aSecretKey", None, 5)
            client.url("/bin/0381d6f4-0155-4b8c-937b-73d3d88b2a3f").delete()
            raise Exception("Should have failed")
        except RateLimitExceededException as e:
            assert_that(e.errors[0]['code']).is_equal_to("RATE_LIMIT_EXCEEDED")
            wait_time = int(time.time() - start)
            assert_that(wait_time).is_between(10, 20)

    def test_aborts_directly_if_server_returns_other_error_than_429(self):
        start = time.time()
        try:
            client = HttpClient("https://mockbin.org", "aSecretKey", None, 5)
            client.url("/bin/1eea3aab-2bb2-4f92-99c2-50d942fb6294").get()
            raise Exception("Should have failed")
        except SeatsioException as e:
            assert_that(e.message).is_equal_to("Error while executing GET https://mockbin.org/bin/1eea3aab-2bb2-4f92-99c2-50d942fb6294")
            wait_time = int(time.time() - start)
            assert_that(wait_time).is_between(0, 2)

    def test_aborts_directly_if_server_returns_429_but_max_retries_0(self):
        start = time.time()
        try:
            client = HttpClient("https://mockbin.org", "aSecretKey", None, 0)
            client.url("/bin/0381d6f4-0155-4b8c-937b-73d3d88b2a3f").get()
            raise Exception("Should have failed")
        except RateLimitExceededException as e:
            assert_that(e.errors[0]['code']).is_equal_to("RATE_LIMIT_EXCEEDED")
            wait_time = int(time.time() - start)
            assert_that(wait_time).is_between(0, 2)

    def test_returns_successfully_when_server_sends_429_and_then_successful_response(self):
        client = HttpClient("https://httpbin.org", "aSecretKey", None, 5)

        i = 0
        while i < 20:
            client.url("/status/429:0.25,204:0.75").post()
            i += 1
