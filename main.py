import logging.config
import sys
import io
import logging
import logging.config
from src.cli_interface import KnowledgeCLI

# 修复标准流的编码
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 安全的日志配置加载
try:
    with open('config/logging.conf', 'r', encoding='utf-8') as f:
        logging.config.fileConfig(f)
except Exception as e:
    logging.basicConfig(level=logging.INFO)
    logging.warning(f"无法加载日志配置: {str(e)}，使用基础配置")

if __name__ == "__main__":
    cli = KnowledgeCLI()
    cli.cmdloop()
from config import settings
from src.cli_interface import KnowledgeCLI

def setup_logging():
    logging.config.fileConfig("config/logging.conf")

if __name__ == "__main__":
    setup_logging()
    cli = KnowledgeCLI()
    cli.cmdloop()