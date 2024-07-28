from datasets import load_from_disk
from transformers import AutoTokenizer, AutoModel
import pandas as pd

# Specify the path to your dataset directory
dataset_path = r"C:\Users\DELL\Desktop\Machine Learning\transformer-course\NLP-Hugging-Face-Course\NLP_HF\Part_2\serach engine\embeddings_dataset"

# Load the dataset from the disk
embeddings_dataset = load_from_disk(dataset_path)

# print(embeddings_dataset)
# Dataset({
#     features: ['html_url', 'title', 'comments', 'body', 'number', 'comment_length', 'text', 'embeddings'],
#     num_rows: 6636
# })

model_ckpt = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
model = AutoModel.from_pretrained(model_ckpt)

def cls_pooling(model_output):
    return model_output.last_hidden_state[:, 0]

def get_embeddings(text_list):
    encoded_input = tokenizer(
        text_list, padding=True, truncation=True, return_tensors="pt"
    )
    model_output = model(**encoded_input)
    return cls_pooling(model_output)

embeddings_dataset.add_faiss_index(column="embeddings")

question = "How to load the dataset from a remote repo , to my local machine directly in the json format?"
question_embedding = get_embeddings([question]).cpu().detach().numpy()

scores, samples = embeddings_dataset.get_nearest_examples(
    "embeddings", question_embedding, k=3
)

samples_df = pd.DataFrame.from_dict(samples)
samples_df["scores"] = scores
samples_df.sort_values("scores", ascending=False, inplace=True)

for _, row in samples_df.iterrows():
    print(f"COMMENT: {row.comments}")
    print(f"SCORE: {row.scores}")
    print(f"TITLE: {row.title}")
    print(f"URL: {row.html_url}")
    print("-" * 50)
    print()