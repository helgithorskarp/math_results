"""Independent finite checks of the local pieces of the unbounded proof.

Tuple enumeration covers all 30 Pasch sides on six labelled points and
all 8192 legal local fills/orientations. Integer principal minors verify
all 729 possible T patterns. These checks supplement the ordinary proof;
bounded outside-sequence tests do not replace its all-orders argument.
six-downset-2, researcher. Standard library; assertions enabled.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations,product
import json
from pathlib import Path
from pasch_defect import all_trades,perturbation_certificate
from verify import exact_psd_rank,rejects


def matrix_digest(A):
    return sha256(json.dumps(A,separators=(',',':')).encode()).hexdigest()


def principal_rank(A):
    """All principal minors of a symmetric 3 by 3 integer matrix."""
    assert len(A)==3 and all(len(row)==3 for row in A)
    assert all(A[i][j]==A[j][i]for i in range(3)for j in range(3))
    minors=[(1,A[i][i])for i in range(3)]
    minors += [(2,A[i][i]*A[j][j]-A[i][j]**2)for i,j in combinations(range(3),2)]
    det=(A[0][0]*(A[1][1]*A[2][2]-A[1][2]**2)
         -A[0][1]*(A[0][1]*A[2][2]-A[1][2]*A[0][2])
         +A[0][2]*(A[0][1]*A[1][2]-A[1][1]*A[0][2]))
    minors.append((3,det));assert all(z>=0 for _,z in minors)
    return max((k for k,z in minors if z>0),default=0)


def run():
    points=tuple(range(6));triples=tuple(combinations(points,3));pairs=tuple(combinations(points,2))
    # Enumerate four triples directly, without the author's matching generator.
    sides=[]
    for candidate in combinations(triples,4):
        degrees=Counter(x for a in candidate for x in a)
        pair_degrees=Counter(p for a in candidate for p in combinations(a,2))
        if len(degrees)==6 and set(degrees.values())=={2} and set(pair_degrees.values())=={1}:
            assert len(pair_degrees)==12;sides.append(frozenset(candidate))
    assert len(sides)==30
    by_pairs={}
    for side in sides:
        key=tuple(sorted({p for a in side for p in combinations(a,2)}))
        by_pairs.setdefault(key,[]).append(side)
    assert len(by_pairs)==15 and all(len(z)==2 and z[0].isdisjoint(z[1])for z in by_pairs.values())
    independent={tuple(sorted(tuple(sorted(z))for z in two))for two in by_pairs.values()}
    authored={tuple(sorted(tuple(sorted(tuple(x for x in points if a>>x&1)for a in side))
                           for side in (even,odd)))for _,even,odd in all_trades(6)}
    assert authored==independent
    groups=((0,1),(2,3),(4,5))
    parity=[set(),set()]
    for a in triples:
        if all(len(set(a)&set(g))==1 for g in groups):
            parity[sum(next(j for j,x in enumerate(g)if x in a)for g in groups)%2].add(a)
    free=sorted(set(triples)-parity[0]-parity[1]);assert len(free)==12
    A=[[int(x==a)-int(x==b)for a,b in groups]for x in points]
    patterns=set();assignments=0;local_transcript=sha256()
    for bits in product((0,1),repeat=12):
        fill={a for a,bit in zip(free,bits)if bit}
        for orientation in (0,1):
            old=fill|parity[orientation];new=fill|parity[1-orientation]
            C=[[int(tuple(sorted((x,)+p))in old)if x not in p else 0 for p in pairs]for x in points]
            D=[[int(tuple(sorted((x,)+p))in new)if x not in p else 0 for p in pairs]for x in points]
            # Recover W from actual changed completions at each first partner.
            W=[[D[a][j]-C[a][j]for a,b in groups]for j in range(15)]
            assert all(D[x][j]-C[x][j]==sum(A[x][k]*W[j][k]for k in range(3))
                       for x in points for j in range(15))
            assert all(sum(W[j][k]*W[j][h]for j in range(15))==4*int(k==h)
                       for k in range(3)for h in range(3))
            assert all(sum(row[k]for row in W)==0 for k in range(3))
            assert all(sum(int(x in p)*W[j][k]for j,p in enumerate(pairs))==0
                       for x in points for k in range(3))
            Y=[[sum(C[x][j]*W[j][k]for j in range(15))+2*A[x][k]
                for k in range(3)]for x in points]
            T=[Y[a]for a,b in groups]
            assert all(Y[b]==[-z for z in T[k]]for k,(a,b)in enumerate(groups))
            assert all(T[k][k]==0 for k in range(3))
            assert all(abs(z)<=1 for row in T for z in row)
            flat=tuple(z for row in T for z in row);patterns.add(flat);assignments+=1
            local_transcript.update(json.dumps([orientation,bits,T],separators=(',',':')).encode()+b'\n')
    assert assignments==8192 and len(patterns)==729
    ranks=Counter();norm_transcript=sha256()
    for flat in sorted(patterns):
        T=[flat[3*i:3*i+3]for i in range(3)]
        for sign in (-1,1):
            form=[[8*int(i==j)+sign*2*(T[i][j]+T[j][i])for j in range(3)]for i in range(3)]
            ranks[principal_rank(form)]+=1
            norm_transcript.update(json.dumps(form,separators=(',',':')).encode()+b'\n')
    assert sum(ranks.values())==1458
    bounded=[]
    for n in range(8):
        count=0;maximum=0
        for sequence in product(range(-2,3),repeat=n):
            if sum(sequence):continue
            count+=1;value=sum(map(abs,sequence));assert value<=4*(n//2)
            maximum=max(maximum,value)
        assert maximum==4*(n//2)
        bounded.append({'outside_points':n,'zero_sum_sequences':count,'maximum_L1':maximum})
    certificate=perturbation_certificate(13,F(50,3))
    comparison=[[F(26,3),F(-12)],[F(-12),F(50,3)]]
    assert exact_psd_rank(comparison)==2
    assert certificate['comparison_determinant_margin']==F(4,9)
    assert certificate['young_alpha_margin']==F(2,75)
    controls=[]
    def reject(name,call):rejects(call);controls.append(name)
    reject('order_below_seven',lambda:perturbation_certificate(6,F(50,3)))
    reject('kappa_below_eight',lambda:perturbation_certificate(7,7))
    reject('insufficient_v13_kappa',lambda:perturbation_certificate(13,16))
    reject('indefinite_local_norm_form',lambda:principal_rank([[0,1,0],[1,0,0],[0,0,0]]))
    reject('indefinite_comparison_form',lambda:exact_psd_rank([[F(8),F(-12)],[F(-12),F(16)]]))
    return {'agent':'six-downset-2','role':'researcher','all_four_triple_subsets_tested':4845,
        'independent_six_point_Pasch_sides':30,'independent_six_point_trades':15,
        'free_inside_triples':12,'all_local_fills_and_orientations':assignments,
        'distinct_T_patterns':len(patterns),'local_transcript_sha256':local_transcript.hexdigest(),
        'all_integer_principal_minor_forms':1458,'local_norm_form_rank_histogram':{str(k):z for k,z in sorted(ranks.items())},
        'norm_form_transcript_sha256':norm_transcript.hexdigest(),
        'bounded_outside_sequence_checks':bounded,
        'unbounded_outside_bound_source':'Ordinary positive/negative-count proof in PASCH_DEFECT_STABILITY.md',
        'v13_rational_certificate':{k:str(z)for k,z in certificate.items()},
        'v13_comparison_matrix':[[str(z)for z in row]for row in comparison],
        'v13_comparison_Fraction_PSD_rank':2,'rejection_controls':controls}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected);out=run()
    expected=Path(__file__).with_name('pasch_local_expected.json')
    if args.check:assert out==json.loads(expected.read_text()),'Expected output mismatch'
    if args.write_expected:expected.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
