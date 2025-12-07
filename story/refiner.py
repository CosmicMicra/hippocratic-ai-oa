import os
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def refine_story(story_text: str, evaluation: dict) -> str:
    """
    Takes a story that failed quality check and improves it.
    
    Args:
        story_text: The story that needs improvement
        evaluation: Judge's feedback with what's wrong
    
    Returns:
        Improved version of the story
    """
    instructions = evaluation.get("rewrite_instructions", "Make it safer and more age-appropriate.")

    prompt = f"""You are a bedtime story editor for kids ages 5-10.

Original story that needs fixing:
"{story_text}"

Problems found:
{instructions}

Rewrite the story to fix these problems while keeping:
- Same characters and main idea
- Simple, gentle language
- Calm bedtime tone
- NO violence, fear, or sad content
- Length: 300-500 words

Fixed story:"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content



