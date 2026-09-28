import unittest
from datetime import datetime

from assistant_utils import build_local_response, extract_intent, normalize_query, parse_reminder


class AssistantUtilsTests(unittest.TestCase):
    def test_normalize_query(self):
        self.assertEqual(normalize_query("  Hello   WORLD  "), "hello world")

    def test_extract_time_intent(self):
        result = extract_intent("what time is it")
        self.assertEqual(result["type"], "time")

    def test_build_local_response(self):
        response = build_local_response("tell me a joke")
        self.assertIn("programmers", response.lower())

    def test_date_time_intent(self):
        result = extract_intent("say the date and time")
        self.assertEqual(result["type"], "date_time")

    def test_parse_reminder(self):
        now = datetime(2026, 7, 2, 12, 0, 0)
        reminder = parse_reminder("set reminder to drink water in 10 minutes", now)
        self.assertIsNotNone(reminder)
        self.assertEqual(reminder["message"], "drink water")


if __name__ == "__main__":
    unittest.main()
