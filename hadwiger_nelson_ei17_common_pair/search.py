"""Optional numerical discovery only; the rigorous verifier needs no SAT package."""
import argparse
import json
import math
from itertools import combinations, product
from pathlib import Path
from pysat.solvers import Cadical195

HERE=Path(__file__).resolve().parent


def colour(raw):
    representatives=[]
    mapping=[]
    for z in raw:
        k=next((k for k,w in enumerate(representatives) if abs(z-w)<1e-8),None)
        if k is None:
            k=len(representatives);representatives.append(z)
        mapping.append(k)
    edges=[(i,j) for i,j in combinations(range(len(representatives)),2)
           if abs(abs(representatives[i]-representatives[j])-1)<1e-8]
    clauses=[[4*i+c+1 for c in range(4)] for i in range(len(representatives))]
    clauses += [[-4*i-c-1,-4*j-c-1] for i,j in edges for c in range(4)]
    clauses.append([1])
    with Cadical195(bootstrap_with=clauses) as solver:
        solver.conf_budget(300000)
        status=solver.solve_limited()
        if status is not True:
            raise RuntimeError('candidate requires investigation; no certified colouring')
        model=set(solver.get_model())
        word=''.join(str(next(c for c in range(4) if 4*i+c+1 in model))
                     for i in range(len(representatives)))
    return ''.join(word[i] for i in mapping)


def generate(output):
    p=[complex(*map(float,row)) for row in json.loads((HERE/'seed_midpoint.json').read_text())]
    groups=[]
    for i,j in combinations(range(17),2):
        distance=abs(p[j]-p[i])
        k=next((k for k,c in enumerate(groups) if abs(c['distance']-distance)<1e-9),None)
        if k is None:
            k=len(groups);groups.append(dict(distance=distance,pairs=[]))
        groups[k]['pairs'].append([i,j])
    certificate=[]
    for group in groups:
        raw=[]
        for i,j in group['pairs']:
            for reverse,mirror in product((False,True),repeat=2):
                a,b=(p[j],p[i]) if reverse else (p[i],p[j])
                rotation=(b-a).conjugate()/abs(b-a)
                for z in p:
                    w=(z-a)*rotation
                    raw.append(w.conjugate() if mirror else w)
        certificate.append(dict(pairs=group['pairs'],word=colour(raw)))
    raw=p[:]
    for i,j in combinations(range(17),2):
        a,b=p[i],p[j];d=abs(b-a)
        if 0<d<2:
            for sign in (-1,1):
                raw.append((a+b)/2+sign*1j*(b-a)*math.sqrt(1/d**2-.25))
    circle_word=colour(raw)
    output.mkdir(parents=True,exist_ok=True)
    (output/'fan_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    (output/'circle_word.txt').write_text(circle_word+'\n')
    print(json.dumps(dict(groups=len(groups),frames=4*sum(len(c['pairs']) for c in groups),
                          circle_labels=len(raw),output=str(output))))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=HERE/'out')
    generate(parser.parse_args().output)
