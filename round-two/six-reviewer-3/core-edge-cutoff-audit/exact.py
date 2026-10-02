"""Independent dense Q[n] and normalized rational functions; no CAS dependency."""
from fractions import Fraction as F
from math import comb


def need(ok,label):
    if not ok:raise ValueError(label)


class P:
    def __init__(self,value=0):
        if isinstance(value,P):self.c=value.c;return
        raw=value if isinstance(value,(list,tuple)) else [value]
        need(not any(isinstance(x,float) for x in raw),'no floating polynomial input')
        rows=list(map(F,raw))
        while rows and rows[-1]==0:rows.pop()
        self.c=tuple(rows)
    def __add__(self,b):
        b=P(b);return P([(self.c[i] if i<len(self.c) else 0)+(b.c[i] if i<len(b.c) else 0) for i in range(max(len(self.c),len(b.c)))])
    __radd__=__add__
    def __neg__(self):return P([-x for x in self.c])
    def __sub__(self,b):return self+-P(b)
    def __rsub__(self,b):return P(b)+-self
    def __mul__(self,b):
        b=P(b);rows=[F(0)]*max(0,len(self.c)+len(b.c)-1)
        for i,x in enumerate(self.c):
            for j,y in enumerate(b.c):rows[i+j]+=x*y
        return P(rows)
    __rmul__=__mul__
    def __pow__(self,n):
        need(type(n)is int and n>=0,'nonnegative polynomial power');out=P(1)
        for _ in range(n):out*=self
        return out
    def __eq__(self,b):return self.c==P(b).c
    def divide(self,b):
        b=P(b);need(bool(b.c),'nonzero polynomial divisor');r=list(self.c);q=[F(0)]*max(0,len(r)-len(b.c)+1)
        while len(r)>=len(b.c):
            shift=len(r)-len(b.c);factor=r[-1]/b.c[-1];q[shift]=factor
            for j,x in enumerate(b.c):r[j+shift]-=factor*x
            while r and r[-1]==0:r.pop()
        return P(q),P(r)
    def exact_divide(self,b):
        q,r=self.divide(b);need(r==0,'exact polynomial division');return q
    def monic(self):return P([x/self.c[-1] for x in self.c]) if self.c else self
    def gcd(self,b):
        a=self;b=P(b)
        while b.c:a,b=b,a.divide(b)[1]
        return a.monic()
    def evaluate(self,n):
        out=F(0)
        for x in reversed(self.c):out=out*n+x
        return out
    def shifted(self,n):
        return P([sum((self.c[i]*comb(i,j)*F(n)**(i-j) for i in range(j,len(self.c))),F(0)) for j in range(len(self.c))])
    def record(self):return list(map(str,self.c))


class R:
    def __init__(self,a=0,b=1):
        if isinstance(a,R):self.a,self.b=a.a,a.b;return
        a,b=P(a),P(b);need(b!=0,'nonzero rational-function denominator')
        g=a.gcd(b);a,b=a.exact_divide(g),b.exact_divide(g)
        scale=b.c[-1];self.a=P([x/scale for x in a.c]);self.b=P([x/scale for x in b.c])
    def __add__(self,b):
        if isinstance(b,A):return NotImplemented
        b=R(b);return R(self.a*b.b+b.a*self.b,self.b*b.b)
    __radd__=__add__
    def __neg__(self):return R(-self.a,self.b)
    def __sub__(self,b):
        if isinstance(b,A):return NotImplemented
        return self+-R(b)
    def __rsub__(self,b):return R(b)+-self
    def __mul__(self,b):
        if isinstance(b,A):return NotImplemented
        b=R(b);return R(self.a*b.a,self.b*b.b)
    __rmul__=__mul__
    def __truediv__(self,b):
        b=R(b);return R(self.a*b.b,self.b*b.a)
    def __rtruediv__(self,b):return R(b)/self
    def __pow__(self,n):
        need(type(n)is int and n>=0,'nonnegative rational-function power');return R(self.a**n,self.b**n)
    def __eq__(self,b):b=R(b);return self.a==b.a and self.b==b.b
    def evaluate(self,n):return self.a.evaluate(n)/self.b.evaluate(n)
    def record(self):return {'numerator':self.a.record(),'denominator':self.b.record()}


class A:
    """Affine dependence on a FORMAL T, coefficients in Q(n)."""
    def __init__(self,a=0,b=0):
        if isinstance(a,A):self.a,self.b=a.a,a.b
        else:self.a,self.b=R(a),R(b)
    def __add__(self,b):b=A(b);return A(self.a+b.a,self.b+b.b)
    __radd__=__add__
    def __neg__(self):return A(-self.a,-self.b)
    def __sub__(self,b):return self+-A(b)
    def __rsub__(self,b):return A(b)+-self
    def __mul__(self,b):
        b=A(b);need(self.b*b.b==0,'scalar proof remains affine in formal T')
        return A(self.a*b.a,self.a*b.b+self.b*b.a)
    __rmul__=__mul__
    def __truediv__(self,b):b=A(b);need(b.b==0,'affine division only by Q(n)');return A(self.a/b.a,self.b/b.a)
    def __eq__(self,b):b=A(b);return self.a==b.a and self.b==b.b
    def evaluate(self,n,T):return self.a.evaluate(n)+self.b.evaluate(n)*T
    def record(self):return {'constant':self.a.record(),'formal_T_coefficient':self.b.record()}
