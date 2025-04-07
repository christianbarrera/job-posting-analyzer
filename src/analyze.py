import argparse
import string
from collections import Counter
from nltk import ngrams
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from tabulate import tabulate
import yaml
import pprint
import os

# Define base directories for the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
CV_DIR = os.path.join(BASE_DIR, 'cv')

# Update file paths to use the new directory structure
def load_stopwords(file_path=os.path.join(DATA_DIR, 'stopwords.txt')):
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
    plt.show()  # Commented out

# Find contextual uses of a word
def find_context(word, text, window=5):
    words = text.split()
    indices = [i for i, w in enumerate(words) if w == word]
    for i in indices:
        start = max(i - window, 0)
        end = min(i + window + 1, len(words))
        print(f"Context for '{word}':", ' '.join(words[start:end]))

# Function to load and process the CV text
def load_cv_text(cv_file_path, stopwords_file):
    text = load_text(cv_file_path)  # reuse the existing load_text function
    stopwords = load_stopwords(stopwords_file)
    words = text.split()
    # Filter out stopwords
    words = [word for word in words if word not in stopwords]
    return text, Counter(words)

# Function to extract n-grams from a list of words
def extract_cv_ngrams(cv_words):
    unigrams = Counter(cv_words)
    bigrams = generate_ngrams(cv_words, 2)
    trigrams = generate_ngrams(cv_words, 3)
    return unigrams, bigrams, trigrams

# Function to compare job description n-grams with CV n-grams
# This simple comparison prints common unigrams, bigrams, and trigrams
# and indicates which top job description terms are missing in the CV.
def compare_cv_and_job(job_ngrams, cv_ngrams):
    job_unigrams, job_bigrams, job_trigrams = job_ngrams
    cv_unigrams, cv_bigrams, cv_trigrams = cv_ngrams

    print("\n--- Comparison between Job Description and CV ---\n")

    # Compare Unigrams (sorted by difference in counts)
    print("Common Unigrams (sorted by difference):")
    common_uni = set(job_unigrams.keys()) & set(cv_unigrams.keys())
    uni_diffs = [(word, job_unigrams[word], cv_unigrams[word], abs(job_unigrams[word] - cv_unigrams[word])) for word in common_uni]
    uni_diffs.sort(key=lambda x: x[3], reverse=True)
    print(tabulate(uni_diffs, headers=["Unigram", "JD", "CV", "Diff"], tablefmt="github"))
    print("\n")

    # Compare Bigrams (sorted by difference in counts)
    print("Common Bigrams (sorted by difference):")
    common_bi = set(job_bigrams.keys()) & set(cv_bigrams.keys())
    bi_diffs = [( ' '.join(phrase), job_bigrams[phrase], cv_bigrams[phrase], abs(job_bigrams[phrase] - cv_bigrams[phrase]) ) for phrase in common_bi]
    bi_diffs.sort(key=lambda x: x[3], reverse=True)
    print(tabulate(bi_diffs, headers=["Bigram", "JD", "CV", "Diff"], tablefmt="github"))
    print("\n")

    # Compare Trigrams (sorted by difference in counts)
    print("Common Trigrams (sorted by difference):")
    common_tri = set(job_trigrams.keys()) & set(cv_trigrams.keys())
    tri_diffs = [( ' '.join(phrase), job_trigrams[phrase], cv_trigrams[phrase], abs(job_trigrams[phrase] - cv_trigrams[phrase]) ) for phrase in common_tri]
    tri_diffs.sort(key=lambda x: x[3], reverse=True)
    print(tabulate(tri_diffs, headers=["Trigram", "JD", "CV", "Diff"], tablefmt="github"))
    print("\n")

    # Identify top job unigrams missing in CV
    print("Top Job Description Unigrams Missing in CV:")
    missing = [(word, count) for word, count in job_unigrams.most_common(10) if word not in cv_unigrams]
    print(tabulate(missing, headers=["Unigram", "JD"], tablefmt="github"))

# Load structured YAML CV data
def load_cv_yaml(yaml_path=os.path.join(CONFIG_DIR, 'cv_database.yaml')):
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

