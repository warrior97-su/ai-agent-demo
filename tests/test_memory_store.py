import tempfile
import unittest
from pathlib import Path

from agent.memory_store import SQLiteMemoryStore


class SQLiteMemoryStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store = SQLiteMemoryStore(Path(self.temp_dir.name) / "memory.db")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_upsert_updates_an_existing_fact(self):
        self.store.upsert_fact("default", "profile", "city", "上海")
        self.store.upsert_fact("default", "profile", "city", "杭州")

        facts = self.store.list_facts("default")

        self.assertEqual(len(facts), 1)
        self.assertEqual(facts[0]["value"], "杭州")

    def test_forget_hides_a_fact_and_upsert_reactivates_it(self):
        self.store.upsert_fact("default", "profile", "name", "阿大")

        self.assertTrue(self.store.forget_fact("default", "profile", "name"))
        self.assertEqual(self.store.list_facts("default"), [])

        self.store.upsert_fact("default", "profile", "name", "大啊")
        facts = self.store.list_facts("default")

        self.assertEqual(len(facts), 1)
        self.assertEqual(facts[0]["value"], "大啊")

    def test_facts_are_isolated_between_users(self):
        self.store.upsert_fact("alice", "profile", "city", "南京")
        self.store.upsert_fact("bob", "profile", "city", "北京")

        self.assertEqual(self.store.list_facts("alice")[0]["value"], "南京")
        self.assertEqual(self.store.list_facts("bob")[0]["value"], "北京")


if __name__ == "__main__":
    unittest.main()
