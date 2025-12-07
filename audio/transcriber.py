import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(audio_bytes):
    """
    Takes audio bytes from Streamlit and sends to Whisper.
    """
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_bytes
    )
    return response.text
