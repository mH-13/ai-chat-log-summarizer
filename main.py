# Main script to run the tool. Serves as the CLI entry point, orchestrating parsing, analysis, keyword extraction, and summary printing. 

import argparse
import glob
import os
from summarizer.chat_parser import parse_chat
from summarizer.analyzer import message_stats
from summarizer.keyword_extractor import top_n_freq, top_n_tfidf
from summarizer.summarizer import generate_summary

#function to process a single file end to end
#Calls parser → analyzer → extractor → summarizer.
def process_file(path: str, use_tfidf: bool):
    turns = parse_chat(path)
    stats = message_stats(turns)
    if use_tfidf:
        kws = top_n_tfidf(turns)
    else:
        kws = top_n_freq(turns)
    summary = generate_summary(stats, kws)
    print(f"\n--- {os.path.basename(path)} ---")
    print(summary)

def main():
    p = argparse.ArgumentParser(
        description="AI Chat Log Summarizer"
    )
    p.add_argument(
        "--input", "-i", required=True, # -input/-i: required; accepts either a single file or folder
        help="Path to a .txt file or a folder containing .txt files"
    )
    p.add_argument(
        "--tfidf", action="store_true", # optional switch; when present, uses TF-IDF mode.
        help="Use TF-IDF for keyword extraction"
    )
    args = p.parse_args()

    paths = []
    if os.path.isdir(args.input):
        paths = glob.glob(os.path.join(args.input, "*.txt"))
    else:
        paths = [args.input]

    for path in paths:
        process_file(path, args.tfidf)

if __name__ == "__main__":
    main()
