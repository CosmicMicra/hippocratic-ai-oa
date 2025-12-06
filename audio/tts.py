from openai import OpenAI
client = OpenAI()
import uuid

def speak_story(text):
    """
    Generates speech and saves as an mp3 file.
    Returns filename to be played by Streamlit.
    """
    filename = f"story_{uuid.uuid4().hex}.mp3"

    audio = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    with open(filename, "wb") as f:
        f.write(audio.read())

    return filename
