from seatsio.domain import ObjectStatus
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ChangeBestAvailableObjectStatusTest(SeatsioClientTest):

    def test_number(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        result = self.client.events.change_best_available_object_status(event.key, 3, "myStatus")
        assert_that(result.next_to_each_other).is_true()
        assert_that(result.objects).contains_exactly("B-4", "B-5", "B-6")

    def test_categories(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        result = self.client.events.change_best_available_object_status(event.key, 3, "myStatus", categories=["cat2"])
        assert_that(result.objects).contains_exactly("C-4", "C-5", "C-6")

    def test_extra_data(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        d1 = {"key1": "value1"}
        d2 = {"key2": "value2"}
        extra_data = [d1, d2]
        result = self.client.events.change_best_available_object_status(
            event_key=event.key,
            number=2,
            status="mystatus",
            extra_data=extra_data
        )
        assert_that(result.objects).contains_exactly("B-4", "B-5")
        assert_that(self.client.events.retrieve_object_status(event.key, "B-4").extra_data).is_equal_to(d1)
        assert_that(self.client.events.retrieve_object_status(event.key, "B-5").extra_data).is_equal_to(d2)

    def test_hold_token(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()

        best_available_objects = self.client.events.change_best_available_object_status(
            event_key=event.key,
            number=1,
            status=ObjectStatus.HELD,
            hold_token=hold_token.hold_token
        )

        object_status = self.client.events.retrieve_object_status(event.key, best_available_objects.objects[0])
        assert_that(object_status.status).is_equal_to(ObjectStatus.HELD)
        assert_that(object_status.hold_token).is_equal_to(hold_token.hold_token)

    def test_order_id(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        best_available_objects = self.client.events.change_best_available_object_status(
            event.key, number=1,
            status="mystatus",
            order_id="anOrder"
        )
        object_status = self.client.events.retrieve_object_status(event.key, best_available_objects.objects[0])
        assert_that(object_status.order_id).is_equal_to("anOrder")

    def test_book_best_available(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        best_available_objects = self.client.events.book_best_available(event.key, number=3)

        assert_that(best_available_objects.next_to_each_other).is_true()
        assert_that(best_available_objects.objects).contains_exactly("B-4", 'B-5', 'B-6')

    def test_hold_best_available(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()

        best_available_objects = self.client.events.hold_best_available(event.key, 1, hold_token=hold_token.hold_token)

        object_status = self.client.events.retrieve_object_status(event.key, best_available_objects.objects[0])
        assert_that(object_status.status).is_equal_to(ObjectStatus.HELD)
        assert_that(object_status.hold_token).is_equal_to(hold_token.hold_token)
