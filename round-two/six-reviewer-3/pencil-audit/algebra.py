"""Independent residue Gram solve and complete coefficient case audit over Q."""
from fractions import Fraction as F
from polys import Poly, cast, symbol, need

Z=cast(0)

def trim(p):
    p=list(p)
    while p and p[-1]==0:p.pop()
    return p

def coeff(p,k):return p[k] if k<len(p) else Z
def add(a,b):return trim([coeff(a,i)+coeff(b,i) for i in range(max(len(a),len(b)))])
def scale(a,c):return trim([x*c for x in a])
def neg(a):return scale(a,-1)
def mul(a,b):
    out=[Z]*(max(0,len(a)+len(b)-1))
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]=out[i+j]+x*y
    return trim(out)
def deriv(p):return trim([p[i]*i for i in range(1,len(p))])
def divrem(p,h):
    p=trim(p);h=trim(h);need(h and h[-1]==1,'monic divisor')
    q=[Z]*max(0,len(p)-len(h)+1)
    while len(p)>=len(h):
        j=len(p)-len(h);t=p[-1];q[j]=q[j]+t
        for k,x in enumerate(h):p[j+k]=p[j+k]-t*x
        p=trim(p)
    return trim(q),p
def rem(p,h):return divrem(p,h)[1]
def same(a,b):return trim(a)==trim(b)
def specialize(p,m):return trim([x.substitute(m) for x in p])
def record(p):return [x.record() for x in trim(p)]
def power_sums(h,count):
    n=len(h)-1;out=[cast(n)]
    for k in range(1,count+1):
        v=Z
        for j in range(1,min(k,n)+1):
            v=v+coeff(h,n-j)*(k if j==k else out[k-j])
        out.append(-v)
    return out

def gram_adjoint(h):
    """Solve G*T=D^t*G by anti-triangular unit pivots; no node inverse."""
    n=len(h)-1;rs=[];r=[cast(1)]
    for k in range(2*n-1):
        rs.append(coeff(r,n-1));r=rem([Z]+r,h)
    G=[[rs[i+j] for j in range(n)] for i in range(n)]
    cols=[]
    for i in range(n):
        rhs=[Z]+[G[j-1][i]*j for j in range(1,n)];x=[Z]*n
        for row in range(n):
            col=n-1-row;need(G[row][col]==1,'unit anti-diagonal pivot')
            need(all(G[row][j]==0 for j in range(col)),'zero anti-triangle')
            x[col]=rhs[row]-sum((G[row][j]*x[j] for j in range(col+1,n)),Z)
        cols.append(trim(x))
    def T(p):
        need(len(trim(p))<=n,'normal representative before adjoint')
        out=[]
        for i,x in enumerate(p):out=add(out,scale(cols[i],x))
        return out
    return G,cols,T

def structures():
    A,B,E,Fc,G,J,C,N,t,d=[symbol(x) for x in ('A','B','E','F','G','J','C','N','t','d')]
    h=[J,G,Fc,E,B,A,Z,cast(1)]
    f=[symbol('f0'),8*J,4*G,F(8,3)*Fc,2*E,F(8,5)*B,F(4,3)*A,Z,cast(1)]
    p=[symbol('p'+str(i)) for i in range(7)]
    Q,_=divrem(add(scale(f,8),mul(p,deriv(h))),h)
    gram,cols,T=gram_adjoint(h)
    K=add(scale(p,-16),add(scale(T(T(rem(mul(p,p),h))),-F(1,4)),scale(T(rem(mul(p,add(Q,neg(deriv(p)))),h)),F(1,4))))
    O=add(mul(p,deriv(deriv(h))),add(mul(add(deriv(p),neg(Q)),deriv(h)),mul(add([cast(64)],neg(deriv(Q))),h)))
    return locals()
