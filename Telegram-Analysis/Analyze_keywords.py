from collections import Counter
from utils import preprocess_messages
import arabic_reshaper
from bidi.algorithm import get_display


def get_top_terms_per_group(n, path="telegram_messages_by_group.json"):
    """
    Return the top n frequent words for each group.
    Uses the preprocessed (cleaned) tokens.
    """
    preprocessed = preprocess_messages(path)
    result = {}
    for group, tokens in preprocessed.items():
        freq = Counter(tokens)
        result[group] = freq.most_common(n)
    return result


def get_top_hashtags_per_group(n, path="telegram_messages_by_group.json"):
    """
    Return the top n hashtags for each group.
    """
    preprocessed = preprocess_messages(path)
    result = {}
    for group, tokens in preprocessed.items():
        hashtags = [t for t in tokens if t.startswith("#")]
        freq = Counter(hashtags)
        result[group] = freq.most_common(n)
    return result


def get_keyword_overlap(top_k, path="telegram_messages_by_group.json"):
    """
    Return overlap of top_k keywords between all pairs of groups.
    """
    preprocessed = preprocess_messages(path)

    # get top-k per group
    top_keywords = {
        group: set([w for w, _ in Counter(tokens).most_common(top_k)])
        for group, tokens in preprocessed.items()
    }

    overlaps = []
    groups = list(top_keywords.keys())
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            g1, g2 = groups[i], groups[j]
            overlap = top_keywords[g1] & top_keywords[g2]
            if overlap:
                overlaps.append({
                    "group1": g1,
                    "group2": g2,
                    "common_keywords": list(overlap)
                })
    return overlaps



if __name__ == "__main__":
    
    # here , i need to fix the arabic display issue in the output , i used arabic_reshaper and bidi libraries to reshape and reorder the text for proper display.
    top_terms = get_top_terms_per_group(5)
    print("\nTop 5 terms per group:")
    for group, terms in top_terms.items():
        # Reshape and reorder Arabic text for both group name and terms
        group_display = get_display(arabic_reshaper.reshape(group))
        formatted_terms = []
        for term, count in terms:
            reshaped_term = get_display(arabic_reshaper.reshape(term))
            formatted_terms.append((reshaped_term, count))
        print(f"{group_display}:")
        for term, count in formatted_terms:
            print(f"  - {term}: {count}")

    # Get top hashtags
    top_hashtags = get_top_hashtags_per_group(5)
    print("\nTop 5 hashtags per group:")
    for group, hashtags in top_hashtags.items():
        group_display = get_display(arabic_reshaper.reshape(group))
        formatted_hashtags = []
        for hashtag, count in hashtags:
            reshaped_hashtag = get_display(arabic_reshaper.reshape(hashtag))
            formatted_hashtags.append((reshaped_hashtag, count))
        print(f"{group_display}:")
        for hashtag, count in formatted_hashtags:
            print(f"  - {hashtag}: {count}")

    overlaps = get_keyword_overlap(5)
    print("\nKeyword overlaps between groups:")
    for overlap in overlaps:
        # Reshape group names
        group1_display = get_display(arabic_reshaper.reshape(overlap['group1']))
        group2_display = get_display(arabic_reshaper.reshape(overlap['group2']))
        
        # Reshape common keywords
        formatted_keywords = [get_display(arabic_reshaper.reshape(k)) for k in overlap['common_keywords']]
        
        print(f"{group1_display} & {group2_display}:")
        for keyword in formatted_keywords:
            print(f"  - {keyword}")