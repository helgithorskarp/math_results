"""Independent exact controls for content-normalized Schur PSD/rank.

729 symmetric ternary 3-by-3 matrices are compared to *all* principal
minors, computed by recursive determinants, and Fraction Schur. Also
checks positive rational scaling, singular rank, shape and symmetry.
This finite audit validates an implementation; the congruence argument
in content_psd.py supplies its general mathematical soundness.
"""
from fractions import Fraction as F
from itertools import combinations,product
import json
from content_psd import content_psd_rank
from verify import exact_psd_rank,rejects


def determinant(A):
    if not A:return F(1)
    return sum((-1)**j*A[0][j]*determinant([row[:j]+row[j+1:] for row in A[1:]])
               for j in range(len(A)))


def principal_minor_rank(A):
    largest=0
    for k in range(1,len(A)+1):
        for subset in combinations(range(len(A)),k):
            d=determinant([[A[i][j] for j in subset] for i in subset])
            if d<0:return None
            if d>0:largest=k
    return largest


def run():
    accepted=rejected=0
    for entries in product((-1,0,1),repeat=6):
        a,b,c,d,e,f=map(F,entries);A=[[a,b,c],[b,d,e],[c,e,f]]
        rank=principal_minor_rank(A)
        if rank is None:
            rejects(lambda:content_psd_rank(A));rejects(lambda:exact_psd_rank(A));rejected+=1
        else:
            assert content_psd_rank(A)==exact_psd_rank(A)==rank;accepted+=1
            scaled=[[F(37,101)*z for z in row] for row in A]
            assert content_psd_rank(scaled)==rank
    assert accepted+rejected==729
    assert content_psd_rank([])==0
    assert content_psd_rank([[F(0)]])==0
    assert content_psd_rank([[F(7,23)]])==1
    rejects(lambda:content_psd_rank([[1,2],[0,1]]))
    rejects(lambda:content_psd_rank([[1,2],[2]]))
    return {'agent':'six-downset-2','role':'researcher','all_symmetric_ternary_3x3':729,
        'PSD_cases':accepted,'non_PSD_cases':rejected,
        'independent_oracles':['all principal minors, recursive exact determinant','Fraction Schur'],
        'rational_rescaling_cases':accepted,'extra_controls':5}


if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
