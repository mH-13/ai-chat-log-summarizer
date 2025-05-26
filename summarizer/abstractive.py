# summarizer/abstractive.py

import re
from typing import List, Tuple
from transformers import pipeline, AutoTokenizer

def generate_abstractive_summary(
    turns: List[Tuple[str, str]],
    num_segments: int = 6,
    summary_ratio: float = 0.5,
    overlap: int = 20,
    **kwargs
) -> str:
    """ 1) Builds speaker-aware full text
        2) Chunks into N segments of roughly equal size
        3) Summarizes each segment with controlled decoding
        4) Joins segment summaries and bulletizes by sentence """

    # Building the full text with speaker tags
    doc = []
    for speaker, text in turns:
        token = "<USER>" if speaker == "User" else "<AI>"
        doc.append(f"{token} {text}")
    full_text = " ".join(doc)

    #Loading the summarization model
    # Note: we can change the model to any other summarization model available on Hugging Face
    model_name = "sshleifer/distilbart-cnn-12-6"
    summarizer = pipeline("summarization", model=model_name, device=0) # Use device=-1 for CPU, or set to GPU id if available
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    max_tokens = tokenizer.model_max_length # e.g. 1024

    #Approx token per segment
    tokens = tokenizer.tokenize(full_text)
    total_tokens = len(tokens)
    chunk_token_size = total_tokens // num_segments

    #Building the overlaping token segments
    chunks = []
    for i in range(num_segments):
        start = max(0, i * chunk_token_size - overlap)
        end = min(total_tokens, (i + 1) * chunk_token_size + overlap)
        chunk_text = tokenizer.convert_tokens_to_string(tokens[start:end])
        chunks.append(chunk_text)

    #summarizing each chunk
    # Note: we can adjust the max_length and min_length based on the chunk size
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

    #Combining summaries for clearn output
    combined = " ".join(partial_summaries)
    # Remove duplicate sentences
    sentences = re.split(r'(?<=[.!?])\s+', combined)
    seen = set()
    unique = []
    for s in sentences:
        if s not in seen:
            seen.add(s)
            unique.append(s)

    # Bulletizing the unique sentences
    # Note: we can adjust the bullet format as needed
    bullets = [f"- {s.rstrip('. ')}." for s in unique if s.strip()]
    return "\n".join(bullets)