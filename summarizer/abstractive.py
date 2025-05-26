# summarizer/abstractive.py

import re
from typing import List, Tuple
from transformers import pipeline, AutoTokenizer

def generate_abstractive_summary(
    turns: List[Tuple[str, str]],
    num_segments: int = 6,
    summary_ratio: float = 0.4,
    overlap: int = 50,
    **kwargs
) -> str:
    """
    1) Builds speaker-aware full text
    2) Chunks into N segments of roughly equal size
    3) Summarizes each segment with controlled decoding
    4) Joins segment summaries and bulletizes by sentence
    """

    # 1) Build the text
    doc = []
    for speaker, text in turns:
        token = "<USER>" if speaker == "User" else "<AI>"
        doc.append(f"{token} {text}")
    full_text = " ".join(doc)

    # 2) Prepare model + tokenizer
    model_name = "sshleifer/distilbart-cnn-12-6"
    summarizer = pipeline("summarization", model=model_name, device=-1)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    max_tokens = tokenizer.model_max_length

    # 3) Compute approximate tokens per segment
    tokens = tokenizer.tokenize(full_text)
    total_tokens = len(tokens)
    chunk_token_size = total_tokens // num_segments

    # 4) Build overlapping token‐based chunks
    chunks = []
    for i in range(num_segments):
        start = max(0, i * chunk_token_size - overlap)
        end = min(total_tokens, (i + 1) * chunk_token_size + overlap)
        chunk_text = tokenizer.convert_tokens_to_string(tokens[start:end])
        chunks.append(chunk_text)

    # 5) Summarize each chunk
    partial_summaries = []
    for chunk in chunks:
        # skip empty chunks
        if not chunk.strip():
            continue
        chunk_len = len(tokenizer.tokenize(chunk))
        max_len = max(20, int(chunk_len * summary_ratio))
        min_len = max(10, int(max_len * 0.3))

        out = summarizer(
            chunk,
            max_length=max_len,
            min_length=min_len,
            num_beams=4,
            no_repeat_ngram_size=3,
            repetition_penalty=2.0,
            early_stopping=True,
            **kwargs
        )
        partial_summaries.append(out[0]["summary_text"].strip())

    # 6) Combine & clean
    combined = " ".join(partial_summaries)
    # Remove duplicate sentences
    sentences = re.split(r'(?<=[.!?])\s+', combined)
    seen = set()
    unique = []
    for s in sentences:
        if s not in seen:
            seen.add(s)
            unique.append(s)

    # 7) Bulletize
    bullets = [f"- {s.rstrip('. ')}." for s in unique if s.strip()]
    return "\n".join(bullets)
