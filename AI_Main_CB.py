import ollama
import pandas as pd
import json
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

#file path
def load_data(file_path):
    return pd.read_csv(file_path)

#changed df to json object
def prepare_data_for_model(df):
    return df.to_json(orient='records')

#creates vector frame / retriever
#broke code works but only sees 4 movies
def create_retriever_from_dataframe(df, rows_per_chunk=25):
    chunks = []
    for i in range(0, len(df), rows_per_chunk):
        chunk_df = df.iloc[i:i+rows_per_chunk]
        text_block = "\n".join(json.dumps(row.to_dict()) for _, row in chunk_df.iterrows())
        chunks.append(Document(page_content=text_block))

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore.as_retriever()

def get_initial_response(model_name, messages):
    response = ollama.chat(model=model_name, messages=messages)
    print("Bot:", response.message.content)

def continue_conversation(model_name, messages, retriever=None):
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("end", ""):
            break
        
        if retriever:
            docs = retriever.invoke(user_input)
            retrieved_context = "\n".join([doc.page_content for doc in docs])
            user_input = f"Context: {retrieved_context}\nQuestion: {user_input}"
        
        messages.append({"role": "user", "content": user_input})
        response = ollama.chat(model=model_name, messages=messages)
        answer = response.message.content
        print("Bot:", answer)
        messages.append({"role": "assistant", "content": answer})

def main():
    model_name = 'gemma3:1b'  
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]

    file_path = "test_set.csv"  #file location
    data = load_data(file_path)

    retriever = create_retriever_from_dataframe(data)
    get_initial_response(model_name, messages)
    continue_conversation(model_name, messages, retriever)

if __name__ == "__main__":
    main()