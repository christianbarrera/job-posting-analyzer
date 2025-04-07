from collections import Counter
from nltk import ngrams
from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment

def generate_ngrams(words, n):
    return Counter(ngrams(words, n))

def find_context(word, text, window=5):
    words = text.split()
    indices = [i for i, w in enumerate(words) if w == word]
    for i in indices:
        start = max(i - window, 0)
        end = min(i + window + 1, len(words))
        print(f"Context for '{word}':", ' '.join(words[start:end]))