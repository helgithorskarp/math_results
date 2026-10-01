#!/usr/bin/env python3
"""Exact coloring maxima for literal34-word Y18 anchors, with per-case saves."""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import resource
import time
import interface as Y
import color

M = Y.M


def run(args):
    started = time.monotonic()
    args.work.mkdir(parents=True, exist_ok=True)
    data = json.loads(args.inventory.read_text())
    anchors = data['anchors']
    anchor_hash = sha256(M.encoded(anchors)).hexdigest()
    M.require(data['anchors_sha256'] == anchor_hash and
              data['status'] in ('COMPLETE scoped positive-anchor inventory',
                                 'COMPLETE requested literal Y18 census') and anchors,
              'bad input inventory')
    indices = [int(i) for i in args.cases.split(',')] if args.cases else list(range(len(anchors)))
    resources, rows = M.orbit_carrier()
    records = []
    for i in indices:
        source = anchors[i]
        words = tuple(source['words'])
        available, adjacency = Y.finite_graph(words, resources, rows)
        graph_hash = sha256(M.encoded(dict(vertices=[r['representative'] for r in available],
                                         adjacency=adjacency))).hexdigest()
        path = args.work / f'case-{i:03}.json'
        if path.exists():
            record = json.loads(path.read_text())
            M.require(record['graph_sha256'] == graph_hash and record['anchor_sha256'] == anchor_hash,
                      'saved graph differs')
            if record['status'] == 'COMPLETE':
                records.append(record)
                continue
        begin = time.monotonic()
        try:
            alpha, maxima, nodes = color.maximum_cliques(adjacency)
        except color.Incomplete as e:
            record = dict(status='INCOMPLETE', case=i, graph_sha256=graph_hash,
                          anchor_sha256=anchor_hash, reason=str(e), seconds=time.monotonic()-begin,
                          mathematical_absence_proved=False)
            path.write_bytes(M.encoded(record))
            print(json.dumps(record, sort_keys=True), flush=True)
            records.append(record)
            break
        M.require(maxima and all(len(q) == alpha for q in maxima), 'bad maxima')
        witness = tuple(sorted(words + tuple(w for j in maxima[0] for w in available[j]['words'])))
        stats = M.check_code(witness)
        M.require(len(witness) == 34 + 2*alpha and stats['replications'][16:] == (20, 18),
                  'bad literal maximum witness')
        maxima_path = args.work / f'case-{i:03}.maxima.json'
        maxima_path.write_bytes(M.encoded(maxima))
        record = dict(status='COMPLETE', case=i, fixture=source['fixture'], matching=source.get('matching'),
                      fixed_Y=source.get('fixed_Y', 4),
                      vertices=len(available), alpha=alpha, maximum_families=len(maxima),
                      maxima_sha256=sha256(M.encoded(maxima)).hexdigest(), nodes=nodes,
                      words=len(witness), witness=witness, stats=stats,
                      graph_sha256=graph_hash, anchor_sha256=anchor_hash,
                      literal_graph_entrywise=True, seconds=time.monotonic()-begin)
        path.write_bytes(M.encoded(record))
        records.append(record)
        print(json.dumps({k:v for k,v in record.items() if k not in ('witness','stats')}, sort_keys=True), flush=True)
    summary = dict(agent='six-code-2', role='researcher', cases=len(records), requested_cases=len(indices),
                   inventory_cases=len(anchors), all_subfamily_coverage_claimed=False,
                   status='COMPLETE requested maxima' if len(records) == len(indices) and
                   all(r['status'] == 'COMPLETE' for r in records) else 'INCOMPLETE requested maxima',
                   anchor_sha256=anchor_hash, records=records,
                   maximum_words=max((r['words'] for r in records if r['status']=='COMPLETE'), default=None),
                   seconds=time.monotonic()-started, own_peak_RSS_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (args.work/'summary.json').write_bytes(M.encoded(summary))
    print(json.dumps({k:v for k,v in summary.items() if k!='records'}, sort_keys=True), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inventory', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--cases')
    run(p.parse_args())
