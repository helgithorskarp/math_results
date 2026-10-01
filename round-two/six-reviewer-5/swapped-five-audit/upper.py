"""Independent complete raw carrier, positive transports and literal graphs.

Imports only the byte-pinned, previously reviewed generic normalizer.
No swapped-pair researcher module or solver is imported.
"""
from collections import Counter
from itertools import combinations, permutations, product
import importlib.util
import json
from pathlib import Path
import time
from core import HERE, G, code_check, digest, image, mask, pin_inputs, points, require
from clique import maximum, twins

def actual_maps(quads, mate):
    tails = sorted(tuple(v for v in q if v != mate) for q in quads if mate in q)
    used = {v for t in tails for v in t}
    require(len(tails) == 5 and len(used) == 15, 'common-tail partition')
    complement = set(range(17)) - {mate} - used
    require(len(complement) == 1, 'tail complement')
    maps = set()
    for fixed in range(5):
        others = [i for i in range(5) if i != fixed]
        for partner in others[1:]:
            rest = [i for i in others if i not in (others[0], partner)]
            pairs = ((others[0], partner), tuple(rest))
            for stationary in tails[fixed]:
                transposition = [v for v in tails[fixed] if v != stationary]
                for choices in product(permutations(tails[pairs[0][1]]),
                                       permutations(tails[pairs[1][1]])):
                    q = list(range(18))
                    q[17], q[mate] = mate, 17
                    q[transposition[0]], q[transposition[1]] = transposition[1], transposition[0]
                    for (a, b), values in zip(pairs, choices):
                        for x, y in zip(tails[a], values):
                            q[x], q[y] = y, x
                    require(sorted(q) == list(range(18)) and all(q[q[v]] == v for v in range(18))
                            and sum(q[v] == v for v in range(18)) == 2, 'raw involution domain')
                    require({frozenset(q[v] for v in t) for t in tails} ==
                            {frozenset(t) for t in tails}, 'raw common-tail action')
                    maps.add(tuple(q))
    require(len(maps) == 1620, 'complete raw-map product/uniqueness')
    return tuple(sorted(maps))

def raw_carrier(quads):
    star = tuple(mask(q) | 1 << 17 for q in quads)
    require(len(star) == 20, 'complete star size')
    degrees = code_check(star)
    valid, counts, raw_hashes = {}, [], []
    for mate in range(17):
        if degrees[mate] != 5:
            continue
        started = time.monotonic()
        maps = actual_maps(quads, mate)
        raw_hashes.append((mate, digest(maps)))
        private = tuple(tuple(q) for q in quads if mate not in q)
        private_masks = tuple(mask(q) for q in private)
        accepted = 0
        for g in maps:
            moved = tuple(mask(g[v] for v in q) for q in private)
            if any((a & b).bit_count() > 2 for a in private_masks for b in moved):
                continue
            words = tuple(sorted(set(star) | {image(w, g) for w in star}))
            reps = code_check(words, g)
            require(len(words) == 35 and reps[17] == reps[mate] == 20 and
                    sum(w >> mate & 1 and w >> 17 & 1 for w in words) == 5, 'positive star union')
            valid[(mate, g)] = words
            accepted += 1
        require(time.monotonic() - started < 30, 'INCOMPLETE per-mate guard')
        counts.append((mate, len(maps), accepted))
    return valid, counts, raw_hashes

def fixture_groups(quads, normalizer):
    q = normalizer.blocks(quads)
    k = normalizer.key(q)
    maps = sorted(set(p for target, p in normalizer.normalized(q) if target == k))
    require(all(sorted(p) == list(range(17)) and
                tuple(sorted(tuple(sorted(p[v] for v in b)) for b in q)) == q for p in maps),
            'nonactual fixture map')
    return tuple(p + (17,) for p in maps)

