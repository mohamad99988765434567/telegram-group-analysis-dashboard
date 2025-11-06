import re
import json

STOPWORDS = {"من", "في", "على", "عن", "إلى", "الى", "و", "او", "the", "and"} # sample stopwords

def clean_text(text: str):
    """Clean and tokenize text."""
    if not text:
        return []
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9#@_\s\u0600-\u06FF]", "", text)
    tokens = text.lower().split()

    cleaned = []
    for t in tokens:
        # skip numbers
        if t.isdigit():
            continue
        # skip very short
        if len(t) < 2:
            continue
        # skip stopwords
        if t in STOPWORDS:
            continue
        cleaned.append(t)
    return cleaned



def load_data(path="telegram_messages_by_group.json"):
    """Load messages JSON from file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def preprocess_messages(path="telegram_messages_by_group.json"):
    """Load and clean all messages once per group."""
    data = load_data(path)
    processed = {}

    for group, msgs in data.items():
        tokens = []
        for m in msgs:
            tokens += clean_text(m.get("message_text", ""))
        processed[group] = tokens

    return processed
