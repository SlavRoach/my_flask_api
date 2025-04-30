import unittest
from unittest.mock import patch
from server import app

class TestSearchAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch("server.call_google_api")
    def test_search_valid_keyword(self, mock_call):
        mock_call.return_value = {
            "items": [
                {"title": "Test Title", "link": "http://example.com", "snippet": "Test snippet"}
            ]
        }

        response = self.client.post("/search", json={"keyword": "test"})
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]["title"], "Test Title")
        self.assertEqual(data[0]["link"], "http://example.com")
        self.assertEqual(data[0]["snippet"], "Test snippet")

    def test_search_no_keyword(self):
        response = self.client.post("/search", json={"keyword": ""})
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Nebolo zadané kľúčové slovo")

    @patch("server.call_google_api")
    def test_search_empty_results(self, mock_call):
        mock_call.return_value = {"items": []}

        response = self.client.post("/search", json={"keyword": "empty"})
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    @patch("server.call_google_api")
    def test_search_api_error(self, mock_call):
        mock_call.side_effect = Exception("Chyba pri volaní Google API")

        response = self.client.post("/search", json={"keyword": "error"})
        self.assertEqual(response.status_code, 500)

        data = response.get_json()
        self.assertIn("Chyba pri volaní Google API", data["error"])

if __name__ == "__main__":
    unittest.main()