def normalize(words, g, mate):
    p = [-1] * 18
    p[17], p[mate] = 0, 1
    pairs = [(v, g[v]) for v in range(18) if v < g[v] and v not in (17, mate)]
    fixed = [v for v in range(18) if g[v] == v]
    require(len(pairs) == 7 and len(fixed) == 2, 'normalizing cycle structure')
    for i, (a, b) in enumerate(pairs, 1):
        p[a], p[b] = 2 * i, 2 * i + 1
    for i, a in enumerate(fixed, 16):
        p[a] = i
    require(sorted(p) == list(range(18)) and all(p[g[v]] == G[p[v]] for v in range(18)),
            'false conjugacy')
    normalized = tuple(sorted(image(w, p) for w in words))
    require(code_check(normalized, G)[:2] == (20, 20), 'normalized centers')
    return normalized

def rooted_cover(valid, group):
    remaining, roots, coverage = set(valid), [], []
    while remaining:
        mate, g = min(remaining)
        anchor = valid[(mate, g)]
        reached = {}
        for p in group:
            conjugate = [-1] * 18
            for v in range(18):
                conjugate[p[v]] = p[g[v]]
            key = (p[mate], tuple(conjugate))
            require(key in valid, 'fixture map left complete positive carrier')
            if key not in reached:
                moved = tuple(sorted(image(w, p) for w in anchor))
                require(moved == valid[key], 'false positive literal transport')
                reached[key] = p
        require(set(reached) <= remaining and (mate, g) in reached, 'overlapping/incomplete orbit cover')
        roots.append({'mate': mate, 'mapping': g, 'words': anchor,
                      'normalized': normalize(anchor, g, mate), 'orbit_size': len(reached)})
        for key, transport in sorted(reached.items()):
            coverage.append((key[0], key[1], len(roots) - 1, transport))
        remaining -= set(reached)
    require({(m, g) for m, g, root, p in coverage} == set(valid) and len(coverage) == len(valid),
            'positive coverage equality')
    return roots, coverage

def residual_universe():
    words = tuple(mask(w) for w in combinations(range(2, 18), 5))
    all_orbits = {tuple(sorted({w, image(w, G)})) for w in words}
    orbits = tuple(sorted(o for o in all_orbits if len(o) == 1 or (o[0] & o[1]).bit_count() <= 2))
    require({w for o in all_orbits for w in o} == set(words), 'incomplete whole-word orbits')
    owners, resources = {}, []
    for i, orbit in enumerate(orbits):
        triples = tuple(mask(t) for w in orbit for t in combinations(points(w), 3))
        require(len(triples) == len(set(triples)), 'internally invalid orbit')
        resources.append(triples)
        for t in triples:
            owners[t] = owners.get(t, 0) | 1 << i
    conflicts = []
    for ts in resources:
        occupied = 0
        for t in ts:
            occupied |= owners[t]
        conflicts.append(occupied)
    return orbits, owners, tuple(conflicts)

def residual_graph(anchor, universe):
    orbits, owners, conflicts = universe
    forbidden = 0
    for w in anchor:
        for t in combinations(points(w), 3):
            forbidden |= owners.get(mask(t), 0)
    selected = [i for i in range(len(orbits)) if not forbidden >> i & 1]
    local = tuple(orbits[i] for i in selected)
    rows = tuple(sum(1 << j for j, b in enumerate(selected) if i != j and not conflicts[a] >> b & 1)
                 for i, a in enumerate(selected))
    require(all((w & a).bit_count() <= 2 for o in local for w in o for a in anchor),
            'invalid eligible residual orbit')
    # The physical triple-incidence encoding is checked against every literal edge.
    require(all(bool(rows[i] >> j & 1) == all((a & b).bit_count() <= 2
                for a in local[i] for b in local[j])
                for i in range(len(local)) for j in range(i)), 'literal edge differs')
    return local, rows

