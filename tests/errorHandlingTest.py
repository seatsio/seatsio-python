from seatsio.exceptions import SeatsioException
from tests.asserts import assertThat
from tests.helpers import SeatsioClientTest


class ErrorHandlingTest(SeatsioClientTest):

    def test_400(self):
        try:
            self.client.charts().retrieve("unexistingChart")
            self.fail("expected exception")
        except SeatsioException as e:
            # assertThat(e.message).contains("GET " + self.client.baseUrl + "/charts/unexistingChart resulted in a 404 Not Found response. Reason: Chart not found: unexistingChart. Request ID:")
            assertThat(e.messages).hasSize(1).isEqualTo(["Chart not found: unexistingChart"])
            assertThat(e.requestId).isNotNone()