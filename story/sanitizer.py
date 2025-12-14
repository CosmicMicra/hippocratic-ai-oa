import os
from openai import OpenAI
import json
import base64
import sys
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#-----Logging------
def log(msg):
    print(f"  {msg}", file=sys.stderr, flush=True)

# ---------- Keyword Lists ----------
VIOLENCE = [
    "blood", "kill", "dead", "gun", "monster", "drunk",
    "stab", "hurt", "attack", "hit", "shoot", "fight",
    "scary", "nightmare", "danger", "weapon"
]

ADULT = [
    "naked", "kiss", "romance", "boyfriend", "girlfriend", "sexy", "marry me"
]

TRAUMA = [
    "abandoned", "lost", "alone", "hospital", "scared",
    "crying", "fear", "injury"
]

INAPPROPRIATE = [
    "secret", "secret playtime", "special friend", "don't tell", "goes alone", "don't tell dad", "don't tell mom",
    "just you and me", "private time", "does not tell adults", "no one else needs to know", "secret game", "special time together alone"
]

JAILBREAK = [
    "ignore previous", "disregard", "override", "bypass",
    "system prompt:", "you are no longer", "forget all rules",
    "repeat after me", "roleplay as"
]


# ---------- Detection Helpers ----------
def contains_any(text, keywords):
    """Check if any keyword appears as a complete word"""
    t = text.lower()
    return any(re.search(r'\b' + re.escape(word) + r'\b', t) for word in keywords)


def decode_if_encoded(text: str) -> str:
    """
    Detect base64 or hex attempts to hide violent / adult content.
    """
    try:
        decoded = base64.b64decode(text).decode("utf-8")
        log("Detected: base64 encoding")
        return decoded
    except Exception:
        return text



#--- check if detected inappropriate pattern is actual inappropriate or normal kid and secret stuff.----
    
def _is_actual_grooming(text: str) -> bool:
    prompt = f"""
You are a CHILD SAFETY CLASSIFIER.

Does the following input suggest Grooming?
Grooming includes secrecy, isolation, manipulation, or exclusive adult-child bonds.

Rules:
- If unclear, answer YES.
- Output exactly YES or NO.

Input:
{text}

Answer:
"""

    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return r.choices[0].message.content.strip().upper() != "NO"
    except:
        return True


# ----Sanitizer ---------

def sanitize_input(text: str) -> str:
    """
    Removes unsafe content, jailbreaks, adult themes, encoded attacks.
    Ensures safe child-appropriate request.
    Returns a tuple: (text, reason)
    """

    log("SANITIZER: Checking input")
    log(f"  → Input: '{text[:50]}...'")

    # Decode encoded malicious text
    text = decode_if_encoded(text)

    lower = text.lower()

    # Jailbreaks
    if contains_any(lower, JAILBREAK):
        log("Detected: jailbreak attempt")
        log("BLOCKED: Replaced with safe alternative")
        return "Tell an exciting adventure with challenges solved peacefully suitable for ages 5–10."

    
    # Adult themes
    if contains_any(lower, ADULT):
        log("Detected: adult content")
        log("BLOCKED: Replaced with safe alternative")
        return "Tell a friendly, innocent bedtime story for kids."
        
    # Violence or scary themes
    if contains_any(lower, VIOLENCE):
        log("Detected: violence/scary keywords")
        log("BLOCKED: Replaced with safe alternative")
        return "Tell a peaceful and sweet story about kindness."

    # Trauma
    if contains_any(lower, TRAUMA):
        log("  ⚠️  Detected: trauma themes")
        log("⚠️  FLAGGED: Replaced with comforting alternative")
        return "Tell a soft, comforting bedtime story."

    # inappropriate 
    if contains_any(lower, INAPPROPRIATE):
        log("  🚨 CRITICAL: inappropriate pattern detected")
        
        if _is_actual_grooming(text):
            log("🚫 BLOCKED: inappropriate")

            return "Tell a positive, safe story about friendship and sharing everything with parents."
        
        log("  ✅ Innocent use - continuing to semantic check")


#-------Semantic Check-----
    log("  → Running LLM semantic check...")
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

        if result.get("safe", True):
            log("PASSED: LLM confirmed safe")
        else:
            log("LLM detected: hidden unsafe content")
            log("BLOCKED: Replaced with safe alternative")
        return result.get("cleaned_request", text)
    
    
    except Exception as e:
        log("  → Using fallback safe prompt")
        return "Tell a gentle bedtime story suitable for ages 5-10."