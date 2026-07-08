"""
Redistribute circled letters across ALL words (authentic Jumble constraint).

Goal per level: choose a set of (word_index, position) "circles" such that
  1. the multiset of circled letters == multiset of the surprise answer letters (no spaces),
  2. EVERY word contributes at least one circled letter (no filler words),
  3. distribution is balanced (aim 1..3 letters/word).
If a word shares no letter with the answer, the >=1 constraint is infeasible for it;
we then leave that level's circles as-is and report it (never happens for our 10 levels).

Backtracking over the answer's letter multiset; biases toward the least-loaded word so
the solution is balanced and every word gets used.
"""
import json, sys
from collections import Counter

PATH = "levels.json"


def solve(words, answer_letters):
    """words: list of answer strings. answer_letters: list[str] (multiset to cover).
    Returns list[set[int]] circles per word, or None if infeasible with every-word>=1."""
    n = len(words)
    # positions available per word: list of (pos, letter)
    avail = [[(i, ch) for i, ch in enumerate(w)] for w in words]
    target = Counter(answer_letters)
    total = sum(target.values())

    # Feasibility precheck: every word must have >=1 letter that appears in target.
    for wi, w in enumerate(words):
        if not any(ch in target for ch in w):
            return None  # this word cannot contribute -> can't satisfy every-word>=1

    best = None
    # We assign 'total' letter-slots. Each slot -> (word, pos) with letter matching a needed one.
    # Backtrack over target letters (expanded), choosing distinct positions.
    need = []
    for ch, c in sorted(target.items()):
        need.extend([ch] * c)

    used = [set() for _ in range(n)]  # positions used per word
    load = [0] * n

    def remaining_can_fill_empty(idx):
        # crude prune: ensure words still at load 0 can still be reached by some remaining letter
        empties = [wi for wi in range(n) if load[wi] == 0]
        if not empties:
            return True
        rest = Counter(need[idx:])
        for wi in empties:
            if not any(pos not in used[wi] and words[wi][pos] in rest
                       for pos in range(len(words[wi]))):
                return False
        return True

    def bt(idx):
        nonlocal best
        if best is not None:
            return
        if idx == len(need):
            if all(load[wi] >= 1 for wi in range(n)):
                best = [set(s) for s in used]
            return
        if not remaining_can_fill_empty(idx):
            return
        ch = need[idx]
        # candidate (word,pos) offering this letter; prefer least-loaded, then cap at 3/word
        cands = []
        for wi in range(n):
            if load[wi] >= len(words[wi]):
                continue  # physical limit only; least-loaded ordering keeps it balanced
            for pos in range(len(words[wi])):
                if pos not in used[wi] and words[wi][pos] == ch:
                    cands.append((load[wi], wi, pos))
        cands.sort()  # least-loaded first -> balanced + fills empties
        for _, wi, pos in cands:
            used[wi].add(pos); load[wi] += 1
            bt(idx + 1)
            used[wi].discard(pos); load[wi] -= 1
            if best is not None:
                return

    bt(0)
    return best


def main():
    data = json.load(open(PATH, encoding="utf-8"))
    changed, skipped = [], []
    for lv in data["levels"]:
        words = [w["answer"] for w in lv["words"]]
        ans = "".join(lv["surprise"]["answer"])
        letters = list(ans)
        # already all-contributing? still re-solve to enforce balance only if there is a filler
        has_filler = any(len(w["circles"]) == 0 for w in lv["words"])
        if not has_filler:
            continue
        sol = solve(words, letters)
        if sol is None:
            skipped.append(lv["id"])
            continue
        for wi, w in enumerate(lv["words"]):
            w["circles"] = sorted(sol[wi])
        # sanity
        circ = Counter("".join(words[wi][p] for wi in range(len(words)) for p in sol[wi]))
        assert circ == Counter(letters), f"L{lv['id']} multiset mismatch"
        assert all(len(s) >= 1 for s in sol), f"L{lv['id']} empty word remains"
        dist = [len(s) for s in sol]
        changed.append((lv["id"], dist))

    json.dump(data, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Redistributed circles (every word now contributes >=1):")
    for lid, dist in changed:
        print(f"  L{lid:>2}: per-word circle counts {dist}")
    if skipped:
        print("Left as-is (a word shares no letter with the answer):", skipped)
    else:
        print("All levels satisfy the authentic-Jumble every-word constraint.")


if __name__ == "__main__":
    main()
