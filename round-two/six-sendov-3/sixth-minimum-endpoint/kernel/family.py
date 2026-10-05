"""Literal mixed mean/skew family; six-sendov-3, ordinary author work.

Same-author10212/10280 lower coefficients are openly reused.
Kronecker32u+v is injective because every t factor costs epsilon degree.
"""
import series as s
import constants as m
from arithmetic import F, need
t={1:s.ar.N1};mu={32:s.ar.N1}
f=lambda a,b=0,d=0:s.const(s.fcf(a,b,d))
NU4=f(F(-2424695,13122),F(-136157,4374),F(144046,6561))
SIGMA4=f(F(-536333191,1119744),F(-805399537,559872),F(891296017,559872))
DELTA_M3=f(0,F(56,9),F(-56,9))
DELTA_B2=f(F(1,2),2)
DELTA_M4=f(F(-51583,972),F(-175385,486),448)
DELTA_B3=f(F(1771,324),F(-94039,1296),F(12347,162))
DELTA_B3Q=s.ns(s.na(s.N1,s.c),F(2,7))
SIGMA7=f(F(-2,49),F(-4,49),F(-2,49))
NU9=f(F(-35,81),F(-29,27),F(-34,81))
SIGMA9=f(F(-34849,42336),F(-41053,21168),F(-3265,2646))

def symbolic_repairs(r):
    """Literal credited 10212 shrinking-family lower repairs."""
    center=s.na(s.C['m3'],s.nm(f(F(35,81),F(-2086,81),F(616,27)),s.np(r,2)))
    beta=s.na(s.C['Gamma2'],s.nm(f(F(14537,1512),F(-3889,756),F(-1661,756)),s.np(r,2)),
              s.nm(f(F(-2,49),F(-4,49),F(-2,49)),s.np(r,4)))
    nu=s.na(s.nm(f(F(-17983,972),F(-25711,486),F(4564,81)),r),
            s.nm(f(F(28,81),F(56,81)),s.np(r,3)))
    sigma=s.na(s.nm(f(F(-1967,81),F(5479,432),F(-5375,162)),r),
               s.nm(f(F(-55,189),F(11,63),F(88,189)),s.np(r,3)))
    return center,beta,nu,sigma

def parts(joint=True):
    r={1:s.ar.N1};rinv=s.ni(s.ns(s.H,3));order=9
    center,beta,nu,sigma=symbolic_repairs(r)
    def sub(z,e):
        out={}
        for index,p in enumerate(z):
            for power,a in p.items():
                if e+power>order:continue
                g=[s.N0,s.N0];g[index]={power:s.ar.nm(a,s.np(rinv,power)[0])}
                out=s.pa(out,{(e+power,0):tuple(g)})
        return out
    q1=s.na(s.gamma,s.ns(s.nm(s.np(r,2),s.ni(s.H)),F(-4,3)))
    v2=s.ns(s.nm(s.nm(s.k,s.H),r),F(3,7))
    A=s.pa(sub((s.uz,s.ns(r,F(-1,3))),2),sub((s.w2,v2),4),
           sub((center,nu),6),sub((m.Mstar,s.nm(NU4,r)),8),{(9,0):s.G1})
    B=s.pa(sub((s.up,r),2),sub((s.w2,v2),4),
           sub((center,nu),6),sub((m.Mstar,s.nm(NU4,r)),8),{(9,0):s.G1})
    K=s.pa({(0,0):(s.N0,s.N1)},sub((s.nm(s.d,r),q1),2),sub((sigma,beta),4),
           sub((s.nm(SIGMA4,r),m.betastar),6))
    if joint:
        A=s.pa(A,{(4,0):s.gf(s.ns(mu,F(-1,3))),(6,0):s.gf(s.nm(DELTA_M3,mu)),
                  (8,0):s.gf(s.nm(DELTA_M4,mu))})
        B=s.pa(B,{(4,0):s.gf(mu),(6,0):s.gf(s.nm(DELTA_M3,mu)),
                  (8,0):s.gf(s.nm(DELTA_M4,mu))})
        K=s.pa(K,{(4,0):(s.N0,s.nm(DELTA_B2,mu)),
                  (6,0):(s.N0,s.na(s.nm(DELTA_B3,mu),s.nm(DELTA_B3Q,s.np(mu,2))))})
    return A,B,K

def add_odd(parts,degree,nu,sigma):
    A,B,K=parts
    return (s.pa(A,{(degree,0):(s.N0,nu)}),
            s.pa(B,{(degree,0):(s.N0,nu)}),
            s.pa(K,{(degree-2,0):s.gf(sigma)}))

