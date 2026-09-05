#!/usr/bin/env python3
"""Canonical complete Ramsey formula for permutation type 1^13 3^10.

Vertices 0..29 form ten rotating triples; 30..42 are fixed.
True edge variables mean red; the first r triples are internally red.
The explicit reduction, gate definitions, counters and normalizations
are proved in PROOF.md. No solver or Python package is imported.
"""
from itertools import combinations, product
from pathlib import Path
import argparse

parser=argparse.ArgumentParser(description='Generate the exact order-three ten-cycle formula.')
parser.add_argument('--red-cycles',type=int,choices=range(6),required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
r = args.red_cycles
colors = [1]*r+[0]*(10-r)
pairs = list(combinations(range(10), 2))
ids = {p: tuple(range(1+3*i, 4+3*i)) for i,p in enumerate(pairs)}
nv = 135
fixed = {}
for i,j in combinations(range(30,43),2):
    nv+=1;fixed[i,j]=nv
links={}
for j in range(30,43):
    for i in range(10):
        nv+=1;links[i,j]=nv
clauses = set()
def add(clause):
    clause = set(clause)
    if any(-v in clause for v in clause): return
    clauses.add(tuple(sorted(clause)))
T = 100000
def edge(a,b):
    if a>=30:return fixed[a,b]
    i,u=divmod(a,3)
    if b>=30:return links[i,b]
    j,v=divmod(b,3)
    if i==j:return T if colors[i] else -T
    return ids[i,j][(v-u)%3]
for vertices in combinations(range(43), 5):
    es=[edge(a,b) for a,b in combinations(vertices,2)]
    for sign in (-1,1):
        ls=[sign*e for e in es]
        if T not in ls:add(l for l in ls if l!=-T)
ramsey_clauses = len(clauses)
tokens=[[] for _ in range(10)]; full=[[] for _ in range(10)]
for (i,j),bits in ids.items():
    gates={}
    for color in sorted(set((colors[i],colors[j]))):
        u,v,z=nv+1,nv+2,nv+3; nv+=3
        gates[color]=(u,v,z)
        for vals in product((0,1),repeat=3):
            weight=sum(x==color for x in vals)
            cost=2 if weight in (0,3) else 2-weight
            antecedent=[-b if x else b for b,x in zip(bits,vals)]
            add(antecedent+[u if cost>=1 else -u])
            add(antecedent+[v if cost>=2 else -v])
            add(antecedent+[z if weight==3 else -z])
    for a in (i,j):
        tokens[a].extend(gates[colors[a]][:2]);full[a].append(gates[colors[a]][2])
    if i==0:
        add((-bits[1],bits[0]));add((-bits[2],bits[1]))
for row in tokens:
    for subset in combinations(row,7):add(-x for x in subset)
def atmost(lits,k):
    global nv
    previous={}
    for index,lit in enumerate(lits,1):
        row={}
        for q in range(1,min(index,k+1)+1):
            nv+=1;row[q]=nv
            if q==1:add((-lit,row[q]))
            if q in previous:add((-previous[q],row[q]))
            if q>1 and q-1 in previous:add((-lit,-previous[q-1],row[q]))
        previous=row
    if k+1 in previous:add((-previous[k+1],))
for i in range(10):
    sign=1 if colors[i] else -1
    fixed_own=[sign*links[i,j] for j in range(30,43)]
    atmost(fixed_own+[z for z in full[i] for _ in range(3)],4)
    cross=[sign*v for pair,vals in ids.items() if i in pair for v in vals]
    atmost([-x for x in fixed_own+cross],24) # own cross+fixed >=16
# Every fixed vertex also has both color-degrees at most 24.
for j in range(30,43):
    incident=[fixed[tuple(sorted((j,k)))] for k in range(30,43) if k!=j]
    incident += [links[i,j] for i in range(10) for _ in range(3)]
    atmost(incident,24)
    atmost([-x for x in incident],24)
for j in range(30,42):
    a=[links[i,j] for i in range(10)]; b=[links[i,j+1] for i in range(10)]
    for q in range(10):
        for prefix in product((0,1),repeat=q):
            row=[]
            for t,x in enumerate(prefix):row.extend(((-a[t],-b[t]) if x else (a[t],b[t])))
            add(row+[-a[q],b[q]])
cs=sorted(clauses,key=lambda c:(len(c),c))
path=args.output
path.write_text(f'p cnf {nv} {len(cs)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in cs))
print(f'GENERATED r={r} variables={nv} clauses={len(cs)} ramsey_clauses={ramsey_clauses}')
