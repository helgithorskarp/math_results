"""Independent exact readout and charge audit, six-reviewer-5.

No author modules, solvers, or search certificates are imported. The unchanged
classified nineteen-star manifest is credited input, not reclassified here.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import argparse
import json
import random
import resource
import time

HERE = Path(__file__).resolve().parent
MANIFEST_SHA = '83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':')) + '\n').encode()


def digest(obj):
    return sha256(encode(obj)).hexdigest()


def literal_mark(mi, ci, u, blocks):
    require(len(blocks) == len(set(blocks)) == 19, 'nineteen distinct blocks')
    require(all(len(b) == len(set(b)) == 4 and all(type(a) is int and 0 <= a < 17 for a in b)
                for b in blocks), 'literal block domain')
    require(all(len(set(b) & set(d)) <= 1 for b, d in combinations(blocks, 2)), 'repeated pair')
    require(type(u) is int and 0 <= u < 17, 'hub domain')
    rho = [sum(a in b for b in blocks) for a in range(17)]
    require(rho[u] == 5 and sum(rho) == 76 and max(rho) <= 5, 'marked replication')
    low = [a for a in range(17) if rho[a] == 5]
    high = [a for a in range(17) if a not in low]
    # Construct each uncovered pair directly from the literal words.
    leave = [(a, b) for a, b in combinations(range(17), 2)
             if not any(a in w and b in w for w in blocks)]
    require(len(leave) == 22, 'exact leave size')
    neighbor = {a: [b for b in range(17) if tuple(sorted((a, b))) in leave] for a in low}
    require(all(len(v) == 1 for v in neighbor.values()), 'low leaves are unique')
    x = neighbor[u][0]
    C = sorted({a for w in blocks if u in w for a in w if a != u})
    require(C == sorted(set(range(17)) - {u, x}), 'all fifteen covered tails')
    ll = [list(e) for e in leave if set(e) <= set(low)]
    require(len({a for e in ll for a in e}) == 2 * len(ll), 'low-low matching')
    mu, j, p = len(ll), int(x in low), len(high)
    require(mu in (1, 2), 'positive-mu classification scope')
    friends = [[y, [a for a in low if a != u and neighbor[a] == [y]]] for y in high]
    friends = [[y, a] for y, a in friends if a]
    require(all(a in C for y, aa in friends for a in aa), 'every friend is covered')
    q = sum(len(aa) for y, aa in friends)
    require(q == 16 - p - 2 * mu + j, 'classification-free friend identity')
    require(len({a for y, aa in friends for a in aa}) == q, 'distinct friends')
    return dict(model=mi, **{'class': ci}, u=u, x=x,
                blocks=sorted(sum(1 << a for a in w) for w in blocks), rho=rho,
                low=low, W=high, C=C, W_C=[a for a in high if a in C],
                q=[[y, len(aa)] for y, aa in friends], friends=friends,
                low_low_pairs=ll, sat_low_low=[e for e in ll if u not in e],
                mu=mu, j=j, p=p, k=sum(a in C for a in high),
                heavy_v=[a for a in high if rho[a] == 3])


def reconstruct():
    raw = (HERE / 'NINETEEN_STARS.json').read_bytes()
    require(sha256(raw).hexdigest() == MANIFEST_SHA, 'manifest integrity')
    data = json.loads(raw)
    rows = []
    for mi, model in enumerate(data['models']):
        holes, offset = set(), 0
        for length in model['cycle_half_lengths']:
            for k in range(length):
                holes |= {(offset+k, offset+k), (offset+k, offset+(k+1) % length)}
            offset += length
        require(offset == 5, 'five-row anchor')
        cells = sorted(set(product(range(5), repeat=2)) - holes)
        anchors = [tuple(sorted([15] + [i for i, (r, c) in enumerate(cells) if r == a]))
                   for a in range(5)]
        anchors += [tuple(sorted([16] + [i for i, (r, c) in enumerate(cells) if c == a]))
                    for a in range(5)]
        candidates = [b for b in combinations(range(15), 4)
                      if all(len(set(b) & set(a)) <= 1 for a in anchors)]
        require(len(candidates) in (95, 96), 'anchor candidate rank domain')
        for ci, entry in enumerate(model['marked_classes']):
            require(len(entry['clique']) == len(set(entry['clique'])) == 9, 'nine extra blocks')
            blocks = tuple(anchors + [candidates[k] for k in entry['clique']])
            for u in range(17):
                if sum(u in b for b in blocks) == 5:
                    rows.append(literal_mark(mi, ci, u, blocks))
    require(len(rows) == 381, 'all classified low hub marks')
    return rows


def inventories(rows):
    raw, cut = [], []
    for row in rows:
        # Subset convolution carries its literal T_C selection and its full
        # charge. z is obtained from the derived exact allowable interval.
        charge = dict(row['q'])
        states = [((), 0)]
        for y in row['W_C']:
            old = states
            states = old + [(tc + (y,), extra + max(charge.get(y, 0), 2) - charge.get(y, 0))
                            for tc, extra in old]
        base = sum(charge.values())
        z_domain = len(set(row['low']) & set(row['C']))
        for tc, extra in states:
            c, Q = len(tc), base + extra
            for X in range(3):
                z_max = min(5, z_domain, 5-c-2*X, 5+c-2*X-Q)
                for z in range(z_max+1):
                    entry = [row['model'], row['class'], row['u'], X, list(tc), z, Q, 5+c-z-2*X]
                    raw.append(entry)
                    if X >= row['mu'] - row['j']:
                        cut.append(entry)
    return sorted(raw, key=encode), sorted(cut, key=encode)


def discharge(rows, cut):
    lookup = {(r['model'], r['class'], r['u']): r for r in rows}
    exceptional, flat = [], 0
    for entry in cut:
        row = lookup[tuple(entry[:3])]
        X, tc, z, Q, R = entry[3:]
        if X == 0:
            # No classification assumption is used in this dual contradiction.
            mu, j = row['mu'], row['j']
            require(mu <= j and j in (0, 1), 'sharp67 forbids flat saturated low-low edges')
            require(4*mu - 2*j < 4 + z, 'flat branch has strictly positive dual obstruction')
            flat += 1
            continue
        require(X == 1 and row['mu'] == 1 and row['j'] == z == 0 and R == Q,
                'positive-excess exceptional domain')
        heavy = row['sat_low_low']
        require(len(heavy) == 1, 'one mandatory heavy edge consumes all excess')
        endpoints = set(heavy[0])
        friends = dict(row['friends'])
        require(all(not endpoints & set(aa) for aa in friends.values()), 'friends avoid heavy endpoints')
        require(not endpoints & set(tc), 'covered T centers have unit internal deficits')
        candidates = [y for y in tc if row['rho'][y] == 4 and len(friends.get(y, [])) >= 2]
        require(candidates, 'extra two-charge local-lemma center')
        y = min(candidates)
        allocated = max(len(friends[y]), 2)
        required = len(friends[y]) + 2
        require(required > allocated and R == Q, 'strict exceptional contradiction')
        exceptional.append(dict(inventory=entry, center=y, friends=friends[y],
                                heavy_edge=sorted(endpoints), allocated=allocated, required=required))
    require(flat == 700 and len(exceptional) == 5, 'complete finite discharge')
    return dict(flat=flat, exceptions=exceptional)


def charge_controls():
    local = 0
    for q in range(17):
        for bad in range(q+1):
            minimum = q+2 if bad < q else max(q, 2)
            require(minimum >= q+2-bad, 'unit covered-T weakening')
            local += 1
    scalar, excluded, positive_excess_zero_mu = 0, 0, 0
    for p, mu, j, c, z in product(range(10), range(9), range(2), range(6), range(6)):
        if mu < j or 2*mu > 17-p or c+z > 5:
            continue
        q = 16-p-2*mu+j
        if q < 0:
            continue
        R = 5-z+c
        first = R-q
        second = R-(q+2*c-z-2*(9-p))
        require(first+second == 4*mu-2*j-4-z, 'exact dual coefficient identity')
        scalar += 1
        if mu <= j:
            require(first+second < 0, 'classification-free flat exclusion')
            excluded += 1
    for p, X, c, z in product(range(10), range(1, 3), range(6), range(6)):
        if c+z+2*X > 5:
            continue
        R, q = 5-z+c-2*X, 16-p
        require(R <= 6 < q, 'zero-mu positive excess exclusion')
        positive_excess_zero_mu += 1
    return dict(local_cost_checks=local, exact_dual_checks=scalar,
                flat_scalar_exclusions=excluded, zero_mu_positive_excess=positive_excess_zero_mu)


def controls(rows, raw, cut):
    rejected = []
    row = rows[0]
    blocks = tuple(tuple(a for a in range(17) if mask >> a & 1) for mask in row['blocks'])
    def reject(name, function):
        try:
            function()
        except (ValueError, KeyError, IndexError, TypeError):
            rejected.append(name)
            return
        raise ValueError('negative control accepted: ' + name)
    reject('missing word', lambda: literal_mark(0, 0, row['u'], blocks[:-1]))
    reject('repeated word', lambda: literal_mark(0, 0, row['u'], blocks[:-1]+blocks[:1]))
    reject('out of range hub', lambda: literal_mark(0, 0, 17, blocks))
    reject('high hub', lambda: literal_mark(0, 0, row['W'][0], blocks))
    reject('out of range point', lambda: literal_mark(0, 0, row['u'], blocks[:-1]+((0, 1, 2, 17),)))
    reject('missing flat inventory', lambda: discharge(rows, cut[1:]))
    bad = [list(s) for s in cut]
    exceptional = next(i for i, s in enumerate(bad) if s[3] == 1)
    bad[exceptional][7] += 1
    reject('false exhausted budget', lambda: discharge(rows, bad))
    return rejected


def relabel_controls(rows):
    rng = random.Random(8820)
    for r in rows:
        g = list(range(17))
        rng.shuffle(g)
        blocks = tuple(tuple(sorted(g[a] for a in range(17) if mask >> a & 1)) for mask in r['blocks'])
        moved = literal_mark(r['model'], r['class'], g[r['u']], blocks)
        require(all(moved[k] == r[k] for k in ('mu', 'j', 'p', 'k')), 'mark statistics under relabeling')
        for k in ('low', 'W', 'C', 'W_C', 'heavy_v'):
            require(moved[k] == sorted(g[a] for a in r[k]), 'actual point set under relabeling')
        require(moved['x'] == g[r['x']] and moved['rho'] == [r['rho'][g.index(i)] for i in range(17)],
                'outside point and replications under relabeling')
        require(moved['friends'] == sorted([[g[y], sorted(g[a] for a in aa)] for y, aa in r['friends']]),
                'actual friends under relabeling')
        for k in ('low_low_pairs', 'sat_low_low'):
            require(moved[k] == sorted(sorted(g[a] for a in e) for e in r[k]), 'matching under relabeling')
    return dict(seed=8820, arbitrary_point_relabelings=len(rows))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path)
    parser.add_argument('--details', type=Path)
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    start = time.monotonic()
    rows = reconstruct()
    raw, cut = inventories(rows)
    proof = discharge(rows, cut)
    exact = dict(agent='six-reviewer-5', role='independent mathematical reviewer',
                 manifest_sha256=MANIFEST_SHA, marks=len(rows), raw_count=len(raw), cut_count=len(cut),
                 carrier_sha256=digest(rows), raw_sha256=digest(raw), cut_sha256=digest(cut),
                 discharge=proof, charge_checks=charge_controls(), negative_controls=controls(rows, raw, cut),
                 relabel_controls=relabel_controls(rows),
                 types=[[list(k), n] for k, n in sorted(Counter((r['mu'], r['j'], r['p']) for r in rows).items())])
    if args.write_expected:
        (HERE / 'EXPECTED.json').write_bytes(encode(exact))
    else:
        require(exact == json.loads((HERE / 'EXPECTED.json').read_text()), 'complete exact readout differs')
    if args.details:
        args.details.write_bytes(encode(dict(rows=rows, raw=raw, cut=cut)))
    result = dict(status='COMPLETE', exact_sha256=digest(exact), exact=exact,
                  seconds=time.monotonic()-start, peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if args.out:
        args.out.write_bytes(encode(result))
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
