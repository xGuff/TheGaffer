from mistralai import Mistral
import streamlit as st

api_key = st.secrets["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

def generate_response(user_input, coach_description, scenario, history):
    # Build strict system message
    system_message = (
        f"{coach_description}\n"
        "Your replies must be short, no more than one WhatsApp-style message. "
        "Reply in *one single message only*. No follow-ups, no lists, no new lines. "
        "You are The Gaffer. Stay in character."
    )

    # Scenario-specific intro
    if scenario == "Blank canvas":
        system_message += "\nA new player has messaged you for a chat."
    else:
        system_message += f"\nThe player is coming to you with this situation: '{scenario}'."

    # Messages
    messages = [{"role": "system", "content": system_message}]
    messages.extend(history[-6:])

    # Opening or response
    if user_input.strip():
        messages.append({"role": "user", "content": user_input})
    else:
        messages.append({
            "role": "user",
            "content": f"Send exactly one blunt, WhatsApp-style message to start the chat. Be casual but firm, e.g. 'What's this I'm hearing about {scenario.lower()}?'"
        })

    # Call LLM
    response = client.chat.complete(
        model="mistral-small",
        messages=messages,
        temperature=0.5,
        top_p=0.9,
        max_tokens=120 
    )

    return response.choices[0].message.content.strip().strip('"')
