"""Whole finite-eta critical products and a separate moving-unit-root expansion.

These exact positive-eta controls corroborate the universal identities proved
in PROOF.md; finite samples are not a replacement for those identities.
"""
from fractions import Fraction as F
from sector import K,require,anchored,correction_poly
from series import series_ring
from centered import forcing


def gaussian_ring(Base):
    class G:
        def __init__(self,re=0,im=0):
            if isinstance(re,G): self.re,self.im=re.re,re.im
            else: self.re,self.im=Base(re),Base(im)
        def __add__(self,b):
            b=G(b);return G(self.re+b.re,self.im+b.im)
        __radd__=__add__
        def __neg__(self):return G(-self.re,-self.im)
        def __sub__(self,b):return self+-G(b)
        def __mul__(self,b):
            b=G(b);return G(self.re*b.re-self.im*b.im,self.re*b.im+self.im*b.re)
        __rmul__=__mul__
        def __pow__(self,n):
            require(type(n)is int and n>=0,'Gaussian nonnegative power');out=G(1)
            for _ in range(n):out*=self
            return out
        def __eq__(self,b):
            b=G(b);return self.re==b.re and self.im==b.im
    return G


def multiply(a,b):
    G=type(a[0]);out=[G(0)]*(len(a)+len(b)-1)
    for j,v in enumerate(a):
        for k,w in enumerate(b):out[j+k]+=v*w
    return out


def factor_primitive(roots,a):
    G=type(roots[0]);p=[G(1)]
    for root in roots:p=multiply(p,[-root,G(1)])
    primitive=[G(0)]+[v*F(9,j+1) for j,v in enumerate(p)]
    primitive[0]=-sum((v*a**j for j,v in enumerate(primitive[1:],1)),G(0))
    return primitive


def evaluate(poly,z):
    G=type(z);out=G(0)
    for v in reversed(poly):out=out*z+v
    return out


def derivative(poly):return [v*(j+1) for j,v in enumerate(poly[1:])]


