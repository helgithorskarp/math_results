"""Complete literal action and original matrix checks, including q4 boundary."""
from fractions import Fraction as F
from matrices import build,typ,ST,QT,delta
from systems import R,sector,DEGREES,read_r
from polynomials import forms,evaluate
from exact import require,schur_psd,polynomial_psd,lift,digest

def harmonic(x,j,ell):
 core=1 if j==0 else int(bool(x&2))-int(bool(x&4));w=x>>4
 outside=1 if ell==0 else int(bool(w&1))-int(bool(w&2)) if ell==1 else (int(bool(w&1))-int(bool(w&2)))*(int(bool(w&4))-int(bool(w&8)))
 return core*outside

def check(q,p,r,d):
 X,C,U,P,meta=build(q);n=len(X);s=3*q+4;Y=X[1:]
 literal_p=[[F(x) for x in meta[key]] for key in ['p','r','internal_d']]
 for field,literal in zip([p,r,d],literal_p):require([x.at(q-5) for x in field]==literal,'symbolic/literal potential equality')
 action_count=0;absent=0;dimensions=[];secondary=0
 for j,ell in DEGREES:
  copies=1 if ell==0 else q-2 if ell==1 else (q-1)*(q-4)//2
  if copies==0:absent+=1;continue
  block=sector(R(q),*[ [R(x) for x in values] for values in literal_p],j,ell)
  columns=[];norms=[]
  for star,types,weights in [(True,block['S_types'],block['S_norms']),(False,block['Q_types'],block['Q_norms'])]:
   for t,g in zip(types,weights):
    col=[harmonic(x,j,ell) if bool(x&1)==star and typ(x)==t else 0 for x in Y]
    require(sum(v*v for v in col)==g.at(0)*2**(j+ell),'literal lift norm')
    columns.append(col);norms.append(g.at(0))
  ns=len(block['S_types']);nq=len(block['Q_types']);H=[]
  for a in range(ns+nq):
   row=[]
   for b in range(ns+nq):
    if a<ns and b<ns:z=F(s*int(a==b))-(norms[b] if j==ell==0 else 0)
    elif a<ns:z=block['B_action'][a][b-ns].at(0)
    elif b<ns:z=block['BT_action'][a-ns][b].at(0)
    else:z=block['D_action'][a-ns][b-ns].at(0)
    row.append(z)
   H.append(row)
  for h,col in enumerate(columns):
   actual=[sum(row[b]*col[b] for b in range(n-1)) for row in C]
   predicted=[sum(columns[a][b]*H[a][h] for a in range(ns+nq)) for b in range(n-1)]
   require(actual==predicted,'literal original sector action');action_count+=1
  polynomial=forms(R((5,1)),p,r,d,(j,ell))
  for name in ['lower','upper']:
   G=[[x.at(0) for x in row] for row in block[name]]
   require(schur_psd(G)==nq-int(j==ell==0),'literal compressed floor rank')
   if q==4:
    require(polynomial_psd(G)[0]==nq-int(j==ell==0),'secondary characteristic floor rank');secondary+=1
   den=evaluate(polynomial[name+'_denominator'],q-5)
   require(den!=0,'nonzero literal clearing denominator')
   require(all(evaluate(polynomial[name][a][b],q-5)/den==G[a][b] for a in range(nq) for b in range(nq)),'polynomial/literal complete Schur identity')
  dimensions.append((ns+nq)*copies)
 require(sum(dimensions)==n-1,'complete dimension coverage')
 require(schur_psd([[C[i][j]-P[i][j]/4 for j in range(n-1)] for i in range(n-1)])==n-3,'whole lower quarter floor')
 require(schur_psd([[U[i][j]-F(i==j)/4 for j in range(n-1)] for i in range(n-1)])==n-1,'whole upper quarter floor')
 K=3*q*(q+1)*(q+2)//2;t=F(1,8*K);trade=delta(X,q)
 require(max(sum(abs(x) for x in row) for row in trade)<=K,'trade row-sum bound')
 Ct=[[C[i][j]+t*trade[i][j] for j in range(n-1)] for i in range(n-1)]
 Ut=[[U[i][j]-t*trade[i][j]-F(i==j)/8 for j in range(n-1)] for i in range(n-1)]
 require(schur_psd(Ct)==n-2 and schur_psd(Ut)==n-1,'repaired core rank/eighth gap')
 L=lift(Ct);V=[[F(n*int(i==j))-L[i][j] for j in range(n)] for i in range(n)]
 require(all(sum(row)==n for row in L),'original rows')
 require(all(L[i][j]==s*int(i==j) for i in range(n) for j in range(n) if X[i]&X[j]),'original support')
 star=[F(bool(x&1))-F(s,n) for x in X]
 require(all(sum(row[j]*star[j] for j in range(n))==0 for row in L),'original centered a-star')
 require(schur_psd(L)==n-1 and schur_psd(V)==n-1,'original repaired ranks')
 require(schur_psd([[V[i][j]-(F(i==j)-F(1,n))/8 for j in range(n)] for i in range(n)])==n-1,'original eighth gap')
 return {'q':q,'N':n,'s':s,'literal_action_columns':action_count,'absent_sectors':absent,'secondary_characteristic_forms':secondary,'sector_dimensions':dimensions,'t':str(t),'rank_L':n-1,'rank_upper':n-1,'upper_eighth_floor':True}
