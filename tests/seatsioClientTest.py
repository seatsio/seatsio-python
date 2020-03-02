import os
import uuid

import requests
import unittest2

import seatsio
from seatsio.domain import Subaccount

BASE_URL = "https://api-staging.seatsio.net"


class SeatsioClientTest(unittest2.TestCase):

    def setUp(self):
        super(SeatsioClientTest, self).setUp()
        company = self.create_test_company()
        self.user = company["admin"]
        self.subaccount = Subaccount(company["subaccount"])
        self.client = self.create_client(self.user["secretKey"], None)

    def tearDown(self):
        super(SeatsioClientTest, self).tearDown()

    def newClient(self, secret_key):
        return seatsio.Client(secret_key, None, BASE_URL)

    def create_test_company(self):
        response = requests.post(BASE_URL + "/system/public/users/actions/create-test-company")
        if response.ok:
            return response.json()
        else:
            raise Exception("Failed to create a test user")

    @staticmethod
    def create_client(secretKey, workspaceKey):
        return seatsio.Client(secretKey, workspaceKey, BASE_URL)

    @staticmethod
    def random_email():
        return str(uuid.uuid4()) + "@mailinator.com"

    def create_test_chart(self):
        return self.create_test_chart_from_file('sampleChart.json')

    def create_test_chart_with_sections(self):
        return self.create_test_chart_from_file('sampleChartWithSections.json')

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
