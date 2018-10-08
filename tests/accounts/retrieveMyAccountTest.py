from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrieveMyAccountTest(SeatsioClientTest):

    def test(self):
        account = self.client.accounts.retrieve_my_account()

        assert_that(account.secret_key).is_not_blank()
        assert_that(account.designer_key).is_not_blank()
        assert_that(account.public_key).is_not_blank()
        assert_that(account.email).is_not_blank()
        assert_that(account.settings.draftChartDrawingsEnabled).is_true()
        assert_that(account.settings.chartValidation.validateDuplicateLabels).is_equal_to("ERROR")
        assert_that(account.settings.chartValidation.validateObjectsWithoutCategories).is_equal_to("ERROR")
        assert_that(account.settings.chartValidation.validateUnlabeledObjects).is_equal_to("ERROR")
