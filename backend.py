from fastapi import FastAPI, HTTPException, Response
from pathlib import Path
from dotenv import load_dotenv
import traceback
import os

from models import NewsRequest
from utils import generate_broadcast_news, text_to_audio_elevenlabs_sdk
# 1. CHANGED: Import NewsEngine (the new name), not NewsScraper
from news_scraper import NewsEngine 
from reddit_scraper import scrape_reddit_topics

app = FastAPI()
load_dotenv()

@app.post("/generate-news-audio")
async def generate_news_audio(request: NewsRequest):
    try:
        print(f"Received request for topics: {request.topics}, source_type: {request.source_type}")
        results = {}
        
        if request.source_type in ["news", "both"]:
            print("Initializing NewsEngine...")
            # 2. CHANGED: Create an instance of NewsEngine
            news_scraper = NewsEngine()
            print(f"NewsEngine type: {type(news_scraper)}")
            
            print("Calling scrape_news...")
            news_results = await news_scraper.scrape_news(request.topics)
            print(f"News results: {news_results}")
            results["news"] = news_results
        
        if request.source_type in ["reddit", "both"]:
            print("Scraping Reddit...")
            reddit_results = await scrape_reddit_topics(request.topics)
            print(f"Reddit results: {reddit_results}")
            results["reddit"] = reddit_results

        # Safely extract nested data with defaults
        news_data = results.get("news", {})
        reddit_data = results.get("reddit", {})
        
        print("Generating broadcast news...")
        news_summary = generate_broadcast_news(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            news_data=news_data,
            reddit_data=reddit_data,
            topics=request.topics
        )
        print(f"Generated summary length: {len(news_summary)} characters")

        print("Converting to audio...")
        audio_path = text_to_audio_elevenlabs_sdk(
            text=news_summary,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
            output_dir="audio"
        )
        print(f"Audio path: {audio_path}")

        if audio_path and Path(audio_path).exists():
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()

            return Response(
                content=audio_bytes,
                media_type="audio/mpeg",
                headers={"Content-Disposition": "attachment; filename=news-summary.mp3"}
            )
        else:
            raise HTTPException(status_code=500, detail="Audio file generation failed")
    
    except Exception as e:
        # Detailed error logging
        error_detail = f"{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        print("=" * 80)
        print("ERROR OCCURRED:")
        print(error_detail)
        print("=" * 80)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend:app",
        host="0.0.0.0",
        port=1234,
        reload=True
    )