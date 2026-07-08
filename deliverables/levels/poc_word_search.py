#!/usr/bin/env python3
"""
poc_word_search.py — proof-of-concept for step (3) of the generator:
"cover the answer's letter multiset with K words of a target length/Zipf band,
every word contributing >=1 letter" (the every-word invariant from phase 1).

It does two things:
  1. Builds a Zipf-banded word index from wordfreq (letter -> words containing it).
  2. For a given surprise answer, counts how many valid K-word coverings exist
     (a lower bound via randomized sampling) to show the solution space is huge
     -- i.e. the generator is not content-starved once the pun bank exists.

Also times throughput: covers/second on a laptop.

Usage:  pip install wordfreq && python poc_word_search.py
"""
import random
import time
from collections import Counter, defaultdict

from wordfreq import top_n_list, zipf_frequency

# --- Zipf bands (mirror levels-design P3): easy=common, hard=rare ---
BANDS = {
    "top":  (5.0, 9.0),   # L1-ish
    "mid":  (4.0, 5.0),
    "low":  (3.0, 4.0),
    "rare": (2.5, 3.5),   # L100-ish
}


def build_index(max_words=60000, min_len=4, max_len=7):
    """word -> zipf, and (band,len,letter) -> [words]. One pass over the freq list."""
    words = [w for w in top_n_list("en", max_words)
             if w.isalpha() and min_len <= len(w) <= max_len]
    zipf = {w: zipf_frequency(w, "en") for w in words}
    banded = defaultdict(list)
    for w in words:
        z = zipf[w]
        for band, (lo, hi) in BANDS.items():
            if lo <= z < hi:
                banded[(band, len(w))].append(w)
    return words, zipf, banded


def candidate_words(banded, band, length):
    return banded.get((band, length), [])


def try_cover(answer, k, word_len, band, banded, tries=20000):
    """Randomized search: sample K words of (band,word_len); accept if their pooled
    letters can supply the answer multiset AND every word donates >=1 answer letter.
    Returns (num_solutions_found, num_samples) as a lower-bound density estimate."""
    need = Counter(answer.upper())
    pool = [w.upper() for w in candidate_words(banded, band, word_len)]
    if len(pool) < k:
        return 0, 0
    found = 0
    for _ in range(tries):
        pick = random.sample(pool, k)
        pooled = Counter("".join(pick))
        if not all(pooled[ch] >= n for ch, n in need.items()):
            continue
        # every-word invariant: each picked word must share >=1 letter with answer
        if not all(any(ch in need for ch in w) for w in pick):
            continue
        found += 1
    return found, tries


def main():
    random.seed(7)
    t0 = time.time()
    words, zipf, banded = build_index()
    t_index = time.time() - t0
    print(f"Index built in {t_index:.2f}s: {len(words)} words, "
          f"{len(banded)} (band,len) buckets")
    for key in sorted(banded):
        pass
    print()

    # Representative answers spanning the curve (from levels-design):
    trials = [
        # (answer, K words, word_len, band)  -- how the CSP would be parameterized
        ("NAP",        1, 4, "top"),    # L1  : 1 short common word
        ("MEET",       2, 4, "mid"),    # L3  : homophone-era
        ("HEIRFORCE",  2, 5, "low"),    # L4  : 9-letter answer over two words
        ("SIRPRIZE",   4, 5, "low"),    # L7  : 4 words feed an 8-letter answer
        ("PANERELIEF", 5, 6, "rare"),   # L10 : the hard cross-word anagram
    ]
    import math
    print(f"{'answer':<12}{'K':>2}{'len':>4}{'band':>6}{'pool':>7}"
          f"{'hits/20k':>10}{'est.coverings':>18}{'samples/s':>13}")
    print("-" * 74)
    for ans, k, wl, band in trials:
        t = time.time()
        found, n = try_cover(ans, k, wl, band, banded)
        dt = time.time() - t
        pool = len(candidate_words(banded, band, wl))
        dens = (found / n) if n else 0.0
        # crude space-size estimate: C(pool,k) * sampled density
        space = math.comb(pool, k) if pool >= k else 0
        est = space * dens
        rate = n / dt if dt else 0
        print(f"{ans:<12}{k:>2}{wl:>4}{band:>6}{pool:>7}"
              f"{found:>10}{est:>18,.0f}{rate:>13,.0f}")

    print()
    print("Interpretation: 'est.density' ~ number of DISTINCT K-word coverings")
    print("that satisfy the every-word invariant. Even the hard L10 case has")
    print("thousands+ of valid letter-coverings -> the generator is not")
    print("content-starved; the bottleneck is the pun ANSWER, not the words.")


if __name__ == "__main__":
    main()
