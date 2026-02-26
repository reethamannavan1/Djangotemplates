import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_ai(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful resume assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content