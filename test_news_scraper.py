"""
Quick diagnostic test to identify the exact issue
"""
import asyncio
import sys

async def test_news_scraper():
    """Test if NewsScraper works correctly"""
    print("=" * 80)
    print("TESTING NEWS SCRAPER")
    print("=" * 80)
    
    try:
        from news_scraper import NewsEngine
        print("✓ NewsEngine imported successfully")
        
        scraper = NewsEngine()
        print(f"✓ NewsEngine instance created: {type(scraper)}")
        print(f"✓ scrape_news method exists: {hasattr(scraper, 'scrape_news')}")
        print(f"✓ scrape_news is callable: {callable(scraper.scrape_news)}")
        
        print("\nAttempting to scrape Bitcoin news...")
        result = await scraper.scrape_news(['Bitcoin'])
        print(f"✓ Scraping completed successfully!")
        print(f"Result structure: {type(result)}")
        print(f"Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
        
        if isinstance(result, dict) and 'news_analysis' in result:
            print(f"Topics in result: {result['news_analysis'].keys()}")
            print(f"\nSample output (first 200 chars):")
            for topic, content in result['news_analysis'].items():
                print(f"  {topic}: {str(content)[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_reddit_scraper():
    """Test if Reddit scraper works"""
    print("\n" + "=" * 80)
    print("TESTING REDDIT SCRAPER")
    print("=" * 80)
    
    try:
        from reddit_scraper import scrape_reddit_topics
        print("✓ scrape_reddit_topics imported successfully")
        
        print("\nAttempting to scrape Reddit for Technology...")
        result = await scrape_reddit_topics(['Technology'])
        print(f"✓ Scraping completed successfully!")
        print(f"Result structure: {type(result)}")
        print(f"Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
        
        if isinstance(result, dict) and 'reddit_analysis' in result:
            print(f"Topics in result: {result['reddit_analysis'].keys()}")
            print(f"\nSample output (first 200 chars):")
            for topic, content in result['reddit_analysis'].items():
                print(f"  {topic}: {str(content)[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_broadcast_generation():
    """Test broadcast news generation"""
    print("\n" + "=" * 80)
    print("TESTING BROADCAST NEWS GENERATION")
    print("=" * 80)
    
    try:
        import os
        from dotenv import load_dotenv
        from utils import generate_broadcast_news
        
        load_dotenv()
        
        # Mock data structure
        mock_news_data = {
            "news_analysis": {
                "Bitcoin": "Bitcoin surged to new highs today amid institutional adoption."
            }
        }
        
        mock_reddit_data = {
            "reddit_analysis": {
                "Bitcoin": "Reddit users are excited about the price movement."
            }
        }
        
        print("Testing with mock data...")
        result = generate_broadcast_news(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            news_data=mock_news_data,
            reddit_data=mock_reddit_data,
            topics=["Bitcoin"]
        )
        
        print(f"✓ Broadcast generation successful!")
        print(f"Output length: {len(result)} characters")
        print(f"Sample output: {result[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("COMPREHENSIVE DIAGNOSTIC TEST")
    print("=" * 80 + "\n")
    
    results = []
    
    # Test 1: News Scraper
    results.append(("News Scraper", await test_news_scraper()))
    
    # Test 2: Reddit Scraper (only if news scraper works)
    if results[0][1]:
        results.append(("Reddit Scraper", await test_reddit_scraper()))
    
    # Test 3: Broadcast Generation
    results.append(("Broadcast Generation", await test_broadcast_generation()))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} | {test_name}")
    
    total = len(results)
    passed = sum(1 for _, success in results if success)
    print(f"\nTotal: {total} | Passed: {passed} | Failed: {total - passed}")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())