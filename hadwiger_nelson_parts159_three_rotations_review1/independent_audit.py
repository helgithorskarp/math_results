#!/usr/bin/env python3
"""Clean-room exact audit of the three-rotation Parts159 theorem.

The submitted Python modules are never imported.  Base-field elements use the
quotient basis 1,t,r,tr with t^2=-3 and r^2=-11, rather than the submitted
1,sqrt(33),t,r formulas.  Quadratic contact fields use a second quotient
generator q with q^2=d.  The target's compact positive certificate is checked
against geometry reconstructed from the hash-bound point file.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_parts159_three_rotations"
POINTS = ROOT / "hadwiger_nelson_nonmono159_214_lowden2" / "points159.tsv"
LIBRARY = ROOT / "hadwiger_nelson_nonmono159_origin_pencil" / "colorings.txt"
FIELD_SOURCE = ROOT / "hadwiger_nelson_nonmono_field_obstruction" / "coloring.py"

EXPECTED_HASHES = {
    TARGET / "certificate.json": "5c492df795e1703548e77126454bca5ca2a007e17a39b8633d63535d6005214a",
    TARGET / "PROOF.md": "c8b46e7679174cf5bfdf3f010d81b9c8b222cde0523f0ef0418336249e7913fa",
    POINTS: "4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02",
    LIBRARY: "1c2fab00fd9d8ceff169336f7015012dc9c6e9487d8e5b628419a3e2d98660dd",
    FIELD_SOURCE: "a612f6f145f511340d930cf093939cf102128e960ae12977e86dfb1d1e5b486e",
}

# Bit 0 denotes t=i*sqrt(3), bit 1 denotes r=i*sqrt(11).
E = tuple[Q, Q, Q, Q]
X = tuple[E, E]                 # a+b*q, q^2=d
R = tuple[Q, Q]                 # a+b*sqrt(33), target real-basis order
ZERO: E = (Q(0),) * 4
ONE: E = (Q(1), Q(0), Q(0), Q(0))
T: E = (Q(0), Q(1), Q(0), Q(0))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(x: E, y: E) -> E:
    return tuple(a + b for a, b in zip(x, y, strict=True))  # type: ignore[return-value]


def neg(x: E) -> E:
    return tuple(-a for a in x)  # type: ignore[return-value]


def sub(x: E, y: E) -> E:
    return add(x, neg(y))


def scale(x: E, a: Q) -> E:
    return tuple(a * b for b in x)  # type: ignore[return-value]


def mul(x: E, y: E) -> E:
    """Multiply in Q[t,r]/(t^2+3,r^2+11)."""
    out = [Q(0)] * 4
    for i, a in enumerate(x):
        if not a:
            continue
        for j, b in enumerate(y):
            if not b:
                continue
            factor = Q(1)
            if i & j & 1:
                factor *= -3
            if i & j & 2:
                factor *= -11
            out[i ^ j] += factor * a * b
    return tuple(out)  # type: ignore[return-value]


def galois(x: E, mask: int) -> E:
    return tuple(
        -a if (i & mask).bit_count() % 2 else a for i, a in enumerate(x)
    )  # type: ignore[return-value]


def bar(x: E) -> E:
    """Ordinary complex conjugation: t,r change sign and tr is fixed."""
    return galois(x, 3)


def inv(x: E) -> E:
    require(x != ZERO, "division by zero")
    numerator = ONE
    for mask in (1, 2, 3):
        numerator = mul(numerator, galois(x, mask))
    denominator = mul(x, numerator)
    require(not any(denominator[1:]) and denominator[0] != 0, "bad field norm")
    answer = scale(numerator, 1 / denominator[0])
    require(mul(x, answer) == ONE, "field inverse")
    return answer


def norm(x: E) -> E:
    answer = mul(x, bar(x))
    require(answer[1] == answer[2] == 0, "nonreal complex norm")
    return answer


def real_to_e(x: R) -> E:
    # tr=-sqrt(33) in this quotient basis.
    return x[0], Q(0), Q(0), -x[1]


def e_to_real(x: E) -> R:
    require(x[1] == x[2] == 0, "element is not real")
    return x[0], -x[3]


def target_tuple(x: E) -> tuple[Q, Q, Q, Q]:
    """Convert to the target's order 1,sqrt(33),t,r for index alignment."""
    return x[0], -x[3], x[1], x[2]


def radd(x: R, y: R) -> R:
    return x[0] + y[0], x[1] + y[1]


def rneg(x: R) -> R:
    return -x[0], -x[1]


