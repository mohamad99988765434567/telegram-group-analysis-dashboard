import streamlit as st
import pandas as pd
from collections import Counter
from utils import preprocess_messages
from Analyze_keywords import get_top_terms_per_group
from detect_common import detect_common_topics_embeddings


def main():
    st.title("Telegram groups analysis")

    json_path = "telegram_messages_by_group.json"

    # sidebar
    st.sidebar.header("Options")
    top_n = st.sidebar.number_input("Top terms per group", min_value=3, max_value=50, value=10)
    top_k_overlap = st.sidebar.number_input("Top-K for keyword overlap", min_value=10, max_value=200, value=50)
    sim_threshold = st.sidebar.slider("Semantic similarity threshold", 0.3, 0.9, 0.6)

    # preprocess
    messages_by_group = preprocess_messages(json_path)

    # 1. top terms per group
    st.subheader("Top terms per group")
    top_terms = get_top_terms_per_group(top_n, json_path)

    for group, terms in top_terms.items():
        st.write(f"**{group}**")
        if terms:
            words = [w for (w, _) in terms]
            counts = [c for (_, c) in terms]
            df = pd.DataFrame({"word": words, "count": counts})
            st.bar_chart(df, x="word", y="count")
        else:
            st.write("no terms")

    # 2. shared topics by keyword
    st.subheader("Shared topics (by keyword)")
    group_top = {}
    for group, tokens in messages_by_group.items():
        freq = Counter(tokens)
        group_top[group] = [w for (w, _) in freq.most_common(top_k_overlap)]

    from collections import defaultdict
    kw_to_groups = defaultdict(list)
    for group, words in group_top.items():
        for w in words:
            kw_to_groups[w].append(group)

    shared = {k: v for k, v in kw_to_groups.items() if len(v) > 1}

    if shared:
            df_shared = pd.DataFrame(
                [{"keyword": k, "groups": ", ".join(v)} for k, v in shared.items()]
                )
            st.dataframe(df_shared, width=True)
    else:
        st.write("no shared keywords found")

    # 3. semantic similarities (embeddings)
    st.subheader("Similar groups (by embeddings)")
    try:
        pairs = detect_common_topics_embeddings(path=json_path, threshold=sim_threshold)
        if pairs:
            for p in pairs:
                st.write(f"{p['group1']}  <->  {p['group2']}    similarity={p['similarity']:.3f}")
        else:
            st.write("no similar pairs above threshold")
    except Exception as e:
        st.warning(f"embedding step failed: {e}")


if __name__ == "__main__":
    main()
