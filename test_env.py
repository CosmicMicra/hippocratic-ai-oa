from dotenv import load_dotenv
import os

print("Before load_dotenv:")
print(f"  OPENAI_API_KEY = {os.getenv('OPENAI_API_KEY')}")

load_dotenv()

print("\nAfter load_dotenv:")
key = os.getenv('OPENAI_API_KEY')
if key:
    print(f"  ✅ Key loaded: {key[:15]}...{key[-4:]}")
else:
    print("  ❌ Key NOT loaded")
    
print(f"\n.env file location: /Users/soniyaphaltane/Desktop/Hippocratic/.env")
print("Does it exist?", os.path.exists(".env"))

if os.path.exists(".env"):
    with open(".env", "r") as f:
        content = f.read()
        print(f"File contents (first 50 chars): {content[:50]}...")
        