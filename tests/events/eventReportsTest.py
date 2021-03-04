from seatsio.domain import EventReport, EventReportItem, Channel
from seatsio.events.objectProperties import ObjectProperties
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class EventReportsTest(SeatsioClientTest):

    def test_reportItemProperties(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data = {"foo": "bar"}

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1", extra_data=extra_data)], order_id="order1")

        self.client.events.update_channels(event.key, {
            'channelKey1': Channel(name='channel 1', color='#00FF00', index=1)
        })
        self.client.events.assign_objects_to_channels(event.key, {
            "channelKey1": ["A-1"]
        })

        report = self.client.events.reports.by_label(event.key)

        assert_that(report).is_instance(EventReport)
        report_item = report.get("A-1")[0]
        assert_that(report_item).is_instance(EventReportItem)
        assert_that(report_item.status).is_equal_to("booked")
        assert_that(report_item.label).is_equal_to("A-1")
        assert_that(report_item.labels).is_equal_to({"own": {"label": "1", "type": "seat"}, "parent": {"label": "A", "type": "row"}})
        assert_that(report_item.category_label).is_equal_to("Cat1")
        assert_that(report_item.category_key).is_equal_to("9")
        assert_that(report_item.ticket_type).is_equal_to("tt1")
        assert_that(report_item.order_id).is_equal_to("order1")
        assert_that(report_item.object_type).is_equal_to("seat")
        assert_that(report_item.for_sale).is_true()
        assert_that(report_item.section).is_none()
        assert_that(report_item.entrance).is_none()
        assert_that(report_item.num_booked).is_none()
        assert_that(report_item.capacity).is_none()
        assert_that(report_item.book_as_a_whole).is_none()
        assert_that(report_item.extra_data).is_equal_to(extra_data)
        assert_that(report_item.is_accessible).is_false()
        assert_that(report_item.is_companion_seat).is_false()
        assert_that(report_item.has_restricted_view).is_false()
        assert_that(report_item.displayed_object_type).is_none()
        assert_that(report_item.left_neighbour).is_none()
        assert_that(report_item.right_neighbour).is_equal_to("A-2")
        assert_that(report_item.is_selectable).is_false()
        assert_that(report_item.is_disabled_by_social_distancing).is_false()
        assert_that(report_item.channel).is_equal_to('channelKey1')

    def test_holdToken(self):
        chart_key = self.create_test_chart()
        hold_token = self.client.hold_tokens.create()
        event = self.client.events.create(chart_key)

        self.client.events.hold(event.key, "A-1", hold_token.hold_token)

        report = self.client.events.reports.by_label(event.key)

        report_item = report.get("A-1")[0]
        assert_that(report_item.hold_token).is_equal_to(hold_token.hold_token)

    def test_reportItemPropertiesForGA(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.book(event.key, [ObjectProperties("GA1", quantity=5)])
        hold_token = self.client.hold_tokens.create()
        self.client.events.hold(event.key, [ObjectProperties("GA1", quantity=3)], hold_token.hold_token)

        report = self.client.events.reports.by_label(event.key)

        assert_that(report).is_instance(EventReport)
        report_item = report.get("GA1")[0]
        assert_that(report_item).is_instance(EventReportItem)
        assert_that(report_item.status).is_equal_to("free")
        assert_that(report_item.label).is_equal_to("GA1")
        assert_that(report_item.object_type).is_equal_to("generalAdmission")
        assert_that(report_item.category_label).is_equal_to("Cat1")
        assert_that(report_item.category_key).is_equal_to("9")
        assert_that(report_item.ticket_type).is_none()
        assert_that(report_item.order_id).is_none()
        assert_that(report_item.for_sale).is_true()
        assert_that(report_item.section).is_none()
        assert_that(report_item.entrance).is_none()
        assert_that(report_item.num_booked).is_equal_to(5)
        assert_that(report_item.num_held).is_equal_to(3)
        assert_that(report_item.num_free).is_equal_to(92)
        assert_that(report_item.capacity).is_equal_to(100)
        assert_that(report_item.book_as_a_whole).is_equal_to(False)
        assert_that(report_item.is_accessible).is_none()
        assert_that(report_item.is_companion_seat).is_none()
        assert_that(report_item.has_restricted_view).is_none()
        assert_that(report_item.displayed_object_type).is_none()

    def testByStatus(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.change_object_status(event.key, ["A-1", "A-2"], "mystatus")
        self.client.events.change_object_status(event.key, ["A-3"], "booked")

        report = self.client.events.reports.by_status(event.key)

        assert_that(report).is_instance(EventReport)
        assert_that(report.get("mystatus")).has_size(2)
        assert_that(report.get("booked")).has_size(1)
        assert_that(report.get("free")).has_size(31)

    def testByStatusEmptyChart(self):
        chart_key = self.client.charts.create().key
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_status(event.key)

        assert_that(report.items).has_size(0)

    def testBySpecificStatus(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.change_object_status(event.key, ["A-1", "A-2"], "mystatus")
        self.client.events.change_object_status(event.key, ["A-3"], "booked")

        report = self.client.events.reports.by_status(event.key, status="mystatus")

        assert_that(report).is_instance(list)
        assert_that(report[0]).is_instance(EventReportItem)
        assert_that(report).has_size(2)

    def testBySpecificNonExistingStatus(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_status(event.key, status="mystatus")

        assert_that(report).is_instance(list)
        assert_that(report).has_size(0)

    def testByCategoryLabel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_category_label(event.key)

        assert_that(report).is_instance(EventReport)
        assert_that(report.get("Cat1")).has_size(17)
        assert_that(report.get("Cat2")).has_size(17)

    def testBySpecificCategoryLabel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_category_label(event.key, "Cat1")

        assert_that(report).is_instance(list)
        assert_that(report[0]).is_instance(EventReportItem)
        assert_that(report).has_size(17)

    def testByCategoryKey(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_category_key(event.key)

        assert_that(report).is_instance(EventReport)
        assert_that(report.get("9")).has_size(17)
        assert_that(report.get("10")).has_size(17)

    def testBySpecificCategoryKey(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_category_key(event.key, "9")

        assert_that(report).is_instance(list)
        assert_that(report[0]).is_instance(EventReportItem)
        assert_that(report).has_size(17)

    def testByLabel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_label(event.key)

        assert_that(report).is_instance(EventReport)
        assert_that(report.get("A-1")).has_size(1)
        assert_that(report.get("A-2")).has_size(1)

    def testBySpecificLabel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_label(event.key, "A-1")

        assert_that(report).is_instance(list)
        assert_that(report[0]).is_instance(EventReportItem)
        assert_that(report).has_size(1)

    def testByOrderId(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.book(event.key, ["A-1", "A-2"], order_id="order1")
        self.client.events.book(event.key, ["A-3"], order_id="order2")

        report = self.client.events.reports.by_order_id(event.key)

        assert_that(report).is_instance(EventReport)
        assert_that(report.get("order1")).has_size(2)
        assert_that(report.get("order2")).has_size(1)
        assert_that(report.get("NO_ORDER_ID")).has_size(31)

    def testBySpecificOrderId(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.book(event.key, ["A-1", "A-2"], order_id="order1")
        self.client.events.book(event.key, ["A-3"], order_id="order2")

        report = self.client.events.reports.by_order_id(event.key, "order1")

        assert_that(report).is_instance(list)
        assert_that(report[0]).is_instance(EventReportItem)
        assert_that(report).has_size(2)

    def testBySection(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_section(event.key)

        assert_that(report).is_instance(EventReport)
        assert_that(report.get("NO_SECTION")).has_size(34)

    def testBySpecificSection(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_section(event.key, "NO_SECTION")

        assert_that(report).is_instance(list)
        assert_that(report[0]).is_instance(EventReportItem)
        assert_that(report).has_size(34)

    def testBySelectability(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.book(event.key, ["A-1", "A-2"])

        report = self.client.events.reports.by_selectability(event.key)

        assert_that(report).is_instance(EventReport)
        assert_that(report.get("selectable")).has_size(32)
        assert_that(report.get("not_selectable")).has_size(2)

    def testBySpecificSelectability(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.book(event.key, ["A-1", "A-2"])

        report = self.client.events.reports.by_selectability(event.key, "selectable")

        assert_that(report).is_instance(list)
        assert_that(report[0]).is_instance(EventReportItem)
        assert_that(report).has_size(32)

    def testByChannel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.update_channels(event.key, {
            'channelKey1': Channel(name='channel 1', color='#00FF00', index=1)
        })
        self.client.events.assign_objects_to_channels(event.key, {
            "channelKey1": ["A-1", "A-2"]
        })

        report = self.client.events.reports.by_channel(event.key)

        assert_that(report).is_instance(EventReport)
        assert_that(report.get("NO_CHANNEL")).has_size(32)
        assert_that(report.get("channelKey1")).has_size(2)

    def testBySpecificChannel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.update_channels(event.key, {
            'channelKey1': Channel(name='channel 1', color='#00FF00', index=1)
        })
        self.client.events.assign_objects_to_channels(event.key, {
            "channelKey1": ["A-1", "A-2"]
        })

        report = self.client.events.reports.by_channel(event.key, "channelKey1")

        assert_that(report).is_instance(list)
        assert_that(report[0]).is_instance(EventReportItem)
        assert_that(report).has_size(2)
