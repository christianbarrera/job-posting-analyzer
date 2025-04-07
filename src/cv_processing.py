from collections import Counter
from tabulate import tabulate

def load_cv_text(cv_file_path, stopwords_file, load_text, load_stopwords):
    text = load_text(cv_file_path)
    stopwords = load_stopwords(stopwords_file)
    words = text.split()
    words = [word for word in words if word not in stopwords]
    return text, Counter(words)

def extract_cv_ngrams(cv_words, generate_ngrams):
    unigrams = Counter(cv_words)
    bigrams = generate_ngrams(cv_words, 2)
    trigrams = generate_ngrams(cv_words, 3)
    return unigrams, bigrams, trigrams

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

def generate_custom_cv(job_keywords, cv_data, output_path="custom_cv.txt"):
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