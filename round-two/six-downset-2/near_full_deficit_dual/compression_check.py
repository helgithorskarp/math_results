"""Independent literal and complete-layer controls of the ordinary proof."""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import hashlib,json,sys,time
from deficit_functional import parameters,phi,optimizer,require,rational_profile
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from affine import direct
from model import choose

def layer_energy(n,B,u):
 h=2**(n-1)-1
 return h*sum(comb(n,a)*u[a]*u[a] for a in range(1,n-1))-sum(
  comb(n,a)*u[a]*B[a][b]*choose(n-a,b)*u[b]
  for a in range(1,n-1) for b in range(1,n-1))

def layer_control(n,k):
 path=ROOT/f'fixtures/n{n}.json'
 doc=json.loads(path.read_text());B=direct(n,[Q(v) for v in doc['free_values']])
 N,s,h,r,c=parameters(n,k);bulk=range(k+1,n-k);z={a:Q(s)-B[a][n-a] for a in bulk}
 require(all(z[a]==z[n-a] for a in bulk),'Complete complementary profile')
 E=c+sum(comb(n,a)*phi(n,a,z[a]) for a in bulk)
 even=c+sum(comb(n,a)*phi(n,a,z[a],odd=False) for a in bulk)
 require(E>0 and even>=E,'Credited capped seed compression sign')
 ell={a:Q(0 if a<=k else 1 if a<n-k else 2) for a in range(1,n-1)}
 ell_energy=Q(s)*sum(comb(n,a)*ell[a]**2 for a in ell)-sum(comb(n,a)*ell[a] for a in ell)**2+sum(
  comb(n,a)*ell[a]*B[a][b]*choose(n-a,b)*ell[b] for a in ell for b in ell)
 mass=sum(comb(n,a)*z[a] for a in bulk)
 require(ell_energy==4*s-4-mass and ell_energy>=0,'Entire lower budget identity')
 records=[]
 for perturb in (False,True):
  u={a:Q(a) for a in range(1,n-1)}
  for a in range(n-k,n-1):u[a]=Q(s*(n-a),h)+(Q(a-n+k+1,7) if perturb else 0)
  for a in bulk:
   v,t=optimizer(n,a,z[a])
   if perturb:
    v+=Q((2*a-n)**2+3,13);t+=Q(2*a-n,11)
   u[a]=v+t
  energy=layer_energy(n,B,u);squares=h*sum(comb(n,a)*(u[a]-Q(s*(n-a),h))**2 for a in range(n-k,n-1))
  for a in bulk:
   v=(u[a]+u[n-a])/2;t=(u[a]-u[n-a])/2;v0,t0=optimizer(n,a,z[a])
   squares+=comb(n,a)*((r+z[a])*(v-v0)**2+(N-z[a])*(t-t0)**2)
  require(energy==E+squares,'Full high/even/odd exact square identity')
  records.append({'perturbed':perturb,'energy':str(energy),'squares':str(squares)})
 return {'n':n,'k':k,'seed_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
  'compressed_upper_minimum':str(E),'complement_even_minimum':str(even),
  'odd_refinement':str(even-E),'lower_budget_slack':str(ell_energy),'controls':records}

