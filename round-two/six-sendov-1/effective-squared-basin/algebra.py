"""Whole-interval rational caps and analytic coefficient majorants."""
from fractions import Fraction as Q
from math import comb, factorial

from polynomials import add, mul, power, scale, value, integral, to_a, trim, require, digest
MU=Q(22096964222976,21378414915091)
def polar_integral(k,n):
    return [Q(factorial(n)*factorial(k+n-j),factorial(n-j)*factorial(k+n+1)) for j in range(n+1)]

def bern(p, lo, hi, n=None):
    n=max(len(p)-1, n or 0)
    a=[sum(p[j]*comb(j,k)*lo**(j-k)*(hi-lo)**k for j in range(k,len(p))) for k in range(n+1)]
    b=[sum(a[k]*Q(comb(i,k),comb(n,k)) for k in range(i+1)) for i in range(n+1)]
    inverse=[Q(0)]*(n+1)
    for i,c in enumerate(b):
        for j in range(n-i+1): inverse[i+j]+=c*comb(n,i)*comb(n-i,j)*(-1)**j
    require(a==inverse,'whole elevated Bernstein inverse')
    return b

def ratio_bound(p,d,lo,hi):
    n=max(len(p),len(d))-1
    bp,bd=bern(p,lo,hi,n),bern(d,lo,hi,n)
    require(all(v>0 for v in bd),'strict positive denominator Bernstein')
    return max(abs(x)/y for x,y in zip(bp,bd))

def cap_record(p,d,lo,hi):
    n=max(len(p),len(d))-1
    bp,bd=bern(p,lo,hi,n),bern(d,lo,hi,n)
    require(all(v>0 for v in bd),'positive elevated denominator')
    return {'degree':n,'numerator':p,'denominator':d,
            'numerator_bernstein':bp,'denominator_bernstein':bd,
            'cap':max(abs(x)/y for x,y in zip(bp,bd))}

def bounds():
    x,a=[0,1],[0,1]; one_minus=[1,-1]; b=[1,0,-1]; L=[1,1]
    ko,bo,dc,dh=[],[],[],[]
    certificates={'origin_small':[],'origin_heavy':[], 'polar_small':[], 'polar_heavy':[]}
    for k in range(8):
        n=7-k
        if k:
            raw=scale(mul(power(x,k),add(integral(k,n),scale(mul(x,integral(k+1,n)),-9))),9)
            rec=cap_record(raw,power(one_minus,k),Q(5,13),Q(1,2))
            certificates['origin_small'].append(rec); ko.append(rec['cap'])
            p=mul(power(b,k-1),add(polar_integral(k,8-k),scale(mul(one_minus,polar_integral(k+1,7-k)),8)))
            rec=cap_record(p,[1],Q(5,8),Q(1))
            certificates['polar_small'].append(rec); dc.append(rec['cap'])
        raw=scale(mul(power(x,k+1),integral(k+1,n)),9)
        rec=cap_record(raw,power(one_minus,k+1),Q(5,13),Q(1,2))
        certificates['origin_heavy'].append(rec); bo.append(rec['cap'])
        rec=cap_record(mul(power(b,k),polar_integral(k+1,n)),[1],Q(5,8),Q(1))
        certificates['polar_heavy'].append(rec); dh.append(rec['cap'])
    # Model heavy curvature numerator over18(1+a)^6.
    ip=to_a(integral(1,7)); j1=polar_integral(1,7)
    bn=add(scale(mul(power(a,2),power(ip,2)),81),[-1],scale(mul(b,power(L,6),power(j1,2)),-9*MU))
    shift=add(bn,scale(power(L,6),-Q(18,4)))
    bc=bern(shift,Q(5,8),Q(1))
    require(all(v>0 for v in bc),'full heavy curvature shifted certificate')
    return {'ko':ko,'bo':bo,'dc':dc,'dh':dh,'certificates':certificates,
            'heavy_B_numerator':bn,'heavy_B_shift_polynomial':shift,
            'heavy_B_shift':bc,'heavy_B_min':min(bc)}

