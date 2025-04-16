import cmd
from src.database import Neo4jConnection
from src.query_builder import CypherQueryBuilder


class KnowledgeCLI(cmd.Cmd):
    """交互式命令行界面"""

    prompt = "\n(知识图谱) > "
    intro = "欢迎使用智能数据工程知识问答系统！输入 help 查看命令列表"

    def __init__(self):
        super().__init__()
        self.conn = Neo4jConnection()
        self.current_page = 1

    def do_search(self, arg):
        """执行搜索: search <关键词> [--page 页码]"""
        # 解析参数
        args = arg.split()
        keyword = args[0]
        page = 1
        if "--page" in args:
            page_index = args.index("--page")
            page = int(args[page_index + 1])

        # 构建查询
        query = CypherQueryBuilder.build_query(
            "basic_search",
            {"label": "Course", "limit": 10}
        )
        results = self.conn.execute_query(query, keyword=keyword)

        # 分页显示
        self._display_results(results, page)

    def _display_results(self, results: list, page: int):
        # 实现分页逻辑
        pass

    def do_exit(self, arg):
        """退出系统: exit"""
        print("感谢使用！")
        return True