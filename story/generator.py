import os
from openai import OpenAI
import json
import sys


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def log(msg):
    print(f"  {msg}", file=sys.stderr, flush=True)



def build_story_prompt(request, story_type):
    
    return f"""
    You are a gentle and creative bedtime storyteller for kids ages 5–10.
    Story type: {story_type} based on User request: {request}

    [Story content - 300-500 words]

    Rules:
    - Story that teaches some morals or values
    - No fear, no violence, no sadness.
    - Simple, calm language.
    - Clear beginning, middle, and end.
    - Friendly and comforting tone.
    - End story with "Good Night Seedlings + some positive message"
    """

def generate_first_draft(request, story_type):

    log("GENERATOR: Creating story")  
    log(f"  → Type: {story_type}")  
    log(f"  → Request: {request[:50]}...") 

    prompt = build_story_prompt(request, story_type)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7  
    )

    return response.choices[0].message.content