# Rectangular rational jets around(t,S,Z). Coefficients are Taylor values,
# so evaluation derivatives are coefficient times factorial.
LIMIT=(4,2,2)
def const(v): return {(0,0,0):Q(v)} if v else {}
def jadd(*ps):
    r={}
    for p in ps:
        for k,v in p.items(): r[k]=r.get(k,Q(0))+v
    return {k:v for k,v in r.items() if v}
def jscale(p,c): return {k:v*c for k,v in p.items() if v*c}
def jmul(*ps):
    r=const(1)
    for p in ps:
        out={}
        for i,x in r.items():
            for j,y in p.items():
                k=tuple(u+v for u,v in zip(i,j))
                if all(u<=v for u,v in zip(k,LIMIT)): out[k]=out.get(k,Q(0))+x*y
        r={k:v for k,v in out.items() if v}
    return r
def jpow(p,n): return jmul(*([p]*n))
def jinv(p):
    c=p.get((0,0,0),Q(0)); require(c!=0,'jet reciprocal domain')
    u=jscale(jadd(p,const(-c)),-1/c)
    r={}; v=const(1)
    for _ in range(sum(LIMIT)+1):
        r=jadd(r,v); v=jmul(v,u)
    return jscale(r,1/c)
def deriv(p,k): return p.get(k,Q(0))*factorial(k[0])*factorial(k[1])*factorial(k[2])

def majorants(bs,t0,s0,z0=Q(0)):
    t=jadd(const(t0),{(1,0,0):Q(1)})
    s=jadd(const(s0),{(0,1,0):Q(1)})
    z=jadd(const(z0),{(0,0,1):Q(1)})
    t2,t4=jpow(t,2),jpow(t,4)
    htail=jmul(t4,jinv(jadd(const(1),jscale(t2,-Q(5,3)))))
    H=jmul(jadd(jscale(t2,Q(1,4)),jscale(htail,Q(64,507))),
           jinv(jadd(const(1),jscale(t2,-Q(1,2)),jscale(htail,-Q(8,39)))))
    def exp_bound(v):
        return jadd(const(1),v,jscale(jpow(v,2),Q(1,2)),jscale(jpow(v,3),Q(1,6)),
                    jscale(jmul(jpow(v,4),jinv(jadd(const(1),jscale(v,-Q(1,5))))),Q(1,24)))
    E=exp_bound(t)
    B=jadd(jscale(t,Q(64,39)),jscale(jadd(E,const(-1),jscale(t,-1)),Q(8,13)),jmul(E,H),jmul(E,s))
    V=jadd(jscale(jadd(E,const(-1)),Q(72,13)),jmul(E,H),jmul(E,s),jmul(E,z))
    wo=jadd(*(jscale(jpow(B,k),bs['ko'][k-1]/factorial(k)) for k in range(1,8)),
            jmul(V,jadd(*(jscale(jpow(B,k),bs['bo'][k]/factorial(k)) for k in range(8)))))
    wd=jadd(*(jscale(jpow(B,k),bs['dc'][k-1]/factorial(k)) for k in range(1,8)),
            jmul(V,jadd(*(jscale(jpow(B,k),bs['dh'][k]/factorial(k)) for k in range(8)))))
    U=jadd(H,s)
    rad=jmul(jpow(jadd(const(1),jscale(jadd(U,z),Q(2,9))),2),exp_bound(jscale(U,4)))
    W=jadd(wo,jscale(jpow(wo,2),Q(128,9)),
           jscale(jadd(rad,const(-1)),Q(9,2)*Q(8,13)**8),
           jscale(jadd(wd,jscale(jpow(wd,2),Q(39,128))),MU))
    wa=jadd(*(jscale(jpow(B,k),bs['bo'][k]/factorial(k)) for k in range(1,8)))
    we=jadd(*(jscale(jpow(B,k),bs['dh'][k]/factorial(k)) for k in range(1,8)))
    WB=jadd(jscale(jadd(jscale(wa,2*bs['bo'][0]),jpow(wa,2)),Q(128,9)),
            jscale(jadd(exp_bound(jscale(U,4)),const(-1)),Q(8,13)**6/Q(18)),
            jscale(jadd(we,jpow(we,2)),MU*Q(39,128)))
    return W,WB

