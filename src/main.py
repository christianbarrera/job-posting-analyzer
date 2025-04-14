import argparse
import os
from file_utils import load_text, load_stopwords, load_cv_yaml, ensure_cv_database_exists
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
    parser.add_argument("job_file", help="Path to the job description file (e.g., example_JD.txt)")
    parser.add_argument("--stopwords", default=os.path.join(DATA_DIR, 'stopwords.txt'), help="Path to the stopwords file (default: stopwords.txt)")
    parser.add_argument("--cv_file", help="Path to the CV file to compare (optional)")
    parser.add_argument("--fast", action="store_true", help="Skip slow visualizations and context search")
    parser.add_argument("--output_file", default="output/custom_cv.txt", help="Path to the output file for the tailored CV (default: output/custom_cv.txt)")
    parser.add_argument("--use_model", nargs="?", const="gpt-4o-mini", default=None, help="Specify the model to use (e.g., gpt-4o-mini, gpt-4o). If no model is specified, the default is gpt-4o-mini.")
    parser.add_argument("--cv_database", default=os.path.join(CONFIG_DIR, 'cv_database.yaml'), help="Path to the CV database file (default: config/cv_database.yaml)")
    parser.add_argument("--generate_cover_letter", action="store_true", help="Generate a cover letter for the job posting.")

    args = parser.parse_args()

    # Ensure the file path is relative to the appropriate directory
    job_file_path = os.path.join(DATA_DIR, os.path.basename(args.job_file))

    if args.cv_file:
        cv_file_path = os.path.join(CV_DIR, os.path.basename(args.cv_file))
    else:
        cv_file_path = None

    # Ensure the CV database exists
    ensure_cv_database_exists(
        os.path.join(CONFIG_DIR, 'cv_database_template.yaml'),
        os.path.join(CONFIG_DIR, 'cv_database.yaml')
    )

    # Ensure the stopwords file path is relative to the appropriate directory
    stopwords_file_path = os.path.join(DATA_DIR, os.path.basename(args.stopwords))

    # Analyze job description
    job_text = load_text(job_file_path)
    stopwords = load_stopwords(stopwords_file_path)
    job_words = [word for word in job_text.split() if word not in stopwords]

    job_unigrams = Counter(job_words)
    job_bigrams = generate_ngrams(job_words, 2)
    job_trigrams = generate_ngrams(job_words, 3)

    # Load the selected CV database
    cv_database_path = os.path.join(CONFIG_DIR, os.path.basename(args.cv_database))
    cv_data = load_cv_yaml(cv_database_path)

    # Ensure the output file path is relative to the output directory
    output_file_path = os.path.join(OUTPUT_DIR, os.path.basename(args.output_file))

    # Generate the tailored CV
    from cv_processing import generate_custom_cv
    generate_custom_cv(job_words, cv_data, output_path=output_file_path)

    # Generate a detailed report
    from cv_processing import generate_detailed_report
    generate_detailed_report(job_words, cv_data, output_path=os.path.join(OUTPUT_DIR, 'detailed_report.txt'), job_file_name=os.path.basename(job_file_path))

    # Compare the tailored CV with the job description
    from analyze import compare_cv_to_jd
    compare_cv_to_jd(
        job_file_path=job_file_path,
        cv_file_path=os.path.join(OUTPUT_DIR, 'custom_cv.txt'),
        output_path=os.path.join(OUTPUT_DIR, 'detailed_report.txt')
    )

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

    # Update logic to handle the --use_model flag
    model = args.use_model
    if model:
        from analyze import run_gpt_model
        descriptive_copy_path = os.path.join(CV_DIR, f"{os.path.splitext(os.path.basename(job_file_path))[0].replace('_', ' ').title().replace(' ', '_')}_CV.txt")

        # Define the path to the cover letters folder
        COVER_LETTERS_DIR = os.path.join(BASE_DIR, 'cover_letters')
        os.makedirs(COVER_LETTERS_DIR, exist_ok=True)

        run_gpt_model(
            job_file_path=job_file_path,
            cv_database_path=cv_database_path,
            detailed_report_path=os.path.join(OUTPUT_DIR, 'detailed_report.txt'),
            output_path=os.path.join(OUTPUT_DIR, 'custom_cv.txt'),
            descriptive_copy_path=descriptive_copy_path,
            cover_letter_output_path=os.path.join(OUTPUT_DIR, f"Cover_Letter_{os.path.splitext(os.path.basename(job_file_path))[0]}.txt"),
            reference_folder=COVER_LETTERS_DIR if args.generate_cover_letter else None,
            model=model
        )
        print(f"Generated CV saved to: {descriptive_copy_path}")

        # Create an archive folder for CV .txt files
        ARCHIVE_DIR = os.path.join(BASE_DIR, 'archive')
        os.makedirs(ARCHIVE_DIR, exist_ok=True)

        # Archive the resulting CV .txt file with a timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file_path = os.path.join(ARCHIVE_DIR, f"{os.path.splitext(os.path.basename(output_file_path))[0]}_{timestamp}.txt")
        os.rename(output_file_path, archive_file_path)
        print(f"Archived CV to: {archive_file_path}")

        # Convert the Markdown CV to PDF format only
        from analyze import convert_md_to_pdf_and_word
        markdown_copy_path = descriptive_copy_path.replace('.txt', '.md')
        convert_md_to_pdf_and_word(markdown_copy_path)

        # Validate the Markdown CV for ATS-friendly formatting
        from analyze import validate_ats_friendly_format
        validate_ats_friendly_format(markdown_copy_path)

        # Compare the tailored CV with the job description and append results to the rewritten CV
        compare_cv_to_jd(
            job_file_path=job_file_path,
            cv_file_path=descriptive_copy_path,
            output_path=descriptive_copy_path,  # Append results to the same file
        )

if __name__ == "__main__":
    main()