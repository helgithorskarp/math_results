"""Independent exact audit of the public two-defect Schur-six fixtures."""

from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schur_s6_distant_two_defect_search"
N = 537


def word(path):
    raw = path.read_bytes()
    assert raw.endswith(b"\n") and raw.count(b"\n") == 1
    value = raw[:-1].decode("ascii")
    assert len(value) == N and set(value) <= set("123456?")
    return value


def triples():
    # Traverse by first summand, independently of the source's z-first audit.
    return [(a, b, a + b) for a in range(1, N + 1)
            for b in range(a, N - a + 1)]


def defects(value, rows):
    return [(a, b, z) for a, b, z in rows
            if value[a - 1] != "?" and
            value[a - 1] == value[b - 1] == value[z - 1]]


def completion_floor(value, rows):
    holes = [i for i, c in enumerate(value, 1) if c == "?"]
    assert len(holes) == 2
    scores = []
    for choices in product("123456", repeat=2):
        filled = list(value)
        for at, c in zip(holes, choices):
            filled[at - 1] = c
        scores.append((len(defects("".join(filled), rows)), "".join(choices)))
    return holes, min(score for score, _ in scores), sorted(
        choices for score, choices in scores
        if score == min(s for s, _ in scores))


def distance_under_relabelling(value, old):
    assert len(old) == N and set(old) == set("123456")
    return min(sum(a != relabel[int(b) - 1] for a, b in zip(value, old))
               for relabel in permutations("123456"))


def radius_two_barrier(value, rows):
    # Every zero-defect repair must change 3 or 6 to remove 3+3=6.
    # Check all one-site changes and all two-site changes containing either.
    incidence = [set() for _ in range(N + 1)]
    for index, row in enumerate(rows):
        for at in set(row):
            incidence[at].add(index)
    assert defects(value, rows) == [(3, 3, 6), (3, 6, 9)]
    one_best = N + 1
    for at in range(1, N + 1):
        local = [rows[i] for i in incidence[at]]
        old = sum(value[a - 1] == value[b - 1] == value[z - 1]
                  for a, b, z in local)
        for c in "123456":
            if c == value[at - 1]:
                continue
            def color(v):
                return c if v == at else value[v - 1]
            new = sum(color(a) == color(b) == color(z)
                      for a, b, z in local)
            one_best = min(one_best, 2 - old + new)
    pair_best = N + 1
    tested = 0
    for a, b in combinations(range(1, N + 1), 2):
        if a not in (3, 6) and b not in (3, 6):
            continue
        local = [rows[i] for i in incidence[a] | incidence[b]]
        for ca in "123456":
            if ca == value[a - 1]:
                continue
            for cb in "123456":
                if cb == value[b - 1]:
                    continue
                def color(v):
                    return ca if v == a else cb if v == b else value[v - 1]
                new = sum(color(x) == color(y) == color(z)
                          for x, y, z in local)
                pair_best = min(pair_best, new)
                tested += 1
    assert tested == 26775
    return one_best, pair_best, tested


def main():
    rows = triples()
    assert len(rows) == 72092
    assert sum(a == b for a, b, _ in rows) == 268
    names = ["20261001", "20261002", "20261003", "20261004",
             "20261005", "20261006", "20261008", "20261009",
             "20261010", "20261011"]
    expected = {
        "20261001": ([202, 404], 30), "20261002": ([7, 14], 17),
        "20261003": ([2, 4], 13), "20261004": ([13, 26], 18),
        "20261005": ([10, 20], 29), "20261006": ([3, 6], 25),
        "20261008": ([2, 4], 12), "20261009": ([5, 10], 9),
        "20261010": ([13, 26], 21), "20261011": ([2, 4], 14),
    }
    partials = {}
    for name in names:
        value = word(SOURCE / "partials" / f"{name}.partial")
        assert value[0] == "1"
        assert not defects(value, rows)
        holes, floor, minimizers = completion_floor(value, rows)
        assert (holes, floor) == expected[name]
        assert holes[1] == 2 * holes[0]
        partials[name] = (value, minimizers)
    complete = word(SOURCE / "completed29.txt")
    assert complete == partials["20261005"][0].replace("?", "1")
    assert "11" in partials["20261005"][1]
    assert len(defects(complete, rows)) == 29
    three = word(SOURCE / "best3.txt")
    two = word(SOURCE / "best2.txt")
    assert set(three) == set(two) == set("123456")
    assert defects(three, rows) == [(3, 3, 6), (3, 6, 9), (12, 15, 27)]
    assert defects(two, rows) == [(3, 3, 6), (3, 6, 9)]
    assert sha256((two + "\n").encode()).hexdigest() == \
        "8b6d6ae59d806f53b633c1ec4c6c9989c7f521a5924295ea4c2dc8868ebabdd2"
    previous = json.loads((ROOT / "schur_s6_multi_alignment_recombination" /
                           "sources.json").read_text())
    distances = {name: distance_under_relabelling(two, row["word"])
                 for name, row in previous.items()}
    assert distances == {"W": 414, "190": 428, "359": 425,
                         "best3": 421, "347": 427}
    one, pair, checked = radius_two_barrier(two, rows)
    assert (one, pair, checked) == (2, 33, 26775)
    print("PASS triples=72092 doublings=268 partials=10 "
          "best2_defects=[(3,3,6),(3,6,9)] "
          f"distances={distances} one_site_min={one} "
          f"repair_relevant_two_site_min={pair} two_site_candidates={checked}")


if __name__ == "__main__":
    main()
