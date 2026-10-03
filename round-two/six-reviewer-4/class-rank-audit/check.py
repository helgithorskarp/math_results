"""Independent decoder/Pascal-frame physical forms and determinant-polynomial test."""
import json,sys
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from exact import need,canon,digest,polynomial_psd,rref

def pascal(n):
 rows=[[1]]
 for a in range(n):rows.append([1]+[rows[-1][i-1]+rows[-1][i]for i in range(1,len(rows[-1]))]+[1])
 return rows

def rebuild(case):
 n=case['n'];r=n-2;s=2**(n-1)-n;P=pascal(n)
 def C(a,b):return P[a][b]if 0<=b<=a else 0
 active=case['active'];T=set(active+[n-a for a in active]+[n//2]);want=['d'+str(a)for a in active+[n//2]]
 want+=['t'+str(a)+'_'+str(b)for a in range(2,r+1)for b in range(a,r+1)if a+b<n and a in T and b in T]
 need(case['names']==want and len(want)==len(case['values']),'independent complete coordinate face');need(all(type(x)in(str,int,F)for x in case['values']),'independent rational only')
 vals={k:F(v)for k,v in zip(want,case['values'],strict=True)};B=[[F(0)]*r for _ in range(r)]
 for a in range(2,n//2+1):B[a-1][n-a-1]=B[n-a-1][a-1]=s-vals.get('d'+str(a),0)
 for k,v in vals.items():
  if k.startswith('t'):
   a,b=map(int,k[1:].split('_'));B[a-1][b-1]=B[b-1][a-1]=v
 for a in reversed(range(2,r+1)):
  B[0][a-1]=B[a-1][0]=((n-a)*s-sum(b*B[a-1][b-1]*C(n-a,b)for b in range(2,r+1)))/(n-a)
 B[0][0]=((n-1)*s-sum(b*B[0][b-1]*C(n-1,b)for b in range(2,r+1)))/(n-1)
 return B,P

def structure(case,B,P):
 n=case['n'];r=n-2;N=2**n-n-1;s=2**(n-1)-n
 def C(a,b):return P[a][b]if 0<=b<=a else 0
 E=[N-s-sum(C(n-a,b)*B[a-1][b-1]for b in range(1,r+1))for a in range(1,r+1)];loop=N-sum(C(n,a)*E[a-1]for a in range(1,r+1))
 need(loop+sum(C(n,a)*E[a-1]for a in range(1,r+1))==N,'independent empty row')
 for a in range(1,r+1):
  need(sum(C(n-a-1,b-1)*B[a-1][b-1]for b in range(1,r+1))==s,'independent excluding star')
  need(s+E[a-1]+sum(C(n-a,b)*B[a-1][b-1]for b in range(1,r+1))==N,'independent original row')
 need(sum(C(n-1,a-1)*E[a-1]for a in range(1,r+1))==s,'independent empty star')
 need(all(B[a-1][b-1]==B[b-1][a-1]for a in range(1,r+1)for b in range(1,r+1)),'independent symmetry')
 need(all(not B[a-1][b-1]for a in range(1,r+1)for b in range(1,r+1)if a+b>n),'unsupported disjoint orbit')
 for a in range(2,n//2+1):
  deficit=s-B[a-1][n-a-1];need(deficit>0 if a in case['active']or a==n//2 else deficit==0,'actual deficit profile')
 return dict(empty_loop=str(loop),empty_rows=list(map(str,E)),centered=all(x==1 for x in E))

def forms(n,B,P,j):
 """Frame: product of j paired-coordinate differences; layer norm and disjoint action."""
 s=2**(n-1)-n;N=2**n-n-1;r=n-2;layers=[a for a in range(1,r+1)if j<=a<=n-j]
 def C(a,b):return P[a][b]if 0<=b<=a else 0
 # One pair has squared norm2; divide the entire layer norm by2**j.
 g=[C(n-2*j,a-j)for a in layers];L=[];U=[]
 for a,ga in zip(layers,g,strict=True):
  l=[];u=[]
  # j forced opposite choices contribute (-1)**j; unpaired B choices are Pascal coefficients.
  for b in layers:
   interaction=(-1)**j*B[a-1][b-1]*C(n-2*j-(a-j),b-j)
   z=(s if a==b else 0)+interaction-(C(n,b)if j==0 else 0)
   l.append(ga*z);u.append(ga*((N if a==b else 0)-(C(n,b)if j==0 else 0)-z))
  L.append(l);U.append(u)
 return layers,g,L,U

def run(w,record):
 need(len(w['cases'])==2 and [c['n']for c in w['cases']]==[12,16],'exact two cases');need(len(record['cases'])==2,'record cases');out=[]
 for case,c in zip(w['cases'],record['cases'],strict=True):
  n=case['n'];need(c['n']==n and c['N']==2**n-n-1 and c['s']==2**(n-1)-n and c['h']==2**(n-1)-1 and c['active']==case['active']and c['coordinate_count']==len(case['names'])and c['floor']==str(F(case['floor'])),'all physical case parameters');B,P=rebuild(case);need(c['table']==[[str(x)for x in r]for r in B],'EVERY table coordinate');orig=structure(case,B,P);need(orig==c['original'],'EVERY original empty/row coordinate');eps=F(case['floor']);need(eps>0,'independent floor')
  need(len(c['parts'])==n//2+1 and [p['j']for p in c['parts']]==list(range(n//2+1)),'EVERY physical degree');parts=[];lr=0;ur=0;dim=0
  for j,p in enumerate(c['parts']):
   layers,g,L,U=forms(n,B,P,j);need(layers==p['layers']and g==p['g'],'full physical metric');need([[str(x)for x in r]for r in L]==p['lower']and [[str(x)for x in r]for r in U]==p['upper'],'EVERY physical form entry')
   known=[]
   if j==0:known.append(list(map(F,layers)))
   if j==1:known.append([F(1)]*len(layers))
   for a in range(2,n//2):
    if a in layers and B[a-1][n-a-1]==2**(n-1)-n:known.append([F((x==a)-(-1)**j*(x==n-a))for x in layers])
   need(p['kernels']==[[str(x)for x in z]for z in known],'EVERY forced kernel coordinate')
   need(all(not sum(L[i][k]*z[k]for k in range(len(g)))for z in known for i in range(len(g))),'literal full kernel')
   _,piv=rref(known);need(len(piv)==len(known),'known kernel dimension')
   rank,poly=polynomial_psd(L);u,upoly=polynomial_psd(U);keep=p['keep'];need(keep==[i for i in range(len(g))if i not in piv],'complete retained quotient');need(len(set(keep))==len(keep)and all(0<=i<len(g)for i in keep),'principal retained positions')
   A=[[L[i][k]-(eps*g[i]if i==k else 0)for k in keep]for i in keep];V=[[U[i][k]-(eps*g[i]if i==k else 0)for k in range(len(g))]for i in range(len(g))]
   ar,apoly=polynomial_psd(A);vr,vpoly=polynomial_psd(V);need(rank==p['lower_rank']==len(keep)and u==p['upper_rank']==len(g),'independent full rank');need(ar==len(keep)and vr==len(g),'independent physical floors')
   # No congruence pivot/kernel is used in the spectral PSD or rank decision.
   mult=P[n][j]-(P[n][j-1]if j else 0);need(mult==p['multiplicity'],'whole multiplicity');lr+=mult*rank;ur+=mult*u;dim+=mult*len(g)
   parts.append(dict(j=j,rank=rank,upper_rank=u,determinant_polynomial=poly,upper_polynomial=upoly,retained_floor_polynomial=apoly,upper_floor_polynomial=vpoly))
  need(dim==2**n-n-2,'complete original nonempty dimension');need(lr+1==c['lower_rank']and ur==c['upper_rank'],'independent weighted original ranks')
  q=sum(P[n][a]for a in range(2,n//2)if a not in case['active']);need(c['q']==q and c['gap']==str(eps/(2**(n-1)-1)),'physical q and gap');need(lr+1==2**n-n-1-n-q,'all-real rank ceiling attained')
  classes=list(range(2,n//2));census=[]
  for k in range(len(classes)+1):
   for absent in combinations(classes,k):
    qabs=sum(P[n][a]for a in absent);census.append(dict(absent=list(absent),population=qabs,rank_ceiling=2**n-n-1-n-qabs,count_possible=qabs<=(2**(n-1)-n)//(n-1)))
  minclasses=min(len(classes)-len(x['absent'])for x in census if x['count_possible']);need(minclasses==len(case['active']),'exact necessary minimum')
  maxrank=max(x['rank_ceiling']for x in census if len(x['absent'])==len(classes)-minclasses);profiles=[x['absent']for x in census if len(x['absent'])==len(classes)-minclasses and x['rank_ceiling']==maxrank];need(profiles==[[2]if n==12 else [2,3]],'unique equality saturation profile')
  out.append(dict(n=n,original=orig,full_spectrum=parts,all_absent_class_subsets=census,minimum_classes=minclasses,rank_ceiling=maxrank,unique_absent_profiles=profiles,rankL=lr+1,rankCap=ur))
 return dict(cases=out)
if __name__=='__main__':
 w=json.loads(Path(__file__).with_name('WITNESS.json').read_text());record=json.loads(Path(sys.argv[1]).read_text());v=run(w,record);Path(sys.argv[2]).write_bytes(canon(v));print(json.dumps({'complete':True,'bytes':len(canon(v)),'sha256':digest(v),'profiles':[(c['n'],c['unique_absent_profiles'])for c in v['cases']]}))
