import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def judge_story(story_text: str) -> dict:
    prompt = build_judge_prompt(story_text)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message["content"]

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
