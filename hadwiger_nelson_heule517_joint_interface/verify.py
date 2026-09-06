#!/usr/bin/env python3
"""Independent exact separator, witness and CNF audit; optional DRAT replay."""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
EXPONENTS = [(i & 1, (i >> 1) & 1, (i >> 2) & 1) for i in range(8)]


def require(condition, detail):
    if not condition: raise ValueError(detail)


def product(x, y):
    out = [0]*8
    for i, a in enumerate(x):
        if not a: continue
        for j, b in enumerate(y):
            if not b: continue
            exponents = [u+v for u,v in zip(EXPONENTS[i], EXPONENTS[j])]
            coefficient = a*b
            for e, prime in zip(exponents, [3,5,11]): coefficient *= prime**(e//2)
            k = sum((e % 2)*2**q for q,e in enumerate(exponents))
            out[k] += coefficient
    return out


def graph():
    for name, digest in json.loads((HERE/'manifest.json').read_text()).items():
        require(sha256((REPO/name).read_bytes()).hexdigest() == digest, ('input hash',name))
    old = json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json').read_text())
    labels = [v for v in range(553) if '510' in old['provenance'][v]]
    fresh = json.loads((REPO/'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json').read_text())
    added = [r for r in fresh if r['degree'] >= 7]
    require([r['centre_index'] for r in added] == [327,439,671,1040,1074,1377,1383], 'whole stratum')
    raw = [old['coordinates'][str(v)] for v in labels] + [r['coordinates'] for r in added]
    points = []
    for p in raw:
        require(len(p) == 2 and all(len(a) == 8 for a in p), 'point shape')
        axes = []
        for axis in p:
            xs = [96*Fraction(x) for x in axis]
            require(all(x.denominator == 1 for x in xs), 'common denominator')
            axes.append(tuple(int(x) for x in xs))
        points.append(tuple(axes))
    require(len(points) == len(set(points)) == 517, 'distinct support')
    edges = []
    for u,v in combinations(range(517), 2):
        diffs = [tuple(points[u][a][k]-points[v][a][k] for k in range(8)) for a in (0,1)]
        d = [a+b for a,b in zip(product(diffs[0],diffs[0]),product(diffs[1],diffs[1]))]
        if d == [96**2]+[0]*7: edges.append((u,v))
    return points, edges


def verify(work=None, drat=None):
    start = time.monotonic(); points, edges = graph()
    L = {v for v,p in enumerate(points) if all(p[a][k] == 0 for a in (0,1) for k in [2,3,6,7])}
    S = set(range(517))-L; cross = [e for e in edges if (e[0] in L) != (e[1] in L)]
    I = sorted({v for e in cross for v in e if v in L}); J = sorted({v for e in cross for v in e if v in S})
    le = [e for e in edges if set(e) <= L]; se = [e for e in edges if set(e) <= S]
    A = set(range(510,517)); B = sorted({u for u,v in edges if v in A})
    sep = dict(large=sorted(L),small=sorted(S),boundary=I,terminals=J,cross_edges=cross,large_edges=le)
    # JSON normalization preserves ordering and compares every entry.
    require(json.loads(json.dumps(sep)) == json.loads((HERE/'separator.json').read_text()), 'separator entrywise')
    require(len(L)==375 and len(S)==142 and len(le)==1920 and len(se)==605 and len(cross)==30, 'block counts')
    require(len(edges)==2555 and len(I)==19 and len(J)==30 and len(B)==48, 'interface counts')
    require(not any(v in A for e in cross for v in e) and not any(u in A for u,v in edges), 'independent noncontact additions')
    require(sum(u in B and v in B for u,v in edges)==67, 'direct-neighbour boundary')
    vertices = sorted(L); pos = {v:i for i,v in enumerate(vertices)}
    n = 4*len(vertices)
    clauses = [[4*i+1,4*i+2,4*i+3,4*i+4] for i in range(len(vertices))]
    for u,v in le:
        for c in range(4): clauses.append([-4*pos[u]-c-1,-4*pos[v]-c-1])
    clauses.append([4*pos[0]+1])
    def raw(cs): return (f'p cnf {n} {len(cs)}\n'+''.join(' '.join(str(v) for v in c)+' 0\n' for c in cs)).encode()
    base = raw(clauses)
    rows = json.loads((HERE/'certificate.json').read_text())['rows']; seen = set(); patterns=[]
    for row in rows:
        c = row['colouring']; p = row['pattern']
        require(len(c)==375 and set(c)<=set('0123'), 'full witness domain')
        require(c[pos[0]]=='0' and all(c[pos[u]]!=c[pos[v]] for u,v in le), 'large-block witness')
        require(p==''.join(c[pos[v]] for v in I) and len(p)==19, 'projection')
        rename={}; canonical=''
        for x in p:
            if x not in rename: rename[x]=str(len(rename))
            canonical += rename[x]
        require(p==canonical and p not in patterns, 'canonical distinct pattern')
        patterns.append(p)
        orbit = set()
        for perm in permutations('0123'):
            if perm[0]=='0': orbit.add(''.join(perm[int(x)] for x in p))
        require(not seen.intersection(orbit), 'disjoint pattern orbits'); seen.update(orbit)
        for s in sorted(orbit): clauses.append([-4*pos[v]-int(x)-1 for v,x in zip(I,s)])
    require(len(rows)==20 and len(seen)==120, 'complete claimed positive list')
    final = raw(clauses); proof_result=None
    if work:
        require((work/'base.cnf').read_bytes()==base, 'actual base CNF')
        require((work/'exhaustion.cnf').read_bytes()==final, 'actual exhaustion CNF')
        require(json.loads((work/'certificate.json').read_text())=={'rows':rows}, 'actual native witnesses')
        if drat:
            with (work/'independent_drat_check.log').open('w') as log:
                r=subprocess.run([str(drat),str(work/'exhaustion.cnf'),str(work/'exhaustion.drat')],stdout=log,stderr=subprocess.STDOUT)
            require(r.returncode==0 and 's VERIFIED' in (work/'independent_drat_check.log').read_text(), 'checked complete exhaustion')
            proof_result={'verified':True,'proof_bytes':(work/'exhaustion.drat').stat().st_size,
                          'proof_sha256':sha256((work/'exhaustion.drat').read_bytes()).hexdigest()}
    result={'status':'SEPARATOR,20 WITNESSES AND EXACT CNF VERIFIED', 'vertices':517,'edges':len(edges),
            'large_vertices':len(L),'small_vertices':len(S),'large_edges':len(le),'small_edges':len(se),
            'cross_edges':len(cross),'large_boundary':I,'small_terminals':J,'added_neighbour_union':B,
            'added_neighbour_union_edges':67,'added_to_base_edges':51,'canonical_patterns':len(rows),
            'origin_fixed_patterns':len(seen),'full_witness_edge_checks':len(rows)*len(le),
            'exact_pair_checks':517*516//2,'cnf_variables':n,'cnf_clauses':len(clauses),
            'cnf_sha256':sha256(final).hexdigest(),'proof':proof_result,
            'large_relation_complete':bool(proof_result),'full_H517_family_closed':False,
            'record_improvement':False,'seconds':time.monotonic()-start}
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path);ap.add_argument('--drat',type=Path);ap.add_argument('--report',type=Path)
    args=ap.parse_args();require(not args.drat or args.work, 'proof requires work directory')
    result=verify(args.work,args.drat)
    if args.report:args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
