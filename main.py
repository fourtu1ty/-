import sys
import logging
import logging.config
from src.cli_interface import KnowledgeCLI

def setup_logging():
    try:
        with open('config/logging.conf', 'r', encoding='utf-8') as f:
            logging.config.fileConfig(f)
    except Exception as e:
        logging.basicConfig(level=logging.INFO)
        logging.warning(f"日志配置加载失败: {str(e)}")

if __name__ == "__main__":
    setup_logging()
    cli = KnowledgeCLI()
    cli.cmdloop()