from seatsio.charts.chartsClient import ChartsClient
from seatsio.eventlog.eventLogClient import EventLogClient
from seatsio.events.eventsClient import EventsClient
from seatsio.holdtokens.HoldTokenClient import HoldTokensClient
from seatsio.httpClient import HttpClient
from seatsio.reports.usage.usageReports import UsageReports
from seatsio.seasons.seasonsClient import SeasonsClient
from seatsio.ticketBuyers.ticketBuyersClient import TicketBuyersClient
from seatsio.workspaces.workspacesClient import WorkspacesClient


class Client:
    IDEMPOTENCY_KEY_HEADER = "Idempotency-Key"

    def __init__(self, region, secret_key, workspace_key=None, max_retries=5):
        self.__init_with_http_client(HttpClient(region.url, secret_key, workspace_key, max_retries))

    @classmethod
    def _from_http_client(cls, http_client):
        client = cls.__new__(cls)
        client.__init_with_http_client(http_client)
        return client

    def __init_with_http_client(self, http_client):
        self.http_client = http_client
        self.base_url = http_client.base_url
        self.charts = ChartsClient(self.http_client)
        self.events = EventsClient(self.http_client)
        self.seasons = SeasonsClient(self.http_client, self)
        self.workspaces = WorkspacesClient(self.http_client)
        self.hold_tokens = HoldTokensClient(self.http_client)
        self.usage_reports = UsageReports(self.http_client)
        self.event_log = EventLogClient(self.http_client)
        self.ticket_buyers = TicketBuyersClient(self.http_client)

    def with_idempotency_key(self, idempotency_key):
        return Client._from_http_client(self.http_client.with_idempotency_key(idempotency_key))

    def withIdempotencyKey(self, idempotency_key):
        return self.with_idempotency_key(idempotency_key)
