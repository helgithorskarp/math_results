"""Own derivation of the twelve-point frame from the signed written equations.

All clipping encloses the feasible subset, including tangencies. Domain
failures are unresolved arithmetic, never geometric exclusions.
"""
from fractions import Fraction as F
from enclosure import Box

LABELS = (0,1,2,4,5,6,7,8,9,10,11,12)
AA = (0,5,6,7,9,11)
BB = (1,2,4,8,10,12)
CONTACTS = (
 (0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),(2,4),(2,8),
 (2,10),(4,8),(5,7),(5,9),(5,11),(6,11),(7,12),(9,10),(9,11),(10,12))
TESTS = tuple((a,b) for a in AA for b in BB if (a,b) not in ((7,12),(9,10),(7,1)))

def plus(x,y): return [a+b for a,b in zip(x,y)]
def scale(a,x): return [a*b for b in x]
def cross(x,y):
    return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]
def dot(x,y,t):
    return (1-t)*sum(a*b for a,b in zip(x,y))+t*sum(x)*sum(y)
def inverse_metric(x,t):
    j=t*sum(x)/(1+2*t)
    return [(a-j)/(1-t) for a in x]
def base(t):
    r=2*t/(1+t)
    b={1:[1,0,0],2:[0,1,0],4:[0,0,1]}
    b[8]=plus(scale(r,plus(b[2],b[4])),scale(-1,b[1]))
    b[10]=plus(scale(r,plus(b[1],b[2])),scale(-1,b[4]))
    b[12]=plus(scale(r,plus(b[1],b[10])),scale(-1,b[2]))
    return r,b

class NecessaryEmpty(ArithmeticError):
    pass

def necessary_clip(x,lo,hi=None):
    try: return x.clip(lo,hi)
    except ArithmeticError as e: raise NecessaryEmpty(str(e))

def scalar_frame(t,z):
    r,b=base(t)
    determinant=(1-t).square()*(1+2*t)
    chart=1+determinant*z.square()
    k=necessary_clip(t*(9*t.square()-2*t-3)/(1+t).square(),F(-3,10),F(-1,5))
    d=inverse_metric(cross(b[12],b[1]),t)
    w=plus(scale(t,b[12]),plus(scale((determinant*z.square()-1)/chart,plus(b[1],scale(-t,b[12]))),scale(2*determinant*z/chart,d)))
    # The sealed symbolic audit proved this closed quotient independently.
    # Intersect two algebraically identical enclosures to reduce dependency.
    sh=(determinant*(t*z.square()-2*z)+t*(2*t-1))/chart
    sd=dot(w,b[10],t)
    s=necessary_clip(Box(max(sh.lo,sd.lo),min(sh.hi,sd.hi),raw=True),F(-24,25),F(7,10))
    g=1-s.square()-k.square()-t.square()+2*s*k*t
    return dict(t=t,z=z,r=r,b=b,D=determinant,C=chart,k=k,W=w,s=s,g=g)

def all_points(a,epsilon,eta):
    t,r,k,w,s=a['t'],a['r'],a['k'],a['W'],a['s']
    g=necessary_clip(a['g'],0)
    den=necessary_clip(1-s.square(),F(49,625),1)
    b=a['b']
    root=(a['D']*g).sqrt()
    v=scale(1/den,plus(plus(scale(k-s*t,w),scale(t-s*k,b[10])),scale(epsilon*root,inverse_metric(cross(w,b[10]),t))))
    gamma=k/(1+k)
    # Factorization checked in the sealed rational identity kernel.
    mu=(t-1)*(t+1)*(2*t+1)*(3*t-1)/((1+t).square()*(1+k))
    u=plus(scale(gamma,plus(w,v)),scale(eta*mu,inverse_metric(cross(w,v),t)))
    denominator=(2*r-1)*(r+1)
    out=dict(b);out.update({6:u,7:w,9:v})
    out[0]=scale(1/denominator,plus(plus(scale(r,u),scale(r,w)),scale(1-r,v)))
    out[5]=scale(1/denominator,plus(plus(scale(1-r,u),scale(r,w)),scale(r,v)))
    out[11]=scale(1/denominator,plus(plus(scale(r,u),scale(1-r,w)),scale(r,v)))
    return out

def chart_gap(t,z):
    return (1-t).square()*z.square()-1
