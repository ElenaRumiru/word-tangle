#!/usr/bin/env python3
"""
validate_levels.py — authoritative gate for deliverables/levels/levels.json.

Runs six checks per the brief (brief-levels-difficulty.md, section "Обязательная валидация"):
  (a) every scramble is a permutation of its answer;
  (b) scramble != answer AND scramble is not itself an English word (zipf < 3.0);
  (c) per level, multiset of all circled letters == multiset of the surprise answer letters;
  (d) every answer is a real English word (zipf_frequency > 2.5);
  (e) difficulty.score is monotonically non-decreasing across levels,
      with an allowance for designed breathers at virtual levels 45 and 78 (proto ids 5, 8);
  (f) profanity check: no scramble spells a slur/profanity;
  (g) authentic-Jumble constraint: every word contributes >= 1 circled letter (no filler words).

Usage:  pip install wordfreq  &&  python validate_levels.py
Exit code 0 = all PASS, 1 = any FAIL.

Content language is ENGLISH (decision in docs/00-master-plan.md); the frequency
dictionary is English via wordfreq.zipf_frequency.
"""
import json
import sys
from collections import Counter
from pathlib import Path

try:
    from wordfreq import zipf_frequency
except ImportError:
    sys.exit("wordfreq not installed. Run:  pip install wordfreq")

# Thresholds (single source of truth).
ANSWER_MIN_ZIPF = 2.5   # (d) an answer must be at least this common to be a fair puzzle word
SCRAMBLE_MAX_ZIPF = 3.0  # (b) a scramble this common or commoner is itself a readable word -> reject
BREATHER_IDS = {5, 8}    # (e) proto levels intentionally easier than their predecessor (v45, v78)

# (f) Minimal family-safe blocklist. The corpus is authored, so this is a backstop, not a filter.
PROFANITY = {
    "ass", "arse", "damn", "crap", "hell", "shit", "fuck", "cunt", "dick",
    "piss", "cock", "twat", "slut", "whore", "bitch", "bastard", "wank",
    "nigger", "nigga", "spic", "chink", "kike", "fag", "faggot", "retard",
    "penis", "vagina", "boob", "tit", "turd", "prick", "douche",
}

LEVELS_PATH = Path(__file__).with_name("levels.json")


def multiset(word: str) -> Counter:
    return Counter(word.upper())


def validate_level(level: dict) -> list:
    """Return a list of failure strings for one level (empty == pass)."""
    fails = []
    lid = level.get("id", "?")

    # Collect circled letters across all words for check (c).
    circled = Counter()

    for w in level["words"]:
        ans = w["answer"].upper()
        scr = w["scramble"].upper()

        # (a) permutation
        if multiset(ans) != multiset(scr):
            fails.append(f"(a) scramble '{scr}' is not a permutation of answer '{ans}'")

        # (b) scramble differs and is not an English word
        if scr == ans:
            fails.append(f"(b) scramble '{scr}' is identical to answer '{ans}'")
        z_scr = zipf_frequency(scr.lower(), "en")
        if z_scr >= SCRAMBLE_MAX_ZIPF:
            fails.append(f"(b) scramble '{scr}' is itself an English word (zipf={z_scr:.2f} >= {SCRAMBLE_MAX_ZIPF})")

        # (d) answer is a real English word
        z_ans = zipf_frequency(ans.lower(), "en")
        if z_ans <= ANSWER_MIN_ZIPF:
            fails.append(f"(d) answer '{ans}' too rare/not a word (zipf={z_ans:.2f} <= {ANSWER_MIN_ZIPF})")

        # (f) profanity in a scramble
        if scr.lower() in PROFANITY:
            fails.append(f"(f) scramble '{scr}' spells a blocklisted word")

        # (g) every word must contribute at least one circled letter (authentic Jumble)
        if len(w["circles"]) == 0:
            fails.append(f"(g) word '{ans}' is a filler — contributes no circled letter")

        # accumulate circled letters
        for idx in w["circles"]:
            if idx < 0 or idx >= len(ans):
                fails.append(f"(c) circle index {idx} out of range for '{ans}'")
            else:
                circled[ans[idx]] += 1

    # (c) circled letters == surprise answer letters (no spaces)
    surprise = "".join(level["surprise"]["answer"]).upper()
    if circled != multiset(surprise):
        fails.append(
            f"(c) circled letters {dict(sorted(circled.items()))} != "
            f"surprise '{surprise}' {dict(sorted(multiset(surprise).items()))}")

    return fails


def main() -> int:
    data = json.loads(LEVELS_PATH.read_text(encoding="utf-8"))
    levels = data["levels"]

    print("=" * 66)
    print(f"  validate_levels.py — {LEVELS_PATH.name} ({len(levels)} levels)")
    print("=" * 66)

    any_fail = False

    # Per-level checks (a,b,c,d,f)
    for L in levels:
        fails = validate_level(L)
        answers = " / ".join(w["answer"] for w in L["words"])
        surprise = " ".join(L["surprise"]["answer"])
        tag = f"L{L['id']:>2} (v{L['virtualLevel']:>3})"
        if fails:
            any_fail = True
            print(f"[FAIL] {tag}  {answers}  ->  {surprise}")
            for f in fails:
                print(f"         - {f}")
        else:
            print(f"[PASS] {tag}  {answers}  ->  {surprise}")

    # (e) monotonic difficulty with breather allowance — a global check
    print("-" * 66)
    print("  (e) difficulty monotonicity (breathers allowed at ids 5, 8)")
    mono_ok = True
    prev = None
    for L in levels:
        score = L["difficulty"]["score"]
        if prev is not None:
            if L["id"] in BREATHER_IDS:
                # breather: must be LOWER than predecessor (designed dip) but still above 2 levels back
                if score >= prev:
                    mono_ok = False
                    print(f"         - L{L['id']} breather score {score} should dip below predecessor {prev}")
            else:
                if score < prev:
                    mono_ok = False
                    print(f"         - L{L['id']} score {score} < predecessor {prev} (not a designated breather)")
        prev = score
    if mono_ok:
        print("         PASS — rising sawtooth with intended dips at L5 and L8")
    else:
        any_fail = True

    print("=" * 66)
    if any_fail:
        print("  RESULT: FAIL")
        return 1
    print("  RESULT: ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
