#!/usr/bin/env python3
"""Standard-library checker for the three-power homogeneous-pencil theorem."""
import argparse
from collections import Counter,defaultdict
from itertools import combinations,product
import hashlib
import json
from pathlib import Path
import exact as E

HERE=Path(__file__).resolve().parent


def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def normalized_signs(rows):
    two={tuple(i for i,c in enumerate(r) if c!=(0,0)):r for r in rows if sum(c!=(0,0) for c in r)==2}
    E.need(set(two)=={(0,1),(0,2),(1,2)},'three binomial sections')
    p,q,_=two[0,1];r,_,s=two[0,2];_,t,h=two[1,2]
    div=lambda x,y:E.emul(x,E.econj(y))
    wphase=div(E.emul(p,s),r)
    eps=div(div(h,wphase),div(t,q))
    sign=lambda x:1 if x==(1,0) else -1 if x==(-1,0) else 0
    e=sign(eps);E.need(e!=0,'third anchor sign')
    full={}
    for row in rows:
        if any(c==(0,0) for c in row):continue
        x,y,z=row
        alpha=div(div(y,q),div(x,p));beta=div(div(z,wphase),div(x,p))
        pair=(E.residue(alpha),E.residue(beta))
        E.need(pair in {(2,3),(3,2)} and pair not in full,'two full sections')
        aa,bb=((0,1),(-1,1)) if pair==(2,3) else ((-1,1),(0,1))
        full[pair]=(sign(div(alpha,aa)),sign(div(beta,bb)))
        E.need(all(full[pair]),'full-section signs')
    E.need(set(full)=={(2,3),(3,2)},'both full sections')
    return (e,)+full[2,3]+full[3,2]


def normalization_audit():
    rows=sorted({E.canonical_row(r) for r in product(((0,0),)+E.EUNITS,repeat=3)
                 if sum(c!=(0,0) for c in r)>=2})
    E.need(len(rows)==54,'all unit rows on three variables')
    buckets=defaultdict(list)
    for r in rows:buckets[E.canonical_normal(tuple(map(E.residue,r)))].append(r)
    normals=sorted(buckets);E.need(len(normals)==18,'realized homogeneous signatures')
    points=list(product(range(4),repeat=3));masks={}
    for n in normals:
        masks[n]=sum(1<<i for i,w in enumerate(points) if E.gf_mul(n[0],w[0])^E.gf_mul(n[1],w[1])^E.gf_mul(n[2],w[2])==0)
    pencils=[p for p in combinations(normals,5) if (masks[p[0]]|masks[p[1]]|masks[p[2]]|masks[p[3]]|masks[p[4]])==(1<<64)-1]
    E.need(len(pencils)==9,'all five-hyperplane homogeneous covers')
    templates={}
    for signs in product((-1,1),repeat=5):
        e,s,t,k,l=signs
        sm=lambda a,x:E.emul((a,0),x)
        rr=[((1,0),(1,0),(0,0)),((1,0),(0,0),(1,0)),((0,0),(1,0),(e,0)),
            ((1,0),sm(s,(0,1)),sm(t,(-1,1))),((1,0),sm(k,(-1,1)),sm(l,(0,1)))]
        key=tuple(sorted(E.canonical_row(row) for row in rr))
        E.need(key not in templates,'distinct normal-form row sets');templates[key]=signs
    counts=Counter();transcript=[];gauge_checks=0
    for p in pencils:
        E.need(sorted(map(lambda n:len(buckets[n]),p))==[2,2,2,4,4],'pencil bucket sizes')
        for lift in product(*(buckets[n] for n in p)):
            signs=normalized_signs(lift)
            # Separate exhaustive diagonal-unit gauge check of the algebraic normalization.
            found=set()
            for alpha,beta in product(E.EUNITS,repeat=2):
                gauge_checks+=1
                transformed=tuple(sorted(E.canonical_row((row[0],E.emul(row[1],alpha),E.emul(row[2],beta))) for row in lift))
                if transformed in templates:found.add(templates[transformed])
            E.need(found=={signs},'independent unit-gauge normalization')
            counts[signs]+=1;transcript.append([lift,signs])
    E.need(set(counts)==set(product((-1,1),repeat=5)) and set(counts.values())=={36},'complete sign normalization')
    return {'three_variable_pencils':9,'three_variable_lifts':len(transcript),'normalized_cases':len(counts),
            'lifts_per_case':36,'unit_gauge_checks':gauge_checks,'normalization_sha256':digest(transcript)}


