"""Independent, standard-library checker of semantic interval dual certificates.

Imports neither the linear-model generator nor an optimizer. Reconstructs
only the certificate's selected inequalities directly from their interval
meanings, then checks their nonnegative rational sum exactly.
"""
import argparse
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path


def plus(*polynomials):
    p={}
    for q in polynomials:
        for i,v in q.items():p[i]=p.get(i,0)+v
    return {i:v for i,v in p.items() if v}


def times(c,p):return {i:c*v for i,v in p.items() if c*v}
def minus(p,q):return plus(p,times(-1,q))


def check_word(w):
    n=len(w)+1;assert n%5==0 and n%2
    assert all(type(c)is int and c in range(6) for c in w)
    assert all(w[x-1]==w[n-x-1] for x in range(1,n))
    sets=[{x for x,c in enumerate(w,1) if c==j} for j in range(6)]
    for C in sets:
        assert not any((x+y)%n in C for x in C for y in C)
    for x,c in enumerate(w,1):
        if c==0:assert x%5 in (0,1,4)
        if c==1:assert x%5 in (0,2,3)
    return [sum(w[5*q+b-1]==b-1 for q in range(n//5)) for b in (1,2)]


def unit_image(w,u):
    n=len(w)+1;v=pow(u,-1,n);result=[]
    for x in range(1,n):
        c=w[(v*x)%n-1]
        result.append(1-c if u%5 in (2,3) and c<2 else c)
    return result


def symbolic_runs(w):
    a=(len(w)+1)//5
    sequences=[[w[5*x-1] for x in range(1,(a+1)//2)]]
    for b in (1,2):sequences.append([c if c>=2 else 0 for c in (w[5*q+b-1] for q in range(a))])
    parsed=[[(c,len(list(g))) for c,g in itertools.groupby(values)] for values in sequences]
    counts=list(map(len,parsed));seed=[length for part in parsed for _,length in part];dim=len(seed)
    one={-1:1};aform={-1:1,**{i:2 for i in range(counts[0])}}
    all_intervals=[];ends=[];index=0
    for part_index,part in enumerate(parsed):
        cursor=one.copy() if part_index==0 else {};group={c:[] for c in range(6)}
        for c,length in part:
            after=plus(cursor,{index:1});group[c].append((cursor,minus(after,one)))
            cursor=after;index+=1
        all_intervals.append(group);ends.append(cursor)
    positive,A,B=all_intervals
    E={c:positive[c]+[(minus(aform,U),minus(aform,L)) for L,U in positive[c]] for c in range(6)}
    eq=[minus(ends[1],aform),minus(ends[2],aform)]
    return dict(a=aform,one=one,E=E,A=A,B=B,seed=seed,dimension=dim,counts=counts,equalities=eq)


def semantic_inequality(m,reason,derived=()):
    one=m['one'];a=m['a'];E=m['E'];A=m['A'];B=m['B']
    def sum_intervals(*parts):return plus(*(p[0] for p in parts)),plus(*(p[1] for p in parts))
    def shifted(X,t):return plus(X[0],times(t,a)),plus(X[1],times(t,a))
    kind=reason[0]
    if kind=='integer_rounding':
        index=reason[1];assert 0<=index<len(derived)
        return derived[index]
    if kind=='positive_run_length':
        j=reason[1];assert 0<=j<m['dimension'];form=minus(one,{j:1})
    else:
        side=reason[-1];assert side in ('left_before_right','right_before_left')
        if kind=='axis_sum':
            _,c,i,j,z,t,_=reason;assert c in range(6) and t in (0,1)
            left=sum_intervals(E[c][i],E[c][j]);right=shifted(E[c][z],t)
        elif kind=='A_A_B':
            _,c,i,j,z,t,_=reason;assert c in (2,3,4,5) and t in (0,1)
            left=sum_intervals(A[c][i],A[c][j]);right=shifted(B[c][z],t)
        elif kind=='A_B_B_minus_one':
            _,c,i,j,k,t,_=reason;assert c in (2,3,4,5) and t in (1,2)
            left=sum_intervals(A[c][i],B[c][j],B[c][k]);point=minus(times(t,a),one);right=(point,point)
        else:
            assert kind=='difference_axis'
            _,name,state,i,j,z,t,_=reason
            assert name in ('A','B') and state in (0,2,3,4,5) and t in (-1,0)
            P=A if name=='A' else B;c=(0 if name=='A' else 1) if state==0 else state
            X,Y=P[state][i],P[state][j]
            left=(minus(X[0],Y[1]),minus(X[1],Y[0]));right=shifted(E[c][z],t)
        form=plus(minus(left[1],right[0]),one) if side=='left_before_right' else plus(minus(right[1],left[0]),one)
    # Match the canonical harmless positive gcd division used in the file.
    divisor=math.gcd(*form.values())
    assert divisor>=1
    form={i:v//divisor for i,v in form.items()}
    value=sum(v*(1 if i==-1 else m['seed'][i]) for i,v in form.items())
    assert value<=0,(reason,value)
    return form


def interval_membership(seed,word):
    """Compare literal numeric interval orders, not symbolic model rows."""
    def table(w):
        a=(len(w)+1)//5
        sequences=[[w[5*q-1] for q in range(1,(a+1)//2)]]
        for b in (1,2):sequences.append([c if c>=2 else 0 for c in (w[5*q+b-1] for q in range(a))])
        patterns=[];parts=[];lengths=[]
        for index,values in enumerate(sequences):
            start=1 if index==0 else 0;part={c:[] for c in range(6)};colours=[]
            for c,g in itertools.groupby(values):
                count=len(list(g));colours.append(c);lengths.append(count)
                part[c].append((start,start+count-1));start+=count
            patterns.append(colours);parts.append(part)
        positive,A,B=parts
        E={c:positive[c]+[(a-U,a-L) for L,U in positive[c]] for c in range(6)}
        return a,patterns,lengths,E,A,B
    old=table(seed);new=table(word);assert old[1]==new[1]
    checks=0
    def add(*parts):return sum(p[0] for p in parts),sum(p[1] for p in parts)
    def shift(p,t,a):return p[0]+t*a,p[1]+t*a
    def compare(values):
        nonlocal checks
        (x,y),(X,Y)=values
        assert x[1]<y[0] or y[1]<x[0]
        if x[1]<y[0]:assert X[1]<Y[0]
        else:assert Y[1]<X[0]
        checks+=1
    for c in range(6):
        for z in range(len(old[3][c])):
            for i in range(len(old[3][c])):
                for j in range(len(old[3][c])):
                    for t in (0,1):compare([(add(d[3][c][i],d[3][c][j]),shift(d[3][c][z],t,d[0])) for d in (old,new)])
    for c in (2,3,4,5):
        for z in range(len(old[5][c])):
            for i in range(len(old[4][c])):
                for j in range(len(old[4][c])):
                    for t in (0,1):compare([(add(d[4][c][i],d[4][c][j]),shift(d[5][c][z],t,d[0])) for d in (old,new)])
        for i in range(len(old[4][c])):
            for j in range(len(old[5][c])):
                for k in range(len(old[5][c])):
                    for t in (1,2):compare([(add(d[4][c][i],d[5][c][j],d[5][c][k]),(t*d[0]-1,t*d[0]-1)) for d in (old,new)])
    for part,special in ((4,0),(5,1)):
        for state in (0,2,3,4,5):
            c=special if state==0 else state
            for z in range(len(old[3][c])):
                for i in range(len(old[part][state])):
                    for j in range(len(old[part][state])):
                        for t in (-1,0):compare([((d[part][state][i][0]-d[part][state][j][1],d[part][state][i][1]-d[part][state][j][0]),shift(d[3][c][z],t,d[0])) for d in (old,new)])
    return dict(status='LITERAL_INTERVAL_CHAMBER_MEMBERSHIP_VERIFIED',comparisons=checks,
                run_lengths=new[2],run_counts=list(map(len,new[1])))


def verify(source,complete=True,witness_source=None):
    data=json.loads(Path(source).read_text());w=data['seed_word'];a0=data['seed_axis_factor'];n=5*a0
    assert len(w)==n-1;residual=check_word(w);assert residual[0]!=residual[1]
    expected=[u for u in range(1,n//2+1) if math.gcd(u,n)==1]
    actual=[c['multiplier'] for c in data['chambers']]
    assert len(actual)==len(set(actual)) and set(actual)<=set(expected)
    if complete:assert actual==expected
    bounds=[];terms=0;types=Counter();dimensions=[]
    for cert in data['chambers']:
        u=cert['multiplier'];image=unit_image(w,u);assert unit_image(w,n-u)==image
        assert check_word(image) in (residual,residual[::-1])
        m=symbolic_runs(image);assert m['counts']==cert['run_counts'] and m['dimension']==cert['dimension']
        dimensions.append(m['dimension']);derived=[]
        def combine(proof):
            nonlocal terms
            total={}
            for term in proof['terms']:
                weight=Fraction(term['weight']);assert weight>0
                p=semantic_inequality(m,term['reason'],derived)
                total=plus(total,times(weight,p));terms+=1;types[term['reason'][0]]+=1
            assert len(proof['equality_weights'])==2
            for weight,eq in zip(proof['equality_weights'],m['equalities']):total=plus(total,times(Fraction(weight),eq))
            return total
        for cut in cert.get('rounding_cuts',[]):
            j=cut['coordinate'];assert 0<=j<m['dimension'];upper=Fraction(cut['upper'])
            assert combine(cut)==plus({j:1},{-1:-upper})
            floor=upper.numerator//upper.denominator
            derived.append(plus({j:1},{-1:-floor}))
        total=combine(cert)
        upper=Fraction(cert['upper_bound_axis_factor'])
        assert total==plus(m['a'],{-1:-upper}),('dual identity',u,total)
        assert upper>=a0;bounds.append(upper)
    maximum=max(bounds);integer_cap=maximum.numerator//maximum.denominator
    while integer_cap%2==0 or integer_cap%3==0:integer_cap-=1
    result=dict(status='INDEPENDENT_SEMANTIC_RATIONAL_CERTIFICATES_VERIFIED',complete_unit_cover=actual==expected,
                unit_representatives=len(actual),all_units=2*len(expected),seed_endpoint=n-1,
                seed_residual_counts=residual,dimensions=[min(dimensions),max(dimensions)],
                rational_bounds=sorted(set(map(str,bounds))),maximum_rational_axis_bound=str(maximum),
                integer_axis_upper_bound=integer_cap,endpoint_upper_bound=5*integer_cap-1,
                certificate_terms=terms,reason_counts=dict(types))
    if witness_source:
        witness=json.loads(Path(witness_source).read_text());u=witness['multiplier'];assert u in actual
        counts=check_word(witness['word']);assert counts[0]!=counts[1]
        assert len(witness['word'])==5*witness['axis_factor']-1==result['endpoint_upper_bound']
        membership=interval_membership(unit_image(w,u),witness['word'])
        assert membership['run_lengths']==witness['run_lengths']
        result.update(attained_endpoint=len(witness['word']),witness_residual_counts=counts,
                      witness_class_sizes=[witness['word'].count(c) for c in range(6)],
                      witness_membership_comparisons=membership['comparisons'],
                      family_maximum_exact=True)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source');p.add_argument('--partial',action='store_true')
    p.add_argument('--witness')
    args=p.parse_args();print(json.dumps(verify(args.source,not args.partial,args.witness),indent=2))
