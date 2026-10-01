"""Exact centralizer partition of all three-promotion/three-join cases."""
import argparse
import hashlib
import json
import resource
import time
from collections import Counter
from itertools import combinations
from pathlib import Path

import model as m
MODEL = Path(__file__).resolve().parent/'model.py'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise ValueError('refusing to overwrite case inventory')
    started = time.monotonic()
    g = m.geometry()
    maps = m.centralizer(g)
    effective = sorted(set(tuple(tuple(x) for x in entry) for entry in maps))
    m.need(len(effective) == 6, 'effective centralizer order')
    counts = Counter()
    for J in combinations(range(7), 3):
        for P in combinations(range(35), 3):
            key = min((tuple(sorted(v[i] for i in J)),
                       tuple(sorted(b[i] for i in P))) for v, r, b in effective)
            counts[key] += 1
    m.need(sum(counts.values()) == 229075, 'labeled case coverage')
    m.need(all(6 % w == 0 for w in counts.values()), 'orbit cardinality')
    cases = []
    for index, ((J, P), weight) in enumerate(sorted(counts.items())):
        orbit = {(tuple(sorted(v[i] for i in J)), tuple(sorted(b[i] for i in P)))
                 for v, r, b in effective}
        m.need(len(orbit) == weight, 'explicit orbit size vs complete-domain count')
        cases.append(dict(index=index, joins=J, promotions=P, weight=weight))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    text = ''.join(' '.join(map(str, [c['index'], *c['joins'], *c['promotions'], c['weight']]))+'\n'
                   for c in cases)
    args.output.write_text(text)
    metadata = dict(status='COMPLETE', representatives=len(cases), labeled=229075,
                    multiplicities=dict(sorted(Counter(counts.values()).items())),
                    manifest_sha256=hashlib.sha256(text.encode()).hexdigest(),
                    source_hashes={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in (Path(__file__), MODEL)},
                    seconds=time.monotonic()-started,
                    peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    args.output.with_suffix('.json').write_text(json.dumps(metadata, indent=2, sort_keys=True)+'\n')
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
