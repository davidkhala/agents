import unittest
from davidkhala.ai.agent.ragflow import Client

class ClientTest(unittest.TestCase):
    def setUp(self):
        self.client = Client("ragflow-EzMTA0ZTg4YmE1YTExZjA5ZTk4NTI0Nz")
    def test_datasets(self):
        print(self.client.datasets)

if __name__ == "__main__":
    unittest.main()