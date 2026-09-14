#!/usr/bin/env python3
"""Independent definition-level verifier for the quadratic kernel certificate."""
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
import argparse
import copy
import hashlib
import json


# Independent explicit multiplication in 1,r,i,ir with r^2=3.
def ka(x,y):return tuple(a+b for a,b in zip(x,y))
def kn(x):return tuple(-a for a in x)
def ks(x,y):return ka(x,kn(y))
def km(x,y):
    a,b,c,d=x;e,f,g,h=y
    return (a*e+3*b*f-c*g-3*d*h,
            a*f+b*e-c*h-d*g,
            a*g+3*b*h+c*e+3*d*f,
            a*h+b*g+c*f+d*e)
def kc(x):return (x[0],x[1],-x[2],-x[3])
K0=(F(0),)*4;K1=(F(1),F(0),F(0),F(0));K53=(F(5,3),F(0),F(0),F(0))


# Quotient by t^2=(5/3)t-1.  The physical conjugation has t-bar=5/3-t.
def add(x,y):return (ka(x[0],y[0]),ka(x[1],y[1]))
def neg(x):return (kn(x[0]),kn(x[1]))
def sub(x,y):return add(x,neg(y))
def mul(x,y):
    a,b=x;c,d=y;bd=km(b,d)
    return (ks(km(a,c),bd),ka(ka(km(a,d),km(b,c)),km(K53,bd)))
def conj(x):
    a,b=x;cb=kc(b)
    return (ka(kc(a),km(K53,cb)),kn(cb))
def norm(x):return mul(x,conj(x))


ZERO=(K0,K0);ONE=(K1,K0);T=(K0,K1)
OMEGA=((F(1,2),F(0),F(0),F(1,2)),K0);ROOTS=[ONE]
for _ in range(5):ROOTS.append(mul(ROOTS[-1],OMEGA))
if mul(ROOTS[-1],OMEGA)!=ONE or norm(T)!=ONE:raise RuntimeError('field relation')


def dec(x):return tuple(tuple(F(n,d) for n,d in part) for part in x)
def enc(x):return [[[q.numerator,q.denominator] for q in part] for part in x]
def raw(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x):return hashlib.sha256(raw(x)).hexdigest()
def orbit(direction):
    candidates=[mul(direction,u) for u in ROOTS];rep=min(candidates)
    return rep,next(k for k,u in enumerate(ROOTS) if mul(rep,u)==direction)
def proper(word,edges):return len(word)>0 and all(word[a]!=word[b] for a,b in edges)


def base_patterns():
    out=set()
    for word in product(range(4),repeat=4):
        if word[0]==word[1] or word[2]==word[3]:continue
        rename={};row=[]
        for c in word:
            if c not in rename:rename[c]=len(rename)
            row.append(rename[c])
        out.add(''.join(map(str,row)))
    return sorted(out)


