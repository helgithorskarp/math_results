#!/usr/bin/env python3
"""Two exact physical six-curve members; default verification needs no CAS."""
import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
import exact as X

HERE = Path(__file__).resolve().parent
POLY = (-1,0,0,1,0,0,1,1)
LABELS = tuple(product(range(3),repeat=5))


def coordinates(sign):
    return [[[sign**j if t==1 else 0 for j,t in enumerate(label)],
             [sign**j if t==2 else 0 for j,t in enumerate(label)]] for label in LABELS]


def produce():
    import flint
    modulus = flint.fmpz_poly(list(POLY))
    graphs=[]
    for sign in (1,-1):
        points=coordinates(sign)
        edges=[]
        for u,v in combinations(range(243),2):
            a=flint.fmpz_poly([x-y for x,y in zip(points[u][0],points[v][0])])
            b=flint.fmpz_poly([x-y for x,y in zip(points[u][1],points[v][1])])
            norm=a*a+a*b+b*b
            X.need(norm % modulus != 0, 'distinct physical points')
            if (norm-1) % modulus == 0:
                edges.append([u,v])
        word=[label[0] for label in LABELS]
        X.need(all(word[u]!=word[v] for u,v in edges), 'proper physical colouring')
        graphs.append({'parameter_sign':sign,'coordinates_in_basis_1_omega':points,'edges':edges,
                       'colouring':word,'unit_triangle':[0,81,162],'chromatic_number':3})
    return {'schema':'hn-radix-reflection-physical-v1','real_generator_minimal_polynomial':POLY,
            'real_generator_isolating_interval':[[4,5],[81,100]],
            'omega':'(1+i sqrt(3))/2, with positive imaginary part',
            'coordinate_convention':'Low-order coefficient arrays a,b mean a(r)+omega*b(r); vertex order is lexicographic {0,1,2}^5.',
            'graphs':graphs}


def verify(certificate):
    X.need(certificate['schema']=='hn-radix-reflection-physical-v1','physical schema')
    q=certificate['real_generator_minimal_polynomial']
    X.need(tuple(q)==POLY,'fixed real-generator polynomial')
    X.irreducible_degree_seven_mod_five(q)
    left,right=[Fraction(*v) for v in certificate['real_generator_isolating_interval']]
    X.need(Fraction(1,2)<left<right<1,'off-circle target-radius interval')
    X.need(X.root_count(q)==1 and X.root_count(q,left,right)==1,'unique isolated real root')
    X.need(len(certificate['graphs'])==2,'both real-parameter signs')
    results=[]
    for sign,g in zip((1,-1),certificate['graphs']):
        X.need(g['parameter_sign']==sign,'parameter sign')
        points=g['coordinates_in_basis_1_omega']
        X.need(points==coordinates(sign),'physical radix coordinates')
        edges=[]
        for u,v in combinations(range(243),2):
            # Independent real/imaginary expansion of four times the distance.
            da=X.add(points[u][0],points[v][0],-1)
            db=X.add(points[u][1],points[v][1],-1)
            real_twice=X.add([2*a for a in da],db)
            rho=X.add(X.mul(real_twice,real_twice),X.mul(db,db),3)
            X.need(X.rem(rho,q),'all 243 physical points distinct')
            if not X.rem(X.add(rho,[4],-1),q):
                edges.append([u,v])
        X.need(edges==g['edges'],'all and only strict unit edges')
        word=g['colouring']
        X.need(len(word)==243 and all(type(c) is int and 0<=c<3 for c in word),'three-colour domain')
        X.need(all(word[u]!=word[v] for u,v in edges),'proper colouring of every unit edge')
        triangle=g['unit_triangle']
        X.need(len(set(triangle))==3 and all(sorted(e) in edges for e in combinations(triangle,2)),'unit triangle lower bound')
        X.need(g['chromatic_number']==3,'exact chromatic claim')
        results.append({'parameter_sign':sign,'vertices':243,'edges':len(edges),'chromatic_number':3,
                        'edges_sha256':X.digest(edges),'coordinate_sha256':X.digest(points)})
    return {'verified':True,'prime_for_degree_seven_irreducibility':5,'real_root_count':1,
            'checked_point_pairs':2*29403,'graphs':results,'record_improvement':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--produce',type=Path)
    parser.add_argument('--certificate',type=Path,default=HERE/'physical.json')
    args=parser.parse_args()
    if args.produce:
        data=produce()
        with args.produce.open('x') as f:
            json.dump(data,f,sort_keys=True,separators=(',',':'))
            f.write('\n')
        print(json.dumps({'output':str(args.produce),'bytes':args.produce.stat().st_size},sort_keys=True))
    else:
        print(json.dumps(verify(json.loads(args.certificate.read_text())),indent=2,sort_keys=True))