def literal_control():
 n=6;k=2;N,s,h,r,c=parameters(n,k)
 F=[A for A in range(1,1<<n) if A.bit_count()<=n-2];m=len(F);full=(1<<n)-1
 require(m==N-1 and N==57,'Literal original order and actual empty census')
 sizes=[A.bit_count() for A in F];pos={A:i for i,A in enumerate(F)}
 B=[[Q(0)]*m for _ in F]
 for i,A in enumerate(F):
  if sizes[i]<2:continue
  for j in range(i+1,m):
   D=F[j]
   if sizes[j]<2 or A&D:continue
   if A|D==full:
    deficit=Q(1+(min(A,D)%7),5);value=Q(s)-deficit
   elif min(sizes[i],sizes[j])<=k:value=Q((A+3*D)%11-5,17)
   else:value=Q(0)
   B[i][j]=B[j][i]=value
 for i,A in enumerate(F):
  if sizes[i]<2:continue
  residual=Q((n-sizes[i])*s)-sum(sizes[j]*B[i][j] for j in range(m) if sizes[j]>=2)
  for bit in range(n):
   if not(A>>bit&1):
    j=pos[1<<bit];B[i][j]=B[j][i]=residual/(n-sizes[i])
 singles=[pos[1<<bit] for bit in range(n)]
 targets=[Q((n-1)*s)-sum(sizes[j]*B[i][j] for j in range(m) if sizes[j]>=2) for i in singles]
 total=sum(targets)
 for a,i in enumerate(singles):
  for b in range(a+1,len(singles)):
   j=singles[b];B[i][j]=B[j][i]=(targets[a]+targets[b]-total/(n-1))/(n-2)
 require(all(sum(sizes[j]*B[i][j] for j in range(m))==(n-sizes[i])*s for i in range(m)),
  'Every original cardinality-kernel row of noninvariant control')
 require(all(not B[i][j] or not(F[i]&F[j]) for i in range(m) for j in range(m)),'Every supported original position')
 bulk=[i for i in range(m) if k<sizes[i]<n-k];high=[i for i in range(m) if sizes[i]>=n-k]
 z={i:Q(s)-B[i][pos[full^F[i]]] for i in bulk}
 require(len(set(z.values()))>1,'Literal control is not permutation invariant')
 E=c+sum(phi(n,sizes[i],z[i]) for i in bulk);checks=[]
 for scale in (Q(0),Q(1),Q(-3,2)):
  u=[scale*size for size in sizes]
  for i in high:u[i]=scale*Q(s*(n-sizes[i]),h)+Q(F[i]%5-2,9)
  for i in bulk:
   A=F[i];j=pos[full^A];v,t=optimizer(n,sizes[i],z[i])
   u[i]=scale*(v+t)+Q((min(A,full^A)%5)+1,7)+Q(A-(full^A),23)
  energy=h*sum(x*x for x in u)-sum(u[i]*B[i][j]*u[j] for i in range(m) for j in range(m))
  square=h*sum((u[i]-scale*Q(s*(n-sizes[i]),h))**2 for i in high)
  for i in bulk:
   j=pos[full^F[i]];v=(u[i]+u[j])/2;t=(u[i]-u[j])/2;v0,t0=optimizer(n,sizes[i],z[i])
   square+=(r+z[i])*(v-scale*v0)**2+(N-z[i])*(t-scale*t0)**2
  require(energy==scale*scale*E+square,'Literal original noninvariant full square identity')
  checks.append({'scale':str(scale),'energy':str(energy),'squares':str(square)})
 # Verify the actual empty row/loop lift and full original cap row sums.
 C=[[Q(s*int(i==j)-1)+B[i][j] for j in range(m)] for i in range(m)]
 sums=[sum(row) for row in C];L=[[Q(1)+sum(sums)]+[Q(1)-x for x in sums]]
 L+=[[Q(1)-sums[i]]+[Q(1)+x for x in row] for i,row in enumerate(C)]
 require(len(L)==N and all(sum(row)==N for row in L),'Actual original empty lift and regularity')
 require(all(L[i+1][j+1]==s*int(i==j)+B[i][j] for i in range(m) for j in range(m)),
  'Every original nonempty upper position')
 damaged=[row[:] for row in B];damaged[0][1]+=Q(1);damaged[1][0]+=Q(1)
 require(any(sum(sizes[j]*damaged[i][j] for j in range(m))!=(n-sizes[i])*s for i in range(m)),
  'Damaged kernel is detected')
 return {'n':n,'k':k,'literal_vertices':N,'noninvariant_cardinality_kernel_only':True,
  'synthetic_control_is_not_claimed_H':True,'complete_lift_positions':N*N,
  'compressed_minimum':str(E),'controls':checks,'damaged_kernel_detected':True}

def scalar_controls():
 controls=0
 for n in range(6,15):
  for a in range(3,n-2):
   for z in (Q(0),Q(1,3),Q(2),Q(2*(2**(n-1)-n)-2)):
    v,t=optimizer(n,a,z);x=Q(a)-Q(n,2);N=2**n-n-1;r=n-1
    expanded=Q(a*(n-a))*z-Q(n*n,4)*z*z/(r+z)-x*x*z*z/(N-z)
    require(phi(n,a,z)==expanded,'All-order functional factorization control')
    require(phi(n,a,z,odd=False)-phi(n,a,z)==x*x*z*z/(N-z),'Exact odd gain')
    controls+=1
 for n,k in ((6,2),(7,2),(24,6),(32,8),(40,11),(64,18)):
  lam=Q((2*n-5)**2,16);bound,profile=rational_profile(n,k,lam)
  r=n-1;N,s,h,r,c=parameters(n,k)
  prior=c+lam*(4*s-4)+r*sum(comb(n,a)*max(Q(0),Q(5,4)-Q((2*a-n)**2,4*n))**2 for a in range(k+1,n-k))
  require(bound<=prior,'Exact rational optimized-profile improvement at prior multiplier')
  for a,v,w in profile:
   for z in (Q(0),Q(1,3),Q(2)):
    F=phi(n,a,z,odd=False)
    square=(r+z)*(v-Q(n,2)*z/(r+z))**2+z*(lam-w)
    require(r*v*v+lam*z-F==square and square>=0,'Exact scalar square certificate')
    require(F-lam*z<=r*v*v,'Exact rational upper envelope witness')
    controls+=1
 return controls
