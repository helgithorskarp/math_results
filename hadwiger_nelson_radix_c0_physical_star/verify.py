#!/usr/bin/env python3
"""Solver-free verifier: resultant/fiber coverage and direct physical distances.

No call to the producer's Groebner routine or to SAT is made here.
"""
import argparse
import hashlib
import json
from collections import Counter,defaultdict
from pathlib import Path
import algebra as A
import physical
from flint import fmpq,fmpq_poly


def trim(a):
    while a and not a[-1]:
        a.pop()
    return a


def inverse(a,q):
    h,u,_ = a.xgcd(q)
    A.need(h.degree()==0,'quotient must be a field')
    return (u/h[0]) % q


def outer_gcd(a,b,q):
    """Euclid in (Q[s]/q)[Y], monic output; outer coefficients ascend."""
    a,b = trim(a),trim(b)
    while b:
        inv = inverse(b[-1],q)
        while a and len(a)>=len(b):
            k = len(a)-len(b)
            c = a[-1]*inv % q
            for j in range(len(b)):
                a[j+k] = (a[j+k]-c*b[j]) % q
            trim(a)
        a,b = b,a
    if a:
        inv = inverse(a[-1],q)
        a = [p*inv%q for p in a]
    return a


def fiber(sparse,q):
    a = [fmpq_poly([]) for _ in range(1+max(j for i,j,c in sparse))]
    for i,j,c in sparse:
        a[j] += fmpq_poly([0]*i+[c])
    return [p%q for p in a]


def resultant_components(left,right,x,y,s):
    f,g = [A.expression(p,x,y) for p in (left,right)]
    resultant = A.sp.Poly(A.sp.resultant(f,g,y),x,domain=A.sp.QQ)
    A.need(not resultant.is_zero,'nonzero resultant required')
    output = []
    for q0,_ in A.sp.factor_list(resultant)[1]:
        qx = A.primitive(q0,x)
        nreal = int(qx.count_roots(-A.sp.oo,A.sp.oo))
        if not nreal:
            continue
        q = fmpq_poly([fmpq(v) for v in A.coefficients(qx)])
        h = outer_gcd(fiber(left,q),fiber(right,q),q)
        A.need(h,'common vertical component is unsupported')
        if len(h)==1:
            continue  # A spurious resultant factor has no affine intersection.
        if qx.degree()==1:
            x0 = -qx.nth(0)/qx.nth(1)
            hy = A.sp.Poly(sum(A.sp.Rational(str(a[0]))*y**j for j,a in enumerate(h)),y,domain=A.sp.QQ)
            for h0,_ in A.sp.factor_list(hy)[1]:
                qy = A.primitive(h0.as_expr().subs(y,s),s)
                nr = int(qy.count_roots(-A.sp.oo,A.sp.oo))
                if nr:
                    c = A.encode(qy,A.sp.Poly(x0,s,domain=A.sp.QQ),A.sp.Poly(s,s,domain=A.sp.QQ),s)
                    output.append((c,nr))
        else:
            A.need(len(h)==2 and h[1]==fmpq_poly([1]),'unsupported nonlinear algebraic fiber')
            qsym = A.sp.Poly(qx.as_expr().subs(x,s),s,domain=A.sp.QQ)
            yy = A.sp.Poly(sum(-A.sp.Rational(str(v))*s**i for i,v in enumerate(h[0].coeffs())),s,domain=A.sp.QQ)
            output.append((A.encode(qsym,A.sp.Poly(s,s,domain=A.sp.QQ),yy,s),nreal))
    for c,nr in output:
        ev = A.evaluator(c)
        A.need(ev(left) and ev(right),'resultant fiber substitution')
    return output


def check_asymmetry(pairs,factors,x,y):
    # If a group element stabilizes {C0,Cb}, its image of C0 is C0 or Cb.
    f0 = A.expression(factors[0],x,y)
    transforms=[]
    for reflect in (False,True):
        xx,yy=x,-y if reflect else y
        for rotation in range(3):
            p = A.sp.Poly(A.sp.expand(f0.subs({x:xx,y:yy},simultaneous=True)),x,y,domain=A.sp.QQ)
            _,p=p.clear_denoms(convert=True)
            sparse=A.geometry.primitive({(i,j):int(c) for (i,j),c in p.terms()})
            transforms.append(sparse)
            xx,yy=(-xx-3*yy)/2,(xx-yy)/2
    A.need(transforms[0]==factors[0],'D3 identity')
    for a,b in pairs:
        for transformed in transforms[1:]:
            A.need(transformed not in (factors[a],factors[b]),'pair may have a nontrivial stabilizer')


