#!/usr/bin/env python3
"""Clean-room exact check of the point606 horizontal-shear exclusion.

The reviewed modules are never imported.  Arithmetic uses the reversed tower
Q(sqrt(11))(sqrt(5))(sqrt(3)), and the source coordinates and positive
deletion certificates are decoded directly from their pinned data files.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from math import isqrt
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SOURCE = REPO / "hadwiger_nelson_point606_shear_class"
POINTS = REPO / "hadwiger_nelson_parts509_completion_census_degree9/points.tsv"
COMPLETIONS = REPO / "hadwiger_nelson_parts509_swap_closure/completion_points.json"
CORE_CERT = REPO / "hadwiger_nelson_point606_criticality_gate/certificate.json"
OLD_CERT = REPO / "hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json"
CATALOGUE = REPO / "hadwiger_nelson_parts509_degree6_lift_family/catalogue.json"

PINS = {
    "source/README.md": "d9feb2c2aafdda42096f1d51760f2e5ee3aadf90fc9f1cf2a69285a90560330f",
    "source/EXPECTED.json": "15fadfab6d93fe777c51b3e22f21fe4d3b7f3d9ad6416f27d11adccb347b1673",
    "source/audit.cpp": "fc3dc80191c54e6d9a56737065ac979e7c9073bcfdb941c125eda8501fe14b6f",
    "source/controls.py": "94c5a80e1386a32642970af0bd7e9e2f34a227d80fd236f3e1a96cdc4eebf943",
    "source/field.py": "8d0ba3eea249cb6fa3cb14504ff7894db9b4e3933b6ab1bc46f31308418cc9a2",
    "source/inputs.json": "dbb8d60405bcf19c5feec50e6bf82b50a34fab8f5f5e906d97869eed7e4a06cc",
    "source/model.py": "e921343715835c2583f8de9c0388df40bb5cf7bb93ff4694b05b1947aa1a09df",
    "source/verify.py": "2b49dcf1d069a8f557b1d3bfcfde206c69cfa1bd5fc3c3fa1e622afc02ad8c26",
    "points": "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    "completions": "b82909c48ce088deb89b555f4c8fa554bba44030570fdaaf0b9b607e9552a5a6",
    "core_cert": "be652a44cb9e070c77a6404ee7cfc45a6956e94f600a0b486ec1d21ed6bfdb20",
    "old_cert": "41a47be8d0568be7e1497f16a45c17d433e31e01fb62877856189fbf1ad53729",
    "catalogue": "0282698f8bfb3b7df241c3d60af0dfef82f6f0535f114af71bf0db11807d0a4f",
}


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def add(a, b):
    return tuple(x + y for x, y in zip(a, b, strict=True))


def neg(a):
    return tuple(-x for x in a)


def sub(a, b):
    return add(a, neg(b))


def scale(a, q):
    return tuple(q * x for x in a)


class ReverseTower:
    """Elements ordered as 1,r11,r5,r55,r3,r33,r15,r165."""

    radicals = (11, 5, 3)

    def mul(self, a, b):
        require(len(a) == len(b), "field width")
        if len(a) == 1:
            return (a[0] * b[0],)
        half = len(a) // 2
        d = self.radicals[len(a).bit_length() - 2]
        x, y = a[:half], a[half:]
        u, v = b[:half], b[half:]
        return add(self.mul(x, u), scale(self.mul(y, v), d)) + add(
            self.mul(x, v), self.mul(y, u)
        )

    def inv(self, a):
        if len(a) == 1:
            require(a[0] != 0, "division by zero")
            return (1 / a[0],)
        half = len(a) // 2
        d = self.radicals[len(a).bit_length() - 2]
        x, y = a[:half], a[half:]
        norm_inverse = self.inv(sub(self.mul(x, x), scale(self.mul(y, y), d)))
        return self.mul(x, norm_inverse) + neg(self.mul(y, norm_inverse))

    def div(self, a, b):
        return self.mul(a, self.inv(b))

    def sqrt(self, a):
        """Return an exact square root in the tower, or None, exhaustively."""
        if not any(a):
            return a
        if len(a) == 1:
            q = F(a[0])
            if q < 0:
                return None
            p, r = isqrt(q.numerator), isqrt(q.denominator)
            return (F(p, r),) if p * p == q.numerator and r * r == q.denominator else None
        half = len(a) // 2
        d = self.radicals[len(a).bit_length() - 2]
        A, B = a[:half], a[half:]
        zero = (F(0),) * half
        if not any(B):
            x = self.sqrt(A)
            if x is not None:
                return x + zero
            y = self.sqrt(scale(A, F(1, d)))
            return zero + y if y is not None else None
        norm_root = self.sqrt(sub(self.mul(A, A), scale(self.mul(B, B), d)))
        if norm_root is None:
            return None
        for signed_root in (norm_root, neg(norm_root)):
            x = self.sqrt(scale(add(A, signed_root), F(1, 2)))
            if x is not None and any(x):
                y = self.div(B, scale(x, 2))
                answer = x + y
                if self.mul(answer, answer) == a:
                    return answer
        return None


K = ReverseTower()
Z = (F(0),) * 8
ONE = (F(1),) + Z[1:]


def reverse_basis(a):
    """Convert published (3,5,11) bit order to the checker tower order."""
    return tuple(F(a[((i & 1) << 2) | (i & 2) | ((i & 4) >> 2)]) for i in range(8))


def original_basis(a):
    return reverse_basis(a)  # the bit-reversal permutation is an involution


def load_points_and_labels():
    raw = []
    for line in POINTS.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(3 * int(x) for x in line.split())
        require(len(row) == 16, "point row width")
        raw.append((row[:8], row[8:]))
    require(len(raw) == 509, "base point count")
    for point in json.loads(COMPLETIONS.read_text())["points"]:
        row = []
        for axis in ("x", "y"):
            coeffs = tuple(288 * F(v) for v in point[axis])
            require(len(coeffs) == 8 and all(v.denominator == 1 for v in coeffs), "completion")
            row.append(tuple(int(v) for v in coeffs))
        raw.append(tuple(row))
    cert = json.loads(CORE_CERT.read_text())
    deleted = cert["deleted_labels"]
    require(deleted == sorted(set(deleted)), "deleted labels")
    labels = [v for v in list(range(585)) + [606] if v not in deleted]
    selected_raw = [raw[v] for v in labels]
    require(len(selected_raw) == 530 and len(set(selected_raw)) == 530, "core points")
    selected = [
        (scale(reverse_basis(x), F(1, 288)), scale(reverse_basis(y), F(1, 288)))
        for x, y in selected_raw
    ]
    return selected_raw, selected, labels, cert


def canonical_difference(raw_a, raw_b):
    x = tuple(v - u for u, v in zip(raw_a[0], raw_b[0], strict=True))
    y = tuple(v - u for u, v in zip(raw_a[1], raw_b[1], strict=True))
    first = next(c for c in x + y if c)
    if first < 0:
        x, y = tuple(-c for c in x), tuple(-c for c in y)
    return x, y


def enumerate_events(raw_points):
    differences = {}
    for i, j in combinations(range(len(raw_points)), 2):
        differences.setdefault(canonical_difference(raw_points[i], raw_points[j]), []).append((i, j))
    fixed = set()
    event_only = {}
    vertical_tests = {}
    eligible_classes = 0
    contact_checks = 0
    for (raw_x, raw_y), pair_list in sorted(differences.items()):
        x = scale(reverse_basis(raw_x), F(1, 288))
        y = scale(reverse_basis(raw_y), F(1, 288))
        if y == Z:
            if K.mul(x, x) == ONE:
                fixed.update(pair_list)
            continue
        if y not in vertical_tests:
            discriminant = sub(ONE, K.mul(y, y))
            root = K.sqrt(discriminant)
            require(root is None or K.mul(root, root) == discriminant, "bad field root")
            vertical_tests[y] = root
        root = vertical_tests[y]
        if root is None:
            continue
        eligible_classes += 1
        for signed_root in sorted({root, neg(root)}):
            t = K.div(sub(signed_root, x), y)
            require(add(K.mul(add(x, K.mul(t, y)), add(x, K.mul(t, y))), K.mul(y, y)) == ONE,
                    "root substitution")
            event_only.setdefault(t, set()).update(pair_list)
            contact_checks += len(pair_list)
    events = {t: tuple(sorted(edges | fixed)) for t, edges in event_only.items()}
    return tuple(sorted(fixed)), events, vertical_tests, {
        "pair_count": len(raw_points) * (len(raw_points) - 1) // 2,
        "signed_difference_classes": len(differences),
        "nonzero_y_values": len(vertical_tests),
        "root_eligible_difference_classes": eligible_classes,
        "field_events": len(events),
        "fixed_edges": len(fixed),
        "nonfixed_event_edge_incidences": contact_checks,
    }


def peel_and_colour(n, edges):
    """Bucketed minimum-degree deletion; no target heap implementation used."""
    adj = [set() for _ in range(n)]
    for a, b in edges:
        require(0 <= a < b < n, "edge domain")
        adj[a].add(b)
        adj[b].add(a)
    degrees = [len(row) for row in adj]
    buckets = [set() for _ in range(n)]
    for v, d in enumerate(degrees):
        buckets[d].add(v)
    alive = [True] * n
    order = []
    degeneracy = 0
    for _ in range(n):
        d = next(k for k, bucket in enumerate(buckets) if bucket)
        v = min(buckets[d])
        buckets[d].remove(v)
        alive[v] = False
        order.append(v)
        degeneracy = max(degeneracy, d)
        for u in adj[v]:
            if alive[u]:
                buckets[degrees[u]].remove(u)
                degrees[u] -= 1
                buckets[degrees[u]].add(u)
    colour = [-1] * n
    for v in reversed(order):
        forbidden = {colour[u] for u in adj[v] if colour[u] >= 0}
        colour[v] = next(c for c in range(degeneracy + 1) if c not in forbidden)
    require(all(colour[a] != colour[b] for a, b in edges), "invalid greedy colouring")
    return degeneracy, "".join(str(c) for c in colour)


def proper_on_labels(labels, label_edges, word, palette="0123"):
    require(len(labels) == len(word) and set(word) <= set(palette), "word format")
    colour = dict(zip(labels, word, strict=True))
    for a, b in label_edges:
        if a in colour and b in colour:
            require(colour[a] != colour[b], ("monochromatic", a, b))


def check_deletion_words(labels, zero_edges, core_cert):
    label_edges = [(labels[a], labels[b]) for a, b in zero_edges]
    old = json.loads(OLD_CERT.read_text())
    require(old["vertices"] == list(range(585)) and len(old["forced"]) == 451, "old certificate")
    library = {v: [old["forced_witness"][str(v)]] for v in old["forced"]}
    for row in json.loads(CATALOGUE.read_text()):
        if row["kind"] == "forced":
            require(row["index"] == len(library[row["key"]]), "catalogue indexing")
            library[row["key"]].append(row["witness"])
    checked = set()
    incidences = 0
    for vertex, index, append in core_cert["original_deletion_references"]:
        require(vertex in labels and vertex not in checked, "duplicate reference")
        if vertex == 606:
            require(index == "original122" and append is None, "q606 reference")
            colour = dict(zip([v for v in old["vertices"] if v != 122], library[122][0], strict=True))
        else:
            require(isinstance(index, int) and 0 <= index < len(library[vertex]), "reference index")
            require(append in "0123", "appended colour")
            colour = dict(zip([v for v in old["vertices"] if v != vertex], library[vertex][index], strict=True))
            colour[606] = append
        kept = [v for v in labels if v != vertex]
        proper_on_labels(kept, label_edges, "".join(colour[v] for v in kept))
        incidences += sum(vertex not in edge for edge in label_edges)
        checked.add(vertex)
    for key, word in core_cert["new_deletion_words"].items():
        vertex = int(key)
        require(vertex in labels and vertex not in checked, "duplicate literal word")
        proper_on_labels([v for v in labels if v != vertex], label_edges, word)
        incidences += sum(vertex not in edge for edge in label_edges)
        checked.add(vertex)
    require(checked == set(labels), "incomplete deletion cover")
    proper_on_labels(labels, label_edges, core_cert["five_colouring"], "01234")
    return len(checked), incidences


def phase_hash(events):
    original_events = sorted(original_basis(t) for t in events)
    data = "".join(",".join(str(F(x)) for x in t) + "\n" for t in original_events).encode()
    return sha256(data).hexdigest()


def event_edge_hash(events):
    rows = []
    for original_t, t in sorted((original_basis(t), t) for t in events):
        rows.append(",".join(str(F(x)) for x in original_t))
        rows.extend(f"{a},{b}" for a, b in events[t])
        rows.append(";")
    return sha256(("\n".join(rows) + "\n").encode()).hexdigest()


def run():
    paths = {
        "source/README.md": SOURCE / "README.md",
        "source/EXPECTED.json": SOURCE / "EXPECTED.json",
        "source/audit.cpp": SOURCE / "audit.cpp",
        "source/controls.py": SOURCE / "controls.py",
        "source/field.py": SOURCE / "field.py",
        "source/inputs.json": SOURCE / "inputs.json",
        "source/model.py": SOURCE / "model.py",
        "source/verify.py": SOURCE / "verify.py",
        "points": POINTS,
        "completions": COMPLETIONS,
        "core_cert": CORE_CERT,
        "old_cert": OLD_CERT,
        "catalogue": CATALOGUE,
    }
    for name, expected in PINS.items():
        require(digest(paths[name]) == expected, ("pin mismatch", name, digest(paths[name]), expected))
    for relative, expected in json.loads((SOURCE / "inputs.json").read_text()).items():
        require(digest(REPO / relative) == expected, ("source input pin mismatch", relative))

    raw_points, _, labels, core_cert = load_points_and_labels()
    fixed, events, vertical_tests, facts = enumerate_events(raw_points)
    require(Z in events, "missing zero event")
    require(ONE not in events, "the declared generic field test parameter is exceptional")
    zero_edges = events[Z]
    deletion_words, deletion_checks = check_deletion_words(labels, zero_edges, core_cert)

    generic_degree, generic_word = peel_and_colour(len(labels), fixed)
    require(generic_degree == 1 and all(generic_word[a] != generic_word[b] for a, b in fixed), "generic graph")
    degree_histogram = Counter()
    edge_histogram = Counter()
    words = []
    for original_t, t in sorted((original_basis(t), t) for t in events if t != Z):
        degree, word = peel_and_colour(len(labels), events[t])
        require(degree <= 3 and set(word) <= set("0123"), ("non-four event", original_t))
        degree_histogram[degree] += 1
        edge_histogram[len(events[t])] += 1
        words.append(word)

    # Definition-level arithmetic controls in the reversed tower.
    basis = [tuple(F(i == j) for i in range(8)) for j in range(8)]
    reverse_radicals = (1, 11, 5, 55, 3, 33, 15, 165)
    for i, a in enumerate(basis):
        for j, b in enumerate(basis):
            expected_product = scale(basis[i ^ j], reverse_radicals[i & j])
            require(K.mul(a, b) == expected_product, ("basis product", i, j))
    constructed = 0
    for i, j in combinations(range(8), 2):
        for a, b in product(range(-2, 3), repeat=2):
            x = add(scale(basis[i], a), scale(basis[j], b))
            square = K.mul(x, x)
            root = K.sqrt(square)
            require(root is not None and K.mul(root, root) == square, "constructed square")
            constructed += 1

    predecessor_manifest = json.loads((REPO / "hadwiger_nelson_point606_criticality_gate/manifest.json").read_text())
    point_hash = sha256(json.dumps(raw_points, separators=(",", ":")).encode()).hexdigest()
    label_edge_hash = sha256("".join(f"{labels[a]},{labels[b]}\n" for a, b in zero_edges).encode()).hexdigest()
    require(point_hash == predecessor_manifest["facts"]["point_sha256"], "predecessor point identity")
    require(label_edge_hash == predecessor_manifest["facts"]["edge_sha256"], "predecessor edge identity")

    result = {
        **facts,
        "points": len(labels),
        "zero_edges": len(zero_edges),
        "nonzero_events": len(events) - 1,
        "field_event_unit_edge_incidences": sum(len(edges) for edges in events.values()),
        "field_events_plus_generic_unit_edge_incidences": sum(len(edges) for edges in events.values()) + len(fixed),
        "nonzero_degeneracy_histogram": dict(sorted(degree_histogram.items())),
        "nonzero_edge_min": min(edge_histogram),
        "nonzero_edge_max": max(edge_histogram),
        "square_vertical_differences": sum(root is not None for root in vertical_tests.values()),
        "generic_degeneracy": generic_degree,
        "zero_deletion_words_checked": deletion_words,
        "zero_deletion_edge_checks": deletion_checks,
        "phase_sha256": phase_hash(events),
        "greedy_words_sha256": sha256(("\n".join(words) + "\n").encode()).hexdigest(),
        "event_edge_sha256": event_edge_hash(events),
        "constructed_square_controls": constructed,
        "basis_product_controls": 64,
        "point_sha256": point_hash,
        "zero_edge_sha256": label_edge_hash,
        "all_nonzero_field_events_four_colourable": True,
        "all_proper_zero_parameter_subsets_four_colourable": True,
        "status": "INDEPENDENT_EXACT_SHEAR_CENSUS_AND_POSITIVE_CERTIFICATES_PASS",
    }

    expected = json.loads((SOURCE / "EXPECTED.json").read_text())
    comparisons = {
        "pair_count": result["pair_count"],
        "signed_difference_classes": result["signed_difference_classes"],
        "nonzero_y_values": result["nonzero_y_values"],
        "root_eligible_difference_classes": result["root_eligible_difference_classes"],
        "field_events": result["field_events"],
        "fixed_edges": result["fixed_edges"],
        "points": result["points"],
        "zero_edges": result["zero_edges"],
        "nonzero_events": result["nonzero_events"],
        "nonzero_degeneracy_histogram": {str(k): v for k, v in result["nonzero_degeneracy_histogram"].items()},
        "nonzero_edge_min": result["nonzero_edge_min"],
        "nonzero_edge_max": result["nonzero_edge_max"],
        "generic_degeneracy": result["generic_degeneracy"],
        "zero_deletion_words_checked": result["zero_deletion_words_checked"],
        "zero_deletion_edge_checks": result["zero_deletion_edge_checks"],
        "phase_sha256": result["phase_sha256"],
        "greedy_words_sha256": result["greedy_words_sha256"],
    }
    for name, value in comparisons.items():
        require(value == expected[name], ("source mismatch", name, value, expected[name]))
    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
