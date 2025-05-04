import ollama
import pandas as pd
import json
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

class AIModel:
    def __init__(self, model_name='gemma3:1b', file_path="test_set.csv"):
        self.model_name = model_name
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]
        self.retriever = None

        # Load data and create retriever
        try:
            data = self.load_data(file_path)
            self.retriever = self.create_retriever_from_dataframe(data)
        except Exception as e:
            print(f"Error initializing retriever: {e}")

    def load_data(self, file_path):
        return pd.read_csv(file_path)

    def create_retriever_from_dataframe(self, df, rows_per_chunk=25):
        chunks = []
        for i in range(0, len(df), rows_per_chunk):
            chunk_df = df.iloc[i:i+rows_per_chunk]
            text_block = "\n".join(json.dumps(row.to_dict()) for _, row in chunk_df.iterrows())
            chunks.append(Document(page_content=text_block))

        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = FAISS.from_documents(chunks, embeddings)
        return vectorstore.as_retriever()

    def get_response(self, user_input):
        if self.retriever:
            docs = self.retriever.invoke(user_input)
            retrieved_context = "\n".join([doc.page_content for doc in docs])
            user_input = f"Context: {retrieved_context}\nQuestion: {user_input}"

        self.messages.append({"role": "user", "content": user_input})
        response = ollama.chat(model=self.model_name, messages=self.messages)
        answer = response.message.content
        self.messages.append({"role": "assistant", "content": answer})
        return answer

def main():
    ai_model = AIModel()

    print("Bot: Hello!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("end", ""):
            break
        response = ai_model.get_response(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    main()