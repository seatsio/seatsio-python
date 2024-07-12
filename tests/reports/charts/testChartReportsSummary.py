from parameterized import parameterized
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ChartReportsSummaryTest(SeatsioClientTest):

    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.summary_by_object_type(chart_key=chart_key)
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key=chart_key),
            lambda instance, chart_key: instance.client.charts.reports.summary_by_object_type(chart_key=chart_key, version='draft')
        ]
    ])
    def test_summaryByObjectType(self, update_chart, get_report):
        chart_key = self.create_test_chart()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report.get("seat").get("count")).is_equal_to(32)
        assert_that(report.get("seat").get("bySection").get("NO_SECTION")).is_equal_to(32)
        assert_that(report.get("seat").get("byCategoryKey").get("9")).is_equal_to(16)
        assert_that(report.get("seat").get("byCategoryKey").get("10")).is_equal_to(16)
        assert_that(report.get("seat").get("byCategoryLabel").get("Cat1")).is_equal_to(16)
        assert_that(report.get("seat").get("byCategoryLabel").get("Cat2")).is_equal_to(16)

        assert_that(report.get("generalAdmission").get("count")).is_equal_to(200)
        assert_that(report.get("generalAdmission").get("bySection").get("NO_SECTION")).is_equal_to(200)
        assert_that(report.get("generalAdmission").get("byCategoryKey").get("9")).is_equal_to(100)
        assert_that(report.get("generalAdmission").get("byCategoryKey").get("10")).is_equal_to(100)
        assert_that(report.get("generalAdmission").get("byCategoryLabel").get("Cat1")).is_equal_to(100)
        assert_that(report.get("generalAdmission").get("byCategoryLabel").get("Cat2")).is_equal_to(100)

    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.summary_by_object_type(chart_key=chart_key,
                                                                                              book_whole_tables='true')
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key=chart_key),
            lambda instance, chart_key: instance.client.charts.reports.summary_by_object_type(chart_key=chart_key,
                                                                                              book_whole_tables='true',
                                                                                              version='draft')
        ]
    ])
    def test_summaryByObjectType_bookWholeTablesTrue(self, update_chart, get_report):
        chart_key = self.create_test_chart_with_tables()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report.get("seat").get("count")).is_equal_to(0)
        assert_that(report.get("table").get("count")).is_equal_to(2)

    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.summary_by_category_key(chart_key=chart_key)
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key=chart_key),
            lambda instance, chart_key: instance.client.charts.reports.summary_by_category_key(chart_key=chart_key,
                                                                                               version='draft')
        ]
    ])
    def test_summaryByCategoryKey(self, update_chart, get_report):
        chart_key = self.create_test_chart()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report.get("9").get("count")).is_equal_to(116)
        assert_that(report.get("9").get("bySection").get("NO_SECTION")).is_equal_to(116)

        assert_that(report.get("10").get("count")).is_equal_to(116)
        assert_that(report.get("10").get("bySection").get("NO_SECTION")).is_equal_to(116)

    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.summary_by_category_label(chart_key=chart_key)
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key=chart_key),
            lambda instance, chart_key: instance.client.charts.reports.summary_by_category_label(chart_key=chart_key,
                                                                                                 version='draft')
        ]
    ])
    def test_summaryByCategoryLabel(self, update_chart, get_report):
        chart_key = self.create_test_chart()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report.get("Cat1").get("count")).is_equal_to(116)
        assert_that(report.get("Cat1").get("bySection").get("NO_SECTION")).is_equal_to(116)

        assert_that(report.get("Cat2").get("count")).is_equal_to(116)
        assert_that(report.get("Cat2").get("bySection").get("NO_SECTION")).is_equal_to(116)

    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.summary_by_section(chart_key=chart_key)
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key=chart_key),
            lambda instance, chart_key: instance.client.charts.reports.summary_by_section(chart_key=chart_key,
                                                                                          version='draft')
        ]
    ])
    def test_summaryBySection(self, update_chart, get_report):
        chart_key = self.create_test_chart()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report.get("NO_SECTION").get("count")).is_equal_to(232)
        assert_that(report.get("NO_SECTION").get("byCategoryKey").get("9")).is_equal_to(116)
        assert_that(report.get("NO_SECTION").get("byCategoryKey").get("10")).is_equal_to(116)
        assert_that(report.get("NO_SECTION").get("byCategoryLabel").get("Cat1")).is_equal_to(116)
        assert_that(report.get("NO_SECTION").get("byCategoryLabel").get("Cat2")).is_equal_to(116)

    @parameterized.expand([
        [
            lambda instance, chart_key: {},
            lambda instance, chart_key: instance.client.charts.reports.summary_by_zone(chart_key=chart_key)
        ],
        [
            lambda instance, chart_key: instance.create_draft_chart(chart_key=chart_key),
            lambda instance, chart_key: instance.client.charts.reports.summary_by_zone(chart_key=chart_key,
                                                                                          version='draft')
        ]
    ])
    def test_summaryByZone(self, update_chart, get_report):
        chart_key = self.create_test_chart_with_zones()
        update_chart(self, chart_key)

        report = get_report(self, chart_key)

        assert_that(report.get("midtrack").get("count")).is_equal_to(6032)
        assert_that(report.get("midtrack").get("byCategoryKey").get("2")).is_equal_to(6032)
        assert_that(report.get("midtrack").get("byCategoryLabel").get("Mid Track Stand")).is_equal_to(6032)
        assert_that(report.get("midtrack").get("bySection").get("MT1")).is_equal_to(2418)
        assert_that(report.get("midtrack").get("bySection").get("MT3")).is_equal_to(3614)
        assert_that(report.get("midtrack").get("byObjectType").get("seat")).is_equal_to(6032)

    def create_draft_chart(self, chart_key):
        self.client.events.create(chart_key)
        self.client.charts.update(chart_key, "Foo")
