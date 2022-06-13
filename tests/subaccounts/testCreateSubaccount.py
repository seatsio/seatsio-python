from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CreateSubaccountTest(SeatsioClientTest):

    def test(self):
        subaccount = self.client.subaccounts.create("joske")

        assert_that(subaccount.secret_key).is_not_blank()
        assert_that(subaccount.designer_key).is_not_blank()
        assert_that(subaccount.public_key).is_not_blank()
        assert_that(subaccount.name).is_equal_to("joske")
        assert_that(subaccount.active).is_true()

    def test_name_is_optional(self):
        subaccount = self.client.subaccounts.create()
        assert_that(subaccount.name).is_not_blank()