def verify(residual_path,certificate_path):
    certificate=json.loads(Path(certificate_path).read_text())
    A.need(certificate['schema']=='hn-radix-c0-physical-star-v1','schema')
    _,_,factors,_,_,_,_,_=A.architecture.build()
    pairs=A.select(residual_path,factors)
    A.need(certificate['source_residual_sha256']==A.RESIDUAL_HASH,'residual hash')
    A.need(certificate['curve_inventory_sha256']==A.digest(factors),'curve hash')
    x,y,s=A.sp.symbols('x y s')
    check_asymmetry(pairs,factors,x,y)
    data,sources,pair_rows={},defaultdict(list),[]
    for a,b in pairs:
        keys=[]
        for c,nr in resultant_components(factors[a],factors[b],x,y,s):
            key=A.digest(c)
            A.need(key not in data or data[key]==dict(c,real_embeddings=nr),'inconsistent component')
            data[key]=dict(c,real_embeddings=nr)
            sources[key].append([a,b]);keys.append(key)
        A.need(len(keys)==len(set(keys)),'duplicate pair root component')
        pair_rows.append({'pair':[a,b],'components':sorted(keys)})
    A.need(certificate['pairs']==pair_rows,'complete pair-component coverage')
    records={c['key']:c for c in certificate['components']}
    A.need(len(records)==len(certificate['components']) and set(records)==set(data),'component list completeness')
    histogram=Counter();active_hist=Counter();degree_hist=Counter();max_active=0
    for key in sorted(data):
        expected=data[key];c=records[key]
        for k,v in expected.items():
            A.need(c[k]==v,'exact component field '+k)
        A.need(c['source_pairs']==sorted(sources[key]),'source pairs')
        ev=A.evaluator(c);active=[i for i,f in enumerate(factors) if ev(f)]
        A.need(c['active_curves']==active,'active curve list')
        points,labels,edges,triangle=physical.graph(c)
        A.need(c['point_count']==len(points) and c['edge_count']==len(edges),'physical counts')
        A.need(c['edge_sha256']==A.digest(edges),'complete physical edge set')
        A.need(c['label_map_sha256']==A.digest(labels),'physical collision quotient')
        physical.check_word(c['three_colouring'],len(points),edges)
        # Three distinct mutually adjacent physical points supply chi >= 3.
        A.need(len(set(triangle))==3,'triangle distinctness')
        n=c['real_embeddings']
        histogram[f"{len(points)}v_{len(edges)}e"]+=n
        active_hist[str(len(active))]+=n
        degree_hist[str(len(c['q'])-1)]+=n
        max_active=max(max_active,len(active))
    return {'status':'PASS','pair_count':len(pairs),'component_count':len(records),
            'distinct_real_parameters':sum(c['real_embeddings'] for c in data.values()),
            'all_chromatic_numbers':3,'physical_graph_histogram_by_parameter':dict(sorted(histogram.items())),
            'active_curve_histogram_by_parameter':dict(sorted(active_hist.items(),key=lambda a:int(a[0]))),
            'field_degree_histogram_by_parameter':dict(sorted(degree_hist.items(),key=lambda a:int(a[0]))),
            'source_residual_sha256':A.RESIDUAL_HASH,'pair_list_sha256':A.digest(pairs),
            'certificate_sha256':hashlib.sha256(Path(certificate_path).read_bytes()).hexdigest()}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--residual',type=Path);p.add_argument('--certificate',type=Path,default=Path(__file__).parent/'certificate.json');p.add_argument('--check-expected',action='store_true')
    args=p.parse_args();result=verify(args.residual,args.certificate)
    if args.check_expected:
        A.need(result==json.loads((Path(__file__).parent/'EXPECTED.json').read_text()),'expected output')
    print(json.dumps(result,sort_keys=True,indent=2))
