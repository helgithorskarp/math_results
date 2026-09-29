"""Independent exact checker of axis-only interval chamber certificates.

Only Python's standard library is used. No model or optimizer is imported.
Intervals are reconstructed as sparse affine polynomials; multiplication
of positions and literal interval membership are checked separately.
"""
import argparse
from collections import Counter
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path

if not __debug__:
    raise RuntimeError('Run this proof checker with assertions enabled; omit -O.')


def plus(*parts):
    result={}
    for part in parts:
        for j,v in part.items():result[j]=result.get(j,0)+v
    return {j:v for j,v in result.items() if v}


def times(v,p):return {j:v*x for j,x in p.items() if v*x}
def minus(p,q):return plus(p,times(-1,q))


def check_word(word):
    n=len(word)+1;assert n%2 and n>=3
    assert all(type(c)is int and c in range(6) for c in word)
    assert word==word[::-1]
    supports=[{x for x,c in enumerate(word,1) if c==j} for j in range(6)]
    for S in supports:assert all((x+y)%n not in S for x in S for y in S)
    return dict(modulus=n,endpoint=n-1,class_sizes=list(map(len,supports)),status='LITERAL_MODULAR_WORD_VERIFIED')


def unit_image(word,u):
    n=len(word)+1;assert math.gcd(u,n)==1;image=[None]*len(word)
    for x,c in enumerate(word,1):image[(u*x)%n-1]=c
    assert None not in image
    return image


def intervals(word):
    h=len(word)//2;parsed=[(c,len(list(g))) for c,g in itertools.groupby(word[:h])]
    lengths=[v for c,v in parsed];d=len(parsed);cursor={-1:1};one={-1:1}
    a={-1:1,**{j:2 for j in range(d)}};positive={c:[] for c in range(6)}
    for j,(c,length) in enumerate(parsed):
        after=plus(cursor,{j:1});positive[c].append((cursor,minus(after,one)));cursor=after
    E={c:positive[c]+[(minus(a,U),minus(a,L)) for L,U in positive[c]] for c in range(6)}
    return dict(dimension=d,lengths=lengths,colours=[c for c,v in parsed],E=E,a=a,one=one)


