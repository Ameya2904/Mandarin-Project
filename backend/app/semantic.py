"""English semantic matching via WordNet (used for free-text answer checking)."""
import re

import nltk

# Ensure the WordNet corpus is available for synonym checking.
try:
    from nltk.corpus import wordnet as wn
    wn.synsets("call")  # probe to trigger LookupError if data missing
except LookupError:
    nltk.download("wordnet", quiet=True)
    nltk.download("omw-1.4", quiet=True)
    from nltk.corpus import wordnet as wn


def normalize_en(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[.;]+$", "", s)
    s = re.sub(r"^(to |a |an |the )", "", s)
    return s.strip()


def _word_synonyms(word: str) -> set:
    synonyms = set()
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name().lower().replace("_", " "))
    return synonyms


def words_match(w1: str, w2: str) -> bool:
    if w1 == w2:
        return True
    syns1 = _word_synonyms(w1)
    syns2 = _word_synonyms(w2)
    return w2 in syns1 or w1 in syns2


def answer_matches_target(answer: str, target: str) -> bool:
    """True if `answer` matches any of the `;`/`,`/`/`/`or`-separated target parts."""
    answer_clean = normalize_en(answer)
    parts = re.split(r"[;,/]|\bor\b", target)
    target_parts = [normalize_en(p) for p in parts if p.strip()]
    return any(words_match(answer_clean, part) for part in target_parts)
