# NewsNinja 🎙️

Welcome to **NewsNinja**, a cutting-edge automated news broadcasting system designed to deliver personalized audio news reports. This application scrapes the latest news and Reddit discussions, analyzes the content using advanced AI, and generates professional-grade audio broadcasts. It prioritizes delivering concise, high-quality information tailored to your specific interests, making it the perfect tool for staying informed on the go.

## Features

- **News Aggregation:** Real-time news scraping from Google News via BrightData.
- **Social Sentiment:** Scrapes and analyzes relevant Reddit discussions for community perspective.
- **AI-Powered Scripting:** Uses advanced LLMs (OpenRouter/DeepSeek) to summarize content and generate engaging broadcast scripts.
- **Realistic Audio:** High-quality text-to-speech conversion using ElevenLabs for a professional listening experience.
- **Interactive UI:** User-friendly interface built with Streamlit for easy topic selection and control.

## Built With 🛠️

- **Backend:** Python (FastAPI)
- **Frontend:** Streamlit
- **AI/LLM:** OpenRouter, LangChain
- **TTS:** ElevenLabs
- **Scraping:** BrightData, PRAW (Reddit)

## Setup Instructions ⚙️

1. **Clone the repository:**

   ```bash
   git clone https://github.com/PraveenNPatil07/NewsNinja.git
   cd NewsNinja
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory and add the following keys:

   - `OPENROUTER_API_KEY`: API key for OpenRouter LLM access.
   - `ELEVENLABS_API_KEY`: API key for ElevenLabs TTS.
   - `BRIGHTDATA_API_TOKEN`: Token for BrightData scraping.
   - `WEB_UNLOCKER_ZONE`: BrightData zone configuration.
   - `REDDIT_CLIENT_ID`: Reddit App Client ID.
   - `REDDIT_CLIENT_SECRET`: Reddit App Client Secret.
   - `REDDIT_USER_AGENT`: Reddit App User Agent.

4. **Run the backend server:**

   ```bash
   python backend.py
   ```

5. **Run the frontend application:**
   ```bash
   python -m streamlit run frontend.py
   ```
   Access the app locally at `http://localhost:8501`.

## Usage Instructions 📖

1. **Select Topics:** Enter the news topics you are interested in (e.g., "Bitcoin", "AI", "Climate Change").
2. **Choose Source:** Select whether to fetch data from News, Reddit, or Both.
3. **Generate:** Click the "Generate Audio" button to start the process.
4. **Listen:** Once processing is complete, play or download the generated MP3 news report.

## File Structure 📂

```bash
NewsNinja/
│
├── backend.py           # FastAPI backend server
├── frontend.py          # Streamlit frontend UI
├── news_scraper.py      # Logic for scraping and analyzing news
├── reddit_scraper.py    # Logic for scraping and analyzing Reddit
├── utils.py             # Helper functions (TTS, URL generation, etc.)
├── models.py            # Pydantic data models
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .env                 # Environment variables
```

## Current Limitations and Future Plans 🚀

- **Limitations:**

  - Requires valid API keys for multiple services (OpenRouter, ElevenLabs, BrightData, Reddit).
  - Audio generation speed depends on external API latency.

- **Future Plans:**
  - Add support for more diverse news sources.
  - Implement custom voice cloning options.
  - Enable automated daily podcast feed generation.
