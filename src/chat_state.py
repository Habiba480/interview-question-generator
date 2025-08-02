def init_session_state():
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}
    if "current_session" not in st.session_state:
        st.session_state.current_session = None
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

def update_session_state(role, content):
    st.session_state.chat_messages.append({"role": role, "content": content})
    if st.session_state.current_session:
        st.session_state.chat_sessions[st.session_state.current_session] = st.session_state.chat_messages
