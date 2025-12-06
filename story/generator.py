import os
from openai import OpenAI
import json


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_story_prompt(request, story_type):
    return f"""
    You are a gentle bedtime storyteller for kids ages 5–10.
    Story type: {story_type}
    User request: {request}

    Rules:
    - No fear, no violence, no sadness.
    - Simple, calm language.
    - Clear beginning, middle, and end.
    - Friendly and comforting tone.
    """

def generate_first_draft(request, story_type):
    prompt = build_story_prompt(request, story_type)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
