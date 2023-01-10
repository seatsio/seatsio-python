import time

from seatsio.exceptions import SeatsioException, RateLimitExceededException
from seatsio.httpClient import HttpClient
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ExponentialBackoffTest(SeatsioClientTest):

    def test_aborts_eventually_if_server_keeps_returning_429_get(self):
        start = time.time()
        try:
            client = HttpClient("https://httpbin.seatsio.net", "aSecretKey", None, 5)
            client.url("/status/429").get()
            raise Exception("Should have failed")
        except RateLimitExceededException as e:
            assert_that(e.message).is_equal_to("Error while executing GET https://httpbin.seatsio.net/status/429")
            wait_time = int(time.time() - start)
            assert_that(wait_time).is_between(10, 20)

    def test_aborts_eventually_if_server_keeps_returning_429_post(self):
        start = time.time()
        try:
            client = HttpClient("https://httpbin.seatsio.net", "aSecretKey", None, 5)
            client.url("/status/429").post()
            raise Exception("Should have failed")
        except RateLimitExceededException as e:
            assert_that(e.message).is_equal_to("Error while executing POST https://httpbin.seatsio.net/status/429")
            wait_time = int(time.time() - start)
            assert_that(wait_time).is_between(10, 20)

    def test_aborts_eventually_if_server_keeps_returning_429_delete(self):
        start = time.time()
        try:
            client = HttpClient("https://httpbin.seatsio.net", "aSecretKey", None, 5)
            client.url("/status/429").delete()
            raise Exception("Should have failed")
        except RateLimitExceededException as e:
            assert_that(e.message).is_equal_to("Error while executing DELETE https://httpbin.seatsio.net/status/429")
            wait_time = int(time.time() - start)
            assert_that(wait_time).is_between(10, 20)

    def test_aborts_directly_if_server_returns_other_error_than_429(self):
        start = time.time()
        try:
            client = HttpClient("https://httpbin.seatsio.net", "aSecretKey", None, 5)
            client.url("/status/400").get()
            raise Exception("Should have failed")
        except SeatsioException as e:
            assert_that(e.message).is_equal_to("Error while executing GET https://httpbin.seatsio.net/status/400")
            wait_time = int(time.time() - start)
            assert_that(wait_time).is_between(0, 5)

    def test_aborts_directly_if_server_returns_429_but_max_retries_0(self):
        start = time.time()
        try:
            client = HttpClient("https://httpbin.seatsio.net", "aSecretKey", None, 0)
            client.url("/status/429").get()
            raise Exception("Should have failed")
        except RateLimitExceededException as e:
            assert_that(e.message).is_equal_to("Error while executing GET https://httpbin.seatsio.net/status/429")
            wait_time = int(time.time() - start)
            assert_that(wait_time).is_between(0, 5)

    def test_returns_successfully_when_server_sends_429_and_then_successful_response(self):
        client = HttpClient("https://httpbin.seatsio.net", "aSecretKey", None, 5)

        i = 0
        while i < 20:
            client.url("/status/429:0.25,204:0.75").post()
            i += 1
