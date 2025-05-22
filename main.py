# Main script to run the tool. Serves as the CLI entry point, orchestrating parsing, analysis, keyword extraction, and summary printing. 

import argparse
import glob
import os
from summarizer.chat_parser import parse_chat
from summarizer.analyzer import message_stats
from summarizer.keyword_extractor import top_n_freq, top_n_tfidf
from summarizer.summarizer import generate_summary
from summarizer.abstractive import generate_abstractive_summary  # <-- new import



#function to process a single file end to end
#Calls parser → analyzer → extractor → summarizer.
def process_file(path: str, use_tfidf: bool, use_abstractive: bool):
    
    # 1) Parsing the chat turns
    turns = parse_chat(path)
    print(f"Parsed {len(turns)} turns from {os.path.basename(path)}")
    # If using abstractive summarization, call the function and return
    
    # 2) Computing stats & keywords for both modes
    stats = message_stats(turns)
    kws = top_n_tfidf(turns) if use_tfidf else top_n_freq(turns)
    top_keys = [kw for kw, _ in kws]

    # 3) Printing the extractive-style summary block
    print("\nSummary:")
    print(f"- The conversation had {stats['total_messages']} exchanges.")
    

    nature = top_keys[0] if top_keys else "general topics"
    print(f"- The user asked mainly about {nature}.")
    print(f"- Most common keywords: {', '.join(top_keys)}.\n")
    
    # 4) Branch on summarization mode
    if use_abstractive:
        #skilp stats/keywords and go straight to abstractive summary
        abstractive = generate_abstractive_summary(turns)
        print("=== Abstractive Summary ===")
        print(abstractive)
        return
    else:
        # Extractive fallback
        summary = generate_summary(stats, kws)
        print(f"\n--- {os.path.basename(path)} (Extractive) ---")
        print(summary)
    
    # Otherwise, proceed with the original pipeline
    # # Generate stats and keywords 
    
    # stats = message_stats(turns)
    # if use_tfidf:
    #     kws = top_n_tfidf(turns)
    # else:
    #     kws = top_n_freq(turns)
    
    # summary = generate_summary(stats, kws)
    # print(f"\n--- {os.path.basename(path)} ---")
    # print(summary)

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
    p.add_argument("--abstractive", action="store_true", # optional switch; when present, uses abstractive summarization.
        help="Use transformer based  abstractive summarization" # <--new argument
    )
    
    
    args = p.parse_args()

    paths = []
    
    if os.path.isdir(args.input):
        paths = glob.glob(os.path.join(args.input, "*.txt"))
    else:
        paths = [args.input]

    for path in paths:
        process_file(path, args.tfidf, args.abstractive) # <-- pass the new argument

if __name__ == "__main__":
    main()
