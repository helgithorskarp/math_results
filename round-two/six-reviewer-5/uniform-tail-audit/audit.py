"""Independent raw M/S carrier audit of committed8947; six-reviewer-5.

No author producer, verifier, certificate or supplied group is imported.
local_pair is this reviewer's previously published full-carrier routine.
The generic 23-fixture coverage is a credited, separately reviewed premise.
"""
from collections import Counter
from hashlib import sha256
from itertools import permutations
from pathlib import Path
import argparse
import json
import resource
import time

from local_pair import (FIXTURE_SHA, Incomplete, compatible_maps, encode,
                        positive_control, require, star, two_charge_control)

HERE = Path(__file__).resolve().parent


def domains():
    raw = (HERE/'TWENTY_STARS.json').read_bytes()
    require(sha256(raw).hexdigest() == FIXTURE_SHA, 'fixture integrity')
    data = json.loads(raw)
    require(len(data['stars']) == 23, 'generic fixture count')
    stars, first, mixed, single = [], [], [], []
    for i, row in enumerate(data['stars']):
        words, rho, high, leave, core = star(row)
        stars.append(words)
        def covered(a, b):
            return frozenset((a, b)) not in leave
        for u in sorted(high):
            if rho[u] in (3, 4) and all(u not in e for e in core) and all(rho[a] == 4 for a in high-{u}):
                for a in sorted(high-{u}):
                    for v in range(17):
                        if rho[v] == 5 and not covered(a, v):
                            first.append((i, u, a, v))
        for u, v, b in permutations(range(17), 3):
            if rho[b] != 4 or not covered(u, b) or not covered(u, v) or covered(v, b):
                continue
            eu = sum(u in e for e in core)
            if rho[u] == 4 and rho[v] == 3 and eu == 0 and all(rho[a] == 4 for a in high-{v}):
                mixed.append((i, u, v, b, eu))
            if rho[u] < 5 and rho[v] == 5 and eu == 1 and all(rho[a] == 4 for a in high-{u}):
                single.append((i, u, v, b, eu))
    require(len(first) == 14 and len(mixed) == 2 and len(single) == 231,
            'full raw mark counts, not orbit representatives')
    return stars, sorted(first), sorted(mixed), sorted(single)


def relabel(words, p):
    return tuple(frozenset(p[a] for a in w) for w in words)


def guards_and_covariance(stars, first, mixed):
    f, s = first[0], mixed[0]
    Q, P = stars[f[0]], stars[s[0]]
    base = compatible_maps(Q, P, f, s)
    # Two unrelated complete label changes; no star automorphism assumption.
    q = [(5*a+3) % 17 for a in range(17)]
    p = [(7*a+6) % 17 for a in range(17)]
    fp = (f[0], q[f[1]], q[f[2]], q[f[3]])
    sp = (s[0], p[s[1]], p[s[2]], p[s[3]], s[4])
    changed = compatible_maps(relabel(Q, q), relabel(P, p), fp, sp)
    require(not changed['solutions'] and changed['full_maps'] == base['full_maps'] and
            changed['collision_maps'] == base['collision_maps'], 'independent label covariance')
    rejected = []
    for name, kwargs, error in [('zero nodes', {'nodes':0}, Incomplete),
                               ('excess nodes', {'nodes':200001}, ValueError),
                               ('excess seconds', {'seconds':11}, ValueError)]:
        try:
            compatible_maps(Q, P, f, s, **kwargs)
        except error:
            rejected.append(name)
        else:
            raise ValueError('bad local resource guard accepted')
    damaged = json.loads((HERE/'TWENTY_STARS.json').read_text())['stars'][0]
    damaged[1] = damaged[0][:]
    try:
        star(damaged)
    except ValueError:
        rejected.append('duplicate fixture word')
    else:
        raise ValueError('damaged fixture accepted')
    return dict(label_changes=2, full_maps=base['full_maps'], rejections=rejected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path)
    parser.add_argument('--records', type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    stars, first, mixed, single = domains()
    records, summary = [], {}
    for tag, second in [('M',mixed), ('S',single)]:
        total, nodes, peak, rejects = 0, 0, 0, Counter()
        for f in first:
            for s in second:
                if time.monotonic()-started > 180:
                    raise Incomplete('INCOMPLETE bounded whole raw audit')
                r = compatible_maps(stars[f[0]], stars[s[0]], f, s)
                require(not r['solutions'], 'literal counterexample to local '+tag)
                records.append(dict(lemma=tag, first=list(f), second=list(s), **r))
                total += r['full_maps']
                nodes += r['nodes']
                peak = max(peak,r['nodes'])
                rejects.update(r['prunes'])
        summary[tag] = dict(second_marks=len(second), cases=len(first)*len(second),
                            full_maps=total, nodes=nodes, max_case_nodes=peak,
                            pruning_stages=dict(sorted(rejects.items())))
    exact = dict(agent='six-reviewer-5', role='independent mathematical reviewer',
                 fixture_sha256=FIXTURE_SHA, first_marks=[list(f) for f in first],
                 M_marks=[list(s) for s in mixed], S_marks=[list(s) for s in single],
                 records=records, positive=positive_control(),
                 two_charge=two_charge_control(), covariance=guards_and_covariance(stars,first,mixed))
    digest = sha256(encode(exact)).hexdigest()
    if (HERE/'EXPECTED.json').exists():
        expected = json.loads((HERE/'EXPECTED.json').read_text())
        require(expected['exact_sha256'] == digest and expected['lemmas'] == summary,
                'frozen independently recorded output changed')
    result = dict(status='COMPLETE', exact_sha256=digest, first_marks=len(first),
                  lemmas=summary, positive=exact['positive'], two_charge=exact['two_charge'],
                  covariance=exact['covariance'], seconds=time.monotonic()-started,
                  peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if args.records:
        args.records.write_bytes(encode(exact))
    if args.out:
        args.out.write_bytes(encode(result))
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
