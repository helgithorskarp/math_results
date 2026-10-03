"""Independent standard-library arithmetic in Q(c), 8c^3-6c-1=0.

The real embedding is the unique root in (15/16,47/50).  Complex values
use T=i*sin(pi/9), T^2=c^2-1. No producer module or data is imported.
"""
from fractions import Fraction as Q


def need(condition, message):
    if not condition:
        raise ValueError(message)


class F:
    def __init__(self, value=0):
        if isinstance(value, F):
            self.a = value.a
        elif isinstance(value, (tuple, list)):
            need(len(value) == 3, 'Field element must have three coefficients')
            self.a = tuple(Q(x) for x in value)
        else:
            self.a = (Q(value), Q(0), Q(0))

    def __add__(self, other):
        if not isinstance(other,(F,Q,int,str,tuple,list)):
            return NotImplemented
        b = F(other)
        return F(tuple(x+y for x,y in zip(self.a,b.a)))

    __radd__ = __add__

    def __neg__(self):
        return F(tuple(-x for x in self.a))

    def __sub__(self, other):
        if not isinstance(other,(F,Q,int,str,tuple,list)):
            return NotImplemented
        return self+-F(other)

    def __rsub__(self, other):
        return F(other)+-self

    def __mul__(self, other):
        if not isinstance(other,(F,Q,int,str,tuple,list)):
            return NotImplemented
        b = F(other)
        p = [Q(0)]*5
        for i,x in enumerate(self.a):
            for j,y in enumerate(b.a):
                p[i+j] += x*y
        for k in (4,3):
            p[k-3] += p[k]/8
            p[k-2] += 3*p[k]/4
        return F(p[:3])

    __rmul__ = __mul__

    def inverse(self):
        need(self != F(0), 'Division by zero')
        columns = [(self*F(tuple(int(i==j) for i in range(3)))).a for j in range(3)]
        rows = [[columns[j][i] for j in range(3)]+[Q(i==0)] for i in range(3)]
        for j in range(3):
            pivot = next((i for i in range(j,3) if rows[i][j]),None)
            need(pivot is not None,'Singular field inverse')
            rows[j],rows[pivot] = rows[pivot],rows[j]
            d = rows[j][j]
            rows[j] = [x/d for x in rows[j]]
            for i in range(3):
                if i != j:
                    d = rows[i][j]
                    rows[i] = [x-d*y for x,y in zip(rows[i],rows[j])]
        result = F(tuple(rows[i][3] for i in range(3)))
        need(self*result == 1,'Inverse product fails')
        return result

    def __truediv__(self, other):
        if not isinstance(other,(F,Q,int,str,tuple,list)):
            return NotImplemented
        return self*F(other).inverse()

    def __rtruediv__(self, other):
        return F(other)*self.inverse()

    def __pow__(self, n):
        need(isinstance(n,int),'Noninteger field exponent')
        if n < 0:
            return self.inverse()**(-n)
        result,base = F(1),self
        while n:
            if n%2:
                result = result*base
            base = base*base
            n //= 2
        return result

    def __eq__(self, other):
        try:
            return self.a == F(other).a
        except (ValueError,TypeError):
            return False

    def serial(self):
        return [str(x) for x in self.a]

    def sign(self):
        if self == 0:
            return 0
        lo,hi = Q(15,16),Q(47,50)
        for _ in range(180):
            a,b = Q(0),Q(0)
            for coefficient in reversed(self.a):
                p = (a*lo,a*hi,b*lo,b*hi)
                a,b = min(p)+coefficient,max(p)+coefficient
            if a > 0:
                return 1
            if b < 0:
                return -1
            mid = (lo+hi)/2
            if 8*mid**3-6*mid-1 < 0:
                lo = mid
            else:
                hi = mid
        raise ValueError('Unresolved exact embedding sign')


C = F((0,1,0))


class Z:
    def __init__(self, real=0, imag=0):
        if isinstance(real,Z):
            self.r,self.t = real.r,real.t
        else:
            self.r,self.t = F(real),F(imag)

    def __add__(self, other):
        b = Z(other)
        return Z(self.r+b.r,self.t+b.t)

    __radd__ = __add__

    def __neg__(self):
        return Z(-self.r,-self.t)

    def __sub__(self, other):
        return self+-Z(other)

    def __rsub__(self, other):
        return Z(other)+-self

    def __mul__(self, other):
        b = Z(other)
        return Z(self.r*b.r+(C*C-1)*self.t*b.t,self.r*b.t+self.t*b.r)

    __rmul__ = __mul__

    def conjugate(self):
        return Z(self.r,-self.t)

    def norm(self):
        return self.r*self.r+(1-C*C)*self.t*self.t

    def __truediv__(self, other):
        b = Z(other)
        return self*b.conjugate()*b.norm().inverse()

    def __rtruediv__(self, other):
        return Z(other)/self

    def __pow__(self, n):
        if n < 0:
            return (Z(1)/self)**(-n)
        result,base = Z(1),self
        while n:
            if n%2:
                result = result*base
            base = base*base
            n //= 2
        return result

    def __eq__(self, other):
        b = Z(other)
        return self.r == b.r and self.t == b.t

    def serial(self):
        return dict(real=self.r.serial(),T_coefficient=self.t.serial())


class Poly:
    """Sparse multivariate polynomials with exact field coefficients."""
    def __init__(self, n, terms=None):
        self.n = n
        self.d = {tuple(k):F(v) for k,v in (terms or {}).items() if F(v)!=0}
        need(all(len(k)==n and all(isinstance(i,int)and i>=0 for i in k) for k in self.d),'Malformed monomial')

    @classmethod
    def const(cls, n, value):
        return cls(n,{(0,)*n:F(value)})

    @classmethod
    def var(cls, n, index):
        return cls(n,{tuple(int(i==index)for i in range(n)):F(1)})

    def lift(self, value):
        if isinstance(value,Poly):
            need(value.n==self.n,'Polynomial dimension mismatch')
            return value
        return Poly.const(self.n,value)

    def __add__(self, other):
        b = self.lift(other)
        d = dict(self.d)
        for k,v in b.d.items():
            d[k] = d.get(k,F(0))+v
        return Poly(self.n,d)

    __radd__ = __add__

    def __neg__(self):
        return Poly(self.n,{k:-v for k,v in self.d.items()})

    def __sub__(self, other):
        return self+-self.lift(other)

    def __rsub__(self, other):
        return self.lift(other)+-self

    def __mul__(self, other):
        b = self.lift(other)
        d = {}
        for i,x in self.d.items():
            for j,y in b.d.items():
                k = tuple(a+b for a,b in zip(i,j))
                d[k] = d.get(k,F(0))+x*y
        return Poly(self.n,d)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self*F(other).inverse()

    def __pow__(self, n):
        need(isinstance(n,int)and n>=0,'Polynomial exponent')
        result = Poly.const(self.n,1)
        for _ in range(n):
            result = result*self
        return result

    def derivative(self, index=0):
        d = {}
        for k,v in self.d.items():
            if k[index]:
                j = list(k)
                j[index] -= 1
                d[tuple(j)] = v*k[index]
        return Poly(self.n,d)

    def evaluate(self, values):
        need(len(values)==self.n,'Evaluation dimension')
        result = F(0)
        for powers,coefficient in self.d.items():
            for p,v in zip(powers,values):
                coefficient = coefficient*F(v)**p
            result = result+coefficient
        return result

    def serial(self):
        return [[list(k),v.serial()]for k,v in sorted(self.d.items())]

    def same(self, other):
        return self.d == self.lift(other).d
