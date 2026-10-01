"""Exact PSD/rank by integer Bareiss, credited to published uniform code.

The independent rational Schur checker in verify.py cross-checks these
small harmonic blocks. No float, solver or assertion is a proof check.
"""
from fractions import Fraction as Q
from math import lcm
from matrices import require


def psd_rank(A):
    d=len(A)
    require(all(len(row)==d for row in A),"PSD shape")
    require(all(type(v) in (int,Q) for row in A for v in row),"Exact PSD input")
    require(all(A[i][j]==A[j][i] for i in range(d) for j in range(d)),"PSD symmetry")
    if not d:return 0
    den=lcm(*(Q(v).denominator for row in A for v in row))
    z=[[int(Q(v)*den) for v in row] for row in A];previous=1;rank=0
    for k in range(d):
        require(all(z[i][i]>=0 for i in range(k,d)),"Negative Schur diagonal")
        i=next((i for i in range(k,d) if z[i][i]>0),None)
        if i is None:
            require(all(z[i][j]==0 for i in range(k,d) for j in range(k,d)),"Nonzero zero-diagonal residual")
            break
        if i!=k:
            z[k],z[i]=z[i],z[k]
            for row in z:row[k],row[i]=row[i],row[k]
        pivot=z[k][k]
        for i in range(k+1,d):
            for j in range(i,d):
                value=pivot*z[i][j]-z[i][k]*z[k][j]
                require(value%previous==0,"Integer elimination divisibility")
                z[i][j]=z[j][i]=value//previous
        previous=pivot;rank+=1
    return rank
