"""Supplemental exact full-matrix inertia audit of the affine classification.

Actual agent six-reviewer-1, independent mathematical reviewer.
Imports only this review's partition constructor; no author code/fixture.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path
import audit


def signature(matrix):
    audit.need(all(len(r)==len(matrix) for r in matrix),'square inertia input')
    audit.need(all(matrix[i][j]==matrix[j][i] for i in range(len(matrix)) for j in range(len(matrix))),'symmetric inertia input')
    a=[[F(x) for x in r] for r in matrix];positive=negative=zero=0
    while a:
        pivot=next((i for i in range(len(a)) if a[i][i]),None)
        if pivot is not None:
            d=a[pivot][pivot];positive+=int(d>0);negative+=int(d<0)
            ix=[i for i in range(len(a)) if i!=pivot]
            a=[[a[i][j]-a[i][pivot]*a[pivot][j]/d for j in ix] for i in ix]
        else:
            pair=next(((i,j) for i in range(len(a)) for j in range(i+1,len(a)) if a[i][j]),None)
            if pair is None:zero+=len(a);break
            i,j=pair;d=a[i][j];ix=[k for k in range(len(a)) if k not in pair]
            a=[[a[k][l]-(a[k][i]*a[j][l]+a[k][j]*a[i][l])/d for l in ix] for k in ix]
            positive+=1;negative+=1
    return positive,negative,zero


def predicted(n,z):
    _,s,N,q,_=audit.counts(n)
    if n==4:
        positive=3+int(z<F(22,13))+3*int(z>F(4,3))
        zero=int(z==F(22,13))+3*int(z==F(4,3))
    else:
        positive=s+(n-1)*int(z>F(s,q+1));zero=(n-1)*int(z==F(s,q+1))
    return positive,N-positive-zero,zero


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',type=Path);args=parser.parse_args()
    controls=0
    for a,b,c,d,e,f in product((-1,0,1),repeat=6):
        m=[[a,b,c],[b,d,e],[c,e,f]];pos,neg,zero=signature(m)
        minors=[audit.determinant_permutations([[m[i][j] for j in ix] for i in ix]) for size in (1,2,3) for ix in combinations(range(3),size)]
        audit.need((neg==0)==all(v>=0 for v in minors),'inertia versus all PSD principal minors')
        audit.need((pos==0)==all((-1)**size*audit.determinant_permutations([[m[i][j] for j in ix] for i in ix])>=0 for size in (1,2,3) for ix in combinations(range(3),size)),'negative semidefinite principal minors')
        audit.need(pos+neg+zero==3 and (zero>0)==(audit.determinant_permutations(m)==0),'inertia determinant consistency')
        controls+=1
    audit.need(signature([[0,1],[1,0]])==(1,1,0),'offdiagonal pivot control')
    cases=[]
    for n,values in [(4,[F(0),F(1),F(15,13),F(4,3),F(3,2),F(22,13),F(2)]),
                     (5,[F(0),F(1),F(3,2),F(11,7),F(19,10),F(2)]),
                     (6,[F(1),F(26,15),F(2)])]:
        labels,pairs,C0,C1=audit.partition_matrices(n);p,s,N,q,t=audit.counts(n)
        for z in values:
            L=audit.lower(audit.core(n,z,labels,C0,C1));shift=[[L[i][j]-s*int(i==j) for j in range(N)] for i in range(N)]
            got=signature(shift);audit.need(got==predicted(n,z),'full literal M inertia')
            cases.append({'n':n,'z':str(z),'positive':got[0],'negative':got[1],'zero':got[2],'nonnegative':got[0]+got[2],'s':s})
    audit.need(F(97)*F(11,7)**2-1858*F(11,7)+3016==F(16455,49)>0,'n5 cap versus inertia threshold')
    rejects=0
    for matrix in [[[1,0]],[[0,1],[0,0]]]:
        try:signature(matrix)
        except ValueError:rejects+=1
    audit.need(rejects==2,'malformed inertia matrices reject')
    result={'agent':'six-reviewer-1','role':'independent mathematical reviewer','method':'Exact symmetric congruence with signed scalar and zero-diagonal two-by-two pivots','finite_cases':cases,'ternary_3x3_controls':controls,'offdiagonal_pivot_control':True,'malformed_rejections':rejects,'all_order_trust':'Written full spectrum and threshold proof, not extrapolation from these finite matrices.'}
    data=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.check:audit.need(args.check.read_text()==data,'complete inertia output comparison')
    print(data,end='')


if __name__=='__main__':main()
