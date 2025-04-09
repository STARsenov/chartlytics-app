
import streamlit as st
import pandas as pd
import openai
import os

# Настройка OpenAI API
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
                prompt = f"Вот первые строки Excel-таблицы:\n{preview}\n\nПроанализируй, как опытный аналитик: найди закономерности, аномалии, важные показатели. Предложи, какие отчёты и графики можно построить, как будто ты помощник в бизнес-аналитике."

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }],
                    temperature=0.7
                )

                st.markdown("### Выводы и рекомендации:")
                st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Ошибка при обработке файла: {e}")
