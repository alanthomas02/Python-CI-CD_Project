import json
import threading
import unittest
from http.server import HTTPServer
from urllib.request import urlopen

from app import AppHandler


class HealthEndpointTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), AppHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(
            target=cls.server.serve_forever,
            daemon=True
        )
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_health_endpoint(self):
        with urlopen(
            f"http://127.0.0.1:{self.port}/health"
        ) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(
                response.headers.get("Content-Type"),
                "application/json"
            )
            data = json.loads(response.read().decode())

        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["application"], "python-cicd-ec2")


if __name__ == "__main__":
    unittest.main()
