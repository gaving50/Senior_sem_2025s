import google.generativeai as genai

genai.configure(api_key="")

model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Initialize the chat session
# The session is used to maintain the context of the conversation
# Previous chat session cannot be recalled

chat = model.start_chat(history=[])  

def get_ai_response(prompt):
    try:
        response = chat.send_message(prompt) # Add error handling here.
        return response.text
    except Exception as e:
        print(f"Error getting response from Gemini: {e}")
        return "Sorry, I encountered an error processing your request."

def main():
#optimal_prompt not created yet, will be used for pre-prompting the AI
    prompt = open("optimal_prompt.txt","r")
    pre_prompt_response = get_ai_response(prompt)
    print("Pre-prompt response: ", pre_prompt_response)
    
    print("Welcome! Let's start a conversation. Type 'exit' to end.")
    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        ai_response = get_ai_response(user_input)
        print("AI: ", ai_response)

if __name__ == "__main__":
    main()