#!/usr/bin/env python3
"""Frozen 32-candidate screen; exact CM-field geometry, capped SAT discovery."""
import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import product
import ctypes
import json
from pathlib import Path
import time

CENTRES = [[0,0,0,0],[4,13,7,9],[0,6,13,9],[5,11,13,6],
           [10,14,14,6],[9,3,8,10],[6,14,10,3],[11,8,11,12]]
CAP = 100000


def norm16(v):
    a,b,c,d = v
    x,y,z = 4*a+2*b+2*c+d, 2*b+d, 2*c+d
    return x*x+213*d*d+3*y*y+71*z*z, -2*d*x+2*y*z


def rank(vectors):
    basis = {}
    for v in vectors:
        row = list(map(Fraction, v))
        for j in sorted(basis):
            if row[j]:
                factor = row[j]
                row = [a-factor*b for a,b in zip(row,basis[j])]
        if any(row):
            j = next(i for i,x in enumerate(row) if x)
            lead = row[j]
            basis[j] = [x/lead for x in row]
            if len(basis) == 4:
                return 4
    return len(basis)


def window(h):
    rows = []
    for v in product(range(-10,11),range(-10,11),range(-3,4),range(-3,4)):
        score = norm16(tuple(16*x-y for x,y in zip(v,h)))[0]
        rows.append((score,v))
    chosen = sorted(rows)[:508]
    threshold = chosen[-1][0]
    # Dual quadratic-form bounds exclude every point outside the scan box.
    if not all(6*threshold < 71*(176-h[j])**2 for j in (0,1)):
        raise ValueError('a/b window truncation')
    if not all(threshold < 213*(64-h[j])**2 for j in (2,3)):
        raise ValueError('c/d window truncation')
    points = [v for score,v in chosen]
    edges, directions = defaultdict(list), defaultdict(set)
    for i,v in enumerate(points):
        for j,w in enumerate(points[:i]):
            delta = tuple(a-b for a,b in zip(v,w))
            n = norm16(delta)
            edges[n].append([j,i])
            directions[n].add(delta)
    selected = []
    screened = []
    for n in sorted(edges,key=lambda n:(-len(edges[n]),n)):
        r = rank(sorted(directions[n]))
        screened.append({'norm16':list(n),'edges':len(edges[n]),'step_rank':r})
        if r == 4:
            selected.append({'norm16':list(n),'edges':sorted(edges[n]),
                             'step_rank':r,'observed_step_vectors':len(directions[n])})
            if len(selected) == 4:
                break
    if len(selected) != 4:
        raise ValueError('fewer than four rank-four fibres')
    return {'centre16':h,'points':points,'threshold':threshold,
            'screened':screened,'candidates':selected}


def cnf(vertices,edges,colours=4):
    clauses = []
    for v in range(vertices):
        xs = [colours*v+c+1 for c in range(colours)]
        clauses.append(xs)
        clauses.extend([-xs[a],-xs[b]] for a in range(colours) for b in range(a))
    clauses.extend([-colours*a-c-1,-colours*b-c-1] for a,b in edges for c in range(colours))
    # Pin a genuine unit triangle; every proper colouring can rename it.
    adjacency = [set() for _ in range(vertices)]
    for a,b in edges:
        adjacency[a].add(b);adjacency[b].add(a)
    triangle = None
    for a,b in edges:
        common = adjacency[a] & adjacency[b]
        if common:
            triangle = [a,b,min(common)]
            clauses.extend([[colours*v+c+1] for c,v in enumerate(triangle)])
            break
    return clauses,triangle


def dump_cnf(path,n,clauses):
    path.write_text(f'p cnf {n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))


def solve_candidate(w,index,work):
    from pysat.solvers import Solver
    edges = w['candidates'][index]['edges']
    clauses,triangle = cnf(508,edges)
    started = time.monotonic()
    with Solver(name='cadical195',bootstrap_with=clauses,with_proof=True) as solver:
        solver.conf_budget(CAP)
        result = solver.solve_limited()
        stats = solver.accum_stats()
        record = {'status':'SAT' if result is True else 'UNSAT' if result is False else 'UNKNOWN',
                  'seconds':time.monotonic()-started,'stats':stats,'triangle_pin':triangle,
                  'variables':2032,'clauses':len(clauses),'conflict_cap':CAP}
        if result is True:
            positive = {x for x in solver.get_model() if x>0}
            colours = []
            for v in range(508):
                choices = [c for c in range(4) if 4*v+c+1 in positive]
                if len(choices)!=1:raise ValueError('non-one-hot model')
                colours.append(choices[0])
            if any(colours[a]==colours[b] for a,b in edges):raise ValueError('improper model')
            record['colouring']=''.join(map(str,colours))
        else:
            dump_cnf(work/'query.cnf',2032,clauses)
            if result is False:
                # Flush the C FILE before python-sat reads its proof stream.
                ctypes.CDLL(None).fflush(None)
                proof=solver.get_proof()
                (work/'query.drat').write_text('\n'.join(proof)+'\n')
    return record


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--generate-only',action='store_true')
    args=p.parse_args();args.work.mkdir(exist_ok=True,parents=True)
    certificate={'format':1,'field':'Q(sqrt(-3),sqrt(-71))','vertices':508,
                 'candidate_cap':32,'conflict_cap':CAP,'windows':[]}
    for wi,h in enumerate(CENTRES):
        w=window(h)
        (args.work/f'window_{wi}.json').write_text(json.dumps(w,separators=(',',':'))+'\n')
        row={'centre16':h,'threshold':w['threshold'],'candidates':[]}
        for ci,candidate in enumerate(w['candidates']):
            case=args.work/f'case_{wi}_{ci}';case.mkdir(exist_ok=True)
            result={} if args.generate_only else solve_candidate(w,ci,case)
            entry={k:v for k,v in candidate.items() if k!='edges'}
            entry['edge_count']=len(candidate['edges']);entry.update(result)
            row['candidates'].append(entry)
            print(json.dumps({'window':wi,'case':ci,**{k:v for k,v in entry.items() if k!='colouring'}},sort_keys=True),flush=True)
            if result.get('status')=='UNSAT':
                certificate['windows'].append(row)
                certificate['stopped_on_signal']=True
                (args.work/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
                return
        certificate['windows'].append(row)
        (args.work/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    certificate['stopped_on_signal']=False
    (args.work/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')


if __name__=='__main__':main()
