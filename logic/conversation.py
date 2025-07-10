from mistralai import Mistral
import streamlit as st
import re

api_key = st.secrets["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

from logic.persona_builder import build_persona_description 

def generate_response(user_input, communication_style, aggression, temperament, coaching_style, scenario, history, preset_choice=None):
    
    coach_description = build_persona_description(
        communication_style,
        aggression,
        temperament,
        coaching_style,
        preset_choice=preset_choice
    )

    system_message = (
        f"{coach_description}\n"
        "Your replies must be short, no more than one WhatsApp-style message. "
        "Reply in *one single message only*. No follow-ups, no lists, no new lines. "
        "You are The Gaffer. Stay in character."
    )

    if scenario == "Blank canvas":
        system_message += "\nA new player has messaged you for a chat."
    else:
        system_message += f"\nYou've heard that one of your players wants to talk about this situation: {scenario}. Talk to them directly, don’t use names — just talk like you would in a WhatsApp chat."

    messages = [{"role": "system", "content": system_message}]
    messages.extend(history[-6:])

    if user_input.strip():
        messages.append({"role": "user", "content": user_input})
    else:
        messages.append({
            "role": "user",
            "content": f"Send exactly one blunt, WhatsApp-style message to start the chat. Be casual but firm, e.g. 'What's this I'm hearing about {scenario.lower()}?'"
        })

    response = client.chat.complete(
        model="mistral-small",
        messages=messages,
        temperature=0.9,
        top_p=0.9,
        max_tokens=120 
    )

    content = response.choices[0].message.content.strip()
    return trim_incomplete_sentences(content)



def trim_incomplete_sentences(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return ' '.join(sentences[:-1]) if len(sentences) > 1 and not text.strip().endswith(('.', '!', '?')) else text
