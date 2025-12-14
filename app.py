import streamlit as st
from main import create_story
from audio.transcriber import transcribe_audio
from audio.tts import speak_story
from story.sanitizer import sanitize_input
from utils.pdf_generator import generate_pdf


#page configuration
st.set_page_config(
    page_title="Sleepy Seeds - Bedtime Story Maker",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

#load css('styles.css')
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
        if 'last_audio_id' not in st.session_state or id(audio_bytes) != st.session_state.last_audio_id:
            with st.spinner("Transcribing your audio..."):
                try:
                    transcribed = transcribe_audio(audio_bytes)
                    st.session_state.transcribed_text = transcribed
                    st.session_state.last_audio_id = id(audio_bytes)
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
                key=f"edit_transcript_{st.session_state.last_audio_id}"
            )
            
            # Use edited text as user request
            user_request = edited_text if edited_text.strip() else None
    else: 
        if 'last_audio_id' in st.session_state:
            del st.session_state.last_audio_id
        st.session_state.transcribed_text = None
    

#option 2 - category
            
elif input_mode == "🧸 Category":
    st.markdown("#### 🧸 Choose from Available Categories")
    
    story_categories= st.multiselect(
        "Pick one or more!:",
        ["Princess", "Animals", "Cars", "Surprise Me!", "Space", "Adventure", "Underwater"],
        default=None,
        max_selections=3
    )
    
    if story_categories: 
        if "Surprise Me!" in story_categories:
            user_request = "Create a surprise bedtime story with mixed themes and creative elements for kids"
        elif len(story_categories) == 1:
            user_request = f"A story about {story_categories[0].lower()} for kids"
        else:
            categories_text = ", ".join([cat.lower() for cat in story_categories if cat != "Surprise Me!"])
            user_request = f"A story that combines {categories_text} for kids"
    else:
        user_request = None


#Option 3- type
        
else: 
    st.markdown("#### ⌨️ Type in your ideas")
    typed_text = st.text_input("Tell me what kind of story you want...")
    #label_visibility="collapsed"
    if typed_text.strip():
        user_request = typed_text

#Generate story
        
if st.button("✨ Generate Story", disabled=not user_request, use_container_width=True):

    clean_check = sanitize_input(user_request)
    if clean_check and "sharing everything with parents" in clean_check.lower():
        st.error("⚠️ Inappropriate prompt for kids story")
        st.info("Creating a safe story instead")
    elif clean_check != user_request:
        st.warning("Generating appropriate story")

    with st.spinner("Creating your bedtime story..."):
        story = create_story(user_request)
        

    st.success("Your story is ready!")
    st.session_state.story = story
    st.session_state.transcribed_text = None
    

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
            st.session_state.audio_file = None 
            st.rerun()

#audio player
    if 'audio_file' in st.session_state and st.session_state.audio_file:
        st.markdown("---")
        st.markdown("**🎵 Now playing your story**")
        with open(st.session_state.audio_file, 'rb') as audio:
            st.audio(audio.read(), format='audio/mp3')

#Story display
    st.markdown("")
    st.markdown("### Your Bedtime Story")
    st.markdown(st.session_state.story)
    #st.markdown(f'<div class="story-container">{st.session_state.story}</div>', unsafe_allow_html=True)
    

