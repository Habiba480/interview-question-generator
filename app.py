import streamlit as st
import time
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from fpdf import FPDF
from datetime import datetime
from io import BytesIO

llm = ChatOpenAI(
    base_url="http://0.0.0.0:1234/v1",
    model="meta-llama-3.1-8b-instruct",
    api_key="lm-studio"
)

st.set_page_config(page_title="Interview Prep Bot", layout="wide")

st.markdown(
    """
    <style>
    body { background-color: #0e0e0e; color: white; }
    .stChatMessage { background-color: #1a1a1a; padding: 1rem; border-radius: 1rem; }
    .stTextInput>div>div>input { background-color: #1a1a1a; color: white; }
    .css-1n76uvr { background-color: #111111; }
    .css-1c7y2kd { background-color: #1a1a1a; }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if "current_session" not in st.session_state:
    st.session_state.current_session = None
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

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

st.title("AI Interview Question Generator")

# Show chat history
for msg in st.session_state.chat_messages:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# Input topic
topic = st.chat_input("Enter a tech topic (e.g., CNNs, SQL)...")

if topic:
    st.session_state.chat_messages.append({"role": "user", "content": topic})
    with st.chat_message("user"):
        st.markdown(topic)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        prompt = f'''You are a technical interviewer assistant for programmers. Based on the topic "{topic}", generate relevant technical questions or coding problems.

Instructions:
- If the user specifies a number of questions, generate exactly that number.
- If the user specifies the type (MCQs, short answers, essays, coding problems), generate only that type.
- If no type is specified, generate a balanced mix of all types.
- If the user requests coding practice or "FAANG-style problems", generate coding challenges with example input/output and a brief Python solution.
- Correctly interpret typos in the user's request (e.g., 'wquestyions', 'miltiple chice').
- Adjust code examples based on the language mentioned (e.g., Python, Java, C++).
- For each question, label it with the appropriate Bloom’s Taxonomy level (e.g., Knowledge, Application, Analysis).

Use clean markdown formatting. Here's the required structure:

## Essay Questions

**1. What is ...?**  
**Answer:** Explanation here.

**2. Why is ... important?**  
**Answer:** Explanation here.

---

## Short Answer Questions

**1. What is ...?**  
**Answer:** Short answer here.

**2. How does ... work?**  
**Answer:** Short answer here.

---

## Multiple Choice Questions

**1. What is the purpose of a compiler?**  
**a)** To execute high-level code directly  
**b)** To convert code into machine language  
**c)** To check runtime errors  
**d)** To debug the program  

**Answer:** **b) To convert code into machine language**

---

## Coding Problems

**1. Write a function to reverse a string in Python.**  
**Example Input:** "hello"  
**Example Output:** "olleh"  
**Solution:**  
```python
def reverse_string(s):
    return s[::-1]
```'''

        response = llm([HumanMessage(content=prompt)]).content

        # Typing animation
        for char in response:
            full_response += char
            response_placeholder.code(full_response, language="markdown")
            time.sleep(0.005)

        # Final markdown rendering
        response_placeholder.markdown(full_response, unsafe_allow_html=True)

        # Store to session
        st.session_state.chat_messages.append({"role": "assistant", "content": full_response})
        if st.session_state.current_session:
            st.session_state.chat_sessions[st.session_state.current_session] = st.session_state.chat_messages

        # PDF export function
        def save_as_pdf(content):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)

            for line in content.strip().split("\n"):
                pdf.multi_cell(0, 10, txt=line.strip())

            buffer = BytesIO()
            pdf.output(buffer)
            buffer.seek(0)
            return buffer

        # PDF download UI
        with st.expander("📄 Export as PDF"):
            filename = f"{topic.replace(' ', '_')}_questions.pdf"
            if st.button("Generate PDF"):
                pdf_file = save_as_pdf(full_response)
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_file,
                    file_name=filename,
                    mime="application/pdf"
                )
