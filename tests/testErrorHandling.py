import seatsio
from seatsio import Region
from seatsio.exceptions import SeatsioException
from tests.util.asserts import assert_that
from tests.seatsioClientTest import SeatsioClientTest


class ErrorHandlingTest(SeatsioClientTest):

    def test_400(self):
        try:
            self.client.charts.retrieve("unexistingChart")
            self.fail("expected exception")
        except SeatsioException as e:
            assert_that(e.message).contains("Chart not found: unexistingChart was not found in workspace")
            assert_that(e.errors).has_size(1)
            assert_that(e.errors[0]['code']).is_equal_to("CHART_NOT_FOUND")
            assert_that(e.errors[0]['message']).contains("Chart not found: unexistingChart was not found in workspace")
            assert_that(e.requestId).is_not_none()

    def test_weird_error(self):
        try:
            seatsio.Client(Region("unknownProtocol://"), "").charts.retrieve("unexistingChart")
            self.fail("expected exception")
        except SeatsioException as e:
            assert_that(e.message).contains("Error while executing GET unknownProtocol:///charts/unexistingChart")
            assert_that(e.errors).is_none()
            assert_that(e.requestId).is_none()
            assert_that(e.cause).is_not_none()

    def test_timeout_raises_seatsio_exception(self):
        from seatsio.httpClient import HttpClient
        try:
            client = HttpClient("https://httpbin.seatsio.net", "aSecretKey", None, 0, timeout=0.1)
            client.url("/delay/1").get()
            self.fail("expected exception")
        except SeatsioException as e:
            assert_that(e.message).is_equal_to("Error while executing GET https://httpbin.seatsio.net/delay/1")
            assert_that(e.cause).is_not_none()
