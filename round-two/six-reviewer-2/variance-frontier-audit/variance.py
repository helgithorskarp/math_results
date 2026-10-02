"""Independent whole row census and scalar closure; no author program/oracle.

Exact original table credited9145; unchanged own affine/linear primitives.
Weighted row moments are derived by membership and deleted-column action.
"""
from fractions import Fraction as F
from math import comb,isqrt
from linear import need,canonical,digest
from affine import table,parameters

def domain(q,k):
 need(type(q)is int and type(k)is int and q>=4 and 1<=k<=q,'full integer domain')
def boundary(k):
 need(type(k)is int and k>=1,'integer boundary')
 return (6*k-7+isqrt(28*k*k-36*k+17))//2

def rows(q,k):
 domain(q,k);w=F(3*q+1,q-1)-F(2,q*(q-1));beta=F(2*(q-1),q*(q-2))
 out=[['bc',5*q+6-k,F(1-k)],['a',1,1+2*k+F(2*k,q)],['az',k,(k-1)*(w-1)],['aw',q-k,1+k*(w-1)],['oz',k,F(k-1,q)],['ow',q-k,1+F(k,q)]]
 out += [['pair'+str(z),comb(k,z)*comb(q-k,2-z),1-z+(k-z)*beta]for z in range(3)]
 need(all(c>=0 for name,c,r in out),'nonnegative actual class counts')
 return out

def scalar(q,k):
 cc=rows(q,k);N=(q*q+13*q+16)//2-k;n=N-1;s=3*q+4;g=N-2*s
 ee=sum(c*r for name,c,r in cc);V=sum(c*r*r for name,c,r in cc);h0=V-ee*ee/n;m=ee-h0/g
 need(sum(c for name,c,r in cc)==n and ee==F(q*q+(13-6*k)*q+2*k*k-10*k+14,2),'complete counted census and e')
 pairvar=sum(c*d*(r-v)**2 for i,(name,c,r)in enumerate(cc)for name2,d,v in cc[i+1:])/n
 need(g>0 and h0==pairvar>=0,'exact variance identity and positive complement floor')
 rec={'q':q,'k':k,'N':N,'s':s,'g':g,'e':ee,'V':V,'h0':h0,'m':m,'b':boundary(k)}
 if m>0:
  mu=min(F(g,2),m/(n+2*h0/g**2));kap=min(F(1,8),mu/(4*(16*s+1)));old_t=kap/24
  new_t=F(k,4*(2*k+1))*kap
  need(mu>0 and 0<kap<=F(1,8) and 16*s*kap+2*old_t<mu/4,'original strict cap perturbation')
  need(16*s*kap+2*new_t<mu/4 and (4+F(2,k))*new_t/kap==F(1,2),'closed enlarged lower residual/cap')
  need(new_t/old_t==F(6*k,2*k+1),'enlargement ratio')
  rec.update({'mu':mu,'kappa':kap,'t':old_t,'new_t':new_t,'new_t_ratio':new_t/old_t})
 return rec

def assigned_row(A,q,k,Z):
 need(A!=0 and A.bit_count()<=3,'nonempty actual member')
 cls={name:r for name,c,r in rows(q,k)}
 if A&6:return cls['bc']
 core=A&7;outside=A>>3
 if core==1:
  if not outside:return cls['a']
  return cls['az'if A&Z else'aw']
 need(core==0,'remaining core class exhausted')
 if outside.bit_count()==1:return cls['oz'if A&Z else'ow']
 return cls['pair'+str((A&Z).bit_count())]

def constant_row(A,q,k,Z,kap,t):
 """Constant-size deleted action, including zero absent class counts."""
 Q=table(q,kap);a=(A&7).bit_count();z=(A&Z).bit_count();typ=(a,(A>>3).bit_count());h=F(1,3*q+5)
 r=F(1)if a==0 else h if a in [1,2]else-3*(q+1)*h
 deleted=-k if A&6 else -z+(k-z)*(Q[tuple(sorted((typ,(2,1))))]-1)
 repair_row=2 if A==1 else-1 if A in [3,5]else 0
 return kap*r-deleted+t*repair_row

def closure():
 cases=[];failed=[];hist=[]
 for k in range(5,19):
  start=boundary(k)-4;need(start>=max(4,k),'complete positive-domain lower bound')
  kk=[]
  for q in range(start,6*k):
   r=scalar(q,k);kk.append(q)
   if r['m']<=0:failed.append([q,k]);need([q,k]==[24,6],'unexpected failed sufficient estimate')
   cases.append(r)
  hist.append({'k':k,'first':start,'last':6*k-1,'count':len(kk)})
 need(len(cases)==192 and failed==[[24,6]],'complete192pair closure/one failed sufficient scalar')
 first=scalar(266,49);need(first['N']==37066 and first['m']==F(1508528528159230867,167560174190824800)>0,'whole first Pell scalar without domain allocation')
 pel=[];p,u=8,3
 for j in range(1,9):
  need(p*p-7*u*u==1,'Pell recurrence invariant')
  if j>=2:
   k=u+1;start=3*u+p-5;b=boundary(k);need(b==3*u+p,'strict Pell root floor')
   rr=[]
   for q in range(start,b+1):
    r=scalar(q,k);need(r['m']>0,'Pell finite calibrations of ordinary infinite proof');rr.append({field:r[field]for field in ['q','k','N','e','V','m']})
   pel.append({'index':j,'p':p,'u':u,'k':k,'orders':rr})
  p,u=8*p+21*u,3*p+8*u
 Q0=parameters(23,6)['Q0'];need(Q0==F(-91568355216,12536354677)<0,'owned all-real necessary q23 obstruction')
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','status':'PASS','cases':cases,'complete_case_ranges':hist,'failed_sufficient_estimate':failed,'first_Pell':first,'Pell_calibrations':pel,'six_deletion_q23_Q0':Q0,'whole_record_sha256':digest([cases,pel])}

if __name__=='__main__':
 import json,signal
 def alarm(*args):raise TimeoutError('fixed60s; incomplete is not nonexistence')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(60)
 print(json.dumps(canonical(closure()),sort_keys=True,separators=(',',':')))
