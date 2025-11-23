import re
from dataclasses import dataclass
from typing import Dict, Any

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from spellchecker import SpellChecker   # ✅ REPLACEMENT (No Java Needed)

# ---------- GLOBAL TOOLS ----------

sentiment_analyzer = SentimentIntensityAnalyzer()
spell = SpellChecker()   # ✅ simple grammar/spelling checker

FILLER_WORDS = {
    "um", "uh", "like", "you know", "so", "actually", "basically",
    "right", "i mean", "well", "kinda", "sort of", "okay", "hmm", "ah"
}

# greeting, content, closing keywords for Content & Structure
GREETINGS = ["hello everyone", "hello", "hi", "good morning", "good afternoon", "good evening"]
NAME_PATTERNS = ["my name is", "myself", "i am"]
AGE_PATTERNS = ["years old"]
SCHOOL_PATTERNS = ["school", "class", "grade"]
FAMILY_PATTERNS = ["family", "father", "mother", "parents", "sister", "brother"]
HOBBY_PATTERNS = ["hobby", "hobbies", "enjoy", "i like", "i love", "in my free time"]
GOAL_PATTERNS = ["goal", "dream", "ambition", "i want to be"]
UNIQUE_PATTERNS = ["special", "unique", "fun fact", "one thing about me"]
CLOSING_PATTERNS = ["thank you", "thanks for listening", "thank you for listening"]


@dataclass
class Preprocessed:
    text: str
    lowered: str
    tokens: list
    word_count: int
    sentences: list
    sentence_count: int


def preprocess(text: str) -> Preprocessed:
    clean = text.strip()
    lowered = clean.lower()
    tokens = re.findall(r"\w+", lowered)
    sentences = re.split(r"[.!?]+", clean)
    sentences = [s.strip() for s in sentences if s.strip()]
    return Preprocessed(
        text=clean,
        lowered=lowered,
        tokens=tokens,
        word_count=len(tokens),
        sentences=sentences,
        sentence_count=len(sentences),
    )


# ---------- CONTENT & STRUCTURE (40%) ----------

def has_any_pattern(lowered: str, patterns) -> bool:
    return any(p in lowered for p in patterns)


def content_structure_score(pp: Preprocessed) -> float:
    score_parts = []

    # 1. Salutation
    score_parts.append(1.0 if has_any_pattern(pp.lowered, GREETINGS) else 0.0)

    # 2. Required info blocks
    blocks = [
        NAME_PATTERNS, AGE_PATTERNS, SCHOOL_PATTERNS, FAMILY_PATTERNS,
        HOBBY_PATTERNS, GOAL_PATTERNS, UNIQUE_PATTERNS
    ]
    hits = sum(1 for b in blocks if has_any_pattern(pp.lowered, b))
    score_parts.append(hits / len(blocks))

    # 3. Flow: greeting -> name -> closing
    def first_pos(patterns):
        idx = [pp.lowered.find(p) for p in patterns if pp.lowered.find(p) != -1]
        return min(idx) if idx else -1

    g = first_pos(GREETINGS)
    n = first_pos(NAME_PATTERNS)
    c = first_pos(CLOSING_PATTERNS)

    if g != -1 and n != -1 and c != -1:
        flow_score = 1.0 if g < n < c else 0.3
    else:
        flow_score = 0.5

    score_parts.append(flow_score)

    return sum(score_parts) / len(score_parts)


# ---------- SPEECH RATE (10%) ----------

def speech_rate_score(pp: Preprocessed, duration_seconds: float | None = None) -> Dict[str, Any]:
    if not duration_seconds or duration_seconds <= 0:
        return {"score": 0.7, "wpm": None}

    wpm = (pp.word_count * 60) / duration_seconds

    if 111 <= wpm <= 140:
        s = 1.0
    elif (81 <= wpm < 111) or (140 < wpm <= 160):
        s = 0.8
    elif (61 <= wpm < 81) or (160 < wpm <= 180):
        s = 0.6
    else:
        s = 0.4

    return {"score": s, "wpm": round(wpm, 2)}


# ---------- LANGUAGE & GRAMMAR (20%) - SpellCheck version ----------

def grammar_score(pp: Preprocessed) -> Dict[str, Any]:
    tokens = pp.tokens
    misspelled = spell.unknown(tokens)
    error_count = len(misspelled)

    if pp.word_count == 0:
        return {"score": 0.0, "errors": None}

    errors_per_100 = (error_count / pp.word_count) * 100

    if errors_per_100 <= 1:
        s = 1.0
    elif errors_per_100 <= 3:
        s = 0.8
    elif errors_per_100 <= 5:
        s = 0.6
    elif errors_per_100 <= 10:
        s = 0.4
    else:
        s = 0.2

    return {
        "score": s,
        "errors": list(misspelled),
        "errors_per_100": round(errors_per_100, 2)
    }


# ---------- CLARITY – FILLER WORD RATE (15%) ----------

def filler_word_score(pp: Preprocessed) -> Dict[str, Any]:
    if pp.word_count == 0:
        return {"score": 0.0, "filler_rate": None, "filler_count": 0}

    text = pp.lowered
    filler_count = sum(text.count(w) for w in FILLER_WORDS)
    rate = (filler_count / pp.word_count) * 100

    if rate <= 1:
        s = 1.0
    elif rate <= 3:
        s = 0.8
    elif rate <= 5:
        s = 0.6
    elif rate <= 8:
        s = 0.4
    else:
        s = 0.2

    return {"score": s, "filler_rate": round(rate, 2), "filler_count": filler_count}


# ---------- ENGAGEMENT – SENTIMENT (15%) ----------

def engagement_score(pp: Preprocessed) -> Dict[str, Any]:
    scores = sentiment_analyzer.polarity_scores(pp.text)
    compound = scores["compound"]

    if compound >= 0.9:
        s = 1.0
    elif compound >= 0.7:
        s = 0.8
    elif compound >= 0.5:
        s = 0.6
    elif compound >= 0.3:
        s = 0.4
    else:
        s = 0.2

    return {"score": s, "compound": compound}
