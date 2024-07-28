import requests
import time
import math
import json
from pathlib import Path
import pandas as pd
from tqdm import tqdm
from datasets import Dataset
from datasets import load_dataset
from datasets import load_dataset, Features, Value, ClassLabel
from transformers import AutoTokenizer, AutoModel

url = "https://api.github.com/repos/huggingface/datasets/issues?page=1&per_page=1"
response = requests.get(url)

# print(response.status_code) --> 200 sucessful , it's working fine

GITHUB_TOKEN = ""  #GitHub token here
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# Making a function to use GitHub rest api to fetch all the issues on the hugging face datasets , and using personal token so that we get limit of 5000 per hour.
def fetch_issues(
    owner="huggingface",
    repo="datasets",
    num_issues=10_000,
    rate_limit=5_000,
    issues_path=Path("."),
):
    if not issues_path.is_dir():
        issues_path.mkdir(exist_ok=True)

    batch = []
    all_issues = []
    per_page = 100  # Number of issues to return per page
    num_pages = math.ceil(num_issues / per_page)
    base_url = "https://api.github.com/repos"

    for page in tqdm(range(num_pages)):
        # Query with state=all to get both open and closed issues
        query = f"issues?page={page}&per_page={per_page}&state=all"
        issues = requests.get(f"{base_url}/{owner}/{repo}/{query}", headers=headers)
        batch.extend(issues.json())

        if len(batch) > rate_limit and len(all_issues) < num_issues:
            all_issues.extend(batch)
            batch = []  # Flush batch for next time period
            print(f"Reached GitHub rate limit. Sleeping for one hour ...")
            time.sleep(60 * 60 + 1)

    all_issues.extend(batch)
    df = pd.DataFrame.from_records(all_issues)
    df.to_json(f"{issues_path}/{repo}-issues.jsonl", orient="records", lines=True)
    print(
        f"Downloaded all the issues for {repo}! Dataset stored at {issues_path}/{repo}-issues.jsonl"
    )

fetch_issues() # calling the function and data gets saved to local by name - dataset-issues.jsonl , this is unfiltered data which have all the features/fields which aren't required to make search engine application for hugging face datasets issues.

