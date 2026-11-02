"""Extractive summarization with no dependencies and no API calls.

The approach is deliberately simple: score each sentence by the
frequency of its content words across the whole text, then keep the
highest-scoring sentences in their original order. That is enough to
trim a news article blurb down to its core points, and it runs
anywhere Python runs.
"""

import re

STOPWORDS = frozenset(
    """
    a an the and or but if while with of at by for to in on from as is are was
    were be been being have has had do does did will would can could should
    may might it its this that these those there here he she they we you i
    his her their our your my me him us them what which who whom when where
    why how all any both each few more most other some such no nor not only
    own same so than too very just also into over under again further then
    once about between through during before after above below up down out
    off per via
    """.split()
)

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"[a-z0-9]+")


def split_sentences(text):
    """Split text into sentences, dropping empty fragments."""
    return [s.strip() for s in _SENTENCE_SPLIT.split(text.strip()) if s.strip()]


def _content_words(sentence):
    return [w for w in _WORD.findall(sentence.lower()) if w not in STOPWORDS]


def summarize(text, max_sentences=3):
    """Return the most representative sentences of ``text``.

    Returns the original text when it is already short, and an empty
    string for empty input. Output sentences keep their original order.
    """
    if not text or not text.strip():
        return ""
    sentences = split_sentences(text)
    if len(sentences) <= max_sentences:
        return text.strip()
    frequencies = {}
    for sentence in sentences:
        for word in _content_words(sentence):
            frequencies[word] = frequencies.get(word, 0) + 1
    scored = []
    for index, sentence in enumerate(sentences):
        words = _content_words(sentence)
        if not words:
            continue
        # Normalize by length so long sentences do not win by word count.
        score = sum(frequencies[w] for w in words) / len(words)
        scored.append((score, index, sentence))
    scored.sort(key=lambda item: (-item[0], item[1]))
    chosen = sorted(scored[:max_sentences], key=lambda item: item[1])
    return " ".join(sentence for _, _, sentence in chosen)
