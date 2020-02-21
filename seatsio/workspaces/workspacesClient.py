from seatsio.domain import Workspace
from seatsio.pagination.listableObjectsClient import ListableObjectsClient
from seatsio.workspaces.UpdateWorkspaceRequest import UpdateWorkspaceRequest
from seatsio.workspaces.createWorkspaceRequest import CreateWorkspaceRequest


class WorkspacesClient(ListableObjectsClient):

    def __init__(self, http_client):
        ListableObjectsClient.__init__(self, http_client, Workspace, "/workspaces")

    def create(self, name, is_test=None):
        response = self.http_client.url("/workspaces").post(
            CreateWorkspaceRequest(name, is_test))
        return Workspace(response.json())

    def update(self, key, name):
        self.http_client.url("/workspaces/{key}", key=key).post(
            UpdateWorkspaceRequest(name))

    def retrieve(self, key):
        return self.http_client.url("/workspaces/{key}", key=key).get_as(Workspace)
