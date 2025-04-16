import unittest
from src.query_builder import CypherQueryBuilder

class TestQueryBuilder(unittest.TestCase):
    def test_basic_search(self):
        query = CypherQueryBuilder.build_query(
            "basic_search",
            {"label": "Course", "limit": 10}
        )
        self.assertIn("MATCH (n:Course)", query)