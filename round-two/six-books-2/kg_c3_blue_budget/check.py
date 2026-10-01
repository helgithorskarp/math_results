"""Rebuild the pair-clique cover, match every native labeled case and controls."""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
from itertools import combinations
import json
from math import comb
from pathlib import Path
import model as m


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def maximal_cliques(adj):
    """Bron--Kerbosch; differs from the producer's fixed-size ordered DFS."""
    neighbors = [{j for j in range(len(adj)) if row >> j & 1} for row in adj]
    def visit(R, P, X):
        if not P and not X:
            yield tuple(sorted(R))
            return
        pivot = max(P | X, key=lambda u: len(P & neighbors[u])) if P | X else None
        for v in sorted(P - (neighbors[pivot] if pivot is not None else set())):
            yield from visit(R | {v}, P & neighbors[v], X & neighbors[v])
            P.remove(v)
            X.add(v)
    yield from visit(set(), set(range(len(adj))), set())


def critical_keys(adj, target):
    return {tuple(C) for clique in maximal_cliques(adj) for C in combinations(clique, target)}


def verify_local(g, record):
    p, pool, adj = record['promotions'], record['pool'], record['compatibility']
    m.need(p in (1, 2) and pool == sorted(set(pool)) and all(type(d) is int and 0 <= d < 35 for d in pool), 'pool domain')
    m.need(type(record['base_blue_valid']) is bool and len(adj) == len(pool), 'pair domain shape')
    for i, row in enumerate(adj):
        m.need(type(row) is int and 0 <= row < 1 << len(pool) and not row >> i & 1, 'pair row range/diagonal')
        m.need(all((row >> j & 1) == (adj[j] >> i & 1) for j in range(len(adj))), 'pair symmetry')
    keys = critical_keys(adj, 2*p+2)
    supplied = []
    for critical in record['critical']:
        D = critical['deletions']
        m.need(D == sorted(set(D)) and len(D) == 2*p+2 and set(D) <= set(pool), 'critical subset domain')
        supplied.append(tuple(pool.index(d) for d in D))
        u, v, pages = critical['violation']
        rows = m.literal(g, record['joins'], record['additions'], D)
        actual = sorted(w for w in range(22) if w not in (u, v) and w not in rows[u] and w not in rows[v])
        m.need(u < v and v not in rows[u] and pages == actual and len(actual) > 6, 'literal blue-book witness')
    m.need(len(supplied) == len(set(supplied)) and set(supplied) == keys, 'complete critical clique cover')


def expanded_cases(g, records):
    tasks = [(p, J, P, w) for p in (1, 2) for J, P, w in m.choices(g, p)]
    m.need(len(records) == len(tasks), 'producer case coverage')
    maps = m.centralizer(g)
    expanded = {1: {}, 2: {}}
    for record, (p, J, P, weight) in zip(records, tasks):
        m.need(record['promotions'] == p and record['joins'] == list(J) and record['additions'] == list(P)
               and record['multiplicity'] == weight, 'producer case/order/weight')
        verify_local(g, record)
        transports = maps if p == 2 else [(tuple(range(7)), tuple(range(35)), tuple(range(35)))]
        for vertex, red, blue in transports:
            key = (tuple(sorted(vertex[i] for i in J)), tuple(sorted(blue[i] for i in P)))
            mapped_pool = sorted(red[d] for d in record['pool'])
            location = {d: i for i, d in enumerate(mapped_pool)}
            pair_rows = [0]*len(mapped_pool)
            for i, d in enumerate(record['pool']):
                for j, e in enumerate(record['pool']):
                    if record['compatibility'][i] >> j & 1:
                        pair_rows[location[red[d]]] |= 1 << location[red[e]]
            value = dict(base_blue_valid=record['base_blue_valid'], pool=mapped_pool, compatibility=pair_rows)
            if key in expanded[p]:
                m.need(expanded[p][key] == value, 'stabilizer/transport inconsistency')
            expanded[p][key] = value
    m.need(len(expanded[1]) == 1225 and len(expanded[2]) == 20825, 'complete labeled case expansion')
    return expanded


