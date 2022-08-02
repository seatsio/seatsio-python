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
            expected_msg = "GET " + self.client.base_url + "/charts/unexistingChart "
            expected_msg += "resulted in a 404 Not Found response. "
            expected_msg += "Reason: Chart not found: unexistingChart. Request ID:"
            assert_that(e.message).contains(expected_msg)
            assert_that(e.errors).has_size(1).is_equal_to([{
                "code": "CHART_NOT_FOUND",
                "message": "Chart not found: unexistingChart"
            }])
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
