import asyncio
import os
from typing import Dict, List

from aiolimiter import AsyncLimiter
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

from utils import (
    generate_news_urls_to_scrape,
    scrape_with_brightdata,
    clean_html_to_text,
    extract_headlines,
    summarize_with_openrouter_news_script
)

load_dotenv()

class NewsEngine:
    def __init__(self):
        # Initialize rate limiter in __init__
        self._rate_limiter = AsyncLimiter(5, 1)  # 5 requests per second

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def scrape_news(self, topics: List[str]) -> Dict[str, str]:
        """Scrape and analyze news articles"""
        results = {}
        
        for topic in topics:
            async with self._rate_limiter:
                try:
                    print(f"DEBUG: Processing topic {topic}")
                    urls = generate_news_urls_to_scrape([topic])
                    
                    if not urls or topic not in urls:
                         print(f"DEBUG: No URL found for {topic}")
                         results[topic] = "Error: No URL found."
                         continue
                         
                    search_html = scrape_with_brightdata(urls[topic])
                    clean_text = clean_html_to_text(search_html)
                    headlines = extract_headlines(clean_text)
                    
                    if not headlines:
                        print(f"DEBUG: No headlines extracted for {topic}")
                        results[topic] = "No headlines found."
                        continue

                    print(f"DEBUG: Generating summary for {topic}")
                    summary = summarize_with_openrouter_news_script(
                        api_key=os.getenv("OPENROUTER_API_KEY"),
                        headlines=headlines
                    )
                    results[topic] = summary
                except Exception as e:
                    print(f"ERROR scraping {topic}: {str(e)}")
                    results[topic] = f"Error: {str(e)}"
                await asyncio.sleep(1)

        return {"news_analysis" : results}