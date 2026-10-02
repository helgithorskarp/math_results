"""Post-seal exact diagnostic for the sole additional local alias without angles.
This is an identically-zero obstruction diagnostic, not a geometric realization.
"""
import json
from algebra import dotN,L,B,D,R,ZERO,add,sub,mul,power,scale,determinant
A=dotN(L[1],L[10]);BB=dotN(L[1],L[12]);k=dotN(B[6],B[7]);DD=power(D,2)
P=sub(DD,power(A,2));Q=sub(DD,power(BB,2));U=sub(mul(R,D),mul(A,BB));N=sub(DD,power(k,2));V=sub(mul(k,D),power(k,2));W=sub(mul(R,D),mul(BB,k));Z=sub(mul(R,D),mul(A,k))
f=[Q,scale(mul(U,W),-2),sub(add(mul(P,power(W,2)),mul(N,power(U,2))),mul(mul(P,Q),N))]
g=[N,scale(mul(V,Z),-2),sub(add(mul(N,power(Z,2)),mul(P,power(V,2))),mul(P,power(N,2)))]
F=determinant([f+[ZERO],[ZERO]+f,g+[ZERO],[ZERO]+g])
if F!=(0,):raise ValueError('additional alias resultant not identically zero')
print(json.dumps({'additional_local_alias':[[0,12],[6,1]],'projected_resultant_full_coefficients':list(F),'geometric_realization_claimed':False},sort_keys=True))