def audit(damage=None):
    D=series_ring(2,K);G=gaussian_ring(D);GK=gaussian_ring(K)
    delta=D([0,1]);count=0;records=[]
    def check(ok,label):
        nonlocal count
        require(ok,label);count+=1
    for epsilon in (F(1,16),F(1,12),F(1,8)):
        eta=epsilon*epsilon;a=1-eta
        x,y,q0=F(-2,3),F(1,2),F(5,4);T=q0*q0
        V,M=F(7,5),F(-2,7);r=eta*x;s=eta*y
        values=[K(v) for v in (x,y,T,F(-1,6),F(1,3),F(-3,4))]
        qV=anchored([(8,K(-F(9,8))),(7,K(-F(9,7)*(r-2*s)))],K(r),K(a))
        qM=anchored([(7,K(-F(9,7)))],K(r),K(a))
        qd=anchored([(6,K(-9*(T+eta*(x-y)**2)))],K(r),K(a))
        if damage=='odd-primitive':qV[8]*=2
        # Literal heavy critical factors independently retain the square root
        # and asymmetry. The degree-two series for sqrt is exact in this ring.
        for label,v1,m1,small in (('V',1,0,False),('M',0,1,False),('common',V,M,True)):
            mh=delta*(eta*v1/2-(3 if small else 0))
            nn=delta*((m1-eta*v1*y+(6*(y-x) if small else 0))/2)
            sh=D(q0)*(1-mh*mh/(2*T));du=nn/sh
            h1,h2=mh+sh,mh-sh;u1,u2=D(y)+du,D(y)-du
            roots=[G(D(eta)*u1,D(epsilon)*h1),G(D(eta)*u2,D(epsilon)*h2)]
            roots += [G(r,delta*(epsilon if small else 0))]*6
            p=factor_primitive(roots,D(a))
            wanted=[qV[j]*v1+qM[j]*m1+(qd[j] if small else 0) for j in range(10)]
            check(all(p[j].re.a[1]==0 and p[j].im.a[1]==epsilon**3*wanted[j] for j in range(10)),
                  'all ten odd primitive coefficients '+label)
            check(evaluate(p,G(D(a)))==0,'whole marked-root anchor '+label)
            check(h1+h2==2*mh and h1*h1+h2*h2==2*T and u1+u2==2*y
                  and h1*u1+h2*u2==2*mh*y+2*nn,'all four literal pair moment identities '+label)
            if not small:continue
            corr,n=correction_poly(K(eta),values,K(V),K(M))
            _,split=forcing(K(eta),values,K(F(15,16)));split+= [K(0)]*(10-len(split))
            if damage=='common-second-primitive':corr[6]+=1
            P2=[-3*eta*split[j]+eta*eta*corr[j] for j in range(10)]
            check(all(p[j].re.a[2]==P2[j] and p[j].im.a[2]==0 for j in range(10)),
                  'all ten common second primitive coefficients')
            # Independent Taylor composition at a rational point on the circle;
            # b is arbitrary, so this checks the universal chain rule including
            # the unit-circle radial acceleration, not a fitted root motion.
            z0=GK(F(3,5),F(4,5));b=K(F(7,6))
            z=G(D(z0.re),D(z0.im))*(G(1)+G(0,delta*(-epsilon**3)*b)+G(delta*delta*(-epsilon**6/2)*b*b))
            check(z.re*z.re+z.im*z.im==1,'whole moving unit-root modulus through delta squared')
            actual=evaluate(p,z);literal=GK(actual.re.a[2],actual.im.a[2])
            p0=[K(v.re.a[0]) for v in p];qp=derivative(wanted)
            pz=evaluate(derivative(p0),z0);pzz=evaluate(derivative(derivative(p0)),z0)
            correction=z0*evaluate(qp,z0)*b-(z0*pz+z0*z0*pzz)*(b*b/2)
            if damage=='root-radial-acceleration':correction=z0*evaluate(qp,z0)*b-z0*z0*pzz*(b*b/2)
            check(literal==evaluate(P2,z0)+correction*epsilon**6,'complete moving-unit-root second response')
            # Expand the two actual heavy distances, normalized by their common
            # positive squared base. No exact square root of that base is needed.
            mean2=K((a-s)**2+eta*T)
            def normalized_inverse_root(squared):
                shift=squared/mean2-1
                return 1-shift/2+F(3,8)*shift*shift
            dist=[]
            for root in roots[:2]:dist.append((D(a)-root.re)**2+root.im**2)
            literal_cost=(normalized_inverse_root(dist[0])+normalized_inverse_root(dist[1])).a[2]/(eta*eta)
            mh1=K(eta*V/2-3);DD=K(a-s)
            variance=2 if damage=='heavy-distance-variance' else 3
            expected=-n*n/(T*mean2)+variance*(mh1*T-DD*n)**2/(T*mean2*mean2)
            check(literal_cost==expected,'whole two-heavy-distance second coefficient')
            check(all(p[j].re.a[0]==p0[j] for j in range(10)),'whole common base coefficient list')
            records.append({'eta':str(eta),'common_first_primitive':[v.record() for v in wanted],
                            'common_second_primitive':[v.record() for v in P2],
                            'moving_unit_second':{'re':literal.re.record(),'im':literal.im.record()},
                            'normalized_heavy_cost':literal_cost.record()})
        pair=factor_primitive([G(r,delta*epsilon),G(r,-delta*epsilon)]+[G(r)]*4+
                             [G(s,epsilon*q0),G(s,-epsilon*q0)],D(a))
        _,split=forcing(K(eta),values,K(F(15,16)));split +=[K(0)]*(10-len(split))
        if damage=='paired-forcing':split[7]=-split[7]
        if damage=='paired-anchor':split[0]+=F(1,1000)
        check(all(pair[j].re.a[2]==-eta*split[j] and pair[j].im.a[2]==0 and
                  pair[j].re.a[1]==pair[j].im.a[1]==0 for j in range(10)),
              'all ten centered imaginary-pair forcing coefficients')
    # Exact zero-eta rows and common response, regenerated in the cubic field.
    c=K((0,1,0));O=[[K(F(1,8)),K(-F(1,7))],[K(F(1,8)),-2*c/7]]
    det=O[0][0]*O[1][1]-O[0][1]*O[1][0]
    check(det==(1-2*c)/56,'complete initial odd determinant')
    for t,row in zip((K(-F(1,2)),-c),O):
        u=[K(1),2*t]
        for _ in range(2,8):u.append(2*t*u[-1]-u[-2])
        check(row==[-u[7]/8,-u[6]/7],'both complete initial odd rows from Chebyshev')
        T=K(F(7,6));V=8*(2*c+1)*T;M=7*(2*c+1)*T
        check(row[0]*V+row[1]*M-T*u[5]==0,'both common initial odd response equations')
    return {'exact_identity_controls':count,'positive_eta_whole_records':records,
            'initial_odd_matrix':[[v.record() for v in row] for row in O],
            'initial_odd_determinant':det.record()}
