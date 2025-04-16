class DatabaseConnectionError(Exception):
    """数据库连接异常"""
    pass

class QueryExecutionError(Exception):
    """查询执行异常"""
    pass