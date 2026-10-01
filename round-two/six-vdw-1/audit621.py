"""Definition-level checks, using literal cyclic coordinates and column bits.

This verifier imports no encoding/search implementation. Only Python integers
and the standard library are used; failed checks raise, including under -O.
"""
from collections import Counter
from itertools import product
from math import gcd
import hashlib
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def direct_edges(tau):
    require(len(tau) == 207 and all(type(t) is int and t in (0, 1, 2) for t in tau),
            "invalid skeleton")
    columns = [1 << t for t in tau]
    counts = Counter()
    omitted = 0
    for step in range(1, 311):
        for start in range(621):
            colors = {}
            tautology = False
            for j in range(7):
                n = (start + j * step) % 621
                x, y = n % 207, n // 207
                bit = (columns[x] >> y) & 1
                if x in colors and colors[x] != bit:
                    tautology = True
                colors[x] = bit
            if tautology:
                require(step % 69 == 0, "unexpected repeated-variable safety")
                omitted += 1
                continue
            require(len(colors) == 7, "unexpected short signed constraint")
            support = tuple(sorted(colors))
            word = sum(colors[x] << i for i, x in enumerate(support))
            counts[support, min(word, word ^ 127)] += 1
    require(omitted == 2484, "short-orbit count mismatch")
    return counts


def cyclic_count(word):
    require(len(word) == 621 and all(type(b) is int and b in (0, 1) for b in word),
            "invalid cyclic word")
    count = 0
    for step in range(1, 621):
        for start in range(621):
            color = word[start]
            if all(word[(start + j * step) % 621] == color for j in range(1, 7)):
                count += 1
    return count


