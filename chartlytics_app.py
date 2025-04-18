import streamlit as st
import pandas as pd
import openai
import PyPDF2
from pathlib import Path
from chartlytics_core import ChartLyticsCore

st.set_page_config(page_title="ChartLytics 3.0 — Multilingual AI Analyst", layout="wide")
st.title("ChartLytics 3.0 — Universal File Analysis")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Upload files
uploaded_files = st.file_uploader("Upload any files (Excel, PDF, etc.)", type=["xlsx", "xls", "pdf"], accept_multiple_files=True)

# Function to read PDFs
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Initialize analysis core
core = ChartLyticsCore(api_key=openai.api_key)

if uploaded_files:
    combined_text = ""
    filenames = []

    for file in uploaded_files:
        ext = Path(file.name).suffix.lower()
        filenames.append(file.name)
        if ext in [".xlsx", ".xls"]:
            df = pd.read_excel(file)
            st.subheader(f"Excel File: {file.name}")
            st.dataframe(df.head(15))
            combined_text += f"Excel file: {file.name}\n{df.head(15).to_string(index=False)}\n\n"
        elif ext == ".pdf":
            pdf_text = read_pdf(file)
            st.subheader(f"PDF File: {file.name}")
            st.text_area("PDF Preview", pdf_text[:1000])
            combined_text += f"PDF file: {file.name}\n{pdf_text[:2000]}\n\n"
        else:
            st.warning(f"Unsupported file type: {file.name}")

    # Use the core brain
    lang = core.initialize_context(combined_text)

    with st.spinner("ChartLytics thinking..."):
        initial_reply = core.respond("Analyze all the uploaded data and provide insights.")
        st.chat_message("assistant").markdown(initial_reply)

# Chat interface
user_input = st.chat_input("Talk to ChartLytics...")

if user_input:
    reply = core.respond(user_input)
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(reply)