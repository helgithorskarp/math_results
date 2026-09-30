#!/usr/bin/env python3
"""Export any of the224 equivalent exact polynomial feasibility systems.

Variables are t,y00,y01,y02,...,y40,y41,y42. Relations mean the listed
integer polynomial is eq0/ge0/gt0. Each coefficient denominator is
proved nonzero on the window before clearing by a common square.
No system is solved here; generated systems are not saved by default.
"""
from itertools import combinations,combinations_with_replacement
from pathlib import Path
import argparse,json
from rational import Rat
from family import H,t,one,zero
from polynomial import need,mul,pgcd,exactdiv,F
from polytope import normal,polynomial_sign
from check import audit_type

ASSIGNMENTS=list(combinations_with_replacement(range(4),5))
EMPTY=(0,)*15
def monomial(*indices):
    p=[0]*15
    for i in indices:p[i]+=1
    return tuple(p)

def clear(expr,relation):
    expr={p:q for p,q in expr.items() if q.n};common=(1,)
    for q in expr.values():
        need(polynomial_sign(q.d) in (-1,1),'coefficient denominator nonzero')
        common=mul(exactdiv(common,pgcd(common,q.d)),q.d)
    positive=mul(common,common);terms=[]
    for powers,q in sorted(expr.items()):
        coeffs=mul(q.n,exactdiv(positive,q.d))
        for k,c in enumerate(coeffs):
            if c:terms.append([c,[k,*powers]])
    return {'relation':relation,'positive_multiplier':list(positive),'terms':terms}

def build(points,outside,assignment,type_key):
    need(type(assignment) is int and 0<=assignment<56,'assignment index')
    selected=ASSIGNMENTS[assignment];constraints=[]
    def append(expr,relation,name):
        z=clear(expr,relation);z['name']=name;constraints.append(z)
    append({EMPTY:Rat((-113,225))},'ge','cap area lower bound')
    append({EMPTY:Rat((-1,2))},'gt','open lower window')
    append({EMPTY:Rat((3,-5))},'gt','open upper window')
    append({EMPTY:Rat(tuple(-c for c in F))},'gt','strict incumbent improvement')
    for i in range(5):
        expr={EMPTY:-one}
        for j in range(3):
            for k in range(3):
                p=monomial(3*i+j,3*i+k);expr[p]=expr.get(p,zero)+H[j][k]
        append(expr,'eq','unit '+str(i))
        for label,point in sorted(points.items()):
            cov=normal(point);expr={EMPTY:t}
            expr.update({monomial(3*i+j):-cov[j] for j in range(3)})
            append(expr,'ge','core '+str(label)+' extra '+str(i))
        cov=normal(outside[selected[i]]['y']);expr={EMPTY:-one}
        expr.update({monomial(3*i+j):cov[j] for j in range(3)})
        append(expr,'ge','assigned cap '+str(selected[i])+' extra '+str(i))
    for i,j in combinations(range(5),2):
        expr={EMPTY:t}
        for k in range(3):
            for l in range(3):expr[monomial(3*i+k,3*j+l)]=-H[k][l]
        append(expr,'ge','pair '+str(i)+' '+str(j))
    need(len(constraints)==74,'complete constraint count')
    return {'type_key':type_key,'assignment_index':assignment,'cap_assignment':list(selected),'variables':['t']+['y'+str(i)+str(j) for i in range(5) for j in range(3)],'constraints':constraints,'status':'EXACT_POLYNOMIAL_SYSTEM_NOT_SOLVED'}

def system(entry,assignment):
    summary,points,mapping,outside=audit_type(entry)
    return build(points,outside,assignment,entry['key'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--type',type=int,choices=range(4),required=True);p.add_argument('--assignment',type=int,choices=range(56),required=True);args=p.parse_args()
    data=json.loads(Path(__file__).with_name('certificate.json').read_text())
    print(json.dumps(system(data['types'][args.type],args.assignment),separators=(',',':')))
