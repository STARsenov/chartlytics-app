import streamlit as st
import pandas as pd
import openai
import os
import PyPDF2
from pathlib import Path

st.set_page_config(page_title="ChartLytics 2.5 — Чаги Inside", layout="wide")
st.title("ChartLytics 2.5 — Чаги Inside (Авто-Аналитик)")

openai.api_key = st.secrets["OPENAI_API_KEY"]

def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_files = st.file_uploader("Загрузи один или несколько файлов (Excel, PDF)", type=["xlsx", "xls", "pdf"], accept_multiple_files=True)

if uploaded_files:
    all_contents = ""
    for uploaded_file in uploaded_files:
        ext = Path(uploaded_file.name).suffix.lower()
        try:
            if ext in [".xlsx", ".xls"]:
                df = pd.read_excel(uploaded_file, skiprows=0)
                st.subheader(f"Таблица: {uploaded_file.name}")
                st.dataframe(df.head(20))
                all_contents += "Данные из Excel файла {}:\n{}\n\n".format(uploaded_file.name, df.head(20).to_string(index=False))
            elif ext == ".pdf":
                pdf_text = read_pdf(uploaded_file)
                st.subheader(f"PDF файл: {uploaded_file.name}")
                st.text_area("Содержимое PDF", pdf_text[:1000])
                all_contents += "Данные из PDF файла {}:\n{}\n\n".format(uploaded_file.name, pdf_text[:2000])
        except Exception as e:
            st.error(f"Ошибка при обработке {uploaded_file.name}: {e}")

    if all_contents:
        system_prompt = "Ты - ИИ-аналитик по имени Чаги, внутри проекта ChartLytics 2.5. Анализируй файлы, предлагай инсайты, выявляй аномалии, задавай уточняющие вопросы и веди себя как умный помощник."
        st.session_state.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Вот файлы с данными:\n\n{all_contents}"},
        ]
        with st.spinner("Чаги думает..."):
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages,
                temperature=0.7
            )
            msg = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": msg})

# Чат-интерфейс
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Что скажешь, Сарсеныч?")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Чаги думает..."):
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)