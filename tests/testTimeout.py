import unittest
from unittest.mock import patch, MagicMock

import seatsio
from seatsio.httpClient import HttpClient
from tests.util.asserts import assert_that


def ok_response():
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {}
    return response


class TimeoutTest(unittest.TestCase):

    def test_default_timeout(self):
        with patch("seatsio.httpClient.requests.get", return_value=ok_response()) as get:
            HttpClient("http://localhost", "aSecretKey", None, 5).url("/ping").get()
            assert_that(get.call_args.kwargs["timeout"]).is_equal_to((10, 30))

    def test_client_default_timeout(self):
        with patch("seatsio.httpClient.requests.get", return_value=ok_response()) as get:
            seatsio.Client(seatsio.Region.EU(), "aSecretKey").http_client.url("/ping").get()
            assert_that(get.call_args.kwargs["timeout"]).is_equal_to((10, 30))

    def test_client_custom_timeout(self):
        with patch("seatsio.httpClient.requests.get", return_value=ok_response()) as get:
            seatsio.Client(seatsio.Region.EU(), "aSecretKey", timeout=(5, 60)).http_client.url("/ping").get()
            assert_that(get.call_args.kwargs["timeout"]).is_equal_to((5, 60))

    def test_client_custom_timeout_applies_to_post(self):
        with patch("seatsio.httpClient.requests.post", return_value=ok_response()) as post:
            seatsio.Client(seatsio.Region.EU(), "aSecretKey", timeout=45).http_client.url("/ping").post()
            assert_that(post.call_args.kwargs["timeout"]).is_equal_to(45)
