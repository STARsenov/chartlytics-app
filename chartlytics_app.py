
import streamlit as st
import pandas as pd
import openai
import os
import PyPDF2

st.set_page_config(page_title="ChartLytics 2.5 — Чаги Inside", layout="wide")
st.title("ChartLytics 2.5 — Чаги Inside (Авто-Аналитик)")

openai.api_key = st.secrets["OPENAI_API_KEY"]

def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

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
    all_contents += f"""Данные из Excel файла {uploaded_file.name}:
{df.head(20).to_string(index=False)}

"""
elif ext == ".pdf":
    pdf_text = read_pdf(uploaded_file)
    st.subheader(f"PDF файл: {uploaded_file.name}")
    st.text_area("Содержимое PDF", pdf_text[:1000])
    all_contents += f"""Данные из PDF файла {uploaded_file.name}:
{pdf_text[:2000]}

"
        except Exception as e:
            st.error(f"Ошибка при обработке {uploaded_file.name}: {e}")

    if all_contents:
        with st.spinner("Чаги думает..."):
            prompt = f"""Ты - ИИ-аналитик по имени Чаги, внутри системы ChartLytics 2.5. Тебе загрузили следующие файлы с данными:

{all_contents}

Проанализируй содержимое, выяви закономерности, аномалии, тренды, и предложи 3–5 полезных инсайтов. Используй деловой стиль, предлагай варианты визуализации. Задай пользователю уточняющие вопросы, если чего-то не хватает."""
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            st.markdown("### Ответ Чаги:")
            st.write(response.choices[0].message.content)
