# 1. take a wiki URL
# 2. distill the content
# 3. convert to audio

import argparse
import os

import pyttsx3
import requests
from bs4 import BeautifulSoup


def get_wiki_content(url):
    """Fetch and return the main text content from a Wikipedia page."""
    if not url:
        return ""

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return ""

    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('div', {'id': 'mw-content-text'})
    if not content:
        return ""

    paragraphs = []
    for paragraph in content.find_all('p'):
        text = paragraph.get_text(' ', strip=True)
        if text:
            paragraphs.append(' '.join(text.split()))
    return '\n'.join(paragraphs)


def distill_content(text, max_length=1000):
    """Distill the content to a summary (simple truncation for demo)."""
    if not text:
        return ""
    if max_length is None or max_length <= 0:
        return ""
    return text[:max_length]


def convert_to_audio(text, filename='output.mp3'):
    """Convert text to audio and save as an MP3 file."""
    if not text or not text.strip():
        raise ValueError('Text must not be empty.')

    output_dir = os.path.dirname(filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    engine = pyttsx3.init()
    try:
        engine.save_to_file(text, filename)
        engine.runAndWait()
    finally:
        engine.stop()


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
    try:
        convert_to_audio(distilled, filename=args.output)
    except ValueError as exc:
        print(f"Audio generation failed: {exc}")
        return
    print(f"Done! Audio saved to {args.output}")


if __name__ == "__main__":
    print("running wikiToPodcast.py")
    main()