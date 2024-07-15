import json

from munch import munchify

from seatsio.reports.charts.chartReports import ChartReports
from seatsio.charts.chartsRequest import ChartRequest
from seatsio.domain import Chart, ChartValidation, Category
from seatsio.pagination.listableObjectsClient import ListableObjectsClient
from seatsio.pagination.lister import Lister
from seatsio.pagination.pageFetcher import PageFetcher


class ChartsClient(ListableObjectsClient):

    def __init__(self, http_client):
        ListableObjectsClient.__init__(self, http_client, Chart, "/charts")
        self.archive = Lister(PageFetcher(Chart, self.http_client, "/charts/archive"))
        self.reports = ChartReports(self.http_client)

    def retrieve(self, chart_key):
        return self.http_client.url("/charts/{key}", key=chart_key).get_as(Chart)

    def retrieve_with_events(self, chart_key):
        return self.http_client.url("/charts/{key}?expand=events", key=chart_key).get_as(Chart)

    def create(self, name=None, venue_type=None, categories=None):
        request = ChartRequest(name, venue_type, categories)
        response = self.http_client.url("/charts").post(request)
        return Chart(response.json())

    def retrieve_published_version(self, key):
        response = self.http_client.url("/charts/{key}/version/published", key=key).get()
        return munchify(response)

    def retrieve_draft_version(self, key):
        response = self.http_client.url("/charts/{key}/version/draft", key=key).get()
        return munchify(response)

    def retrieve_draft_version_thumbnail(self, key):
        return self.http_client.url("/charts/{key}/version/draft/thumbnail", key=key).get_raw()

    def retrieve_published_version_thumbnail(self, key):
        return self.http_client.url("/charts/{key}/version/published/thumbnail", key=key).get_raw()

    def copy(self, key):
        return self.http_client \
            .url("/charts/{key}/version/published/actions/copy", key=key) \
            .post_empty_and_return(Chart)

    def copy_to_workspace(self, chart_key, to_workspace_key):
        return self.http_client \
            .url("/charts/{key}/version/published/actions/copy-to-workspace/{toWorkspaceKey}",
                 key=chart_key,
                 toWorkspaceKey=to_workspace_key) \
            .post_empty_and_return(Chart)

    def copy_from_workspace_to(self, chart_key, from_workspace_key, to_workspace_key):
        return self.http_client \
            .url("/charts/{key}/version/published/actions/copy/from/{fromWorkspaceKey}/to{toWorkspaceKey}",
                 key=chart_key,
                 toWorkspaceKey=to_workspace_key) \
            .post_empty_and_return(Chart)

    def copy_from_workspace_to(self, chart_key, from_workspace_key, to_workspace_key):
        return self.http_client \
            .url("/charts/{key}/version/published/actions/copy/from/{fromWorkspaceKey}/to/{toWorkspaceKey}",
                 key=chart_key,
                 fromWorkspaceKey=from_workspace_key,
                 toWorkspaceKey=to_workspace_key) \
            .post_empty_and_return(Chart)

    def copy_draft_version(self, key):
        return self.http_client \
            .url("/charts/{key}/version/draft/actions/copy", key=key) \
            .post_empty_and_return(Chart)

    def discard_draft_version(self, key):
        self.http_client.url("/charts/{key}/version/draft/actions/discard", key=key).post()

    def update(self, key, new_name=None, categories=None):
        request = ChartRequest(name=new_name, categories=categories)
        self.http_client.url("/charts/{key}", key=key).post(request)

    def add_category(self, chart_key, category):
        self.http_client.url("/charts/{chart_key}/categories", chart_key=chart_key)\
            .post(category)

    def remove_category(self, chart_key, category_key):
        self.http_client.url("/charts/{chart_key}/categories/{category_key}",
                             chart_key=chart_key,
                             category_key=category_key) \
            .delete()

    def list_categories(self, chart_key):
        response = self.http_client.url("/charts/{chart_key}/categories",
                                        chart_key=chart_key) \
            .get()
        return Category.create_list(response["categories"])

    def update_category(self, chart_key, category_key, label, color, accessible):
        self.http_client.url("/charts/{chart_key}/categories/{category_key}",
                             chart_key=chart_key,
                             category_key=category_key) \
            .post(UpdateCategoryRequest(label, color, accessible))

    def move_to_archive(self, chart_key):
        self.http_client.url("/charts/{key}/actions/move-to-archive", key=chart_key).post()

    def move_out_of_archive(self, chart_key):
        self.http_client.url("/charts/{key}/actions/move-out-of-archive", key=chart_key).post()

    def publish_draft_version(self, chart_key):
        self.http_client.url("/charts/{key}/version/draft/actions/publish", key=chart_key).post()

    def list_all_tags(self):
        response = self.http_client.url("/charts/tags").get()
        return response["tags"]

    def add_tag(self, key, tag):
        return self.http_client.url("/charts/{key}/tags/{tag}", key=key, tag=tag).post()

    def remove_tag(self, key, tag):
        self.http_client.url("/charts/{key}/tags/{tag}", key=key, tag=tag).delete()

    def list(self, chart_filter=None, tag=None, expand_events=False, expand_validation=False, expand_venue_type=False, expand_zones=False):
        page_fetcher = PageFetcher(Chart, self.http_client, "/charts") \
            .set_query_param("filter", chart_filter) \
            .set_query_param("tag", tag) \
            .set_query_param("expand", self.list_expand_params(expand_events, expand_validation, expand_venue_type, expand_zones))
        return Lister(page_fetcher).list()

    def validate_published_version(self, key):
        response = self.http_client.url("/charts/{key}/version/published/actions/validate", key=key).post()
        return ChartValidation(json.loads(response.text))

    def validate_draft_version(self, key):
        response = self.http_client.url("/charts/{key}/version/draft/actions/validate", key=key).post()
        return ChartValidation(json.loads(response.text))

    def list_expand_params(self, expand_events, expand_validation, expand_venue_type, expand_zones):
        result = []
        if expand_events:
            result.append("events")
        if expand_validation:
            result.append("validation")
        if expand_venue_type:
            result.append("venueType")
        if expand_zones:
            result.append("zones")
        return result


class UpdateCategoryRequest:
    def __init__(self, label, color, accessible):
        if label:
            self.label = label
        if color:
            self.color = color
        if accessible:
            self.accessible = accessible
