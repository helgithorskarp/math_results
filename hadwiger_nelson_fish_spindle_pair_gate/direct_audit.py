"""Alternate formal-address interval and transposed relation checks.

This shares the rational root proof and atom coordinates with model.py, but
uses interval products on all161 formal addresses rather than the midpoint
squared-distance error bound on the157 physical representatives.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
from math import isqrt
import json
from model import fish,moser,build,need,FIXED

HERE=Path(__file__).resolve().parent

def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[1],-a[0])
def mul(a,b):
    p=[x*y for x in a for y in b];return(min(p),max(p))
def point(a):return(a,a)

def run():
    graph,summary=build(HERE/'geometry_certificate.json')
    F,FE,r,_=fish(HERE/'geometry_certificate.json');M,ME=moser()
    H=10**40;root=[point(Q(1))]
    for d in (3,11,33):
        a=isqrt(d*H*H);need(a*a<d*H*H<(a+1)*(a+1),'radical bounds')
        root.append((Q(a,H),Q(a+1,H)))
    mi=[]
    for m in M:
        pair=[]
        for coord in m:
            z=point(Q(0))
            for a,b in zip(coord,root):z=add(z,mul(point(a),b))
            pair.append(z)
        mi.append(pair)
    P=[]
    for i,f in enumerate(F):
        fi=[point(z) if i in FIXED else(z-r,z+r) for z in f]
        for m in mi:P.append([add(fi[d],m[d]) for d in range(2)])
    phys={raw:i for i,cl in enumerate(graph['classes']) for raw in cl}
    E=set(map(tuple,graph['edges']));counts={'collision_pairs':0,'unit_pairs':0,'nonunit_pairs':0}
    for a,b in combinations(range(161),2):
        if phys[a]==phys[b]:counts['collision_pairs']+=1;continue
        dd=[add(P[a][d],neg(P[b][d])) for d in range(2)]
        d2=add(mul(dd[0],dd[0]),mul(dd[1],dd[1]))
        need(d2[0]>0,'formal address separation')
        edge=tuple(sorted((phys[a],phys[b]))) in E
        if edge:
            need(d2[0]<=1<=d2[1],'known Cartesian unit edge enclosure')
            counts['unit_pairs']+=1
        else:
            need(d2[1]<1 or d2[0]>1,'exclude every remaining formal pair')
            counts['nonunit_pairs']+=1
    words=json.loads((HERE/'relation_certificate.json').read_text())['words'];mask=(1<<len(words))-1
    columns=[[sum(1<<j for j,w in enumerate(words) if w[v]==str(c)) for c in range(4)] for v in range(len(graph['classes']))]
    same=diff=0
    for a,b in combinations(range(len(columns)),2):
        eq=0
        for c in range(4):eq |= columns[a][c]&columns[b][c]
        need(bool(eq)==((a,b) not in E),'transposed equality relation')
        need((mask^eq)!=0,'transposed inequality relation')
        same+=bool(eq);diff+=1
    return {'status':'FORMAL-ADDRESS AND TRANSPOSED PAIR CHECKS PASS',
            'formal_pair_count':161*160//2,**counts,
            'physical_nonunit_pairs_allowing_equality':same,
            'physical_pairs_allowing_inequality':diff,
            'radical_enclosure_denominator':str(H),
            'shares_root_proof_and_atom_definition':True,
            'independent_author_review':False}

if __name__=='__main__':print(json.dumps(run(),indent=2))
