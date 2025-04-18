# chartlytics_app.py
# Streamlit front-end for ChartLytics 3.0

import streamlit as st
import pandas as pd
import openai
import PyPDF2
import docx
from PIL import Image
from io import BytesIO
from pathlib import Path
from chartlytics_core import ChartLyticsCore

st.set_page_config(page_title="ChartLytics 3.0 — Smart Data AI", layout="wide")
st.title("ChartLytics 3.0 — AI Analyst (Multimodal)")

openai.api_key = st.secrets["OPENAI_API_KEY"]
core = ChartLyticsCore(api_key=openai.api_key)

uploaded_files = st.file_uploader("Upload multiple files (Excel, PDF, DOCX, PNG, JPG)", 
                                   type=["xlsx", "xls", "pdf", "docx", "png", "jpg", "jpeg"], 
                                   accept_multiple_files=True)

if uploaded_files:
    full_context = ""
    for uploaded_file in uploaded_files:
        ext = Path(uploaded_file.name).suffix.lower()
try:
    df = pd.read_excel(uploaded_file, skiprows=0)
    st.subheader(f"Table: {uploaded_file.name}")
    st.dataframe(df.head(20))
    full_context += f"""Data from Excel {uploaded_file.name}:
{df.head(20).to_string(index=False)}

"""
except Exception as e:
    st.error(f"Error processing {uploaded_file.name}: {e}")

            elif ext == ".pdf":
                reader = PyPDF2.PdfReader(uploaded_file)
                pdf_text = "".join([p.extract_text() or "" for p in reader.pages])
                st.subheader(f"PDF Preview — {uploaded_file.name}")
                st.text_area("PDF Content", pdf_text[:1000])
                full_context += f"PDF content from {uploaded_file.name}:
{pdf_text[:2000]}

"
            elif ext == ".docx":
                doc = docx.Document(uploaded_file)
                doc_text = "
".join([para.text for para in doc.paragraphs])
                st.subheader(f"DOCX Preview — {uploaded_file.name}")
                st.text_area("Word Content", doc_text[:1000])
                full_context += f"Word content from {uploaded_file.name}:
{doc_text[:2000]}

"
            elif ext in [".png", ".jpg", ".jpeg"]:
                img = Image.open(uploaded_file)
                st.image(img, caption=f"Image: {uploaded_file.name}", use_column_width=True)
                full_context += f"Image file received: {uploaded_file.name}

"
        except Exception as e:
            st.error(f"Error reading {uploaded_file.name}: {e}")

    if full_context:
        lang = core.initialize_context(full_context)
        with st.spinner("ChartLytics thinking..."):
            result = core.respond("Start intelligent analysis based on uploaded data.")
        st.markdown("### ChartLytics AI Output:")
        st.write(result)
        st.session_state["latest_ai_output"] = result

        user_input = st.text_input("Your follow-up (any language):")
        if user_input:
            with st.spinner("ChartLytics thinking..."):
                followup = core.respond(user_input)
            st.markdown("### Follow-up Reply:")
            st.write(followup)
