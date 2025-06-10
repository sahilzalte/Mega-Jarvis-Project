import webbrowser
from main import speak  # Import speak function from main.py

def google_search(query):
    """Searches Google for the given query."""
    query = query.lower().strip()
    
    if query:
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        speak(f"Searching Google for {query}")
    else:
        speak("Please specify what you want to search for.")
