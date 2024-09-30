from parameterized import parameterized

from seatsio.domain import ChartReport, ChartObjectInfo
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ChartReportsTest(SeatsioClientTest):

    @parameterized.expand([
        [
                lambda instance, chart_key: {},
                lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key)
        ],
        [
                lambda instance, chart_key: instance.create_draft_chart(chart_key=chart_key),
                lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key, version='draft')
        ]
    ])
    def test_reportItemProperties(self, update_chart, get_report):
        chart_key = self.create_test_chart()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report).is_instance(ChartReport)
        report_item = report.get("A-1")[0]
        assert_that(report_item).is_instance(ChartObjectInfo)
        assert_that(report_item.label).is_equal_to("A-1")
        assert_that(report_item.labels).is_equal_to({"own": {"label": "1", "type": "seat"}, "parent": {"label": "A", "type": "row"}})
        assert_that(report_item.ids).is_equal_to({"own": "1", "parent": "A"})
        assert_that(report_item.category_label).is_equal_to("Cat1")
        assert_that(report_item.category_key).is_equal_to("9")
        assert_that(report_item.object_type).is_equal_to("seat")
        assert_that(report_item.section).is_none()
        assert_that(report_item.entrance).is_none()
        assert_that(report_item.capacity).is_none()
        assert_that(report_item.left_neighbour).is_none()
        assert_that(report_item.right_neighbour).is_equal_to("A-2")
        assert_that(report_item.distance_to_focal_point).is_not_none()
        assert_that(report_item.is_accessible).is_not_none()
        assert_that(report_item.is_companion_seat).is_not_none()
        assert_that(report_item.has_restricted_view).is_not_none()
        assert_that(report_item.floor).is_none()

    @parameterized.expand([
        [
                lambda instance, chart_key: {},
                lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key)
        ],
        [
                lambda instance, chart_key: instance.create_draft_chart(chart_key),
                lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key, version='draft')
        ]
    ])
    def test_reportItemPropertiesForGA(self, update_chart, get_report):
        chart_key = self.create_test_chart()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report).is_instance(ChartReport)
        report_item = report.get("GA1")[0]
        assert_that(report_item).is_instance(ChartObjectInfo)
        assert_that(report_item.label).is_equal_to("GA1")
        assert_that(report_item.object_type).is_equal_to("generalAdmission")
        assert_that(report_item.category_label).is_equal_to("Cat1")
        assert_that(report_item.category_key).is_equal_to("9")
        assert_that(report_item.section).is_none()
        assert_that(report_item.entrance).is_none()
        assert_that(report_item.capacity).is_equal_to(100)
        assert_that(report_item.book_as_a_whole).is_equal_to(False)

    @parameterized.expand([
        [
                lambda instance, chart_key: {},
                lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key, book_whole_tables='true')
        ],
        [
                lambda instance, chart_key: instance.create_draft_chart(chart_key),
                lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key, book_whole_tables='true', version='draft')
        ]
    ])
    def test_reportItemPropertiesForTable(self, update_chart, get_report):
        chart_key = self.create_test_chart_with_tables()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        report_item = report.get("T1")[0]
        assert_that(report_item.num_seats).is_equal_to(6)
        assert_that(report_item.book_as_a_whole).is_false()

    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key)
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key),
            lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key, version='draft')
        ]
    ])
    def testByLabel(self, update_chart, get_report):
        chart_key = self.create_test_chart()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report).is_instance(ChartReport)
        assert_that(report.get("A-1")).has_size(1)
        assert_that(report.get("A-2")).has_size(1)

    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key)
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key),
            lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key, version='draft')
        ]
    ])
    def testByLabelWithFloors(self, update_chart, get_report):
        chart_key = self.create_test_chart_with_floors()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report).is_instance(ChartReport)
        assert_that(report.get("S1-A-1")[0].floor).is_equal_to({"name": "1", "displayName": "Floor 1"})
        assert_that(report.get("S1-A-2")[0].floor).is_equal_to({"name": "1", "displayName": "Floor 1"})
        assert_that(report.get("S2-B-1")[0].floor).is_equal_to({"name": "2", "displayName": "Floor 2"})
        assert_that(report.get("S2-B-2")[0].floor).is_equal_to({"name": "2", "displayName": "Floor 2"})


    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.by_object_type(chart_key=chart_key)
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key),
            lambda instance, chart_key: instance.client.charts.reports.by_object_type(chart_key=chart_key,
                                                                                      version='draft')
        ]
    ])
    def testByObjectType(self, update_chart, get_report):
        chart_key = self.create_test_chart()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report).is_instance(ChartReport)
        assert_that(report.get("seat")).has_size(32)
        assert_that(report.get("generalAdmission")).has_size(2)

    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.by_object_type(chart_key=chart_key)
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key),
            lambda instance, chart_key: instance.client.charts.reports.by_object_type(chart_key=chart_key,
                                                                                      version='draft')
        ]
    ])
    def testByObjectTypeWithFloors(self, update_chart, get_report):
        chart_key = self.create_test_chart_with_floors()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report).is_instance(ChartReport)
        assert_that(report.get("seat")[0].floor).is_equal_to({"name": "1", "displayName": "Floor 1"})
        assert_that(report.get("seat")[1].floor).is_equal_to({"name": "1", "displayName": "Floor 1"})
        assert_that(report.get("seat")[2].floor).is_equal_to({"name": "2", "displayName": "Floor 2"})
        assert_that(report.get("seat")[3].floor).is_equal_to({"name": "2", "displayName": "Floor 2"})

    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key)
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key),
            lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key, version='draft')
        ]
    ])
    def testByLabel_BookWholeTablesNone(self, update_chart, get_report):
        chart_key = self.create_test_chart_with_tables()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report).is_instance(ChartReport)
        assert_that(report.items).has_size(14)

    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key,
                                                                                book_whole_tables='chart')
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key),
            lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key,
                                                                                book_whole_tables='chart',
                                                                                version='draft')
        ]
    ])
    def testByLabel_BookWholeTablesChart(self, update_chart, get_report):
        chart_key = self.create_test_chart_with_tables()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report).is_instance(ChartReport)
        assert_that(report.items).has_size(7)

    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key,
                                                                                book_whole_tables='true')
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key),
            lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key,
                                                                                book_whole_tables='true',
                                                                                version='draft')
        ]
    ])
    def testByLabel_BookWholeTablesTrue(self, update_chart, get_report):
        chart_key = self.create_test_chart_with_tables()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report).is_instance(ChartReport)
        assert_that(report.items).has_size(2)

    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key,
                                                                                book_whole_tables='false')
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key),
            lambda instance, chart_key: instance.client.charts.reports.by_label(chart_key=chart_key,
                                                                                book_whole_tables='false',
                                                                                version='draft')
        ]
    ])
    def testByLabel_BookWholeTablesFalse(self, update_chart, get_report):
        chart_key = self.create_test_chart_with_tables()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report).is_instance(ChartReport)
        assert_that(report.items).has_size(12)


    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.by_zone(chart_key=chart_key)
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key),
            lambda instance, chart_key: instance.client.charts.reports.by_zone(chart_key=chart_key,
                                                                                      version='draft')
        ]
    ])
    def testByZone(self, update_chart, get_report):
        chart_key = self.create_test_chart_with_zones()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report).is_instance(ChartReport)
        assert_that(report.get("midtrack")).has_size(6032)
        assert_that(report.get("midtrack")[0].zone).is_equal_to("midtrack")
        assert_that(report.get("finishline")).has_size(2865)
        assert_that(report.get("NO_ZONE")).has_size(0)


    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.by_section(chart_key=chart_key)
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key),
            lambda instance, chart_key: instance.client.charts.reports.by_section(chart_key=chart_key,
                                                                                      version='draft')
        ]
    ])
    def testBySectionWithFloors(self, update_chart, get_report):
        chart_key = self.create_test_chart_with_floors()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report).is_instance(ChartReport)
        assert_that(report.get("S1")[0].floor).is_equal_to({"name": "1", "displayName": "Floor 1"})
        assert_that(report.get("S1")[1].floor).is_equal_to({"name": "1", "displayName": "Floor 1"})
        assert_that(report.get("S2")[0].floor).is_equal_to({"name": "2", "displayName": "Floor 2"})
        assert_that(report.get("S2")[1].floor).is_equal_to({"name": "2", "displayName": "Floor 2"})

    def create_draft_chart(self, chart_key):
        self.client.events.create(chart_key)
        self.client.charts.update(chart_key, "Foo")
