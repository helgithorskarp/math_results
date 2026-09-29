"""Cross-check coset construction, all-field coverage, and exhaustive search."""
import hashlib
import json
import random
from pathlib import Path
from certify import P, Exhaustive, direct_edges


def reduced_edges(m):
    # A discrete-log representation and scaling reduction, in contrast to
    # certify.py's explicit multiplicative cosets and all (a,d) enumeration.
    ids = [m] * P
    x = 1
    for e in range(P-1):
        ids[x] = e % m
        x = x * 3 % P
    base = {tuple(sorted({ids[(a+j)%P] for j in range(7)})) for a in range(P)}
    return sorted({sum(1 << v for v in {(w+t)%m if w < m else m for w in S}) for S in base for t in range(m)})


def brute(edges, n, assigned, ones):
    for colors in range(1 << n):
        if colors & assigned != ones:
            continue
        if all(mask & colors and mask & ~colors for mask in edges):
            return colors
    return None


def validate_search():
    rng = random.Random(617)
    checked = 0
    for n in range(1,9):
        for _ in range(24):
            edges = sorted({rng.randrange(1,1 << n) for _ in range(2*n)})
            assigned = rng.randrange(1 << n)
            ones = rng.randrange(1 << n) & assigned
            expected = brute(edges,n,assigned,ones)
            actual = Exhaustive(100000).run(edges,assigned,ones)
            assert (expected is None) == (actual is None)
            if actual is not None:
                A,T = actual
                assert T & assigned == ones and assigned & ~A == 0
                assert all(S & T and S & (A ^ T) for S in edges)
            checked += 1
    return checked


def check_colors(colors, cyclic=False):
    n = len(colors)
    checked = 0
    for d in range(1,n if cyclic else (n-1)//6+1):
        for a in range(n if cyclic else n-6*d):
            checked += 1
            positions = [(a+j*d)%n if cyclic else a+j*d for j in range(7)]
            if all(colors[t] == colors[positions[0]] for t in positions[1:]):
                raise AssertionError(('monochromatic progression',a,d,positions))
    return checked


def main():
    assert all(P % d for d in range(2,25))
    assert len({pow(3,j,P) for j in range(P-1)}) == P-1
    regressions = validate_search()
    records = []
    expected = json.loads(Path(__file__).with_name('expected.json').read_text())
    for m in (8,28,44):
        direct,ids = direct_edges(m)
        reduced = reduced_edges(m)
        assert direct == reduced  # Entry-level comparison, not aggregate counts.
        digest = hashlib.sha256('\n'.join(map(str,direct)).encode()).hexdigest()
        assert digest == next(r['direct_edge_masks_sha256'] for r in expected if r['m']==m)
        records.append({'m':m,'edge_sets_identical':True,'full_edges':len(direct)})
    # Brute force every 8-coset coloring, independent of the branching search.
    edges,ids = direct_edges(8)
    nz = [S for S in edges if not S & (1 << 8)]
    admissible = [v for v in range(256) if all(S & v and S & ~v for S in nz)]
    assert admissible == [85,170]
    qr = [int(pow(i,308,P) != 1) for i in range(P)]
    cyclic_checks = 0
    for z in (0,1):
        qr[0] = z
        cyclic_checks += check_colors(qr,cyclic=True)
    incumbent = [qr[i%P] for i in range(3703)]
    for j in range(7):
        incumbent[j*P] = int(j==6)
    interval_checks = check_colors(incumbent)
    digest = hashlib.sha256(''.join(map(str,incumbent)).encode()).hexdigest()
    assert digest == 'a27ec1e5f03030b2e88f0e5d7b493a8cd18976bbdbce94a0043f95b2823da83f'
    print(json.dumps({'exhaustive_search_regressions':regressions,'edge_crosschecks':records,
                     'm8_all_admissible_masks':admissible,'qr_cyclic_progressions_checked':cyclic_checks,
                     'incumbent_interval_progressions_checked':interval_checks,'incumbent_bits_sha256':digest},sort_keys=True))


if __name__ == '__main__':
    main()
