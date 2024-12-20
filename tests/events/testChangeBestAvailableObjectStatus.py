from seatsio.domain import EventObjectInfo, Channel
from seatsio.exceptions import BestAvailableObjectsNotFoundException, SeatsioException
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ChangeBestAvailableObjectStatusTest(SeatsioClientTest):

    def test_number(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        result = self.client.events.change_best_available_object_status(event.key, 3, "myStatus")
        assert_that(result.next_to_each_other).is_true()
        assert_that(result.objects).contains_exactly("A-4", "A-5", "A-6")

    def test_objectDetails(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        result = self.client.events.change_best_available_object_status(event.key, 1, "myStatus")
        assert_that(list(result.objectDetails)).contains_exactly_in_any_order("A-5")
        object = result.objectDetails["A-5"]
        assert_that(object.status).is_equal_to("myStatus")
        assert_that(object.label).is_equal_to("A-5")
        assert_that(object.labels).is_equal_to({"own": {"label": "5", "type": "seat"}, "parent": {"label": "A", "type": "row"}})
        assert_that(object.ids).is_equal_to({"own": "5", "parent": "A"})
        assert_that(object.category_label).is_equal_to("Cat1")
        assert_that(object.category_key).is_equal_to("9")
        assert_that(object.ticket_type).is_none()
        assert_that(object.order_id).is_none()
        assert_that(object.object_type).is_equal_to("seat")
        assert_that(object.for_sale).is_true()
        assert_that(object.section).is_none()
        assert_that(object.entrance).is_none()
        assert_that(object.num_booked).is_none()
        assert_that(object.capacity).is_none()
        assert_that(object.left_neighbour).is_equal_to("A-4")
        assert_that(object.right_neighbour).is_equal_to("A-6")

    def test_categories(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        result = self.client.events.change_best_available_object_status(event.key, 3, "myStatus", categories=["cat2"])
        assert_that(result.objects).contains_exactly("C-4", "C-5", "C-6")

    def test_zone(self):
        chart_key = self.create_test_chart_with_zones()
        event = self.client.events.create(chart_key)

        result_midtrack = self.client.events.change_best_available_object_status(event.key, 1, "myStatus", zone="midtrack")
        assert_that(result_midtrack.objects).contains_exactly("MT3-A-139")

        result_finishline = self.client.events.change_best_available_object_status(event.key, 1, "myStatus", zone="finishline")
        assert_that(result_finishline.objects).contains_exactly("Goal Stand 4-A-1")

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
        assert_that(result.objects).contains_exactly("A-4", "A-5")
        assert_that(self.client.events.retrieve_object_info(event.key, "A-4").extra_data).is_equal_to(d1)
        assert_that(self.client.events.retrieve_object_info(event.key, "A-5").extra_data).is_equal_to(d2)

    def test_do_not_try_to_prevent_orphan_seats(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.book(event.key, ["A-4", "A-5"])

        result = self.client.events.change_best_available_object_status(
            event_key=event.key,
            number=2,
            status="mystatus",
            try_to_prevent_orphan_seats=False
        )
        assert_that(result.objects).contains_exactly("A-2", "A-3")

    def test_ticket_types(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        result = self.client.events.change_best_available_object_status(
            event_key=event.key,
            number=2,
            status="mystatus",
            ticket_types=["adult", "child"]
        )
        assert_that(result.objects).contains_exactly("A-4", "A-5")
        assert_that(self.client.events.retrieve_object_info(event.key, "A-4").ticket_type).is_equal_to("adult")
        assert_that(self.client.events.retrieve_object_info(event.key, "A-5").ticket_type).is_equal_to("child")

    def test_hold_token(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()

        best_available_objects = self.client.events.change_best_available_object_status(
            event_key=event.key,
            number=1,
            status=EventObjectInfo.HELD,
            hold_token=hold_token.hold_token
        )

        object_status = self.client.events.retrieve_object_info(event.key, best_available_objects.objects[0])
        assert_that(object_status.status).is_equal_to(EventObjectInfo.HELD)
        assert_that(object_status.hold_token).is_equal_to(hold_token.hold_token)

    def test_order_id(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        best_available_objects = self.client.events.change_best_available_object_status(
            event.key, number=1,
            status="mystatus",
            order_id="anOrder"
        )
        object_status = self.client.events.retrieve_object_info(event.key, best_available_objects.objects[0])
        assert_that(object_status.order_id).is_equal_to("anOrder")

    def test_book_best_available(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        best_available_objects = self.client.events.book_best_available(event.key, number=3)

        assert_that(best_available_objects.next_to_each_other).is_true()
        assert_that(best_available_objects.objects).contains_exactly("A-4", 'A-5', 'A-6')

    def test_hold_best_available(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()

        best_available_objects = self.client.events.hold_best_available(event.key, 1, hold_token=hold_token.hold_token)

        object_status = self.client.events.retrieve_object_info(event.key, best_available_objects.objects[0])
        assert_that(object_status.status).is_equal_to(EventObjectInfo.HELD)
        assert_that(object_status.hold_token).is_equal_to(hold_token.hold_token)

    def test_keepExtraDataTrue(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data = {"foo": "bar"}
        self.client.events.update_extra_data(event.key, "A-5", extra_data)

        self.client.events.change_best_available_object_status(event.key, 1, "someStatus", keep_extra_data=True)

        object_info = self.client.events.retrieve_object_info(event.key, "A-5")
        assert_that(object_info.extra_data).is_equal_to(extra_data)

    def test_keepExtraDataFalse(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data = {"foo": "bar"}
        self.client.events.update_extra_data(event.key, "A-5", extra_data)

        self.client.events.change_best_available_object_status(event.key, 1, "someStatus", keep_extra_data=False)

        object_info = self.client.events.retrieve_object_info(event.key, "A-5")
        assert_that(object_info.extra_data).is_none()

    def test_noKeepExtraData(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data = {"foo": "bar"}
        self.client.events.update_extra_data(event.key, "A-5", extra_data)

        self.client.events.change_best_available_object_status(event.key, 1, "someStatus")

        object_info = self.client.events.retrieve_object_info(event.key, "A-5")
        assert_that(object_info.extra_data).is_none()

    def test_channelKeys(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key, channels=[
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-6"])
        ])

        result = self.client.events.change_best_available_object_status(event.key, 1, "myStatus", channel_keys=["channelKey1"])

        assert_that(result.objects).contains_exactly("A-6")

    def test_ignoreChannels(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key, channels=[
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-5"])
        ])

        result = self.client.events.change_best_available_object_status(event.key, 1, "myStatus", ignore_channels=True)

        assert_that(result.objects).contains_exactly("A-5")

    def test_accessibleSeats(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        result = self.client.events.change_best_available_object_status(event.key, 3, "myStatus", accessible_seats=1)
        assert_that(result.next_to_each_other).is_true()
        assert_that(result.objects).contains_exactly("A-6", "A-7", "A-8")

    def test_throwsBestAvailableObjectsNotFoundException(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        try :
            self.client.events.change_best_available_object_status(event.key, 3000, "myStatus")
            self.fail("expected exception")
        except BestAvailableObjectsNotFoundException as e:
            assert_that(e.message).is_equal_to("Best available objects not found.")

    def test_genericSeatsioExceptionWhenEventNotFound(self):
        try :
            self.client.events.change_best_available_object_status("unexisting_event", 3000, "myStatus")
        except SeatsioException as e:
            assert_that(e).is_not_instance(BestAvailableObjectsNotFoundException)
