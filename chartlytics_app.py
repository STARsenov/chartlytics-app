import streamlit as st
import pandas as pd
import openai
import PyPDF2
from pathlib import Path
from chartlytics_core import ChartLyticsCore

st.set_page_config(page_title="ChartLytics 3.0", layout="wide")
st.title("ChartLytics 3.0 — Smart Autonomous Analyst")

openai.api_key = st.secrets["OPENAI_API_KEY"]
core = ChartLyticsCore(api_key=openai.api_key)

uploaded_files = st.file_uploader("Upload multiple files (Excel, PDF)", type=["xlsx", "xls", "pdf"], accept_multiple_files=True)

if uploaded_files:
    full_content = ""
    for uploaded_file in uploaded_files:
        ext = Path(uploaded_file.name).suffix.lower()
        try:
            if ext in [".xlsx", ".xls"]:
                df = pd.read_excel(uploaded_file)
                st.subheader(f"📊 Data Preview: {uploaded_file.name}")
                st.dataframe(df.head(20))
                full_content += f"Extracted from Excel file {uploaded_file.name}:\n{df.head(20).to_string(index=False)}\n\n"
            elif ext == ".pdf":
                reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                st.subheader(f"📄 PDF Extract: {uploaded_file.name}")
                st.text_area("Preview", text[:1000])
                full_content += f"Extracted from PDF file {uploaded_file.name}:\n{text[:2000]}\n\n"
        except Exception as e:
            st.error(f"❌ Error reading {uploaded_file.name}: {e}")

    if full_content:
        st.info("🧠 Chartlytics thinking...")
        lang = core.initialize_context(full_content)
        reply = core.respond("Start analyzing the data, suggest insights, detect anomalies, ask follow-up questions, and propose visualizations.")
        st.markdown("### 🧠 Chartlytics Insight:")
        st.write(reply)

        # Optional follow-up
        user_followup = st.text_input("Continue the conversation:")
        if user_followup:
            st.info("💬 Thinking...")
            followup_reply = core.respond(user_followup)
            st.markdown("### 📌 Follow-up:")
            st.write(followup_reply)
