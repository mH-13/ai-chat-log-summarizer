# summarizer/abstractive.py

from typing import List, Tuple

def generate_abstractive_summary(
    turns: List[Tuple[str, str]],
    max_length: int = 450,
    min_length: int = 40,
    **kwargs
) -> str:
    """Builds a speaker-aware input string from 'turns', then
    lazily initializes and calls the HF summarization pipeline."""
    # 1) Build the combined document with speaker tokens
    doc = []
    for speaker, text in turns:
        token = "<USER>" if speaker == "User" else "<AI>"
        doc.append(f"{token} {text}")
    full_text = " ".join(doc)

    # 2) Lazy import & init of the pipeline
    from transformers import pipeline
    summarizer = pipeline(
        "summarization",
        # model="facebook/bart-large-cnn",  # or your chosen model
        #switching smaller modlel for faster inference\
        model="sshleifer/distilbart-cnn-12-6",
        device=-1                            # -1 for CPU
    )

    # 3) Run summarization only now
    result = summarizer(
        full_text,
        max_length=max_length,
        min_length=min_length,
        **kwargs
    )
    return result[0]["summary_text"]


#this code has issue to working with large size of txt file. 
#otherwise, it works well with small size of txt file.