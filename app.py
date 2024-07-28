import streamlit as st
from datasets import load_from_disk
from transformers import AutoTokenizer, AutoModel
import pandas as pd

# Load the dataset and model
def load_data_and_model():
    dataset_path = r"C:\Users\DELL\Desktop\Machine Learning\transformer-course\NLP-Hugging-Face-Course\NLP_HF\Part_2\serach engine\embeddings_dataset" # Update this path
    embeddings_dataset = load_from_disk(dataset_path)
    embeddings_dataset.add_faiss_index(column="embeddings")
    
    model_ckpt = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
    tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
    model = AutoModel.from_pretrained(model_ckpt)
    return embeddings_dataset, tokenizer, model

embeddings_dataset, tokenizer, model = load_data_and_model()

def get_embeddings(text_list):
    encoded_input = tokenizer(
        text_list, padding=True, truncation=True, return_tensors="pt"
    )
    model_output = model(**encoded_input)
    return model_output.last_hidden_state[:, 0].cpu().detach().numpy()

# Streamlit UI
st.title("Semantic Search Engine")
st.write("Enter your query below:")
query = st.text_input("Query", "")

if st.button("Search"):
    if query:
        query_embedding = get_embeddings([query])
        scores, samples = embeddings_dataset.get_nearest_examples(
            "embeddings", query_embedding, k=3
        )
        samples_df = pd.DataFrame.from_dict(samples)
        samples_df["scores"] = scores
        samples_df.sort_values("scores", ascending=False, inplace=True)
        
        st.write("Top 3 Nearest Results:")
        for index, row in samples_df.iterrows():
            with st.container():
                st.markdown(f"#### Title: {row.title}")
                st.write(f"**Score:** {row.scores:.4f}")
                st.write(f"**URL:** [Link]({row.html_url})")
                st.write(f"**Comment:** {row.comments}")
                st.write(f"**Body:** {row.body}")
                st.markdown("---")
    else:
        st.write("Please enter a query to search.")
