#!/usr/bin/env python3
"""Summarises the one-anchor enumeration (run2/stats.json, configs.json, filter.log) and the coverage result
(run2/cover.json) into the numbers needed for the README and the chain body.
usage: summarize_results.py RUNDIR"""
import json, sys
from pathlib import Path
from collections import Counter
R = Path(sys.argv[1])
stats = json.loads((R / 'stats.json').read_text())
print('anchors:', len(stats))
tot = Counter()
for st in stats:
    for k in ('groups2', 'disc_V', 'disc_QK', 'disc_QN', 'kept', 'kept_K2', 'kept_K1', 'kept_N', 'near_unresolved', 'typeI', 'typeII'):
        tot[k] += st[k]
print('group totals:', dict(tot))
print('max group size:', max(st['maxg'] for st in stats), 'seconds total:', round(sum(st['seconds'] for st in stats)))
# distinct candidate points by rounded coordinates
pts = {}
for st in stats:
    for p in st['points']:
        key = (round(p['x'][0], 6), round(p['x'][1], 6))
        pts.setdefault(key, []).append((st['anchor'], len(p['nbrs']), len(p['gens'])))
nv = Counter(len(set(a for a, _, _ in v)) for v in pts.values())
print('distinct candidate points:', len(pts), ' by number of anchors they were found from:', dict(sorted(nv.items())))
ng = Counter(max(g for _, _, g in v) for v in pts.values())
print('by Q-degree (max group size):', dict(sorted(ng.items())))
confs = json.loads((R / 'configs.json').read_text())
print('configurations (distinct point sets):', len(confs), Counter(c['type'] for c in confs))
edge_pat = Counter(tuple(sorted(tuple(e) for e in c['edges'])) for c in confs)
print('internal edge patterns:', {str(k): v for k, v in edge_pat.most_common(8)})
if (R / 'filter.log').exists():
    print('filter:', (R / 'filter.log').read_text().strip())
if (R / 'configs_f.json').exists():
    cf = json.loads((R / 'configs_f.json').read_text()); print('filtered configurations:', len(cf), Counter(c['type'] for c in cf))
if (R / 'cover.json').exists():
    cov = json.loads((R / 'cover.json').read_text())
    print('cover: n_configs', cov['n_configs'], 'histogram |Û(A)|', cov['histogram'], 'candidates', cov['candidates'])
    print('declared pairs:', len(cov['status']), Counter(cov['status'].values()), 'fresh rows:', len(cov['new_rows']))
    print('direct tests:', len(cov['direct']), Counter(d['status'] for d in cov['direct']))
