"""Chinese text normalization and pinyin pronunciation scoring."""
import re
from collections import Counter

from pypinyin import Style, lazy_pinyin


def normalize_chinese(text: str) -> str:
    """Strip whitespace and punctuation for comparison."""
    return re.sub(r"[\s\W_，。!?,.!?]", "", text or "")


def pinyin_syllables(text: str) -> list[str]:
    """Tone-numbered pinyin syllables, e.g. '你好' -> ['ni3', 'hao3']."""
    return [s.lower() for s in lazy_pinyin(text, style=Style.TONE3)]


def _strip_tone(syllable: str) -> str:
    """Drop the trailing tone digit from a TONE3 syllable ('hao3' -> 'hao')."""
    return syllable.rstrip("012345")


def pinyin_display(text: str) -> str:
    """Space-separated pinyin with tone marks, for showing back to the learner."""
    return " ".join(lazy_pinyin(text, style=Style.TONE))


def score_pronunciation(target: str, spoken: str) -> dict:
    """Score spoken pinyin against the target at the syllable level.

    Full credit for a syllable whose sound *and* tone match the target; half
    credit when the syllable (sound) is right but the tone is wrong. This is
    order-independent (a bag/multiset match) so a single dropped or swapped
    syllable doesn't cascade into everything after it counting as wrong.
    """
    target_syls = pinyin_syllables(target)
    spoken_syls = pinyin_syllables(spoken)
    total = len(target_syls)
    if total == 0:
        return {"score": 0, "correct": False, "syllables_right": 0,
                "tones_wrong": 0, "total": 0}

    pool = Counter(spoken_syls)

    # Pass 1: exact syllable + tone match.
    full = 0
    unmatched: list[str] = []
    for syl in target_syls:
        if pool.get(syl, 0) > 0:
            pool[syl] -= 1
            full += 1
        else:
            unmatched.append(syl)

    # Pass 2: same base sound but wrong tone -> partial credit.
    base_pool: Counter = Counter()
    for syl, cnt in pool.items():
        if cnt > 0:
            base_pool[_strip_tone(syl)] += cnt
    tone_wrong = 0
    for syl in unmatched:
        base = _strip_tone(syl)
        if base_pool.get(base, 0) > 0:
            base_pool[base] -= 1
            tone_wrong += 1

    credit = full + 0.5 * tone_wrong
    score = round(credit / total * 100)
    # "Correct" is strict: every target syllable matched in sound AND tone, and
    # the learner said no extra syllables (the length check rejects insertions).
    correct = full == total and len(spoken_syls) == total
    return {
        "score": score,
        "correct": correct,
        "syllables_right": full + tone_wrong,
        "tones_wrong": tone_wrong,
        "total": total,
    }


def pronunciation_feedback(p: dict) -> str:
    """Human feedback string for a score_pronunciation result."""
    if p["correct"]:
        return "Perfect pronunciation! 完美!"
    if p["total"] and p["syllables_right"] == p["total"] and p["tones_wrong"] > 0:
        return "All the syllables right, but check your tones"
    if p["tones_wrong"] > 0:
        return "Some sounds are right, but watch your tones."
    if p["score"] >= 80:
        return "Great pronunciation! Almost there."
    if p["score"] >= 50:
        return "Good attempt. Some syllables were off."
    return "Try again. Listen and speak more clearly."
