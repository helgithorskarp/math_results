"""Credited exact Gaussian solve function, copied from own9778/9751.
No independent peer reconstruction is claimed.
"""
from fractions import Fraction as F
from exact import require

def solve(A,b):
    A=[list(map(F,row))+[F(z)] for row,z in zip(A,b)];length=len(A)
    for j in range(length):
        i=next((i for i in range(j,length) if A[i][j]),None)
        require(i is not None,'invertible deleted residual')
        A[j],A[i]=A[i],A[j];z=A[j][j];A[j]=[x/z for x in A[j]]
        for i in range(length):
            if i!=j:
                z=A[i][j];A[i]=[x-z*y for x,y in zip(A[i],A[j])]
    return [row[-1] for row in A]
