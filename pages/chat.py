import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from logic.persona_builder import build_persona_description
from logic.conversation import generate_response

# --- Streamlit Config ---
st.set_page_config(page_title="Chat", page_icon="📱")

# --- WhatsApp-style Bubble CSS ---
st.markdown("""
    <style>
    .chat-row {
        display: flex;
        width: 100%;
    }

    .chat-row.user {
        justify-content: flex-end;
    }

    .chat-row.assistant {
        justify-content: flex-start;
    }

    .whatsapp-bubble {
        display: inline-block;
        padding: 10px 14px;
        border-radius: 16px;
        max-width: 85%;
        word-wrap: break-word;
        font-size: 0.95rem;
        line-height: 1.4;
    }

    .user-bubble {
        background-color: #dcf8c6;
    }

    .assistant-bubble {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
    }

    /* Remove background from chat container */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        box-shadow: none !important;
    }

    /* Sticky chat header */
    div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
        position: sticky;
        top: 3.5rem;
        background-color: white;
        z-index: 999;
    }

    .fixed-header {
        border-bottom: 1px solid #ddd;
        padding: 14px 14px;
    }

    .header-inner {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .header-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        object-fit: cover;
    }

    .header-text {
        font-size: 1.05rem;
        font-weight: 600;
        color: rgb(81, 168, 104);
    }
    </style>
""", unsafe_allow_html=True)

# --- Check Setup ---
if not st.session_state.get("ready"):
    st.warning("Please start again from the home page.")
    st.stop()


# --- Build Persona ---
coach_description = build_persona_description(
    st.session_state.communication_style,
    st.session_state.aggression,
    st.session_state.temperament,
    st.session_state.coaching_style,
)
scenario = st.session_state.scenario

# # --- Session Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

    # Automatically add a first message from the Gaffer if scenario isn't blank
    if st.session_state["scenario"] != "Blank canvas":
        system_message = (
            f"{coach_description}\n"
            f"Start the WhatsApp chat by confronting the player about this situation: '{scenario}'. "
            f"Be short, informal, and in-character as The Gaffer. Only send one message."
        )

        # Generate assistant's opening message
        response = generate_response(
            user_input="",
            coach_description=system_message,
            scenario="",
            history=[]
        )

        st.session_state["messages"].append({"role": "assistant", "content": response})

# --- Load Avatar as Base64 ---
def get_base64_image(image_path):
    img = Image.open(image_path)
    # Resize while maintaining aspect ratio, fit within 32x32
    img.thumbnail((128, 128), Image.LANCZOS)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_b64}"

avatar_base64 = get_base64_image("gaffer.png")

# --- Sticky Header ---
header = st.container()
with header:
    st.markdown(f"""
    <div class="fixed-header">
        <div class="header-inner">
            <img class="header-avatar" src="{avatar_base64}" alt="avatar" />
            <div class="header-text">The Gaffer</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Display Chat History ---
for msg in st.session_state.messages:
    role = msg["role"]
    role_class = "user" if role == "user" else "assistant"
    bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
    avatar = None if role == "user" else "gaffer.png"

    with st.chat_message(role, avatar=avatar):
        st.markdown(
            f'''
            <div class="chat-row {role_class}">
                <div class="whatsapp-bubble {bubble_class}">{msg["content"]}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

# --- Chat Input ---
if prompt := st.chat_input("Type a message"):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=None):
        st.markdown(
            f'''
            <div class="chat-row user">
                <div class="whatsapp-bubble user-bubble">{prompt}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    # Generate and display assistant response
    with st.chat_message("assistant", avatar="gaffer.png"):
        response = generate_response(prompt, coach_description, scenario, st.session_state.messages)
        st.markdown(
            f'''
            <div class="chat-row assistant">
                <div class="whatsapp-bubble assistant-bubble">{response}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    # Append assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
