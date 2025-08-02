import streamlit as st
from datetime import datetime
from src.chat_state import init_session_state, update_session_state
from src.llm_handler import get_questions_from_llm
from src.ui_helpers import render_chat_history, render_pdf_export, apply_custom_style

# Configure Streamlit
st.set_page_config(page_title="Interview Prep Bot", layout="wide")
apply_custom_style()

# Initialize session state
init_session_state()

# Sidebar
with st.sidebar:
    st.title("Interview Bot")
    if st.button("New Chat"):
        session_id = f"Chat - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        st.session_state.chat_sessions[session_id] = []
        st.session_state.current_session = session_id
        st.session_state.chat_messages = []

    if st.session_state.chat_sessions:
        selected = st.selectbox(
            "Previous Chats",
            list(st.session_state.chat_sessions.keys())[::-1],
            key="select_chat"
        )
        if selected != st.session_state.current_session:
            st.session_state.current_session = selected
            st.session_state.chat_messages = st.session_state.chat_sessions[selected]

# Main Title
st.title("AI Interview Question Generator")

# Render previous messages
render_chat_history()

# Handle new user input
topic = st.chat_input("Enter a tech topic (e.g., CNNs, SQL)...")
if topic:
    update_session_state("user", topic)
    with st.chat_message("user"):
        st.markdown(topic)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response = get_questions_from_llm(topic, response_placeholder)
        update_session_state("assistant", response)

    render_pdf_export(topic, response)
