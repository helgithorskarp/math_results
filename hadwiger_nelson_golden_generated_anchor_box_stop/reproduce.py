#!/usr/bin/env python3
"""Regenerate one frozen physical graph; optional ordinary SAT word generation."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROWS=((0,0,0,0,5),(1,0,0,0,4),(0,0,0,1,4),(1,0,0,1,3),
      (0,1,0,0,4),(0,0,1,0,4),(1,0,1,0,3),(0,1,0,1,3),
      (1,1,0,0,3),(0,0,1,1,3),(1,1,0,1,2),(1,0,1,1,2),
      (0,1,1,0,3),(1,1,1,0,2),(0,1,1,1,2),(1,1,1,1,1))
POWERS=((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(-1,-1,-1,-1))
LAMBDA=(0,-1,0,-1)
UNIT=(3,0,1,1)

def need(ok,msg):
    if not ok: raise ValueError(msg)

def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def minus(a,b):return tuple(x-y for x,y in zip(a,b))
def times(a,b):
    c=[0]*7
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    for k in range(6,3,-1):
        for j in range(1,5):c[k-j]-=c[k]
    return tuple(c[:4])
def conjugate(a):
    a,b,c,d=a
    return (a-b,-b,d-b,c-b)
def source():return [tuple(sum(row[k]*POWERS[k][j] for k in range(5)) for j in range(4)) for row in ROWS]
def construct():
    B=source();d=[minus(POWERS[i],POWERS[4]) for i in range(4)]
    P={n:plus(B[0],times(LAMBDA,tuple(sum(n[k]*d[k][j] for k in range(4)) for j in range(4))))
       for n in itertools.product(range(4),range(4),range(4),range(7))}
    need(len(set(P.values()))==448,'grid collision');need(len(set(B)&set(P.values()))==2,'base collisions')
    points=sorted(set(B)|set(P.values()));need(len(points)==462 and len(points)<=508,'physical cap')
    edges=[(i,j) for i,j in itertools.combinations(range(len(points)),2)
           if times(minus(points[j],points[i]),conjugate(minus(points[j],points[i])))==UNIT]
    return points,edges

def serial(rows):return ''.join(','.join(map(str,r))+'\n' for r in rows).encode('ascii')
def cnf(n,edges):
    cs=[]
    for i in range(n):
        cs.append([4*i+c+1 for c in range(4)])
        cs.extend([-4*i-c-1,-4*i-d-1] for c,d in itertools.combinations(range(4),2))
    for i,j in edges:cs.extend([-4*i-c-1,-4*j-c-1] for c in range(4))
    return cs

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--solve',action='store_true');a=ap.parse_args()
    p,e=construct();cert=json.loads((HERE/'certificate.json').read_text());a.output.mkdir(parents=True,exist_ok=True)
    for name,rows in [('points.csv',p),('edges.csv',e)]:
        blob=serial(rows);need(blob==(HERE/name).read_bytes(),'nonidentical '+name);(a.output/name).write_bytes(blob)
    cs=cnf(len(p),e);blob=('p cnf %d %d\n'%(4*len(p),len(cs))+''.join(' '.join(map(str,c))+' 0\n' for c in cs)).encode('ascii')
    need(hashlib.sha256(blob).hexdigest()==cert['four_cnf_sha256'],'CNF differs');word=cert['four_word']
    if a.solve:
        from pysat.solvers import Solver
        with Solver(name='cadical195',bootstrap_with=cs) as solver:
            need(solver.solve(),'unexpected non-four signal');pos={v for v in solver.get_model() if v>0}
        word=''.join(str(next(c for c in range(4) if 4*i+c+1 in pos)) for i in range(len(p)))
    need(len(word)==len(p) and set(word)<=set('0123'),'invalid word');need(all(word[i]!=word[j] for i,j in e),'improper word')
    (a.output/'four_word.txt').write_text(word+'\n')
    print(json.dumps({'vertices':len(p),'edges':len(e),'four_word_checked':True,'same_frozen_word':word==cert['four_word'],'source_only_single_architecture':True},sort_keys=True))
if __name__=='__main__':main()
