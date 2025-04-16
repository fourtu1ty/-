import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Neo4j 连接配置
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

    # 查询参数
    MAX_RESULTS = 10
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()