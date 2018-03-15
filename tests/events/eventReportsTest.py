from seatsio import ObjectProperties
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class EventReportsTest(SeatsioClientTest):

    def test_reportItemProperties(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.by_label(event.key)

        report_item = report.get("A-1")[0]
        assert_that(report_item.status).is_equal_to("booked")
        assert_that(report_item.label).is_equal_to("A-1")
        assert_that(report_item.categoryLabel).is_equal_to("Cat1")
        # TODO assert_that(report_item.categoryKey).is_equal_to(9)
        assert_that(report_item.ticketType).is_equal_to("tt1")
        assert_that(report_item.orderId).is_equal_to("order1")
        assert_that(report_item.forSale).is_true()
        # TODO assert_that(report_item.section).is_none()
        # TODO assert_that(report.entrance).is_none()
        # TODO assert_that(report.numBooked).is_none()
        # TODO assert_that(report.capacity).is_none()

    def test_reportItemPropertiesForGA(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.book(event.key, [ObjectProperties("GA1", quantity=5)])

        report = self.client.events.reports.by_label(event.key)

        report_item = report.get("GA1")[0]
        assert_that(report_item.status).is_equal_to("free")
        assert_that(report_item.label).is_equal_to("GA1")
        assert_that(report_item.categoryLabel).is_equal_to("Cat1")
        # TODO assert_that(report_item.categoryKey).is_equal_to(9)
        # TODO assert_that(report_item.ticketType).is_equal_to("tt1")
        # TODO assert_that(report_item.orderId).is_equal_to("order1")
        # TODO assert_that(report_item.forSale).is_true()
        # TODO assert_that(report_item.section).is_none()
        # TODO assert_that(report.entrance).is_none()
        assert_that(report_item.numBooked).is_equal_to(5)
        assert_that(report_item.capacity).is_equal_to(100)

    def test_byStatus(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.change_object_status(event.key, ["A-1", "A-2"], "mystatus")
        self.client.events.change_object_status(event.key, ["A-3"], "booked")

        report = self.client.events.reports.by_status(event.key)

        assert_that(report.get("mystatus")).has_size(2)
        assert_that(report.get("booked")).has_size(1)
        assert_that(report.get("free")).has_size(31)

    def testBySpecificStatus(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.change_object_status(event.key, ["A-1", "A-2"], "mystatus")
        self.client.events.change_object_status(event.key, ["A-3"], "booked")

        report = self.client.events.reports.by_status(event.key, status="mystatus")

        assert_that(report).has_size(2)

    def testByCategoryLabel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_category_label(event.key)

        assert_that(report.get("Cat1")).has_size(17)
        assert_that(report.get("Cat2")).has_size(17)

    def testBySpecificCategoryLabel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_category_label(event.key, "Cat1")

        assert_that(report).has_size(17)

    def testByCategoryKey(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_category_key(event.key)

        assert_that(report.get("9")).has_size(17)
        assert_that(report.get("10")).has_size(17)

    def testBySpecificCategoryKey(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_category_key(event.key, "9")

        assert_that(report).has_size(17)

    def testByLabel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_label(event.key)

        assert_that(report.get("A-1")).has_size(1)
        assert_that(report.get("A-2")).has_size(1)

    def testBySpecificLabel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_label(event.key, "A-1")

        assert_that(report).has_size(1)

    def testByOrderId(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.book(event.key, ["A-1", "A-2"], order_id="order1")
        self.client.events.book(event.key, ["A-3"], order_id="order2")

        report = self.client.events.reports.by_order_id(event.key)

        assert_that(report.get("order1")).has_size(2)
        assert_that(report.get("order2")).has_size(1)
        assert_that(report.get("NO_ORDER_ID")).has_size(31)

    def testBySpecificOrderId(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.book(event.key, ["A-1", "A-2"], order_id="order1")
        self.client.events.book(event.key, ["A-3"], order_id="order2")

        report = self.client.events.reports.by_order_id(event.key, "order1")

        assert_that(report).has_size(2)

    def testBySection(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_section(event.key)

        assert_that(report.get("NO_SECTION")).has_size(34)

    def testBySpecificSection(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.by_section(event.key, "NO_SECTION")

        assert_that(report).has_size(34)
