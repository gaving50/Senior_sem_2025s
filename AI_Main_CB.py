import ollama
import pandas as pd
import json

# Function to load the data into a DF
def load_data(file_path):
    return pd.read_csv(file_path)

# Function to convert the DF to a string format
def prepare_data_for_model(df):
    # Convert DF to JSON
    return df.to_json(orient='records')

def get_initial_response(model_name, messages):
    response = ollama.chat(model=model_name, messages=messages)
    print("Bot:", response.message.content)

def continue_conversation(model_name, messages, data_context=None):
    while True:
        user_input = input("You: ")
        if user_input == "end" or not user_input:
            break  # exit loop on empty input or 'end' command
        
        if data_context:
            user_input = f"Data context: {data_context} Question: {user_input}"
        
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

    file_path = "c:\\Users\gavin\Desktop\idbm_top_1000.csv"  # Replace file
    data = load_data(file_path)
    data_context = prepare_data_for_model(data)
    
    get_initial_response(model_name, messages)
    continue_conversation(model_name, messages, data_context)

if __name__ == "__main__":
    main()