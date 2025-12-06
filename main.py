
from dotenv import load_dotenv
load_dotenv()

import json
import os
from openai import OpenAI


from story.sanitizer import sanitize_input
from story.classifier import classify_story
from story.generator import generate_first_draft
from story.judge import judge_story
from story.refiner import refine_story

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_story(request_text: str) -> str:
    """
    Main pipeline to generate a safe bedtime story.
    Includes:
    - Sanitization
    - First draft generation
    - LLM judge evaluation
    - Refinement loop with max 2 attempts
    - Safe fallback generation
    """

    # 1. Clean + de-jailbreak user input
    clean_request = sanitize_input(request_text)

    # 2. Identify type of story (princess, animals, cars, etc.)
    story_type = classify_story(clean_request)

    # 3. Generate first draft
    story = generate_first_draft(clean_request, story_type)

    # 4. Judge first draft
    evaluation = judge_story(story)

    # 5. Refinement loop
    max_refines = 2
    attempts = 0

    while evaluation.get("should_rewrite") and attempts < max_refines:
        story = refine_story(story, evaluation)
        evaluation = judge_story(story)
        attempts += 1

    # 6. Fallback if still unsafe after max attempts
    if evaluation.get("should_rewrite"):
        story = generate_first_draft(
            "Tell a gentle bedtime story appropriate for ages 5–10.",
            story_type,
        )

    return story


if __name__ == "__main__":
    user_input = input("Tell me your story idea: ")
    story = create_story(user_input)
    print("\n\n✨ Final Story ✨\n")
    print(story)
