from mistralai import Mistral
import streamlit as st

# Load API key from .streamlit/secrets.toml
api_key = st.secrets["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

def generate_response(user_input, coach_description, scenario, history):
    # Build the system message
    system_message = coach_description
    if scenario == "Blank canvas":
        system_message += "\nA new player has approached you for a chat."
    else:
        system_message += f"\nThe player is coming to you with this situation: '{scenario}'."

    # Start message list with the system prompt
    messages = [{"role": "system", "content": system_message}]

    # Add prior chat history (if any)
    messages.extend(history[-6:])

    # Add user input (if present), otherwise add a dummy prompt
    if user_input.strip():
        messages.append({"role": "user", "content": user_input})
    else:
        # Use a fake prompt to trigger the assistant's opening message
        messages.append({"role": "user", "content": "Start the conversation, along the lines of: What's this I'm hearing about the scenario?"})

    # Mistral call
    response = client.chat.complete(
        model="mistral-small",
        messages=messages,
        temperature=0.4,
        max_tokens=150,
    )

    return response.choices[0].message.content
