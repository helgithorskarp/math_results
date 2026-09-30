#!/usr/bin/env python3
"""Complete normalized leave domain and resumable bitset exact-cover exclusion.

The written reduction and prior 56/57 bounds are essential proof premises.
Generated domains, native inputs/outputs and checkpoints are local run state.
"""
import argparse
import hashlib
import itertools as it
import json
import resource
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'a18_6_5_saturated_single_pair'))
from geometry import automorphisms, image, normalization, points, word

PAIRS = list(it.combinations(range(16), 2))
PI = {e: j for j, e in enumerate(PAIRS)}
CUBIC = (
 ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),(4,5),(4,6),(4,7),(5,6),(5,7),(6,7)),
 ((0,1),(0,2),(0,3),(1,2),(1,3),(2,4),(3,5),(4,6),(4,7),(5,6),(5,7),(6,7)),
 ((0,1),(0,2),(0,3),(1,2),(1,4),(2,5),(3,4),(3,6),(4,7),(5,6),(5,7),(6,7)),
 ((0,1),(0,2),(0,3),(1,2),(1,4),(2,5),(3,6),(3,7),(4,6),(4,7),(5,6),(5,7)),
 ((0,1),(0,2),(0,3),(1,4),(1,5),(2,4),(2,6),(3,5),(3,6),(4,7),(5,7),(6,7)),
 ((0,1),(0,2),(0,3),(1,4),(1,5),(2,4),(2,6),(3,5),(3,7),(4,7),(5,6),(6,7)))
CYCLES = (((0,1),(0,2),(1,2),(3,4),(3,5),(4,5)),
          ((0,1),(0,2),(1,3),(2,4),(3,5),(4,5)))

def require(value, message):
    if not value:
        raise ValueError(message)

def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low

def edge_mask(edges):
    return sum(1 << PI[tuple(sorted(e))] for e in edges)

def pair_mask(block):
    return edge_mask(it.combinations(points(block), 2))

def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()

