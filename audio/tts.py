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
        model="tts-1",
        voice="fable",
        input=text
    )

    #with open(filename, "wb") as f:
     #   f.write(audio.read())
    
    audio.stream_to_file(filename)

    return filename
