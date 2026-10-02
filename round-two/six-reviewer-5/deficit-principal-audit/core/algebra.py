"""Fresh exact field audit of the written identities; no target code or data."""
import json
from sympy.polys.fields import field
from sympy.polys.domains import QQ
K,n,s,a,z,v,t,lam=field('n,s,a,z,v,t,lam',QQ)
r=n-1;N=2*s+r;h=s+r;x=a-n/2
phi=n*n*r*z/(4*(r+z))-N*x*x*z/(N-z)
f=a-v-t;fc=n-a-v+t
vp=n*z/(2*(r+z));tp=-x*z/(N-z)
checks=[]
def check(name,difference):
 if difference:raise ValueError(name)
 checks.append(name)
check('scalar square, arbitrary real v,t',r*v*v+N*t*t+lam*z-phi-((r+z)*(v-vp)**2+(N-z)*(t-tp)**2+z*(lam-f*fc)))
check('optimal complementary product derivative', (a-vp-tp)*(n-a-vp+tp)-phi.diff(z))
check('quartic derivative equation',(phi.diff(z)-lam)*(r+z)**2*(N-z)**2+((lam*(r+z)**2-n*n*r*r/4)*(N-z)**2+N*N*x*x*(r+z)**2))
check('first derivative',phi.diff(z)-(n*n*r*r/(4*(r+z)**2)-N*N*x*x/(N-z)**2))
check('strict concavity',phi.diff(z).diff(z)+n*n*r*r/(2*(r+z)**3)+2*N*N*x*x/(N-z)**3)
pair=h*((v+t)**2+(v-t)**2)+2*s*((a-n)*(v+t)-a*(v-t))-s*(a*a+(n-a)**2)-2*(s-z)*f*fc
check('literal original complementary pair',pair-(-s*n*n+2*phi+2*(r+z)*(v-vp)**2+2*(N-z)*(t-tp)**2))
lowhigh=h*(a*a+(s*a/h)**2)+2*s*((a-n)*a-a*s*a/h)-s*(a*a+(n-a)**2)
check('literal original low/high pair',lowhigh-((h-s*s/h)*a*a-s*n*n))
check('original singleton',h+2*s*(1-n)-s-(N-2*n*s))
check('global constant cancellation',n*n*s*s-s*n*n*(s-1)+n*(N-2*n*s)-(n*h-n*(n-1)*s))
check('odd improvement',(n*n*r*z/(4*(r+z))-x*x*z)-phi-x*x*z*z/(N-z))
check('endpoint derivative',(phi.diff(z)-a*(n-a)).evaluate(z,0))
# Exposing the original cardinality defect keeps every individual supported edge.
L,j,beta,uA,uB,eA,eB=field('L,j,beta,uA,uB,eA,eB',QQ)[1:]
# separate field names represent sizes eA,eB and lower coefficients eA/eB tests.
# The free-edge upper coefficient minus the kernel defect is exactly shifted.
check('free original upper edge coefficient',-2*uA*uB-(2*eA*eB-2*uA*eB-2*uB*eA)+2*(eA-uA)*(eB-uB))
print(json.dumps({'field':'QQ(n,s,a,z,v,t,lambda)','identities':checks,'count':len(checks)},sort_keys=True))
