"""Literal calibration of the original inventory, CRT grid, group and lift."""
import hashlib
from itertools import product
import json
from math import gcd
import struct
from grid import PERIOD, PREFIX, affine_partition, coordinates, need


def run():
    physical, required, labels, masks = coordinates()
    rset = set(required)
    literal = {x for x in range(PERIOD) if x % 8 != 4}
    for n, a in PREFIX:
        literal.difference_update(range(a, PERIOD, n))
    need(literal == rset, "AP and CRT required-set equality")
    index = {x: i for i, x in enumerate(required)}
    classes = memberships = 0
    all_masks = hashlib.sha256()
    for n in labels:
        for a in range(n):
            ap = set(range(a, PERIOD, n)) & literal
            decoded = {x for x, i in index.items() if (masks[n][a] >> i) & 1}
            need(ap == decoded, "every original phase, literal point equality")
            memberships += len(ap)
            classes += 1
            all_masks.update(struct.pack("<HH", n, a))
            all_masks.update(struct.pack("<" + str(len(ap)) + "H", *sorted(ap)))
    maps, orbits = affine_partition()
    mset = set(maps)
    need(len(maps) == 288 and len(orbits) == 60, "entire group and pair partition")
    need((1, 0) in mset, "identity")
    for u, v in maps:
        inv = pow(u, -1, PERIOD)
        need((inv, -inv * v % PERIOD) in mset, "group inverse")
        need((4 * u + v) % 8 == 4, "parent four preservation")
        need({(u * x + v) % PERIOD for x in required} == rset,
             "full physical required-point transport")
        for w, z in maps:
            need((u * w % PERIOD, (u * z + v) % PERIOD) in mset,
                 "group closure")
    tail = tuple(n for n in range(8, 10081) if 10080 % n == 0
                 and n not in labels and n not in {n for n, _ in PREFIX})
    odd = tuple(d for d in range(1, 316) if 315 % d == 0)
    need(set(tail) == {16 * d for d in odd} | {32 * d for d in odd},
         "all original tail labels, no omissions or aliases")
    fibre_hash = hashlib.sha256()
    fibres = 0
    for n in tail:
        expected = 2 if n % 32 else 1
        for x in range(PERIOD):
            phases = [(x + PERIOD * j) % n for j in range(4)]
            counts = {a: phases.count(a) for a in set(phases)}
            need(set(counts.values()) == {expected}, "every nonempty tail/lift incidence")
            need(all(a % 8 == x % 8 for a in phases), "one actual mod8 parent")
            need(gcd(n, PERIOD) * (4 // expected) == n,
                 "exact period of the four lifted points")
            fibre_hash.update(struct.pack("<6H", n, x, *phases))
            fibres += 1
    # All completions of a small analogue. No assumption that maxima coexist.
    small_r = {1, 2, 4, 5, 7, 8, 10}
    small_labels = (2, 3, 4, 6, 12)
    worst = {}
    for phases in product(*(range(n) for n in small_labels)):
        actual = set()
        for n, a in zip(small_labels, phases):
            actual |= small_r & set(range(a, 12, n))
        key = phases[:2]
        worst[key] = max(worst.get(key, 0), len(actual))
    slack = []
    for p in product(range(2), range(3)):
        covered = small_r & (set(range(p[0], 12, 2)) | set(range(p[1], 12, 3)))
        residual = small_r - covered
        bound = len(covered) + sum(max(len(residual & set(range(a, 12, n)))
                                     for a in range(n)) for n in small_labels[2:])
        need(bound >= worst[p], "literal exhaustive union-bound calibration")
        slack.append(bound - worst[p])
    need(max(slack) > 0, "independent maxima are a genuine relaxation")
    # These physical controls distinguish parent, phase, and original ownership.
    wrong_prefix = tuple((n, 3 if n == 12 else a) for n, a in PREFIX)
    wrong_r = set(coordinates(prefix=wrong_prefix)[1])
    need(wrong_r != rset, "different phase12 prefix is not this theorem")
    need(21 in labels and 16 not in labels and 32 not in labels,
         "retain original21; do not spend original16/32 in BASE")
    need(any(x % 8 == 4 and all(x % n != a for n, a in PREFIX)
             for x in range(PERIOD)), "excluded-parent points exist")
    # Explicit incidence sharpness, not a BASE realization or full cover.
    x = min(required)
    lifts = tuple(x + PERIOD * j for j in range(4))
    first = x % 16
    second = next(a for a in range(48)
                  if {z for z in lifts if z % 48 == a} ==
                     {z for z in lifts if z % 16 != first})
    need(all(z % 16 == first or z % 48 == second for z in lifts),
         "two distinct valuation-four original labels can clear one fibre")
    return {"required_count": len(required), "original_labels": list(labels),
            "literal_classes": classes, "literal_class_memberships": memberships,
            "literal_masks_sha256": all_masks.hexdigest(),
            "affine_maps": len(maps), "pair_orbits": orbits,
            "group_products": len(maps) ** 2,
            "physical_required_transports": len(maps) * len(required),
            "tail_labels": list(tail), "literal_four_lift_fibres": fibres,
            "tail_fibres_sha256": fibre_hash.hexdigest(),
            "small_analogue_completions": 2 * 3 * 4 * 6 * 12,
            "small_analogue_slacks": slack,
            "abstract_two_tail_fibre": {"x": x, "lifts": list(lifts),
                "classes": [[16, first], [48, second]], "BASE_realization_claimed": False}}


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, separators=(",", ":")))
