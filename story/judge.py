import os
from openai import OpenAI
import json
import sys

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
temperature=0

def log(msg):
    print(f"  {msg}", file=sys.stderr, flush=True)

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
    log("JUDGE: Evaluating story")
    log(f"  → Story length: {len(story_text)} chars")

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

    log(f"  → Safety: {data.get('safety', 'N/A')}/10")
    log(f"  → Age-fit: {data.get('age_fit', 'N/A')}/10")
    log(f"  → Tone: {data.get('tone', 'N/A')}/10")

    if data.get('should_rewrite', False):
            log("NOT APPROVED: Needs rewrite")
            log(f"  → Issues: {data.get('rewrite_instructions', 'Unknown')}")
    else:
        log("APPROVED: Story is good!")
        
    return data

    
