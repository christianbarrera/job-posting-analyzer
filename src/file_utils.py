import os
import string
import yaml
import shutil

def load_stopwords(file_path):
    try:
        with open(file_path, 'r') as file:
            stopwords = set(line.strip().lower() for line in file)
        return stopwords
    except FileNotFoundError:
        print(f"Warning: Stopwords file '{file_path}' not found. Continuing without stopwords.")
        return set()

def load_text(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read().lower().translate(str.maketrans('', '', string.punctuation))
        return text
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit(1)

def load_cv_yaml(yaml_path):
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def ensure_cv_database_exists(template_path, target_path):
    if not os.path.exists(target_path):
        print(f"The CV database file '{target_path}' does not exist.")
        print(f"Creating a copy of the template '{template_path}' for you to fill in.")
        shutil.copy(template_path, target_path)
        print(f"Please edit '{target_path}' with your personal information before running the script again.")
        exit(1)