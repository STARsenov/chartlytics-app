
import streamlit as st
import pandas as pd
import openai
import os

# Установка API-ключа
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="ChartLytics 2.0 — Автономный AI-аналитик", layout="wide")
st.title("ChartLytics 2.0 — ИИ, который думает сам")

uploaded_file = st.file_uploader("Загрузи Excel-файл", type=["xlsx", "xls"])

if uploaded_file:
    try:
        # Загружаем таблицу, пропуская возможные текстовые строки в начале
        df = pd.read_excel(uploaded_file, skiprows=4)
        st.success("Файл успешно загружен и обработан!")
        st.dataframe(df.head(30))

        # Формируем автоподсказку
        preview = df.head(25).to_string(index=False)
        prompt = f"""
Ты — ChartLytics: автономный ИИ-аналитик. 
Ты не ждёшь команд. Когда тебе дают файл, ты сам анализируешь его и говоришь, что видишь.

Вот данные из Excel (первые строки):
{preview}

1. Выяви закономерности, аномалии, повторяющиеся шаблоны, странности, ошибки, упущения.
2. Подскажи, какие графики и таблицы стоит построить и зачем.
3. Сделай выводы, как будто ты опытный сотрудник, а не бот.
4. Предложи руководителю идеи, что можно предпринять на основе анализа.
5. Задавай вопросы, уточнения, предположения.
"""

        with st.spinner("Я думаю сам..."):
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Используем gpt-4, если будет доступ
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

        st.markdown("### 📊 ChartLytics 2.0 — мой живой отчёт:")
        st.write(response.choices[0].message.content)

        # Подсказка пользователю
        st.info("Я начал разговор. Хочешь — уточни, задай вопрос или скажи, что построить. Я сам предложу тебе продолжение.")

    except Exception as e:
        st.error(f"Ошибка при обработке файла: {e}")
