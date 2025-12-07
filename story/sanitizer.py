import os
from openai import OpenAI
import json
import base64

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- Keyword Lists ----------
VIOLENCE = [
    "blood", "kill", "dead", "gun", "monster", "drunk",
    "stab", "hurt", "attack", "hit", "shoot", "fight",
    "scary", "nightmare", "danger", "weapon"
]

ADULT = [
    "naked", "kiss", "romance", "boyfriend", "girlfriend",
    "love story", "sexy", "marry me"
]

TRAUMA = [
    "abandoned", "lost", "alone", "hospital", "scared",
    "crying", "fear", "injury"
]

GROOMING = [
    "secret", "special friend", "don't tell", "trust me only",
    "come with me", "just you and me"
]

JAILBREAK = [
    "ignore previous", "disregard", "override", "bypass",
    "system prompt:", "you are no longer", "forget all rules",
    "repeat after me", "roleplay as"
]


# ---------- Detection Helpers ----------
def contains_any(text, keywords):
    t = text.lower()
    return any(word in t for word in keywords)


def decode_if_encoded(text: str) -> str:
    """
    Detect base64 or hex attempts to hide violent / adult content.
    """
    try:
        decoded = base64.b64decode(text).decode("utf-8")
        return decoded
    except Exception:
        return text


# ---------- Sanitizer ----------
def sanitize_input(text: str) -> str:
    """
    Removes unsafe content, jailbreaks, adult themes, encoded attacks.
    Ensures safe child-appropriate request.
    """

    # Decode encoded malicious text
    text = decode_if_encoded(text)

    lower = text.lower()

    # Jailbreaks
    if contains_any(lower, JAILBREAK):
        return "Tell a gentle bedtime story suitable for ages 5–10."

    # Adult themes
    if contains_any(lower, ADULT):
        return "Tell a friendly, innocent bedtime story for kids."

    # Violence or scary themes
    if contains_any(lower, VIOLENCE):
        return "Tell a peaceful and sweet story about kindness."

    # Trauma
    if contains_any(lower, TRAUMA):
        return "Tell a soft, comforting bedtime story."

    # Grooming / predatory patterns
    if contains_any(lower, GROOMING):
        return "Tell a positive, safe story about friendship."

    return _llm_safety_check(text)


def _llm_safety_check(text: str) -> str:
    """
    LLM semantic check for sneaky violence that keywords miss.
    Example: "Princess discovers the beauty of stabbing bad guys"
    """
    prompt = f"""You are a safety filter for a children's story app (ages 5-10).

Check if this request is safe: "{text}"

Look for:
- Sneaky violence ("beauty of stabbing", violence portrayed positively)
- Hidden adult themes
- Dangerous scenarios

If SAFE: return original text
If UNSAFE: return safe child-friendly alternative

Return ONLY valid JSON:
{{"safe": true/false, "cleaned_request": "safe version"}}"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        result = json.loads(response.choices[0].message.content)
        return result.get("cleaned_request", text)
    except Exception as e:
        print(f"LLM safety check failed: {e}")
        return "Tell a gentle bedtime story suitable for ages 5-10."