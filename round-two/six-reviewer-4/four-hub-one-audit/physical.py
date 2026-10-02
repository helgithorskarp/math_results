"""Definition-level physical rows; earlier owned row compiler is credited input.
Every hub placement is labelled. No target source/certificate is imported.
"""
from itertools import combinations, permutations
from collections import Counter, defaultdict
from rows import census, need, encoded
from populations import project, types_of
import hashlib, json, time

def catalogue(stars):
    raw = project(census(stars))
    types = types_of(raw)
    need(len(raw) == 426 and len(types) == 60, 'raw carrier/types')
    mapping = {(r['fixture'], tuple(r['hubs'])): r for r in raw}
    decisions = bytearray()
    frequency = Counter()
    options = defaultdict(set)
    # Full (type, HHH-mask, hub deficits, LOW-SAT friend counts) frequencies.
    signatures = Counter()
    start = time.monotonic()
    for sid, blocks in enumerate(stars):
        replication = [sum(p in b for b in blocks) for p in range(17)]
        deficit = [5-r for r in replication]
        covered = {tuple(p) for b in blocks for p in combinations(sorted(b),2)}
        adjacency = [set() for _ in range(17)]
        for u,v in combinations(range(17),2):
            if (u,v) not in covered:
                adjacency[u].add(v); adjacency[v].add(u)
        low = {p for p in range(17) if not deficit[p]}
        for hubs in combinations(range(17),4):
            hs = set(hubs)
            row = mapping[sid, tuple(p for p in hubs if deficit[p])]
            t = (row['e'],row['k'],row['q'],row['eligible'],tuple(row['colors']),row['psi'],row['margin3'])
            tid = types.index(t)
            ls = low-hs
            friends = [len(adjacency[p] & ls) if deficit[p] else 0 for p in range(17)]
            sat_ok = all(deficit[p]+friends[p] <= 5 for p in range(17) if p not in hs and deficit[p])
            for heavy in hubs:
                ok = sat_ok and all(deficit[p]+friends[p] <= (13 if p==heavy else 9) for p in hubs if deficit[p])
                decisions.append(int(ok))
                if not ok: continue
                frequency[tid] += 1
                light = [p for p in hubs if p != heavy]
                for rest in permutations(light):
                    named = (heavy,)+rest
                    triples = list(combinations(range(4),3))
                    mask = sum(1<<i for i,triple in enumerate(triples)
                               if any(set(named[a] for a in triple) <= set(b) for b in blocks))
                    ds = tuple(deficit[p] for p in named)
                    fs = tuple(friends[p] for p in named)
                    signatures[tid,mask,ds,fs] += 1
                    for a in range(4): options[tid,mask,a].add((ds[a],fs[a]))
        need(time.monotonic()-start < 60, 'INCOMPLETE physical60s guard')
    return {'types':types,'raw':raw,'decisions_sha256':hashlib.sha256(decisions).hexdigest(),
            'marks':len(decisions),'accepted':sum(decisions),'frequency':sorted(frequency.items()),
            'signatures':sorted((list(k[:2])+[list(k[2]),list(k[3])],v) for k,v in signatures.items()),
            'options':sorted(([tid,mask,a],sorted(opts)) for (tid,mask,a),opts in options.items())}

if __name__ == '__main__':
    from pathlib import Path
    p=Path(__file__).resolve().parent
    z=catalogue(json.loads((p/'fixtures.json').read_bytes())['stars'])
    (p/'physical-local.json').write_bytes(encoded(z))
    print(json.dumps({k:z[k] for k in ('marks','accepted','frequency','decisions_sha256')},sort_keys=True))
