"""Original principal matrices and independent rational Schur classification."""
from fractions import Fraction as Q
import json
from original import vertices,parameters,need

def schur(A):
 B=[r[:] for r in A];rank=0
 while B:
  n=len(B);bad=next((i for i in range(n) if B[i][i]<0),None)
  if bad is not None:return False,rank
  pivot=max(range(n),key=lambda i:B[i][i])
  if B[pivot][pivot]==0:return not any(x for r in B for x in r),rank
  ids=[i for i in range(n) if i!=pivot];d=B[pivot][pivot]
  B=[[B[i][j]-B[i][pivot]*B[pivot][j]/d for j in ids] for i in ids];rank+=1
 return True,rank

def main():
 n=6;k=2;s,h,N,r,Z,T,K,G,c=parameters(n,k);full=2**n-1;V=[A for A in vertices(n) if A.bit_count()>k];pairs=sorted(A for A in V if k<A.bit_count()<n-k and A<full^A)
 cases=[]
 for label,base in [('strict',Q(1,3)),('odd_zero',Q(1,3)),('rank_one',Q(4*s,G+2)),('rank_negative',Q(5)),('noninvariant',Q(1,3)),('odd_negative',Q(1,3))]:
  d={A:base for A in pairs}
  if label=='odd_zero':d[pairs[0]]=Q(0)
  if label=='odd_negative':d[pairs[0]]=Q(-1,5)
  if label=='noninvariant':
   for i,A in enumerate(pairs):d[A]=Q(i+1,37)
  z={A:d[min(A,full^A)] for A in V if k<A.bit_count()<n-k}
  matrix=[[Q(s*int(A==B)-1)+(s-z[A] if A^B==full else 0) for B in V] for A in V]
  ok,rank=schur(matrix);gamma=sum(z[A]/(2*s-z[A]) for A in z);criterion=all(q>=0 for q in z.values()) and gamma<=2
  need(ok==criterion,'original complete principal criterion')
  if label=='strict' or label=='noninvariant':need(ok and rank==len(V),'whole positive definite')
  if label in ('odd_zero','rank_one'):need(ok and rank==len(V)-1,'exact boundary nullity')
  if label in ('rank_negative','odd_negative'):need(not ok,'negative energies detected')
  # For positive pair diagonals, direct weighted minimizer supplies rank-one failure.
  witness={A:Q(1,s) if A not in z else Q(1,2*s-z[A]) for A in V}
  qenergy=sum(witness[A]*matrix[i][j]*witness[B] for i,A in enumerate(V) for j,B in enumerate(V))
  if label=='rank_negative':need(qenergy<0,'literal negative rank-one witness')
  cases.append(dict(label=label,dimension=len(V),psd=ok,rank=rank if ok else None,gamma=str(gamma),rank_one_witness_energy=str(qenergy),pair_deficits=[str(d[A]) for A in pairs]))
 return dict(original_principal_cases=cases,full_matrix_positions=len(cases)*len(V)**2)
if __name__=='__main__':print(json.dumps(main(),sort_keys=True))
