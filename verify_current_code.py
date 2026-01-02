"""
Verify what's actually being imported in your code
"""
import sys
import os

print("=" * 80)
print("VERIFYING CURRENT IMPORTS")
print("=" * 80)

print("\n1. Checking news_scraper.py file...")
try:
    with open("news_scraper.py", "r") as f:
        content = f.read()
        if "class NewsScraper" in content:
            print("❌ FOUND: class NewsScraper (OLD)")
        if "class NewsEngine" in content:
            print("✓ FOUND: class NewsEngine (NEW)")
except Exception as e:
    print(f"Error reading file: {e}")

print("\n2. Checking backend.py imports...")
try:
    with open("backend.py", "r") as f:
        content = f.read()
        if "from news_scraper import NewsScraper" in content:
            print("❌ FOUND: from news_scraper import NewsScraper (OLD)")
        if "from news_scraper import NewsEngine" in content:
            print("✓ FOUND: from news_scraper import NewsEngine (NEW)")
        if "NewsScraper()" in content:
            print("❌ FOUND: NewsScraper() instantiation (OLD)")
        if "NewsEngine()" in content:
            print("✓ FOUND: NewsEngine() instantiation (NEW)")
except Exception as e:
    print(f"Error reading file: {e}")

print("\n3. Attempting to import news_scraper module...")
try:
    # Clear any cached imports
    if 'news_scraper' in sys.modules:
        print("⚠ Module was already cached, removing...")
        del sys.modules['news_scraper']
    
    import news_scraper
    
    # Check what's actually in the module
    print(f"✓ Module imported: {news_scraper.__file__}")
    print(f"  Available classes/functions:")
    for name in dir(news_scraper):
        if not name.startswith('_'):
            obj = getattr(news_scraper, name)
            print(f"    - {name}: {type(obj)}")
    
    # Try to access NewsEngine
    if hasattr(news_scraper, 'NewsEngine'):
        print("\n✓ NewsEngine class exists")
        engine = news_scraper.NewsEngine()
        print(f"  Instance created: {type(engine)}")
        print(f"  Has scrape_news: {hasattr(engine, 'scrape_news')}")
    else:
        print("\n❌ NewsEngine class NOT FOUND")
    
    # Check for old class
    if hasattr(news_scraper, 'NewsScraper'):
        print("\n⚠ WARNING: NewsScraper class still exists (OLD CODE)")
    
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("RECOMMENDATION")
print("=" * 80)
print("""
If you see 'NewsScraper' anywhere above:
1. Kill the backend server (Ctrl+C)
2. Delete any __pycache__ directories:
   - del /S /Q __pycache__  (Windows)
   - rm -rf __pycache__     (Mac/Linux)
3. Restart the backend server
""")