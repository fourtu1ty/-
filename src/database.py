from py2neo import Graph
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class Neo4jConnection:
    """封装Neo4j数据库连接池"""
    def __init__(self):
        try:
            self.graph = Graph(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
                secure=True,  # 如果使用加密连接
                encodings='utf-8'  # 显式指定编码
            )
        except Exception as e:
            logging.error(f"数据库连接失败: {str(e)}")
            raise
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        try:
            self.graph = Graph(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
                max_connection_lifetime=3600
            )
            logger.info("Neo4j连接成功")
        except Exception as e:
            logger.error(f"数据库连接失败: {str(e)}")
            raise

    def execute_query(self, cypher: str, **kwargs) -> list:
        """执行Cypher查询并返回格式化结果"""
        try:
            result = self.graph.run(cypher, **kwargs).data()
            logger.debug(f"执行查询: {cypher[:50]}...")
            return result
        except Exception as e:
            logger.error(f"查询执行错误: {str(e)}")
            return []