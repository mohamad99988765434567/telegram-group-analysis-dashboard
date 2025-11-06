# Telegram Group Analysis Dashboard

## Overview
This project collects messages from public Telegram groups and analyzes the main discussion topics.
It uses `Telethon` to fetch messages, `Streamlit` for visualization, and `sentence-transformers` for semantic similarity.

## Features
- Scrapes messages per group and stores them in JSON
- Cleans and tokenizes text (Arabic + English)
- Displays top keywords and hashtags per group
- Detects shared topics and semantic similarity between groups
- Interactive dashboard built with Streamlit

## Project structure
