import streamlit as st
import pandas as pd
import openai
import PyPDF2
from pathlib import Path

st.set_page_config(page_title="ChartLytics 2.6 — Powered by Chaggy", layout="wide")
st.title("ChartLytics 2.6 — Your AI-Powered Analyst")

openai.api_key = st.secrets["OPENAI_API_KEY"]

def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Init chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Upload
uploaded_files = st.file_uploader("Upload Excel or PDF files", type=["xlsx", "xls", "pdf"], accept_multiple_files=True)

if uploaded_files:
    combined_content = ""
    for uploaded_file in uploaded_files:
        ext = Path(uploaded_file.name).suffix.lower()
        try:
            if ext in [".xlsx", ".xls"]:
                df = pd.read_excel(uploaded_file, skiprows=0)
                st.subheader(f"Excel File: {uploaded_file.name}")
                st.dataframe(df.head(20))
                combined_content += "From Excel file {}:\n{}\n\n".format(uploaded_file.name, df.head(20).to_string(index=False))
            elif ext == ".pdf":
                pdf_text = read_pdf(uploaded_file)
                st.subheader(f"PDF File: {uploaded_file.name}")
                st.text_area("PDF Content", pdf_text[:1000])
                combined_content += "From PDF file {}:\n{}\n\n".format(uploaded_file.name, pdf_text[:2000])
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")

    if combined_content:
        system_prompt = (
            "You are an intelligent, proactive, and confident AI analyst named Chaggy inside ChartLytics 2.6. "
            "You analyze uploaded documents (Excel, PDF), detect patterns, highlight anomalies, suggest insights and possible visualizations. "
            "You speak clearly and directly. You initiate analysis without waiting. Ask follow-up questions. Guide the user like a business expert. "
        )
        st.session_state.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here are the uploaded files:

{combined_content}"},
        ]
        with st.spinner("ChartLytics thinking..."):
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages,
                temperature=0.7
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})

# Display full chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Talk to ChartLytics...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("ChartLytics thinking..."):
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)