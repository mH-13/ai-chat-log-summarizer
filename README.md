<!-- Project Title & Badges -->
# AI Chat Log Summarizer  
[![PyPI version](https://img.shields.io/pypi/v/ai-chat-log-summarizer)]()  
[![Build Status](https://img.shields.io/github/actions/workflow/status/your-username/ai-chat-log-summarizer/ci.yml)]()

---

## Overview  
**AI Chat Log Summarizer** is a lightweight Python CLI tool that  
- Parses `.txt` chat logs (`User:` / `AI:`)  
- Computes message statistics  
- Extracts top keywords via frequency or TF-IDF  
- Generates a concise summary report  

This helps you quickly understand large chat transcripts without manual reading.

---

## Features  
- **Chat Parsing**: Splits lines into `User` / `AI` messages  
- **Statistics**: Counts total, user vs. AI messages  
- **Keyword Extraction**: Top-5 keywords (stopword-filtered)  
- **Summaries**: Outputs counts, top keywords, and “nature” insights  
- **Bonus**: `--tfidf` flag for TF-IDF–based keywords  
- **Batch Mode**: Summarize all `.txt` files in a folder

---

## Installation & Usage
```bash
git clone https://github.com/<your-username>/ai-chat-log-summarizer.git
cd ai-chat-log-summarizer

# Create & activate venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
---


*Summarizing Single file*

```bash
python main.py -i data/chat1.txt
```

**Output Example**

```text
--- chat1.txt ---
=== Conversation Summary ===
- Total messages: 8 (5 User, 3 AI)
- Top keywords: python, ai, data, use, language
- Nature: Questions about Python usage.
```

### Batch + TF-IDF

```bash
python main.py -i data/ --tfidf
```

---