def check_coloring(text, required_length=None):
    bits = "".join(text.split())
    require(bits and all(c in "01" for c in bits), "malformed binary word")
    if required_length is not None:
        require(len(bits) == required_length, "wrong witness length")
    for step in range(1, (len(bits) - 1) // 6 + 1):
        for start in range(len(bits) - 6 * step):
            color = bits[start]
            if all(bits[start + j * step] == color for j in range(1, 7)):
                raise ValueError(f"monochromatic seven-AP: start={start}, step={step}")
    return {"valid": True, "length": len(bits)}


def balance_audit():
    cases = 0
    for m in (3, 6):
        for tau in product(range(3), repeat=m):
            sigma = [(tau[n % m] - n // m) % 3 for n in range(3 * m)]
            total = sum(sigma[(x + 3 * r) % (3 * m)] != sigma[x]
                        for x in range(m) for r in range(m))
            require(3 * total == 2 * m * m, "small twisted-balance identity failed")
            cases += 1
    return {"complete_skeletons": cases, "quotient_moduli": [3, 6]}


def controls():
    rejected = 0
    for text, length in [("", None), ("012", None), ("0000000", None),
                         ("1111111", None), ("0101010", 8), ("0,1", None)]:
        try:
            check_coloring(text, length)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("malformed/invalid coloring accepted")
    # A generic seven-AP checker must test steps greater than one.
    try:
        check_coloring("0101010101010")
    except ValueError as e:
        require("step=2" in str(e), "nonconsecutive AP control failed")
        rejected += 1
    else:
        raise ValueError("step-two monochromatic AP accepted")
    require(check_coloring("001011") == {"valid": True, "length": 6},
            "valid short control failed")
    for tau in ([0] * 206, [0] * 208, [0] * 206 + [3], [0] * 206 + [False]):
        try:
            direct_edges(tau)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("invalid skeleton accepted")
    return {"rejected_inputs": rejected, "valid_short_word": True}


def local_counts(t):
    # Enumerate each orientation and directly test all nine literal columns.
    columns = [1 << value for value in t]
    counts = Counter()
    for orientation in range(64):  # seventh bit zero chooses a complement class
        total = 0
        for start in range(3):
            for step in range(3):
                color = ((orientation >> 0) & 1) ^ ((columns[0] >> start) & 1)
                if all((((orientation >> j) & 1) ^
                        ((columns[j] >> ((start + j * step) % 3)) & 1)) == color
                       for j in range(1, 7)):
                    total += 1
        if total:
            counts[orientation] = total
    return counts


def compare_local(encoded_patterns):
    histogram = Counter()
    entry_checks = 0
    for t in product(range(3), repeat=7):
        got = local_counts(t)
        expected = encoded_patterns(t)
        require(got == expected, f"local multiplicities disagree: {t}")
        entry_checks += 64
        profile = tuple(sorted(Counter(got.values()).items()))
        histogram[profile] += 1
        periodic = all(t[j] == t[j + 3] for j in range(4))
        require((len(got) == 4) == periodic, "minimum-profile characterization failed")
    return {"vectors": 2187, "entry_checks": entry_checks,
            "profiles": [{"multiplicity": list(profile), "vectors": count}
                         for profile, count in sorted(histogram.items())]}


def support_and_carry_audit(tau):
    supports = Counter()
    bad_total = 0
    local_bad_total = 0
    defect_total = 0
    for r in range(1, 207):
        if 207 // gcd(r, 207) < 7:
            continue
        a_set = set()
        bad = set()
        for a in range(207):
            positions = [(a + j * r) % 621 for j in range(7)]
            residues = [n % 207 for n in positions]
            supports[tuple(sorted(residues))] += 1
            t = [(tau[n % 207] - n // 207) % 3 for n in positions]
            if any(t[j] != t[j + 3] for j in range(4)):
                bad.add(a)
            new_n = a + 3 * r
            if (tau[new_n % 207] - tau[a] - new_n // 207) % 3:
                a_set.add(a)
        union = {(x - j * r) % 207 for x in a_set for j in range(4)}
        require(union == bad, "bad-start identity failed")
        if r % 9:
            component_size = 207 // gcd(r, 207)
            require(component_size >= 9, "unexpected short orbit")
            require(len(bad) >= 6 * gcd(r, 207), "carry lower bound failed")
            # Each +3r cycle has nonzero winding modulo three.
            unvisited = set(range(207))
            while unvisited:
                first = min(unvisited)
                cycle = []
                x = first
                while x not in cycle:
                    cycle.append(x)
                    x = (x + 3 * r) % 207
                require(x == first, "cycle did not close at start")
                unvisited.difference_update(cycle)
                winding = sum((x + 3 * r) // 207 for x in cycle)
                require(winding % 3 != 0 and any(x in a_set for x in cycle),
                        "missing nonzero-carry defect")
        bad_total += len(bad)
        local_bad_total += len(union)
        defect_total += len(a_set)
    require(len(supports) == 21114 and set(supports.values()) == {2},
            "projected support is not unique up to reversal")
    require(defect_total == 28152, "exact carry-defect identity failed")
    require(bad_total == local_bad_total and bad_total >= defect_total,
            "global carry count failed")
    # The universal sum follows from threefold twisted balance on each
    # residue class mod3. Check that balance directly from the column table.
    for residue in range(3):
        histogram = Counter((tau[n % 207] - n // 207) % 3
                            for n in range(residue, 621, 3))
        require(histogram == {0: 69, 1: 69, 2: 69}, "twisted balance failed")
    return {"projected_supports": len(supports), "ordered_bad_starts": bad_total,
            "ordered_defects": defect_total,
            "universal_ordered_bad_floor": 28152, "universal_edge_floor": 112608}


def dictionary_digest(edges):
    payload = json.dumps([[list(support), mask, weight]
                          for (support, mask), weight in sorted(edges.items())],
                         separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("word")
    p.add_argument("--length", type=int)
    p.add_argument("--cyclic", action="store_true")
    args = p.parse_args()
    content = Path(args.word).read_text()
    if args.cyclic:
        bits = "".join(content.split())
        require(len(bits) == 621 and all(c in "01" for c in bits), "malformed cyclic word")
        pairs = cyclic_count(list(map(int, bits)))
        print(json.dumps({"valid_cyclic": pairs == 0, "cyclic_monochromatic_pairs": pairs,
                          "half_count": pairs // 2,
                          "file_sha256": hashlib.sha256(Path(args.word).read_bytes()).hexdigest()},
                         sort_keys=True))
    else:
        print(json.dumps(check_coloring(content, args.length), sort_keys=True))
