"""Source-only fraction-free polynomial determinant and adjugate solve.

This generator uses no saved solve or symbolic algebra package. Every
division is exact in Z[q,k] and multiplied back. The verifier separately
checks all original solve equations and a complete determinant grid.
"""
import ipoly as p


def seven(G):
    if len(G)!=11 or any(len(row)!=11 for row in G):
        raise ValueError('complete original eleven-family shape required')
    integral=[]
    for row in G:
        values=[]
        for poly in row:
            if any(value.denominator!=1 for value in poly.values()):
                raise ValueError('complete original Gram must be integral')
            values.append({power:int(value) for power,value in poly.items()})
        integral.append(values)
    R=list(range(3,10));T=[0,1,2,10];n,r=7,4
    B=[[integral[i][j] for j in R] for i in R]
    X=[[integral[i][j] for j in T] for i in R]
    work=[[dict(v) for v in row+cross] for row,cross in zip(B,X)]
    previous={(0,0):1}
    for j in range(n-1):
        pivot=work[j][j]
        if not pivot:raise ValueError('zero leading polynomial pivot')
        for i in range(j+1,n):
            factor=work[i][j]
            for c in range(j+1,n+r):
                work[i][c]=p.divide(p.add(p.mul(pivot,work[i][c]),
                                         p.scale(p.mul(factor,work[j][c]),-1)),previous)
            work[i][j]={}
        previous=pivot
    determinant=work[n-1][n-1]
    if not determinant:raise ValueError('zero original seven determinant')
    Y=[[{} for _ in range(r)] for _ in range(n)]
    for i in range(n-1,-1,-1):
        for c in range(r):
            residual=p.add(p.mul(determinant,work[i][n+c]),
                           *(p.scale(p.mul(work[i][j],Y[j][c]),-1)
                             for j in range(i+1,n)))
            Y[i][c]=p.divide(residual,work[i][i])
    H=[[p.add(p.mul(determinant,integral[T[i]][T[j]]),
              *(p.scale(p.mul(X[t][i],Y[t][j]),-1) for t in range(n)))
         for j in range(r)] for i in range(r)]
    return determinant,Y,H
