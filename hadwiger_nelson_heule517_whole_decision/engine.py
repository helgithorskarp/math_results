#!/usr/bin/env python3
"""Full graph and complete target-frontier input for one bounded decision."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
spec = importlib.util.spec_from_file_location('full_h517',REPO/'hadwiger_nelson_heule517_family_pilot/engine.py')
P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)


def inputs(frontier):
    for name,digest in json.loads((HERE/'manifest.json').read_text()).items():
        P.require(sha256((REPO/name).read_bytes()).hexdigest() == digest, ('input hash',name))
    expected = json.loads((REPO/'hadwiger_nelson_heule517_whole_cover/result.json').read_text())
    raw = frontier.read_bytes()
    P.require(sha256(raw).hexdigest() == expected['frontier_sha256'], 'complete initial frontier')
    tuples = [tuple(map(int,line.split(','))) for line in raw.decode('ascii').splitlines()]
    P.require(len(tuples) == expected['residual'] == 39453 and tuples == sorted(set(tuples)), 'initial tuple count and order')
    P.require(all(len(t) == 9 and t == tuple(sorted(set(t))) and min(t) >= 0 and max(t) < 517 for t in tuples), 'omission tuples')
    data = P.geometry()
    large = [v for v,p in enumerate(data['points']) if all(p[a][k] == 0 for a in (0,1) for k in (2,3,6,7))]
    L = set(large); small = sorted(set(range(517))-L)
    buckets = {i:[] for i in range(5,10)}
    for t in tuples: buckets[len(set(t) & L)].append(t)
    P.require({str(i):len(ts) for i,ts in buckets.items()} == expected['residual_by_large_omissions'], 'complete block histogram')
    data.update(large=large,small=small)
    return data,buckets


def prune(buckets,omitted):
    mask = sum(1 << v for v in omitted)
    for i,tuples in buckets.items():
        buckets[i] = [t for t in tuples if sum(1 << v for v in t) & mask != mask]


def stream(buckets):
    return ''.join(','.join(map(str,t))+'\n' for t in sorted(t for ts in buckets.values() for t in ts)).encode('ascii')
