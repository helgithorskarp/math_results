"""Separate exact coefficient-identity checker, no producer/field imports.

Integer Horner evaluation and conservative COMPLETE bidegree grids prove
nine rational identities. Binomial composition proves full-quadrant signs.
These are same-author checks, not independent person review or formalization.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name]='1'
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json,sys,signal,time,resource,argparse

DOMAIN='auxiliary real h>=2,q>=4; original integer h>=2,q=2^(n-1),integer n>=3'
NAMES=('a0','b0','beta','c0','comparison','kappa','nu','nu_upper','upper_gap')
def require(ok,msg):
    if not ok:raise ValueError(msg)
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def maximum(a,b):return tuple(max(x,y) for x,y in zip(a,b))
class Degree:
    def __init__(self,v=0,n=None,d=(0,0)):
        if isinstance(v,Degree):self.n,self.d=v.n,v.d
        else:self.n=n if n is not None else (0,0) if v else None;self.d=d
    def __neg__(self):return Degree(1,self.n,self.d) if self.n is not None else Degree()
    def __add__(self,b):
        b=Degree(b)
        if self.n is None:return b
        if b.n is None:return self
        return Degree(1,maximum(plus(self.n,b.d),plus(b.n,self.d)),plus(self.d,b.d))
    __radd__=__add__
    def __sub__(self,b):return self+-Degree(b)
    def __rsub__(self,b):return Degree(b)+-self
    def __mul__(self,b):
        b=Degree(b)
        return Degree(1,plus(self.n,b.n),plus(self.d,b.d)) if self.n is not None and b.n is not None else Degree()
    __rmul__=__mul__
    def __truediv__(self,b):
        b=Degree(b);require(b.n is not None,'nonzero degree divisor')
        return Degree(1,plus(self.n,b.d),plus(self.d,b.n)) if self.n is not None else Degree()
    def __rtruediv__(self,b):return Degree(b)/self
    def __pow__(self,n):
        require(type(n)is int and n>=0,'degree power');out=Degree(1)
        for _ in range(n):out=out*self
        return out

def model(q,h):
    """Independent common-denominator primitive seed reconstruction."""
    if type(q)is int:q=F(q)
    if type(h)is int:h=F(h)
    s=q+3*h;N=2*q+12*h;ell=6*h+1;E=ell-q+1
    beta=(2*ell**2*s**2*(h-1)-9*(h+3)*E**2)/(3*ell**2*s*(h-1))
    mu_n=2*ell**2*s*(h-1)*(s-3)-6*s*(h-1)*(ell*q-9*h-1)-27*E**2
    nu=h*mu_n/(3*ell**2*s*(h-1)*(2*h-1))
    kappa=2/nu+4/beta;theta=(2*h-1)/(2*h)
    a0=(12*N+9*theta*nu)/N**2;b0=(2*N+beta+theta*nu)/N**2
    Z=6*h**2-2*h-1;c0=(3*Z-3*h+1)/(Z*N)
    D=ell*(2*h-1);nu_upper=(D+1)*N/(6*D)-nu
    upper_gap=2*h/(2*h-1)*(h*(ell**2-3)/ell**2+9*E**2/(2*ell**2*s*(h-1)))
    comparison=36*a0*b0-(kappa-6*c0)**2
    return dict(beta=beta,nu=nu,kappa=kappa,a0=a0,b0=b0,c0=c0,nu_upper=nu_upper,upper_gap=upper_gap,comparison=comparison)

class Polynomial:
    def __init__(self,c):
        require(type(c)is dict and set(c)=={'denominator','terms'},'entire polynomial schema')
        d=c['denominator'];terms=c['terms']
        require(type(d)is int and d>0 and type(terms)is list and 0<len(terms)<=512,'positive denominator and unchanged512term bound')
        a={};last=None
        for z in terms:
            require(type(z)is list and len(z)==2 and type(z[0])is list and len(z[0])==2,'polynomial term schema')
            e=tuple(z[0]);require(all(type(x)is int and 0<=x<=64 for x in e),'bounded nonnegative integer exponents')
            require(last is None or last<e,'entire sorted unique monomials');last=e
            require(type(z[1])is str and str(int(z[1]))==z[1] and int(z[1])!=0,'canonical nonzero integer coefficient')
            a[e]=int(z[1])
        self.a,self.den=a,d;self.degree=tuple(max(e[i] for e in a) for i in range(2))
        # Independent homogeneous Horner in h, followed by Horner in q.
        self.rows={}
        for (i,j),v in a.items():self.rows.setdefault(i,{})[j]=v
    def value(self,h,q):
        result=0
        for i in range(self.degree[0],-1,-1):
            row=self.rows.get(i,{});v=0
            for j in range(self.degree[1],-1,-1):v=v*q+row.get(j,0)
            result=result*h+v
        return F(result,self.den)
    def shifted(self):
        a={}
        for (i,j),v in self.a.items():
            for k in range(i+1):
                for l in range(j+1):
                    e=(k,l);a[e]=a.get(e,0)+v*comb(i,k)*2**(i-k)*comb(j,l)*4**(j-l)
        a={e:v for e,v in a.items() if v};require(len(a)<=512,'unchanged512shift term bound')
        require(a.get((0,0),0)>0 and all(v>=0 for v in a.values()),'strict full-quadrant shifted coefficient sign')
        return {'original_terms':len(self.a),'shifted_terms':len(a),'bidegree':list(self.degree),'shifted_positive_constant':str(F(a[(0,0)],self.den)),'nonnegative_every_coefficient':True}

class Rational:
    def __init__(self,c,poles):
        require(type(c)is dict and set(c)=={'numerator','denominator_factors'},'entire rational schema')
        self.num=Polynomial(c['numerator']);self.den=[];degree=(0,0)
        require(type(c['denominator_factors'])is list and len(c['denominator_factors'])<=16,'bounded factored denominator')
        seen=set()
        for z in c['denominator_factors']:
            require(type(z)is dict and set(z)=={'factor','power'},'factor schema')
            require(type(z['power'])is int and 1<=z['power']<=8,'bounded positive integer pole power')
            key=json.dumps(z['factor'],sort_keys=True,separators=(',',':'))
            require(key not in seen,'no duplicate factor');seen.add(key)
            if key not in poles:poles[key]=Polynomial(z['factor'])
            p=poles[key];power=z['power'];self.den.append((key,power));degree=plus(degree,tuple(power*x for x in p.degree))
        self.degree=Degree(1,self.num.degree,degree)
    def value(self,h,q,pole_values):
        value=self.num.value(h,q)
        for key,power in self.den:value/=pole_values[key]**power
        return value

def verify(certificate):
    require(type(certificate)is dict and set(certificate)=={'domain','fields'},'whole certificate schema')
    require(certificate['domain']==DOMAIN and set(certificate['fields'])==set(NAMES),'full domain and all nine identities')
    poles={};fields={n:Rational(certificate['fields'][n],poles) for n in NAMES}
    signs={n:fields[n].num.shifted() for n in NAMES}
    pole_signs=[p.shifted() for _,p in sorted(poles.items())]
    symbolic=model(Degree(1,(0,1)),Degree(1,(1,0)))
    bounds={}
    for n in NAMES:
        a,b=fields[n].degree,symbolic[n]
        require(b.n is not None,'expected nonzero rational expression')
        bounds[n]=maximum(plus(a.n,b.d),plus(b.n,a.d))
    global_bound=tuple(max(d[i] for d in bounds.values()) for i in range(2))
    nodes=(global_bound[0]+1)*(global_bound[1]+1)
    require(nodes<=8379,'unchanged prior8379node complete-grid guard')
    count=0
    for h in range(2,global_bound[0]+3):
        for q in range(4,global_bound[1]+5):
            values={k:p.value(h,q) for k,p in poles.items()};require(all(v>0 for v in values.values()),'all grid poles strictly positive')
            expected=model(q,h)
            for n in NAMES:
                require(fields[n].value(h,q,values)==expected[n],'complete coefficient identity '+n+' at '+str((h,q)));count+=1
    require(count==9*nodes,'entire Cartesian identity grid completed')
    require(signs['comparison']['shifted_terms']==403,'entire403term active-endpoint comparison')
    return {'status':'COMPLETE nine exact rational identities and full-quadrant signs','domain':DOMAIN,'conservative_cross_product_bidegrees':{n:list(d) for n,d in bounds.items()},'complete_grid_bidegree':list(global_bound),'complete_nodes':nodes,'exact_equalities':count,'numerator_signs':signs,'distinct_positive_denominator_factors':len(poles),'denominator_signs':pole_signs,'same_author_separate_arithmetic':True,'ordinary_physical_bridge':'Unformalized author proof; no independent person verdict'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('certificate',nargs='?',default='CERTIFICATE.json');args=parser.parse_args()
    def alarm(a,b):raise TimeoutError('unchanged60s separate coefficient checker')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    c=json.loads(Path(args.certificate).read_text());out=verify(c);signal.alarm(0)
    work=Path(__file__).resolve().parent/'work';work.mkdir(exist_ok=True)
    (work/f'checker-O{sys.flags.optimize}.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'complete_nodes':out['complete_nodes'],'exact_equalities':out['exact_equalities'],'complete_grid_bidegree':out['complete_grid_bidegree'],'seconds':time.monotonic()-start,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'optimized':sys.flags.optimize,'status':out['status']}),flush=True)
if __name__=='__main__':main()
