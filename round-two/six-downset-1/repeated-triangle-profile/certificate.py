"""Exact characteristic-zero scalar/Sylvester certificate for realq>=4.
Uniformity and original-space interpretation are written in PROOF.md.
"""
import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[name]='1'
from pathlib import Path
from fractions import Fraction as F
import sys,json,signal,time,resource
from bivariate import P,R,ATOMS,PROBES,DEN_CACHE,atom,denominator
from clearing import shift,encode,clear_original
from exact import require,gram,zero,unit,scale,vecadd
from model import construct,blocks


def leading_polynomial_minors(matrix):
 a=[row[:] for row in matrix];last=P(1);out=[]
 for k in range(len(a)):
  pivot=a[k][k];require(bool(pivot),'nonzero original-field leading pivot');out.append(pivot)
  for i in range(k+1,len(a)):
   for j in range(k+1,len(a)):
    num=pivot*a[i][j]-a[i][k]*a[k][j];quot=num.exact_div(last)
    require(quot is not None,'EVERY fraction-free Bareiss division exact');a[i][j]=quot
  last=pivot
 return out


def generate():
 ATOMS.clear();PROBES.clear();DEN_CACHE.clear();q=R(P({(0,1):1}))
 for z in [q,q-1,q+2,q+3,q+6]:atom(z.num)
 p,G,S,cap,vec=construct(q,'mean',F(0),F(-2,5),fraction=R)
 matrices,ids=blocks(G,S,cap,vec);rows=[];original_forms={}
 from exact import dot,matvec
 V,U=vec['V'],vec['U'];vi=[matvec(G,z) for z in V];ui=[matvec(G,z) for z in U];field=0
 for z,img in zip(V+U,vi+ui):require(dot(z,img)==p['w'],'EVERY original nonempty norm field identity');field+=1
 for i in range(9):
  for j in range(9):
   if (i<6 and j<6) or (i>=6 and j>=6):require(dot(V[i],vi[j])==p['s']*(i==j)-1,'ALL same-mark clique field positions');field+=1
   if i//3==j//3 and ((1,2,3)[i%3] & (1,2,3)[j%3]):require(dot(U[i],vi[j])==-1,'ALL mandatory private/marked field positions');field+=1
   if i!=j and i//3==j//3 and ((1,2,3)[i%3] & (1,2,3)[j%3]):require(dot(U[i],ui[j])==-1,'ALL mandatory private/private field positions');field+=1
 require(dot(vec['K'],matvec(G,vec['K']))==10*q-4 and dot(vec['E'],matvec(G,vec['E']))==p['E2'] and dot(vec['K'],matvec(G,vec['E']))==0,'ALL fixed projection normalizations');field+=3
 require(field==99,'all99 definition-level original field positions')
 ids['original_field_positions']=field
 catalogue=[(name,[[p[name]]]) for name in ['alphaH','betaH','alphaL','betaL','nu','muL']]+list(matrices.items())
 for group,matrix in catalogue:
  raw=[[R(z) for z in row] for row in matrix]
  cleared,domains,removed,constants=clear_original(raw)
  original_forms[group]={'raw_original':[[{'numerator':encode(z.num),'denominator_factors':[{'factor':encode(ATOMS[key]),'power':power} for key,power in z.den.items()]} for z in row] for row in raw], 'cleared':[[encode(z) for z in row] for row in cleared], 'domains':domains,'removed':removed,'constants':constants}

  # Bind EVERY cleared original entry, including all sign and positive scaling factors.
  for i,row in enumerate(cleared):
   domain=P(1);rem=P(1)
   for f in domains[i]:domain=domain*P.decode([(z[0],F(int(z[1]),f['original']['denominator'])) for z in f['original']['terms']])**f['power']
   for f in removed[i]:rem=rem*P.decode([(z[0],F(int(z[1]),f['original']['denominator'])) for z in f['original']['terms']])**f['power']
   for j,z in enumerate(row):require(R(z)*rem==raw[i][j]*domain*F(constants[i]),'EVERY whole row-clearing original entry identity')
  determinants=leading_polynomial_minors(cleared)
  for k,det in enumerate(determinants,1):
   shifted=shift(det);positive=shifted.positive()
   row={'group':group,'order':k,'original':encode(det),'shifted':encode(shifted),'cleared_original_matrix':[[encode(z) for z in v[:k]] for v in cleared[:k]],'positive_row_domains':domains[:k],'positive_removed_row_factors':removed[:k],'positive_row_constants':constants[:k],
        'positive':positive,'degree':det.degree(),'coefficients':len(shifted.a)}
   rows.append(row)
   require(positive,'whole positive shifted leading sign '+group+'/'+str(k))

 return {'agent':'six-downset-1','role':'researcher','status':'exact generated signs; separate checking and original bridge required','domain':'realq>=4,q4+v,v>=0','rows':rows,'identities':ids,'forms':original_forms}
