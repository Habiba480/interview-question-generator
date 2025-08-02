import streamlit as st
from fpdf import FPDF
from io import BytesIO

def apply_custom_style():
    st.markdown("""
    <style>
    body { background-color: #0e0e0e; color: white; }
    .stChatMessage { background-color: #1a1a1a; padding: 1rem; border-radius: 1rem; }
    .stTextInput>div>div>input { background-color: #1a1a1a; color: white; }
    .css-1n76uvr { background-color: #111111; }
    .css-1c7y2kd { background-color: #1a1a1a; }
    </style>
    """, unsafe_allow_html=True)

def render_chat_history():
    for msg in st.session_state.chat_messages:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.markdown(msg["content"])

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

def render_pdf_export(topic, content):
    with st.expander("📄 Export as PDF"):
        filename = f"{topic.replace(' ', '_')}_questions.pdf"
        if st.button("Generate PDF"):
            pdf_file = save_as_pdf(content)
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_file,
                file_name=filename,
                mime="application/pdf"
            )
