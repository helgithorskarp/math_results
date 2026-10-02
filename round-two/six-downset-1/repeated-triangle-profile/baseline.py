"""Exact useful9361 baseline replay and uniform limitation of that seed.

The defining closure9361.py is byte-identical credited prior source.
This check is validation, not a new ordinary H existence result.
"""
from fractions import Fraction as F
from closure9361 import construct,cube
from exact import require,psd_rank

def replay(n):
 family,C,M,old=construct(n,[(0,cube(2)),(0,cube(2)),(1,cube(2))]);N=old['N'];q=old['q'];s=old['s'];B=sum(map(sum,C))
 require(B==19*q-55+F(288,q),'whole original baseline empty formula')
 energy=N*N*((N-1)-B)
 require(energy<0,'original empty-centered negative cap quadratic')
 require(17*q*q-72*q+288==17*(F(q)-F(36,17))**2+F(3600,17),'exact complete-square uniform numerator')
 try:psd_rank([[F(i==j)-M[i][j] for j in range(N)] for i in range(N)])
 except ValueError:pass
 else:raise ValueError('ordinary baseline unexpectedly capped')
 return {k:old[k] for k in ['n','q','N','s','core_rank','lower_rank','core_sha256','matrix_sha256','ordered_core_positions']}|{'empty_energy':str(B),'negative_whole_cap_energy':str(energy)}
