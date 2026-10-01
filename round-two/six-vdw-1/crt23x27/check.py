"""Independent complete bit-parallel truth-table verification.

This imports neither the native enumerator nor a solver. Bit i of each
Python integer represents one explicitly indexed assignment. Ordinary
integer Boolean operations evaluate literal constraints on ALL assignments.
"""
import argparse
import hashlib
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def repeat(block, width, copies):
    result = used = 0
    while copies:
        if copies & 1:
            result |= block << used
            used += width
        copies >>= 1
        if copies:
            block |= block << width
            width *= 2
    return result


def set_indices(bitmap):
    indices = []
    while bitmap:
        bottom = bitmap & -bitmap
        indices.append(bottom.bit_length() - 1)
        bitmap ^= bottom
    return indices


def binary_tables(q):
    count = 1 << (q - 1)
    tables = [0]
    for j in range(q - 1):
        width = 1 << j
        block = ((1 << width) - 1) << width
        tables.append(repeat(block, 2 * width, count // (2 * width)))
    return count, tables


def classify_u(q):
    coverage, tables = binary_tables(q)
    universe = (1 << coverage) - 1
    live = universe
    rejected = []
    for r in range(1, (q - 1) // 2 + 1):
        bad = 0
        for a in range(q):
            points = [(a + j * r) % q for j in range(7)]
            equalities = universe
            for j in range(4):
                equalities &= universe ^ (tables[points[j]] ^ tables[points[j + 3]])
            bad |= equalities
        rejected.append((live & bad).bit_count())
        live &= universe ^ bad
    return {"u_coverage": coverage, "u_survivors": [2 * i for i in set_indices(live)],
            "u_first_rejection": rejected}


def qr_word(q):
    return [int(x != 0 and pow(x, (q - 1) // 2, q) != 1) for x in range(q)]


def qr_orbit(q):
    bits = qr_word(q)
    words = set()
    for a in range(q):
        for multiplier in range(1, q):
            word = sum(bits[(a + multiplier * x) % q] << x for x in range(q))
            words.update((word, word ^ ((1 << q) - 1)))
    return words


def forbidden_patterns():
    bits = qr_word(23)
    patterns = set()
    for a in range(23):
        for r in range(23):
            pattern = sum(bits[(a + j * r) % 23] << j for j in range(7))
            patterns.update((pattern, 127 ^ pattern))
    return sorted(patterns)


TRIPLES = ((1, 0, 0), (0, 1, 0), (0, 0, 1),
           (0, 1, 1), (1, 0, 1), (1, 1, 0))
FIRST_TRIPLES = ((0, 1, 0), (0, 0, 1), (0, 1, 1))


def decode_column_assignment(index, columns=9):
    first = FIRST_TRIPLES[index % 3]
    index //= 3
    triples = [first]
    for _ in range(columns - 1):
        triples.append(TRIPLES[index % 6])
        index //= 6
    require(index == 0, "assignment index out of range")
    return [triples[x][y] for y in range(3) for x in range(columns)]


def column_tables(columns=9):
    coverage = 3 * 6 ** (columns - 1)
    tables = [0] * (3 * columns)
    for x in range(columns):
        choices = FIRST_TRIPLES if x == 0 else TRIPLES
        width = 1 if x == 0 else 3 * 6 ** (x - 1)
        period = len(choices) * width
        require(coverage % period == 0, "nonintegral truth-table period")
        unit = (1 << width) - 1
        for y in range(3):
            block = 0
            for digit, triple in enumerate(choices):
                if triple[y]:
                    block |= unit << (digit * width)
            tables[x + columns * y] = repeat(block, period, coverage // period)
    # Boundary and mixed-radix carry controls of the indexing, not a proof by sample.
    for i in sorted({0, 1, 2, 3, 5, 17, coverage // 2, coverage - 1}):
        direct = decode_column_assignment(i, columns)
        require([table >> i & 1 for table in tables] == direct, "truth-table index mismatch")
    return coverage, tables


def classify_v(patterns):
    coverage, tables = column_tables()
    universe = (1 << coverage) - 1
    complements = [universe ^ t for t in tables]
    live = universe
    rejected = []
    after_two = []
    for step in (1, 2, 3):
        before = live.bit_count()
        for a in range(27):
            if not live:
                break
            points = [(a + j * step) % 27 for j in range(7)]
            bad = 0
            for pattern in patterns:
                match = live
                for j, x in enumerate(points):
                    match &= tables[x] if pattern >> j & 1 else complements[x]
                    if not match:
                        break
                bad |= match
            live &= universe ^ bad
        rejected.append(before - live.bit_count())
        if step == 2:
            after_two = sorted(sum(bit << j for j, bit in enumerate(decode_column_assignment(i)))
                               for i in set_indices(live))
    survivors = sorted(sum(bit << j for j, bit in enumerate(decode_column_assignment(i)))
                       for i in set_indices(live))
    return {"v_coverage": coverage, "v_survivors": survivors,
            "v_first_rejection": rejected, "v_after_step2": after_two}


def classify_v9(patterns):
    live = list(range(0, 512, 2))
    rejected = []
    after_two = []
    for step in (1, 2, 3):
        previous = len(live)
        live = [word for word in live
                if all(sum((word >> ((a + j * step) % 9) & 1) << j for j in range(7)) not in patterns
                       for a in range(9))]
        rejected.append(previous - len(live))
        if step == 2:
            after_two = live[:]
    require(after_two == [146, 292, 438], "nine-bit rigidity failed")
    require(all((word >> x & 1) == (word >> ((x + 3) % 9) & 1)
                for word in after_two for x in range(9)), "survivors are not three-periodic")
    # An additional definition-level check bypasses forbidden-pattern tables:
    # build every normalized actual product on Z207 and find a real nonzero AP.
    q = qr_word(23)
    actual_obstructions = []
    for word in range(0, 512, 2):
        coloring = [q[n % 23] ^ (word >> (n % 9) & 1) for n in range(207)]
        obstruction = None
        for d in range(1, 207):
            for a in range(207):
                if len({coloring[(a + j * d) % 207] for j in range(7)}) == 1:
                    obstruction = [word, a, d, coloring[a]]
                    break
            if obstruction is not None:
                break
        require(obstruction is not None, "actual product lacks a monochromatic AP")
        actual_obstructions.append(obstruction)
    payload = json.dumps(actual_obstructions, separators=(",", ":")).encode()
    return {"v9_coverage": 256, "v9_survivors": live,
            "v9_first_rejection": rejected, "v9_after_step2": after_two}, hashlib.sha256(payload).hexdigest()


def scalar_u(q):
    survivors = []
    for index in range(1 << (q - 1)):
        word = index << 1
        bits = [word >> j & 1 for j in range(q)]
        if all(any(bits[(a + j * r) % q] != bits[(a + (j + 3) * r) % q] for j in range(4))
               for r in range(1, q) for a in range(q)):
            survivors.append(word)
    return survivors


def controls():
    small = []
    for q in (7, 11, 13):
        result = classify_u(q)
        require(result["u_survivors"] == scalar_u(q), "small full scalar classification mismatch")
        require(sum(result["u_first_rejection"]) + len(result["u_survivors"]) == result["u_coverage"],
                "small coverage mismatch")
        small.append({"q": q, "coverage": result["u_coverage"], "survivors": len(result["u_survivors"])})
    coverage, tables = column_tables(3)
    for index in range(coverage):
        require([t >> index & 1 for t in tables] == decode_column_assignment(index, 3),
                "small full column-table mismatch")
    # A genuine positive XOR-product fixture uses a single-one Z7 word and
    # mixed Z3 word. Every nonzero cyclic step, including repeated residues,
    # is checked directly. Rejecting all products would fail this control.
    word = [int(n % 7 == 0) ^ int(n % 3 == 0) for n in range(21)]
    require(all(len({word[(a + j * d) % 21] for j in range(7)}) > 1
                for a in range(21) for d in range(1, 21)), "positive product fixture failed")
    q = qr_word(23)
    word69 = [q[n % 23] ^ int(n % 3 == 0) for n in range(69)]
    require(all(len({word69[(a + j * d) % 69] for j in range(7)}) > 1
                for a in range(69) for d in range(1, 69)), "QR23 times Z3 positive fixture failed")
    return {"small_u": small, "all_small_column_assignments": coverage,
            "positive_product_modulus": 21, "positive_product_windows": 420,
            "positive_qr_product_modulus": 69, "positive_qr_product_windows": 4692}


def verify(native):
    result = classify_u(23)
    orbit = qr_orbit(23)
    normalized_orbit = sorted(w for w in orbit if not w & 1)
    require(len(orbit) == 92 and len(normalized_orbit) == 46, "incorrect QR orbit cardinality")
    require(result["u_survivors"] == normalized_orbit, "23-word classification is not the QR orbit")
    require(sum(result["u_first_rejection"]) + 46 == result["u_coverage"], "incomplete u coverage")
    patterns = forbidden_patterns()
    require(len(patterns) == 50, "incorrect forbidden pattern count")
    result["forbidden_words"] = patterns
    v9, actual_obstructions_digest = classify_v9(patterns)
    result.update(v9)
    require(result["v9_survivors"] == [] and sum(result["v9_first_rejection"]) == 256,
            "incomplete nine-bit exclusion")
    result.update(classify_v(patterns))
    require(result["v_survivors"] == [] and sum(result["v_first_rejection"]) == result["v_coverage"],
            "v exclusion or coverage failed")
    require(len(result["v_after_step2"]) == 54, "step-three omission control failed")
    def match_native(candidate):
        require(isinstance(candidate, dict) and result == candidate,
                "native and independent full truth tables disagree")
    match_native(native)
    # Meaningful corruptions must not match the independently computed result.
    corruptions = [dict(native) for _ in range(4)]
    corruptions[0]["u_survivors"] = native["u_survivors"][1:]
    corruptions[1]["v_coverage"] -= 1
    corruptions[2]["v_survivors"] = native["v_after_step2"][:1]
    corruptions[3]["forbidden_words"] = native["forbidden_words"][1:]
    for corrupt in corruptions:
        try:
            match_native(corrupt)
        except ValueError:
            pass
        else:
            raise ValueError("corrupted result accepted")
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    return {"status": "COMPLETE_CRT23X27_CLASSIFICATION_AND_EXCLUSION_CHECKED",
            "result": result, "labeled_u_words": len(orbit), "controls": controls(),
            "corruptions_rejected": len(corruptions),
            "definition_level_207_products_checked": 256,
            "actual_obstructions_sha256": actual_obstructions_digest,
            "result_sha256": hashlib.sha256(canonical).hexdigest()}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("native", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = verify(json.loads(args.native.read_text()))
    text = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")
