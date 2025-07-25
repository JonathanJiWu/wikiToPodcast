# 1. taka a wiki url
# 2. disdtill the content
# 3. convert to audio

import requests
from bs4 import BeautifulSoup
import pyttsx3
import argparse

def get_wiki_content(url):
    """Fetch and return the main text content from a Wikipedia page."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('div', {'id': 'mw-content-text'})
    if not content:
        return ""
    paragraphs = content.find_all('p')
    text = '\n'.join([p.get_text() for p in paragraphs if p.get_text(strip=True)])
    return text

def distill_content(text, max_length=1000):
    """Distill the content to a summary (simple truncation for demo)."""
    # For demo, just truncate. For real use, apply NLP summarization.
    return text[:max_length]

def convert_to_audio(text, filename='output.mp3'):
    """Convert text to audio and save as an MP3 file."""
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()

def main():
    parser = argparse.ArgumentParser(description="Convert Wikipedia article to podcast audio.")
    parser.add_argument('url', help='Wikipedia article URL')
    parser.add_argument('--output', default='output.mp3', help='Output MP3 filename')
    parser.add_argument('--max_length', type=int, default=1000, help='Max length of distilled content')
    args = parser.parse_args()

    print(f"Fetching content from: {args.url}")
    wiki_text = get_wiki_content(args.url)
    if not wiki_text:
        print("Could not fetch content from the provided URL.")
        return
    print("Distilling content...")
    distilled = distill_content(wiki_text, max_length=args.max_length)
    print(f"Converting to audio: {args.output}")
    convert_to_audio(distilled, filename=args.output)
    print(f"Done! Audio saved to {args.output}")

if __name__ == "__main__":
    print("runing wikiToPodcast.py")
    main()