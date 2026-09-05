#!/usr/bin/env python3
"""Find four blue-triangle witnesses in each residual marked-action core."""
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parent
PREV = ROOT.parent/'ramsey_r55_order3_eleven_residual_sweep'
PINS = {'result.json': 'aa6fe619507d058d69aadf36f5ef92ec7bc073f5cfab2d1e99b3191d8b2e658c',
        'cases.json': 'b14870da74f34b18f326b649be79452d05ff6517dcf21a86af47b7caad3c3a65'}


def require(ok, why):
    if not ok:
        raise ValueError(why)


def inputs():
    data = {}
    for name, pin in PINS.items():
        raw = (PREV/name).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == pin, 'input changed '+name)
        data[name] = json.loads(raw)
    open_indices = data['result.json']['open']
    require(len(open_indices) == len(set(open_indices)) == 45, 'residual domain')
    rows = [r for r in data['cases.json'] if r['index'] in open_indices]
    require([r['index'] for r in rows] == open_indices, 'ordered coverage')
    return rows


def red(bits, a, b):
    i, x = divmod(a, 3)
    j, y = divmod(b, 3)
    if i == j:
        return True
    if i > j:
        i, j, x, y = j, i, y, x
    pair = list(combinations(range(4), 2)).index((i, j))
    return bits[3*pair+(y-x) % 3] == '1'


def classify():
    rows = []
    for case in inputs():
        witnesses = []
        for omit in range(4):
            triangles = [i for i in range(4) if i != omit]
            found = None
            for phases in product(range(3), repeat=3):
                vertices = [3*i+p for i, p in zip(triangles, phases)]
                if all(not red(case['bits'], a, b) for a, b in combinations(vertices, 2)):
                    found = vertices
                    break
            witnesses.append(found)
        rows.append(dict(case, blue_triangles=witnesses,
                         forces_empty=all(w is not None for w in witnesses)))
    selected = [r['index'] for r in rows if r['forces_empty']]
    return dict(format='r55-k11-r4-empty-signature-v1', rows=rows,
                selected=selected, other=[r['index'] for r in rows if not r['forces_empty']],
                selected_labeled=sum(r['labeled'] for r in rows if r['forces_empty']))


def fixture(bits, signatures):
    edges = [[a,b] for a,b in combinations(range(12),2) if red(bits,a,b)]
    for f, signature in enumerate(signatures,12):
        edges += [[v,f] for v in range(12) if signature >> (v//3) & 1]
    edges += [[12+i,12+j] for i,j in combinations(range(len(signatures)),2)
              if signatures[i] & signatures[j] == 0]
    return dict(vertices=12+len(signatures), core_bits=bits, signatures=signatures,
                red_edges=sorted(edges))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    args = p.parse_args()
    args.work.mkdir(parents=True,exist_ok=True)
    result = classify()
    (args.work/'classification.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    first = next(r for r in result['rows'] if r['index']==87)
    weakened = next(r for r in result['rows'] if r['index']==194)
    fixtures = dict(local_zero_empty=fixture(first['bits'],[1,2,4,8,3,5,9,6,10,12]),
                    repeated_singleton=fixture(weakened['bits'],[1,1]))
    (args.work/'fixtures.json').write_text(json.dumps(fixtures,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['selected','other','selected_labeled']}))


if __name__ == '__main__':
    main()
