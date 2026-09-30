"""Check ten integer phase inequalities and complete restricted repair sets.

Actual author six-covering-1, researcher. Python standard library only.
All sums use ordinary physical residues and phases. No LP, SAT, projected
capacity, CRT updater or construction heuristic is a proof dependency.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path


def physical_tables(N, B, C, moduli, f):
    if (N != B*C or math.gcd(B, C) != 1 or len(f) != B
            or any(type(w) is not int or w < 0 for w in f)
            or not max(f, default=0) or len(set(moduli)) != len(moduli)
            or any(type(m) is not int or m < 1 or N % m for m in moduli)):
        raise ValueError('Invalid weighted residue instance')
    physical = [f[x % B] for x in range(N)]
    coefs, maxima = {}, {}
    for m in moduli:
        # Each physical point contributes to exactly one ordinary phase.
        sums = [0] * m
        for x, w in enumerate(physical):
            sums[x % m] += w
        if m % C:
            if B % m or any(s % C for s in sums):
                raise ValueError('Base multiplicity differs')
            coefs[m] = sums
        else:
            maxima[m] = max(sums)
    cap = sum(maxima.values())
    totals = dict(base_weight_total=sum(f), full_weight_total=sum(physical),
                  tail_capacity=cap, weighted_gap=sum(physical)-cap,
                  max_weight=max(f), support_size=sum(w > 0 for w in f))
    return coefs, totals


def load(assignment, certificate):
    raw = assignment.read_bytes()
    rows = [tuple(map(int, line.split())) for line in raw.decode().splitlines()]
    obj = json.loads(certificate.read_text())
    N, B, C = obj['period'], obj['base_period'], obj['prime']
    if ((N, B, C) != (10080, 1440, 7)
            or any(type(x) is not int for x in (N, B, C))
            or obj['assignment_sha256'] != hashlib.sha256(raw).hexdigest()
            or [m for a, m in rows] != [m for m in range(8, N+1) if N % m == 0]
            or any(not 0 <= a < m for a, m in rows)
            or math.lcm(*(m for a, m in rows)) != N
            or len(obj['vectors']) != 10 or obj['vectors'][0]['target'] is not None):
        raise ValueError('Wrong specified complete assignment or vector set')
    targets = {(20, 4), (40, 32), (60, 46), (60, 58), (80, 32), (80, 72),
               (96, 1), (120, 72), (120, 84)}
    base = {m: a for a, m in rows if m % C}
    vectors = []
    seen = set()
    for j, rec in enumerate(obj['vectors']):
        target = None if rec['target'] is None else tuple(rec['target'])
        if j and (target not in targets or target in seen):
            raise ValueError('Missing, duplicate or extraneous trade vector')
        if target is not None:
            if any(type(x) is not int for x in target) or base[target[0]] == target[1]:
                raise ValueError('Invalid trade phase')
            seen.add(target)
        f = [0] * B
        previous = -1
        for pair in rec['nonzero_weights']:
            if not isinstance(pair, list) or len(pair) != 2:
                raise ValueError('Expected sorted integer point/weight pairs')
            z, w = pair
            if type(z) is not int or type(w) is not int or not previous < z < B or w < 1:
                raise ValueError('Invalid sparse integer weight')
            f[z], previous = w, z
        coefs, totals = physical_tables(N, B, C, [m for a, m in rows], f)
        if (set(rec['expected']) != set(totals)
                or any(type(v) is not int or totals[k] != v for k, v in rec['expected'].items())
                or totals['weighted_gap'] <= 0):
            raise ValueError('Exact certificate totals differ')
        specified = dict(base)
        if target is not None:
            specified[target[0]] = target[1]
        if sum(coefs[m][a] for m, a in specified.items()):
            raise ValueError('Vector has positive weight under its specified base')
        vectors.append(dict(target=target, coefs=coefs, **totals))
    if seen != targets:
        raise ValueError('Trade vector set incomplete')
    return rows, vectors


def uniform_gap(N, base, tails):
    covered = bytearray(N)
    for m, a in base.items():
        for x in range(a, N, m):
            covered[x] = 1
    physical = [int(not covered[x]) for x in range(N)]
    demand = sum(physical)
    cap = 0
    for m in tails:
        sums = [0] * m
        for x, w in enumerate(physical):
            sums[x % m] += w
        cap += max(sums)
    return demand-cap


def run(assignment, certificate):
    rows, vectors = load(assignment, certificate)
    N, C = 10080, 7
    base = {m: a for a, m in rows if m % C}
    tails = [m for a, m in rows if m % C == 0]
    if len(base) != 30 or len(tails) != 35 or base[80] != 59:
        raise ValueError('Wrong base/tail partition')
    literal_holes = sum(not any(x % m == a for a, m in rows) for x in range(N))
    if literal_holes != 87:
        raise ValueError('Specified near-cover differs')
    original = vectors[0]
    named = {v['target']: v for v in vectors[1:]}
    baseline = (original['weighted_gap']+original['max_weight']-1)//original['max_weight']
    single = dict(examined=0, original_cut_closed=0, uniform_closed=0, named_weight_closed=0,
                  minimum_hole_floor=baseline, maximum_original_R_among_cut_cases=0,
                  minimum_uniform_gap=N)
    uniform_cases = 0
    events = hashlib.sha256()
    for m, prior in base.items():
        for a in range(m):
            if a == prior:
                continue
            single['examined'] += 1
            deficit = original['weighted_gap']-original['coefs'][m][a]
            if deficit > 0:
                kind = 'original_cut_closed'
                floor = (deficit+original['max_weight']-1)//original['max_weight']
                single['maximum_original_R_among_cut_cases'] = max(
                    single['maximum_original_R_among_cut_cases'], original['coefs'][m][a]//C)
            else:
                changed = dict(base)
                changed[m] = a
                gap = uniform_gap(N, changed, tails)
                uniform_cases += 1
                if gap > 0:
                    kind, floor = 'uniform_closed', gap
                    single['minimum_uniform_gap'] = min(single['minimum_uniform_gap'], gap)
                else:
                    v = named.get((m, a))
                    if v is None:
                        raise ValueError('Unexcluded single trade')
                    deficit = v['weighted_gap']-sum(v['coefs'][n][b] for n, b in changed.items())
                    if deficit <= 0:
                        raise ValueError('Named trade weight failed')
                    kind = 'named_weight_closed'
                    floor = (deficit+v['max_weight']-1)//v['max_weight']
            single[kind] += 1
            single['minimum_hole_floor'] = min(single['minimum_hole_floor'], floor)
            events.update(json.dumps([m, a, kind, floor]).encode())
    if single != dict(examined=4863, original_cut_closed=4791, uniform_closed=63,
                      named_weight_closed=9, minimum_hole_floor=4,
                      maximum_original_R_among_cut_cases=21, minimum_uniform_gap=4):
        raise ValueError('Complete single-trade partition differs')
    anchored = dict(examined=0, weighted_closed=0, uniform_closed=0,
                    minimum_hole_floor=N, minimum_uniform_gap=N)
    anchor_vectors = [named[(80, a)] for a in (32, 72)]
    initial = [sum(v['coefs'][m][a] for m, a in base.items()) for v in anchor_vectors]
    for anchor in (32, 72):
        for m, prior in base.items():
            if m == 80:
                continue
            for a in range(m):
                if a == prior:
                    continue
                anchored['examined'] += 1
                for v, cost in zip(anchor_vectors, initial):
                    selected = (cost-v['coefs'][80][base[80]]+v['coefs'][80][anchor]
                                -v['coefs'][m][prior]+v['coefs'][m][a])
                    deficit = v['weighted_gap']-selected
                    if deficit > 0:
                        floor = (deficit+v['max_weight']-1)//v['max_weight']
                        anchored['weighted_closed'] += 1
                        break
                else:
                    changed = dict(base)
                    changed[80], changed[m] = anchor, a
                    floor = uniform_gap(N, changed, tails)
                    uniform_cases += 1
                    if floor <= 0:
                        raise ValueError('Unexcluded anchored two-trade case')
                    anchored['uniform_closed'] += 1
                    anchored['minimum_uniform_gap'] = min(anchored['minimum_uniform_gap'], floor)
                anchored['minimum_hole_floor'] = min(anchored['minimum_hole_floor'], floor)
                events.update(json.dumps([anchor, m, a, floor]).encode())
    if anchored != dict(examined=9568, weighted_closed=9546, uniform_closed=22,
                        minimum_hole_floor=6, minimum_uniform_gap=106):
        raise ValueError('Complete anchored two-trade partition differs')
    return dict(agent='six-covering-1', role='researcher', status='EXACT_PHYSICAL_CHECK_PASSED',
                period=N, baseline_hole_floor=baseline, literal_fixture_holes=literal_holes,
                vectors=[{k: v[k] for k in ('target', 'base_weight_total', 'tail_capacity',
                                          'weighted_gap', 'max_weight')} for v in vectors],
                single_base_changes=single, anchored_two_base_changes=anchored,
                physical_tail_phase_evaluations=(len(vectors)+uniform_cases)*sum(tails),
                assignment_sha256=hashlib.sha256(assignment.read_bytes()).hexdigest(),
                certificate_sha256=hashlib.sha256(certificate.read_bytes()).hexdigest(),
                events_sha256=events.hexdigest(),
                scope='Ten necessary cuts for any eligible cover. Zero/one base change'
                      ' leaves at least4 holes. Specified80anchor plus one other change'
                      ' leaves at least6 holes. All35 tails free; global10080 remains open.')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('assignment', type=Path)
    ap.add_argument('certificate', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    result = run(args.assignment, args.certificate)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