def identity_audit(certificate):
    E.need(len(certificate)==32,'certificate case count')
    E.need([tuple(c['signs']) for c in certificate]==list(product((-1,1),repeat=5)),'all sign cases exactly once')
    count=0;equal=0;degree_hist=Counter()
    for case in certificate:
        F,norms=E.equations(case['signs']);G=list(map(E.decode,case['basis']))
        E.need(G and all(G),'nonzero consequence polynomials')
        E.need(len(case['identities'])==len(G),'one identity per consequence')
        bound=case['membership_degree'];E.need(type(bound)==int and 2<=bound<=4,'small membership degree')
        for g,identity in zip(G,case['identities']):
            E.need(len(identity)==4,'four defining equations')
            total={}
            for f,encoded in zip(F,identity):
                h=E.decode(encoded)
                E.need(all(sum(m)<=bound-2 for m in h),'multiplier degree')
                total=E.add(total,E.mul(h,f))
            E.need(total==g,'exact defining-ideal identity')
            count+=1
        uv,uw,vw=E.add(norms[0],norms[1],-1),E.add(norms[0],norms[2],-1),E.add(norms[1],norms[2],-1)
        delta=E.ONE
        for factor in (uv,uw,vw):delta=E.remainder(E.mul(delta,factor),G)
        E.need(type(case['delta_zero'])==bool,'classification type')
        if case['delta_zero']:
            E.need(not delta,'equal-radius consequence');equal+=1
        else:
            for n in norms:
                target=delta
                for root in (1,3,7):
                    factor=E.add(E.scale(4,n),E.constant(root),-1)
                    target=E.remainder(E.mul(target,factor),G)
                E.need(not target,'three exceptional squared radii')
        degree_hist[str(bound)]+=1
    return {'polynomial_identities':count,'equal_radius_cases':equal,'exceptional_radius_cases':32-equal,
            'membership_degree_histogram':dict(sorted(degree_hist.items()))}


def unit_audit():
    cases=0;survivors=[]
    for signs in product((-1,1),repeat=5):
        e,s,t,k,l=signs
        for U,V,W in product(E.EUNITS,repeat=3):
            if E.eadd(U,V)!=(1,0):continue
            cases+=1
            sm=lambda z,x:E.emul((z,0),x)
            vectors=[E.eadd(U,W),E.eadd(V,sm(e,W)),
                     E.eadd(E.eadd(U,sm(s,E.emul((0,1),V))),sm(t,E.emul((-1,1),W))),
                     E.eadd(E.eadd(U,sm(k,E.emul((-1,1),V))),sm(l,E.emul((0,1),W)))]
            if all(E.enorm(v)==1 for v in vectors):survivors.append([signs,U,V,W])
    E.need(cases==384 and not survivors,'all-unit case impossible')
    return {'normalized_unit_cases':cases,'unit_survivors':0}


def verify(path):
    certificate=json.loads(Path(path).read_text())
    return {'status':'PASS',**normalization_audit(),**identity_audit(certificate),**unit_audit(),
            'a5_pencils':36,'a5_lifts':4608,'real_radix_concurrences':0,
            'certificate_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest()}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'certificate.json');p.add_argument('--check-expected',action='store_true');args=p.parse_args()
    result=verify(args.certificate)
    if args.check_expected:E.need(result==json.loads((HERE/'EXPECTED.json').read_text()),'expected output')
    print(json.dumps(result,sort_keys=True,indent=2))
