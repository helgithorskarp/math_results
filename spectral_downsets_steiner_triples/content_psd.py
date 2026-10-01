"""Exact PSD/rank by positive-content-normalized integer Schur elimination.

Every step replaces A by (d*A_rest-u*u^T)/g, where d>0 is the pivot
and g>0 is the gcd of all nonzero residual entries. This is d/g times
the rational Schur complement. Positive scaling preserves PSD and rank;
the pivot contributes exactly one to rank. No division by an old pivot
or presumed Bareiss divisibility is used. A zero diagonal residual must
be identically zero for PSD. All arithmetic is standard-library exact.
Author: six-downset-2, researcher.
"""
from fractions import Fraction as F
from math import gcd, lcm


def content_psd_rank(Q, stats=None):
    n=len(Q)
    assert all(len(row)==n for row in Q)
    assert all(Q[i][j]==Q[j][i] for i in range(n) for j in range(n))
    scale=lcm(*(F(x).denominator for row in Q for x in row))
    A=[[int(F(x)*scale) for x in row] for row in Q]
    content=0
    for row in A:
        for z in row:
            if content!=1:content=gcd(content,z)
    if content>1:A=[[z//content for z in row] for row in A]
    info={'order':n,'rank':0,'positive_content_divisions':int(content>1),
          'peak_integer_bits':max((z.bit_length() for row in A for z in row),default=0)}
    rank=0
    while A:
        p=max(range(len(A)),key=lambda i:A[i][i]);d=A[p][p]
        if d<0:raise ValueError('negative diagonal in content-normalized residual')
        if d==0:
            if any(z for row in A for z in row):
                raise ValueError('nonzero content-normalized residual with zero diagonal')
            break
        pivot_row=A.pop(p);column=pivot_row[:p]+pivot_row[p+1:]
        for row in A:row.pop(p)
        content=0
        for i,row in enumerate(A):
            for j in range(i,len(A)):
                z=d*row[j]-column[i]*column[j]
                row[j]=z;A[j][i]=z
                if content!=1:content=gcd(content,z)
                info['peak_integer_bits']=max(info['peak_integer_bits'],z.bit_length())
        rank+=1
        if content==0:break
        if content>1:
            info['positive_content_divisions']+=1
            for row in A:
                for j,z in enumerate(row):
                    quotient,remainder=divmod(z,content)
                    assert remainder==0
                    row[j]=quotient
    info['rank']=rank
    if stats is not None:stats.update(info)
    return rank
