"""Complete cyclic13 point budgets by tuple incidences and integer minors.

All3372 fixed-shift designs: independent generating-function counts,
literal tuple pair degrees/link intersections, all point entries and
unit-permutation congruences. Positive leading minors certify157 distinct
12x12 point forms, independently of the constructor's integer Schur method.
Negative principal minors prove only the least COMMON INTEGER point budget.
No full isomorphism census or dense slack elimination. Author-side check,
not a reviewer verdict. six-downset-2, researcher; assertions enabled.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from cyclic13_gram import balanced_masks,blocks_from_mask
from cyclic13_spectral import cohort_parameters,initial_point_certificate,comparison_data
from pasch_defect import point_defect
from verify_defect_gram import independent_signatures,independent_count
from verify import rejects


def determinant(matrix):
    """Integer Bareiss determinant, with exact row swaps and divisibility.

    This is a determinant calculation, not a PSD elimination. Sylvester's
    criterion is applied to independently selected leading principal forms.
    """
    n=len(matrix);assert all(len(row)==n for row in matrix)
    assert all(type(z)is int for row in matrix for z in row)
    if n==0:return 1
    A=[row[:]for row in matrix];old=1;sign=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n)if A[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:A[k],A[pivot]=A[pivot],A[k];sign=-sign
        d=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                q,r=divmod(d*A[i][j]-A[i][k]*A[k][j],old)
                assert r==0,'Bareiss divisibility failed'
                A[i][j]=q
        for i in range(k+1,n):A[i][k]=0
        old=d
    return sign*A[-1][-1]


def leading_minors(matrix):
    assert all(matrix[i][j]==matrix[j][i]for i in range(len(matrix))for j in range(len(matrix)))
    return [determinant([row[:k]for row in matrix[:k]])for k in range(1,len(matrix)+1)]


def tuple_defect(lam,blocks):
    assert len(blocks)==len(set(blocks))==26*lam
    triples=[]
    for a in blocks:
        assert type(a)is int and 0<a<1<<13 and a.bit_count()==3
        triples.append(tuple(x for x in range(13)if a>>x&1))
    degree=Counter(p for t in triples for p in combinations(t,2))
    assert len(degree)==78 and set(degree.values())=={lam}
    links=[{tuple(y for y in t if y!=x)for t in triples if x in t}for x in range(13)]
    assert all(len(link)==6*lam for link in links)
    u=lam*(lam-1)//2
    Z=[[0 if x==y else len(links[x]&links[y])-u for y in range(13)]for x in range(13)]
    assert all(sum(row)==0 for row in Z)
    assert all(Z[x][y]==Z[y][x]for x in range(13)for y in range(13))
    return Z


def point_form(row,gamma):
    assert len(row)==13 and type(gamma)is int and gamma>=0
    assert row[0]==sum(row)==0 and all(row[j]==row[(-j)%13]for j in range(13))
    return [[gamma*(13*int(x==y)-1)-13*row[(y-x)%13]for y in range(13)]for x in range(13)]


def reduced_point_form(row,gamma):
    full=point_form(row,gamma)
    assert all(sum(line)==0 for line in full)
    return [line[1:]for line in full[1:]]


def run():
    orbit,sig,families=balanced_masks();independent=independent_signatures()
    out={'agent':'six-downset-2','role':'researcher','v':13,'cohorts':{},
        'triple_orbits':22,'pair_orbits':6,'simple_fixed_shift_subset_space':1<<22,
        'whole_dense_Schur_forms':0}
    checked={};positive_transcript=sha256();all_rows={};total=0
    common_counts={4:762,5:1305,6:1305};pattern_counts={4:(335,59),5:(575,98),6:(575,98)}
    for lam,gamma,h,bound,witness in cohort_parameters():
        count,states=independent_count(lam,independent)
        assert len(families[lam])==len(set(families[lam]))==count==common_counts[lam]
        rows={};classes={};digest=sha256();all_rows[lam]={}
        for mask in families[lam]:
            blocks=blocks_from_mask(mask,orbit);Z=tuple_defect(lam,blocks)
            assert Z==point_defect(13,lam,blocks)[2]
            row=tuple(Z[0]);all_rows[lam][mask]=row
            assert all(Z[x][y]==row[(y-x)%13]for x in range(13)for y in range(13))
            rows.setdefault(row,mask)
            transforms=[(tuple(row[(k*j)%13]for j in range(13)),k)for k in range(1,13)]
            canonical,k=min(transforms)
            assert canonical==min(r for r,_ in transforms[:6])
            assert all(canonical[(y-x)%13]==Z[(k*x)%13][(k*y)%13]
                       for x in range(13)for y in range(13))
            classes.setdefault(canonical,mask)
            digest.update(json.dumps([mask,row],separators=(',',':')).encode()+b'\n')
        assert (len(rows),len(classes))==pattern_counts[lam]
        constructor_forms=0
        for row,mask in sorted(classes.items()):
            key=(gamma,row)
            if key not in checked:
                minors=leading_minors(reduced_point_form(row,gamma))
                assert len(minors)==12 and min(minors)>0
                checked[key]=minors
                positive_transcript.update(json.dumps([gamma,row,minors],separators=(',',':')).encode()+b'\n')
            actual,info=initial_point_certificate(13,lam,blocks_from_mask(mask,orbit),gamma)
            assert info['rank']==12 and tuple(actual[0])==all_rows[lam][mask]
            constructor_forms+=1
        badrow=all_rows[lam][witness];bad=reduced_point_form(badrow,gamma-1)
        minors=leading_minors(bad);negative=next((i for i,d in enumerate(minors)if d<0),None)
        assert negative is not None,'Need an explicit negative principal minor for the integer lower witness'
        controls={'initial_mask':witness,'gamma':gamma-1,'point_row':list(badrow),
            'principal_points':list(range(1,negative+2)),'negative_determinant':minors[negative]}
        rejects(lambda:initial_point_certificate(13,lam,blocks_from_mask(witness,orbit),gamma-1))
        caps=[]
        for moves in range(h+1):
            data=comparison_data(13,lam,F(gamma)+moves*F(50,3),bound)
            # Direct rational Sylvester minors, distinct from constructor Schur arithmetic.
            M=data['comparison'];p=M[0][0]
            q=p*M[1][1]-M[0][1]*M[1][0]
            d=(M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
               -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
               +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
            assert min(p,q,d)>0 and data['comparison_rank']==3
            caps.append({'moves':moves,'gamma':str(data['gamma']),
                'G':[[str(z)for z in row]for row in data['G']],
                'comparison_leading_minors':[str(z)for z in (p,q,d)],
                'B':str(data['B']),'delta':str(data['delta']),
                'half_gap_margin':str(data['half_gap_margin']),
                'old_row_criterion_sufficient':data['row_criterion_sufficient']})
        out['cohorts'][str(lam)]={'fixed_shift_labelled_designs':count,
            'independent_DP_max_states':states,'ordered_circulant_point_rows':len(rows),
            'unit_point_row_classes':len(classes),'mean_point_budget':gamma,
            'least_COMMON_INTEGER_budget_witness':controls,
            'author_constructor_point_forms':constructor_forms,
            'complete_point_transcript_sha256':digest.hexdigest(),'all_shorter_path_comparisons':caps}
        total+=count
    # The complete-triple complement identity Z_l=Z_(11-l) is credited to8260.
    full=(1<<22)-1
    assert {full^mask for mask in families[5]}==set(families[6])
    assert all(all_rows[5][mask]==all_rows[6][full^mask]for mask in families[5])
    assert len(checked)==157 and total==3372
    # Determinant controls include a pivot exchange and a singular principal form.
    assert determinant([[0,1],[1,0]])==-1
    assert determinant([[1,1],[1,1]])==0
    assert leading_minors([[2,-1],[-1,2]])==[2,3]
    rejects(lambda:tuple_defect(4,blocks_from_mask(23768,orbit)[:-1]))
    rejects(lambda:comparison_data(13,4,F(160,3),0))
    out.update(complete_designs_checked=total,direct_point_entries_checked=169*total,
        direct_tuple_link_intersections_checked=156*total,pair_degrees_checked=78*total,
        unit_congruence_entries_checked=169*total,constructor_entry_comparisons=169*total,
        distinct_positive_12x12_point_forms=len(checked),positive_integer_leading_minors=12*len(checked),
        positive_minor_transcript_sha256=positive_transcript.hexdigest(),
        constructor_13x13_point_forms=sum(c['author_constructor_point_forms']for c in out['cohorts'].values()),
        complement_mask_pairs_checked=1305,complement_point_entries_transferred=169*1305,
        joint_3x3_comparisons=sum(len(c['all_shorter_path_comparisons'])for c in out['cohorts'].values()),
        joint_positive_leading_minors=3*sum(len(c['all_shorter_path_comparisons'])for c in out['cohorts'].values()),
        budget_negative_principal_minors=3,rejection_controls=5,determinant_controls=3,
        trust_boundary='Complete exact fixed-shift coverage, entry checks, unit congruence and Sylvester point/comparison forms. Ordinary zero-row-sum and full-mode bridges are written in CYCLIC13_SPECTRAL_CAP.md; no isomorphism census, whole slack elimination, real-optimal point budget or general H/I resolution.')
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected);out=run()
    expected=Path(__file__).with_name('cyclic13_spectral_expected.json')
    if args.check:assert out==json.loads(expected.read_text()),'Expected output mismatch'
    if args.write_expected:expected.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
