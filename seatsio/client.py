from seatsio.accounts.accountsClient import AccountsClient
from seatsio.charts.chartsClient import ChartsClient
from seatsio.events.eventsClient import EventsClient
from seatsio.holdtokens.HoldTokenClient import HoldTokensClient
from seatsio.httpClient import HttpClient
from seatsio.reports.usage.usageReports import UsageReports
from seatsio.subaccounts.subaccountsClient import SubaccountsClient
from seatsio.workspaces.workspacesClient import WorkspacesClient


class Client:
    def __init__(self, secret_key, workspaceKey=None, base_url="https://api.seatsio.net"):
        self.base_url = base_url
        self.http_client = HttpClient(base_url, secret_key, workspaceKey)
        self.charts = ChartsClient(self.http_client)
        self.events = EventsClient(self.http_client)
        self.accounts = AccountsClient(self.http_client)
        self.subaccounts = SubaccountsClient(self.http_client)
        self.workspaces = WorkspacesClient(self.http_client)
        self.hold_tokens = HoldTokensClient(self.http_client)
        self.usage_reports = UsageReports(self.http_client)
