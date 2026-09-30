"""Exact finite LCM sieve: standard-library certificate checker.

The prior lower bound and two three-prime exponent barriers are mathematical
inputs cited in proof.md. Every NEW finite exclusion is replayed here.
No solver, orbit constructor, floating point, or incomplete-success return.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from math import gcd,lcm,prod
from pathlib import Path
from time import monotonic
import kernel

BASE=Path(__file__).resolve().parent
# Separately cited mathematical inputs; this checker replays the new finite exclusions.
UPPER_BOUND_INPUT=20160
BINARY_EXPONENT_INPUT=5
TARGET_REMAINING=[10080,12600,15120,15840,18480,20160,22680,23760,25200,27720,28080]


def key(L,A):
    return L,tuple(tuple(t) for t in A)


def prime_powers(L):
    return tuple(p**len(levels) for p,levels in kernel.factor_levels(L))


def decode(L,boxes):
    periods=prime_powers(L);coefficients=[L//P*pow(L//P,-1,P) for P in periods]
    weights=[0]*L
    for box in boxes:
        if len(box)!=len(periods)+1 or type(box[-1]) is not int or box[-1]<=0:
            raise ValueError('Invalid weighted box')
        axes=[]
        for mask,P in zip(box[:-1],periods):
            if type(mask) is not int or not 0<mask<1<<P:raise ValueError('Invalid axis mask')
            axes.append([a for a in range(P) if mask>>a&1])
        for coordinates in product(*axes):
            x=sum(r*c for r,c in zip(coordinates,coefficients))%L
            if weights[x]:raise ValueError('Overlapping weighted boxes')
            weights[x]=box[-1]
    return weights


def histogram(weights,m):
    counts=[0]*m
    for x,w in enumerate(weights):
        if w:counts[x%m]+=w
    return counts


def pair_capacities(weights,m,n):
    """Exact inclusion-exclusion through the compatible CRT intersection."""
    ell=lcm(m,n);g=gcd(m,n);q=n//g;inverse=pow(m//g,-1,q)
    left=histogram(weights,m);right=histogram(weights,n);meet=histogram(weights,ell)
    largest=0;digest=sha256()
    for a in range(m):
        for b in range(n):
            intersection=meet[(a+m*((b-a)//g*inverse%q))%ell] if (b-a)%g==0 else 0
            value=left[a]+right[b]-intersection
            largest=max(largest,value);digest.update((str(value)+',').encode('ascii'))
    return largest,digest.hexdigest(),m*n


def uniform_bound(L,A):
    U=sum(1<<x for x in range(L) if all(x%m!=a for m,a in A))
    demand=U.bit_count();remaining=[m for m in kernel.divisors(L) if m>=8 and m not in dict(A)]
    return demand,sum(kernel.maximum_fibre(U,L,m) for m in remaining)


def seen_for_prefix(A):
    seen={}
    for m,a in A:
        for p,levels in kernel.factor_levels(m):
            for power in levels:
                k=p,power,a%power;c=a//power%p;old=seen.get(k,0)
                if c>=min(p,old+1):raise ValueError('Noncanonical certificate prefix')
                seen[k]=max(old,c+1)
    return seen


def next_options(m,A):
    return [a for a,_ in kernel.canonical_options(m,seen_for_prefix(A))]


def sieve():
    density=[];structural=[];retained=[]
    for L in range(10080,30240,8):
        capacity=sum(L//m for m in kernel.divisors(L) if m>=8)
        if capacity<L:density.append(L);continue
        rest=L
        for p in (2,3,5):
            while rest%p==0:rest//=p
        if rest==1 and L%5400:structural.append(L);continue
        retained.append(L)
    return density,structural,retained


def prove(certificate,reference_bound=None,reference_options=None,
          decoder=decode,pair_counter=pair_capacities,uniform_counter=uniform_bound,
          child_options=next_options,sieve_fn=sieve):
    if certificate['format_version']!=1 or certificate['agent']!='six-covering-2' or certificate['role']!='researcher':
        raise ValueError('Unknown schema or author')
    if (certificate['lower'],certificate['upper_exclusive'])!=(10080,30240):raise ValueError('Wrong interval')
    density,structural,retained=sieve_fn()
    if len(density)+len(structural)+len(retained)!=2520:raise ValueError('Incomplete interval scan')
    plans=certificate['plans'];plan_L=[p['L'] for p in plans]
    if any(p['method'] not in ('uniform','weighted_leaves') for p in plans):raise ValueError('Unknown case method')
    if plan_L!=sorted(set(plan_L)) or not set(plan_L).issubset(retained):raise ValueError('Invalid case plans')
    remaining=sorted(set(retained)-set(plan_L))
    if remaining!=certificate['remaining_LCMs'] or remaining!=TARGET_REMAINING:
        raise ValueError('The theorem requires every stated LCM exclusion')
    records={}
    for record in certificate['nodes']:
        L=record['L'];A=record['anchors'];K=key(L,A)
        if K in records:raise ValueError('Duplicate certificate prefix')
        if len({m for m,a in A})!=len(A) or any(type(m) is not int or type(a) is not int or m<8 or L%m or not 0<=a<m for m,a in A):
            raise ValueError('Invalid placed classes')
        if record['kind'] not in ('uniform','weighted','expanded'):raise ValueError('Open or invalid proof record')
        records[K]=record
    used=set();events=sha256();pair_events=sha256();counts=Counter();cases=[]
    pair_phase_count=0;support_points=0;box_count=0
    def visit(L,A):
        nonlocal pair_phase_count,support_points,box_count
        K=key(L,A)
        if K not in records:raise ValueError('Missing completion certificate')
        if K in used:raise ValueError('Repeated proof-node use')
        used.add(K);record=records[K];kind=record['kind'];payload=record['payload'];counts[kind]+=1
        B=[m for m in kernel.divisors(L) if m>=8 and m not in dict(A)]
        if kind=='expanded':
            m=payload['modulus'];phases=payload['phases']
            if m not in B or phases!=child_options(m,A):raise ValueError('Incomplete canonical child list')
            if not phases:raise ValueError('Empty branch')
            events.update((json.dumps([L,A,kind,m,phases],separators=(',',':'))+'\n').encode())
            for a in phases:visit(L,A+[(m,a)])
            return
        if kind=='uniform':
            D,C=uniform_counter(L,A)
            if D<=C or (D,C)!=(payload['demand'],payload['capacity']):raise ValueError('Failed uniform cut')
            events.update((json.dumps([L,A,kind,D,C],separators=(',',':'))+'\n').encode())
            return
        boxes=payload['boxes'];weights=decoder(L,boxes);D=sum(weights)
        if D<=0 or any(w and any(x%m==a for m,a in A) for x,w in enumerate(weights)):
            raise ValueError('Weights have invalid support')
        support_points+=sum(bool(w) for w in weights);box_count+=len(boxes)
        pairs=payload.get('pairs',[]);assigned=set()
        for pair in pairs:
            if len(pair)!=2 or pair[0]==pair[1] or any(type(m) is not int or m not in B or m in assigned for m in pair):
                raise ValueError('Invalid or overlapping resource groups')
            assigned.update(pair)
        groups=[tuple(pair) for pair in pairs]+[(m,) for m in B if m not in assigned]
        capacities=[]
        for group in groups:
            if len(group)==1:C=max(histogram(weights,group[0]))
            else:
                C,h,phases=pair_counter(weights,*group);pair_phase_count+=phases
                pair_events.update((json.dumps([L,A,group,h],separators=(',',':'))+'\n').encode())
            capacities.append(C)
        C=sum(capacities)
        if D<=C or (D,C)!=(payload['demand'],payload['capacity']):raise ValueError('Failed exact weighted cut')
        counts['grouped_weighted']+=bool(pairs)
        events.update((json.dumps([L,A,kind,D,list(zip(groups,capacities))],separators=(',',':'))+'\n').encode())
    for plan in plans:
        L=plan['L'];anchors=plan['anchors'];before=counts.copy();before_used=len(used)
        deferred=[]
        def callback(tag,phases,value):
            if value>=L:
                if plan['method']!='weighted_leaves':raise ValueError('Unexcluded ordinary anchor leaf')
                A=list(zip(anchors,phases));deferred.append(A);visit(L,A)
        manifest=kernel.search_case(L,anchors,prune=True,reference_bound=reference_bound,
                                   reference_options=reference_options,terminal_callback=callback)
        if plan['method']=='uniform' and not manifest['excludes']:raise ValueError('Case not excluded')
        if plan['method']=='weighted_leaves' and len(deferred)!=manifest['leaves']:raise ValueError('Missing deferred leaf')
        completion=counts-before
        cases.append({'L':L,'method':plan['method'],'base_manifest':manifest,
                      'completion_nodes':len(used)-before_used,'completion_counts':dict(sorted(completion.items()))})
    if used!=set(records):raise ValueError('Unused certificate records')
    return {'agent':'six-covering-2','role':'researcher','status':'COMPLETE EXACT FINITE LCM REDUCTION',
        'interval':[10080,30240],'upper_exclusive':True,'raw_multiples_of_8':2520,
        'density_exclusions':len(density),'structural_exclusions':structural,
        'direct_LCM_exclusions':plan_L,'remaining_LCMs':remaining,
        'upper_L_min_8_input':UPPER_BOUND_INPUT,
        'possible_L_min_8':[L for L in remaining if L<=UPPER_BOUND_INPUT],
        'binary_exponent_lower_bound_input':BINARY_EXPONENT_INPUT,
        'three_prime_235_LCM_multiple_input':2**BINARY_EXPONENT_INPUT*3**3*5**2,
        'three_prime_235_LCM_lower_bound':2*(2**BINARY_EXPONENT_INPUT*3**3*5**2),
        'completion_node_counts':dict(sorted(counts.items())),'boxes':box_count,
        'positive_weight_points_checked':support_points,'pair_phase_tuples_checked':pair_phase_count,
        'completion_events_sha256':events.hexdigest(),'pair_capacities_sha256':pair_events.hexdigest(),
        'cases':cases}


def main():
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=BASE/'certificate.json')
    p.add_argument('--write',type=Path);p.add_argument('--expected',type=Path,default=BASE/'expected.json')
    args=p.parse_args();start=monotonic();certificate=json.loads(args.certificate.read_text())
    actual=prove(certificate)
    if args.write:args.write.write_text(json.dumps(actual,indent=2)+'\n')
    else:
        if actual!=json.loads(args.expected.read_text()):raise ValueError('Manifest mismatch')
    print(json.dumps({k:v for k,v in actual.items() if k!='cases'},indent=2))
    print(f'Elapsed seconds: {monotonic()-start:.3f}')


if __name__=='__main__':main()