def rmul(x: R, y: R) -> R:
    return x[0] * y[0] + 33 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def rinv(x: R) -> R:
    denominator = x[0] * x[0] - 33 * x[1] * x[1]
    require(denominator != 0, "real division by zero")
    return x[0] / denominator, -x[1] / denominator


def rdiv(x: R, y: R) -> R:
    return rmul(x, rinv(y))


def rational_sqrt(x: Q) -> Q | None:
    if x < 0:
        return None
    a, b = math.isqrt(x.numerator), math.isqrt(x.denominator)
    return Q(a, b) if a * a == x.numerator and b * b == x.denominator else None


def real_sign(x: R) -> int:
    a, b = x
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0 or (a > 0) == (b > 0):
        return (b > 0) - (b < 0)
    relative_norm = a * a - 33 * b * b
    require(relative_norm != 0, "unexpected rational sqrt(33)")
    return ((a > 0) - (a < 0)) * ((relative_norm > 0) - (relative_norm < 0))


def real_sqrt(x: R) -> R | None:
    """Return one exact root in Q(s33), iff it exists."""
    a, b = x
    if b == 0:
        q = rational_sqrt(a)
        if q is not None:
            return q, Q(0)
        q = rational_sqrt(a / 33)
        return None if q is None else (Q(0), q)
    n = rational_sqrt(a * a - 33 * b * b)
    if n is None:
        return None
    # This order duplicates only the public certificate's canonical root labels;
    # existence is rechecked by multiplication below.
    for sign in (-1, 1):
        q = rational_sqrt((a + sign * n) / 2)
        if q:
            answer = q, b / (2 * q)
            require(rmul(answer, answer) == x, "real square-root reconstruction")
            return answer
    return None


def xadd(x: X, y: X) -> X:
    return add(x[0], y[0]), add(x[1], y[1])


def xneg(x: X) -> X:
    return neg(x[0]), neg(x[1])


def xsub(x: X, y: X) -> X:
    return xadd(x, xneg(y))


def xmul(x: X, y: X, d: E) -> X:
    return (
        add(mul(x[0], y[0]), mul(mul(x[1], y[1]), d)),
        add(mul(x[0], y[1]), mul(x[1], y[0])),
    )


def xbar(x: X) -> X:
    return bar(x[0]), bar(x[1])


def xnorm(x: X, d: E) -> X:
    return xmul(x, xbar(x), d)


def read_points() -> list[E]:
    lines = POINTS.read_text(encoding="ascii").splitlines()
    require(lines[0] == "# scale 12", "point scale")
    points = []
    for line in lines[1:]:
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        require(len(row) == 16, "point width")
        require(all(row[i] == 0 for i in range(16) if i not in (0, 5, 9, 12)),
                "point outside the stated field")
        points.append((Q(row[0], 12), Q(row[9], 12), Q(row[12], 12), Q(-row[5], 12)))
    require(len(points) == len(set(points)) == 159 and points[0] == ZERO, "point inventory")
    return points


def unit_edges(points: list[E]) -> list[tuple[int, int]]:
    return [
        (i, j)
        for i, j in itertools.combinations(range(len(points)), 2)
        if norm(sub(points[i], points[j])) == ONE
    ]


def bit0_root33(bits: int) -> int:
    """The root sqrt(33)=1 mod 8 modulo 2^bits, lifted independently."""
    require(bits >= 1, "bad 2-adic precision")
    # Write root=1+8*u.  After expansion and division by 16,
    # root^2=33 is equivalent to 4*u^2+u-2=0.
    # The latter polynomial has odd derivative, so u has one lift per bit.
    u = 0
    for exponent in range(max(0, bits - 3)):
        modulus = 1 << (exponent + 1)
        candidates = (u, u + (1 << exponent))
        good = [x for x in candidates if (4 * x * x + x - 2) % modulus == 0]
        require(len(good) == 1, "shifted 2-adic lift is not unique")
        u = good[0]
    root = (1 + 8 * u) % (1 << bits)
    require((root * root - 33) % (1 << bits) == 0, "bad 2-adic root")
    return root


def field_color(x: E) -> int:
    a, b, c, d = target_tuple(x)
    denominator = math.lcm(*(v.denominator for v in (a, b, c, d)))
    aa, bb, cc, dd = (int(v * denominator) for v in (a, b, c, d))
    exponent = (denominator & -denominator).bit_length() - 1
    modulus = 1 << (exponent + 1)
    radical = bit0_root33(exponent + 1)
    odd_inverse = pow(3 * (denominator >> exponent), -1, modulus)
    first = ((3 * aa + 3 * bb * radical + 3 * cc + dd * radical) * odd_inverse) % modulus
    second = ((6 * cc + 2 * dd * radical) * odd_inverse) % modulus
    return (first >> exponent) + 2 * (second >> exponent)


