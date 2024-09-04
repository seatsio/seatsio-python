import os
import unittest
import uuid
import time

import requests

import seatsio
from seatsio.region import Region

BASE_URL = "https://api-staging-eu.seatsio.net"


class SeatsioClientTest(unittest.TestCase):

    def setUp(self):
        super(SeatsioClientTest, self).setUp()
        company = self.create_test_company()
        self.user = company["admin"]
        self.workspace = seatsio.Workspace.create(company["workspace"])
        self.client = self.create_client(self.user["secretKey"], None)

    def tearDown(self):
        super(SeatsioClientTest, self).tearDown()

    def newClient(self, secret_key):
        return seatsio.Client(Region(BASE_URL), secret_key)

    def create_test_company(self):
        response = requests.post(BASE_URL + "/system/public/users/actions/create-test-company")
        if response.ok:
            return response.json()
        else:
            raise Exception("Failed to create a test user")

    @staticmethod
    def create_client(secret_key, workspace_key):
        return seatsio.Client(Region(BASE_URL), secret_key, workspace_key)

    @staticmethod
    def random_email():
        return str(uuid.uuid4()) + "@mailinator.com"

    def create_test_chart(self):
        return self.create_test_chart_from_file('sampleChart.json')

    def create_test_chart_with_sections(self):
        return self.create_test_chart_from_file('sampleChartWithSections.json')

    def create_test_chart_with_floors(self):
        return self.create_test_chart_from_file('sampleChartWithFloors.json')

    def create_test_chart_with_zones(self):
        return self.create_test_chart_from_file('sampleChartWithZones.json')

    def create_test_chart_with_tables(self):
        return self.create_test_chart_from_file('sampleChartWithTables.json')

    def create_test_chart_with_errors(self):
        return self.create_test_chart_from_file('sampleChartWithErrors.json')

    def create_test_chart_from_file(self, file):
        with open(os.path.join(os.path.dirname(__file__), file), 'r') as test_chart_json:
            data = test_chart_json.read().replace('\n', '')
            chart_key = str(uuid.uuid4())
            url = BASE_URL + "/system/public/charts/" + chart_key
            response = requests.post(
                url=url,
                headers={"Accept": "application/json"},
                data=data,
                auth=(self.user["secretKey"], ''),
            )
            if response.status_code == 201:
                return chart_key
            else:
                raise Exception("Failed to create a test user")

    def wait_for_status_changes(self, event, num_status_changes):
        start = time.time()
        while True:
            status_changes = self.client.events.status_changes(event.key).list()
            if len(list(status_changes)) != num_status_changes:
                if time.time() - start > 10:
                    raise Exception("No status changes for event " + event.key)
                else:
                    time.sleep(1)
            else:
                return status_changes

    def demo_company_secret_key(self):
        return os.environ["DEMO_COMPANY_SECRET_KEY"]

    def assert_demo_company_secret_key_set(self):
        if "DEMO_COMPANY_SECRET_KEY" not in os.environ:
            self.skipTest("DEMO_COMPANY_SECRET_KEY environment variable not set, skipping test")
