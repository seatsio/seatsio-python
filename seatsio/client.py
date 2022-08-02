from seatsio.charts.chartsClient import ChartsClient
from seatsio.events.eventsClient import EventsClient
from seatsio.holdtokens.HoldTokenClient import HoldTokensClient
from seatsio.httpClient import HttpClient
from seatsio.reports.usage.usageReports import UsageReports
from seatsio.seasons.seasonsClient import SeasonsClient
from seatsio.subaccounts.subaccountsClient import SubaccountsClient
from seatsio.workspaces.workspacesClient import WorkspacesClient


class Client:
    def __init__(self, region, secret_key, workspace_key=None, max_retries=5):
        base_url = region.url
        self.base_url = base_url
        self.http_client = HttpClient(base_url, secret_key, workspace_key, max_retries)
        self.charts = ChartsClient(self.http_client)
        self.events = EventsClient(self.http_client)
        self.seasons = SeasonsClient(self.http_client, self)
        self.subaccounts = SubaccountsClient(self.http_client)
        self.workspaces = WorkspacesClient(self.http_client)
        self.hold_tokens = HoldTokensClient(self.http_client)
        self.usage_reports = UsageReports(self.http_client)
