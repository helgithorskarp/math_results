#!/usr/bin/env python3
"""Independent ordered three-star reconstruction and exact capacity audit."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import select
import subprocess
import time

HERE = Path(__file__).resolve().parent
INPUT_SHA = '83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca'
CERT_SHA = '1ccf38f9ceaec313916c282b0453f0f4e2e050ca029e68416bbadb73b570428e'
TRIPLES = list(combinations(range(18), 3))
TRIPLE_INDEX = {q: i for i, q in enumerate(TRIPLES)}
CENTERS = (15, 16, 17)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def encode(data):
    return (json.dumps(data, sort_keys=True, separators=(',', ':')) + '\n').encode()


def digest(data):
    return hashlib.sha256(encode(data)).hexdigest()


def mask(points):
    return sum(1 << x for x in points)


def points(word):
    require(type(word) is int and 0 <= word < (1 << 18), 'word domain')
    return tuple(x for x in range(18) if word & (1 << x))


def triples(word):
    return sum(1 << TRIPLE_INDEX[q] for q in combinations(points(word), 3))


def ownership(words, size):
    require(len(words) == len(set(words)) == size, 'word count/distinctness')
    covered = 0
    for word in words:
        require(word.bit_count() == 5, 'word weight')
        t = triples(word)
        require(not (covered & t), 'repeated triple')
        covered |= t
    require(covered.bit_count() == 10 * size, 'triple ownership count')
    return covered


def profile(words, center):
    containing = [w for w in words if w & (1 << center)]
    require(len(containing) == 19, 'completed center replication')
    labels = [x for x in range(18) if x != center]
    rho = [sum(bool(w & (1 << x)) for w in containing) for x in labels]
    require(max(rho) <= 5, 'pair replication cap')
    full = [x for x, r in zip(labels, rho) if r == 5]
    covered = ownership(containing, 19)
    m = sum(not (covered & (1 << TRIPLE_INDEX[tuple(sorted((center, a, b)))]))
            for a, b in combinations(full, 2))
    return {'m': m, 'rho': rho, 'positive_deficits': sorted(5-r for r in rho if r < 5)}


class Ordered:
    """One native process, one completely framed graph per request."""
    def __init__(self, executable):
        self.proc = subprocess.Popen([str(executable)], stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     text=True, bufsize=1)
        self.requests = self.nodes = self.largest_request = 0

    def close(self):
        if self.proc.poll() is None:
            self.proc.stdin.close()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()
        require(self.proc.returncode == 0, 'native process failed: ' + self.proc.stderr.read())

    def enumerate(self, adjacent, selected, target=9):
        if len(selected) < target:
            return []
        require(len(selected) <= 128, 'selected graph exceeds fixed bit domain')
        # Fixed degree order permutes the selected domain; it removes nothing.
        order = sorted(selected, key=lambda v: (adjacent[v].bit_count(), v))
        reverse = {v: i for i, v in enumerate(order)}
        rows = [[reverse[w] for w in order if adjacent[v] & (1 << w)] for v in order]
        data = str(len(rows)) + ' ' + str(target) + '\n' + ''.join(
            str(len(row)) + ' ' + ' '.join(map(str, row)) + '\n' for row in rows)
        self.proc.stdin.write(data)
        self.proc.stdin.flush()
        ready, _, _ = select.select([self.proc.stdout], [], [], 30)
        if not ready:
            self.proc.kill()
            self.proc.wait()
            raise RuntimeError('INCOMPLETE native response timeout')
        line = self.proc.stdout.readline()
        require(bool(line), 'native EOF before response')
        result = json.loads(line)
        require(result['status'] == 'COMPLETE', 'incomplete native result')
        qs = sorted(tuple(sorted(order[x] for x in q)) for q in result['cliques'])
        require(len(qs) == len(set(qs)), 'duplicate native clique')
        require(all(len(q) == len(set(q)) == target and all(
            adjacent[a] & (1 << b) for a, b in combinations(q, 2)) for q in qs),
            'decoded clique fails')
        self.requests += 1
        self.nodes += result['nodes']
        self.largest_request = max(self.largest_request, result['nodes'])
        return qs


def inputs():
    raw = (HERE/'INPUT.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == INPUT_SHA, 'audited census input hash')
    data = json.loads(raw)
    missing = {(a+i, a+j) for a, n in ((0, 2), (2, 3))
               for i in range(n) for j in (i, (i+1) % n)}
    cells = [(r, c) for r in range(5) for c in range(5) if (r, c) not in missing]
    row = [mask(i for i, (r, c) in enumerate(cells) if r == j) for j in range(5)]
    col = [mask(i for i, (r, c) in enumerate(cells) if c == j) for j in range(5)]
    quads = [mask(q) for q in combinations(range(15), 4)
             if all((mask(q) & b).bit_count() <= 1 for b in row+col)]
    require(len(cells) == 15 and len(quads) == 96, 'input cell/candidate decoding')
    require(not any(e['low_low_pairs'] == 2 for e in data['models'][0]['marked_classes']),
            'm=2 in omitted carrier')
    reps = [e for e in data['models'][1]['marked_classes'] if e['low_low_pairs'] == 2]
    require(len(reps) == 6, 'six marked input representatives')
    stars = []
    for rep in reps:
        private = [quads[i] for i in rep['clique']]
        fixed = sorted([b | (1 << 15) | (1 << 17) for b in row] +
                       [b | (1 << 16) | (1 << 17) for b in col] +
                       [b | (1 << 17) for b in private])
        ownership(fixed, 19)
        require(profile(fixed, 17)['m'] == 2, 'input double leave')
        stars.append({'clique': rep['clique'], 'row': row, 'col': col,
                      'private': private, 'fixed': fixed})
    return cells, stars


def ordered_partitions(tails):
    """Enumerate increasing five-tail combinations, with disjointness only."""
    start = time.monotonic()
    found = []
    nodes = 0
    def visit(available, used, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > 2000000 or (nodes % 1024 == 0 and time.monotonic()-start > 20):
            raise RuntimeError('INCOMPLETE ordered partition guard')
        need = 5-len(chosen)
        if not need:
            require(used == (1 << 15)-1, 'disjoint five triples fail to cover')
            found.append(tuple(sorted(tails[i] for i in chosen)))
            return
        for pos in range(len(available)-need+1):
            i = available[pos]
            rest = [j for j in available[pos+1:] if not (tails[j] & tails[i])]
            visit(rest, used | tails[i], chosen+[i])
    visit(list(range(len(tails))), 0, [])
    require(len(found) == len(set(found)), 'duplicate ordered partition')
    return sorted(found), nodes


def base(center, forbidden):
    words = [mask(q) | (1 << center) for q in combinations(range(15), 4)
             if not (triples(mask(q) | (1 << center)) & forbidden)]
    ts = [triples(w) for w in words]
    adjacency = [mask(j for j, b in enumerate(ts) if i != j and not (a & b))
                 for i, a in enumerate(ts)]
    require(all(bool(adjacency[i] & (1 << j)) ==
                (i != j and (a & b).bit_count() <= 2)
                for i, a in enumerate(words) for j, b in enumerate(words)),
            'triple/intersection graph bridge')
    return words, ts, adjacency


def reconstruct(native, work, cases):
    cells, stars = inputs()
    summary = {'cells': cells, 'cases': [], 'core_count': 0,
               'status': 'COMPLETE' if set(cases) == set(range(6)) else 'COMPLETE_SELECTED_CASES'}
    cores = []
    for k in cases:
        started = time.monotonic()
        star = stars[k]
        covered = ownership(star['fixed'], 19)
        tails = [mask(q) for q in combinations(range(15), 3)
                 if not (triples(mask(q) | (1 << 15) | (1 << 16)) & covered)]
        partitions, cover_nodes = ordered_partitions(tails)
        yw, yt, ya = base(15, covered)
        zw, zt, za = base(16, covered)
        header = {'star': star, 'triples': tails, 'partitions': partitions,
                  'y_words': yw, 'y_adjacent': ya, 'z_words': zw, 'z_adjacent': za}
        (work/f'header-{k}.json').write_bytes(encode(header))
        counter, joints = Counter(), []
        with (work/f'carrier-{k}.jsonl').open('wb') as stream:
            for pi, p in enumerate(partitions):
                if time.monotonic()-started > 60:
                    raise RuntimeError('INCOMPLETE whole independent case guard')
                extra = [t | (1 << 15) | (1 << 16) for t in p]
                prefix = covered | ownership(extra, 5)
                require(prefix.bit_count() == 240, 'yz prefix triple ownership')
                ys = [i for i, t in enumerate(yt) if not (t & prefix)]
                yc = native.enumerate(ya, ys)
                y2 = [q for q in yc if profile(
                    [w for w in star['fixed'] if w & (1 << 15)] + extra + [yw[i] for i in q], 15)['m'] == 2]
                record = {'partition': p, 'y_candidates': ys, 'y_nine': yc,
                          'y_two': y2, 'z_cases': []}
                counter.update(partitions=1, y_nine=len(yc), y_two=len(y2))
                for q in yc:
                    private_y = [yw[i] for i in q]
                    y_prefix = prefix | ownership(private_y, 9)
                    require(y_prefix.bit_count() == 330, 'y prefix triple ownership')
                    zs = [i for i, t in enumerate(zt) if not (t & y_prefix)]
                    zc = native.enumerate(za, zs)
                    record['z_cases'].append({'y': q, 'z_candidates': zs, 'z_nine': zc})
                    counter.update(z_nine=len(zc))
                    for r in zc:
                        blocks = sorted(star['fixed'] + extra + private_y + [zw[i] for i in r])
                        ownership(blocks, 42)
                        require(all((a & b).bit_count() <= 2 for a, b in combinations(blocks, 2)),
                                'literal core intersection check')
                        profiles = [profile(blocks, c) for c in CENTERS]
                        require(all(s['m'] in (1, 2) for s in profiles), 'core m profile')
                        require(all(sum(bool(w & (1 << a)) and bool(w & (1 << b)) for w in blocks) == 5
                                    for a, b in combinations(CENTERS, 2)), 'core pair replication')
                        require(not any(w & mask(CENTERS) == mask(CENTERS) for w in blocks),
                                'core covers center triple')
                        joint = {'case': k, 'partition_index': pi, 'y': q, 'z': r,
                                 'profiles': profiles, 'blocks': blocks, 'core_sha256': digest(blocks)}
                        joints.append(joint)
                stream.write(encode(record))
        (work/f'joints-{k}.json').write_bytes(encode(joints))
        cores.extend(joints)
        case = {'clique': star['clique'], 'triple_count': len(tails),
                'partition_count': len(partitions), 'y_base': len(yw), 'z_base': len(zw),
                'counts': dict(counter), 'joint_count': len(joints),
                'm_census': dict(sorted(Counter(','.join(str(p['m']) for p in j['profiles'])
                                               for j in joints).items())),
                'header_sha256': digest(header), 'joints_sha256': digest(joints),
                'carrier_sha256': hashlib.sha256((work/f'carrier-{k}.jsonl').read_bytes()).hexdigest()}
        summary['cases'].append(case)
        print(json.dumps({'case': k, 'status': 'COMPLETE', 'seconds': time.monotonic()-started,
                          'cover_nodes': cover_nodes, 'counts': dict(counter), 'cores': len(joints)}), flush=True)
    summary['core_count'] = len(cores)
    return summary, cores


def check_capacity_core(core, cert):
    words = core['blocks']
    covered = ownership(words, 42)
    require(all(w & mask(CENTERS) for w in words), 'core word misses completed centers')
    require(all(sum(bool(w & (1 << c)) for w in words) == 19 for c in CENTERS), 'core center degree')
    require(all(sum(bool(w & (1 << a)) and bool(w & (1 << b)) for w in words) == 5
                for a, b in combinations(CENTERS, 2)), 'core center pair degree')
    require(not (covered & (1 << TRIPLE_INDEX[CENTERS])), 'covered center triple')
    old_words = [mask(q) for q in combinations(range(15), 5)]
    require(cert['core_sha256'] == digest(words), 'core binding')
    require(type(cert['denominator']) is int and cert['denominator'] == 1000, 'integer denominator')
    weights = {}
    for row in cert['weights']:
        require(type(row) is list and len(row) == 4 and all(type(v) is int for v in row),
                'integer weight row')
        a, b, c, weight = row
        require(0 <= a < b < c < 15 and weight > 0, 'weight label/sign')
        index = TRIPLE_INDEX[(a, b, c)]
        require(index not in weights and not (covered & (1 << index)), 'duplicate/covered weight')
        weights[index] = weight
    allowed = [w for w in old_words if not (triples(w) & covered)]
    require(all(all((w & b).bit_count() <= 2 for b in words) for w in allowed),
            'residual decoding check')
    # Cross-check the entire universe, including excluded words, literally.
    literal = [w for w in old_words if all((w & b).bit_count() <= 2 for b in words)]
    require(allowed == literal, 'residual triple/intersection universe disagreement')
    for w in allowed:
        require(sum(weights.get(TRIPLE_INDEX[t], 0) for t in combinations(points(w), 3)) >= 1000,
                'residual word not covered by weights')
    numerator = sum(weights.values())
    require(type(cert['numerator']) is int and numerator == cert['numerator'] <= 20556,
            'capacity numerator/uniform bound')
    require(cert['candidate_count'] == len(allowed) and
            cert['candidate_sha256'] == digest([points(w) for w in allowed]), 'residual universe binding')
    record = {'core_sha256': core['core_sha256'], 'candidate_count': len(allowed),
                    'weight_rows': len(weights), 'numerator': numerator, 'denominator': 1000,
                    'additional_bound': numerator//1000}
    return record, allowed


def capacity(cores, path):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == CERT_SHA, 'capacity source checksum')
    source = json.loads(raw)
    require(source['status'] == 'COMPLETE', 'capacity source incomplete')
    lookup = {c['core_sha256']: c for c in source['certificates']}
    require(len(lookup) == len(source['certificates']) == len(cores) == 226, 'certificate coverage count')
    require(set(lookup) == {c['core_sha256'] for c in cores}, 'certificate/core binding coverage')
    records, universes = [], []
    for core in cores:
        record, allowed = check_capacity_core(core, lookup[core['core_sha256']])
        records.append(record)
        universes.append((core['core_sha256'], allowed, record['additional_bound']))
    result = {'status': 'COMPLETE_EXACT', 'cores': len(records),
              'candidate_count_range': [min(r['candidate_count'] for r in records),
                                        max(r['candidate_count'] for r in records)],
              'additional_bound_census': dict(sorted(Counter(r['additional_bound'] for r in records).items())),
              'maximum_total_bound': 42+max(r['additional_bound'] for r in records),
              'certificate_sha256': hashlib.sha256(raw).hexdigest(), 'record_sha256': digest(records)}
    return result, records, universes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--cases', type=int, nargs='+', default=list(range(6)))
    parser.add_argument('--author-expected', type=Path)
    args = parser.parse_args()
    require(len(args.cases) == len(set(args.cases)) and set(args.cases) <= set(range(6)) and args.cases,
            'case domain')
    args.work.mkdir(parents=True, exist_ok=True)
    native = Ordered(args.native.resolve())
    try:
        summary, cores = reconstruct(native, args.work, sorted(args.cases))
    finally:
        native.close()
    (args.work/'summary.json').write_bytes(encode(summary))
    result = {'status': 'COMPLETE_SELECTED_CASES', 'enumeration': summary,
              'native': {'requests': native.requests, 'nodes': native.nodes,
                         'largest_request_nodes': native.largest_request}}
    if set(args.cases) == set(range(6)):
        cap, records, universes = capacity(cores, args.certificate)
        result.update(status='COMPLETE', capacity=cap)
        from color_certificate import check as check_color_certificate
        exceptional = [row for row in universes if row[2] == 20]
        require(len(exceptional) == 1, 'unique twenty-bound residual carrier')
        core_hash, words, _ = exceptional[0]
        color_cert = json.loads((HERE/'COLOR_CERT.json').read_text())
        color_result = check_color_certificate(color_cert, core_hash, words)
        result['refinement'] = {'maximum_total_bound': 61,
                                'vertex_disjointness_size_threshold': 62,
                                'additional_bound_census': dict(sorted(Counter(
                                    min(r['additional_bound'], 19) for r in records).items())),
                                'color_certificate': color_result,
                                'color_certificate_sha256': hashlib.sha256(
                                    (HERE/'COLOR_CERT.json').read_bytes()).hexdigest()}
        (args.work/'capacity-records.json').write_bytes(encode(records))
        (args.work/'residual-universes.json').write_bytes(encode(universes))
        if args.author_expected:
            expected = json.loads(args.author_expected.read_text())
            author = expected['enumeration']
            logical = {'cells': author['cells'], 'cases': [], 'status': author['status'],
                       'core_count': author['core_count']}
            for original in author['cases']:
                case = dict(original)
                case.pop('cover_nodes')
                case['counts'] = {k: v for k, v in case['counts'].items() if not k.endswith('_nodes')}
                logical['cases'].append(case)
            require(encode(logical) == encode(summary), 'author full-carrier logical record mismatch')
            require(encode(cap) == encode(expected['capacity']), 'author capacity record mismatch')
        own_expected = HERE/'EXPECTED.json'
        if own_expected.exists():
            require(encode(result) == own_expected.read_bytes(), 'independent expected record mismatch')
    (args.work/'result.json').write_bytes(encode(result))
    print(json.dumps({k: v for k, v in result.items() if k != 'enumeration'}), flush=True)


if __name__ == '__main__':
    main()