def native_check(native, expanded, p):
    choices = [(J, P) for J in combinations(range(7), 3) for P in combinations(range(35), p)]
    m.need(len(native) == len(choices), 'native coverage')
    for index, (record, (J, P)) in enumerate(zip(native, choices)):
        m.need(type(record['index']) is int and record['index'] == index and record['joins'] == list(J)
               and record['promotions'] == list(P), 'native case/index order')
        value = {k: record[k] for k in ('base_blue_valid', 'pool', 'compatibility')}
        m.need(value == expanded[J, P], 'entrywise native pool/pair mismatch')
        m.need(type(record['subsets']) is int and record['subsets'] == comb(len(record['pool']), 2*p+2), 'native raw subset coverage')
        m.need(type(record['blue_valid_subsets']) is int and record['blue_valid_subsets'] == 0
               and record['witnesses'] == [], 'native blue-budget counterexample')


def controls(g):
    labels, base, reds, blues = g
    kg = [{j for j in range(21) if row >> j & 1} for row in base]
    positive = []
    for J, P, D in (((0, 1, 5), (29,), (6, 8, 31)),
                    ((0, 1, 2), (26, 28), (8, 13, 17, 24, 25))):
        bits, sets = m.graph(g, J, P, D), m.literal(g, J, P, D)
        m.need(all(sets[u] == {v for v in range(22) if bits[u] >> v & 1} for u in range(22)), 'control constructors')
        summary = m.literal_summary(sets)
        m.need(not any(v[2] == 'blue' for v in summary['violations']) and any(v[2] == 'red' for v in summary['violations']), 'sharp blue-only control')
        action = [3*(u//3)+(u+1) % 3 for u in range(21)] + [21]
        m.need(all({action[v] for v in sets[u]} == sets[action[u]] for u in range(22)), 'control automorphism')
        positive.append(dict(joins=list(J), additions=list(P), deletions=list(D), summary=summary))
    path = Path(__file__).resolve().parent/'primary21.rows'
    content = path.read_bytes()
    m.need(hashlib.sha256(content).hexdigest() == '4f1dd2bc743590a0553107936656e469db6e7d742db0456d697353ce50aac5ec', 'primary fixture hash')
    lines = content.splitlines()
    m.need(len(lines) == 21 and all(len(line) == 21 and set(line) <= {48, 49} for line in lines), 'primary fixture shape')
    primary = m.literal_summary([{j for j, bit in enumerate(line) if bit == 49} for line in lines])
    m.need(primary['edges'] == 93 and not primary['violations'], 'primary positive control')
    return dict(KG=m.literal_summary(kg), primary21=primary, sharp_controls=positive,
                sharp_control_spines=462, KG_spines=210, primary21_spines=210)


def evaluate(records, native):
    g = m.geometry()
    expanded = expanded_cases(g, records)
    stats = {}
    for p in (1, 2):
        native_check(native[p], expanded[p], p)
        local = [r for r in records if r['promotions'] == p]
        stats[str(p)] = dict(representatives=len(local), labeled_cases=len(native[p]),
                            blue_admissible_representatives=sum(r['base_blue_valid'] for r in local),
                            blue_admissible_labeled_cases=sum(r['base_blue_valid'] for r in native[p]),
                            pool_histogram=dict(sorted(Counter(len(r['pool']) for r in local).items())),
                            raw_subsets_representatives=sum(comb(len(r['pool']), 2*p+2) for r in local),
                            raw_subsets_labeled=sum(r['subsets'] for r in native[p]),
                            critical_representatives=sum(len(r['critical']) for r in local),
                            critical_labeled=sum(r['multiplicity']*len(r['critical']) for r in local),
                            blue_valid_raw_subsets=0,
                            pool_pair_case_sha256=digest([[list(J), list(P), expanded[p][J, P]] for J, P in sorted(expanded[p])]),
                            critical_sha256=digest([[r['joins'], r['additions'], r['critical']] for r in local]))
    return json.loads(canonical(dict(schema=1, bounds={'one_promotion': 3, 'two_promotions': 5},
                                     stats=stats, controls=controls(g))))


def damage_controls(records, native):
    g = m.geometry()
    expanded = expanded_cases(g, records)
    rejected = []
    def reject(name, call):
        try:
            call()
        except (ValueError, KeyError, IndexError, TypeError):
            rejected.append(name)
        else:
            raise ValueError('damaged certificate accepted: '+name)
    reject('omitted native case', lambda: native_check(native[1][1:], expanded[1], 1))
    first = next(i for i, r in enumerate(native[1]) if r['pool'])
    def bad_native(field, value):
        altered = native[1][:]
        altered[first] = dict(altered[first], **{field: value})
        native_check(altered, expanded[1], 1)
    reject('changed valid-shape native pool', lambda: bad_native('pool', native[1][first]['pool'][1:]))
    altered_adj = native[1][first]['compatibility'][:]
    altered_adj[0] ^= 1
    reject('changed pair matrix', lambda: bad_native('compatibility', altered_adj))
    reject('forged native valid count', lambda: bad_native('blue_valid_subsets', 1))
    reject('Boolean native count', lambda: bad_native('subsets', True))
    record = next(r for r in records if r['critical'])
    missing = deepcopy(record)
    missing['critical'].pop()
    reject('missing critical subset', lambda: verify_local(g, missing))
    forged = deepcopy(record)
    forged['critical'][0]['violation'][2] = forged['critical'][0]['violation'][2][:-1]
    reject('forged literal pages', lambda: verify_local(g, forged))
    duplicate = deepcopy(record)
    duplicate['critical'].append(deepcopy(duplicate['critical'][0]))
    reject('duplicate critical subset', lambda: verify_local(g, duplicate))
    invalid = deepcopy(record)
    invalid['compatibility'][0] |= 1
    reject('pair diagonal', lambda: verify_local(g, invalid))
    loops = [set() for _ in range(22)]
    loops[0].add(0)
    reject('literal graph loop', lambda: m.literal_summary(loops))
    reject('duplicate deleted orbit', lambda: m.graph(g, (0, 1, 2), (0,), (1, 1)))
    return dict(rejected=rejected, count=len(rejected))


def load(work):
    producer, position = [], 0
    for path in sorted(work.glob('producer-*.json')):
        phase = json.loads(path.read_text())
        m.need(phase['first'] == position and phase['next'] == position+len(phase['records'])
               and phase['total'] == 4768, 'producer phase coverage')
        producer.extend(phase['records'])
        position = phase['next']
    m.need(position == 4768, 'producer incomplete')
    native = {}
    for p, total in ((1, 1225), (2, 20825)):
        records, position = [], 0
        for path in sorted(work.glob(f'native{p}-*.jsonl')):
            lines = [json.loads(line) for line in path.read_text().splitlines()]
            phase = lines[-1]
            m.need(phase.get('segment') is True and phase['first'] == position and phase['total'] == total
                   and phase['next'] == position+len(lines)-1, 'native phase coverage')
            records.extend(lines[:-1])
            position = phase['next']
        m.need(position == total, 'native incomplete')
        native[p] = records
    return producer, native


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    records, native = load(args.work)
    evidence = evaluate(records, native)
    if args.expected:
        m.need(args.expected.is_file(), 'frozen expected fixture absent')
        m.need(evidence == json.loads(args.expected.read_text()), 'entire frozen evidence mismatch')
    out = dict(evidence=evidence, frozen_fixture_compared=args.expected is not None)
    if args.controls:
        out['damage_controls'] = damage_controls(records, native)
    args.out.write_text(json.dumps(out, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(frozen_fixture_compared=out['frozen_fixture_compared'], stats=evidence['stats'],
                          damages=out.get('damage_controls')), sort_keys=True))
