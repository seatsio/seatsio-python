from tests.helpers import SeatsioClientTest

class HelloWorldTests(SeatsioClientTest):

    def test_firsttest(self):
        assert True == True
        assert False == False

    def test_secondtest(self):
        self.assertEqual(1, 1)
