import tempfile
import unittest
from pathlib import Path

from stats_store import get_scoreboard, record_successful_bypass


class WorkshopStatsTests(unittest.TestCase):
    def test_records_and_aggregates_participant_breaks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database = Path(temp_dir) / "stats.sqlite3"
            record_successful_bypass("  Ada   Lovelace ", 50, database)
            record_successful_bypass("Ada Lovelace", 70, database)
            record_successful_bypass("Grace", 40, database)

            scoreboard = get_scoreboard(database)

        self.assertEqual(scoreboard["total_successful_breaks"], 3)
        self.assertEqual(scoreboard["participants"][0]["participant_alias"], "Ada Lovelace")
        self.assertEqual(scoreboard["participants"][0]["successful_breaks"], 2)
        self.assertEqual(scoreboard["participants"][0]["highest_percent"], 70)
        self.assertEqual(len(scoreboard["recent"]), 3)

    def test_rejects_empty_alias_and_non_breaks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database = Path(temp_dir) / "stats.sqlite3"
            with self.assertRaises(ValueError):
                record_successful_bypass("  ", 50, database)
            with self.assertRaises(ValueError):
                record_successful_bypass("Alex", 15, database)


if __name__ == "__main__":
    unittest.main()
