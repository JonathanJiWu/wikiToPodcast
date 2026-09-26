import os

import pytest

import wikiToPodcast


class FakeResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception('HTTP error')


class FakeEngine:
    def __init__(self):
        self.saved = None
        self.file = None

    def save_to_file(self, text, filename):
        self.saved = text
        self.file = filename
        with open(filename, 'w', encoding='utf-8') as handle:
            handle.write(text)

    def runAndWait(self):
        return None

    def stop(self):
        return None


def test_get_wiki_content_extracts_paragraphs(monkeypatch):
    html = '''
    <div id="mw-content-text">
        <p>Alpha beta.</p>
        <p>Gamma delta.</p>
    </div>
    '''

    monkeypatch.setattr(wikiToPodcast.requests, 'get', lambda url, timeout=None: FakeResponse(html))

    assert wikiToPodcast.get_wiki_content('https://example.com') == 'Alpha beta.\nGamma delta.'


def test_get_wiki_content_handles_request_failure(monkeypatch):
    def raise_request_error(*args, **kwargs):
        raise wikiToPodcast.requests.RequestException('boom')

    monkeypatch.setattr(wikiToPodcast.requests, 'get', raise_request_error)

    assert wikiToPodcast.get_wiki_content('https://example.com') == ''


def test_distill_content_rejects_invalid_max_length():
    assert wikiToPodcast.distill_content('abc', max_length=0) == ''
    assert wikiToPodcast.distill_content('', max_length=100) == ''


def test_convert_to_audio_raises_on_empty_text(monkeypatch, tmp_path):
    output = tmp_path / 'voice.mp3'
    monkeypatch.setattr(wikiToPodcast.pyttsx3, 'init', lambda: FakeEngine())

    with pytest.raises(ValueError, match='Text must not be empty'):
        wikiToPodcast.convert_to_audio('', filename=str(output))


def test_convert_to_audio_saves_file(monkeypatch, tmp_path):
    output = tmp_path / 'voice.mp3'
    engine = FakeEngine()
    monkeypatch.setattr(wikiToPodcast.pyttsx3, 'init', lambda: engine)

    wikiToPodcast.convert_to_audio('hello world', filename=str(output))

    assert output.exists()
    assert engine.saved == 'hello world'
    assert engine.file == str(output)
