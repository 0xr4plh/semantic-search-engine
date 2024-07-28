from datasets import load_dataset
from datasets import Dataset
from transformers import AutoTokenizer, AutoModel
# fourth script to change the original data
issues_dataset = load_dataset("amannagrawall002/github-issues", split="train") # loading the data from remote server 

# Data pre-processing , selecting only those rows which can actually resolve user queries

issues_dataset = issues_dataset.filter(lambda x: len(x["comments"]) > 0)
issues_dataset.set_format("pandas")
df = issues_dataset[:]
comments_df = df.explode("comments", ignore_index=True) # All the other columns other than "comments" gets copied and gets mapped that is if any example has 3 comments so 3 rows would be made with three comments and all other information of other elements will get copied as that of the orginal example.
comments_dataset = Dataset.from_pandas(comments_df) # converting it back to dataset.

comments_dataset = comments_dataset.map(
    lambda x: {"comment_length": len(x["comments"].split())}
) # adding a new column to inspect and filter the rows based on comment length

comments_dataset = comments_dataset.filter(lambda x: x["comment_length"] > 15) # Single word comments and very short comments are of no use , choosing 15 as a threshold

def concatenate_text(examples):
    title = examples["title"] if examples["title"] is not None else ""
    body = examples["body"] if examples["body"] is not None else ""
    comments = examples["comments"]
    
    return {
        "text": title + " \n " + body + " \n " + comments
    }

comments_dataset = comments_dataset.map(concatenate_text) # Combining all important information regarding the issue whcih would be helpful to resolve a user query , so combining title , body and comments.

model_ckpt = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
model = AutoModel.from_pretrained(model_ckpt)

def cls_pooling(model_output):
    return model_output.last_hidden_state[:, 0] # basically taking the last hidden state which contains all the information like CLS token of BERT

def get_embeddings(text_list):
    encoded_input = tokenizer(
        text_list, padding=True, truncation=True, return_tensors="pt"
    )
    model_output = model(**encoded_input)
    return cls_pooling(model_output) # I have trained it on my CPU only , took 5 hours.

# embedding = get_embeddings(comments_dataset["text"][0])
# print(embedding.shape)
# # torch.Size([1, 768])

embeddings_dataset = comments_dataset.map(
    lambda x: {"embeddings": get_embeddings(x["text"]).detach().numpy()[0]}
) # A deep embedding representing the whole text is made which will be used later to match the similarity between user query.

embeddings_dataset.save_to_disk("embeddings_dataset") # saved a directory which contains an arrow file , meta data and state.json
# Arrow file would be a large file so cannot be uploaded on github.
