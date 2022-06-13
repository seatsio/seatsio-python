from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RegenerateSubaccountSecretKeyTest(SeatsioClientTest):

    def test(self):
        subaccount = self.client.subaccounts.create()

        self.client.subaccounts.regenerate_secret_key(subaccount.id)

        retrieved_subaccount = self.client.subaccounts.retrieve(subaccount.id)
        assert_that(retrieved_subaccount.secret_key).is_not_blank().is_not_equal_to(subaccount.secret_key)
