from py2neo import Graph, NodeMatcher
import re


class Neo4jConnection:
    def __init__(self):
        # 连接Neo4j
        self.graph = Graph("neo4j://localhost:7687", auth=("neo4j", "yzm643534474"))
        self.matcher = NodeMatcher(self.graph)

    def _execute_query(self, cypher, **kwargs):
        """执行Cypher查询并返回格式化结果"""
        try:
            data = self.graph.run(cypher, **kwargs).data()
            return [self._format_record(record) for record in data]
        except Exception as e:
            print(f"查询错误: {str(e)}")
            return []

    @staticmethod
    def _format_record(record):
        """格式化单条记录为自然语言"""
        parts = []
        for key, value in record.items():
            if isinstance(value, dict):  # 处理节点属性
                label = list(value.labels)[0] if value.labels else "实体"
                props = {k: v for k, v in value.items() if k != 'name'}
                parts.append(f"{label}[{value['name']}] {props}")
            elif isinstance(value, list):  # 处理路径
                parts.extend([f"{n['name']}({n.labels})" for n in value if 'name' in n])
        return " → ".join(parts)

    def search_knowledge(self, keyword):
        """核心检索方法"""
        # 清理输入
        clean_keyword = re.sub(r"[^\w\s]", "", keyword).strip()

        # 执行多维度查询
        queries = [
            # 课程基本信息查询
            ("MATCH (c:Course) WHERE toLower(c.name) CONTAINS toLower($kw) RETURN c", "课程"),
            # 模块章节查询
            ("""
            MATCH (c:Course)-[:HAS_MODULE]->(m:Module)-[:CONTAINS_CHAPTER]->(ch:Chapter)
            WHERE toLower(ch.name) CONTAINS toLower($kw)
            RETURN c, m, ch
            """, "章节"),
            # 技术栈查询
            ("""
            MATCH (t:Tech)<-[:USES_TECH]-(ch:Chapter)
            WHERE toLower(t.name) CONTAINS toLower($kw)
            RETURN ch, t
            """, "技术"),
            # 行业案例查询
            ("""
            MATCH (ic:IndustryCase)-[:USES_TECH]->(t:Tech)
            WHERE toLower(ic.name) CONTAINS toLower($kw)
            RETURN ic, t
            """, "案例")
        ]

        # 执行所有查询并合并结果
        results = []
        for query, category in queries:
            records = self._execute_query(query, kw=clean_keyword)
            if records:
                results.append(f"=== {category}相关信息 ===")
                results.extend(records)

        return "\n".join(results) if results else "未找到相关信息"