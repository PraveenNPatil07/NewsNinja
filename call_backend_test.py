import requests
import json
import time
from pathlib import Path
from typing import Dict, Any

BASE_URL = "http://localhost:1234"
TIMEOUT = 120

class BackendTester:
    def __init__(self):
        self.results = []
        
    def print_result(self, test_name: str, success: bool, message: str, response_data: Any = None):
        """Print formatted test results"""
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"\n{status} | {test_name}")
        print(f"   Message: {message}")
        if response_data:
            print(f"   Response: {response_data}")
        print("-" * 80)
        
        self.results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
    
    def test_server_health(self):
        """Test if the server is running"""
        test_name = "Server Health Check"
        try:
            response = requests.get(f"{BASE_URL}/docs", timeout=5)
            if response.status_code == 200:
                self.print_result(test_name, True, "Server is running")
                return True
            else:
                self.print_result(test_name, False, f"Server returned status {response.status_code}")
                return False
        except Exception as e:
            self.print_result(test_name, False, f"Cannot connect to server: {str(e)}")
            return False
    
    def test_news_only(self):
        """Test with news source only"""
        test_name = "News Source Only"
        url = f"{BASE_URL}/generate-news-audio"
        data = {
            "topics": ["Bitcoin"],
            "source_type": "news"
        }
        
        try:
            print(f"\nTesting: {test_name}...")
            print(f"Request: {json.dumps(data, indent=2)}")
            
            start_time = time.time()
            response = requests.post(url, json=data, timeout=TIMEOUT)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                # Check if response is audio
                content_type = response.headers.get('Content-Type', '')
                if 'audio' in content_type:
                    audio_size = len(response.content)
                    self.print_result(
                        test_name, 
                        True, 
                        f"Audio generated successfully ({audio_size} bytes) in {elapsed:.2f}s"
                    )
                    
                    # Save audio file
                    output_path = Path("test_output_news.mp3")
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    print(f"   Audio saved to: {output_path}")
                    return True
                else:
                    self.print_result(test_name, False, f"Unexpected content type: {content_type}")
                    return False
            else:
                self.print_result(
                    test_name, 
                    False, 
                    f"Status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.print_result(test_name, False, f"Request failed: {str(e)}")
            return False
    
    def test_reddit_only(self):
        """Test with reddit source only"""
        test_name = "Reddit Source Only"
        url = f"{BASE_URL}/generate-news-audio"
        data = {
            "topics": ["Technology"],
            "source_type": "reddit"
        }
        
        try:
            print(f"\nTesting: {test_name}...")
            print(f"Request: {json.dumps(data, indent=2)}")
            
            start_time = time.time()
            response = requests.post(url, json=data, timeout=TIMEOUT)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'audio' in content_type:
                    audio_size = len(response.content)
                    self.print_result(
                        test_name, 
                        True, 
                        f"Audio generated successfully ({audio_size} bytes) in {elapsed:.2f}s"
                    )
                    
                    output_path = Path("test_output_reddit.mp3")
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    print(f"   Audio saved to: {output_path}")
                    return True
                else:
                    self.print_result(test_name, False, f"Unexpected content type: {content_type}")
                    return False
            else:
                self.print_result(
                    test_name, 
                    False, 
                    f"Status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.print_result(test_name, False, f"Request failed: {str(e)}")
            return False
    
    def test_both_sources(self):
        """Test with both news and reddit sources"""
        test_name = "Both Sources (News + Reddit)"
        url = f"{BASE_URL}/generate-news-audio"
        data = {
            "topics": ["Artificial Intelligence"],
            "source_type": "both"
        }
        
        try:
            print(f"\nTesting: {test_name}...")
            print(f"Request: {json.dumps(data, indent=2)}")
            
            start_time = time.time()
            response = requests.post(url, json=data, timeout=TIMEOUT)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'audio' in content_type:
                    audio_size = len(response.content)
                    self.print_result(
                        test_name, 
                        True, 
                        f"Audio generated successfully ({audio_size} bytes) in {elapsed:.2f}s"
                    )
                    
                    output_path = Path("test_output_both.mp3")
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    print(f"   Audio saved to: {output_path}")
                    return True
                else:
                    self.print_result(test_name, False, f"Unexpected content type: {content_type}")
                    return False
            else:
                self.print_result(
                    test_name, 
                    False, 
                    f"Status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.print_result(test_name, False, f"Request failed: {str(e)}")
            return False
    
    def test_multiple_topics(self):
        """Test with multiple topics"""
        test_name = "Multiple Topics"
        url = f"{BASE_URL}/generate-news-audio"
        data = {
            "topics": ["Bitcoin", "AI", "Climate Change"],
            "source_type": "news"
        }
        
        try:
            print(f"\nTesting: {test_name}...")
            print(f"Request: {json.dumps(data, indent=2)}")
            
            start_time = time.time()
            response = requests.post(url, json=data, timeout=TIMEOUT)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'audio' in content_type:
                    audio_size = len(response.content)
                    self.print_result(
                        test_name, 
                        True, 
                        f"Audio generated successfully ({audio_size} bytes) in {elapsed:.2f}s"
                    )
                    
                    output_path = Path("test_output_multiple.mp3")
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    print(f"   Audio saved to: {output_path}")
                    return True
                else:
                    self.print_result(test_name, False, f"Unexpected content type: {content_type}")
                    return False
            else:
                self.print_result(
                    test_name, 
                    False, 
                    f"Status {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.print_result(test_name, False, f"Request failed: {str(e)}")
            return False
    
    def test_invalid_source_type(self):
        """Test with invalid source type"""
        test_name = "Invalid Source Type"
        url = f"{BASE_URL}/generate-news-audio"
        data = {
            "topics": ["Test"],
            "source_type": "invalid"
        }
        
        try:
            print(f"\nTesting: {test_name}...")
            print(f"Request: {json.dumps(data, indent=2)}")
            
            response = requests.post(url, json=data, timeout=TIMEOUT)
            
            # We expect this to fail with 422 (validation error) or handle gracefully
            if response.status_code in [422, 400]:
                self.print_result(
                    test_name, 
                    True, 
                    f"Correctly rejected invalid input with status {response.status_code}"
                )
                return True
            elif response.status_code == 200:
                self.print_result(
                    test_name, 
                    False, 
                    "Should have rejected invalid source_type but returned 200"
                )
                return False
            else:
                self.print_result(
                    test_name, 
                    True, 
                    f"Rejected with status {response.status_code}: {response.text[:100]}"
                )
                return True
                
        except Exception as e:
            self.print_result(test_name, False, f"Request failed: {str(e)}")
            return False
    
    def test_empty_topics(self):
        """Test with empty topics list"""
        test_name = "Empty Topics List"
        url = f"{BASE_URL}/generate-news-audio"
        data = {
            "topics": [],
            "source_type": "news"
        }
        
        try:
            print(f"\nTesting: {test_name}...")
            print(f"Request: {json.dumps(data, indent=2)}")
            
            response = requests.post(url, json=data, timeout=TIMEOUT)
            
            # Should either reject or handle gracefully
            if response.status_code in [422, 400, 500]:
                self.print_result(
                    test_name, 
                    True, 
                    f"Handled empty topics with status {response.status_code}"
                )
                return True
            else:
                self.print_result(
                    test_name, 
                    False, 
                    f"Unexpected handling of empty topics: {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.print_result(test_name, True, f"Appropriately failed: {str(e)}")
            return True
    
    def run_all_tests(self):
        """Run all tests and print summary"""
        print("=" * 80)
        print("BACKEND FUNCTIONALITY TEST SUITE")
        print("=" * 80)
        
        # Test 1: Server health
        if not self.test_server_health():
            print("\n⚠ Server is not running. Please start the backend first.")
            return
        
        # Test 2-6: Functional tests
        self.test_news_only()
        time.sleep(2)  # Brief pause between tests
        
        self.test_reddit_only()
        time.sleep(2)
        
        self.test_both_sources()
        time.sleep(2)
        
        self.test_multiple_topics()
        time.sleep(2)
        
        # Test 7-8: Error handling tests
        self.test_invalid_source_type()
        time.sleep(1)
        
        self.test_empty_topics()
        
        # Print summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r["success"])
        failed = total - passed
        
        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed} ✓")
        print(f"Failed: {failed} ✗")
        print(f"Success Rate: {(passed/total)*100:.1f}%\n")
        
        if failed > 0:
            print("Failed Tests:")
            for r in self.results:
                if not r["success"]:
                    print(f"  - {r['test']}: {r['message']}")
        
        print("=" * 80)


if __name__ == "__main__":
    tester = BackendTester()
    tester.run_all_tests()