def majorant_radius():
    t=Q(1,32); y=t*t
    tail=y*y/(1-Q(5,3)*y)
    H=(y/4+Q(64,507)*tail)/(1-y/2-Q(8,39)*tail)
    require(H<Q(1,4000),'explicit radial-majorant radius')
    require(H+Q(1,128)<Q(1,100),'all positive majorant denominators')
    require(Q(9,2)-H-Q(1,128)>4,'positive reference heavy radius')
    return H

def controls():
    # Polynomial integrals via literal factor multiplication, independently
    # of the signed-binomial/factorial closed formula.
    checks=0; a=[0,1]; b=[1,0,-1]; L=[1,1]
    for n in range(8):
        for k in (1,2):
            literal=power([1,-1],n)
            literal=[v/Q(k+j+1) for j,v in enumerate(literal)]
            require(trim(literal)==integral(k,n),'full origin primitive identity')
            literal=add(*(scale(mul(power(a,n-j),power([1,-1],j)),Q(comb(n,j),k+j+1)) for j in range(n+1)))
            require(literal==polar_integral(k,n),'full polar primitive identity')
            checks+=2
    normalized=[[-1,0,-1,0,-1,0,-1]]
    for k in range(1,9): normalized.append(scale(mul(power(a,8-k),power(b,k-1)),Q(1,k+1)))
    require(add(mul(b,normalized[0]),[1])==power(a,8),'constant C=1+bD coefficient')
    for k in range(1,9):
        require(mul(b,normalized[k])==scale(mul(power(a,8-k),power(b,k)),Q(1,k+1)), 'every elementary-symmetric C coefficient')
        checks+=1
    c0=add(*(scale(mul(power(a,8-k),power(b,k),power(L,8-k)),Q((comb(7,k) if k<=7 else 0)+(9*comb(7,k-1) if k else 0),k+1)) for k in range(9)))
    require(c0==power(L,8),'whole model polar equality')
    origin_poly=mul([1,-9],power([1,-1],7))
    require(trim([v/Q(j+1) for j,v in enumerate(origin_poly)])==power([1,-1],8),'whole model origin integral')
    hnum=add(power(L,8),[-1],scale(mul(a,power(L,6)),-2))
    require(hnum==mul(a,[6,16,26,30,26,16,6,1]),'whole H>1/4 identity')
    checks+=4
    # Definition-level monomial derivative oracle for every retained entry.
    pts=(Q(1,31),Q(1,127),Q(1,29))
    vs=[jadd(const(v),{tuple(int(i==j) for i in range(3)):Q(1)}) for j,v in enumerate(pts)]
    monomials=0
    for i in range(7):
        for j in range(4):
            for k in range(4):
                p=jmul(jpow(vs[0],i),jpow(vs[1],j),jpow(vs[2],k))
                for u in range(5):
                    for v in range(3):
                        for w in range(3):
                            expected=Q(0) if u>i or v>j or w>k else Q(comb(i,u)*comb(j,v)*comb(k,w))*pts[0]**(i-u)*pts[1]**(j-v)*pts[2]**(k-w)
                            require(p.get((u,v,w),Q(0))==expected,'all monomial Taylor entries')
                monomials+=1
    coeff=(Q(1,5),Q(1,7),Q(1,11))
    den=jadd(const(1),*(jscale(v,-c) for v,c in zip(vs,coeff)))
    inv=jinv(den); c=den[(0,0,0)]
    require(jmul(inv,den)==const(1),'whole quotient-ring inverse')
    for i in range(5):
        for j in range(3):
            for k in range(3):
                n=i+j+k
                expected=Q(factorial(n),factorial(i)*factorial(j)*factorial(k))*coeff[0]**i*coeff[1]**j*coeff[2]**k/c**(n+1)
                require(inv.get((i,j,k),Q(0))==expected,'closed reciprocal coefficient oracle')
    try: jinv({(1,0,0):Q(1)})
    except ValueError: pass
    else: raise ValueError('zero reciprocal accepted')
    return {'whole_primitive_identities':checks,'monomial_jets':monomials,
            'retained_entries_per_jet':45,'reciprocal_entries':45,
            'monomial_point':pts,'reciprocal_weights':coeff,
            'full_normalized_polar_coefficients':normalized}

