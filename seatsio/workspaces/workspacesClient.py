from seatsio.domain import Workspace
from seatsio.pagination.listableObjectsClient import ListableObjectsClient
from seatsio.pagination.lister import Lister
from seatsio.pagination.pageFetcher import PageFetcher
from seatsio.workspaces.UpdateWorkspaceRequest import UpdateWorkspaceRequest
from seatsio.workspaces.createWorkspaceRequest import CreateWorkspaceRequest


class WorkspacesClient(ListableObjectsClient):

    def __init__(self, http_client):
        ListableObjectsClient.__init__(self, http_client, Workspace, "/workspaces")
        self.active = Lister(PageFetcher(Workspace, self.http_client, "/workspaces/active"))
        self.inactive = Lister(PageFetcher(Workspace, self.http_client, "/workspaces/inactive"))

    def create(self, name, is_test=None):
        response = self.http_client.url("/workspaces").post(
            CreateWorkspaceRequest(name, is_test))
        return Workspace(response.json())

    def update(self, key, name):
        self.http_client.url("/workspaces/{key}", key=key).post(
            UpdateWorkspaceRequest(name))

    def regenerate_secret_key(self, key):
        response = self.http_client.url("/workspaces/{key}/actions/regenerate-secret-key", key=key).post()
        return response.json()["secretKey"]

    def activate(self, key):
        self.http_client.url("/workspaces/{key}/actions/activate", key=key).post()

    def deactivate(self, key):
        self.http_client.url("/workspaces/{key}/actions/deactivate", key=key).post()

    def set_default(self, key):
        self.http_client.url("/workspaces/actions/set-default/{key}", key=key).post()

    def retrieve(self, key):
        return self.http_client.url("/workspaces/{key}", key=key).get_as(Workspace)

    def list(self, filter=None):
        page_fetcher = PageFetcher(Workspace, self.http_client, "/workspaces")

        if filter is not None:
            page_fetcher.set_query_param("filter", filter)

        return Lister(page_fetcher).list()
