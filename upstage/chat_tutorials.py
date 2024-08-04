# https://developers.upstage.ai/docs/getting-started/tutorials/chatbot

import os

import dotenv
from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI(
    api_key=os.getenv("UPSTAGE_API_KEY"),
    base_url="https://api.upstage.ai/v1/solar"
)

# this system prompt will be used globally on the chat session.
system_prompt = {
    "role": "system",
    "content": "You are a helpful assistant."
}

model = "solar-1-mini-chat"

# Keep chat history in a list.
chat_history = []

# Set a limit for the chat history to manage the token count.
history_size = 10

while True:
    # Step 1: Get user input.
    user_prompt = input("User: ")
    chat_history.append({
        "role": "user",
        "content": user_prompt
    })

    # Step 2: Use the chat history to generate the chatbot's response.
    messages = [system_prompt] + chat_history
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )

    # Step 3: Output the Solar response chunks.
    print("SOLAR: ", end="")
    solar_response = ""
    for chunk in stream:
        response_content = chunk.choices[0].delta.content
        if response_content is not None:
            solar_response += response_content
            print(response_content, end="")
    print()  # Finish response output.

    # Step 4: Append the Solar response to the chat history.
    chat_history.append({
        "role": "assistant",
        "content": solar_response
    })

    # Step 5: Ensure the chat history doesn't exceed the size limit.
    chat_history = chat_history[:history_size]

##################################################
# User:  Hi, SOLAR!
# SOLAR: Hello! How can I help you today?
# User:  What did I say?
# SOLAR: You said "Hi, SOLAR!"
##################################################
