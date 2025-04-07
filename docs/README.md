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

### Running the Project
1. Place job descriptions in the `data/` folder (e.g., `example_JD.txt`).
2. Run the main script:
```bash
python src/main.py example_JD.txt
```
3. Optional arguments:
   - `--stopwords`: Specify a custom stopwords file (default: `data/stopwords.txt`).
   - `--cv_file`: Provide a CV file from the `cv/` folder to compare with the job description.
   - `--fast`: Skip slow visualizations and context search.

### Example Command
```bash
python src/main.py example_JD.txt --stopwords stopwords.txt --cv_file my_cv_data_engineering.txt --fast
```

### Output
- **Custom CV**: A tailored CV will be saved in the `output/` folder (e.g., `custom_cv.txt`).
- **Visualizations**: Word clouds and bar charts will be saved in the `output/` folder (e.g., `example_output.png`).
- **Console Output**: Sentiment analysis, top keywords, and n-gram comparisons will be displayed in the terminal.

## Example Output

After running the script, you will see a visualization similar to this:

<img src="output/example_output.png" alt="Example Output" width="900">

#### Optional: Specify a Custom Stopwords File
By default, the program looks for `data/stopwords.txt`. If you want to use a different stopwords file, specify it with the `--stopwords` option:
```bash
python src/main.py example_JD.txt --stopwords custom_stopwords.txt
```
If no stopwords file is provided, the script will continue without filtering stopwords.

### Contributing

Feel free to submit pull requests! For major changes, please open an issue first.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Quick run
```bash
from analyze import load_cv_yaml, generate_custom_cv, load_stopwords, load_text

# Load keywords from job description
jd_text = load_text("birkenstock_dataengineer.txt")
stopwords = load_stopwords("stopwords.txt")
job_keywords = [word for word in jd_text.split() if word not in stopwords]

# Load CV database
cv_data = load_cv_yaml("cv_database.yaml")

# Generate the tailored CV
generate_custom_cv(job_keywords, cv_data, output_path="custom_cv.txt")
```

### Further development
Instead of actually placing and rating the relevant experience based on job, keep it chronological and instead rate and place based on relevance of the bullet points in each experience category.