def rationalize(x):
    if isinstance(x,Q): return str(x)
    if isinstance(x,dict): return {k:rationalize(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [rationalize(v) for v in x]
    return x

def reject(op,message):
    try: op()
    except ValueError: return
    raise ValueError('damage was accepted: '+message)

def margins(ms,mm,m4,mks,mkt,mbs,mbt,slack_den=64,phase_den=160000):
    require(ms/Q(slack_den)+mm/Q(phase_den)<=Q(3,8),'slack residual >=3/8 gap')
    require(m4/Q(phase_den)<=Q(1,80),'phase residual >=gap/80 from reviewed model bound1/40')
    require((mks/Q(slack_den)+mkt/Q(phase_den))*Q(3,8)<Q(1,8),'heavy derivative variation <1/8')
    require((mbs/Q(slack_den)+mbt/Q(phase_den))*Q(3,8)<Q(1,8),'heavy curvature variation <1/8')
    require(Q(3,8)/slack_den<=Q(1,128),'slack box inside majorant radius')
    require(Q(3,8)/phase_den<=Q(1,32)**2,'phase box inside majorant radius')

def regenerate_record():
    bs=bounds(); T,S=Q(1,32),Q(1,128)
    majorant_radius()
    w0,b0=majorants(bs,Q(0),S)
    w,b=majorants(bs,T,S)
    wp,_=majorants(bs,T,Q(0))
    raw={'MS':deriv(w0,(0,2,0))/2,'Mmix':deriv(w,(2,1,0))/2,
         'M4':deriv(wp,(4,0,0))/24,'MKs':deriv(w0,(0,1,1)),
         'MKt':deriv(w,(2,0,1))/2,'MBs':deriv(b0,(0,1,0)),
         'MBt':deriv(b,(2,0,0))/2}
    caps=dict(zip(raw,(19,800,1200,16,210,4,11)))
    require(all(0<v<Q(caps[k]) for k,v in raw.items()),'all seven rigorous rounded derivative caps')
    margins(*caps.values())
    c=controls()
    nbern=sum(2*(r['degree']+1) for group in bs['certificates'].values() for r in group)+len(bs['heavy_B_shift'])
    require(nbern==631,'full Bernstein coefficient coverage')
    reject(lambda:margins(*caps.values(),slack_den=8),'excessive slack box')
    reject(lambda:margins(*caps.values(),phase_den=10000),'excessive phase box')
    reject(lambda:require(raw['M4']<1100,'false fourth-order cap'),'incorrect derivative cap')
    reject(lambda:require(Q(7,3)**2>=7,'incorrect phase one-norm bound'),'incorrect phase norm factor')
    return rationalize({'schema':1,'author':'six-sendov-1','role':'researcher',
        'weight':MU,'base_interval':['5/8','1'],'majorant_phase_radius':T,'majorant_slack_radius':S,
        'radial_majorant_at_radius':majorant_radius(),'bounds':bs,
        'derivative_values':raw,'derivative_caps':caps,'controls':c,
        'bernstein_coefficients':nbern,'full_basis_reconstructions':61,
        'mathematical_damage_controls':4,'slack_denominator':64,'phase_squared_denominator':160000,
        'phase_coercivity_denominator':100,'slack_coercivity':'3/10',
        'mathematical_dependency':'Independent review9168 model slack>=3gap/4, full phase matrix>=gap I/40 and heavy derivative<9/8; squared functional has exactly those jets, extending author9111. No theorem implementation imported.',
        'trust_boundary':'Exact stdlib Fraction polynomial caps, complete Bernstein reverse identities, rational truncated Taylor arithmetic and ordinary analytic majorant proof. Unformalized, independently unreviewed. No float, solver, CAS or external corpus.'})
