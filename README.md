### Semantic Search Engine

This repository contains a semantic search engine specifically designed to address user queries related to the GitHub issues of the Hugging Face (repo - datasets). The user's query is a short question about issues related to Hugging Face datasets, and in return, the user will get the semantically most similar answer (Title + body + comments) provided by other users on the GitHub issues of Hugging Face datasets.

The concept is based on FAISS indexing of the embeddings representing the text of every row of our final dataset. The user question is converted into an embedding, and every row of our dataset also has an embedding corresponding to it. The row embedding that is most similar to the user question (top 3) is displayed on `app.py` on Streamlit or on `search_engine_on_local.py`/Python console which the user is using. `requirements.txt` is provided to set up the Python environment.

This is hosted on Streamlit, where the user can ask a query related to Hugging Face datasets and receive the top 3 answers which our search engine finds most similar semantically from the dataset rows that we have used. The interface will show the title, similarity score, body, comment, and the HTML URL which will direct us to the original page of the issue on Hugging Face datasets.

An example showing the first nearest similar result with respect to the query asked by the user (only displaying the nearest, there are two others as well) on the Streamlit platform (running `app.py` file after all requirements are satisfied):
![Example Image](https://github.com/user-attachments/assets/67c55a69-eff9-4401-8c24-15b0431feeb6)

The dataset used in this project was built from scratch using GitHub issues from the Hugging Face datasets repo. Detailed information on the dataset can be found on the model card on my Hugging Face account. This provides detailed information on how I approached creating this dataset from scratch for making this search engine: [Dataset Link](https://huggingface.co/datasets/amannagrawall002/github-issues). The code itself is also properly commented and explains the flow.

The numbered files from 0 to 4 are all focused on creating the final dataset that will be used. The dataset made after running the 4th Python file is the one used by `app.py` or `search_engine_on_local.py`. One can directly start from file 4 and ignore the code from 0 to 3 and can directly load the dataset using the `load_dataset` function from the Hugging Face remote server account - `amannagrawall002/github-issues`. Files 0 to 3 are focused on creating, processing, and filtering the original dataset to the one used by our search engine application. The original dataset is created by running the base code which uses the GitHub REST API to create the dataset, where one has to fill the GitHub token with their personal GitHub account token.

**Model used for creating embeddings**: `"sentence-transformers/multi-qa-mpnet-base-dot-v1"`. Sentence-transformers is a library used to create embeddings of the text, which is used in `app.py` file. If one is using a local CPU for preparing the dataset and running `app.py` file (to make embeddings of the text of each row), it would be a time-intensive task, taking about 5-8 hours overall. GPU usage is advisable.

**Why this model**: `sentence-transformers/multi-qa-mpnet-base-dot-v1`
![Model Image](https://github.com/user-attachments/assets/5e03d4a1-0f77-499f-9e17-28cf5ba4dcac)
[Model Overview](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html#model-overview)

### Resources used:

- **NLP Hugging Face course:**
  - [Chapter 5.5](https://huggingface.co/learn/nlp-course/chapter5/5?fw=pt)
  - [Chapter 5.6](https://huggingface.co/learn/nlp-course/chapter5/6?fw=pt)
  
- **Sentence Transformers library:**
  - [Library Overview](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html#model-overview)
  - [Sentence Transformers](https://sbert.net/)
  
- **FAISS documentation:**
  - [FAISS](https://faiss.ai/)
  
- **Hugging Face account:**
  - [Hugging Face Datasets](https://huggingface.co/datasets/amannagrawall002/github-issues)

**Contact**: [amannagrawall002@gmail.com](mailto:amannagrawall002@gmail.com)
