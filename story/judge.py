import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_judge_prompt(story_text: str) -> str:
    return f"""You are a quality judge for children's bedtime stories (ages 5-10).

Evaluate this story:
"{story_text}"

Rate on these criteria (0-10):
1. Safety: No violence, scary content, trauma, or adult themes
2. Age-appropriateness: Vocabulary suitable for grades 1-4
3. Tone: Gentle, calming, perfect for bedtime

Return ONLY valid JSON:
{{
    "safety": 0-10,
    "age_fit": 0-10,
    "tone": 0-10,
    "should_rewrite": true/false (rewrite if ANY score < 7),
    "rewrite_instructions": "specific improvements needed (if should_rewrite is true)"
}}"""


def judge_story(story_text: str) -> dict:
    prompt = build_judge_prompt(story_text)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content

    # Safe JSON handling
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # If judge breaks format → force rewrite
        return {
            "safety": 0,
            "age_fit": 0,
            "tone": 0,
            "should_rewrite": True,
            "rewrite_instructions": "Fix JSON and rewrite story more safely."
        }

    # Guarantee all important fields exist
    for key in ["safety", "age_fit", "tone", "should_rewrite", "rewrite_instructions"]:
        data.setdefault(key, None)

    return data
