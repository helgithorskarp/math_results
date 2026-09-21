"""Exact common similarity multipliers for finite rational binary-form lists."""
from fractions import Fraction as F
from math import isqrt, lcm


def require(ok, msg):
    if not ok: raise ValueError(msg)


def rational(x):
    require(isinstance(x, (int,str,F)) and not isinstance(x,bool), 'exact rational input required')
    return F(x)


def square_root(x):
    x=F(x)
    if x<0:return None
    a,b=isqrt(x.numerator),isqrt(x.denominator)
    return F(a,b) if a*a==x.numerator and b*b==x.denominator else None


def mask_products(rad):
    out=[1]
    for r in rad:out += [r*x for x in out]
    return out


def locate_class(r, rad):
    for mask,v in enumerate(mask_products(rad)):
        z=square_root(F(v,r))
        if z is not None:return mask,z
    return None


def basis_for(determinants):
    rad=[]
    for d in determinants:
        r=-d.numerator*d.denominator
        if locate_class(r,rad) is None:rad.append(r)
    return rad


class Field:
    """Basis e_mask=product sqrt(rad[j]); rad are independent square classes."""
    def __init__(self,rad):
        self.rad=list(rad);self.n=1<<len(rad);prior=[]
        for r in rad:
            require(isinstance(r,int) and r<0,'negative integer radicand required')
            require(locate_class(r,prior) is None,'dependent square classes')
            prior.append(r)
        self.prod=mask_products(rad)
    def scalar(self,c):return (F(c),)+(F(0),)*(self.n-1)
    def add(self,a,b):return tuple(x+y for x,y in zip(a,b))
    def mul(self,a,b):
        out=[F(0)]*self.n
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):
                    if y:out[i^j]+=x*y*self.prod[i&j]
        return tuple(out)
    def linear_factor(self,t,sign):
        out=list(self.scalar(t))
        for j in range(len(self.rad)):out[1<<j]=F(1 if sign&(1<<j) else -1)
        return tuple(out)
    def norm_polynomial(self):
        coeff=[self.scalar(1)]
        for sign in range(self.n):
            root=self.linear_factor(0,sign);out=[self.scalar(0)]*(len(coeff)+1)
            for i,c in enumerate(coeff):
                out[i]=self.add(out[i],self.mul(c,root));out[i+1]=self.add(out[i+1],c)
            coeff=out
        require(all(not any(c[1:]) and c[0].denominator==1 for c in coeff),'nonintegral norm polynomial')
        return [c[0] for c in coeff]
    def relative_norm(self,t,mask):
        require(0<mask<self.n,'nontrivial quadratic subfield required')
        out=self.scalar(1)
        for sign in range(self.n):
            if (sign&mask).bit_count()%2==0:out=self.mul(out,self.linear_factor(t,sign))
        require(all(not c for j,c in enumerate(out) if j not in (0,mask)),'relative norm outside fixed field')
        return out[0],out[mask]


def poly_mul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out


def poly_value(a,t):
    out=F(0)
    for c in reversed(a):out=out*t+c
    return out


def nonsquare_threshold(poly):
    p=list(map(F,poly));degree=len(p)-1
    require(degree>=2 and degree%2==0 and p[-1]==1,'monic positive even degree required')
    require(all(c.denominator==1 for c in p),'integral coefficients required')
    m=degree//2;q=[F(0)]*m+[F(1)]
    for j in range(m-1,-1,-1):q[j]=(p[m+j]-poly_mul(q,q)[m+j])/2
    rem=[a-b for a,b in zip(p,poly_mul(q,q))]
    while rem and not rem[-1]:rem.pop()
    require(rem and len(rem)<=m,'polynomial is a square or square-part construction failed')
    den=lcm(*(x.denominator for x in q));a=sum(abs(x) for x in q[:-1]);c=sum(abs(x) for x in rem)
    root_bound=1+sum(abs(x) for x in rem[:-1])/abs(rem[-1])
    bound=max(F(1),2*a,2*den*c,root_bound)
    threshold=bound.numerator//bound.denominator+1
    return {'square_part':q,'remainder':rem,'denominator':den,'threshold':threshold}


def matmul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):return [list(x) for x in zip(*a)]


def validate_form(g):
    require(len(g)==2 and all(len(row)==2 for row in g),'2x2 form required')
    g=[[rational(x) for x in row] for row in g]
    require(g[0][1]==g[1][0],'symmetric form required')
    d=g[0][0]*g[1][1]-g[0][1]**2
    require(g[0][0]>0 and d>0,'positive definite form required')
    return g,d


def similarity(g,d,u,v):
    a,b=g[0];C=[[F(1),b/a],[F(0),1/a]];Ci=[[F(1),-b],[F(0),a]]
    T=[[u,-d*v],[v,u]]
    return matmul(matmul(Ci,T),C)


def construct(forms,epsilon=F(1,1000)):
    epsilon=rational(epsilon);require(epsilon>0,'positive epsilon required')
    checked=[validate_form(g) for g in forms];dets=[d for _,d in checked]
    rad=basis_for(dets) if dets else [-1]
    field=Field(rad);polynomial=field.norm_polynomial();cert=nonsquare_threshold(polynomial)
    t=cert['threshold'];alpha=poly_value(polynomial,t)
    require(alpha>0 and alpha.denominator==1 and square_root(alpha) is None,'not a positive nonsquare integer')
    norms=[]
    for g,d in checked:
        r=-d.numerator*d.denominator;mask,z=locate_class(r,rad)
        u,c=field.relative_norm(t,mask);v=c*z*d.denominator
        require(u*u+d*v*v==alpha,'relative norm mismatch')
        S=similarity(g,d,u,v)
        require(matmul(matmul(transpose(S),g),S)==[[alpha*x for x in row] for row in g],'similitude identity failed')
        norms.append({'determinant':d,'subfield_mask':mask,'u':u,'v':v,'matrix':S})
    n=1
    while True:
        a=isqrt(alpha.numerator*n*n)
        if a and F(1,a)<epsilon:break
        n*=2
    q=F(n,a);scaled=alpha*q*q
    require(1<scaled<(1+epsilon)**2 and square_root(scaled) is None,'near-identity scaling failed')
    for rec,(g,d) in zip(norms,checked):
        S=[[q*x for x in row] for row in rec['matrix']]
        require(matmul(matmul(transpose(S),g),S)==[[scaled*x for x in row] for row in g],'scaled similitude failed')
        rec['near_identity_matrix']=S
    return {'radicands':rad,'field_degree':field.n,'norm_polynomial':polynomial,
            'nonsquare_certificate':cert,'t':t,'common_integer':alpha,
            'near_identity_rational_factor':q,'squared_scale':scaled,'epsilon':epsilon,'forms':norms}