def proper(word: tuple[int, ...], edges: list[tuple[int, int]]) -> bool:
    return (
        len(word) == 159
        and word[0] == 0
        and all(type(c) is int and 0 <= c < 4 for c in word)
        and all(word[i] != word[j] for i, j in edges)
    )


def bridge(a: tuple[int, ...], b: tuple[int, ...], edges, same=()) -> bool:
    return all(a[i] != b[j] for i, j in edges) and all(a[i] == b[j] for i, j in same)


def direct_e_contacts(points: list[E], z: E):
    edges, same = [], []
    image = [mul(z, point) for point in points]
    denominator = math.lcm(*(v.denominator for point in points + image for v in point))
    left = [tuple(int(v * denominator) for v in point) for point in points]
    right = [tuple(int(v * denominator) for v in point) for point in image]
    for i in range(1, 159):
        for j in range(1, 159):
            a, b, c, d = (x - y for x, y in zip(left[i], right[j], strict=True))
            if a == b == c == d == 0:
                same.append((i, j))
            # In the signed quotient basis the tr coefficient is the negative
            # of the sqrt(33) coefficient.  These two integer equations are
            # exactly norm=1, with no division or approximate comparison.
            if -a * d + b * c == 0 and a * a + 3 * b * b + 11 * c * c + 33 * d * d == denominator * denominator:
                edges.append((i, j))
    return edges, same


def enumerate_geometry(points: list[E]):
    norms = [norm(point) for point in points]
    groups = defaultdict(list)
    group_d = {}
    e_roots = set()
    counts = Counter()
    pair_digest = hashlib.sha256()
    for i in range(1, 159):
        for j in range(1, 159):
            s = sub(add(norms[i], norms[j]), ONE)
            delta = sub(scale(mul(norms[i], norms[j]), Q(4)), mul(s, s))
            d = e_to_real(scale(delta, Q(1, 3)))
            sign = real_sign(d)
            root = real_sqrt(d)
            if sign < 0:
                require(root is None, "negative discriminant square")
                case = "negative"
            elif root is not None:
                c = mul(bar(points[i]), points[j])
                imaginary = mul(T, real_to_e(root))
                for root_sign in (-1, 1):
                    z = scale(mul(add(s, scale(imaginary, Q(root_sign))), inv(c)), Q(1, 2))
                    require(norm(z) == ONE, "E contact root is not a rotation")
                    e_roots.add(z)
                case = "E"
            else:
                require(sign > 0, "unhandled double root")
                c = mul(bar(points[i]), points[j])
                key = target_tuple(mul(s, inv(c))), target_tuple(mul(mul(points[i], bar(points[j])), inv(c)))
                groups[key].append((i, j))
                group_d.setdefault(key, d)
                case = "outside"
            counts[case] += 1
            pair_digest.update(f"{i},{j},{case}\n".encode("ascii"))
    items = sorted(groups.items())
    require(sum(counts.values()) == 158 * 158, "pair census")
    return norms, counts, items, [group_d[key] for key, _ in items], sorted(e_roots), pair_digest.hexdigest()


def classify_fields(ds: list[R]):
    representatives: list[R] = []
    classification = {}
    for d in sorted(set(ds)):
        for index, representative in enumerate(representatives):
            square = real_sqrt(rdiv(d, representative))
            if square is not None:
                classification[d] = index, square
                break
        else:
            classification[d] = len(representatives), (Q(1), Q(0))
            representatives.append(d)
    # The representatives are pairwise inequivalent quadratic extensions.
    for a, b in itertools.combinations(representatives, 2):
        require(real_sqrt(rdiv(a, b)) is None, "duplicate quadratic extension")
    return representatives, classification


def build_roots(items, ds, representatives, classification, points):
    roots = []
    for group_index, (((T_key, _V_key), edges), d0) in enumerate(zip(items, ds, strict=True)):
        field_index, square = classification[d0]
        d = real_to_e(representatives[field_index])
        T_value = (T_key[0], T_key[2], T_key[3], -T_key[1])
        require(T_value != ZERO, "zero-trace outside contact")
        i, j = edges[0]
        c = mul(bar(points[i]), points[j])
        a = scale(T_value, Q(1, 2))
        b = scale(mul(mul(T, real_to_e(square)), inv(c)), Q(1, 2))
        require(b != ZERO, "reducible outside root")
        for sign in (-1, 1):
            z = (a, scale(b, Q(sign)))
            require(xnorm(z, d) == (ONE, ZERO), "outside root is not a rotation")
            for p, q in edges:
                displacement = xsub((points[p], ZERO), xmul(z, (points[q], ZERO), d))
                require(xnorm(displacement, d) == (ONE, ZERO), "listed contact is not unit")
            roots.append((group_index, field_index, z))
    return roots


