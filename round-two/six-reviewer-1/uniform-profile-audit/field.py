"""Fresh exact Q(zeta_36), Phi36=X^12-X^6+1, stdlib Fraction.

No native/earlier campaign executable kernel imported. Physical embedding
zeta_36=exp(pi*i/18); conjugation sends zeta_36 to its inverse.
"""
from fractions import Fraction as Q


def need(ok, message):
    if not ok:
        raise ValueError(message)


def strip(a):
    a=list(a)
    while a and not a[-1]:
        a.pop()
    return a


def pmul(a,b):
    out=[Q(0)]*(len(a)+len(b)-1) if a and b else []
    for j,x in enumerate(a):
        for k,y in enumerate(b):
            out[j+k]+=x*y
    return strip(out)


def psub(a,b):
    out=list(a)+[Q(0)]*max(0,len(b)-len(a))
    for j,v in enumerate(b):
        out[j]-=v
    return strip(out)


def pdiv(a,b):
    a=strip(a);b=strip(b)
    need(bool(b),'zero polynomial divisor')
    q=[Q(0)]*max(0,len(a)-len(b)+1)
    while len(a)>=len(b):
        shift=len(a)-len(b);v=a[-1]/b[-1];q[shift]+=v
        a=psub(a,[Q(0)]*shift+[v*x for x in b])
    return strip(q),a


class E:
    __slots__=('v',)
    def __init__(self,value=0):
        if isinstance(value,E):
            self.v=value.v
            return
        a=list(value) if isinstance(value,(tuple,list)) else [Q(value)]
        a=[Q(x)for x in a]+[Q(0)]*max(0,12-len(a))
        for j in range(len(a)-1,11,-1):
            a[j-6]+=a[j];a[j-12]-=a[j];a[j]=Q(0)
        self.v=tuple(a[:12])
    def __bool__(self):
        return any(self.v)
    def __eq__(self,other):
        try:return self.v==E(other).v
        except (TypeError,ValueError):return False
    def __add__(self,other):
        other=E(other)
        return E([a+b for a,b in zip(self.v,other.v)])
    __radd__=__add__
    def __neg__(self):
        return E([-a for a in self.v])
    def __sub__(self,other):
        return self+-E(other)
    def __rsub__(self,other):
        return E(other)+-self
    def __mul__(self,other):
        other=E(other);a=[Q(0)]*23
        for j,x in enumerate(self.v):
            if not x:continue
            for k,y in enumerate(other.v):
                if y:a[j+k]+=x*y
        return E(a)
    __rmul__=__mul__
    def inverse(self):
        need(bool(self),'zero field inverse')
        a=[Q(0)]*13;a[0]=Q(1);a[6]=Q(-1);a[12]=Q(1)
        b=strip(self.v);s0=[];s1=[Q(1)]
        while b:
            q,r=pdiv(a,b);a,b=b,r;s0,s1=s1,psub(s0,pmul(q,s1))
        need(len(a)==1,'Phi36 field gcd')
        answer=E([x/a[0]for x in s0])
        need(answer*self==1,'field inverse identity')
        return answer
    def __truediv__(self,other):
        return self*E(other).inverse()
    def __rtruediv__(self,other):
        return E(other)*self.inverse()
    def __pow__(self,n):
        if n<0:return self.inverse()**(-n)
        a=E(1);b=self
        while n:
            if n%2:a=a*b
            n//=2
            if n:b=b*b
        return a
    def conjugate(self):
        answer=E(0)
        for j,v in enumerate(self.v):
            if v:answer=answer+v*CONJ[j]
        return answer
    def real(self):
        return (self+self.conjugate())*Q(1,2)
    def imag(self):
        return (self-self.conjugate())/(2*I)
    def record(self):
        return [str(v)for v in self.v]


Z=E([0,1])
I=Z**9
W=Z**4
CONJ=[Z**((-j)%36)for j in range(12)]
C=(Z**2+Z**34)*Q(1,2)
need(Z**36==1 and Z**12-Z**6+1==0,'primitive field relation')
need(I*I==-1 and W**9==1 and W**3!=1,'complex and ninth-root generators')
need(8*C**3-6*C-1==0 and C.conjugate()==C,'physical cosine relation')