def sinpart(j):
    return s.ns(s.na(s.np(s.WW,j%9),s.ns(s.np(s.WW,(-j)%9),-1)),F(-1,2))

ODD=[(sinpart(j),s.ns(s.nm(s.H,sinpart(2*j)),F(1,7))) for j in range(9)]
def repair(q3,q4):
    need(q3[0]==s.N0 and q4[0]==s.N0,'forcing pure Gaussian second component')
    a,b=ODD[3];c,d=ODD[4]
    det=s.na(s.nm(a,d),s.ns(s.nm(c,b),-1))
    nu=s.nm(s.na(s.ns(s.nm(q3[1],d),-1),s.nm(q4[1],b)),s.ni(det))
    sigma=s.nm(s.na(s.ns(s.nm(a,q4[1]),-1),s.nm(c,q3[1])),s.ni(det))
    # Repairs themselves must be physically real on every coefficient.
    s.rpoly(nu);s.rpoly(sigma)
    return nu,sigma

def projection(g,axis):
    out=[]
    for p in g:
        if axis=='mu0':out.append({n:a for n,a in p.items() if n<32})
        elif axis=='t0':out.append({n//32:a for n,a in p.items() if n%32==0})
        else:raise ValueError(axis)
    return tuple(out)

def encoded_parts(parts):
    return [[[list(key),s.encoded_g(g)] for key,g in sorted(p.items())] for p in parts]
def closed_parts(damage=None):
    ps=parts()
    product=s.nm(mu,t)
    sigma7=s.nm(SIGMA7,product)
    nu9=s.nm(NU9,product);sigma9=s.nm(SIGMA9,product)
    if damage=='omit_seventh':sigma7=s.N0
    if damage=='omit_ninth_center':nu9=s.N0
    if damage=='omit_ninth_scale':sigma9=s.N0
    ps=add_odd(ps,7,s.N0,sigma7)
    ps=add_odd(ps,9,nu9,sigma9)
    if damage=='outward_ninth':
        A,B,K=ps
        ps=s.pa(A,{(9,0):s.gs(s.G1,-2)}),s.pa(B,{(9,0):s.gs(s.G1,-2)}),K
    return ps

def signs_and_motion(roots,ids,damage=None):
    # Exact physical embedding and rational polynomial signs, not decimals.
    cubic=lambda z:8*z**3-6*z-1
    lo,hi=F(15,16),F(47,50)
    need(cubic(lo)<0<cubic(hi) and 24*lo**2-6>0,'physical unique cosine bracket')
    for _ in range(40):
        mid=(lo+hi)/2
        if cubic(mid)<0:lo=mid
        else:hi=mid
    signs=[]
    def positive(name,z):
        need(set(z)=={0},'constant physical sign '+name)
        coefficients=list(map(F,s.field_real_form(s.fc,z[0])))
        lower=upper=F(0)
        for a in reversed(coefficients):
            corners=(lower*lo,lower*hi,upper*lo,upper*hi)
            lower,upper=min(corners)+a,max(corners)+a
        need(lower>0,'whole rational positive '+name)
        signs.append({'name':name,'whole_cubic':[str(a) for a in coefficients],
                      'lower':str(lower),'upper':str(upper)})
    for name,z in [('H',s.H),('kappa',s.kappa),('minus_Gmean',s.ns(m.Gmean,-1)),
                   ('strict_G_improvement',m.IMPROVEMENT),('mu_star_positive',m.MUstar),
                   ('minus_Gstar',s.ns(m.Gstar,-1)),('odd_divisor',s.ns(s.nm(s.H,s.na(s.ns(s.c,2),s.ns(s.N1,-1))),F(1,7))),
                   ('motion_A',s.C['motion_A']),('motion_B_over_positive_sin',s.C['motion_B_over_sin']),
                   ('motion_Q',s.C['motion_q2'])]:positive(name,z)
    ideal=[]
    for j,row in enumerate(roots):
        omega=s.np(s.WW,j)
        Lj=s.na(s.ns(omega,F(-1,3)),s.ns(s.C['x'],-1),s.ns(s.nm(s.C['y'],s.np(s.WW,(-j)%9)),-1))
        Wj=s.ns(s.na(s.nm(s.na(s.ns(s.N1,3),s.ns(s.c,4)),omega),
                    s.ns(s.nm(s.na(s.N1,s.ns(s.c,2)),s.na(s.N1,s.np(s.WW,(-j)%9))),-1),
                    s.ns(s.np(s.WW,(-2*j)%9),-1)),F(1,18))
        dj=row['root'][4]
        need(all(set(side)<={0} for side in dj),'ALL9 degree4 motion independent of mean and skew')
        s.eq(ids,'ALL9 absent epsilon1/3 root drift '+str(j),[row['root'][1],row['root'][3]],[s.G0,s.G0])
        W=(s.N0,s.nm(t,Wj))
        s.eq(ids,'ALL9 canonical drift and full fifth skew '+str(j),
             [row['root'][2],row['root'][4],row['root'][5]],[s.gf(Lj),dj,W])
        v=s.ga(dj,W)
        norm=s.gm(v,s.gc(v));ideal.append(norm)
        if j not in (2,7):
            constant=projection(norm,'t0')[0]
            positive('ALL7 zero-skew winning gap '+str(j),s.na(s.C['motion_A'],s.ns(constant,-1)))
        if j not in (3,4,5,6):
            leading=row['normals'][2]
            need(leading[1]==s.N0,'physical inactive leading half-normal '+str(j))
            positive('ALL5 inactive inward leading original '+str(j),s.ns(leading[0],-1))
    sin=(s.N0,sinpart(4))
    bj=s.gm(sin,s.gf(s.nm(s.C['motion_B_over_sin'],t)))
    quad=s.gf(s.na(s.C['motion_A'],s.nm(s.C['motion_q2'],s.np(t,2))))
    if damage=='wrong_motion_winner':bj=s.gs(bj,-1)
    s.eq(ids,'WHOLE positive ideal winning norm',[ideal[7]],[s.ga(quad,bj)])
    s.eq(ids,'WHOLE negative ideal winning norm',[ideal[2]],[s.ga(quad,s.gs(bj,-1))])
    ell_squared=s.ns(s.nm(s.H,s.nm(m.Gmean,s.ni(s.kappa))),-1)
    old_ell_squared=s.ns(s.nm(s.H,s.nm(m.Gstar,s.ni(s.kappa))),-1)
    positive('ellmean_squared',ell_squared)
    positive('strict_endpoint_skew_squared_gain',s.na(ell_squared,s.ns(old_ell_squared,-1)))
    center_cost=s.na(m.Gstar,s.nm(m.L,m.MUstar),s.ns(s.np(m.MUstar,2),F(4,3)))
    s.eq(ids,'WHOLE real mean optimizing coefficient',[s.gf(center_cost)],[s.gf(m.Gmean)])
    ellipse=s.na(m.Gmean,s.ns(s.np(s.na(mu,s.ns(m.MUstar,-1)),2),F(4,3)),
                 s.nm(s.nm(s.kappa,s.ni(s.H)),s.np(t,2)))
    cost=s.na(m.Gstar,s.nm(m.L,mu),s.ns(s.np(mu,2),F(4,3)),
              s.nm(s.nm(s.kappa,s.ni(s.H)),s.np(t,2)))
    s.eq(ids,'WHOLE coupled limiting ellipse',[s.gf(cost)],[s.gf(ellipse)])
    return signs,ideal,ell_squared,old_ell_squared,[str(lo),str(hi)]

def column_controls(ps,ids):
    # Literal factor/integration controls at both orders and every label.
    for degree in (7,9):
        base=s.actual_polynomial(*ps,degree,2)
        for index in (0,1):
            changed=add_odd(ps,degree,s.N1 if index==0 else s.N0,s.N1 if index==1 else s.N0)
            p=s.actual_polynomial(*changed,degree,2)
            delta=[s.ga(a,s.gs(b,-1)) for a,b in zip(p[degree],base[degree])]
            expected=[s.G0]*10
            if index==0:
                expected[0]=(s.N0,s.ns(s.N1,9));expected[8]=(s.N0,s.ns(s.N1,-9))
            else:
                expected[0]=(s.N0,s.ns(s.H,F(9,7)));expected[7]=(s.N0,s.ns(s.H,F(-9,7)))
            s.eq(ids,'WHOLE odd primitive column '+str(degree)+'/'+str(index),delta,expected)
            for j in range(9):
                omega=s.np(s.WW,j);value=s.G0
                for power,g in enumerate(delta):value=s.ga(value,s.gm(g,s.gf(s.np(omega,power))))
                normal=s.gs(s.real(value),F(-1,9))
                s.eq(ids,'ALL9 actual odd normal column '+str(degree)+'/'+str(index)+'/'+str(j),
                     [normal],[(s.N0,ODD[j][index])])
