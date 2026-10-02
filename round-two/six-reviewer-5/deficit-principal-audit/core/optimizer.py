"""Independent necessary relaxation, full principal-lower constraint, exact certificates.
Float scouts select multipliers only; every acceptance is Fraction/integer arithmetic.
"""
from fractions import Fraction as Q
from math import comb
import json
from original import parameters,phi,need
BITS=160;UNIT=2**BITS;ROUND=2**96

def slope(n,a,z):
 s,h,N,r,*_=parameters(n,2);x=Q(2*a-n,2)
 return Q(n*n*r*r,4*(r+z)**2)-Q(N*N)*x*x/(N-z)**2
def gamma(s,z):return z/(2*s-z)
def gprime(s,z):return Q(2*s,(2*s-z)**2)
def ceil(x):return -((-x.numerator)//x.denominator)
def down(x):return Q((x*ROUND).numerator//(x*ROUND).denominator,ROUND)
def up(x):return Q(ceil(x*ROUND),ROUND)
def numeric_root(n,a,mu):
 s,h,N,r,Z,*_=parameters(n,2);x=a-n/2
 def d(z):return n*n*r*r/(4*(r+z)**2)-N*N*x*x/(N-z)**2-mu*(2*s/(2*s-z))**2
 if d(0)<=0:return 0.
 low=0.;high=float(Z)
 for _ in range(110):
  z=(low+high)/2
  if d(z)>0:low=z
  else:high=z
 return (low+high)/2
def scout(n,k):
 s,h,N,r,Z,T,K,G,c=parameters(n,k);lo=0.;hi=n*n/4
 for _ in range(65):
  mu=(lo+hi)/2;mass=0.
  for a in range(k+1,n-k):
   z=numeric_root(n,a,mu);mass+=comb(n,a)*z/(2*s-z)
  if mass>2:lo=mu
  else:hi=mu
 return Q(round(((lo+hi)/2)*2**40),2**40)
def certificate(n,k):
 s,h,N,r,Z,T,K,G,c=parameters(n,k);m=scout(n,k);mu=2*s*m;need(mu>0,'positive full-principal multiplier')
 roots={};upper=Q(c)+2*mu
 for a in range(k+1,(n//2)+1):
  p0=slope(n,a,Q(0))-m
  if p0<=0:lo=hi=Q(0);idx=0
  else:
   low=0;high=UNIT
   for _ in range(BITS):
    j=(low+high)//2;z=Q(Z*j,UNIT);d=slope(n,a,z)-mu*gprime(s,z)
    if d>0:low=j
    else:high=j
   need(high-low==1,'whole bracket');idx=low;lo=Q(Z*low,UNIT);hi=Q(Z*high,UNIT)
   need(slope(n,a,lo)-mu*gprime(s,lo)>=0 and slope(n,a,hi)-mu*gprime(s,hi)<=0,'exact derivative root signs')
  weight=comb(n,a)*(1 if 2*a==n else 2)
  derivative=slope(n,a,hi)-mu*gprime(s,hi)
  need(derivative<=0,'supporting tangent orientation')
  upper+=up(weight*(phi(n,a,hi)-mu*gamma(s,hi)-derivative*(hi-lo)))
  roots[a]=(lo,hi,idx,p0<=0)
 # Positive partial schedule, ensuring all odd modes and the rank-one mode strict.
 xi=Q(1,2**100);proposal={a:z[0]+xi for a,z in roots.items()}
 gamup=sum(up(comb(n,a)*(1 if 2*a==n else 2)*gamma(s,z)) for a,z in proposal.items())
 target=Q(2)-Q(1,2**40);theta=min(Q(1),target/gamup)
 feasible={a:theta*z for a,z in proposal.items()};gupper=sum(up(comb(n,a)*(1 if 2*a==n else 2)*gamma(s,z)) for a,z in feasible.items())
 lower=c+sum(down(comb(n,a)*(1 if 2*a==n else 2)*phi(n,a,z)) for a,z in feasible.items())
 need(gupper<2 and all(0<z<Z for z in feasible.values()),'strict complete free-lower schedule')
 budget=Q(4*s*G,G+2);need(budget<T,'strictly reduced deficit budget')
 return dict(n=n,k=k,normalized_mu=str(m),mu=str(mu),root_bits=BITS,brackets=[dict(a=a,lower_index=str(z[2]),inactive=z[3]) for a,z in roots.items()],upper=str(upper),lower=str(lower),theta=str(theta),schedule_floor=str(xi),gamma_upper=str(gupper),linear_budget=str(budget),old_budget=str(T),principal_schedule_positive=lower>0)
def main():
 records=[]
 for n,k in [(24,6),(32,8),(40,11),(48,14),(64,19),(96,31)]:
  negative=certificate(n,k-1);positive=certificate(n,k)
  need(Q(negative['upper'])<0 and Q(positive['lower'])>0,'full-principal six exact signed cutoffs')
  records.extend([negative,positive])
 return dict(full_principal_certificates=records,root_bits=BITS,round_grid=str(ROUND),float_acceptance=False)
if __name__=='__main__':print(json.dumps(main(),sort_keys=True))
