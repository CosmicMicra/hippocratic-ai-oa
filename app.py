import streamlit as st
from main import create_story
from audio.transcriber import transcribe_audio
from audio.tts import speak_story

from utils.pdf_generator import generate_pdf


st.set_page_config(
    page_title="Bedtime Story Maker",
    page_icon="🌙",
)

st.title("🌙 Bedtime Story Maker")
st.subheader("Create a gentle bedtime story using voice or text.")



#state

if 'story' not in st.session_state:
    st.session_state.story = None
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = None
if 'audio_processed' not in st.session_state: 
    st.session_state.audio_processed = False
if 'audio_file' not in st.session_state:  
    st.session_state.audio_file = None 

#Input mode selection
st.markdown("### 🎨 How would you like to tell me what story you want?")

input_mode = st.radio(
    "Choose one:",
    ["🎤 Speak", "🧸 Category", "⌨️ Type"],
    key="input_mode"
)

user_request = None


#Option 1 - speak
if input_mode == "🎤 Speak":
    st.markdown("### 🎤 Speak your story idea")
    audio_bytes = st.audio_input("Press and speak...")
    
    if audio_bytes:
        # Automatically transcribe when audio is recorded
        if not st.session_state.audio_processed:
            with st.spinner("🔄 Auto-transcribing your audio..."):
                try:
                    transcribed = transcribe_audio(audio_bytes)
                    st.session_state.transcribed_text = transcribed
                    st.session_state.audio_processed = True
                    st.success("✅ Audio transcribed!")
                except Exception as e:
                    st.error(f"❌ Transcription error: {e}")
                    st.session_state.transcribed_text = ""
        
        # Editing transcripts
        if st.session_state.transcribed_text is not None:
            st.markdown("#### 📄 What you said:")
            
            # Show editable text area
            edited_text = st.text_area(
                "Edit your request if needed:",
                value=st.session_state.transcribed_text,
                height=100,
                key="edit_transcript"
            )
            
            # Use edited text as user request
            user_request = edited_text if edited_text.strip() else None
    
    # Reset audio_processed when audio is cleared
    else:
        if st.session_state.audio_processed:
            st.session_state.audio_processed = False
            st.session_state.transcribed_text = None



#option 2 - category
            
elif input_mode == "🧸 Category":
    st.markdown("### 🧸 Choose a story category")
    
    # CHANGE: Use selectbox instead of radio
    story_type_choice = st.selectbox(
        "Pick one:",
        ["Select one...", "Princess", "Animals", "Cars", "Mixed / Surprise"],
        index=0
    )
    
    if story_type_choice != "Select one...":
        user_request = f"A {story_type_choice.lower()} story for kids."


#Option 3- type
        
else: 
    st.markdown("### ⌨️ Type your request")
    typed_text = st.text_input("Tell me what kind of story you want...")
    
    if typed_text.strip():
        user_request = typed_text

#Generate story
        
if st.button("✨ Generate Story", disabled=not user_request):
    with st.spinner("Creating your bedtime story..."):
        story = create_story(user_request)

    st.success("Your story is ready!")
    st.markdown("### 📖 Your Bedtime Story")
    st.write(story)

    st.session_state.story = story
    st.session_state.transcribed_text = None
    st.session_state.audio_processed = False
    

#Action buttons
    
if st.session_state.story:
    st.markdown("---")                                    
    st.markdown("### 🎁 What would you like to do?")
    col1, col2, col3 = st.columns(3)
    
    # Read aloud
    with col1:
        if st.button("🔊 Read Aloud", use_container_width=True):
            with st.spinner("Generating audio..."):
                audio_file = speak_story(st.session_state.story)
                st.session_state.audio_file = audio_file           # ← ADD THIS (Line 136)
            st.success("✅ Audio ready!")
    
    # Download PDF 
    with col2:
        pdf_path = generate_pdf(st.session_state.story)
        with open(pdf_path, "rb") as f:
            
            st.download_button(
                label="📄 Download PDF",
                data=f,
                file_name="bedtime_story.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    # New story 
    with col3:
        if st.button("🔄 New Story", use_container_width=True):
            st.session_state.story = None
            st.session_state.transcribed_text = None
            st.session_state.audio_processed = False
            st.session_state.audio_file = None 
            st.rerun()

    if 'audio_file' in st.session_state and st.session_state.audio_file:
        st.markdown("---")
        st.markdown("#### 🎵 Now playing your story")
        with open(st.session_state.audio_file, 'rb') as audio:
            st.audio(audio.read(), format='audio/mp3')