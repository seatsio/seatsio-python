from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class FilterSubaccountsTest(SeatsioClientTest):

    def test(self):
        subaccount1 = self.client.subaccounts.create("test1")
        subaccount2 = self.client.subaccounts.create("test2")
        subaccount3 = self.client.subaccounts.create("test3")

        subaccounts = self.client.subaccounts.list("test2")

        assert_that(subaccounts).extracting("id").contains_exactly(subaccount2.id)

    def test_on_first_page(self):
        subaccount1 = self.client.subaccounts.create("test1")
        subaccount2 = self.client.subaccounts.create("test2")
        subaccount3 = self.client.subaccounts.create("test3")

        subaccounts = self.client.subaccounts.list_first_page(filter="test2")

        assert_that(subaccounts.items).extracting("id").contains_exactly(subaccount2.id)

    def test_on_previous_page(self):
        subaccount1 = self.client.subaccounts.create("test-/@/11")
        subaccount2 = self.client.subaccounts.create("test-/@/12")
        subaccount3 = self.client.subaccounts.create("test-/@/33")
        self.client.subaccounts.create("test-/@/4")
        self.client.subaccounts.create("test-/@/5")
        self.client.subaccounts.create("test-/@/6")
        self.client.subaccounts.create("test-/@/7")
        self.client.subaccounts.create("test-/@/8")

        subaccounts = self.client.subaccounts.list_page_after(subaccount3.id, filter="test-/@/1")

        assert_that(subaccounts.items).extracting("id").contains_exactly(subaccount2.id, subaccount1.id)

    def test_on_next_page(self):
        subaccount1 = self.client.subaccounts.create("test-/@/11")
        subaccount2 = self.client.subaccounts.create("test-/@/12")
        subaccount3 = self.client.subaccounts.create("test-/@/13")
        self.client.subaccounts.create("test-/@/4")
        self.client.subaccounts.create("test-/@/5")
        self.client.subaccounts.create("test-/@/6")
        self.client.subaccounts.create("test-/@/7")
        self.client.subaccounts.create("test-/@/8")

        subaccounts = self.client.subaccounts.list_page_before(subaccount1.id, filter="test-/@/1")

        assert_that(subaccounts.items).extracting("id").contains_exactly(subaccount3.id, subaccount2.id)
