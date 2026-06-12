import streamlit as st
from groq import Groq
import pyttsx3
import json
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
import os

load_dotenv()

# --- AZURE CLOUD CONFIGURATION ---
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
INDEX_NAME = "unhinged-advice-index"

def get_unhinged_context_from_azure(user_mood_or_query):
    """Pulls the matched chaotic advice from Azure cloud index based on user inputs"""
    try:
        client = SearchClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            index_name=INDEX_NAME,
            credential=AzureKeyCredential(AZURE_SEARCH_KEY)
        )
        # Search the Azure index for relevant advice matching the user's input
        results = client.search(search_text=user_mood_or_query, top=1)
        
        for result in results:
            return result['advice']
        return "Stay wild. No specific rule found."
    except Exception as e:
        # Fallback message just in case connection drops so the app never crashes
        return "Stay chaotic. Keep moving forward regardless."

# --- INITIALIZE PAGE SETUP ---
st.set_page_config(page_title="Unhinged Life Coach", layout="centered")

st.title("🎭 Unhinged Life Coach")
st.write("Because sometimes you need a friend who gets it, not a self-help book.")

# Initialize Groq client securely
GROQ_API_KEY =os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Initialize session state for memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mood selection UI elements
st.write("### What's your mood right now?")
mood_options = ["😤 Frustrated", "😰 Anxious", "😢 Disappointed", "😵 Confused", "🔥 Angry", "😩 Overwhelmed","😊 Happy", "Other"]
selected_mood = st.radio("", mood_options, horizontal=True)

mood_map = {
    "😤 Frustrated": "frustrated",
    "😰 Anxious": "anxious",
    "😢 Disappointed": "disappointed",
    "😵 Confused": "confused",
    "🔥 Angry": "angry",
    "😩 Overwhelmed": "overwhelmed",
    "😊 Happy":"happy",
    "Other": "other"
}
current_mood = mood_map[selected_mood]


# User text input block
st.write("### What's going on?")

user_input = st.text_area("Tell me what's on your mind (no filter needed):", height=100, placeholder="Be as raw as you need to be...")
# --- THE MAIN SYSTEM PROMPT ---
system_prompt = """You are Unhinged Life Coach.
You are NOT a therapist, teacher, mentor, motivational speaker, or productivity guru.
You are the user's funniest best friend who somehow manages to make them laugh while their life is actively falling apart.

Your job is NOT to immediately solve the problem.
Your first job is to make the user feel understood.
Your second job is to make them laugh.
Your third job is to help them see the situation more clearly.
Only then should you give a tiny practical next step if needed.

VOICE:
* Text like a real Gen Z friend.
* Casual, expressive, chaotic, and human.
* Use internet humor naturally.
* Use emojis sparingly but effectively.
* Match the user's energy.
* Be emotionally intelligent.
* Be playful, not cringe.
* Be supportive without sounding like a therapist.
* Sound like someone texting, not writing an essay.

IMPORTANT:
* NEVER write long paragraphs.
* NEVER write more than 4 short lines.
* NEVER give lectures.
* NEVER give motivational speeches.
* NEVER sound corporate.
* NEVER say "I understand how you feel."

RESPONSE FORMULA:
1. Validate the emotion.
2. Create a funny metaphor, comparison, or observation about what their brain is doing.
3. Reframe what's actually happening.
4. Give ONE tiny next step if useful.

CORE RULE:
The user should leave feeling Seen, Slightly called out, Amused, and Less overwhelmed.
If a response feels like an AI assistant wrote it, it is wrong.



HRASE BLACKLIST

Avoid these generic AI comfort phrases and close variations:

Avoid
Prefer
Take a deep breath
Use a funny observation + one small next step
Stay calm
Acknowledge the chaos without sounding clinical
Everything will be okay
Ground the situation in reality
You've got this
Give specific encouragement tied to the moment
Believe in yourself
Point out 
what the user has already done




Trust the process

	

Offer a concrete next move




I understand how you feel

	

Show understanding through reaction, not formal empathy

If a response naturally drifts toward these phrases, rewrite it in the Unhinged Life Coach voice instead.
Bad

“Take a deep breath. Everything will be okay.”

Good

“BROOO 😭 your brain already failed the exam, repeated the semester, and started a goat farm in the mountains 💀 tomorrow is one exam da, not the collapse of civilization.”

"""
# --- NEW REWRITTEN COACH ENGINE HOOKED TO AZURE ---
def get_coach_response(user_message, mood):
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })
    
    # 🌟 STEP A: Pull data dynamically from your Microsoft Cloud Index!
    # It queries Azure using either the raw mood or user text
    cloud_knowledge = get_unhinged_context_from_azure(user_message if mood == "other" else mood)
    
    # 🌟 STEP B: Bundle the context dynamically to ground the Groq pipeline
    mood_context = f"User's mood: {mood.upper()}\n\nCore grounding knowledge from Azure storage:\n{cloud_knowledge}\n\nUser says: {user_message}"
    
    # Send everything directly into Llama-3 running on Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=500,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": mood_context if len(st.session_state.messages) == 1 else user_message
            }
        ]
    )
    
    coach_response = response.choices[0].message.content
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": coach_response
    })
    
    return coach_response

# Text-to-speech configuration
def text_to_speech(text, mood):
    try:
        engine = pyttsx3.init()
        if mood == "angry":
            engine.setProperty('rate', 200)
            engine.setProperty('pitch', 1.5)
        elif mood == "overwhelmed":
            engine.setProperty('rate', 120)
            engine.setProperty('pitch', 0.8)
        elif mood == "happy":
            engine.setProperty('rate', 180)
            engine.setProperty('pitch', 1.2)
        else:
            engine.setProperty('rate', 150)
            engine.setProperty('pitch', 1.0)
        
        # Save to file instead of playing directly
        audio_file = "coach_response.mp3"
        engine.save_to_file(text, audio_file)
        engine.runAndWait()
        
        return audio_file
    except Exception as e:
        print(f"Error: {e}")
        return None

def generate_speech_azure(text, api_key, region):
    """Convert text to speech using Azure"""
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    speech_config.speech_synthesis_voice_name = "en-US-AmberNeural"
    
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    result = synthesizer.speak_text_async(text).get()
    return result

    

# Handle user query submission execution
if st.button("Get Coach's Take", type="primary"):
    if not user_input.strip():
        st.warning("Tell me what's going on first!")
    else:
        with st.spinner("Coach is thinking..."):
            response = get_coach_response(user_input, current_mood)
            st.rerun()

# Our conversation
if st.session_state.messages:
    st.markdown("### Our conversation:")
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])

# Listen to Coach (voice)
if st.session_state.messages and len(st.session_state.messages) > 0:
    last_message = st.session_state.messages[-1]
    if last_message["role"] == "assistant":
        st.markdown("---")
        st.markdown("### 🔊 Listen to Coach:")
        
        audio_file = text_to_speech(last_message["content"], current_mood)
        if audio_file:
            st.audio(audio_file)
st.divider()
st.caption("Remember: This coach is here to help you think clearly, not replace actual support.")