def audit(work):
    pin_inputs()
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    spec = importlib.util.spec_from_file_location('reviewed_generic_normalizer', HERE / 'inputs/generic_star_audit.py')
    normalizer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(normalizer)
    fixtures = json.loads((HERE / 'inputs/fixtures.json').read_text())['stars']
    group_checks = json.loads((HERE / 'GROUP_DIGESTS.json').read_text())
    require(len(fixtures) == len(group_checks) == 23, 'fixture/group count')
    roots, summaries, proof, raw_proof = [], [], [], []
    for fi, quads in enumerate(fixtures):
        valid, counts, hashes = raw_carrier(quads)
        group = fixture_groups(quads, normalizer)
        expected = group_checks[fi]
        require(len(group) == expected['order'] and
                normalizer.digest(tuple(p[:-1] for p in group)) == expected['sha256'], 'reviewed group digest')
        representatives, coverage = rooted_cover(valid, group)
        for r in representatives:
            r['fixture'] = fi
        proof.extend((fi, m, g, len(roots) + ri, p) for m, g, ri, p in coverage)
        raw_proof.append((fi, hashes))
        roots.extend(representatives)
        summaries.append({'fixture': fi, 'eligible_mates': len(counts),
                          'raw_maps': sum(r[1] for r in counts), 'valid_maps': len(valid),
                          'roots': len(representatives), 'group_order': len(group), 'mate_counts': counts})
        print(json.dumps({'stage': 'raw_and_transport', **{k: v for k, v in summaries[-1].items()
                         if k != 'mate_counts'}}), flush=True)
    (work / 'positive-root-cover.json').write_text(json.dumps({'roots': roots, 'coverage': proof}))
    universe = residual_universe()
    cases = []
    for ri, root in enumerate(roots):
        anchor = root['normalized']
        orbits, adjacency = residual_graph(anchor, universe)
        expanded, carriers = twins(adjacency, tuple(map(len, orbits)))
        chosen, nodes = maximum(expanded)
        selected = set(carriers[v] for v in chosen)
        extension = {w for i in selected for w in orbits[i]}
        require(len(extension) == len(chosen), 'partial true-twin maximum')
        words = tuple(sorted(set(anchor) | extension))
        require(code_check(words, G)[:2] == (20, 20) and len(words) == 35 + len(chosen),
                'literal maximum witness')
        case = {'root': ri, 'fixture': root['fixture'], 'orbit_vertices': len(orbits),
                'fixed_orbits': sum(len(o) == 1 for o in orbits), 'expanded_vertices': len(expanded),
                'residual_maximum': len(chosen), 'nodes': nodes,
                'graph_sha256': digest({'orbits': orbits, 'adjacency': adjacency}),
                'witness_sha256': digest(words)}
        cases.append(case)
        (work / ('case-%03d.json' % ri)).write_text(json.dumps({'summary': case, 'words': words}))
        if (ri + 1) % 50 == 0:
            print(json.dumps({'stage': 'clique', 'cases': ri + 1}), flush=True)
    require(len(cases) == len(roots), 'incomplete rooted upper audit')
    require(max(c['residual_maximum'] for c in cases) <= 34, 'counterexample to claimed upper69')
    require(time.monotonic() - started < 240, 'INCOMPLETE whole-audit guard')
    result = {'status': 'PASS_COMPLETE_RAW_SWAPPED_PAIR_AUDIT',
              'fixtures': summaries, 'raw_maps': sum(r['raw_maps'] for r in summaries),
              'eligible_mates': sum(r['eligible_mates'] for r in summaries),
              'valid_maps': len(proof), 'rooted_cases': len(roots),
              'raw_sha256': digest(raw_proof), 'positive_transports_sha256': digest(proof),
              'roots_sha256': digest(roots), 'cases_sha256': digest(cases),
              'maximum_residual': max(c['residual_maximum'] for c in cases),
              'maximum_code_size_distribution': sorted(Counter(35 + c['residual_maximum'] for c in cases).items()),
              'roots_reaching69': [c['root'] for c in cases if c['residual_maximum'] == 34],
              'nodes': sum(c['nodes'] for c in cases), 'max_nodes': max(c['nodes'] for c in cases),
              'expanded_vertex_range': [min(c['expanded_vertices'] for c in cases),
                                        max(c['expanded_vertices'] for c in cases)]}
    (work / 'RESULT.json').write_text(json.dumps(result, indent=2))
    return result

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.work), sort_keys=True))
