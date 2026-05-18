import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "Qwen/Qwen2.5-Coder-7B-Instruct"
)

client = InferenceClient(token=HF_TOKEN)


def explain_with_ai(code: str) -> str:
    if not HF_TOKEN:
        return "HF_TOKEN is missing in .env"

    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert embedded systems engineer. "
                    "Explain the code for beginners and mention any bugs "
                    "or best-practice improvements."
                ),
            },
            {
                "role": "user",
                "content": code,
            },
        ]

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=400,
            temperature=0.2,
        )

        if response and response.choices:
            content = response.choices[0].message.content
            if content:
                return content

        return "No explanation was returned by the model."

    except Exception as e:
        return f"AI explanation unavailable: {str(e)}"