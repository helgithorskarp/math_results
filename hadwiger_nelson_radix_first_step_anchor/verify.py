#!/usr/bin/env python3
"""Standard-library proof checker: bivariate restriction and actual label edges."""
import argparse
from collections import Counter
from itertools import combinations
import hashlib,importlib.util,json
from pathlib import Path
import common as C
X=C.X
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('anchor_reviewer_inventory',HERE.parent/'hadwiger_nelson_radix_four_active_closure_review1/independent_check.py')
V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)


def inventory():
    rows,factors,circle,monos,rowids=V.reconstruct_inventory()
    qs=[[C.bivariate_pull(f,s) for f in factors] for s in (1,-1)]
    base=[];groups=[[] for _ in factors]
    for a,b in combinations(range(243),2):
        c=V.edge_owner(a,b,monos,rowids,circle)
        (base if c=='base' else groups[c]).append((a,b))
    X.need(len(base)==243 and sum(map(len,groups))==29160,'all 29403 actual label pairs')
    return factors,qs,base,groups


def check_products(cert,unique):
    blocks=cert['blocks']
    X.need(blocks==sorted(blocks) and len(set(map(tuple,blocks)))==len(blocks),'distinct sorted blocks')
    for q in blocks:
        X.need(2<=len(q)<=9 and all(type(v)is int for v in q) and tuple(q)==C.primitive(q),'primitive positive-leading integer block')
    X.need(len(cert['factorizations'])==len(unique),'complete factorizations')
    bypoly={}
    for q,(scalar,terms) in zip(unique,cert['factorizations']):
        X.need(type(scalar)is int and scalar>0,'positive factor content')
        X.need(terms==sorted(terms) and len({i for i,e in terms})==len(terms),'canonical factor multiplicities')
        value=[scalar]
        for i,e in terms:
            X.need(type(i)is int and 0<=i<len(blocks) and type(e)is int and 1<=e<=8,'factor index and multiplicity')
            for _ in range(e):value=X.mul(value,blocks[i])
        X.need(tuple(value)==q,'exact integer factorization product')
        bypoly[q]={i for i,e in terms}
    X.need(set().union(*bypoly.values())==set(range(len(blocks))),'every block occurs in a norm restriction')
    return bypoly


def modular_audit(blocks,roots):
    X.need(all(X.is_prime(p) for p in X.PRIMES),'prime certificate moduli')
    real=[i for i,n in enumerate(roots) if n];hist=Counter();trace=hashlib.sha256()
    for i,j in combinations(real,2):
        for p in X.PRIMES:
            # Both degrees must survive: these blocks need not be monic.
            if blocks[i][-1]%p and blocks[j][-1]%p and X.gcd_is_one(blocks[i],blocks[j],p):
                hist[p]+=1;trace.update(f'{i},{j},{p}\n'.encode());break
        else:raise ValueError('no degree-preserving real-block coprimality certificate')
    squarefree=[]
    for q in blocks:
        squarefree.append(next(p for p in X.PRIMES if q[-1]%p and X.gcd_is_one(q,X.derivative(q),p)))
    return {'real_block_pair_checks':sum(hist.values()),'prime_histogram':{str(p):n for p,n in sorted(hist.items())},
            'pair_trace_sha256':trace.hexdigest(),'squarefree_primes_sha256':X.digest(squarefree)}


def check_word(word,events,base,groups):
    colours=[sum(w*a for w,a in zip(word,label))%3 for label in C.LABELS]
    X.need(all(colours[a]!=colours[b] for a,b in base),'proper universal edges')
    for c in events:X.need(all(colours[a]!=colours[b] for a,b in groups[c]),'proper actual edge of every active curve')


def check_colours(cert,qs,bypoly,base,groups):
    n=len(cert['blocks']);roots=cert['real_root_counts'];coll={}
    for entry in cert['collision_witnesses']:
        i=entry['block_id']
        X.need(type(i)is int and 0<=i<n and roots[i]>0 and i not in coll,'distinct real collision block')
        X.need(len(entry['rows'])==2,'witness for each sign')
        for row,s in zip(entry['rows'],(1,-1)):C.check_collision(row,cert['blocks'][i],s)
        coll[i]=entry
    X.need(len(cert['colour_assignments'])==2,'both physical sign representatives')
    for special,colours in zip(qs,cert['colour_assignments']):
        X.need(len(colours)==n and special.count(())==1,'complete annotations and one identically active curve')
        anchor=special.index(());events=[{anchor} for _ in range(n)]
        for c,q in enumerate(special):
            for i in bypoly.get(q,()):events[i].add(c)
        check_word(C.WEIGHTS[0],[anchor],base,groups) # all non-event real t
        for i,k in enumerate(colours):
            if not roots[i] or i in coll:
                X.need(k is None,'imported collision or empty real block');continue
            X.need(type(k)is int and 0<=k<len(C.WEIGHTS),'explicit valid three-colour word')
            check_word(C.WEIGHTS[k],events[i],base,groups)
    return coll


def check_symmetry_and_endpoints():
    power=(1,0);shifts=[]
    for j in range(5):
        points=[V.e_mul(power,d) for d in V.DIGITS]
        candidates=[s for s in points if {(a-s[0],b-s[1]) for a,b in points}==set(V.DIGITS)]
        X.need(len(candidates)==1,'digit triangle translation');shifts.append(candidates[0]);power=V.e_mul(power,(-1,1))
    X.need(shifts==[(0,0),(-1,0),(0,-1),(0,0),(-1,0)],'exact rotation of A5 as a translate')
    # All endpoint coordinates are Eisenstein integers; check their quotient
    # colours directly on physical points, including all collisions.
    for z in (2,-2):
        points={tuple(sum(d[j]*z**i for i,a in enumerate(label) for d in [V.DIGITS[a]]) for j in (0,1)) for label in C.LABELS}
        for a,b in combinations(points,2):
            x,y=a[0]-b[0],a[1]-b[1]
            if x*x+x*y+y*y==1:X.need((x-y)%3!=0,'proper physical endpoint edge')


def run(path):
    cert=json.loads(Path(path).read_text());X.need(cert['schema']=='hn-radix-first-anchor-v1','schema')
    factors,qs,base,groups=inventory();unique=sorted(set(qs[0])-{()})
    X.need(set(qs[0])==set(qs[1]),'both signs have same polynomial inventory')
    X.need(X.digest(factors)==cert['curve_inventory_sha256'],'original curve ID inventory')
    X.need(X.digest(unique)==cert['restriction_inventory_sha256'],'independent bivariate restrictions')
    bypoly=check_products(cert,unique);C.root_audit(cert['blocks'],cert['real_root_counts'])
    check_colours(cert,qs,bypoly,base,groups);check_symmetry_and_endpoints()
    audit=modular_audit(cert['blocks'],cert['real_root_counts'])
    result=C.summarize(cert,qs,audit);X.need(result==cert['result'],'all exact counts and audit hashes')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'certificate.json');args=p.parse_args()
    print(json.dumps(run(args.certificate),indent=2,sort_keys=True))
