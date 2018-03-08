import unittest2
import unirest
import json
import uuid

import seatsio

BASE_URL = "https://api-staging.seats.io"


class SeatsioClientTest(unittest2.TestCase):

    def setUp(self):
        super(SeatsioClientTest, self).setUp()
        self.user = self.createTestUser()
        self.client = seatsio.Client(self.user["secretKey"], BASE_URL)

    def tearDown(self):
        super(SeatsioClientTest, self).tearDown()

    def createTestUser(self):
        response = unirest.post(
            BASE_URL + "/system/public/users",
            headers={"Accept": "application/json"},
            params=json.dumps({
                "email": "test" + str(uuid.uuid4()) + "@seats.io",
                "password": "12345678"
            })
        )
        if (response.code == 200):
            return response.body
        else:
            raise Exception("Failed to create a test user")
