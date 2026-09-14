#!/usr/bin/env python3
"""Optional SAT producer; its answers are checked by verify.py."""
from hashlib import sha256
from pathlib import Path
import argparse
import base64
import json

from pysat.solvers import Cadical195


HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def x(v, c): return 4*v+c+1
def active(n, v): return 4*n+v+1


def graph_inputs(ids):
    union = json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/union_510.json').read_text())
    labels = [v for v, provenance in enumerate(union['provenance']) if '510' in provenance]
    index = {label: i for i, label in enumerate(labels)}
    edges = [(index[a], index[b]) for a, b in union['edges'] if a in index and b in index]
    rows = {r['centre_index']: r for r in json.loads(
        (REPO/'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json').read_text())}
    for j, centre in enumerate(ids): edges.extend((v, 510+j) for v in rows[centre]['neighbors'])
    if len(ids) == 2: edges.append((510, 511))
    return tuple(sorted(edges))


def cnf(n, edges):
    out = [[-active(n, v)]+[x(v, c) for c in range(4)] for v in range(510)]
    out.extend([[x(v, c) for c in range(4)] for v in range(510, n)])
    out.append([x(510, 0)])
    for a, b in edges:
        for c in range(4):
            row = [-x(a, c), -x(b, c)]
            if a < 510: row.insert(0, -active(n, a))
            if b < 510: row.insert(0, -active(n, b))
            out.append(row)
    return out


def pack(colours):
    raw = bytearray((len(colours)+3)//4)
    for i, c in enumerate(colours): raw[i//4] |= c << (2*(i % 4))
    return base64.b64encode(bytes(raw)).decode('ascii')


def stream_hash(words):
    h = sha256()
    for omitted, colours in enumerate(words):
        h.update(f"{omitted} {''.join('.' if i==omitted else str(c) for i,c in enumerate(colours))}\n".encode())
    return h.hexdigest()


def make_support(ids, conflict_limit):
    n = 510+len(ids); edges = graph_inputs(ids); formula = cnf(n, edges); words=[]; conflicts=0
    with Cadical195(bootstrap_with=formula) as solver:
        for omitted in range(510):
            assumptions=[-active(n,v) if v==omitted else active(n,v) for v in range(510)]
            before=solver.accum_stats().get('conflicts',0); solver.conf_budget(conflict_limit)
            answer=solver.solve_limited(assumptions=assumptions, expect_interrupt=True)
            conflicts += solver.accum_stats().get('conflicts',0)-before
            if answer is not True: raise RuntimeError(('non-SAT producer answer',ids,omitted,answer))
            positive={z for z in solver.get_model() if z>0}; colours=[]
            for v in range(n):
                choices=[c for c in range(4) if x(v,c) in positive]
                colours.append(0 if v==omitted else choices[0])
            if any(omitted not in (a,b) and colours[a]==colours[b] for a,b in edges):
                raise RuntimeError('bad decoded word')
            words.append(tuple(colours))
    return {'centre_ids':list(ids),'vertices':n,'edges':len(edges),'packed_singleton_words':[pack(w) for w in words],
            'word_stream_sha256':stream_hash(words)}, conflicts


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--conflicts',type=int,default=200000);args=ap.parse_args()
    if args.out.exists():raise FileExistsError(args.out)
    supports=[];stats=[]
    for ids in ((319,),(1074,1269)):
        support,conflicts=make_support(ids,args.conflicts);supports.append(support);stats.append({'centre_ids':list(ids),'conflicts':conflicts})
    data={'schema':1,'supports':supports}
    args.out.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'output':str(args.out),'supports':stats},sort_keys=True))


if __name__=='__main__':main()
