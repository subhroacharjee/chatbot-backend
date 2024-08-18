from openai import OpenAI
from app.core import assistant


class OpenAiAssistant(assistant.Assistant):
    def __init__(self):
        self.openai = OpenAI()

    def get_response_for_prompt(self, prompt: str) -> str:
        response = self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Answer questions briefly, in a sentence or less.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            stream=False,
        )

        return f"{response.choices[0].message.content}"


def get_assistant():
    assistant = OpenAiAssistant()
    try:
        yield assistant
    finally:
        pass
