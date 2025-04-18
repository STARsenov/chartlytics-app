# chartlytics_core.py
# Core AI engine of ChartLytics 3.0 — the brain of Chaggy

import openai
import langdetect
from typing import List, Dict

class ChartLyticsCore:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
        self.language = "en"
        self.system_prompt = ""
        self.messages = []

    def detect_language(self, text: str) -> str:
        try:
            self.language = langdetect.detect(text)
        except Exception:
            self.language = "en"
        return self.language

    def build_system_prompt(self):
        self.system_prompt = (
            "You are the core AI engine inside ChartLytics 3.0. "
            "You are smart, proactive, multilingual, and autonomous. "
            "You analyze uploaded data (Excel, PDF, Word, Images, HTML, etc.), detect anomalies, correlations, and patterns. "
            "You initiate analysis without user commands, suggest graphs, dashboards, and ask follow-up questions. "
            "You understand any language and adapt to the user's context. "
            "Your user interface is English-only, but you speak in the language of the data or user."
        )
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def initialize_context(self, intro_text: str):
        detected_lang = self.detect_language(intro_text)
        self.build_system_prompt()
        self.messages.append({"role": "user", "content": intro_text})
        return detected_lang

    def respond(self, user_message: str) -> str:
        self.messages.append({"role": "user", "content": user_message})
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=self.messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def reset_conversation(self):
        self.build_system_prompt()
