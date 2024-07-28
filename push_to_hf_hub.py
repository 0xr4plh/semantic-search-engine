# Pushing the dataset that is saved after running the third script , this is the final data that we will use to create the serach engine for hugging face datasets repo
from datasets import load_dataset

reloaded_dataset_jsonl = load_dataset('json', data_files='issues_with_comments.jsonl', split='train')

reloaded_dataset_jsonl.push_to_hub("github-issues") # contributed dataset to the hugging face hub.
# pushed the dataset to the remote server , so that it can be loaded from there.