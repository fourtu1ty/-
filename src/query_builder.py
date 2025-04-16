from typing import Dict, List
import re


class CypherQueryBuilder:
    """动态生成Cypher查询语句"""

    QUERY_TEMPLATES = {
        "basic_search": """
        MATCH (n:{label})
        WHERE toLower(n.name) CONTAINS toLower($keyword)
        RETURN n
        LIMIT {limit}
        """,

        "multi_hop_relation": """
        MATCH path=(start:{start_label})-[*1..3]-(end:{end_label})
        WHERE toLower(start.name) CONTAINS toLower($keyword)
        RETURN nodes(path) AS nodes, relationships(path) AS rels
        LIMIT {limit}
        """,

        "tool_support": """
        MATCH (t:Tool)-[:SUPPORTS]->(a:Algorithm)
        WHERE toLower(t.name) CONTAINS toLower($keyword) 
           OR toLower(a.name) CONTAINS toLower($keyword)
        RETURN t, a
        """
    }

    @classmethod
    def build_query(cls, template_name: str, params: Dict) -> str:
        """根据模板名称和参数生成查询语句"""
        template = cls.QUERY_TEMPLATES.get(template_name)
        if not template:
            raise ValueError(f"未知查询模板: {template_name}")

        # 替换占位符
        query = template.format(**params)
        # 清理多余换行符
        return re.sub(r'\n\s+', ' ', query).strip()