def key_from_e(trace: E, value: E):
    return target_tuple(trace), target_tuple(value)


def relative_contacts(group_map, e_data, u: X, v: X, d: E):
    relative = xmul(xbar(u), v, d)
    if relative[1] == ZERO:
        edges, same = e_data.get(relative[0], ([], []))
        return edges, same, "E", relative[0]
    trace = scale(relative[0], Q(2))
    value = sub(mul(relative[0], relative[0]), mul(mul(relative[1], relative[1]), d))
    return group_map.get(key_from_e(trace, value), []), [], "outside_E", None


def certificate_data(internal):
    raw = (TARGET / "certificate.json").read_text(encoding="ascii")
    cert = json.loads(raw)
    require(set(cert) == {"words", "extensions", "cycles"}, "certificate schema")
    extra = [tuple(map(int, word)) for word in cert["words"]]
    require(len(extra) == len(set(extra)) and all(proper(word, internal) for word in extra),
            "certificate component word")
    extensions = {i: word for i, word in cert["extensions"]}
    cycles = {(i, j): (a, b, c) for i, j, a, b, c in cert["cycles"]}
    require(len(extensions) == len(cert["extensions"]) and len(cycles) == len(cert["cycles"]),
            "duplicate certificate row")
    require(all(0 <= i < len(extra) for i in extensions.values()), "extension word index")
    require(all(0 <= i < len(extra) for row in cycles.values() for i in row), "cycle word index")
    return extra, extensions, cycles


