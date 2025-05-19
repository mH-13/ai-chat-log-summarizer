## Keyword extraction (basic + TF-IDF)  

import re
from collections import Counter
from typing import List, Tuple

import nltk
from nltk.corpus import stopwords

# Download once
nltk.download('stopwords', quiet=True)
STOPWORDS = set(stopwords.words('english'))

def top_n_freq(turns: List[Tuple[str, str]], n: int = 5) -> List[Tuple[str, int]]:
    words = []
    for _, text in turns:
        tokens = re.findall(r'\b\w+\b', text.lower())
        words.extend(tok for tok in tokens if tok not in STOPWORDS)
    return Counter(words).most_common(n)



from sklearn.feature_extraction.text import TfidfVectorizer

def top_n_tfidf(turns: List[Tuple[str, str]], n: int = 5) -> List[Tuple[str, float]]:
    docs = [text for _, text in turns]
    vect = TfidfVectorizer(stop_words='english')
    X = vect.fit_transform(docs)
    scores = X.mean(axis=0).A1
    terms = vect.get_feature_names_out()
    ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
    return ranked[:n]
