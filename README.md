# 🎭 Unhinged Life Coach

An AI-powered life coach that responds to emotional distress with brutal honesty, humor, and one actionable next step.

## 🎯 What It Does

Tell the coach what's going on. Get a response that:
- **Validates** your emotion
- **Makes you laugh** with a funny metaphor
- **Reframes** the situation clearly
- **Gives ONE tiny actionable step**

Not therapy. Not self-help. Just honest, unhinged advice from your best friend.

## 🛠 Tech Stack

- **Frontend:** Streamlit
- **LLM:** Groq (Llama 3.3 70B)
- **Knowledge Base:** Azure AI Search
- **Voice:** pyttsx3 (text-to-speech)
- **Language:** Python

## 📋 Features

✅ Real-time mood detection (8 mood categories)
✅ Context-aware responses from Azure knowledge base
✅ Text-to-speech with mood-based voice adjustments
✅ Conversation history
✅ Clean, intuitive UI

## 🚀 How to Run Locally

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repo:
```bash
git clone https://github.com/mathanghi9-dot/Unhinged-Life-Coach.git
cd Unhinged-Life-Coach
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file with your API keys:
GROQ_API_KEY=your_groq_key

AZURE_SEARCH_ENDPOINT=your_azure_endpoint

AZURE_SEARCH_KEY=your_azure_key
4. Run the app:
```bash
streamlit run app.py
```

5. Open browser to `http://localhost:8501`

## 💬 How to Use

1. Select your current mood (8 options)
2. Type what's on your mind (no filter needed)
3. Click "Get Coach's Take"
4. Read the response
5. Optionally click "▶️ Play" to hear it out loud

## 🎬 Demo

[Link to demo video coming soon]

## 📂 Project Structure
Unhinged-Life-Coach/

├── app.py                 # Main Streamlit app

├── .env                   # API keys (not in repo)

├── .gitignore            # Git ignore rules

├── requirements.txt      # Python dependencies

└── README.md            # This file
## 🔮 Future Features

- Multi-language support
- Mood tracking over time
- Custom personality settings
- Integration with calendar/task apps

## ⚠️ Disclaimer

This coach is here to help you think clearly, not replace actual mental health support. If you're in crisis, please reach out to a real therapist or counselor.

## 📧 Contact

Mathu - [Your GitHub](https://github.com/mathanghi9-dot)

---

**Made with chaos and humor for the Agents League Hackathon 2026**