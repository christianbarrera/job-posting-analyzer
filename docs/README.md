# Job Posting Text Analyzer

This project analyzes job descriptions to help tailor your resume to the most frequently used keywords in job postings. By analyzing the text, it identifies common words, phrases, and key skills, which can assist you in optimizing your resume for specific roles.

## Features

- **Text Analysis**: Analyze job descriptions to find the most frequently used words, bigrams, and trigrams.
- **Sentiment Analysis**: Understand the tone of job descriptions (e.g., positive, negative, or neutral).
- **Skill Highlights**: Identify how often certain skills (e.g., "Python", "data analysis") appear in job descriptions.
- **Word Cloud & Bar Charts**: Visualize the most frequent terms in job descriptions.
- **CV Comparison**: Compare your CV with job descriptions to identify missing keywords.

## Prerequisites

- Python 3.6+
- Virtual environment (recommended)
- `pip` for package management

## Installation Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/christianbarrera/job-posting-analyzer.git
cd job-posting-analyzer
```

### 2. Create and Activate a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements/requirements.txt
```

## Usage

### Updated Usage

### Running the Project
1. Place job descriptions in the `data/` folder (e.g., `example_JD.txt`).
2. Run the main script:
```bash
python src/main.py --file_path data/example_JD.txt --cv_database config/cv_database.yaml
```
3. Optional arguments:
   - `--cv_database`: Specify the CV database file to use (default: `config/cv_database.yaml`).
   - `--use_model`: Use the GPT-4o-mini model for generating tailored CV suggestions.
   - `--fast`: Skip slow visualizations and context search.
   - `--output_file`: Path to the output file for the tailored CV (default: `output/custom_cv.txt`).

### Example Command
```bash
python src/main.py --file_path data/example_JD.txt --cv_database config/cv_database.yaml --use_model
```

### Output
- **Custom CV**: A tailored CV will be saved in the `output/` folder (e.g., `custom_cv.txt`).
- **GPT Output**: If `--use_model` is specified, the GPT-generated CV suggestions will be saved in `output/gpt_generated_cv.txt`.
- **Visualizations**: Word clouds and bar charts will be saved in the `output/` folder (e.g., `example_output.png`).
- **Console Output**: Sentiment analysis, top keywords, and n-gram comparisons will be displayed in the terminal.

### Detailed Report

After running the script, a detailed report will be generated and saved in the `output/` folder as `detailed_report.txt`. This report provides an in-depth analysis of the job description, including:

- A breakdown of the most frequent keywords and phrases.
- Insights into the alignment between your CV and the job description.
- Suggestions for improving your CV to better match the job requirements.

You can use this report to refine your CV and ensure it is tailored to the specific job posting.

### Quick Run Example
```python
from src.analyze import load_cv_yaml, generate_custom_cv, load_text

# Load keywords from job description
jd_text = load_text("data/example_JD.txt")
job_keywords = jd_text.split()

# Load CV database
cv_data = load_cv_yaml("config/cv_database.yaml")

# Generate the tailored CV
generate_custom_cv(job_keywords, cv_data, output_path="custom_cv.txt")
```

### Contributing

Feel free to submit pull requests! For major changes, please open an issue first.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Further development
Instead of actually placing and rating the relevant experience based on job, keep it chronological and instead rate and place based on relevance of the bullet points in each experience category.