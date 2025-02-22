import argparse
import string
from collections import Counter
from nltk import ngrams
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load stopwords from a file
def load_stopwords(file_path):
    try:
        with open(file_path, 'r') as file:
            stopwords = set(line.strip().lower() for line in file)
        return stopwords
    except FileNotFoundError:
        print(f"Warning: Stopwords file '{file_path}' not found. Continuing without stopwords.")
        return set()

# Function to load the job description text
def load_text(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read().lower().translate(str.maketrans('', '', string.punctuation))
        return text
    except FileNotFoundError:
        print(f"Error: Job description file '{file_path}' not found.")
        exit(1)

# Sentiment analysis function
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment

# Bigram and trigram generator
def generate_ngrams(words, n):
    return Counter(ngrams(words, n))

def plot_wordcloud_and_frequencies(unigrams, bigrams, text):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))  # Three side-by-side plots

    # Word Cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    axes[0].imshow(wordcloud, interpolation='bilinear')
    axes[0].axis('off')  # Hide axes
    axes[0].set_title("Word Cloud")

    # Unigrams Bar Chart
    top_unigrams = unigrams.most_common(10)
    words_u, counts_u = zip(*top_unigrams)
    axes[1].bar(words_u, counts_u, color='tab:blue')
    axes[1].set_title("Top Unigrams")
    axes[1].set_xlabel("Words")
    axes[1].set_ylabel("Frequency")
    axes[1].tick_params(axis='x', rotation=45)

    # Bigrams Bar Chart
    top_bigrams = bigrams.most_common(10)
    words_b, counts_b = zip(*[(" ".join(phrase), count) for phrase, count in top_bigrams])
    axes[2].bar(words_b, counts_b, color='tab:green')
    axes[2].set_title("Top Bigrams")
    axes[2].set_xlabel("Phrases")
    axes[2].set_ylabel("Frequency")
    axes[2].tick_params(axis='x', rotation=90)

    plt.tight_layout()

    # Save the figure
    plt.savefig("example_output.png", dpi=300, bbox_inches="tight")
    plt.show()

# Find contextual uses of a word
def find_context(word, text, window=5):
    words = text.split()
    indices = [i for i, w in enumerate(words) if w == word]
    for i in indices:
        start = max(i - window, 0)
        end = min(i + window + 1, len(words))
        print(f"Context for '{word}':", ' '.join(words[start:end]))

# Main function to analyze the job description
def text_analyzer(file_path, stopwords_file, specific_skills):
    stopwords = load_stopwords(stopwords_file)
    text = load_text(file_path)

    # Tokenize and filter stopwords
    words = text.split()
    words = [word for word in words if word not in stopwords]

    # Unigrams, bigrams, trigrams analysis
    unigrams = Counter(words)
    bigrams = generate_ngrams(words, 2)
    trigrams = generate_ngrams(words, 3)

    # Sentiment analysis
    sentiment = analyze_sentiment(text)
    print(f"Sentiment Analysis: Polarity = {sentiment.polarity}, Subjectivity = {sentiment.subjectivity}")

    # Highlight specific skills
    print("\nSkill Highlights:")
    for skill in specific_skills:
        if skill in unigrams:
            print(f"The skill '{skill}' is mentioned {unigrams[skill]} times.")

    # Display frequency of unigrams, bigrams, and trigrams
    print("\nUnigrams:")
    for word, count in unigrams.most_common(10):
        print(f"{word}: {count}")

    print("\nBigrams:")
    for phrase, count in bigrams.most_common(10):
        print(f"{' '.join(phrase)}: {count}")

    print("\nTrigrams:")
    for phrase, count in trigrams.most_common(10):
        print(f"{' '.join(phrase)}: {count}")

    # Generate word cloud and plot top keywords
    plot_wordcloud_and_frequencies(unigrams, bigrams, text)

    # Contextual search for a word
    print("\nContextual Search Example:")
    find_context("python", text)

# Command-line argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze job descriptions for keywords, sentiment, and patterns.")
    parser.add_argument("file_path", help="Path to the job description file (e.g., example_JD.txt)")
    parser.add_argument("--stopwords", default="stopwords.txt", help="Path to the stopwords file (default: stopwords.txt)")

    args = parser.parse_args()

    # Predefined skills
    specific_skills = {
        # # Data Engineering
        "python", "sql", "postgresql", "mssql", "snowflake", 
        "airflow", "aws", "azure", "Looker", "warehouse",
        "redshift", "rest", "data pipelines", "etl", "git",
        "data", "pipeline", "pipelines", "etl/elt",

        # Renewable Energy
        "energy modeling", "renewable energy", "energy efficiency", 
        "energy storage", "photovoltaic", "solar energy", 
        "wind turbines", "battery systems", 
        "geothermal engineering", "carbon capture", 
        "carbon sequestration", "pvsol", "homer energy", 
        "retScreen", "energypro", "life cycle assessment", 
        "energy markets", "policy analysis", "energy",
        "environmental impact analysis", "emissions control", 

        # # Mechanical/Process Engineering
        "matlab", "ansys", "solidworks", "autocad", 
        "six sigma", "lean manufacturing", "process optimization", 
        "finite element analysis", "computational fluid dynamics", 
        "pid control", "scada", "plc programming", 
        "fluid mechanics", "heat transfer", "piping design", 
        "hazop", "risk assessment", "failure modes", 
        "asme", "api", "iso standards", 
        "thermodynamics", "energy conversion", "engineering",
    }

    # Run the analyzer
    text_analyzer(args.file_path, args.stopwords, specific_skills)