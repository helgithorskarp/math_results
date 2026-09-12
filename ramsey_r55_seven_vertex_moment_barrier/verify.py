"""Certify all inequalities and PSDs over integers."""
from pathlib import Path
import json,time,hashlib
import numpy as np
P=Path(__file__).resolve().parent

def positive_definite(matrix):
 a=[[int(x) for x in row] for row in matrix];n=len(a);assert all(a[i][j]==a[j][i] for i in range(n) for j in range(n));previous=1;leading=[]
 for k in range(n):
  pivot=a[k][k];assert pivot>0,('nonpositive leading principal minor',k,pivot);leading.append(pivot)
  for i in range(k+1,n):
   for j in range(i,n):
    num=pivot*a[i][j]-a[i][k]*a[k][j];v,rem=divmod(num,previous);assert rem==0,('inexact Bareiss division',k,i,j);a[i][j]=v;a[j][i]=v
  previous=pivot
 return {'dimension':n,'positive_leading_principal_minors':len(leading),'determinant_decimal_digits':len(str(leading[-1])),'leading_minors_sha256':hashlib.sha256(json.dumps(leading,separators=(',',':')).encode()).hexdigest()}

def arrays():
 z=np.load(P/'M10_sevendeck.npz');z2=np.load(P/'M10_integer_moments.npz');z3=np.load(P/'M10_full_squares.npz');A=np.concatenate([z['A'],z2['A']]);Q=[z[f'Q{i}'] for i in range(5)]+[z2[f'Q{i}'] for i in range(16)]+[z3[f'Q{i}'] for i in range(35)];return z['graphs'].tolist(),A,Q

def check(control):
 started=time.monotonic();graphs,A,Q=arrays();assert control['graphs']==graphs;nums=control['numerators'];D=control['denominator'];assert len(nums)==len(graphs) and all(isinstance(x,int) and x>0 for x in nums) and D==sum(nums)
 nv=np.array(nums,dtype=object);slacks=A.astype(object)@nv;assert all(int(x)>0 for x in slacks);matrices=[]
 for i,q in enumerate(Q):
  m=np.einsum('g,gij->ij',np.array(nums,dtype=np.int64),q) if max(nums)*len(nums)*int(np.max(abs(q)))<2**63 else np.tensordot(nv,q.astype(object),axes=(0,0))
  cert=positive_definite(m);cert['matrix_index']=i;matrices.append(cert);print('PD',i,'dimension',cert['dimension'],'seconds',time.monotonic()-started,flush=True)
 return {'status':'EXACT_STRICTLY_FEASIBLE','density_denominator':D,'positive_densities':len(nums),'strict_scalar_inequalities':len(slacks),'minimum_integer_scalar_slack':int(min(slacks)),'positive_definite_matrices':len(matrices),'positive_leading_principal_minors':sum(m['dimension'] for m in matrices),'matrices':matrices,'seconds':time.monotonic()-started,'claim':'The specified finite moment relaxation is strictly feasible. This is not a physical graph or a Ramsey exclusion.'}

if __name__=='__main__':
 control=json.loads((P/'exact_density.json').read_text());result=check(control);(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print('RESULT',result['status'],result['density_denominator'],result['positive_leading_principal_minors'],result['seconds'],flush=True)
