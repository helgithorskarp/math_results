#!/usr/bin/env python3
"""Resumable exact mixed-row production, checkpointed at each C orbit."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import resource
import subprocess
import time
import mixed_carrier as c
import helpers as p

HERE = p.WORK


def save(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n')
    temporary.replace(path)


def run(shape, max_models):
    started = time.monotonic()
    templates = json.loads((HERE / 'first_star_templates.json').read_text())
    baseline = json.loads((HERE / 'mixed_row_baseline.json').read_text())['cases']
    template = templates[shape]
    saved = baseline[shape]
    triples = saved['common_triples']
    t = set().union(*(set(q) for q in triples))
    groups = p.m.automorphisms(template['star'])
    csets = list(combinations(range(1, 17), 3))
    c_reps = [q for q in csets if q == min(tuple(sorted(g[z] for z in q)) for g in groups)]
    if {tuple(sorted(g[z] for z in q)) for q in c_reps for g in groups} != set(csets):
        raise RuntimeError('C orbit cover mismatch')
    pairs = list(combinations(range(1, 17), 2))
    pair_index = {e: i for i, e in enumerate(pairs)}
    common_pairs = set().union(*(set(combinations(z, 2)) for z in triples))
    rowtext = [f'120 {len(saved["candidate_quadruples"])} 6']
    for w in sorted(saved['candidate_quadruples']):
        rowtext.append(str(w) + ' ' + ' '.join(str(pair_index[e]) for e in combinations(p.points(w), 2)))
    definition = dict(shape=shape, template=template['star'], triples=triples,
                      candidates=saved['candidate_quadruples'], groups=groups, c_reps=c_reps)
    fingerprint = p.digest(definition)
    state_path = HERE / f'census_s{shape}.json'
    if state_path.exists():
        state = json.loads(state_path.read_text())
        if state['definition_sha256'] != fingerprint:
            raise RuntimeError('resume definition differs')
    else:
        state = dict(agent='six-code-3', role='researcher', status='INCOMPLETE; no universal exclusion',
                     shape=shape, definition_sha256=fingerprint, c_orbits=len(c_reps),
                     completed_models=[], elapsed_seconds=0.0)
    completed = {record['c_index']: record for record in state['completed_models']}
    if len(completed) != len(state['completed_models']) or any(q not in range(len(c_reps)) for q in completed):
        raise RuntimeError('bad resumed model indices')
    count = 0
    for c_index, q in enumerate(c_reps):
        if c_index in completed:
            continue
        if count >= max_models:
            break
        model_started = time.monotonic()
        h, stats = c.carrier(triples, q)
        independent, independent_stats = c.carrier_independent(triples, q)
        if h != independent:
            raise RuntimeError('entrywise carrier mismatch')
        stabilizer = [g for g in groups if tuple(sorted(g[z] for z in q)) == q]
        c_orbit = {tuple(sorted(g[z] for z in q)) for g in groups}
        rep_h = []
        orbit_weight = 0
        for v in h:
            c.validate_h(triples, q, v)
            orbit = {p.edge_image(v, g) for g in stabilizer}
            if v == min(orbit):
                rep_h.append(v)
                orbit_weight += len(orbit)
        if orbit_weight != len(h) or len(c_orbit) * len(stabilizer) != len(groups):
            raise RuntimeError('orbit-size accounting mismatch')
        hset = set(h)
        if {p.edge_image(v, g) for v in rep_h for g in stabilizer} != hset:
            raise RuntimeError('leave stabilizer domain coverage mismatch')
        positives = []
        total_nodes = 0
        max_nodes = 0
        total_covers = 0
        fiber_hashes = []
        native_seconds = 0.0
        for lower in range(0, len(rep_h), 512):
            batch = rep_h[lower:lower + 512]
            inp = HERE / f'active_s{shape}.input'
            out = HERE / f'active_s{shape}.jsonl'
            lines = rowtext + [str(len(batch))]
            for i, v in enumerate(batch):
                excluded = sorted(pair_index[e] for e in set(v) | common_pairs)
                if len(excluded) != 18:
                    raise RuntimeError('wrong old-pair exclusion count')
                lines.append(f'{i} 18 ' + ' '.join(map(str, excluded)))
            inp.write_text('\n'.join(lines) + '\n')
            native_started = time.monotonic()
            result = subprocess.run([str(HERE / 'bitset'), str(inp), str(out)],
                                    capture_output=True, text=True, timeout=60)
            native_seconds += time.monotonic() - native_started
            if result.returncode:
                save(HERE / f'incomplete_s{shape}.json', dict(status='INCOMPLETE; no exclusion',
                     c_index=c_index, c=q, lower=lower, batch_fibers=len(batch),
                     stdout=result.stdout, stderr=result.stderr))
                raise RuntimeError('INCOMPLETE native census: ' + result.stderr)
            records = [json.loads(s) for s in out.read_text().splitlines()]
            if [d['index'] for d in records] != list(range(len(batch))):
                raise RuntimeError('native batch coverage mismatch')
            total_nodes += sum(d['nodes'] for d in records)
            max_nodes = max(max_nodes, max(d['nodes'] for d in records))
            fiber_hashes.append(p.digest([d['covers'] for d in records]))
            for i, (v, record) in enumerate(zip(batch, records)):
                total_covers += len(record['covers'])
                for cover in record['covers']:
                    star = p.validate_second(template, triples, cover, v)
                    actual_c = tuple(z for z in range(1, 17) if sum(w >> z & 1 for w in star) == 4)
                    if actual_c != q:
                        raise RuntimeError('positive C profile mismatch')
                    positives.append(dict(h_index=lower + i, cover=cover, star=star))
            save(HERE / f'active_s{shape}_progress.json', dict(status='INCOMPLETE C model',
                 c_index=c_index, c=q, completed_fibers=lower + len(batch), total_fibers=len(rep_h)))
        record = dict(c_index=c_index, c=q, p=len(set(q) & t), c_orbit_size=len(c_orbit),
                      stabilizer_order=len(stabilizer), raw_h=len(h), h_orbits=len(rep_h),
                      raw_h_sha256=p.digest(h), h_representatives_sha256=p.digest(rep_h),
                      core_stats=stats, independent_carrier_stats=independent_stats,
                      native_nodes=total_nodes, native_max_nodes=max_nodes, covers=total_covers,
                      output_cover_batch_sha256s=fiber_hashes, positives=positives,
                      native_seconds=round(native_seconds, 6),
                      seconds=round(time.monotonic() - model_started, 6))
        completed[c_index] = record
        count += 1
        state['completed_models'] = [completed[i] for i in sorted(completed)]
        state['elapsed_seconds'] += record['seconds']
        state['last_maxrss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if len(completed) == len(c_reps):
            state['status'] = 'COMPLETE production second-star census; separate cover replay pending'
        save(state_path, state)
        print(json.dumps({k: v for k, v in record.items()
                          if k not in ('core_stats', 'independent_carrier_stats', 'output_cover_batch_sha256s', 'positives')}), flush=True)
    print(json.dumps(dict(shape=shape, status=state['status'], completed=len(completed), total=len(c_reps),
                          new_models=count, invocation_seconds=round(time.monotonic() - started, 6),
                          total_h_orbits=sum(d['h_orbits'] for d in completed.values()),
                          total_covers=sum(d['covers'] for d in completed.values()))), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--shape', type=int, choices=range(3), required=True)
    parser.add_argument('--max-models', type=int, default=1000)
    args = parser.parse_args()
    if args.max_models < 1:
        raise RuntimeError('positive model count required')
    run(args.shape, args.max_models)
