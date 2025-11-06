# Telegram Group Analysis Dashboard

## Overview
This project analyzes public Telegram groups to understand the main discussion topics and relationships between them.  
It uses Telethon to fetch messages, Streamlit for visualization, and Sentence Transformers to detect semantic similarity between groups.

The goal is to explore trends in AI-related Telegram communities (both Arabic and English), showing what people discuss most and how different groups overlap in topics and meaning.

---

## Features
- Collects and stores Telegram messages from multiple groups in a structured JSON format  
- Cleans and tokenizes text in both Arabic and English  
- Displays top keywords and hashtags per group  
- Detects shared topics between groups based on keyword overlap  
- Calculates semantic similarity between groups using embeddings  
- Presents all results interactively in a Streamlit dashboard  

---

## Analysis Summary
After collecting and cleaning the data, the system identifies the most frequent words and hashtags in each group.  
It then compares groups to find overlapping topics and computes similarity scores using sentence embeddings.  

The analysis revealed strong overlap among Arabic AI groups, with recurring topics like الذكاء الاصطناعي (artificial intelligence), أدوات (tools), and محتوى (content).  
In English-speaking groups, keywords such as AI, ChatGPT, OpenAI, and Python were among the most common, reflecting the popularity of generative AI discussions.

---

## Technologies Used
| Category | Tools |
|-----------|--------|
| Data Collection | Telethon |
| Data Cleaning | Python, Regular Expressions |
| Semantic Similarity | Sentence Transformers |
| Visualization | Streamlit |
| Language Support | Arabic and English |





