from utils import preprocess_messages
from collections import Counter

from sentence_transformers import SentenceTransformer
from torch.nn.functional import cosine_similarity


#Turn each group into one big text (string) so we can embed it.
def build_group_corpus(path="telegram_messages_by_group.json"):
    preprocessed = preprocess_messages(path)
    corpora = {group: " ".join(tokens) for group, tokens in preprocessed.items()}
    return corpora


def detect_common_topics_embeddings(path="telegram_messages_by_group.json", model_name="all-MiniLM-L6-v2", threshold=0.5):
    """
    Compute semantic similarity between groups.
    Returns list of {group1, group2, similarity} for pairs above threshold.
    """
    corpora = build_group_corpus(path)
    model = SentenceTransformer(model_name)

    group_names = list(corpora.keys())
    texts = [corpora[g] for g in group_names]

    embeddings = model.encode(texts, convert_to_tensor=True)

    results = []
    for i in range(len(group_names)):
        for j in range(i + 1, len(group_names)):
            sim = float(cosine_similarity(embeddings[i], embeddings[j], dim=0))
            if sim >= threshold:
                results.append({
                    "group1": group_names[i],
                    "group2": group_names[j],
                    "similarity": sim
                })
    return results