def main() -> None:
    for path, expected in EXPECTED_HASHES.items():
        require(file_hash(path) == expected, f"artifact hash: {path}")

    # Quotient-ring and exact-sign controls are definition-level, not target imports.
    sample = (Q(2), Q(-1, 3), Q(5, 7), Q(4, 9))
    require(mul(sample, inv(sample)) == ONE, "inverse control")
    require(mul(T, T) == scale(ONE, Q(-3)), "t relation")
    require(real_sign((Q(-17, 10), Q(1))) == 1, "real sign control")
    require(real_sqrt((Q(58), Q(10))) == (Q(5), Q(1)), "real square control")

    points = read_points()
    internal = unit_edges(points)
    degree = Counter(vertex for edge in internal for vertex in edge)
    require(len(internal) == 646 and len(degree) == 159 and min(degree.values()) >= 2,
            "strict component graph / coincidence lemma")

    library = [tuple(map(int, line)) for line in LIBRARY.read_text(encoding="ascii").splitlines()]
    require(len(library) == 4 and all(proper(word, internal) for word in library), "base library")
    permutations = [(0,) + p for p in itertools.permutations((1, 2, 3))]
    words = [tuple(permutation[color] for color in word) for word in library for permutation in permutations]
    require(len(words) == 24 and all(proper(word, internal) for word in words), "permuted library")
    fixed = tuple(field_color(point) for point in points)
    require(fixed == library[0], "independent full-field-field colouring interface")

    norms, counts, items, ds, e_roots, pair_sha = enumerate_geometry(points)
    require(counts == Counter({"negative": 2937, "E": 12906, "outside": 9121}), "pair classes")
    require(len(items) == 1490 and len(set(ds)) == 60 and len(e_roots) == 178, "event census")
    group_map = dict(items)

    # Ratios separately reconstruct every possible nonzero coincidence phase.
    coincidence_map = defaultdict(list)
    for i in range(1, 159):
        for j in range(1, 159):
            coincidence_map[mul(points[i], inv(points[j]))].append((i, j))

    e_data = {}
    for z in e_roots:
        edges, same = direct_e_contacts(points, z)
        require(edges, "spurious E event")
        require(same == coincidence_map.get(z, []), "E coincidence reconstruction")
        word = tuple(field_color(mul(z, point)) for point in points)
        require(proper(word, internal) and bridge(fixed, word, edges, same), "E field gluing")
        e_data[z] = edges, same

    representatives, classification = classify_fields(ds)
    require(len(representatives) == 52, "quadratic-extension census")
    roots = build_roots(items, ds, representatives, classification, points)
    require(len(roots) == 2980, "outside root census")

    extra, extensions, cycles = certificate_data(internal)
    used_extensions = set()
    masks = []
    for index, (_key, edges) in enumerate(items):
        masks.append([
            sum(1 << j for j, candidate in enumerate(words) if bridge(central, candidate, edges))
            for central in library
        ])
        witness = next((word for word in words if bridge(fixed, word, edges)), None)
        if witness is None:
            require(index in extensions, "missing extension certificate")
            witness = extra[extensions[index]]
            used_extensions.add(index)
        require(bridge(fixed, witness, edges), "bad extension certificate")
    require(used_extensions == set(extensions), "unused extension certificate")

    roots_by_field = defaultdict(list)
    for index, (_group, field, _root) in enumerate(roots):
        roots_by_field[field].append(index)
    same_field = sum(len(ids) * (len(ids) - 1) // 2 for ids in roots_by_field.values())
    require(same_field == 118734, "same-field pair census")

    compatible_cache = {}
    hist = Counter()
    used_cycles = set()
    used_extra_words = set(extensions.values())
    coverage = hashlib.sha256()
    for field, ids in sorted(roots_by_field.items()):
        d = real_to_e(representatives[field])
        for i, j in itertools.combinations(ids, 2):
            gi, fi, u = roots[i]
            gj, fj, v = roots[j]
            require(fi == fj == field, "field bucket")
            edges, same, kind, e_relative = relative_contacts(group_map, e_data, u, v, d)
            hist[kind] += 1
            if kind == "E":
                exact_same = coincidence_map.get(e_relative, [])
                require(same == exact_same, "relative E coincidence completeness")
                require(not exact_same or edges, "coincidence without forced contact")
            if not edges:
                require(not same, "unhandled coincidence")
                hist["no_outer_edges"] += 1
                continue
            contact_key = tuple(edges), tuple(same)
            if contact_key not in compatible_cache:
                compatible_cache[contact_key] = [
                    sum(1 << k for k, candidate in enumerate(words) if bridge(word, candidate, edges, same))
                    for word in words
                ]
            compatible = compatible_cache[contact_key]
            witness = None
            for a in range(4):
                for b in range(24):
                    options = compatible[b] & masks[gj][a] if masks[gi][a] >> b & 1 else 0
                    if options:
                        witness = a, b, (options & -options).bit_length() - 1
                        break
                if witness is not None:
                    break
            if witness is not None:
                a, b, c = witness
                ca, cb, cc = library[a], words[b], words[c]
                hist["library"] += 1
                tag = ["library", a, b, c]
            else:
                require((i, j) in cycles, "missing cycle certificate")
                indices = cycles[i, j]
                ca, cb, cc = (extra[k] for k in indices)
                used_cycles.add((i, j))
                used_extra_words.update(indices)
                hist["certificate"] += 1
                tag = ["certificate", *indices]
            require(bridge(ca, cb, items[gi][1]), "central/first bridge")
            require(bridge(ca, cc, items[gj][1]), "central/second bridge")
            require(bridge(cb, cc, edges, same), "outer bridge")
            coverage.update((json.dumps([i, j, tag], separators=(",", ":")) + "\n").encode("ascii"))
    require(used_cycles == set(cycles), "unused cycle certificate")
    require(used_extra_words == set(range(len(extra))), "unused component word")

    expected_hist = Counter({
        "E": 40982,
        "outside_E": 77752,
        "no_outer_edges": 80858,
        "library": 37516,
        "certificate": 360,
    })
    require(hist == expected_hist, "same-field outcome census")
    require(coverage.hexdigest() == "5abdc23954147463c5438704a65930fb0ddbfdc4ef9bc848758077f203571140",
            "entry-level certificate coverage")

    result = {
        "E_contact_rotations": len(e_roots),
        "all_checks": True,
        "certificate_component_words": len(extra),
        "certificate_sha256": file_hash(TARGET / "certificate.json"),
        "continuum_reduction_reviewed": True,
        "coverage_sha256": coverage.hexdigest(),
        "cycle_rows": len(used_cycles),
        "different_field_pairs_excluded_by_degree_four": len(roots) * (len(roots) - 1) // 2 - same_field,
        "fixed_extension_rows": len(used_extensions),
        "internal_edges": len(internal),
        "outside_contact_classes": len(items),
        "outside_contact_rotations": len(roots),
        "pair_classification_sha256": pair_sha,
        "positive_radicands": len(set(ds)),
        "quadratic_extensions": len(representatives),
        "same_field_pairs": same_field,
        "same_field_outcomes": dict(sorted(hist.items())),
        "strict_plane_support_checked": True,
        "vertices_per_copy": len(points),
        "vertex_upper_bound": 1 + 3 * (len(points) - 1),
    }
    expected = json.loads((HERE / "EXPECTED.json").read_text(encoding="ascii"))
    require(result == expected, "expected result mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
