"""Independent checks for the support-union theorem source."""

from hashlib import sha256
from itertools import combinations
from json import dumps
from math import comb
from random import Random

from construct import certificate, clique_packing_number, discriminant, support_threshold


def residue_discriminant(k: int) -> int:
    residue = k % 6
    if residue in (1, 3):
        numerator = k * k + 2 * k
    elif residue in (0, 2):
        numerator = k * k - 2 * k
    elif residue == 4:
        numerator = k * k - 2 * k - 8
    else:
        numerator = k * k + 2 * k - 32
    assert numerator % 3 == 0
    return numerator // 3


def direct_cover(k: int, neighborhoods: tuple[tuple[int, ...], ...]) -> tuple[int, bool]:
    active = tuple(n for n in neighborhoods if len(n) >= 2)
    support = set().union(*map(set, active)) if active else set()
    u = len(support)
    ell = max(u, k // 2)
    left = support | (set(range(k)) - support)
    left = set(sorted(left, key=lambda v: (v not in support, v))[:ell])
    deleted = {tuple(sorted(e)) for e in combinations(range(k), 2)
               if (e[0] in left) == (e[1] in left)}
    triangles = [tuple(sorted(t)) for t in combinations(range(k), 3)]
    for i, nhood in enumerate(neighborhoods):
        center = k + i
        triangles.extend((center, a, b) for a, b in combinations(nhood, 2))
    ok = True
    for tri in triangles:
        edges = {tuple(sorted(e)) for e in combinations(tri, 2)}
        if not edges & deleted:
            ok = False
            break
    return len(deleted), ok


def main() -> None:
    threshold_checks = 0
    for k in range(3, 20001):
        p = clique_packing_number(k)
        assert 3 * p <= comb(k, 2)
        assert discriminant(k) == residue_discriminant(k) >= 0
        threshold = support_threshold(k)
        assert threshold >= (k + 1) // 2
        probes = range(k + 1) if k <= 512 else {
            0, k // 2, (k + 1) // 2, threshold, min(k, threshold + 1), k
        }
        for u in probes:
            cert = certificate(k, u)
            assert cert["certifies_tuza"] == (u <= threshold)
            threshold_checks += 1

    rng = Random(20260922)
    graph_checks = 0
    records = []
    for k in range(3, 11):
        for _ in range(168):
            u = rng.randrange(support_threshold(k) + 1)
            support = tuple(sorted(rng.sample(range(k), u)))
            count = rng.randrange(1, 9)
            neighborhoods = []
            for _ in range(count):
                nhood = tuple(v for v in support if rng.randrange(2))
                neighborhoods.append(nhood)
            cover, ok = direct_cover(k, tuple(neighborhoods))
            assert ok
            actual_u = len(set().union(*(set(n) for n in neighborhoods if len(n) >= 2)))
            cert = certificate(k, actual_u)
            assert cover == cert["cover_size"]
            assert cert["certifies_tuza"]
            graph_checks += 1
            records.append((k, actual_u, cover, cert["clique_packing_size"]))

    binary_checks = 0
    for bits in (20, 40, 80, 160, 320, 640, 1000):
        k = (1 << bits) + 6 * bits + 3
        threshold = support_threshold(k)
        assert certificate(k, threshold)["certifies_tuza"]
        if threshold < k:
            assert not certificate(k, threshold + 1)["certifies_tuza"]
        binary_checks += 1

    digest = sha256(dumps(records, separators=(",", ":")).encode()).hexdigest()
    print({
        "threshold_checks": threshold_checks,
        "graph_checks": graph_checks,
        "binary_checks": binary_checks,
        "record_sha256": digest,
        "sample_k100": certificate(100, 78),
    })


if __name__ == "__main__":
    main()
