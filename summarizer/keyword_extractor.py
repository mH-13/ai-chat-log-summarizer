# Keyword extraction (basic + TF-IDF)  
#Provides two methods: frequency-based and TF-IDF keyword extraction from the parsed chat

import re
from collections import Counter
from typing import List, Tuple

import nltk
from nltk.corpus import stopwords #to filter out common words (e.g., “the”, “is”)

# Download once
nltk.download('stopwords', quiet=True)
STOPWORDS = set(stopwords.words('english'))

## Frequency-based keyword extraction: This method counts the frequency of each word in the chat and returns the top N words. It uses a simple regex to tokenize the text and filters out common stopwords. BUT this method is not very sophisticated and may not capture the most relevant keywords in a conversation.


def top_n_freq(turns: List[Tuple[str, str]], n: int = 5) -> List[Tuple[str, int]]:
    words = []
    for _, text in turns:
        tokens = re.findall(r'\b\w+\b', text.lower())
        words.extend(tok for tok in tokens if tok not in STOPWORDS)
    return Counter(words).most_common(n) # Returns the n most common words and their counts


# TF-IDF keyword extraction: This method uses the Term Frequency-Inverse Document Frequency (TF-IDF) algorithm to identify important words in the chat. It considers both the frequency of a word in a document and its rarity across all documents. This is more sophisticated than simple frequency counting and can yield better results for keyword extraction.

from sklearn.feature_extraction.text import TfidfVectorizer

def top_n_tfidf(turns: List[Tuple[str, str]], n: int = 5) -> List[Tuple[str, float]]:
    docs = [text for _, text in turns]
    vect = TfidfVectorizer(stop_words='english') #
    X = vect.fit_transform(docs)
    
    scores = X.mean(axis=0).A1 #computes the average TF-IDF per term across all turn and ranks them descendingly by score
    terms = vect.get_feature_names_out()
    ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
    return ranked[:n]
