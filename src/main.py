import argparse
import os
from file_utils import load_text, load_stopwords, load_cv_yaml
from text_analysis import analyze_sentiment, generate_ngrams, find_context
from visualization import plot_wordcloud_and_frequencies
from cv_processing import load_cv_text, extract_cv_ngrams, compare_cv_and_job
from collections import Counter

def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    CONFIG_DIR = os.path.join(BASE_DIR, 'config')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
    CV_DIR = os.path.join(BASE_DIR, 'cv')

    parser = argparse.ArgumentParser(description="Analyze job descriptions for keywords, sentiment, and patterns.")
    parser.add_argument("file_path", help="Path to the job description file (e.g., example_JD.txt)")
    parser.add_argument("--stopwords", default=os.path.join(DATA_DIR, 'stopwords.txt'), help="Path to the stopwords file (default: stopwords.txt)")
    parser.add_argument("--cv_file", help="Path to the CV file to compare (optional)")
    parser.add_argument("--fast", action="store_true", help="Skip slow visualizations and context search")

    args = parser.parse_args()

    # Ensure the file path is relative to the appropriate directory
    job_file_path = os.path.join(DATA_DIR, os.path.basename(args.file_path))

    if args.cv_file:
        cv_file_path = os.path.join(CV_DIR, os.path.basename(args.cv_file))
    else:
        cv_file_path = None

    # Analyze job description
    job_text = load_text(job_file_path)
    stopwords = load_stopwords(args.stopwords)
    job_words = [word for word in job_text.split() if word not in stopwords]

    job_unigrams = Counter(job_words)
    job_bigrams = generate_ngrams(job_words, 2)
    job_trigrams = generate_ngrams(job_words, 3)

    # Load CV database
    cv_data = load_cv_yaml(os.path.join(CONFIG_DIR, 'cv_database.yaml'))

    # Generate the tailored CV
    from cv_processing import generate_custom_cv
    generate_custom_cv(job_words, cv_data, output_path=os.path.join(OUTPUT_DIR, 'custom_cv.txt'))

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
    if cv_file_path:
        cv_text, cv_counter = load_cv_text(cv_file_path, args.stopwords, load_text, load_stopwords)
        cv_unigrams, cv_bigrams, cv_trigrams = extract_cv_ngrams(cv_text.split(), generate_ngrams)

        # Compare the job description n-grams with CV n-grams
        compare_cv_and_job(
            (job_unigrams, job_bigrams, job_trigrams),
            (cv_unigrams, cv_bigrams, cv_trigrams)
        )

if __name__ == "__main__":
    main()