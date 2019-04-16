from seatsio.exceptions import SeatsioException
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ValidateChartTest(SeatsioClientTest):

    def test_validate_published_chart(self):
        chart_key = self.create_test_chart_with_errors()
        validation = self.client.charts.validate_published_version(chart_key)

        assert_that(validation.errors).contains_exactly(
            "VALIDATE_DUPLICATE_LABELS",
            "VALIDATE_UNLABELED_OBJECTS",
            "VALIDATE_OBJECTS_WITHOUT_CATEGORIES"
        )

    def test_validate_draft_chart(self):
        with self.assertRaises(SeatsioException):
            chart_key = self.create_test_chart_with_errors()
            self.client.events.create(chart_key)
            self.client.charts.update(chart_key, "New name")
            self.client.charts.validate_draft_version(chart_key)
