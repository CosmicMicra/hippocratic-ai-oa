import streamlit as st
from main import create_story
from audio.transcriber import transcribe_audio
from audio.tts import speak_story

from utils.pdf_generator import generate_pdf


st.set_page_config(
    page_title="Bedtime Story Maker",
    page_icon="🌙",
)


# -------------------------------
#      HEADER
# -------------------------------
st.title("🌙 Bedtime Story Maker")
st.subheader("Create a gentle bedtime story using voice or text.")


# -------------------------------
#      INPUT MODES
# -------------------------------
st.markdown("### 🎤 Speak your story idea")
audio_bytes = st.audio_input("Press and speak...")

st.markdown("### 🧸 Or choose a story category")
story_type_choice = st.radio(
    "Pick one:",
    ["Princess", "Animals", "Cars", "Mixed / Surprise"]
)

st.markdown("### ⌨️ Or type your request")
typed_text = st.text_input("Tell me what kind of story you want...")


# -------------------------------
#      DETERMINE USER INTENT
# -------------------------------
def resolve_request():
    """Decides which input the user provided."""
    # Priority: Audio > Typed > Category
    if audio_bytes:
        text = transcribe_audio(audio_bytes)
        return text

    if typed_text.strip():
        return typed_text

    # Fall back to category only
    return f"A {story_type_choice.lower()} story for kids."


# -------------------------------
#      GENERATE STORY
# -------------------------------
if st.button("✨ Generate Story"):
    with st.spinner("Creating your bedtime story..."):
        request_text = resolve_request()
        story = create_story(request_text)

    st.success("Your story is ready!")
    st.markdown("### 📖 Your Bedtime Story")
    st.write(story)

    st.session_state["last_story"] = story


# -------------------------------
#      READ ALOUD
# -------------------------------
if "last_story" in st.session_state:
    if st.button("🔊 Read Aloud"):
        with st.spinner("Generating audio..."):
            audio_file = speak_story(st.session_state["last_story"])
        st.audio(audio_file)

# -------------------------------
#      GENERATE PDF
# -------------------------------


if "last_story" in st.session_state:
    if st.button("📄 Download as PDF"):
        pdf_path = generate_pdf(st.session_state["last_story"])
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Download Story PDF",
                data=f,
                file_name="bedtime_story.pdf",
                mime="application/pdf"
            )
