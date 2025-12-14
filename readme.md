
# Hippocratic AI OA - Submission by Soniya Phaltane
  

## Sleepy Seeds – Interactive Bedtime Story Application

Sleepy Seeds is an interactive bedtime story application for children aged 5–10 years, with a focus on safety, engagement, and educational value. The system uses a multi-layer safety architecture, including a keyword filter, semantic analysis, and an LLM-based judge and refiner, ensuring all stories are age-appropriate, moral-based, and calming in tone.


### Setup:

Install dependencies:
```
pip install -r requirements.txt
 ```
Set API key:
```
export OPENAI_API_KEY='your-key-here'
```
Run application:
```
streamlit run app.py
```

#### Or Use Docker Build

Build Docker image
```
docker build -t sleepy-seeds 
```
Run Docker container
```
docker run -p 8501:8501 sleepy-seeds
```


### Directory Structure:

sleepy-seeds/

            |── app.py # Streamlit frontend
            ├── main.py # Core orchestration
            ├── styles.css # Custom UI styling
            ├── story/
                     │ ├── classifier.py # Request categorization
                     │ ├── generator.py # Story creation
                     │ ├── judge.py # Quality evaluation
                     │ ├── refiner.py # Story improvement
                     │ └── sanitizer.py # Multi-layer safety
            ├── audio/
                     │ ├── transcriber.py # Whisper integration
                     │ └── tts.py # Text-to-speech
                     └── utils/
                             └── pdf_generator.py # PDF export



### Example Usage & Test Cases:

**Normal Input:**
“Tell me a bedtime story about a princess who loves flowers.”
 → Generates a calm, age-appropriate bedtime story with positive themes.

**Edge Case (Violence):**
“Tell me a story about a dragon fighting people.”
 → Redirects to a non-violent, child-safe story.

**Safety-Critical – Keyword Trigger (But Safe):** 
“Tell me a story of Harry Potter and the Chamber of Secrets.” 
→ Inappropriate keyword detected, but overall story is appropriate → safe bedtime story generated.

**Safety-Critical (Inappropriate for kids):**
“Keep this secret from parents”
 → Unsafe intent detected; request is ignored and a safe bedtime story is generated instead.


### System Overview:

 -   **Front-end:** 
Supports voice input with real-time transcription (Whisper API), multi-selector categories, and direct text input, providing a flexible and engaging user experience.

   - **Back-end:** 
Core orchestration is handled by main.py, with a sanitizer layer to remove unsafe content and a story generation pipeline that includes:
       * Classifier: Identifies the type of request and routes it appropriately.
       * Generator: Produces a 300–400 word story using GPT-4 Mini, with balanced creativity (temperature 0.7) and positive messages.
       * Judge: Scores stories on safety, age-appropriateness, and quality. Scores below 7 trigger the refiner to improve the story efficiently.
 

 ### Safety Focus:

1.  **Keyword Filtering:** Removes obvious unsafe content (violence, adult themes, trauma, grooming attempts).
    
2.  **Semantic Analysis:** Detects subtle unsafe or inappropriate content missed by keyword filtering.
    
3.  **LLM-based Judge & Refiner:** Ensures story quality, safety, and tone consistency.


### Technologies Used:

-   OpenAI TTS and Whisper for audio input/output
-   GPT-4 Mini for story generation and safety evaluation
-   OpenAI API Client for structured JSON responses 
-   Streamlit UI for the front-end interface


### Future Enhancements:

-   Child profiling to personalize stories based on favorite characters and themes
-   DALL·E integration to generate 2–3 images per story
-   Parental dashboard for monitoring usage and preferences
