import streamlit as st
import pandas as pd
import openai
import os

# Установка API-ключа
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="ChartLytics — AI Аналитик", layout="wide")
st.title("ChartLytics — Умный анализ Excel-файлов")

uploaded_file = st.file_uploader("Загрузи Excel-файл", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("Файл успешно загружен!")
        st.dataframe(df.head())

        if st.button("Проанализировать"):
            with st.spinner("Анализируем..."):
                preview = df.head(20).to_string(index=False)
                prompt = f"""Вот первые строки Excel-таблицы:\n{preview}\n\nПроанализируй как бизнес-аналитик: найди закономерности, проблемы, интересные факты. Предложи, что можно построить (графики, отчёты) и какие выводы можно сделать."""

                client = openai.OpenAI()
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )

                st.markdown("### Выводы и рекомендации:")
                st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Ошибка при обработке файла: {e}")
