"""Independent literal masks versus binomial fixed-space certificates.

New physical generator ONLY the two published q19/k5,q24/k6 singletons;
old owned affine.family4..23 allocation guard remains unchanged. No
researcher executable/record imported. All actual empty/lift rows kept.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from affine import table,repair,parameters,family
from linear import need,psd,canonical,digest
from variance import scalar,assigned_row,constant_row,rows

def singleton(q,k):
 need((q,k)in [(19,5),(24,6)],'new builder ONLY published original singleton cases')
 bits=list(range(q+3));Z=sum(1<<j for j in range(3,k+3))
 S=[0]+[1<<j for j in bits]+[(1<<i)|(1<<j)for i,j in combinations(bits,2)]+[7]
 for c in [3,5,6]:
  S += [c|(1<<j)for j in range(3,q+3)if c!=6 or not(Z>>j&1)]
 S=sorted(S);N=(q*q+13*q+16)//2-k
 need(len(S)==len(set(S))==N and S[0]==0,'complete actual singleton census')
 present=set(S)
 for A in S:
  need(A.bit_count()<=2 or(A.bit_count()==3 and(A&7).bit_count()>=2 and not(A&7==6 and A&Z)),'membership')
  for j in bits:
   if A>>j&1:need(A^(1<<j)in present,'whole downward closure')
 stars=[sum(bool(A&(1<<j))for A in S)for j in bits]
 need(stars==[3*q+4,3*q+4-k,3*q+4-k]+[q+5]*k+[q+6]*(q-k),'every star size')
 return S,Z,stars

def key(A,Z):return A&7,(A&Z).bit_count(),(A&~(Z|7)).bit_count()
def typ(A):return(A&7).bit_count(),(A>>3).bit_count()
def entry(A,B,s,Q,t):return(F(s-1)if A==B else F(-1)if A&B else Q[tuple(sorted((typ(A),typ(B))))]-1)+t*repair(A,B)
def choose(n,r):return comb(n,r)if 0<=r<=n else 0

def closed_gram(keys,weights,q,k,kap,t):
 Q=table(q,kap);s=3*q+4;G=[]
 for i,(mask,z,w)in enumerate(keys):
  row=[];ni=weights[i]
  for j,(mask2,r,v)in enumerate(keys):
   val=F(s*ni*(i==j)-ni*weights[j])
   count=0 if mask&mask2 else choose(k-z,r)*choose(q-k-w,v)
   if count:val+=ni*count*Q[tuple(sorted(((mask.bit_count(),z+w),(mask2.bit_count(),r+v))))]
   if z+w+r+v==0:val+=t*repair(mask,mask2)
   row.append(val)
  G.append(row)
 return G

def calibration(q,k):
 need((q,k)in [(5,3),(8,3)],'bounded baseline only')
 S,Z=family(q,k);non=S[1:];N=len(S);s=3*q+4;Q=table(q,0);action=[];counted={}
 for A in non:
  row=sum(entry(A,B,s,Q,F(0))for B in non);urow=N-(N-1)-row
  need(urow==assigned_row(A,q,k,Z),'each actual surviving row class')
  # Separate direct deleted-column incidence, without row-class formulas.
  removed=[6|(1<<j)for j in range(3,k+3)]
  deleted=sum(entry(A,B,s,Q,F(0))for B in removed)
  need(urow==1+deleted,'original row-deletion bridge')
  action.append(urow);counted[str(urow)]=counted.get(str(urow),0)+1
 rr=scalar(q,k);need(sum(action)==rr['e']and sum(v*v for v in action)==rr['V'],'whole physical moments')
 return {'q':q,'k':k,'N':N,'original_positions':len(non)**2,'complete_row_vector':action,'e':rr['e'],'V':rr['V'],'family_sha256':digest(S),'row_vector_sha256':digest(action)}

def point(q,k,new=False):
 S,Z,stars=singleton(q,k);non=S[1:];N=len(S);n=N-1;s=3*q+4
 if(q,k)==(24,6):kap,t=F(1,4096),F(5);lower,upper=F(1,2**30),F(1,2**20)
 else:
  rr=scalar(q,k);kap,t=rr['kappa'],rr['new_t'if new else't'];lower,upper=F(0),3*rr['mu']/4
 Q=table(q,kap);Qzero=table(q,0)
 keys=sorted(set(key(A,Z)for A in non));groups=[[i for i,A in enumerate(non)if key(A,Z)==wanted]for wanted in keys];weights=[len(g)for g in groups]
 need(len(keys)==23 and sum(weights)==n,'entire23 orbit census')
 need(weights==[comb(k,z)*comb(q-k,w)for mask,z,w in keys],'actual positive binomial norm weights')
 group_of={i:j for j,g in enumerate(groups)for i in g};G=[[F(0)]*23 for _ in keys];C=[];CzeroRows=[]
 for i,A in enumerate(non):
  row=[];c0=F(0)
  for j,B in enumerate(non):
   v=entry(A,B,s,Q,t);G[group_of[i]][group_of[j]]+=v;row.append(v);c0+=entry(A,B,s,Qzero,F(0))
  C.append(row);CzeroRows.append(c0)
  need(N-n-c0==assigned_row(A,q,k,Z),'whole q19/q24 zero row census')
  need(sum(row)==constant_row(A,q,k,Z,kap,t),'actual repaired constant-row/deleted incidence')
 need(G==closed_gram(keys,weights,q,k,kap,t),'every full original sum versus closed binomial Gram')
 representative=[[len(x)*sum(C[x[0]][j]for j in y)for y in groups]for x in groups]
 need(representative==G,'entire separate representative Gram')
 rowC=[sum(r)for r in C];star=[int(bool(A&1))for A in non]
 need(all(sum(c*a for c,a in zip(row,star))==0 for row in C),'every original star kernel row')
 vv=[weights[i]*(keys[i][0]&1!=0)for i in range(23)]
 HC=[[F(N*weights[i]*(i==j)-weights[i]*weights[j])-G[i][j]for j in range(23)]for i in range(23)]
 shiftedG=[[G[i][j]-lower*(weights[i]*(i==j)-F(vv[i]*vv[j],s))for j in range(23)]for i in range(23)]
 shiftedH=[[HC[i][j]-upper*weights[i]*(i==j)for j in range(23)]for i in range(23)]
 lower_certificate=psd(shiftedG);upper_certificate=psd(shiftedH)
 need(lower_certificate['rank']==22 and upper_certificate['rank']==23,'whole weighted floor/ranks; no omitted sector inference')
 need(all(weights[i]>0 for i in range(23))and sum(vv)==s,'weighted star projection')
 # Entire original whole lift and a second constant-size evaluator agree.
 kapH=F(1,3*q+5);alpha=F(q*(q+1),2)+3*(q+1)*kapH
 L00=1+sum(rowC);formula00=1+k*(s-k)+kap*(alpha-2*k*kapH)
 need(L00==formula00,'actual empty loop double sum')
 M=[];whole_star=[0]+star;cent=[F(v)-F(s,N)for v in whole_star]
 for i,A in enumerate(S):
  row=[]
  for j,B in enumerate(S):
   lift=L00 if i==j==0 else 1-rowC[j-1]if i==0 else 1-rowC[i-1]if j==0 else 1+C[i-1][j-1]
   literal=(lift-s*(i==j))/(N-s)
   independent_lift=formula00 if A==B==0 else 1-constant_row(B,q,k,Z,kap,t)if A==0 else 1-constant_row(A,q,k,Z,kap,t)if B==0 else 1+entry(A,B,s,Q,t)
   value=(independent_lift-s*(A==B))/(N-s);need(value==literal,'every whole original entry versus independent evaluator')
   need(not A&B or literal==0,'every support entry');row.append(literal)
  need(sum(row)==1,'every whole row sum')
  need(sum(((N-s)*v+s*(i==j))*cent[j]for j,v in enumerate(row))==0,'every actual centered star row')
  M.append(row)
 need(all(M[i][j]==M[j][i]for i in range(N)for j in range(N)),'whole symmetry')
 out={'q':q,'k':k,'repair_mode':'enlarged'if new else'original','N':N,'s':s,'kappa':kap,'t':t,'orbit_keys':keys,'norm_weights':weights,'whole_original_nonempty_positions':n*n,'closed_binomial_and_all_original_and_representative_equal':True,'whole_lower_Gram':G,'whole_upper_Gram':HC,'lower_floor':lower,'upper_floor':upper,'lower_certificate':lower_certificate,'upper_certificate':upper_certificate,'complement_dimension':n-23,'complement_lower_floor':kap/2,'complement_upper_floor':N-2*s,'whole_M_positions':N*N,'whole_M_sha256':digest(M),'all_star_sizes':stars,'actual_empty_M':M[0][0],'empty_L':L00,'whole_lower_rank':N-1,'whole_cap_rank':N-1,'zero_row_vector_sha256':digest(CzeroRows)}
 if(q,k)==(19,5):
  out['whole_lower_Gram_sha256']=digest(out.pop('whole_lower_Gram'));out['whole_upper_Gram_sha256']=digest(out.pop('whole_upper_Gram'))
 return out

if __name__=='__main__':
 import sys,json,signal
 def alarm(*args):raise TimeoutError('fixed60s physical phase; incomplete is not exclusion')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(60)
 if sys.argv[1]=='baseline':out=[calibration(5,3),calibration(8,3)]
 elif sys.argv[1]=='point':out=point(int(sys.argv[2]),int(sys.argv[3]),len(sys.argv)>4)
 else:raise ValueError('phase')
 print(json.dumps(canonical(out),sort_keys=True,separators=(',',':')))
