# pyrefly: ignore [missing-import]
from groq import Groq
from core.config import GROQ_API_KEY, MODEL_NAME
from core.prompts import SYSTEM_PROMPT

_client = None


def _get_client():
    global _client
    if _client is None:
        if not GROQ_API_KEY or GROQ_API_KEY == "gsk_your_actual_key_here":
            raise ValueError(
                "GROQ_API_KEY is not set or is still the placeholder. Please set your GROQ_API_KEY in the backend/.env file."
            )
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


class GroqService:

    @staticmethod
    def generate(messages):
        formatted_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in messages:
            role = "user" if msg.role == "user" else "assistant"
            formatted_messages.append({"role": role, "content": msg.content})

        try:
            client = _get_client()
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=formatted_messages,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content if response.choices else ""
        except Exception as e:
            print(f"Error during Groq API call: {e}")
            import traceback
            traceback.print_exc()
            # Fall back gracefully to empty string
            return ""
    @staticmethod
    def transcribe(audio_path):
        import os
        try:
            client = _get_client()
            with open(audio_path, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=(os.path.basename(audio_path), file.read()),
                    model="whisper-large-v3",
                )
                return transcription.text
        except Exception as e:
            print(f"Error during Groq Whisper call: {e}")
            import traceback
            traceback.print_exc()
            return ""