def inequality(m,reason,derived):
    kind=reason[0]
    if kind=='integer_rounding':
        j=reason[1];assert 0<=j<len(derived);return derived[j]
    if kind=='positive_run_length':
        j=reason[1];assert 0<=j<m['dimension'];form={-1:1,j:-1}
    else:
        assert kind=='axis_sum'
        _,c,i,j,z,t,side=reason;assert c in range(6) and t in (0,1)
        assert side in ('left_before_right','right_before_left')
        E=m['E'][c];assert all(0<=v<len(E) for v in (i,j,z))
        lo=plus(E[i][0],E[j][0]);hi=plus(E[i][1],E[j][1])
        L=plus(E[z][0],times(t,m['a']));U=plus(E[z][1],times(t,m['a']))
        form=plus(minus(hi,L),m['one']) if side=='left_before_right' else plus(minus(U,lo),m['one'])
        divisor=math.gcd(*form.values());assert divisor>=1
        form={j:v//divisor for j,v in form.items()}
    value=sum(v*(1 if j==-1 else m['lengths'][j]) for j,v in form.items())
    assert value<=0,(reason,value)
    return form


def membership(seed,word):
    """Literal numeric intervals, independent of the affine proof checker."""
    def numeric(w):
        n=len(w)+1;cursor=1;positive={c:[] for c in range(6)};pattern=[];lengths=[]
        for c,g in itertools.groupby(w[:len(w)//2]):
            count=len(list(g));pattern.append(c);lengths.append(count)
            positive[c].append((cursor,cursor+count-1));cursor+=count
        E={c:positive[c]+[(n-U,n-L) for L,U in positive[c]] for c in range(6)}
        return n,pattern,lengths,E
    old=numeric(seed);new=numeric(word);assert old[1]==new[1];checked=0
    for c in range(6):
        for i,j,z in itertools.product(range(len(old[3][c])),repeat=3):
            for t in (0,1):
                sides=[]
                for n,pattern,lengths,E in (old,new):
                    lo=E[c][i][0]+E[c][j][0];hi=E[c][i][1]+E[c][j][1]
                    L=E[c][z][0]+t*n;U=E[c][z][1]+t*n
                    assert hi<L or U<lo;sides.append(hi<L)
                assert sides[0]==sides[1];checked+=1
    return dict(status='LITERAL_AXIS_CHAMBER_MEMBERSHIP_VERIFIED',comparisons=checked,run_lengths=new[2])


def verify(source,witness_source=None):
    data=json.loads(Path(source).read_text());full=data['seed_word'];a0=data['seed_axis_factor']
    assert len(full)==5*a0-1;full_check=check_word(full)
    seed=[full[5*q-1] for q in range(1,a0)];check_word(seed)
    expected=[u for u in range(1,a0//2+1) if math.gcd(u,a0)==1]
    assert [c['multiplier'] for c in data['chambers']]==expected
    terms=0;cuts=0;types=Counter();bounds=[];dimensions=[];records=[]
    for cert in data['chambers']:
        u=cert['multiplier'];image=unit_image(seed,u);assert image==unit_image(seed,a0-u);check_word(image)
        m=intervals(image);d=m['dimension'];assert d==cert['dimension'] and m['colours']==cert['run_colours']
        dimensions.append(d);derived=[]
        def combine(proof):
            nonlocal terms
            result={}
            for term in proof['terms']:
                weight=Fraction(term['weight']);assert weight>0
                result=plus(result,times(weight,inequality(m,term['reason'],derived)))
                terms+=1;types[term['reason'][0]]+=1
            return result
        for cut in cert['rounding_cuts']:
            if 'coordinate' in cut:
                j=cut['coordinate'];assert 0<=j<d;obj={j:1}
            else:
                vector=cut['coefficients'];assert len(vector)==d and all(type(v)is int for v in vector)
                obj={j:v for j,v in enumerate(vector) if v}
            upper=Fraction(cut['upper']);assert combine(cut)==plus(obj,{-1:-upper})
            derived.append(plus(obj,{-1:-(upper.numerator//upper.denominator)}));cuts+=1
        upper=Fraction(cert['upper_bound_axis_factor']);assert upper>=a0
        assert combine(cert)==plus(m['a'],{-1:-upper})
        cap=upper.numerator//upper.denominator
        while cap%2==0 or cap%3==0:cap-=1
        bounds.append(cap);records.append(dict(multiplier=u,rational_bound=str(upper),integer_axis_cap=cap))
    cap=max(bounds)
    report=dict(status='INDEPENDENT_AXIS_CERTIFICATES_VERIFIED',complete_axis_unit_cover=True,
        axis_unit_representatives=len(expected),axis_units=2*len(expected),seed_modulus=a0,
        dimensions=[min(dimensions),max(dimensions)],certificate_terms=terms,integer_rounding_steps=cuts,
        reason_counts=dict(types),integer_axis_upper_bound=cap,full_symmetric_endpoint_upper_bound=5*cap-1,
        off_axis_colours_unrestricted=True,seed_full_word_check=full_check,bounds=records)
    if witness_source:
        w=json.loads(Path(witness_source).read_text());word=w['axis_word'];u=w['multiplier'];assert u in expected
        check=check_word(word);assert check['modulus']==cap==w['axis_factor']
        member=membership(unit_image(seed,u),word);assert member['run_lengths']==w['run_lengths']
        report.update(axis_maximum_exact=True,axis_witness_check=check,witness_membership_comparisons=member['comparisons'])
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source');p.add_argument('--witness')
    args=p.parse_args();print(json.dumps(verify(args.source,args.witness),indent=2))
