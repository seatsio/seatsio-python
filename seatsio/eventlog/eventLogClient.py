from seatsio.domain import EventLogItem
from seatsio.pagination.listableObjectsClient import ListableObjectsClient


class EventLogClient(ListableObjectsClient):

    def __init__(self, http_client):
        ListableObjectsClient.__init__(self, http_client, EventLogItem, "/event-log")
