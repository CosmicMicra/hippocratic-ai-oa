import os
from openai import OpenAI
from story.sanitizer import sanitize_input
from story.classifier import classify_story
from story.generator import generate_first_draft
from story.judge import judge_story

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def create_story(request_text: str) -> str:
    clean_request = sanitize_input(request_text)
    story_type = classify_story(clean_request)

    # First draft
    story = generate_first_draft(clean_request, story_type)

    # Judge the first draft
    evaluation = judge_story(story)

    max_refines = 2
    attempts = 0

    # Refinement loop
    while evaluation.get("should_rewrite") and attempts < max_refines:
        story = refine_story(story, evaluation)
        evaluation = judge_story(story)
        attempts += 1

    # Fallback if story still not acceptable after max attempts
    if evaluation.get("should_rewrite") and attempts == max_refines:
        print("⚠️ Could not perfect the story. Showing closest safe version.")
        story = generate_first_draft(
            "Tell a gentle bedtime story appropriate for ages 5-10.",
            story_type
        )

    return story
