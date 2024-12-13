import requests
from bs4 import BeautifulSoup
import urllib.parse

class GoogleScraper:
    
    def __init__(self, user_agent=None):
        self.base_url = "https://www.google.com/search"
        self.headers = {
            "User-Agent": user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def search(self, query, num_results=10):
        # Validate input
        if not query:
            raise ValueError("Search query cannot be empty")
        
        # Prepare search parameters
        params = {
            "q": query,
            "num": min(num_results, 100)  # Google limits to 100 results per page
        }
        
        try:
            # Send GET request to Google
            response = requests.get(
                self.base_url, 
                params=params, 
                headers=self.headers
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract search results
            results = []
            for result in soup.find_all('div', class_='yuRUbf'):
                title_elem = result.find('h3')
                link_elem = result.find('a')
                
                if title_elem and link_elem:
                    results.append({
                        'title': title_elem.get_text(),
                        'link': link_elem['href']
                    })
                
                # Stop if we've reached desired number of results
                if len(results) >= num_results:
                    break
            
            return results
        
        except requests.RequestException as e:
            print(f"Error occurred during search: {e}")
            return []
    
# Example usage
def main():
    scraper = GoogleScraper()
    
    try:
        results = scraper.search("Python programming", num_results=5)
        
        # Print results
        for result in results:
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}\n")
        
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
