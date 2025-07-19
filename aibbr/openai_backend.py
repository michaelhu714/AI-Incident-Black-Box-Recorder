# openai_backend.py
from openai import OpenAI
import os

# You must set your OpenAI API key as an environment variable
# export OPENAI_API_KEY="your-key-here"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai(input_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or another model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text}
        ]
    )
    return response.choices[0].message.content.strip()