def reconstruct():
    spec=((0,0,0),(0,0,1),(0,4,4),(0,4,3));cross=((0,0),(0,1),(1,0),(1,1))
    us=[ROOTS[k] for _,k,_ in spec];vs=[mul(ROOTS[l],T) for _,_,l in spec];ds=[sub(u,v) for u,v in zip(us,vs)]
    centres=(ZERO,sub(ds[0],ds[2]),ds[0],ds[1])
    if sub(centres[3],centres[1])!=ds[3] or norm(centres[1])!=ONE or norm(sub(centres[3],centres[2]))!=ONE:
        raise ValueError('centre geometry')
    intersections=[];clauses=[];reps={}
    forbidden=(ZERO,ONE,((F(3),F(0),F(0),F(0)),K0),((F(4),F(0),F(0),F(0)),K0))
    for (i,j),u,v in zip(cross,us,vs):
        if u in (v,neg(v)) or norm(sub(u,v)) in forbidden:raise ValueError('nonregular slot')
        p=add(centres[i],u);q=sub(add(centres[i],centres[2+j]),p)
        if p==q or any(norm(sub(x,centres[i]))!=ONE or norm(sub(x,centres[2+j]))!=ONE for x in (p,q)):
            raise ValueError('intersection')
        intersections.append((p,q));ru,k=orbit(u);rv,l=orbit(v);reps[ru]=None;reps[rv]=None;s=(1+i+j)&1
        clauses.append(((ru,(s+k)&1),(rv,(1+s+l)&1)))
    ordered=sorted(reps);oi={r:i for i,r in enumerate(ordered)}
    clauses=[sorted([[oi[r],v] for r,v in row]) for row in clauses]
    directions=[set(),set()]
    for g in range(2):
        seeds=[sub(centres[2*g+1],centres[2*g])]
        for (i,j),row in zip(cross,intersections):
            owner=centres[i if g==0 else 2+j];seeds.extend(sub(p,owner) for p in row)
        for seed in seeds:directions[g].update(mul(seed,u) for u in ROOTS)
    points=set()
    for h,c in enumerate(centres):points.update(add(c,u) for u in directions[h//2])
    vertices=sorted(points);vi={p:i for i,p in enumerate(vertices)}
    edges=[list(e) for e in combinations(range(len(vertices)),2) if norm(sub(vertices[e[0]],vertices[e[1]]))==ONE]
    return spec,centres,ds,clauses,directions,vertices,edges,[vi[c] for c in centres]


def validate(data):
    if data.get('schema')!=1 or data.get('field')!='Q(sqrt(3),i)[t]/(t^2-(5/3)t+1)':raise ValueError('schema')
    if data.get('parameter_polynomial')!=['1','-5/3','1']:raise ValueError('parameter')
    spec,C,ds,clauses,D,V,E,ci=reconstruct()
    if data.get('directions')!=[list(x) for x in spec] or data.get('centres')!=[enc(x) for x in C] or data.get('centre_indices')!=ci:
        raise ValueError('geometry labels')
    if data.get('cross_squared_norms')!=[enc(norm(d)) for d in ds]:raise ValueError('cross norms')
    solutions=sum(all(any(a[v]==value for v,value in row) for row in clauses) for a in product(range(2),repeat=2))
    if data.get('orbit_variables')!=2 or data.get('clauses')!=clauses or solutions!=0 or data.get('phase_solutions')!=0:
        raise ValueError('phase formula')
    if data.get('direction_sizes')!=list(map(len,D)) or data.get('patch_vertices')!=len(V) or data.get('patch_edges')!=len(E):
        raise ValueError('counts')
    encoded=[enc(x) for x in V]
    if data.get('vertices')!=encoded or data.get('edges')!=E or data.get('point_sha256')!=digest(encoded) or data.get('edge_sha256')!=digest(E):
        raise ValueError('strict graph')
    # The only common unit neighbours of the unit-separated pair C0,C1 are
    # its two equilateral completions.  Test both against C2,C3 exactly.
    ae=sub(C[1],C[0]);candidates=[add(C[0],mul(ae,ROOTS[k])) for k in (1,5)]
    if any(norm(sub(p,C[0]))!=ONE or norm(sub(p,C[1]))!=ONE for p in candidates):raise ValueError('equilateral roots')
    common=[p for p in candidates if norm(sub(p,C[2]))==ONE and norm(sub(p,C[3]))==ONE]
    if common or data.get('common_plane_unit_neighbour') is not False:raise ValueError('common-neighbour claim')
    patterns=base_patterns()
    if data.get('base_terminal_patterns')!=patterns or data.get('terminal_relation')!=patterns or data.get('interface_stronger_than_base') is not False:
        raise ValueError('terminal relation')
    words=data.get('terminal_words',{})
    if sorted(words)!=patterns:raise ValueError('terminal word keys')
    for pattern,word in words.items():
        w=[int(x) for x in word]
        if len(w)!=len(V) or max(w)>3 or not proper(w,E) or ''.join(str(w[x]) for x in ci)!=pattern:raise ValueError('terminal word')
    four=[int(x) for x in data.get('four_colouring','')]
    if len(four)!=len(V) or max(four)>3 or not proper(four,E):raise ValueError('four colouring')
    core=data.get('moser_spindle_indices');expected_core=[25,33,38,39,40,41,44]
    if core!=expected_core:raise ValueError('core indices')
    core_edges=[[i,j] for i,j in combinations(range(7),2) if [min(core[i],core[j]),max(core[i],core[j])] in E]
    if len(core_edges)!=11:raise ValueError('Moser edge count')
    if any(proper(word,core_edges) for word in product(range(3),repeat=7)):raise ValueError('Moser core is 3-colourable')
    if data.get('chromatic_number')!=4 or data.get('record_improved') is not False:raise ValueError('scope')
    return {'status':'PASS','vertices':len(V),'edges':len(E),'chromatic_number':4,'moser_spindle_vertices':7,
            'moser_spindle_edges':11,'orbit_variables':2,'phase_solutions':0,'common_plane_unit_neighbour':False,
            'terminal_patterns':len(patterns),'interface_stronger_than_base':False,'rejected_controls':0,'record_improved':False}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',default=str(Path(__file__).with_name('certificate.json')))
    ap.add_argument('--check-expected',action='store_true');args=ap.parse_args();data=json.loads(Path(args.certificate).read_text());result=validate(data)
    bad=[]
    for key,value in [('phase_solutions',1),('common_plane_unit_neighbour',True),('chromatic_number',3),('interface_stronger_than_base',True)]:
        x=copy.deepcopy(data);x[key]=value;bad.append(x)
    x=copy.deepcopy(data);x['edges']=x['edges'][:-1];bad.append(x)
    x=copy.deepcopy(data);k=next(iter(x['terminal_words']));x['terminal_words'][k]='0'*x['patch_vertices'];bad.append(x)
    rejected=0
    for x in bad:
        try:validate(x)
        except (ValueError,KeyError,IndexError):rejected+=1
    if rejected!=len(bad):raise ValueError('malformed control accepted')
    result['rejected_controls']=rejected
    if args.check_expected and result!=json.loads(Path(__file__).with_name('expected.json').read_text()):raise ValueError('expected mismatch')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
