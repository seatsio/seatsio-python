from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class UpdateSubaccountTest(SeatsioClientTest):

    def test(self):
        subaccount = self.client.subaccounts.create("joske")
        email = self.random_email()

        self.client.subaccounts.update(subaccount.id, name="jefke", email=email)

        retrieved_subaccount = self.client.subaccounts.retrieve(subaccount.id)
        assert_that(retrieved_subaccount.name).is_equal_to("jefke")
        assert_that(retrieved_subaccount.email).is_equal_to(email)

    def test_emailIsOptional(self):
        email = self.random_email()
        subaccount = self.client.subaccounts.create_with_email(email, "joske")

        self.client.subaccounts.update(subaccount.id, name="jefke")

        retrieved_subaccount = self.client.subaccounts.retrieve(subaccount.id)
        assert_that(retrieved_subaccount.name).is_equal_to("jefke")
        assert_that(retrieved_subaccount.email).is_equal_to(email)

    def test_nameIsOptional(self):
        email = self.random_email()
        subaccount = self.client.subaccounts.create_with_email(email, "joske")

        self.client.subaccounts.update(subaccount.id, email=email)

        retrieved_subaccount = self.client.subaccounts.retrieve(subaccount.id)
        assert_that(retrieved_subaccount.name).is_equal_to("joske")
        assert_that(retrieved_subaccount.email).is_equal_to(email)
