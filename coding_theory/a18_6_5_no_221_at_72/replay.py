#!/usr/bin/env python3
"""Independent linked-list replay of every completed production C-model."""
import argparse
from itertools import combinations, product
import json
from pathlib import Path
import resource
import subprocess
import time
import mixed_carrier as c
import helpers as p
from census import save

HERE = p.WORK


def image(edges, permutation):
    return tuple(sorted(tuple(sorted(permutation[z] for z in edge)) for edge in edges))


def run(shape, max_models):
    templates = json.loads((HERE / 'first_star_templates.json').read_text())
    template = templates[shape]
    baseline = json.loads((HERE / 'mixed_row_baseline.json').read_text())['cases'][shape]
    source = json.loads((HERE / f'census_s{shape}.json').read_text())
    raw_c_orbits = json.loads((HERE / f'c_orbits_s{shape}.json').read_text())
    group = raw_c_orbits['groups']
    group_set = set(map(tuple, group))
    first = [frozenset(p.points(w | (1 << 17))) for w in template['star']]
    for perm in group:
        if sorted(perm) != list(range(18)) or perm[:3] != [0, 1, 2] or perm[17] != 17:
            raise RuntimeError('bad literal first-star permutation')
        if {frozenset(perm[z] for z in q) for q in first} != set(first):
            raise RuntimeError('permutation does not preserve literal first star')
    if tuple(range(18)) not in group_set or any(tuple(a[b[z]] for z in range(18)) not in group_set
                                               for a, b in product(group, repeat=2)):
        raise RuntimeError('literal group not closed')
    csets = set(combinations(range(1, 17), 3))
    independent_c_reps = []
    while csets:
        q = min(csets)
        orbit = {tuple(sorted(perm[z] for z in q)) for perm in group}
        if not orbit <= csets:
            raise RuntimeError('literal C orbit overlap')
        csets.difference_update(orbit)
        independent_c_reps.append(q)
    if list(map(list, independent_c_reps)) != raw_c_orbits['c_reps']:
        raise RuntimeError('literal C representative mismatch')
    candidate_sets = [frozenset(q) for q in combinations(range(1, 17), 4)
                      if all(len((frozenset(q) | {0}) & a) <= 2 for a in first)]
    masks = [sum(1 << z for z in q) for q in candidate_sets]
    if masks != baseline['candidate_quadruples']:
        raise RuntimeError('literal second-star candidate mismatch')
    pair_list = list(combinations(range(1, 17), 2))
    pair_index = {edge: i for i, edge in enumerate(pair_list)}
    common_pairs = set().union(*(set(combinations(t, 2)) for t in baseline['common_triples']))
    rowtext = [f'120 {len(masks)} 6']
    for w, q in sorted(zip(masks, candidate_sets)):
        rowtext.append(str(w) + ' ' + ' '.join(str(pair_index[e]) for e in combinations(sorted(q), 2)))
    target_path = HERE / f'replay_s{shape}.json'
    if target_path.exists():
        state = json.loads(target_path.read_text())
        if state['definition_sha256'] != source['definition_sha256']:
            raise RuntimeError('replay resume definition mismatch')
    else:
        state = dict(agent='six-code-3', role='researcher', status='INCOMPLETE separate replay',
                     shape=shape, definition_sha256=source['definition_sha256'], completed_models=[])
    completed = {v['c_index']: v for v in state['completed_models']}
    count = 0
    for model in source['completed_models']:
        ci = model['c_index']
        if ci in completed:
            continue
        if count >= max_models:
            break
        started = time.monotonic()
        q = independent_c_reps[ci]
        if list(q) != model['c']:
            raise RuntimeError('wrong C index in production')
        h, stats = c.carrier_independent(baseline['common_triples'], q)
        if p.digest(h) != model['raw_h_sha256'] or len(h) != model['raw_h']:
            raise RuntimeError('independent carrier entry mismatch')
        stabilizer = [perm for perm in group if tuple(sorted(perm[z] for z in q)) == q]
        unseen = set(h)
        reps = []
        for leave in h:
            if leave not in unseen:
                continue
            orbit = {image(leave, perm) for perm in stabilizer}
            if not orbit <= unseen:
                raise RuntimeError('independent leave orbit overlap')
            unseen.difference_update(orbit)
            reps.append(leave)
        if unseen:
            raise RuntimeError('independent leave orbit coverage incomplete')
        if p.digest(reps) != model['h_representatives_sha256'] or len(reps) != model['h_orbits']:
            raise RuntimeError('independent leave representatives differ')
        expected = {}
        for positive in model['positives']:
            expected.setdefault(positive['h_index'], []).append(positive['cover'])
        for v in expected.values():
            v.sort()
        nodes = 0
        maximum_nodes = 0
        positives = 0
        for lower in range(0, len(reps), 512):
            batch = reps[lower:lower + 512]
            inp = HERE / f'replay_active_s{shape}.input'
            out = HERE / f'replay_active_s{shape}.jsonl'
            lines = rowtext + [str(len(batch))]
            for i, leave in enumerate(batch):
                missing = sorted(pair_index[e] for e in set(leave) | common_pairs)
                lines.append(f'{i} {len(missing)} ' + ' '.join(map(str, missing)))
            inp.write_text('\n'.join(lines) + '\n')
            result = subprocess.run([str(HERE / 'dlx'), str(inp), str(out)],
                                    capture_output=True, text=True, timeout=60)
            if result.returncode:
                save(HERE / f'replay_incomplete_s{shape}.json', dict(status='INCOMPLETE; no exclusion',
                     c_index=ci, lower=lower, stdout=result.stdout, stderr=result.stderr))
                raise RuntimeError('INCOMPLETE linked-list replay: ' + result.stderr)
            native = [json.loads(s) for s in out.read_text().splitlines()]
            if [v['index'] for v in native] != list(range(len(batch))):
                raise RuntimeError('linked-list replay fiber coverage mismatch')
            for v in native:
                if v['covers'] != expected.get(lower + v['index'], []):
                    raise RuntimeError('entrywise linked-list covers differ')
                nodes += v['nodes']
                maximum_nodes = max(maximum_nodes, v['nodes'])
                positives += len(v['covers'])
        record = dict(c_index=ci, c=q, h_orbits=len(reps), nodes=nodes,
                      max_nodes=maximum_nodes, covers=positives,
                      seconds=round(time.monotonic() - started, 6),
                      independent_carrier_stats=stats)
        completed[ci] = record
        count += 1
        state['completed_models'] = [completed[i] for i in sorted(completed)]
        state['maxrss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if len(completed) == source['c_orbits']:
            state['status'] = 'COMPLETE entrywise linked-list cover replay'
        save(target_path, state)
        print(json.dumps({k: v for k, v in record.items() if k != 'independent_carrier_stats'}), flush=True)
    print(json.dumps(dict(shape=shape, status=state['status'], completed=len(completed),
                          total=source['c_orbits'], new_models=count)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--shape', type=int, choices=range(3), required=True)
    parser.add_argument('--max-models', type=int, default=1000)
    args = parser.parse_args()
    if args.max_models < 1:
        raise RuntimeError('positive model count required')
    run(args.shape, args.max_models)
