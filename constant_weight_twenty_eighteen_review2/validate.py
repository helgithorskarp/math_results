"""Independent literal/reference/sanitizer checks and the six-triple application."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import resource
import time

from audit import controls, native, witness
from reference import point_first_covers
from exact import insist, bits, mask, pairs, encoded, packing
from domain import PAIRS


def verify_colors(words, colors):
    insist(sorted(w for c in colors for w in c) == sorted(words), 'color partition mismatch')
    insist(all(all((a & b).bit_count() >= 3 for a, b in combinations(c, 2)) for c in colors), 'same-color compatible pair')


def check_marked(record, p, old_words):
    t, r = record['triangle'], record['cover']
    owners = [line for line in p if line & t == t]
    insist(len(owners) == 1 and t.bit_count() == 3, 'marked triple not uniquely collinear')
    union = [w | 1 << 17 for w in p if w != owners[0]] + [t | 1 << 16 | 1 << 17]
    union += [w | 1 << 16 for w in r]
    packing(union, size=38)
    blocked = {mask(triple) for w in union for triple in combinations(tuple(bits(w)), 3)}
    # Independent candidate encoding: repeated triples, instead of word intersections.
    q = [w for w, triples in old_words if not any(triple in blocked for triple in triples)]
    insist(q == record['residual_candidates'], 'marked complete residual list differs')
    verify_colors(q, record['colors'])
    insist(len(record['colors']) <= 19, 'marked coloring bound exceeds19')


def transfer():
    v, a, b = 0, 1, 2
    cases, proofs = [], []
    for name in ('middle', 'end', 'triangle'):
        if name == 'middle':
            aa, bb, pq = (11, 12, 13), (14, 15, 16), ()
            edges = {(v, a), (v, b)} | {(v, z) for z in range(3, 11)}
        elif name == 'end':
            aa, bb, pq = (12, 13), (14, 15, 16), ()
            edges = {(v, a), (a, b)} | {(v, z) for z in range(3, 12)}
        else:
            aa, bb, pq = (11, 12), (13, 14), (15, 16)
            edges = {(v, a), (v, b), (a, b), pq} | {(v, z) for z in range(3, 11)}
        edges |= {(a, z) for z in aa} | {(b, z) for z in bb}
        edges = {tuple(sorted(e)) for e in edges}
        insist(Counter(z for e in edges for z in e) == Counter({v: 10, a: 4, b: 4, **{z: 1 for z in range(3, 17)}}), 'transfer link leave degrees differ')
        eligible = tuple(sorted(z for z in range(1, 17) if tuple(sorted((v, z))) not in edges))
        insist(len(eligible) == 6, 'shared tail support differs')
        partitions = []
        for tail in combinations(eligible, 3):
            if eligible[0] not in tail:
                continue
            other = tuple(z for z in eligible if z not in tail)
            if any(tuple(e) in edges for t in (tail, other) for e in combinations(t, 2)):
                continue
            partitions.append(tuple(sorted((tail, other))))
        maps = []
        for pa, pb in product(permutations(aa), permutations(bb)):
            for pp in permutations(pq) if pq else [()]:
                for swap in ((False,) if name == 'end' else (False, True)):
                    mapping = list(range(17))
                    for z, y in zip(aa, pa): mapping[z] = y
                    for z, y in zip(bb, pb): mapping[z] = y
                    for z, y in zip(pq, pp): mapping[z] = y
                    if swap:
                        exchange = {a: b, b: a, **dict(zip(aa, bb)), **dict(zip(bb, aa))}
                        mapping = [exchange.get(z, z) for z in mapping]
                    insist({tuple(sorted((mapping[x], mapping[y]))) for x, y in edges} == edges, 'transfer relabeling changes leave')
                    maps.append(tuple(mapping))
        maps = sorted(set(maps))
        insist(len(maps) == {'middle': 72, 'end': 12, 'triangle': 16}[name], 'transfer subgroup size differs')
        pending = set(partitions)
        rows = []
        while pending:
            first = min(pending)
            orbit = {tuple(sorted(tuple(sorted(g[z] for z in t)) for t in first)) for g in maps}
            insist(orbit <= pending, 'transfer partition cover differs')
            pending -= orbit
            h = {e for e in edges if v not in e} | {e for t in first for e in combinations(t, 2)}
            cliques = [q for q in combinations(range(1, 17), 4) if set(combinations(q, 2)) <= h]
            completions = [(q, r) for q, r in combinations(cliques, 2)
                           if not set(combinations(q, 2)) & set(combinations(r, 2)) and
                           set(combinations(q, 2)) | set(combinations(r, 2)) == h]
            insist(len(completions) <= 1, 'ambiguous transfer completion')
            rows.append({'name': name, 'tails': first, 'orbit_size': len(orbit), 'four_cliques': len(cliques), 'completion': list(completions[0]) if completions else []})
            if completions:
                ls = completions[0]
                tails = list(first)
                if not set(tails[0]) <= set(ls[0]): ls = tuple(reversed(ls))
                insist(all(set(t) <= set(line) for t, line in zip(tails, ls)), 'shared triangle not assigned to unique missing line')
                markers = [next(z for z in line if z not in t) for t, line in zip(tails, ls)]
                charges = {mask(pair + (z,)) for t, z in zip(tails, markers) for pair in combinations(t, 2)}
                insist(len(charges) == 6, 'charging triples not distinct')
                four, five = 0, 0
                for q in combinations(range(1, 17), 4):
                    word = set(q)
                    if all(len(word & set(t)) <= 1 for t in tails):
                        four += 1
                        insist(all(len(word & set(line)) <= 2 for line in ls), 'remaining v-word conflicts after transfer')
                for q in combinations(range(1, 17), 5):
                    word = mask(q)
                    if all((word & mask(t)).bit_count() <= 2 for t in tails):
                        five += 1
                        conflict = any((word & mask(line)).bit_count() >= 3 for line in ls)
                        charged = any(word & c == c for c in charges)
                        insist(conflict == charged, 'six-triple characterization differs')
                insist((four, five) == (1335, 4212), 'transfer complete word interface differs')
                proofs.append({'case': name, 'four_sets': four, 'five_sets': five, 'markers': markers, 'charges': sorted(charges)})
        cases.extend(rows)
    insist(sorted(r['orbit_size'] for r in cases if r['name'] == 'middle') == [1, 9] and sorted(r['orbit_size'] for r in cases if r['name'] == 'triangle') == [2, 4], 'transfer five-case census differs')
    insist(len(cases) == 5 and len(proofs) == 2, 'transfer case/completion counts differ')
    # Third interface: the two missing lines share a marker outside both tails, as for row(3,2).
    t1, t2, marker = (1, 2, 3), (4, 5, 6), 7
    charges = {mask(pair + (marker,)) for t in (t1, t2) for pair in combinations(t, 2)}
    tested = 0
    for q in combinations(range(1, 17), 5):
        word = mask(q)
        if all((word & mask(t)).bit_count() <= 2 for t in (t1, t2)):
            tested += 1
            insist(any((word & mask(t + (marker,))).bit_count() >= 3 for t in (t1, t2)) == any(word & c == c for c in charges), 'common-marker charging differs')
    insist(tested == 4212, 'common-marker word count differs')
    return {'status': 'COMPLETE', 'cases': cases, 'replacement_interfaces': proofs, 'common_marker_five_sets': tested}


def run(args):
    started = time.monotonic()
    args.output.mkdir(parents=True, exist_ok=True)
    domain = json.loads((args.work / 'domain.json').read_text())
    insist(sha256(encoded(domain)).hexdigest() == 'b50acb019ad4c1244c5e37f19aebb7d2281b58874a06f1c72b3a404d47e9943f', 'domain bytes changed')
    recorded = {}
    for f in args.work.glob('batch_*.jsonl'):
        for line in f.read_text().splitlines():
            r = json.loads(line);recorded[r['index']] = r
    selected = [r for r in domain['leaves'] if r[5] == 1]
    excluded = [r for r in domain['leaves'] if r[5] == 2]
    selected += [excluded[j * (len(excluded) - 1) // 30] for j in range(31)]
    insist(len(selected) == 100, 'geometric validation case count differs')
    answer, _, native_seconds = native(args.engine.resolve(), args.output, 'geometric100', 16, domain['allowed'], [(r[0], list(bits(r[3]))) for r in selected])
    total = 0
    for row, actual in zip(selected, answer):
        required = tuple(p for j, p in enumerate(PAIRS) if not (row[3] >> j & 1))
        columns = tuple(w for w in domain['allowed'] if pairs(w) <= set(required))
        covers, _ = point_first_covers(required, columns)
        expected = sorted(sorted(mask(q) for q in c) for c in covers)
        insist(actual['covers'] == expected == recorded[row[0]]['covers'], 'geometric entrywise reference disagreement')
        total += len(expected)
    tests = controls(args.engine.resolve(), args.output)
    certificates = json.loads((args.work / 'marked-certificates.json').read_text())
    old = [(mask(q), tuple(mask(t) for t in combinations(q, 3))) for q in combinations(range(16), 5)]
    for r in certificates:
        check_marked(r, domain['plane'], old)
    invalid = [lambda: verify_colors([7], []), lambda: verify_colors([7, 8], [[7, 8]]),
               lambda: verify_colors([7], [[7, 7]])]
    for check in invalid:
        try: check()
        except ValueError: pass
        else: raise ValueError('corrupted color certificate accepted')
    fixture = json.loads((args.target / 'witness62.json').read_text())
    for mode in range(3):
        words = list(fixture['words'])
        if mode == 0: words[0] ^= 1 << 17
        elif mode == 1: words.pop()
        else: words[0] = words[1]
        try: packing(words, size=62)
        except ValueError: pass
        else: raise ValueError('corrupt witness accepted')
    result = {'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer', 'status': 'COMPLETE', 'geometric_cases': len(selected), 'geometric_covers': total, 'native_seconds': native_seconds, 'controls': tests, 'marked_certificates_checked_by_triples': len(certificates), 'corrupt_color_controls': len(invalid), 'corrupt_witness_controls': 3, 'transfer': transfer(), 'seconds': time.monotonic() - started, 'peak_child_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (args.output / 'validation.json').write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--engine', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--target', type=Path, required=True)
    run(parser.parse_args())
