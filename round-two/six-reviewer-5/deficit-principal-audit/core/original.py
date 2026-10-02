"""Definition-level actual coordinates, sparse signed entries, exposed kernel defect."""
from fractions import Fraction as Q
from math import comb
import json

def need(p,label):
 if not p:raise ValueError(label)
def parameters(n,k):
 s=2**(n-1)-n;h=2**(n-1)-1;N=s+h;r=n-1;Z=2*s-2;T=2*Z
 K=sum(comb(n,a) for a in range(2,k+1));G=Z-2*K
 c=n*h-n*r*s+(Q(h)-Q(s*s,h))*sum(a*a*comb(n,a) for a in range(2,k+1))
 return s,h,N,r,Z,T,K,G,c
def phi(n,a,z):
 s,h,N,r,*_=parameters(n,2);x=Q(2*a-n,2)
 return Q(n*n*r)*z/(4*(r+z))-N*x*x*z/(N-z)
def vertices(n):return [x for x in range(1,2**n) if x.bit_count()<=n-2]
def entries(n,free=False,trade=False):
 s,h,N,r,*_=parameters(n,2);V=vertices(n);full=2**n-1;edges={}
 for ii,A in enumerate(V):
  a=A.bit_count()
  for B in V[ii+1:]:
   if A&B:continue
   b=B.bit_count();v=Q(0)
   if free:v=Q(((A*17+B*11)%29)-14,7)
   elif a==b==1:v=s-(2**(n-2)-2)
   elif min(a,b)==1:v=1
   elif A^B==full:v=s-1
   if v:edges[A,B]=Q(v)
 if trade:
  need(n==10,'trade domain')
  def mask(seq):return sum(1<<(i-1) for i in seq)
  pp=[(mask(x),e) for x,e in [([1,2,3],1),([1,4,5],1),([1,2,4],-1),([1,3,5],-1)]]
  qq=[(mask([i+5 for i in x]),e) for x,e in [([1,2,3],1),([1,4,5],1),([1,2,4],-1),([1,3,5],-1)]]
  for A,e in pp:
   for B,f in qq:
    need(not A&B and A.bit_count()==B.bit_count()==3,'proper trade support')
    edges[A,B]=edges.get((A,B),Q(0))+Q(7*e*f,3)
 return V,edges
def forms(n,V,B,u,ell):
 s,h,N,r,*_=parameters(n,2)
 U=h*sum(x*x for x in u.values())-2*sum(w*u[A]*u[C] for (A,C),w in B.items())
 C=s*sum(x*x for x in ell.values())-sum(ell.values())**2+2*sum(w*ell[A]*ell[C] for (A,C),w in B.items())
 card={A:A.bit_count() for A in V};Ca={A:s*card[A]-sum(card.values()) for A in V}
 for (A,D),w in B.items():Ca[A]+=w*card[D];Ca[D]+=w*card[A]
 return U,C,Ca

def main():
 records=[];position_count=star_count=compression_count=0
 for n,free,trade in [(6,False,False),(7,False,False),(8,False,False),(10,False,True),(7,True,False)]:
  k=2;s,h,N,r,Z,T,K,G,c=parameters(n,k);V,B=entries(n,free,trade);full=2**n-1
  ell={A:Q(0 if A.bit_count()<=k else 2 if A.bit_count()>=n-k else 1) for A in V}
  # An explicitly asymmetric complement-odd layer profile.
  profile={a:(Q((a*(n-a))%5,7),Q(2*a-n,13)) for a in range(k+1,n-k)}
  u={A:Q(A.bit_count()) if A.bit_count()<=k else Q(s*(n-A.bit_count()),h) if A.bit_count()>=n-k else sum(profile[A.bit_count()]) for A in V}
  if trade:
   for A in V:
    if k<A.bit_count()<n-k:u[A]=Q((A*19)%37-18,11)
  U,C,Ca=forms(n,V,B,u,ell);bulk=[A for A in V if k<A.bit_count()<n-k]
  z={A:s-B.get(tuple(sorted((A,full^A))),Q(0)) for A in bulk};lam=Q(n*n+3,4)
  f={A:A.bit_count()-u[A] for A in V};mass=sum(w for (A,D),w in B.items() if A in z and D in z and A^D!=full)
  lower=T-sum(z.values())+2*mass
  need(C==lower,'whole lower energy')
  b=c+lam*T+sum(r*((u[A]+u[full^A])/2)**2+N*((u[A]-u[full^A])/2)**2 for A in bulk)
  rhs=b+sum((f[A]*f[full^A]-lam)*z[A] for A in bulk)+2*sum((lam-f[A]*f[D])*w for (A,D),w in B.items() if A in z and D in z and A^D!=full)
  defect=sum((A.bit_count()-2*u[A])*Ca[A] for A in V)
  need(U+lam*C==rhs+defect,'complete arbitrary signed original identity with defect')
  if not free:
   need(not any(Ca.values()),'cardinality kernel')
   for i in range(n):
    ind={A:int(bool(A&(1<<i))) for A in V};action={A:s*ind[A]-sum(ind.values()) for A in V}
    for (A,D),w in B.items():action[A]+=w*ind[D];action[D]+=w*ind[A]
    need(not any(action.values()),'every individual point-star row');star_count+=len(V)
   rowB={A:Q(0) for A in V}
   for (A,D),w in B.items():rowB[A]+=w;rowB[D]+=w
   empty={A:h-rowB[A] for A in V};loop=h-sum(empty.values())
   need(all(rowB[A]+empty[A]==h for A in V) and loop+sum(empty.values())==h,'actual original empty row and loop')
   if not trade:
    for scale in [Q(-2),Q(0),Q(1),Q(3,5)]:
     arbitrary={A:scale*A.bit_count() if A.bit_count()<=k else Q((A*19)%37-18,11) for A in V}
     upper,_,_=forms(n,V,B,arbitrary,ell)
     residual=scale*scale*(c+sum(phi(n,A.bit_count(),z[A]) for A in bulk))
     residual+=h*sum((arbitrary[A]-scale*Q(s*(n-A.bit_count()),h))**2 for A in V if A.bit_count()>=n-k)
     for A in bulk:
      v=(arbitrary[A]+arbitrary[full^A])/2;t=(arbitrary[A]-arbitrary[full^A])/2;x=Q(2*A.bit_count()-n,2)
      residual+=(r+z[A])*(v-scale*Q(n)*z[A]/(2*(r+z[A])))**2+(N-z[A])*(t+scale*x*z[A]/(N-z[A]))**2
     need(upper==residual,'complete original cap compression incl scale zero');compression_count+=1
  else:need(defect!=0,'free signed matrix has a genuine kernel defect')
  position_count+=len(V)**2
  records.append(dict(n=n,k=k,vertices=len(V),unordered_nonzero_edges=len(B),free=free,trade=trade,upper=str(U),lower=str(C),combined=str(U+lam*C),defect=str(defect),proper_signed_beta_mass=str(mass)))
 return dict(original=records,original_full_positions=position_count,individual_star_rows=star_count,full_compressions=compression_count)
if __name__=='__main__':print(json.dumps(main(),sort_keys=True))
