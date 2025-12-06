import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_story(text: str) -> str:
    text = text.lower()

    if "princess" in text or "barbie" in text:
        return "princess"
    if "car" in text or "truck" in text:
        return "cars"
    if any(animal in text for animal in ["cat", "dog", "bunny", "bird"]):
        return "animals"
    
    return "generic"
