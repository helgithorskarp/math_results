"""Exact quotient arithmetic with certified rational root-interval signs."""
from fractions import Fraction
from math import lcm


def trim(p):
    p=list(p)
    while p and not p[-1]:p.pop()
    return tuple(p)


def add(p,q):
    return trim([(p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0)
                 for i in range(max(len(p),len(q)))])


def scale(p,c):
    return trim([x*c for x in p])


def multiply(p,q):
    if not p or not q:return ()
    out=[Fraction(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]+=x*y
    return trim(out)


def divrem(p,q):
    if not q:raise ValueError('zero polynomial divisor')
    r=list(p);out=[Fraction(0)]*max(0,len(p)-len(q)+1)
    while r and len(r)>=len(q):
        shift=len(r)-len(q);c=r[-1]/q[-1];out[shift]=c
        for i,x in enumerate(q):r[shift+i]-=c*x
        r=list(trim(r))
    return trim(out),trim(r)


class Field:
    def __init__(self,polynomial,bracket):
        self.polynomial=tuple(map(Fraction,polynomial))
        self.lo,self.hi=(Fraction(*x) for x in bracket)
        self.degree=len(polynomial)-1
        self.zero=()
        self.one=(Fraction(1),)
        self.t=(Fraction(0),Fraction(1))

    def element(self,p):
        return divrem(tuple(map(Fraction,p)),self.polynomial)[1]

    def number(self,n):
        return self.element((n,))

    def add(self,p,q):return add(p,q)
    def neg(self,p):return scale(p,-1)
    def sub(self,p,q):return add(p,scale(q,-1))
    def mul(self,p,q):return divrem(multiply(p,q),self.polynomial)[1]

    def inv(self,p):
        if not p:raise ValueError('zero field inverse')
        a,b=self.polynomial,p
        x,y=(),self.one
        while b:
            q,r=divrem(a,b)
            a,b=b,r
            x,y=y,add(x,scale(multiply(q,y),-1))
        if len(a)!=1:raise ValueError('noninvertible quotient element')
        return self.element(scale(x,1/a[0]))

    def div(self,p,q):return self.mul(p,self.inv(q))

    def from_rat(self,r):
        return self.div(self.element(r['num']),self.element(r['den']))

    def interval(self,p):
        lo=hi=Fraction(0)
        for c in reversed(p):
            v=(lo*self.lo,lo*self.hi,hi*self.lo,hi*self.hi)
            lo,hi=min(v)+c,max(v)+c
        return lo,hi

    def sign(self,p):
        if not p:return 0
        lo,hi=self.interval(p)
        if lo>0:return 1
        if hi<0:return -1
        raise ValueError('root interval sign unresolved')

    def det3(self,m):
        return self.add(self.sub(self.mul(m[0][0],self.sub(self.mul(m[1][1],m[2][2]),self.mul(m[1][2],m[2][1]))),
                                 self.mul(m[0][1],self.sub(self.mul(m[1][0],m[2][2]),self.mul(m[1][2],m[2][0])))),
                        self.mul(m[0][2],self.sub(self.mul(m[1][0],m[2][1]),self.mul(m[1][1],m[2][0]))))

    def solve3(self,m,rhs):
        d=self.det3(m)
        if not d:return None
        inv=self.inv(d)
        return tuple(self.mul(self.det3([[rhs[i] if j==k else m[i][j] for j in range(3)] for i in range(3)]),inv)
                     for k in range(3))

    def dot(self,x,y):
        total=self.zero
        for i in range(3):
            for j in range(3):
                total=self.add(total,self.mul(self.mul(x[i],y[j]),self.one if i==j else self.t))
        return total

    def encode(self,p):
        denominator=lcm(*(x.denominator for x in p)) if p else 1
        return {'num':[int(x*denominator) for x in p],'den':denominator}


def selftest():
    f=Field((-1,0,3),((57735,100000),(57736,100000)))
    if f.mul(f.t,f.t)!=f.number(Fraction(1,3)):raise ValueError('quadratic reduction')
    if f.mul(f.t,f.inv(f.t))!=f.one:raise ValueError('inverse identity')
    if f.sign(f.sub(f.t,f.number(Fraction(1,2))))!=1:raise ValueError('root sign')
    if f.solve3([[f.one,f.zero,f.zero],[f.zero,f.one,f.zero],[f.zero,f.zero,f.one]],[f.t,f.one,f.zero])!=(f.t,f.one,f.zero):
        raise ValueError('linear solve')


if __name__=='__main__':
    selftest()
    print('exact field controls passed')
