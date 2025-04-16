class CypherQueryBuilder:
    QUERY_TEMPLATES = {
        "basic_search": """
        MATCH (n:{label})
        WHERE toLower(n.name) CONTAINS toLower($keyword)
        RETURN n
        LIMIT {limit}
        """,
        "module_search": """
        MATCH (c:Course)-[:HAS_MODULE]->(m:Module)-[:CONTAINS_CHAPTER]->(ch:Chapter)
        WHERE toLower(ch.name) CONTAINS toLower($kw)
        RETURN c, m, ch
        """,
        "tech_search": """
        MATCH (t:Tech)<-[:USES_TECH]-(ch:Chapter)
        WHERE toLower(t.name) CONTAINS toLower($kw)
        RETURN ch, t
        """,
        "case_search": """
        MATCH (ic:IndustryCase)-[:USES_TECH]->(t:Tech)
        WHERE toLower(ic.name) CONTAINS toLower($kw)
        RETURN ic, t
        """
    }

    @classmethod
    def build_query(cls, template_name: str, params: dict):
        template = cls.QUERY_TEMPLATES.get(template_name)
        if not template:
            raise ValueError(f"无效模板: {template_name}")
        return template.format(**params)