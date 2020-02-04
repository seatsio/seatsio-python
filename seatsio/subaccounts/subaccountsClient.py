from seatsio.domain import Subaccount, Chart
from seatsio.pagination.listableObjectsClient import ListableObjectsClient
from seatsio.pagination.lister import Lister
from seatsio.pagination.pageFetcher import PageFetcher


class SubaccountsClient(ListableObjectsClient):

    def __init__(self, http_client):
        ListableObjectsClient.__init__(self, http_client, Subaccount, "/subaccounts")
        self.active = Lister(PageFetcher(Subaccount, self.http_client, "/subaccounts/active"))
        self.inactive = Lister(PageFetcher(Subaccount, self.http_client, "/subaccounts/inactive"))

    def create(self, name=None):
        body = {}
        if name:
            body['name'] = name
        response = self.http_client.url("/subaccounts").post(body)
        return Subaccount(response.json())

    def update(self, subaccount_id, name=None):
        body = {}
        if name:
            body['name'] = name
        self.http_client.url("/subaccounts/{id}", id=subaccount_id).post(body)

    def retrieve(self, subaccount_id):
        response = self.http_client.url("/subaccounts/{id}", id=subaccount_id).get()
        return Subaccount(response)

    def activate(self, subaccount_id):
        self.http_client.url("/subaccounts/{id}/actions/activate", id=subaccount_id).post()

    def deactivate(self, subaccount_id):
        self.http_client.url("/subaccounts/{id}/actions/deactivate", id=subaccount_id).post()

    def copy_chart_to_parent(self, subaccount_id, chart_key):
        response = self.http_client.url(
            "/subaccounts/{id}/charts/{chartKey}/actions/copy-to/parent",
            id=subaccount_id,
            chartKey=chart_key).post()
        return Chart(response.json())

    def copy_chart_to_subaccount(self, from_id, to_id, chart_key):
        response = self.http_client.url(
            "/subaccounts/{fromId}/charts/{chartKey}/actions/copy-to/{toId}",
            fromId=from_id,
            toId=to_id,
            chartKey=chart_key).post()
        return Chart(response.json())

    def regenerate_designer_key(self, subaccount_id):
        self.http_client.url("/subaccounts/{id}/designer-key/actions/regenerate", id=subaccount_id).post()

    def regenerate_secret_key(self, subaccount_id):
        self.http_client.url("/subaccounts/{id}/secret-key/actions/regenerate", id=subaccount_id).post()

    def list(self, filter=None):
        page_fetcher = PageFetcher(Subaccount, self.http_client, "/subaccounts")

        if filter is not None:
            page_fetcher.set_query_param("filter", filter)

        return Lister(page_fetcher).list()
