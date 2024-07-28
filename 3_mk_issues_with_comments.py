from datasets import load_dataset
import requests
import json
# third script to change the original data
# This code extracts the comments from the body and the previous field "comments" which consists of dtype : integer represting the number of comments is now replaced with dtype : list which have strings csv values of comments

GITHUB_TOKEN = ""  #GitHub token here
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

issues_dataset = load_dataset("json", data_files="selected_fields_issues.jsonl", split="train")

def get_comments(issue_number):
    url = f"https://api.github.com/repos/huggingface/datasets/issues/{issue_number}/comments"
    response = requests.get(url, headers=headers)
    return [r["body"] for r in response.json()]

issues_with_comments_dataset = issues_dataset.map(
    lambda x: {"comments": get_comments(x["number"])}
)

issues_with_comments_dataset.to_json('issues_with_comments.jsonl') # issues_with_comments.jsonl gets saved to the local , comments are now list.