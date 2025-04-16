import spacy
from spacy.matcher import Matcher


class NLPProcessor:
    """自然语言处理与意图识别"""

    def __init__(self):
        self.nlp = spacy.load("zh_core_web_sm")
        self._init_patterns()

    def _init_patterns(self):
        # 定义意图识别规则
        self.matcher = Matcher(self.nlp.vocab)
        patterns = {
            "QUERY_TOOL": [
                [{"LOWER": "哪些"}, {"LOWER": "工具"}, {"LOWER": "支持"}],
                [{"LOWER": "用什么"}, {"LOWER": "工具"}]
            ],
            "QUERY_PAPER": [
                [{"LOWER": "论文"}, {"LOWER": "引用"}]
            ]
        }
        for label, pattern in patterns.items():
            self.matcher.add(label, pattern)

    def parse_intent(self, text: str) -> str:
        """解析用户意图"""
        doc = self.nlp(text)
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            return self.nlp.vocab.strings[match_id]
        return "DEFAULT"