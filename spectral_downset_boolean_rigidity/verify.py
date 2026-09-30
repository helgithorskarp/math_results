#!/usr/bin/env python3
"""Exact finite validation of Boolean boundary H rigidity.

Author six-downset-3, role researcher. CPython3.11.2 standard library only.
The all-orders proof, including arbitrary-real matrix uniqueness and
product completeness, is in PROOF.md; finite replay does not replace it.
No imported campaign code, solver, float, external input or proof assistant.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, separators=(',', ':'), sort_keys=True).encode()


def intersecting(family):
    return all(a & b for a in family for b in family)


def selector(n, family):
    full=(1 << n)-1
    family=set(family)
    return (all(isinstance(a,int) and 0<a<full for a in family) and
            all((a in family)+(full ^ a in family)==1 for a in range(1,full)) and
            all(b in family for a in family for b in range(1,full) if a & b==a))


def exchange(n, a):
    """Finite greedy extension with a forced minimal member a."""
    full=(1 << n)-1
    require(n>=2 and 0<a<full, 'exchange domain')
    f={a}
    f.update(full ^ b for b in range(1,full) if b!=a and b & a==b)
    require(intersecting(f), 'initial forced-minimal seed')
    for b in range(1,full):
        if all(b & c for c in f):
            f.add(b)
    g=(f-{a})|{full ^ a}
    require(a in f and full ^ a not in f, 'exchange membership')
    require(not any(b!=a and b & a==b for b in f), 'a is minimal')
    require(intersecting(f) and intersecting(g), 'both exchange families intersect')
    require(selector(n,f) and selector(n,g), 'both are upward complementary selectors')
    require(len(f)==len(g)==(1 << (n-1))-1, 'exchange cardinalities')
    require(f-g=={a} and g-f=={full ^ a}, 'single-pair exchange')
    return tuple(sorted(f)), tuple(sorted(g))


def cube(n):
    """Binary masks, with the full set removed and the empty set retained."""
    require(isinstance(n,int) and n>=2, 'cube order')
    full=(1 << n)-1
    N=full; s=(1 << (n-1))-1
    L=[[0]*N for _ in range(N)]
    L[0]=[1]*N
    for a in range(1,N):
        L[a][0]=1
        L[a][a]=s
        L[a][full ^ a]=s
    T=[[L[a][b]-s*(a==b) for b in range(N)] for a in range(N)]
    return full,s,L,T


def rank(rows):
    """Exact sparse row rank, including zero-width and rational inputs."""
    width=len(rows[0]) if rows else 0
    require(all(len(row)==width for row in rows), 'rank rectangular input')
    pivots={}
    for source in rows:
        row={i:Q(x) for i,x in enumerate(source) if x}
        while row:
            p=min(row)
            if p not in pivots:
                scale=row[p]
                pivots[p]={i:x/scale for i,x in row.items()}
                break
            t=row[p]
            for i,x in pivots[p].items():
                z=row.get(i,Q(0))-t*x
                if z:row[i]=z
                else:row.pop(i,None)
    return len(pivots)


def unique_constraints(n, L):
    """Eliminate every supported real H variable using exchange equalities.

    A full-rank rational coefficient matrix also has full rank over R.
    No PSD assumption is imposed in this linear elimination: PSD is the
    written justification of the exchange equalities for an arbitrary H.
    """
    full=(1 << n)-1;N=full;s=(1 << (n-1))-1
    variables=[(0,0)]+[(a,b) for a in range(N) for b in range(a+1,N) if not a & b]
    index={v:i for i,v in enumerate(variables)}
    def entry(a,b):
        if a>b:a,b=b,a
        if (a,b) in index:return {index[(a,b)]:Q(1)},Q(0)
        return {},Q(s if a==b else 0)
    equations=[]
    for a in range(1,N):
        ac=full ^ a
        if a>ac:continue
        for b in range(N):
            l,lc=entry(b,a);r,rc=entry(b,ac)
            d=l.copy()
            for i,v in r.items():
                z=d.get(i,Q(0))-v
                if z:d[i]=z
                else:d.pop(i,None)
            equations.append((d,rc-lc))
    for a in range(N):
        row={};constant=Q(0)
        for b in range(N):
            x,y=entry(a,b);constant+=y
            for i,v in x.items():row[i]=row.get(i,Q(0))+v
        equations.append((row,Q(N)-constant))
    values=[Q(L[a][b]) for a,b in variables]
    require(all(sum(x*values[i] for i,x in row.items())==rhs for row,rhs in equations),
            'proposed matrix satisfies every forced linear constraint')
    pivots={}
    for source,rhs in equations:
        row=source.copy()
        while row:
            p=min(row)
            if p not in pivots:
                t=row[p]
                pivots[p]=({i:x/t for i,x in row.items()},rhs/t)
                break
            prior,prior_rhs=pivots[p];t=row[p];rhs-=t*prior_rhs
            for i,x in prior.items():
                z=row.get(i,Q(0))-t*x
                if z:row[i]=z
                else:row.pop(i,None)
        else:require(rhs==0,'forced system is consistent')
    require(len(pivots)==len(variables),'zero homogeneous constraint nullity')
    require(len(variables)==(3**n-1)//2,'complete supported variable count')
    return {'supported_symmetric_variables':len(variables),
            'constraint_rows':len(equations),'coefficient_rank':len(pivots),
            'homogeneous_nullity':len(variables)-len(pivots)}


def check_cube(n):
    full,s,L,T=cube(n);N=full
    require(all(L[a][b]==L[b][a] for a in range(N) for b in range(N)), 'L symmetry')
    require(all(sum(row)==N for row in L), 'L row sums')
    require(all(sum(row)==s+1 for row in T), 'M row sums')
    require(all(T[a][b]==0 for a in range(N) for b in range(N) if a & b), 'M support')
    pairs=[(a,full ^ a) for a in range(1,N) if a<full ^ a]
    require(len(pairs)==s,'literal complementary-pair count')
    V=[[1]*s]+[[s*int(a in pair) for pair in pairs] for a in range(1,N)]
    require(all(sum(x*y for x,y in zip(V[a],V[b]))==s*L[a][b]
                for a in range(N) for b in range(N)),'integer Gram sL=VV^T')
    # Direct sparse multiplication; the construction is not used to infer
    # the desired identity without multiplying its literal entries.
    nz=[[(k,x) for k,x in enumerate(row) if x] for row in T]
    require(all(sum(x*T[k][b] for k,x in nz[a])==s*s*(a==b)+1
                for a in range(N) for b in range(N)), 'T^2=s^2 I+J')
    require(sum(T[a][a] for a in range(N))==1-s,'trace determines multiplicities')
    # s pair differences plus one explicit centered maximum generate the
    # universally forced kernel. Gaussian rank is an implementation check.
    star={a for a in range(1,N) if a & 1}
    basis=[]
    for a,b in pairs:
        v=[0]*N;v[a]=1;v[b]=-1;basis.append(v)
    z=[N*int(a in star)-s for a in range(N)];basis.append(z)
    require(all(sum(L[a][b]*v[b] for b in range(N))==0 for a in range(N) for v in basis),
            'all forced generators lie in actual lower kernel')
    require(rank(basis)==s+1,'forced kernel dimension')
    constraints=unique_constraints(n,L)
    witnesses=[]
    for a in range(1,N):
        f,g=exchange(n,a);witnesses.append([a,list(f),list(g)])
    return {'n':n,'N':N,'s':s,'lower_rank':s,'forced_kernel_dimension':s+1,
            'upper_slack_rank':N-1,'centered_core_rank':s-1,
            'spectrum':{'1':1,str(Q(s,s+1)):s-1,str(-Q(s,s+1)):s+1},
            'all_pair_exchange_witnesses':N-1,
            'exchange_witness_sha256':hashlib.sha256(canonical(witnesses)).hexdigest(),
            'L_binary_order_sha256':hashlib.sha256(canonical(L)).hexdigest(),
            'unique_real_H_linear_constraints':constraints}


def enumerate_intersecting(vertices):
    """Complete include/exclude recursion on a specified finite domain."""
    vertices=list(vertices);count=len(vertices)
    compatible=[sum(1 << j for j,b in enumerate(vertices) if a & b) for a in vertices]
    counts=Counter();maxima=[];best=0;nodes=0
    def visit(available,chosen,size):
        nonlocal best,nodes,maxima
        nodes+=1
        if not available:
            counts[size]+=1
            if size>best:best=size;maxima=[chosen]
            elif size==best:maxima.append(chosen)
            return
        low=available & -available;i=low.bit_length()-1;rest=available ^ low
        visit(rest,chosen,size)
        visit(rest & compatible[i],chosen | low,size+1)
    visit((1 << count)-1,0,0)
    fams=[tuple(vertices[i] for i in range(count) if x >> i & 1) for x in sorted(maxima)]
    return {'recursion_nodes':nodes,'all_intersecting_families':sum(counts.values()),
            'maximum_size':best,'maximum_families':len(fams),
            'cardinality_distribution':{str(k):counts[k] for k in sorted(counts)}},fams


def psd_rank(matrix):
    """Rational symmetric Schur congruence, including singular pivots."""
    n=len(matrix)
    require(all(len(row)==n for row in matrix),'PSD square')
    require(all(matrix[i][j]==matrix[j][i] for i in range(n) for j in range(n)), 'PSD symmetric')
    A=[[Q(x) for x in row] for row in matrix];rank_value=0
    for k in range(n):
        pivot=A[k][k]
        require(pivot>=0,'negative Schur pivot')
        if pivot==0:
            require(all(A[k][j]==0 for j in range(k+1,n)),'zero pivot with nonzero row')
            continue
        rank_value+=1
        for i in range(k+1,n):
            for j in range(i,n):
                z=A[i][j]-A[i][k]*A[k][j]/pivot;A[i][j]=A[j][i]=z
    return rank_value


def tensor(A,B):
    return [[x*y for x in row_a for y in row_b] for row_a in A for row_b in B]


def product_check(orders,census=False):
    matrices=[];vertices=[0];shift=0;N=1
    for n in orders:
        full,s,L,T=cube(n);matrices.append([[Q(x,s+1) for x in row] for row in T])
        vertices=[a | (b << shift) for a in vertices for b in range(full)]
        shift+=n;N*=full
    M=[[Q(1)]]
    for B in matrices:M=tensor(M,B)
    critical=max(orders);c=orders.count(critical);sf=(1 << (critical-1))-1;Nf=(1 << critical)-1
    s=N*sf//Nf;require(s*Nf==N*sf,'integral largest star')
    require(all(sum(row)==1 for row in M),'product row sums')
    require(all(M[a][b]==0 for a in range(N) for b in range(N) if vertices[a] & vertices[b]),
            'product literal disjoint support')
    L=[[(N-s)*M[i][j]+s*(i==j) for j in range(N)] for i in range(N)]
    U=[[int(i==j)-M[i][j] for j in range(N)] for i in range(N)]
    lr=psd_rank(L);ur=psd_rank(U)
    require(lr==N-c*(sf+1) and ur==N-1,'tensor rank formula and simple unit')
    result={'orders':orders,'N':N,'s':s,'critical_order':critical,'critical_factors':c,
            'lower_rank':lr,'universal_forced_kernel_dimension':c*(sf+1),'upper_slack_rank':ur}
    if census:
        cc,fams=enumerate_intersecting(vertices[1:])
        # The all-zero tuple is the only excluded looped vertex.
        expected=[];offset=0
        for i,n in enumerate(orders):
            if n==critical:
                _,base_fams=enumerate_intersecting(range(1,(1 << n)-1))
                mask=(1 << n)-1
                for family in base_fams:
                    expected.append(tuple(a for a in vertices if (a >> offset & mask) in family))
            offset+=n
        require(cc['maximum_size']==s,'complete product maximum size')
        require(set(fams)==set(expected),'complete product census equals predicted cylinders')
        result['complete_intersecting_census']=cc
    return result


def rejected_controls():
    trials=[('negative',[[-1]]),('indefinite',[[1,2],[2,1]]),
            ('zero_form_nonzero_image',[[0,1],[1,1]]),
            ('asymmetric',[[1,1],[0,1]]),('nonsquare',[[1,0]])]
    rejected=[]
    for name,x in trials:
        try:psd_rank(x)
        except ValueError:rejected.append(name)
        else:raise ValueError('bad PSD control accepted: '+name)
    full,s,L,T=cube(3)
    bad=[row.copy() for row in L];bad[1][full ^ 1]+=1
    try:unique_constraints(3,bad)
    except ValueError:rejected.append('corrupted_complement_entry')
    else:raise ValueError('bad rigidity control accepted')
    require(not selector(3,{1,2,3}),'bad selector rejected')
    rejected.append('nonintersecting_selector')
    return rejected


def psd_engine_control():
    """All729 symmetric ternary3-by-3 matrices versus principal minors."""
    psd_count=0
    for a,b,c,d,e,f in itertools.product((-1,0,1),repeat=6):
        A=[[a,b,c],[b,d,e],[c,e,f]]
        exact=(a>=0 and d>=0 and f>=0 and a*d-b*b>=0 and
               a*f-c*c>=0 and d*f-e*e>=0 and
               a*d*f+2*b*c*e-a*e*e-d*c*c-f*b*b>=0)
        try:psd_rank(A);got=True
        except ValueError:got=False
        require(got==exact,'PSD engine agrees with independent principal minors')
        psd_count+=exact
    return {'symmetric_ternary_3_by_3_matrices':729,'positive_semidefinite':psd_count,
            'all_principal_minor_comparison':True}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    cubes=[check_cube(n) for n in range(2,8)]
    enumerations=[]
    for n in range(2,6):
        cc,fams=enumerate_intersecting(range(1,(1 << n)-1))
        require(cc['maximum_size']==(1 << (n-1))-1,'proper-cube maximum census')
        require(all(selector(n,f) for f in fams),'every finite maximum is a monotone selector')
        enumerations.append({'n':n,**cc})
    # Independently reproduce the known n4 rigidity and twelve-maxima input.
    require(cubes[2]['s']==7 and cubes[2]['lower_rank']==7 and
            cubes[2]['forced_kernel_dimension']==8 and
            cubes[2]['unique_real_H_linear_constraints']['supported_symmetric_variables']==40,
            'known four-point spectral baseline')
    require(enumerations[2]['all_intersecting_families']==688 and
            enumerations[2]['maximum_families']==12,'known four-point complete-family baseline')
    require(psd_rank([[Q(1,4),Q(1,2)],[Q(1,2),1]])==1,'singular rational Gram control')
    products=[product_check(v,v in ([2,2],[2,3]))
              for v in ([2,2],[2,3],[3,3],[2,4],[2,2,2])]
    result={'agent':'six-downset-3','role':'researcher','arithmetic':'standard-library integers and Fraction',
            'claim_status':'Author-checked written all-orders proof; finite implementation validation, no independent review or formalization.',
            'proper_cubes':cubes,'complete_small_order_censuses':enumerations,'finite_products':products,
            'PSD_engine_control':psd_engine_control(),
            'negative_controls_rejected':rejected_controls()}
    encoded=json.dumps(result,indent=2)+'\n'
    if args.check:require(result==json.loads(args.check.read_text()),'expected summary differs')
    if args.output:args.output.write_text(encoded)
    print(json.dumps({'ok':True,'agent':'six-downset-3','role':'researcher',
                      'proper_orders':[v['n'] for v in cubes],
                      'exchange_witnesses':sum(v['all_pair_exchange_witnesses'] for v in cubes),
                      'complete_base_orders':[v['n'] for v in enumerations],
                      'maximum_counts':[v['maximum_families'] for v in enumerations],
                      'finite_products':len(products),'negative_controls':len(result['negative_controls_rejected']),
                      'result_sha256':hashlib.sha256(encoded.encode()).hexdigest()}))


if __name__=='__main__':main()
