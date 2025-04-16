import spacy
from spacy.matcher import Matcher


class NLPProcessor:
    def __init__(self):
        self.nlp = spacy.load("zh_core_web_sm")
        self.matcher = Matcher(self.nlp.vocab)
        self._init_patterns()

    def _init_patterns(self):
        patterns = {
            "QUERY_TOOL": [[{"LOWER": "工具"}, {"LOWER": "支持"}]]
        }
        for label, pattern in patterns.items():
            self.matcher.add(label, pattern)

    def parse_intent(self, text: str):
        doc = self.nlp(text)
        matches = self.matcher(doc)
        return [self.nlp.vocab.strings[match_id] for match_id, _, _ in matches]