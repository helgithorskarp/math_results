"""Independent homogeneous and QQ(sqrt7) arithmetic, no target source/CAS."""
import json, math
from pathlib import Path
from fractions import Fraction as F
from shift_signs import polynomial
from literal_check import require
P=Path(__file__).resolve().parent
Z=(F(0),F(0));ONE=(F(1),F(0));rho=(F(3),F(1))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[0],-a[1])
def mul(a,b):return (a[0]*b[0]+7*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def div(a,b):
    norm=b[0]**2-7*b[1]**2;require(norm!=0,'nonzero quadratic field divisor')
    c=mul(a,(b[0],-b[1]));return(c[0]/norm,c[1]/norm)
def scale(a,c):return(a[0]*c,a[1]*c)
def ev(p,at,derivative=0):
    out=Z;powers=[ONE]
    for i in range(max((e[0] for e in p),default=0)):powers.append(mul(powers[-1],at))
    for (i,j),c in p.items():
        if i>=derivative:out=add(out,scale(powers[i-derivative],c*math.prod(range(i-derivative+1,i+1))))
    return out
def layer(p,n):return {e:c for e,c in p.items() if sum(e)==n}
def quadratic_divide(p):
    r=dict(p);out={}
    while r and max(i for i,j in r)>=2:
        e=max(r);i,j=e;c=r[e];ee=(i-2,j);out[ee]=out.get(ee,F(0))+c
        for d,v in (((i,j),c),((i-1,j+1),-6*c),((i-2,j+2),2*c)):
            r[d]=r.get(d,F(0))-v
            if not r[d]:del r[d]
    require(not r,'ENTIRE leading homogeneous quadratic factor')
    return out
def shifted_univariate(p):
    out={}
    for (i,j),c in p.items():
        for e in range(i+1):out[e]=out.get(e,F(0))+c*math.comb(i,e)*3**(i-e)
    out={e:c for e,c in out.items() if c}
    require(out.get(0,F(0))>0 and all(c>=0 for c in out.values()),'whole alpha>=3 leading sign')
    return out
def main():
    raw=json.loads((P/'optimization-polynomials.json').read_text());N=polynomial(raw['R_numerator']);D=polynomial(raw['R_denominator'])
    require(max(map(sum,N))==64 and max(map(sum,D))==62,'exact total residual degrees')
    n64,n63,n62,d62=(layer(p,n) for p,n in ((N,64),(N,63),(N,62),(D,62)))
    Q=quadratic_divide(n64);qp,dp=shifted_univariate(Q),shifted_univariate(d62)
    require(ev(n64,rho)==Z,'critical leading numerator vanishes')
    require(div(ev(n64,rho,1),ev(d62,rho))==(F(0),F(1)),'exact beta coefficient sqrt7')
    require(div(ev(n63,rho),ev(d62,rho))==(F(0),F(14)),'exact intercept -14')
    c0=div(add(add(scale(ev(n64,rho,2),98),scale(ev(n63,rho,1),-14)),ev(n62,rho)),ev(d62,rho))
    require(c0==(-F(7471,8),F(1387,4)),'entire constant at beta=-14')
    gamma=div(neg(c0),(F(0),F(1)))
    require(gamma==(-F(19418,56),F(7471,56)),'root next correction')
    # A further asymptotic Pell gap, conditional only on this checked root expansion.
    gap=add(gamma,(F(0),-F(1,14)))
    require(gap==(-F(19418,56),F(7467,56)),'Pell gap coefficient')
    from pell import sign_quad
    require(sign_quad(*c0)<0 and sign_quad(*gamma)>0 and sign_quad(*gap)>0,'exact quadratic signs')
    out=dict(status='complete homogeneous/root field identities verified',degrees=[64,62],
        homogeneous_quotient=[[list(e),str(c)] for e,c in sorted(Q.items(),reverse=True)],
        leading_positive_coefficients=dict(Q=len(qp),D=len(dp)),C0=list(map(str,c0)),gamma=list(map(str,gamma)),Pell_gap=list(map(str,gap)),
        ordinary_boundary='uniform rational expansion and eventual unique-root argument remain ordinary unformalized; far upper tail explicitly credited9980',CAS_imported=False)
    (P/'asymptotic-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='homogeneous_quotient'},indent=2))
if __name__=='__main__':main()
