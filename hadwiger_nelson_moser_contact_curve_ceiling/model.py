"""Exact contact-polynomial census for the independent three-Moser sum."""

from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import sys

DEPENDENCY = Path(__file__).resolve().parent.parent / "hadwiger_nelson_independent_moser_sum_collisions"
sys.path.insert(0, str(DEPENDENCY))

import arithmetic as K  # noqa: E402
from family import ONE, ZERO, add, inv, mul, norm, require, spindle, sub  # noqa: E402


def canonical(coefficients):
    """Normalize a nonzero Laurent polynomial up to an exact scalar."""
    first = next((coefficient for coefficient in coefficients if coefficient != ZERO), None)
    if first is None:
        return None
    reciprocal = inv(first)
    return tuple(mul(coefficient, reciprocal) for coefficient in coefficients)


def classify(differences):
    a, b, c = differences
    constant = sub(add(add(norm(a), norm(b)), norm(c)), ONE)
    p = mul(b, K.conj(a))
    q = mul(c, K.conj(a))
    r = mul(b, K.conj(c))
    if p == q == r == ZERO:
        return ("baseline" if constant == ZERO else "constant_noncontact"), None, None
    coefficients = (constant, p, K.conj(p), q, K.conj(q), r, K.conj(r))
    key = canonical(coefficients)
    metadata = (
        sum(displacement != ZERO for displacement in differences),
        all(displacement != ZERO and norm(displacement) == ONE for displacement in differences),
    )
    return "curve", key, metadata


def add_group(groups, key, metadata, weight):
    row = groups.setdefault(key, [0, metadata[0], metadata[1]])
    require(tuple(row[1:]) == metadata, "contact-class metadata invariant")
    row[0] += weight


def direct_inventory():
    """Enumerate all unordered formal point pairs directly."""
    M = spindle()
    addresses = list(itertools.product(range(7), repeat=3))
    groups = {}
    baseline = 0
    constant_noncontacts = 0
    for left, right in itertools.combinations(range(343), 2):
        differences = tuple(
            sub(M[addresses[left][axis]], M[addresses[right][axis]]) for axis in range(3)
        )
        kind, key, metadata = classify(differences)
        if kind == "baseline":
            baseline += 1
        elif kind == "constant_noncontact":
            constant_noncontacts += 1
        else:
            add_group(groups, key, metadata, 1)
    return baseline, constant_noncontacts, groups


def factorized_inventory():
    """Independently count ordered pairs by one-factor difference multiplicity."""
    M = spindle()
    differences = K.differences(M)
    groups = {}
    baseline = 0
    constant_noncontacts = 0
    for (a, pa), (b, pb), (c, pc) in itertools.product(differences.items(), repeat=3):
        if a == b == c == ZERO:
            continue
        directed_weight = len(pa) * len(pb) * len(pc)
        kind, key, metadata = classify((a, b, c))
        if kind == "baseline":
            baseline += directed_weight
        elif kind == "constant_noncontact":
            constant_noncontacts += directed_weight
        else:
            add_group(groups, key, metadata, directed_weight)
    require(baseline % 2 == constant_noncontacts % 2 == 0, "orientation parity")
    require(all(row[0] % 2 == 0 for row in groups.values()), "group orientation parity")
    return (
        baseline // 2,
        constant_noncontacts // 2,
        {key: [row[0] // 2, row[1], row[2]] for key, row in groups.items()},
    )


def serial_element(element):
    return [str(coefficient) for coefficient in element]


def serial_inventory(groups):
    return [
        {
            "key": [serial_element(coefficient) for coefficient in key],
            "multiplicity": row[0],
            "active_factors": row[1],
            "unit_triple": row[2],
        }
        for key, row in sorted(groups.items())
    ]


def summarize(baseline, constant_noncontacts, groups):
    distribution = Counter(row[0] for row in groups.values())
    all_three = Counter(row[0] for row in groups.values() if row[1] == 3)
    unit_triples = Counter(row[0] for row in groups.values() if row[2])
    admissible = Counter(row[0] for row in groups.values() if row[1] == 3 and not row[2])
    require(baseline + constant_noncontacts + sum(row[0] for row in groups.values()) == 58653, "pair partition")
    require(max(admissible) == 8, "admissible multiplicity ceiling")
    require(
        all(row[2] for row in groups.values() if row[1] == 3 and row[0] > 8),
        "every larger three-factor class must be a unit triple",
    )
    maximizers = sum(row[1] == 3 and not row[2] and row[0] == 8 for row in groups.values())
    stream = json.dumps(serial_inventory(groups), sort_keys=True, separators=(",", ":")).encode()
    return {
        "claim": "Every non-unit-triple three-factor contact-polynomial class in M+uM+vM has formal edge multiplicity at most eight",
        "formal_points": 343,
        "unordered_pairs": 58653,
        "baseline_edges": baseline,
        "constant_noncontacts": constant_noncontacts,
        "nonconstant_contact_classes": len(groups),
        "multiplicity_distribution": {str(k): distribution[k] for k in sorted(distribution)},
        "all_three_factor_distribution": {str(k): all_three[k] for k in sorted(all_three)},
        "unit_triple_distribution": {str(k): unit_triples[k] for k in sorted(unit_triples)},
        "admissible_three_factor_distribution": {str(k): admissible[k] for k in sorted(admissible)},
        "maximal_admissible_multiplicity": max(admissible),
        "maximal_admissible_classes": maximizers,
        "contact_inventory_sha256": hashlib.sha256(stream).hexdigest(),
    }
