"""Independent literal audit: all 2*C(43,5) physical events per branch.

No producer imports; independently reconstructed frame, pair numbering,
clause order, literal signs and cut clauses. The theorem in PROOF.md supplies
the global unsatisfiability argument, not these formula statistics.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from math import comb


def check(doc):
    def need(p, message):
        if not p:
            raise ValueError(message)
    pairs = [(i, j) for i in range(43) for j in range(i + 1, 43)]
    fixed_frame = {}
    for u, v in pairs:
        if u == 0 and v == 1 or u in (0, 1) and 2 <= v <= 6:
            fixed_frame[u, v] = 1
        elif 2 <= u < v <= 26 and (u - 2) // 5 == (v - 2) // 5:
            fixed_frame[u, v] = int((v - u) % 5 in (1, 4))
    ids = {e: j for j, e in enumerate((e for e in pairs if e not in fixed_frame), 1)}
    need(doc["n"] == 43 and doc["frame_free_variables"] == len(ids) == 842, "frame dimensions")
    need(doc["frame_pins"] == [[u, v, fixed_frame[u, v]] for u, v in pairs if (u, v) in fixed_frame], "frame pins")
    a, b, s = (doc[k] for k in ("a", "b", "separator"))
    need((len(a), len(b), len(s)) == (12, 12, 19), "branch profile")
    need(sorted(a + b + s) == list(range(43)), "partition")
    cross = [e for e in pairs if (e[0] in a and e[1] in b) or (e[1] in a and e[0] in b)]
    need(len(cross) == 144 and all(e in ids for e in cross), "cross variables")
    need([r["cross_color"] for r in doc["branches"]] == [0, 1], "both branches")
    checked = 0
    for row in doc["branches"]:
        c = row["cross_color"]
        colors = fixed_frame | {e: c for e in cross}
        histogram = Counter()
        color_counts = [0, 0]
        digest = sha256()
        body_bytes = 0
        for forbidden in (1, 0):
            for vertices in combinations(range(43), 5):
                checked += 1
                edges = list(combinations(vertices, 2))
                if any(e in colors and colors[e] != forbidden for e in edges):
                    continue
                literals = [ids[e] * (1 - 2 * forbidden) for e in edges if e not in colors]
                payload = (" ".join(map(str, literals)) + (" " if literals else "") + "0\n").encode("ascii")
                digest.update(payload)
                body_bytes += len(payload)
                color_counts[forbidden] += 1
                histogram[len(literals)] += 1
        need(row["fixed_pairs"] == len(colors) == 205, "fixed pair count")
        need(row["free_physical_pairs"] == len(pairs) - len(colors) == 698, "remaining free pairs")
        need(row["red_clauses"] == color_counts[1] and row["blue_clauses"] == color_counts[0], "color counts")
        need(row["ramsey_clauses"] == sum(color_counts), "clause total")
        need(row["length_histogram"] == {str(k): v for k, v in sorted(histogram.items())}, "clause lengths")
        need(row["literal_body_bytes"] == body_bytes and row["literal_body_sha256"] == digest.hexdigest(), "literal body")
        need(row["cut_nogood_in_F27_variables"] == [(1 - 2 * c) * ids[e] for e in cross], "cut nogood")
        need(histogram[0] == 0 and histogram[1] == 0, "branch has an empty/unit initial Ramsey clause")
    need(checked == 4 * comb(43, 5), "physical event coverage")
    return {"status": "PASS", "physical_monochromatic_events": checked,
            "complete_branches": 2, "free_pairs_per_branch": 698,
            "empty_initial_ramsey_clauses": 0, "unit_initial_ramsey_clauses": 0}
