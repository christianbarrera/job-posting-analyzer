# Job Posting Text Analyzer

This project analyzes job descriptions to help tailor your resume to the most frequently used keywords in job postings. By analyzing the text, it identifies common words, phrases, and key skills, which can assist you in optimizing your resume for specific roles.

## Features

- **Text Analysis**: Analyze job descriptions to find the most frequently used words, bigrams, and trigrams.
- **Sentiment Analysis**: Understand the tone of job descriptions (e.g., positive, negative, or neutral).
- **Skill Highlights**: Identify how often certain skills (e.g., "Python", "data analysis") appear in job descriptions.
- **Word Cloud & Bar Charts**: Visualize the most frequent terms in job descriptions.

## Prerequisites

- Python 3.6+
- Virtual environment (recommended)
- `pip` for package management

## Installation Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/job-posting-analyzer.git
cd job-posting-analyzer
```

### 2. Create and Activate a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### Usage
1.	Place job descriptions in example_JD.txt (or modify the script to read another file).
2.	Run the script:
```bash
    python analyze.py example_JD.txt
```
3. 	The program will output:
	•	Top keywords ranked by frequency
	•	Bigram & trigram analysis (common word pairs & triplets)
	•	Sentiment analysis (optional)
	•	Visualizations (word clouds and bar charts)

#### Optional: Specify a Custom Stopwords File
By default, the program looks for stopwords.txt. If you want to use a different stopwords file, specify it with the --stopwords option:
```bash
python text_analyzer.py example_JD.txt --stopwords custom_stopwords.txt
```
If no stopwords file is provided, the script will continue without filtering stopwords.

### Example Output
```bash
Top Keywords:
1. Python (15 times)
2. Data Engineering (12 times)
3. SQL (10 times)
...
```

### Contributing

Feel free to submit pull requests! For major changes, please open an issue first.

### License

This project is licensed under the MIT License. See the LICENSE file for details.