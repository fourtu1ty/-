import cmd
from src.database import Neo4jConnection


class KnowledgeCLI(cmd.Cmd):
    prompt = "(知识图谱) > "
    intro = "欢迎使用智能数据工程问答系统！输入 'exit' 或 'quit' 退出。"

    def __init__(self):
        super().__init__()
        self.qa = Neo4jConnection()

    def default(self, line):
        """处理用户输入的问题"""
        if line.lower() in ("exit", "quit"):
            return self.do_exit(line)
        if line.startswith("feedback:"):
            feedback = line.split(":", 1)[1].strip()
            self.handle_feedback(feedback)
        else:
            answer = self.qa.search_knowledge(line)
            print(f"\n答案：\n{answer}")

    def handle_feedback(self, feedback):
        """处理用户反馈"""
        if "差" in feedback:
            print("用户反馈消极，考虑优化问答策略。")
        elif "不错" in feedback:
            print("用户反馈积极，继续保持当前策略。")
        else:
            print("中立反馈，继续观察。")

    def do_exit(self, arg):
        return True