import os
import unittest2
import unirest
import json
import uuid

import seatsio

BASE_URL = "https://api-staging.seats.io"


class SeatsioClientTest(unittest2.TestCase):

    def setUp(self):
        super(SeatsioClientTest, self).setUp()
        self.user = self.create_test_user()
        self.client = seatsio.Client(self.user["secretKey"], BASE_URL)

    def tearDown(self):
        super(SeatsioClientTest, self).tearDown()

    def newClient(self, secretKey):
        return seatsio.Client(secretKey, BASE_URL)

    def create_test_user(self):
        response = unirest.post(
            BASE_URL + "/system/public/users",
            headers={"Accept": "application/json"},
            params=json.dumps({
                "email": "test" + str(uuid.uuid4()) + "@seats.io",
                "password": "12345678"
            })
        )
        if response.code == 200:
            return response.body
        else:
            raise Exception("Failed to create a test user")

    def create_test_chart(self):
        with open(os.path.join(os.path.dirname(__file__), 'sampleChart.json'), 'r') as test_chart_json:
            data = test_chart_json.read().replace('\n', '')
            chart_key = str(uuid.uuid4())
            url = BASE_URL + "/system/public/" + self.user["designerKey"] + "/charts/" + chart_key
            print(url)
            response = unirest.post(
                url=url,
                headers={"Accept": "application/json"},
                params=data
            )
            if response.code == 201:
                return chart_key
            else:
                raise Exception("Failed to create a test user")
