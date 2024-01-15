import requests
from bs4 import BeautifulSoup

def is_link_indexed(url):
    # Google search URL
    search_url = "https://www.google.com/search"
    
    # Parameters for the search query
    params = {"q": f"site:{url}"}
    
    # Perform the Google search
    response = requests.get(search_url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check if the link is in the search results
    search_results = soup.find_all('div', class_='g')
    for result in search_results:
        link = result.find('a')['href']
        if url in link:
            return True
    
    return False

# Example URL
url = "https://serpapi.com/search-api"
print(is_link_indexed(url))

