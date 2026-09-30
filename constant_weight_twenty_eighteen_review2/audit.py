#!/usr/bin/env python3
"""Independent all-branch leave audit and checked residual coloring certificates."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import resource
import subprocess
import time

from domain import build, PAIRS, holes, pmask
from exact import insist, bits, mask, pairs, encoded, packing, plane, words_json


def native(engine, work, name, n, columns, cases, cap=200000, failure=False):
    inp, out = work / (name + '.in'), work / (name + '.jsonl')
    text = f'{n} {len(columns)} {len(cases)}\n' + '\n'.join(map(str, columns)) + '\n'
    text += '\n'.join(f'{index} {len(excluded)} ' + ' '.join(map(str, excluded)) for index, excluded in cases) + '\n'
    inp.write_text(text)
    started = time.monotonic()
    p = subprocess.run([str(engine), str(inp), str(out), str(cap)], capture_output=True, text=True, timeout=600)
    elapsed = time.monotonic() - started
    if failure:
        insist(p.returncode == 2 and 'AddressSanitizer' not in p.stderr and 'runtime error:' not in p.stderr,
               'native failure is not an explicit input/guard rejection')
        return p.stderr
    if p.returncode:
        (work / (name + '.failure.json')).write_bytes(encoded({'status': 'INCOMPLETE', 'exit_code': p.returncode, 'seconds': elapsed, 'stderr': p.stderr}))
        raise RuntimeError('INCOMPLETE native batch: ' + p.stderr)
    insist(not p.stderr, 'native diagnostic')
    summary = json.loads(p.stdout)
    answers = [json.loads(line) for line in out.read_text().splitlines()]
    insist(summary['status'] == 'COMPLETE' and summary['cases'] == len(cases) and [r['index'] for r in answers] == [i for i, _ in cases], 'missing native cases')
    insist(summary['states'] == sum(r['states'] for r in answers) and summary['covers'] == sum(len(r['covers']) for r in answers), 'native totals differ')
    insist(all(0 <= r['states'] <= cap for r in answers), 'native state bound violated')
    return answers, summary, elapsed


def controls(engine, work):
    graphs = 0
    for n in range(6):
        universe = tuple(combinations(range(n), 2))
        columns = tuple(mask(q) for q in combinations(range(n), 4))
        data = []
        expected = {}
        for code in range(1 << len(universe)):
            required = {p for j, p in enumerate(universe) if code >> j & 1}
            valid = [w for w in columns if pairs(w) <= required]
            covers = []
            for sub in range(1 << len(valid)):
                selected = [valid[j] for j in bits(sub)]
                counts = Counter(p for w in selected for p in pairs(w))
                if set(counts) == required and all(d == 1 for d in counts.values()):
                    covers.append(sorted(selected))
            expected[code] = sorted(covers)
            data.append((code, [j for j in range(len(universe)) if not (code >> j & 1)]))
        for start in range(0, len(data), 1000):
            answer, _, _ = native(engine, work, f'control_{n}_{start}', n, columns, data[start:start + 1000])
            for r in answer:
                insist(r['covers'] == expected[r['index']], 'native covers disagree with literal subsets')
        graphs += len(data)
    ans, _, _ = native(engine, work, 'affine_positive', 16, plane(), [(0, [])])
    insist(ans[0]['covers'] == [list(plane())], 'affine positive cover differs')
    joined = tuple(sorted((mask((0, 1, 2, 3)), mask((0, 4, 5, 6)))))
    required = pairs(joined[0]) | pairs(joined[1])
    universe = tuple(combinations(range(7), 2))
    ans, _, _ = native(engine, work, 'joined_positive', 7, joined, [(0, [j for j, p in enumerate(universe) if p not in required])])
    insist(ans[0]['covers'] == [list(joined)], 'two-block positive cover differs')
    message = native(engine, work, 'zero_cap', 4, (15,), [(0, [])], cap=0, failure=True)
    insist('INCOMPLETE' in message, 'zero cap did not report incomplete')
    invalid = [('dimension', 17, (), []), ('nonquad', 4, (7,), [(0, [])]),
               ('duplicate', 4, (15, 15), [(0, [])]), ('pair_index', 4, (15,), [(0, [6])]),
               ('duplicate_pair', 4, (15,), [(0, [0, 0])]), ('raised_cap', 4, (15,), [(0, [])])]
    for name, n, cols, cases in invalid:
        native(engine, work, name, n, cols, cases, cap=200001 if name == 'raised_cap' else 200000, failure=True)
    return {'literal_graphs': graphs, 'positive_covers': 2, 'incomplete_controls': 1, 'malformed_controls': len(invalid)}


def coloring(words):
    # A complete graph is on compatible words; colors are pairwise incompatible classes.
    adjacency = [0] * len(words)
    for i, j in combinations(range(len(words)), 2):
        if (words[i] & words[j]).bit_count() <= 2:
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
    classes, assigned = [], [0] * len(words)
    unseen = (1 << len(words)) - 1
    while unseen:
        v = max(bits(unseen), key=lambda z: (assigned[z].bit_count(), adjacency[z].bit_count(), words[z]))
        color = 0
        while assigned[v] >> color & 1:
            color += 1
        if color == len(classes):
            classes.append([])
        classes[color].append(words[v])
        unseen ^= 1 << v
        for z in bits(adjacency[v] & unseen):
            assigned[z] |= 1 << color
    insist(sorted(w for c in classes for w in c) == sorted(words) and all(all((a & b).bit_count() >= 3 for a, b in combinations(c, 2)) for c in classes), 'false coloring certificate')
    return [sorted(c) for c in classes]


def check_cover(cover, leave, p):
    insist(len(cover) == len(set(cover)) == 18 and all(w.bit_count() == 4 and 0 <= w < 1 << 16 for w in cover), 'cover domain')
    counts = Counter(q for w in cover for q in pairs(w))
    insist(set(counts.values()) == {1} and edge_mask_from_pairs(counts) == ((1 << 120) - 1) ^ leave, 'false native pair cover')
    insist(all(all((w & line).bit_count() <= 2 for line in p) for w in cover), 'not a four-arc')


def edge_mask_from_pairs(edges):
    index = {p: i for i, p in enumerate(PAIRS)}
    return sum(1 << index[p] for p in edges)


def witness(path, p):
    raw = path.read_bytes()
    data = json.loads(raw)
    words, x, y = data['words'], data['x'], data['y']
    packing(words, size=62)
    degree = [sum(w >> z & 1 for w in words) for z in range(18)]
    insist(degree[x] == 20 and degree[y] == 18 and not any((w >> x & 1) and (w >> y & 1) for w in words), 'wrong witness endpoint data')
    insist(Counter(degree) == Counter({17: 16, 18: 1, 20: 1}), 'wrong witness degree multiset')
    insist((x, y) == (17, 16), 'witness labels differ')
    first = tuple(sorted(w ^ 1 << x for w in words if w >> x & 1))
    insist(first == tuple(p), 'witness first plane differs')
    r = tuple(sorted(w ^ 1 << y for w in words if w >> y & 1))
    leave = ((1 << 120) - 1) ^ edge_mask_from_pairs({q for w in r for q in pairs(w)})
    degree_h = Counter(z for j in bits(leave) for z in PAIRS[j])
    hub = next((z for z, value in degree_h.items() if value == 6), None)
    missing = holes(leave, hub)
    insist(len(missing) == 2, 'witness not uniquely completable')
    residual = [w for w in words if not (w >> x & 1) and not (w >> y & 1)]
    bad = [w for w in residual if any((w & q).bit_count() >= 3 for q in missing)]
    completed = [w for w in words if w not in bad] + [q | 1 << y for q in missing]
    packing(completed, size=56)
    triples = [mask(t) for q in missing for t in combinations(tuple(bits(q)), 3)]
    charges = [tuple(t for t in triples if w & t == t) for w in bad]
    insist(len(bad) == 8 and all(len(t) == 1 for t in charges) and {t[0] for t in charges} == set(triples), 'wrong equality interface')
    return {'sha256': sha256(raw).hexdigest(), 'words': 62, 'degree_multiset': dict(Counter(degree)), 'missing_quads': list(missing), 'discarded_residual_words': sorted(bad), 'completed_words': words_json(completed), 'triple_charges': [list(v) for v in charges]}


def run(args):
    args.work.mkdir(parents=True, exist_ok=True)
    engine = args.engine.resolve()
    started = time.monotonic()
    domain, geometry = build()
    data = encoded(domain)
    (args.work / 'domain.json').write_bytes(data)
    tests = controls(engine, args.work)
    p = domain['plane']
    old = [mask(q) for q in combinations(range(16), 5) if all((mask(q) & line).bit_count() <= 2 for line in p)]
    insist(len(old) == 288, 'old five-arc universe differs')
    base = tuple(w | 1 << 17 for w in p)
    output, digest = [], sha256()
    fingerprint = {'engine_sha256': sha256(engine.read_bytes()).hexdigest(), 'domain_sha256': sha256(data).hexdigest()}
    rows = domain['leaves'][:args.limit] if args.limit else domain['leaves']
    maximum_colors = 0
    for start in range(0, len(rows), 1000):
        selected = rows[start:start + 1000]
        batch_name = f'batch_{start:05d}'
        meta = args.work / (batch_name + '.meta.json')
        if meta.exists():
            record = json.loads(meta.read_text())
            insist(record['fingerprint'] == fingerprint and record['ids'] == [r[0] for r in selected] and record['status'] == 'COMPLETE', 'resumed batch fingerprint differs')
            raw = (args.work / (batch_name + '.jsonl')).read_bytes()
            insist(sha256(raw).hexdigest() == record['output_sha256'], 'resumed batch output changed')
            answers = [json.loads(line) for line in raw.splitlines()]
        else:
            answers, summary, seconds = native(engine, args.work, batch_name, 16, domain['allowed'], [(r[0], list(bits(r[3]))) for r in selected])
            record = {'fingerprint': fingerprint, 'status': 'COMPLETE', 'ids': [r[0] for r in selected], 'summary': summary, 'seconds': seconds, 'output_sha256': sha256((args.work / (batch_name + '.jsonl')).read_bytes()).hexdigest()}
            meta.write_bytes(encoded(record))
        insist(len(answers) == len(selected) and [a['index'] for a in answers] == [r[0] for r in selected], 'resumed case sequence differs')
        for row, answer in zip(selected, answers):
            index, profile, si, leave, orbit_size, kind = row
            if kind == 2:
                insist(not answer['covers'], 'counterexample to completion theorem')
                digest.update(encoded({'index': index, 'covers': []}))
            stars = []
            for cover in answer['covers']:
                check_cover(cover, leave, p)
                union = base + tuple(w | 1 << 16 for w in cover)
                packing(union, size=38)
                record_star = {'cover_sha256': sha256(encoded(cover)).hexdigest()}
                if kind == 0:
                    q = [w for w in old if all((w & r).bit_count() <= 2 for r in cover)]
                    classes = coloring(q)
                    record_star.update(residual_words=len(q), colors=len(classes), color_certificate_sha256=sha256(encoded(classes)).hexdigest())
                    maximum_colors = max(maximum_colors, len(classes))
                    insist(len(classes) < 24, 'collinear branch lacks strict below62 certificate')
                stars.append(record_star)
            output.append({'index': index, 'profile': profile, 'support_index': si, 'orbit_size': orbit_size, 'kind': kind, 'states': answer['states'], 'covers': len(answer['covers']), 'stars': stars})
        progress = {'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer', 'status': 'INCOMPLETE until all45100 cases complete', 'completed': len(output), 'total': len(rows), 'states': sum(r['states'] for r in output), 'covers': sum(r['covers'] for r in output), 'max_collinear_colors': maximum_colors, 'seconds': time.monotonic() - started}
        (args.work / 'progress.json').write_bytes(encoded(progress))
        print(json.dumps(progress, sort_keys=True), flush=True)
    complete = len(rows) == 45100
    if complete:
        insist(digest.hexdigest() == '38bc2c95fb6001828619d29ea9ab3b4e09117d5923531c772e9e6a2e19545e23', 'ordered exclusion digest differs')
        insist(sum(r['covers'] for r in output if r['kind'] == 1) == 1927, 'completed-star census differs')
    result = {'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer', 'status': 'COMPLETE' if complete else 'PARTIAL', 'geometry': geometry, 'controls': tests, 'cases': len(rows), 'case_counts': dict(Counter(r['kind'] for r in output)), 'positive_leave_counts': dict(Counter(r['kind'] for r in output if r['covers'])), 'cover_counts': {str(kind): sum(r['covers'] for r in output if r['kind'] == kind) for kind in range(3)}, 'states': sum(r['states'] for r in output), 'max_case_states': max(r['states'] for r in output), 'max_collinear_colors': maximum_colors, 'excluded_digest': digest.hexdigest(), 'all_cases_sha256': sha256(encoded(output)).hexdigest(), 'witness': witness(args.target / 'witness62.json', p), 'fingerprint': fingerprint, 'seconds': time.monotonic() - started, 'peak_child_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (args.work / 'cases.json').write_bytes(encoded(output))
    (args.work / 'summary.json').write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--engine', type=Path, required=True)
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--limit', type=int, help='Explicit partial pilot')
    run(parser.parse_args())
