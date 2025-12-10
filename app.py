import streamlit as st
from main import create_story
from audio.transcriber import transcribe_audio
from audio.tts import speak_story

from utils.pdf_generator import generate_pdf

#page configuration
st.set_page_config(
    page_title="Sleepy Seeds - Bedtime Story Maker",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

#load css
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#load_css('styles.css')
        
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# main card
st.title("SLEEPY SEEDS 😴")
st.markdown("### Create a gentle bedtime story")

st.markdown('<p class="question-text">How would you like to tell me what story you want?</p>', unsafe_allow_html=True)


#Initialize session state

if 'story' not in st.session_state:
    st.session_state.story = None
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = None
if 'audio_processed' not in st.session_state: 
    st.session_state.audio_processed = False
if 'audio_file' not in st.session_state:  
    st.session_state.audio_file = None 

#Input mode selection

input_mode = st.radio(
    "Choose one:",
    ["🎤 Speak", "🧸 Category", "⌨️ Type"],
    key="input_mode",
    horizontal=True,
    label_visibility="collapsed"
)

user_request = None


#Option 1 - speak
if input_mode == "🎤 Speak":
    st.markdown("#### 🎙️ Talk and tell Seeds the story you'd love to hear")
    audio_bytes = st.audio_input("Press and speak...")
    
    if audio_bytes:
        # Automatically transcribe when audio is recorded
        if not st.session_state.audio_processed:
            with st.spinner("Transcribing your audio..."):
                try:
                    transcribed = transcribe_audio(audio_bytes)
                    st.session_state.transcribed_text = transcribed
                    st.session_state.audio_processed = True
                    st.success("✅ Audio transcribed!")
                except Exception as e:
                    st.error(f" Transcription error: {e}")
                    st.session_state.transcribed_text = ""
        
        # Editing transcripts
        if st.session_state.transcribed_text is not None:
            st.markdown("**📄 What you said:**")
            
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
    st.markdown("#### 🧸 Choose from Available Categories")
    
    story_type_choice = st.selectbox(
        "Pick one:",
        ["Select one...", "Princess", "Animals", "Cars", "Mixed / Surprise"],
        index=0
        #label_visibility="collapsed"
    )
    
    if story_type_choice != "Select one...":
        user_request = f"A {story_type_choice.lower()} story for kids."


#Option 3- type
        
else: 
    st.markdown("#### ⌨️ Type in your ideas")
    typed_text = st.text_input("Tell me what kind of story you want...")
    #label_visibility="collapsed"
    if typed_text.strip():
        user_request = typed_text

#Generate story
        
if st.button("✨ Generate Story", disabled=not user_request, use_container_width=True):
    with st.spinner("Creating your bedtime story..."):
        story = create_story(user_request)

    st.success("Your story is ready!")
    #st.markdown("### 📖 Your Bedtime Story")
    #st.markdown(f'<div class="story-container">{st.session_state.story}</div>', unsafe_allow_html=True)

    st.session_state.story = story
    st.session_state.transcribed_text = None
    st.session_state.audio_processed = False
    

#Action buttons
    
if st.session_state.story:
    st.markdown("---")  
    
    st.markdown("### 🎁 What would you like me to do?")

    col1, col2, col3 = st.columns(3)
    
    # Read aloud
    with col1:
        if st.button("🔊 Read Aloud", use_container_width=True):
            with st.spinner("Generating audio..."):
                audio_file = speak_story(st.session_state.story)
                st.session_state.audio_file = audio_file           # 
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

#audio player
    if 'audio_file' in st.session_state and st.session_state.audio_file:
        st.markdown("---")
        st.markdown("** 🎵 Now playing your story**")
        with open(st.session_state.audio_file, 'rb') as audio:
            st.audio(audio.read(), format='audio/mp3')

#Story display
    st.markdown("")
    st.markdown("### 📖 Your Bedtime Story")
   
    st.markdown(f'<div class="story-container">{st.session_state.story}</div>', unsafe_allow_html=True)
    

