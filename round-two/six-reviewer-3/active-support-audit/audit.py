#!/usr/bin/env python3
"""Independent exact audit of near-middle support, with factor2 refinement."""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from exact import need,R,P
from symbolic import derive
from face import finite_case,profiles,base,forms,quad
from original import run as original
from controls import run as controls

HERE=Path(__file__).resolve().parent


def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()


def scalar(n,k):
    T=2**(n-1);h=T-1;c=F(2,n);q1=-F(5,n*n);q2=-F(2*n+10,n*n)
    B=base(n);p,q=profiles(n,k)
    phi=(n*h-n*(n-1)*B[(1,1)])*q1*q1
    phi+=(n*(n-1)*(2*n-3)-F(n*(n-1)*(n-2)*(n-3),4)*B[(2,2)])*q2*q2
    phi-=(n*(n-1)*(n-2)*B[(1,2)]+2*n*(n-1)*(n-2))*q1*q2
    total=4*(T-n-1)+phi+sum((comb(n,a)*((n-1)*q[a-1]**2-2*(n-2)*c*q[a-1]) for a in range(3,n-2)),F(0))
    return total


def tails():
    records=[]
    for n in (64,128,256):
        T=2**(n-1);B=0;old=2;new=2
        rows=[]
        for k in range(2,(n-1)//2+1):
            if k>=3:B+=comb(n,k)
            if 6*n*n*B<=T:old=k
            if 2*n*n*B<=T:new=k
            rows.append((k,B))
        need(new>=old and new+1<n/2,'complete exact tail scan range')
        b=dict(rows)[new];next_b=dict(rows)[new+1];W=scalar(n,new)
        need(2*n*n*b<=T<2*n*n*next_b,'entire exact factor2 tail threshold and first failing successor')
        need(W<-F(T,4*n),'exact rank-one scalar meets stronger universal negative margin')
        records.append({'n':n,'T':str(T),'original_largest_excluded_k':old,'original_forced_minimum_size':old+1,'improved_largest_excluded_k':new,'improved_forced_minimum_size':new+1,'improved_tail_sum':str(b),'next_tail_sum':str(next_b),'entire_exact_profile_pairing':str(W),'strict_universal_upper_bound':str(-F(T,4*n))})
    return records


def build():
    control=controls();sym=derive();cases=[finite_case(n,k) for n,k in ((9,3),(12,4),(19,5))]
    for case in cases:
        n,k=case['n'],case['k'];need(F(case['combined_energy'])==scalar(n,k),'entire physical pairing versus separately assembled scalar')
        p2,q2=profiles(n,2);K,U=forms(n,base(n));need(quad(K,p2)+quad(U,q2)==scalar(n,2),'whole base k2 scalar versus both physical forms')
        p,q=profiles(n,k);qstar=F(2*(n-2),n*(n-1))
        difference=2*(n-1)*sum((comb(n,a)*((F(2,n)-F((2*n+5)*a,n*n)-qstar)**2-(q2[a-1]-qstar)**2) for a in range(3,k+1)),F(0))
        need(scalar(n,k)-scalar(n,2)==difference,'entire tail modification identity with both mirrors')
    original_record=original();tail=tails()
    return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','method':'direct original-index lift/star actions and rank-one restrictions, independent Q(n)[formal T] scalar certificate, complete low-completion directions, exact binomial tails; no researcher executable','symbolic':sym,'controls':control,'finite_real_faces':cases,'finite_permitted_directions':sum(len(c['all_permitted_directions']) for c in cases),'original_index':original_record,'exact_tail_examples':tail,'proved_quantitative_outside_functional':'h sum_ordered original disjoint nonempty A,B, union proper, min sizes>k (f_|A| f_|B|-g_|A| g_|B|) M_AB > T/(4n), if2n^2 B_(n,k)<=T and integer n>=64','unformalized_bridges':'real PSD zero-energy star kernels and cap restrictions, affine profile shifts on original F, every-coordinate cancellation, Rademacher moment counting, integer exponential induction and ordinary Chernoff bound; no averaging or harmonic-sector completeness needed'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--fixture',type=Path,default=HERE/'EXPECTED.json');p.add_argument('--emit-fixture',type=Path);args=p.parse_args()
    record=build()
    if args.emit_fixture:args.emit_fixture.write_text(json.dumps(record,indent=2)+'\n')
    else:need(canonical(record)==canonical(json.loads(args.fixture.read_text())),'entire independent frozen record')
    print(json.dumps({'status':'PASS','actual_agent':'six-reviewer-3','method':record['method'],'symbolic_real_n_lower':64,'native_math':'standard library exact arithmetic','finite_face_cases':[[c['n'],c['k']] for c in record['finite_real_faces']],'finite_permitted_directions':record['finite_permitted_directions'],'original_index_checks':record['original_index']['checks'],'kernel_checks':record['controls']['exact_kernel_checks'],'mathematical_damage_rejections':len(record['controls']['mathematical_damage_rejections'])+len(record['original_index']['mathematical_damage_rejections']),'domain_rejections':len(record['controls']['domain_rejections']),'improved_tail_factor':2,'improved_forced_sizes':[[r['n'],r['improved_forced_minimum_size']] for r in record['exact_tail_examples']],'record_sha256':sha256(canonical(record)).hexdigest()},sort_keys=True))


if __name__=='__main__':main()
