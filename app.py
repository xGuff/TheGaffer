import streamlit as st

st.set_page_config(page_title="The Gaffer", page_icon="⚙️", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300&display=swap');

    html, body, [class*="css"] {
        font-family: 'Open Sans', sans-serif;
    }

    h1 {
        font-weight: 400 !important;
        color: rgb(81, 168, 104) !important;
        letter-spacing: -0.5px;
    }

    h2, h3 {
        color: rgb(81, 168, 104) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("TheGaffer")

st.markdown("""
<span style="color: black;">
Brought to you by <a href="https://xguff.substack.com/" style="color: orange; text-decoration: underline;">xGuff.substack.com</a>.
</span>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


st.session_state["scenario"] = st.selectbox(
    "Pick a scenario to rehearse:",
    [
        "Blank canvas",
        "Ask for more game time",
        "Admit you're carrying a knock",
        "Request a transfer",
        "Apologise for a red card",
        "Ask why you were subbed at halftime"
    ],
    accept_new_options=False
)

st.markdown("Customise The Gaffer's personality:")

st.markdown("""
<style>
.slider-labels {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    color: gray;
}
</style>
""", unsafe_allow_html=True)

st.markdown("**Communication Style**")
st.markdown('<div class="slider-labels"><span>Formal</span><span>Informal</span></div>', unsafe_allow_html=True)
st.session_state["communication_style"] = st.slider("", 0, 10, 5, key="communication_style_slider")

st.markdown("**Aggression**")
st.markdown('<div class="slider-labels"><span>People-Pleaser</span><span>Loose-Cannon</span></div>', unsafe_allow_html=True)
st.session_state["aggression"] = st.slider("", 0, 10, 5, key="aggression_slider")

st.markdown("**Temperament**")
st.markdown('<div class="slider-labels"><span>Calm</span><span>Hot-Headed</span></div>', unsafe_allow_html=True)
st.session_state["temperament"] = st.slider("", 0, 10, 5, key="temperament_slider")

st.markdown("**Coaching Style**")
st.markdown('<div class="slider-labels"><span>Modern</span><span>Old-School</span></div>', unsafe_allow_html=True)
st.session_state["coaching_style"] = st.slider("", 0, 10, 5, key="style_slider")

col1, col2, col3 = st.columns([1, 1, 1])  # Adjust column widths
with col2:
    if st.button("Enter Conversation", type='primary',use_container_width=True):
        st.session_state["ready"] = True
        st.switch_page("pages/chat.py")