def save(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_bytes(encoded(value))
    temporary.replace(path)

def orbit_cover(domain, group, action):
    todo, output = set(domain), []
    while todo:
        first = min(todo)
        orbit = {action(first, g) for g in group}
        require(orbit <= todo, 'invalid, omitted, or overlapping symmetry orbit')
        todo -= orbit
        output.append((first, len(orbit)))
    require(sum(n for _, n in output) == len(domain), 'incomplete orbit cover')
    return output

def templates(representatives, n, degree):
    """All labelings of a compact catalogue; verifier independently fills degrees."""
    answer = set()
    for graph in representatives:
        require(len(graph) == n * degree // 2 and len(set(graph)) == len(graph) and
                all(sum(v in e for e in graph) == degree for v in range(n)),
                'invalid abstract representative')
        for g in it.permutations(range(n)):
            answer.add(tuple(sorted(tuple(sorted((g[a], g[b]))) for a, b in graph)))
    return sorted(answer)

def holes(mask):
    """Recognize exactly a unique decomposition into two edge-disjoint K4s."""
    edges = [PAIRS[j] for j in bits(mask)]
    support = sorted(set(p for e in edges for p in e))
    cliques = [word(a) for a in it.combinations(support, 4)
               if pair_mask(word(a)) & mask == pair_mask(word(a))]
    decompositions = [(a, b) for a, b in it.combinations(cliques, 2)
                      if not (pair_mask(a) & pair_mask(b)) and pair_mask(a) | pair_mask(b) == mask]
    require(len(decompositions) <= 1, 'ambiguous two-line decomposition')
    return list(decompositions[0]) if decompositions else []

def prepare():
    plane = normalization()['first_plane']
    group = automorphisms(plane)
    abstract = [templates(CUBIC, 8, 3), templates(CYCLES, 6, 2)]
    require([len(t) for t in abstract] == [19355, 70], 'abstract domain mismatch')
    triples = [edge_mask(it.combinations(t, 2)) for line in plane
               for t in it.combinations(points(line), 3)]
    require(len(triples) == len(set(triples)) == 80, 'collinear triple mismatch')
    groups, leaves = [], []
    for profile in range(2):
        if profile == 0:
            domain = {word(s) for s in it.combinations(range(16), 8)}
            action = image
        else:
            domain = {(word(s), p) for s in it.combinations(range(16), 7) for p in s}
            action = lambda v, g: (image(v[0], g), g[v[1]])
        supports = orbit_cover(domain, group, action)
        require(len(supports) == (10 if profile == 0 else 25), 'support orbit mismatch')
        for si, (representative, orbit_size) in enumerate(supports):
            support, hub = (representative, None) if profile == 0 else representative
            order = list(points(support)) if hub is None else list(points(support ^ (1 << hub)))
            stabilizer = [g for g in group if image(support, g) == support and
                          (hub is None or g[hub] == hub)]
            require(len(stabilizer) * orbit_size == 5760, 'incorrect support stabilizer')
            candidates = {edge_mask([(order[a], order[b]) for a, b in graph] +
                                    ([] if hub is None else [(hub, p) for p in order]))
                          for graph in abstract[profile]}
            maps = [[PI[tuple(sorted((g[a], g[b])))] for a, b in PAIRS] for g in stabilizer]
            local = orbit_cover(candidates, maps, lambda v, g: sum(1 << g[j] for j in bits(v)))
            counts = Counter()
            for leave, size in local:
                if any(leave & t == t for t in triples):
                    kind = 0
                elif holes(leave):
                    kind = 1
                    require(all(all((h & line).bit_count() <= 2 for line in plane)
                                for h in holes(leave)), 'missing line is not a P-four-arc')
                else:
                    kind = 2
                counts[kind] += 1
                leaves.append([len(leaves), profile, si, leave, size, kind])
            groups.append([profile, si, support, hub, orbit_size, len(stabilizer),
                           len(candidates), len(local), [counts[k] for k in range(3)]])
    labelled = sum(r[4] * r[6] for r in groups)
    require(labelled == 254704450 and len(leaves) == 45100, 'leave coverage mismatch')
    counts = [[sum(r[1] == p and r[5] == k for r in leaves) for k in range(3)] for p in range(2)]
    require(counts == [[9957, 28, 34050], [676, 41, 348]], 'leaf classification mismatch')
    allowed = [word(a) for a in it.combinations(range(16), 4)
               if all((word(a) & line).bit_count() <= 2 for line in plane)]
    require(len(allowed) == 840, 'four-arc domain mismatch')
    return {'plane': plane, 'groups': groups, 'leaves': leaves, 'allowed': allowed}

def matrix(path, allowed, leaves):
    with path.open('w') as out:
        out.write(f'120 {len(allowed)} 6\n')
        for block in allowed:
            out.write(' '.join(map(str, [block] + list(bits(pair_mask(block))))) + '\n')
        out.write(str(len(leaves)) + '\n')
        for index, row in enumerate(leaves):
            excluded = list(bits(row[3]))
            require(len(excluded) == 12, 'incorrect leave edge count')
            out.write(' '.join(map(str, [index, 12] + excluded)) + '\n')

def run(args):
    started = time.monotonic()
    domain = prepare()
    args.work.mkdir(parents=True, exist_ok=True)
    domain_bytes = encoded(domain)
    domain_hash = hashlib.sha256(domain_bytes).hexdigest()
    domain_path = args.work / 'domain.json'
    if domain_path.exists():
        require(domain_path.read_bytes() == domain_bytes, 'resumed domain differs')
    else:
        domain_path.write_bytes(domain_bytes)
    leaves = [r for r in domain['leaves'] if r[5] == 2]
    engine = args.engine.resolve()
    fingerprint = {'domain_sha256': domain_hash,
                   'engine_sha256': hashlib.sha256(engine.read_bytes()).hexdigest()}
    digest = hashlib.sha256()
    totals = {'cases': 0, 'covers': 0, 'nodes': 0, 'max_leaf_nodes': 0}
    for start in range(0, len(leaves), 1000):
        selected = leaves[start:start + 1000]
        prefix = args.work / f'batch_{start:05d}'
        inp, out, meta = [prefix.with_suffix(s) for s in ['.in', '.jsonl', '.meta.json']]
        if meta.exists():
            record = json.loads(meta.read_text())
            require(record['fingerprint'] == fingerprint and record['start'] == start and
                    record['count'] == len(selected) and record['status'] == 'COMPLETE',
                    'invalid resumed batch')
            require(record['output_sha256'] == hashlib.sha256(out.read_bytes()).hexdigest(),
                    'resumed output changed')
            result_summary = record['summary']
        else:
            matrix(inp, domain['allowed'], selected)
            run_started = time.monotonic()
            result = subprocess.run([str(engine), str(inp), str(out)], capture_output=True, text=True)
            record = {'start': start, 'count': len(selected), 'fingerprint': fingerprint,
                      'exit_code': result.returncode, 'seconds': time.monotonic() - run_started,
                      'stderr': result.stderr, 'stdout': result.stdout}
            if result.returncode:
                record['status'] = 'INCOMPLETE; no exclusion from this unfinished batch'
                save(prefix.with_suffix('.failure.json'), record)
                raise RuntimeError('INCOMPLETE native census; completed batches preserved')
            result_summary = json.loads(result.stdout)
            require(result_summary['status'] == 'COMPLETE' and
                    result_summary['cases'] == len(selected), 'incomplete native output')
            record.update(status='COMPLETE', summary=result_summary,
                          output_sha256=hashlib.sha256(out.read_bytes()).hexdigest())
            save(meta, record)
        results = [json.loads(s) for s in out.read_text().splitlines()]
        require(len(results) == len(selected) and
                [r['index'] for r in results] == list(range(len(selected))), 'missing native case')
        require(sum(r['nodes'] for r in results) == result_summary['nodes'] and
                sum(len(r['covers']) for r in results) == result_summary['covers'],
                'incorrect native totals')
        for row, result in zip(selected, results):
            require(result['covers'] == [], 'counterexample to unique-completion reduction')
            digest.update(encoded({'index': row[0], 'covers': result['covers']}))
        for k in ['cases', 'covers', 'nodes']:
            totals[k] += result_summary[k]
        totals['max_leaf_nodes'] = max(totals['max_leaf_nodes'], max(r['nodes'] for r in results))
        progress = {'status': 'INCOMPLETE until every batch finishes', 'total_leaves': len(leaves),
                    'totals': totals, 'seconds': time.monotonic() - started}
        save(args.work / 'progress.json', progress)
        print(json.dumps(progress), flush=True)
    summary = {'agent': 'six-code-3', 'role': 'researcher',
               'status': 'COMPLETE finite exclusion', 'domain_sha256': domain_hash,
               'exclusion_sha256': digest.hexdigest(), 'leaf_orbits': len(domain['leaves']),
               'labelled_leaves': 254704450,
               'profile_counts': [[9957, 28, 34050], [676, 41, 348]],
               'totals': totals, 'seconds': time.monotonic() - started,
               'max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               'max_child_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    save(args.work / 'summary.json', summary)
    print(json.dumps(summary), flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    run(parser.parse_args())
