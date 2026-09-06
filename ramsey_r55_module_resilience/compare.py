#!/usr/bin/env python3
"""Local-invariant comparison with the 21 previously published saved graphs."""
import hashlib
import itertools
import json
from pathlib import Path


def run():
    source = Path(__file__).resolve().parent.parent / 'ramsey_r55_c5_semidirect_c8_cayley_obstruction' / 'novelty_fixtures.json'
    raw = source.read_bytes()
    data = json.loads(raw)
    out = []
    for rec in data['records']:
        bits = int(rec['red_edge_bits_hex'],16)
        rows = [0]*43
        for i,(u,v) in enumerate(itertools.combinations(range(43),2)):
            if bits >> i & 1:
                rows[u] |= 1 << v
                rows[v] |= 1 << u
        pairmin = min(((rows[u]^rows[v]) & ~((1 << u)|(1 << v))).bit_count()
                      for u,v in itertools.combinations(range(43),2))
        tmin = {'monochromatic':40, 'mixed':40}
        violations = {'monochromatic':0, 'mixed':0}
        for q in itertools.combinations(range(43),3):
            u,v,w = q
            mixed = ((rows[u]^rows[v]) | (rows[u]^rows[w])) & ~sum(1 << x for x in q)
            d = mixed.bit_count()
            name = 'monochromatic' if len({rows[a] >> b & 1 for a,b in itertools.combinations(q,2)})==1 else 'mixed'
            tmin[name] = min(tmin[name],d)
            if d < (18 if name=='monochromatic' else 17): violations[name] += 1
        out.append({'name':rec['name'],'minimum_pair_distinguishers':pairmin,
                    'minimum_triple_distinguishers':tmin,'triple_violations':violations})
    return {'fixture_sha256':hashlib.sha256(raw).hexdigest(),
            'scope':'Local pair/triple checks only; no whole module-family separation or Ramsey verdict.',
            'records':out}


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