# Basic keyword-based CV generator
def generate_custom_cv(job_keywords, cv_data, output_path=os.path.join(OUTPUT_DIR, 'custom_cv.txt')):
    def match_score(item):
        desc = item.get("description", [])
        if isinstance(desc, str):
            desc = [desc]
        skills = item.get("skills", [])
        text = " ".join(desc + skills)
        return sum(1 for word in job_keywords if word in text.lower())

    # Sort and select top entries
    top_experience = sorted(cv_data.get("experience", []), key=match_score, reverse=True)[:4]
    top_projects = sorted(cv_data.get("projects", {}).get("work", []), key=match_score, reverse=True)[:2]
    top_personal_projects = sorted(cv_data.get("projects", {}).get("personal", []), key=match_score, reverse=True)[:1]

    pprint.pprint(top_experience)

    # Start writing the custom CV
    with open(output_path, 'w') as out:
        out.write("CUSTOM CV DRAFT\n\n")

        out.write("EXPERIENCE:\n")
        for job in top_experience:
            out.write(f"{job['title']} - {job['company']}\n")
            out.write(f"{job.get('location', '')} | {job['start_date']} to {job['end_date']}\n")
            for line in job.get("description", []):
                out.write(f" - {line}\n")
            out.write("\n")

        out.write("PROJECTS:\n")
        for proj in top_projects + top_personal_projects:
            out.write(f"{proj['name']} ({proj['year']})\n")
            out.write(f" - {proj['description']}\n")
            out.write("\n")

        out.write("EDUCATION:\n")
        for edu in cv_data.get("education", []):
            out.write(f"{edu['degree']} - {edu['institution']}, {edu['location']}\n")
            out.write(f"Graduated: {edu['graduation_year']}\n")
            if "thesis" in edu:
                out.write(f"Thesis: {edu['thesis']}\n")
            out.write("\n")

    print(f"\nCustom CV draft saved to '{output_path}'")

# Main function to analyze the job description
def text_analyzer(file_path, stopwords_file, specific_skills, args):
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
    if not args.fast:
        plot_wordcloud_and_frequencies(unigrams, bigrams, text)
        find_context("python", text)

# Command-line argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze job descriptions for keywords, sentiment, and patterns.")
    parser.add_argument("file_path", help="Path to the job description file (e.g., example_JD.txt)")
    parser.add_argument("--stopwords", default=os.path.join(DATA_DIR, 'stopwords.txt'), help="Path to the stopwords file (default: stopwords.txt)")
    parser.add_argument("--cv_file", help="Path to the CV file to compare (optional)")
    parser.add_argument("--fast", action="store_true", help="Skip slow visualizations and context search")

    args = parser.parse_args()

    # Analyze job description
    job_text = load_text(os.path.join(DATA_DIR, args.file_path))
    stopwords = load_stopwords(args.stopwords)
    job_words = [word for word in job_text.split() if word not in stopwords]

    job_unigrams = Counter(job_words)
    job_bigrams = generate_ngrams(job_words, 2)
    job_trigrams = generate_ngrams(job_words, 3)

    # Load CV database
    cv_data = load_cv_yaml()

    # Generate the tailored CV
    generate_custom_cv(job_words, cv_data)

    # Existing analysis prints
    print(f"Sentiment Analysis: {analyze_sentiment(job_text)}")

    print("\nUnigrams:")
    for word, count in job_unigrams.most_common(10):
        print(f"{word}: {count}")

    print("\nBigrams:")
    for phrase, count in job_bigrams.most_common(10):
        print(f"{' '.join(phrase)}: {count}")

    print("\nTrigrams:")
    for phrase, count in job_trigrams.most_common(10):
        print(f"{' '.join(phrase)}: {count}")

    # Generate word cloud and frequency plots
    if not args.fast:
        plot_wordcloud_and_frequencies(job_unigrams, job_bigrams, job_text)
        find_context("python", job_text)

    # If a CV file is provided, perform CV analysis and compare with job description
    if args.cv_file:
        cv_text, cv_counter = load_cv_text(os.path.join(CV_DIR, args.cv_file), args.stopwords)
        cv_unigrams, cv_bigrams, cv_trigrams = extract_cv_ngrams(cv_text.split())

        # Compare the job description n-grams with CV n-grams
        compare_cv_and_job(
            (job_unigrams, job_bigrams, job_trigrams),
            (cv_unigrams, cv_bigrams, cv_trigrams)
        )