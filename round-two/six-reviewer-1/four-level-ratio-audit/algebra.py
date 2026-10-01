"""Independent original diagonal-resolvent reconstruction; SymPy1.14 QQ rings.
No researcher module imports. All variables, divisions and signs explicit.
"""
import sympy
from sympy.polys.rings import ring
from fractions import Fraction as Q
from math import gcd,lcm
from itertools import permutations

def need(ok,label):
    if not ok:raise ValueError(label)
def add(a,b):
    zero=a[0]*0 if a else b[0]*0
    return [(a[i] if i<len(a) else zero)+(b[i] if i<len(b) else zero) for i in range(max(len(a),len(b)))]
def mul(a,b):
    out=[a[0]*0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out
def power(a,n):
    out=[a[0]*0+1]
    for _ in range(n):out=mul(out,a)
    return out
def trim(a):
    a=list(a)
    while len(a)>1 and not a[-1]:a.pop()
    return a
def divmonic(a,b):
    need(b[-1]==1,'monic coefficient divisor')
    a=list(a);q=[b[0]*0]*max(1,len(a)-len(b)+1)
    for j in range(len(a)-len(b),-1,-1):
        c=a[j+len(b)-1];q[j]=c
        for k,v in enumerate(b):a[j+k]-=c*v
    return trim(q),trim(a[:len(b)-1] or [b[0]*0])
def mod(a,h):return divmonic(a,h)[1]+[h[0]*0]*max(0,len(h)-1-len(divmonic(a,h)[1]))
def mm(a,b,h):return mod(mul(a,b),h)
def matrix_multiplier(a,h):
    n=len(h)-1;cols=[]
    for j in range(n):cols.append(mod([h[0]*0]*j+a,h))
    return [[cols[j][i] for j in range(n)] for i in range(n)]
def det(matrix):
    n=len(matrix);out=matrix[0][0]*0
    for p in permutations(range(n)):
        sign=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=sign
        for i in range(n):term*=matrix[i][p[i]]
        out+=term
    return out
def adj3(matrix):
    out=[]
    for i in range(3):
        row=[]
        for j in range(3):
            rs=[k for k in range(3) if k!=j];cs=[k for k in range(3) if k!=i]
            row.append((-1)**(i+j)*(matrix[rs[0]][cs[0]]*matrix[rs[1]][cs[1]]-matrix[rs[0]][cs[1]]*matrix[rs[1]][cs[0]]))
        out.append(row)
    return out
def moments(f,kmax):
    n=len(f)-1;need(f[-1]==1,'monic original root polynomial');p=[f[0]*0+n]
    for k in range(1,kmax+1):
        p.append(-k*f[n-k]-sum(f[n-j]*p[k-j] for j in range(1,k)))
    return p
def primitive(p):
    den=lcm(*(Q(str(x)).denominator for x in p.values()));g=gcd(*(int(Q(str(x))*den) for x in p.values()))
    need(g>0,'positive primitive content');return p*(Q(den,g)),Q(den,g)
def normalize(n,d):
    vals=[Q(str(x)) for p in (n,d) for x in p.values()];den=lcm(*(x.denominator for x in vals));g=gcd(*(int(x*den) for x in vals))
    scale=Q(den,g);return n*scale,d*scale,scale
def residue_kernel(f,inactive,ell):
    """u'(z-H)^-1u=8z-64f/f'=8z-8ell/h; residue=-8ell/h'."""
    derivative=[i*f[i]/8 for i in range(1,len(f))]
    h,remainder=divmonic(derivative,inactive)
    need(not any(remainder),'full original derivative/inactive factor division')
    need(len(h)==4 and h[-1]==1,'active cubic degree')
    need(mul(inactive,h)==derivative,'exact full derivative factorization')
    _,ellrem=divmonic(ell,h)
    hp=[h[1],2*h[2],h[3]*3];M=matrix_multiplier(hp,h);delta=det(M);adj=adj3(M)
    numerator=mod([-8*x for x in ellrem],h)
    R=[sum(adj[i][j]*numerator[j] for j in range(3)) for i in range(3)]
    need(mm(hp,R,h)==[delta*x for x in numerator],'inverse quotient residue identity')
    squared=mm(R,R,h);trace=squared[0]*3-squared[1]*h[2]+squared[2]*(h[2]*h[2]-2*h[1])
    p=moments(f,4);N,S3,S4=p[2:5];m2=S4-N*N/8
    # delta=product h'(lambda_i)=-discriminant(h). Cancel this explicitly,
    # then choose -delta as the positive discriminant on real simple cubics.
    num=-(N*N*delta*delta-trace).exquo(delta);den=-m2*delta
    n,d,scale=normalize(num,den)
    return dict(f=f,h=h,N=N,S3=S3,S4=S4,m2=m2,discriminant=-delta,n=n,d=d,scale=scale,residue_numerator=R)
def family(name):
    r,x,V=ring('x,V',sympy.QQ);one=r.one
    if name=='321':
        A=[-x,one];B=[1-V,2*one,one];S=[3*x-4,one]
        f=mul(mul(power(A,3),power(B,2)),S);inactive=mul(power(A,2),B);ell=mul(mul(A,B),S)
    elif name=='421':
        A=[-one,one];B=[-x,one];S=[(2+x)**2-V,2*(2+x),one]
        f=mul(mul(power(A,4),power(B,2)),S);inactive=mul(power(A,3),B);ell=mul(mul(A,B),S)
    else:raise ValueError('unknown original family')
    out=residue_kernel(f,inactive,ell);out['ring']=r
    return out
def paired():
    r,A,T,B=ring('A,T,B',sympy.QQ);g=[B,-T,-A,r.zero,r.one];f=power(g,2)
    out=residue_kernel(f,g,g);out.update(ring=r,A=A,T=T,B=B,g=g);return out
def encode(p):return [[list(k),str(Q(str(v)))] for k,v in sorted(p.items())]
