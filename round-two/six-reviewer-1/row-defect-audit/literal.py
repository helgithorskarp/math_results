"""Full original domains: new incidence-null tensor trades, no PSD assertion."""
from itertools import combinations
from exact import *
from model import *

def family(n):
 # Cardinality order is separate from author bitmask order.
 domain=[sum(1<<i for i in c) for a in range(1,n-1) for c in combinations(range(n),a)]
 scan=[A for A in range(1,1<<n) if A.bit_count()<=n-2]
 need(sorted(domain)==scan and len(domain)==2**n-n-2,'complete_domain')
 return domain

def build(n):
 domain=family(n);index={A:i for i,A in enumerate(domain)};T,N,s,h=params(n);b=base(n)
 C=[[F(s*(A==B)-1)+(weight(b,A.bit_count(),B.bit_count()) if not A&B else 0) for B in domain] for A in domain]
 def incidence_null(points):
  u=[F(0)]*len(domain);u[index[sum(1<<i for i in points)]]=1
  for i in points:u[index[1<<i]]=-1
  return u
 trades=[((0,1,2),(3,4,5),F(5,7)),((0,3,6),(1,2,4),-F(2,3)),((0,2),(1,5),F(3,11))]
 for left,right,c in trades:
  u,v=incidence_null(left),incidence_null(right)
  need(not set(left)&set(right),'disjoint_tensor_trade')
  for a in range(len(domain)):
   for z in range(len(domain)):
    change=c*(u[a]*v[z]+v[a]*u[z])
    if change:C[a][z]+=change
 return domain,C

def inspect(n,k,domain,C,damage=None):
 T,N,s,h=params(n);m=N-1;need(len(domain)==m,'literal_dimension');need(len(set(domain))==m,'literal_unique');need(all(0<A<2**n and A.bit_count()<=n-2 for A in domain),'literal_domain_valid')
 p,q,r,f,g=profiles(n,k);P=[p[A.bit_count()-1] for A in domain];Q=[q[A.bit_count()-1] for A in domain];R=[r[A.bit_count()-1] for A in domain]
 v=[sum(row) for row in C];sigma=sum(v);U=[[F(N*(i==j)-1)-C[i][j] for j in range(m)] for i in range(m)]
 L=[[F(1)+sigma]+[F(1)-x for x in v]]+[[F(1)-v[i]]+[F(1)+x for x in C[i]] for i in range(m)]
 if damage=='empty-row':L[0][1]+=1
 if damage=='empty-loop':L[0][0]+=1
 for i in range(N):
  need(sum(L[i])==N,'actual_regular_row')
  for j in range(N):need(L[i][j]==L[j][i],'actual_symmetry')
 for i,A in enumerate(domain):
  need(C[i][i]==s-1,'nonempty_diagonal')
  for j,B in enumerate(domain):
   if A&B:need(C[i][j]==s*(i==j)-1,'intersecting_support')
 for point in range(n):
  x=[F(bool(A&(1<<point))) for A in domain];need(sum(x)==s,'point_star_size')
  need(all(z==0 for z in mv(C,x)),'original_individual_star_kernel')
 need(dot([A.bit_count() for A in domain],v)==0,'literal_cardinality_defect')
 need(len({C[i][j] for i,A in enumerate(domain) for j,B in enumerate(domain) if A.bit_count()==B.bit_count()==3 and not A&B})>1,'noninvariant_original_weights')
 for X,core,isupper in ((P,C,False),(Q,U,True)):
  mean=sum(X)/N;z=[-mean]+[x-mean for x in X]
  need(sum(z)==0 and [z[i+1]-z[0] for i in range(m)]==X,'full_pullback_vector')
  whole=energy(L,z)
  if isupper:whole=N*dot(z,z)-whole
  need(whole==energy(core,X),'full_lift_quadratic_energy')
 need(any(v) and sigma>0,'signed_noncentered_control');need(sum(x*x for x in v)>0,'physical_defect_norm')
 signed=F(0);positive=negative=0;omitted=[]
 for i,A in enumerate(domain):
  for j in range(i+1,m):
   B=domain[j];a,b=A.bit_count(),B.bit_count()
   if not A&B and a+b<n and min(a,b)>k:
    coefficient=f[a-1]*f[b-1]-g[a-1]*g[b-1];need(coefficient>0,'literal_positive_weights')
    entry=1+C[i][j];signed+=2*coefficient*entry;positive+=entry>0;negative+=entry<0
    omitted.append([A,B,entry,coefficient])
 if damage=='unordered-factor':signed*=2
 actual=energy(C,P)+energy(U,Q);W=scalar(n,k)
 correction=-F(n*n-6,n*n)*sigma+dot(R,v)
 if damage=='drop-row':correction=-F(n*n-6,n*n)*sigma
 if damage=='drop-loop':correction=dot(R,v)
 need(actual==W+signed+correction,'literal_signed_identity')
 beta=debias(n);debiased=[R[i]-beta*(2*A.bit_count()-n) for i,A in enumerate(domain)]
 need(actual==W+signed-(F(n*n-6,n*n)+beta*n)*sigma+dot(debiased,v),'literal_debiased_identity')
 # Two separate physical restrictions of the FULL original lifts, incl empty.
 K,V=physical(n,base(n));sizes=range(1,n-1)
 restrictions=[]
 for a in sizes:
  inds=[i for i,A in enumerate(domain) if A.bit_count()==a];row=[]
  for b in sizes:
   js=[j for j,B in enumerate(domain) if B.bit_count()==b]
   lower=sum(L[i+1][j+1]-1 for i in inds for j in js)
   upper=sum(N*(i==j)-L[i+1][j+1] for i in inds for j in js)
   need(lower==sum(C[i][j] for i in inds for j in js),'whole_lower_restriction')
   need(upper==sum(U[i][j] for i in inds for j in js),'whole_upper_restriction');row.append([lower,upper])
  restrictions.append(row)
 return {'n':n,'k':k,'N':N,'domain':domain,'core_sha256':digest(C),'whole_sha256':digest(L),'physical_restrictions':restrictions,'sigma':sigma,'v_sha256':digest(v),'v_norm2':dot(v,v),'signed':signed,'positive_original_omitted':positive,'negative_original_omitted':negative,'base_scalar':W,'actual_energy':actual,'row_correction':correction,'omitted_sha256':digest(omitted),'debiased_norm2':dot(debiased,debiased),'actual_empty_M_loop':(L[0][0]-s)/h,'PSD_or_cap_claimed':False}

def audit(n,k):
 domain,C=build(n)
 return inspect(n,k,domain,C)


def permutation_control():
 n=7;k=2;domain,C=build(n);old=inspect(n,k,domain,C);pi=(6,3,0,5,1,4,2)
 mapped=[sum(1<<pi[i] for i in range(n) if A&(1<<i)) for A in domain]
 order=sorted(range(len(domain)),key=lambda i:mapped[i]);D=[mapped[i] for i in order];B=[[C[i][j] for j in order] for i in order]
 fresh=inspect(n,k,D,B)
 for tag in ('sigma','v_norm2','signed','actual_energy','row_correction','debiased_norm2'):need(old[tag]==fresh[tag],'point_and_domain_permutation')
 return {'permutation':pi,'new_domain_order':'ascending INTEGER masks','whole_sha256':fresh['whole_sha256'],'invariants':[old[tag] for tag in ('sigma','v_norm2','signed','actual_energy','row_correction','debiased_norm2')]}
