"""Exact sparse Gaussian polynomial dictionaries; no numerical root inputs."""
from fractions import Fraction as F


def pair(x):
    if isinstance(x,tuple):return (F(x[0]),F(x[1]))
    return (F(x),F(0))

def plus(a,b):return (a[0]+b[0],a[1]+b[1])
def times(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def mono(a,b):
    out=dict(a)
    for k,v in b:out[k]=out.get(k,0)+v
    return tuple(sorted((k,v) for k,v in out.items() if v))

class Poly:
    def __init__(self,terms=()):
        self.terms={tuple(k):pair(v) for k,v in dict(terms).items() if pair(v)!=(0,0)}
    @staticmethod
    def constant(value):return Poly({():pair(value)})
    @staticmethod
    def variable(name):return Poly({((name,1),):(1,0)})
    def __add__(self,other):
        other=cast(other);out=self.terms.copy()
        for k,v in other.terms.items():out[k]=plus(out.get(k,(0,0)),v)
        return Poly(out)
    __radd__=__add__
    def __neg__(self):return Poly({k:(-v[0],-v[1]) for k,v in self.terms.items()})
    def __sub__(self,other):return self+-cast(other)
    def __rsub__(self,other):return cast(other)+-self
    def __mul__(self,other):
        other=cast(other);out={}
        for a,x in self.terms.items():
            for b,y in other.terms.items():
                k=mono(a,b);out[k]=plus(out.get(k,(0,0)),times(x,y))
        return Poly(out)
    __rmul__=__mul__
    def __truediv__(self,other):
        other=F(other)
        if not other:raise ValueError('nonzero scalar divisor required')
        return Poly({k:(v[0]/other,v[1]/other) for k,v in self.terms.items()})
    def __pow__(self,n):
        if type(n)!=int or n<0:raise ValueError('nonnegative integral degree required')
        out=cast(1);base=self
        while n:
            if n&1:out=out*base
            base=base*base;n//=2
        return out
    def substitute(self,mapping):
        out=cast(0)
        for k,v in self.terms.items():
            term=cast(v)
            for name,n in k:term=term*cast(mapping.get(name,Poly.variable(name)))**n
            out=out+term
        return out
    def coefficient(self,name,exponent):
        out={}
        for k,v in self.terms.items():
            m=dict(k)
            if m.pop(name,0)==exponent:out[tuple(sorted(m.items()))]=v
        return Poly(out)
    def derivative(self,name):
        out={}
        for k,v in self.terms.items():
            m=dict(k);n=m.get(name,0)
            if not n:continue
            m[name]=n-1;out[tuple(sorted((x,y) for x,y in m.items() if y))]=(n*v[0],n*v[1])
        return Poly(out)
    def integral(self,name):
        out={}
        for k,v in self.terms.items():
            m=dict(k);n=m.get(name,0)+1;m[name]=n
            out[tuple(sorted(m.items()))]=(v[0]/n,v[1]/n)
        return Poly(out)
    def divide_monomial(self,factors):
        out={}
        for k,v in self.terms.items():
            m=dict(k)
            for name,n in factors.items():
                if m.get(name,0)<n:raise ValueError('whole polynomial is not divisible by '+name)
                m[name]=m.get(name,0)-n
            out[tuple(sorted((x,y) for x,y in m.items() if y))]=v
        return Poly(out)
    def conjugate_coefficients(self):return Poly({k:(v[0],-v[1]) for k,v in self.terms.items()})
    def norm(self,bounds):
        out=F(0)
        for k,v in self.terms.items():
            term=abs(v[0])+abs(v[1])
            for name,n in k:term*=F(bounds[name])**n
            out+=term
        return out
    def reduce_square(self,name,value):
        out=cast(0)
        for k,v in self.terms.items():
            m=dict(k);n=m.pop(name,0)
            out+=Poly({tuple(sorted(m.items())):v})*cast(value)**(n//2)*Poly.variable(name)**(n%2)
        return out
    def __eq__(self,other):return self.terms==cast(other).terms
    def record(self):
        return {'*'.join(name+(('^'+str(n)) if n!=1 else '') for name,n in k) or '1':[str(v[0]),str(v[1])] for k,v in sorted(self.terms.items())}

def cast(x):return x if isinstance(x,Poly) else Poly.constant(x)
def symbol(name):return Poly.variable(name)
def need(test,label):
    if not test:raise ValueError(label)


def anchored(q):
    e=symbol('eta');z=symbol('z');a=1-e;primitive=9*q.integral('z')
    return primitive-primitive.substitute({'z':a})


def families():
    z,e,s,x,y,t,n=[symbol(k) for k in ('z','eta','xi','x','y','T','nu')]
    q0=(z-e*x)**6*((z-e*y)**2+e*t)
    shifted=y+8*s
    qv=(z-e*x)**6*(z**2-e*(2*shifted+(0,1)*s)*z+e*t+e**2*(shifted**2+(0,1)*s*shifted-s**2/2))
    qs=(z-e*x)**6*((z-e*(y+32*n))**2+e*t)-e*n
    return q0,qv,qs


def identities():
    z,e,s,x,y,t,n,h,v,q,q0,l=[symbol(k) for k in ('z','eta','xi','x','y','T','nu','eps','v','q','q0','ell')]
    baseline,imbalanced,impulse=families();ps=[anchored(Q) for Q in (baseline,imbalanced,impulse)]
    checked={}
    def equal(name,left,right):
        need(left==right,name);checked[name]=left.record()
    for name,Q,p in zip(('baseline','imbalance','impulse'),(baseline,imbalanced,impulse),ps):
        equal(name+' derivative',p.derivative('z'),9*Q)
        equal(name+' marked anchor',p.substitute({'z':1-e}),cast(0))
        equal(name+' marked variation',p.derivative('xi').substitute({'z':1-e}) if name=='imbalance' else p.derivative('nu').substitute({'z':1-e}),cast(0))
        equal(name+' critical-first-coefficient',p.coefficient('z',8)*F(8,9),Q.coefficient('z',7))
        equal(name+' critical-second-coefficient',p.coefficient('z',7)*F(7,9),Q.coefficient('z',6))
    roots=[symbol('r'+str(i)) for i in range(8)]
    S=sum(roots,cast(0));E2=sum((roots[i]*roots[j] for i in range(8) for j in range(i+1,8)),cast(0))
    equal('generic full Newton second moment',S**2-sum((r**2 for r in roots),cast(0)),2*E2)
    # Literal critical factors give a separate representation of the complex family.
    physical_y=y+8*h*v;mean=h**2*v/2
    heavy_plus=h**2*physical_y+(0,1)*h*(mean+q)
    heavy_minus=h**2*physical_y+(0,1)*h*(mean-q)
    literal=(z-h**2*x)**6*(z-heavy_plus)*(z-heavy_minus)
    literal=literal.reduce_square('q',t-h**4*v**2/4)
    equal('whole literal critical family versus joint polynomial',literal,imbalanced.substitute({'eta':h**2,'xi':h*v}))
    hp=mean+q;hm=mean-q
    equal('literal physical first h moment',hp+hm,h**2*v)
    equal('literal physical mixed hu moment',(hp+hm)*physical_y,h**2*v*physical_y)
    equal('literal mean h squared',(hp**2+hm**2).reduce_square('q',t-h**4*v**2/4)/2,t)
    shift_plus=8*h**3*v+(0,1)*(h**3*v/2+h*(q-q0))
    shift_minus=8*h**3*v+(0,1)*(h**3*v/2-h*(q-q0))
    energy=shift_plus*shift_plus.conjugate_coefficients()+shift_minus*shift_minus.conjugate_coefficients()
    equal('whole critical energy, all cross terms',energy,F(257,2)*h**6*v**2+2*h**2*(q-q0)**2)
    difference=(q-q0)*(q+q0)+h**4*v**2/4
    equal('opening difference of squares',difference.reduce_square('q',t-h**4*v**2/4).reduce_square('q0',t),cast(0))
    trace=-(ps[1]-ps[0]).coefficient('z',8).substitute({'eta':h**2,'xi':h*v})
    equal('whole original trace, complex obstruction',trace,F(9,8)*(cast(16)+cast((0,1)))*h**3*v)
    equal('minimum original energy trace floor',trace*trace.conjugate_coefficients()/8,F(20817,512)*h**6*v**2)
    equal('whole impulse perturbation',impulse-baseline,(z-e*x)**6*(-64*e*n*(z-e*y)+1024*e**2*n**2)-e*n)
    impulse_trace=-(ps[2]-ps[0]).coefficient('z',8)
    equal('whole original trace, real obstruction',impulse_trace,72*e*n)
    equal('real original energy trace floor',impulse_trace**2/8,648*e**2*n**2)
    for name,c in [('left',F(1,2)),('right',F(2))]:
        at=impulse.substitute({'z':e*x+c*e*l,'nu':e**6*l**6}).divide_monomial({'eta':7,'ell':6})
        equal('literal real root sign '+name,at,c**6*(t+e*(x-y-32*e**6*l**6+c*l)**2)-1)
    equal('all powers in physical real trace',impulse_trace.substitute({'nu':e**6*l**6}),72*e**7*l**6)
    # Companion coefficients are conjugated without conjugating the complex parameters.
    equal('literal conjugate critical factors versus holomorphic companion',literal.conjugate_coefficients(),imbalanced.conjugate_coefficients().substitute({'eta':h**2,'xi':h*v}))
    return {'universal_identities':checked,'anchored_families':{name:p.record() for name,p in zip(('baseline','imbalance','impulse'),ps)}}


def majorants():
    e=symbol('eta');z=symbol('z');q0,qv,qs=families();out={}
    for name,Q,param,width in [('imbalance',qv,'xi',F(1,64)),('impulse',qs,'nu',F(1,2048))]:
        p=anchored(Q);divided=(p-z**9+1).divide_monomial({'eta':1});bounds={'eta':F(1,1024),'z':F(17,16),'x':F(9,8),'y':F(9,8),'T':F(25,16),param:width}
        bound=divided.norm(bounds);need(bound<64,'complete anchored family majorant '+name)
        need(p.coefficient('z',9)==1 and p.substitute({'z':1-e})==0,'monic marked family '+name)
        out[name]={'complete_divided_polynomial':divided.record(),'exact_norm':str(bound),'term_count':len(divided.terms),'bounds':{k:str(v) for k,v in bounds.items()}}
    return out
