"""Finite exact corroboration of PROOF.md; not the ordinary analytic bridges.

Sparse polynomials use twenty commuting indeterminates and arbitrary-precision
rational coefficients. Each identity compares its entire coefficient map.
The unchanged sparse-polynomial/cube-field kernel is credited to author
six-sendov-3, source cd6be6d4272505f394bbea6e13ff69a9f73ee5bf,
critical-radius-routing/checks.py (and its credited 38e2 kernel).
New effective stability identities and budgets follow below.
This reuse is not independent review.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import comb
import json

E = F(1, 65536)
DIM = 20
ZERO = (0,) * DIM


class CertificateError(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise CertificateError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def constant(q):
    return {} if not q else {ZERO: F(q)}


def variable(i):
    exponent = list(ZERO)
    exponent[i] = 1
    return {tuple(exponent): F(1)}


def add(*polys):
    out = {}
    for p in polys:
        for monomial, q in p.items():
            out[monomial] = out.get(monomial, F(0)) + q
    return {m: q for m, q in out.items() if q}


def scale(p, q):
    return {m: a * q for m, a in p.items() if a * q}


def multiply(p, q):
    out = {}
    for m, a in p.items():
        for n, b in q.items():
            exponent = tuple(x + y for x, y in zip(m, n))
            out[exponent] = out.get(exponent, F(0)) + a * b
    return {m: a for m, a in out.items() if a}


def power(p, n):
    need(type(n) is int and n >= 0, "invalid polynomial exponent")
    out = constant(1)
    for _ in range(n):
        out = multiply(out, p)
    return out


def derivative(p, i):
    out = {}
    for m, q in p.items():
        if m[i]:
            exponent = list(m)
            exponent[i] -= 1
            out[tuple(exponent)] = q * m[i]
    return out


def substitute(p, i, image):
    out = {}
    for m, q in p.items():
        exponent = list(m)
        exponent[i] = 0
        out = add(out, multiply({tuple(exponent): q}, power(image, m[i])))
    return out


def encoded(p):
    # The whole sparse coefficient map, not a sampled evaluation.
    return [[list(m), str(q)] for m, q in sorted(p.items())]


def identity(rows, name, lhs, rhs):
    difference = add(lhs, scale(rhs, -1))
    need(not difference, "identity: " + name)
    rows.append({"name": name, "coefficient_count": len(lhs),
                 "lhs_sha256": sha256(canonical(encoded(lhs))).hexdigest(),
                 "rhs_sha256": sha256(canonical(encoded(rhs))).hexdigest(),
                 "nonzero_residual_coefficients": len(difference)})


def margin(rows, name, lhs, rhs=0, strict=True):
    lhs, rhs = F(lhs), F(rhs)
    need(lhs > rhs if strict else lhs >= rhs, "budget: " + name)
    rows.append({"name": name, "lhs": str(lhs), "rhs": str(rhs),
                 "difference": str(lhs - rhs), "strict": strict})


def field_multiply(x, y):
    # Q[w]/(w**2+w+1).  conjugation sends w to -1-w.
    a, b = x
    c, d = y
    return (a*c - b*d, a*d + b*c - b*d)


def field_power(x, n):
    out = (F(1), F(0))
    for _ in range(n):
        out = field_multiply(out, x)
    return out


def gp(x, y):
    return (x, y)


def gadd(*items):
    return (add(*(x[0] for x in items)), add(*(x[1] for x in items)))


def gscale(x, q):
    return (scale(x[0], q), scale(x[1], q))


def gmul(x, y):
    return (add(multiply(x[0], y[0]), scale(multiply(x[1], y[1]), -1)),
            add(multiply(x[0], y[1]), multiply(x[1], y[0])))


def norm(x):
    return add(power(x[0], 2), power(x[1], 2))


def gid(rows, name, x, y):
    identity(rows, name+' real', x[0], y[0])
    identity(rows, name+' imaginary', x[1], y[1])


# Fresh exact ninth-cyclotomic field Q[w]/(w^6+w^3+1).
N0=(F(0),)*6
N1=(F(1),)+(F(0),)*5
NW=(F(0),F(1),F(0),F(0),F(0),F(0))
def na(*xs):return tuple(sum(x[j] for x in xs) for j in range(6))
def ns(x,q):return tuple(q*t for t in x)
def nm(x,y):
    z=[F(0)]*11
    for j in range(6):
        for k in range(6):z[j+k]+=x[j]*y[k]
    for k in range(10,5,-1):z[k-3]-=z[k];z[k-6]-=z[k]
    return tuple(z[:6])
def np(x,n):
    z=N1
    for _ in range(n):z=nm(z,x)
    return z
def ni(x):
    columns=[nm(x,tuple(F(j==k) for j in range(6))) for k in range(6)]
    a=[[columns[k][j] for k in range(6)]+[F(j==0)] for j in range(6)]
    for k in range(6):
        pivot=next((j for j in range(k,6) if a[j][k]),None)
        need(pivot is not None,'ninth-field inverse is a unit')
        a[k],a[pivot]=a[pivot],a[k];q=a[k][k];a[k]=[t/q for t in a[k]]
        for j in range(6):
            if j!=k:
                q=a[j][k];a[j]=[u-q*v for u,v in zip(a[j],a[k])]
    z=tuple(row[-1] for row in a)
    need(nm(x,z)==N1,'whole field inverse coefficient map')
    return z
def nc(x):return na(*(ns(np(NW,(-j)%9),x[j]) for j in range(6)))
def pc(x):return tuple(constant(t) for t in x)
def pv(x):return (x,)+({},)*5
def pa(*xs):return tuple(add(*(x[j] for x in xs)) for j in range(6))
def ps(x,q):return tuple(scale(t,q) for t in x)
def pm(x,y):
    z=[{} for _ in range(11)]
    for j in range(6):
        for k in range(6):z[j+k]=add(z[j+k],multiply(x[j],y[k]))
    for k in range(10,5,-1):
        z[k-3]=add(z[k-3],scale(z[k],-1));z[k-6]=add(z[k-6],scale(z[k],-1))
    return tuple(z[:6])
def pconj(x):
    out=[{} for _ in range(6)]
    for j in range(6):
        c=nc(tuple(F(k==j) for k in range(6)))
        for k in range(6):out[k]=add(out[k],scale(x[j],c[k]))
    return tuple(out)
def za(*xs):return pa(*(x[0] for x in xs)),pa(*(x[1] for x in xs))
def zs(x,q):return ps(x[0],q),ps(x[1],q)
def zm(x,y):
    return pa(pm(x[0],y[0]),ps(pm(x[1],y[1]),-1)),pa(pm(x[0],y[1]),pm(x[1],y[0]))
def zc(x):return pconj(x[0]),ps(pconj(x[1]),-1)
def zn(x):return zm(x,zc(x))
def zreal(x):return zs(za(x,zc(x)),F(1,2))
def zf(x):return pc(x),pc(N0)
def zv(x,y=None):return pv(x),pv({} if y is None else y)
def zid(rows,name,x,y):
    need(x==y,'whole phase identity '+name)
    serial=[[encoded(p) for p in side] for side in x]
    rows.append({'name':name,'all_twelve_field_polynomial_maps_sha256':sha256(canonical(serial)).hexdigest(),
                 'all_twelve_coefficient_counts':[len(p) for p in x[0]+x[1]],'whole_maps_compared':True})


def new_identities(changes):
    rows=[]
    roots=[gp(variable(j),variable(j+8)) for j in range(8)]
    mean=gscale(gadd(*roots),F(1,8));nu=[gadd(z,gscale(mean,-1)) for z in roots]
    T=gadd(*(gmul(z,z) for z in nu))
    U3=gadd(*(gmul(gmul(z,z),z) for z in nu))
    e3=gadd(*(gmul(gmul(nu[j],nu[k]),nu[l]) for j in range(8) for k in range(j) for l in range(k)))
    gid(rows,'whole eight-complex-critical centered integrated d6',gscale(e3,F(-3,2)),
        gscale(U3,changes.get('d6_factor',F(-1,2))))
    V=add(*(norm(z) for z in nu));ur,ui=variable(16),variable(17)
    rotated=[gmul(z,gp(ur,scale(ui,-1))) for z in nu]
    rotatedT=gmul(T,gmul(gp(ur,scale(ui,-1)),gp(ur,scale(ui,-1))))
    identity(rows,'whole rotated real-critical energy after clearing r2',
        scale(add(*(power(z[0],2) for z in rotated)),changes.get('real_energy_factor',2)),
        add(multiply(V,add(power(ur,2),power(ui,2))),rotatedT[0]))
    c=ns(na(np(NW,4),np(NW,5)),F(-1,2));d=ns(na(NW,np(NW,8)),F(1,2))
    need(na(ns(np(c,3),8),ns(c,-6),ns(N1,-1))==N0,'selected cubic field relation')
    need(d==na(ns(np(c,2),2),ns(N1,-1)),'whole cosine double-angle map')
    w4=ni(na(c,d));w3=ns(na(ns(N1,7),ns(nm(na(N1,ns(d,-1)),w4),-1)),F(2,3))
    if changes.get('dual_weight'):w4=ns(w4,F(9,10))
    y=ns(ni(na(N1,c)),F(1,3));x=na(ns(N1,F(2,3)),ns(y,-1));C=na(ns(N1,F(8,3)),y)
    A3=ns(N1,F(3,2));B3=A3;A4=na(N1,c);B4=na(N1,ns(d,-1))
    for name,lhs,rhs in [
      ('real leading mean dual',na(nm(w3,A3),nm(w4,A4)),ns(N1,8)),
      ('rotated trace dual',na(nm(w3,B3),nm(w4,B4)),ns(N1,7)),
      ('known sharp coefficient',na(ns(N1,8),ns(w3,-1),ns(w4,-1)),C),
      ('known optimal cube moment',na(nm(A3,x),nm(B3,y)),N1),
      ('known optimal fourth moment',na(nm(A4,x),nm(B4,y)),N1),
      ('whole nonzero Cramer determinant',na(nm(A3,B4),ns(nm(A4,B3),-1)),ns(na(c,d),F(-3,2)))]:
        need(lhs==rhs,'whole exact dual '+name)
        rows.append({'name':name,'whole_six_field_coefficients':[str(t) for t in lhs]})
    M,D,a,Q,J,K,N=[variable(j) for j in range(7)]
    m=zv(M,D);u=zv(add(a,scale(M,-1)),scale(D,-1));rot=zv(Q,J);third=zv(K,N)
    square=add(power(M,2),power(D,2));table=[]
    for k in range(1,5):
        w=np(NW,k);wb=nc(w);A=na(N1,ns(na(w,wb),F(-1,2)))
        zplus=za(m,zm(u,zf(w)));zminus=za(m,zm(u,zf(wb)))
        base=zs(za(zn(zplus),zn(zminus),zf(ns(N1,-2))),F(1,4))
        expected=za(zv(scale(add(power(a,2),constant(-1)),F(1,2))),
                    zm(zf(A),zv(add(scale(multiply(a,M),-1),square))))
        if k==4 and changes.get('base_mean'):expected=za(expected,zv(multiply(a,M)))
        zid(rows,'entire actual paired base normal phase'+str(k),base,expected)
        if k not in (3,4):continue
        def linear(z,power_,den):
            return zs(zreal(zm(z,zf(na(np(w,power_%9),ns(N1,-1))))),F(1,den))
        def reflected(z,power_,den):
            return zs(zreal(zm(z,zf(na(np(wb,power_%9),ns(N1,-1))))),F(1,den))
        B2=na(N1,ns(na(np(w,2),np(wb,2)),F(-1,2)))
        trace=zs(za(linear(rot,-2,14),reflected(rot,-2,14)),F(1,2))
        zid(rows,'full paired complex T normal phase'+str(k),trace,zm(zf(ns(B2,F(-1,14))),zv(Q)))
        cub=zs(za(linear(third,-3,18),reflected(third,-3,18)),F(1,2))
        expected=zv({}) if k==3 else zv(scale(K,changes.get('fourth_cubic',F(-1,12))))
        zid(rows,'full paired cubic normal phase'+str(k),cub,expected)
        if k==3:
            plus=zs(za(zn(zplus),zf(ns(N1,-1))),F(1,2))
            minus=zs(za(zn(zminus),zf(ns(N1,-1))),F(1,2))
            diff=za(plus,zs(minus,-1),linear(rot,-2,14),zs(reflected(rot,-2,14),-1))
            sine=(pc(N0),pc(ns(na(w,ns(wb,-1)),F(-1,2))))
            rhs=zs(zm(sine,zv(add(multiply(a,D),scale(J,F(-1,14))))),2)
            zid(rows,'whole unaveraged ACTUAL cube difference',diff,rhs)
        for j in range(1,8):
            weight=ns(na(N1,ns(na(np(w,j),np(wb,j)),F(-1,2))),F(1,9))
            if k==4 and j==3 and changes.get('omit_d3'):
                need(weight==N0,'uncanceled d3 at fourth phase')
            if k==4 and j==6 and changes.get('omit_cubic'):
                need(weight==N0,'uncanceled d6 at fourth phase')
            table.append({'phase':k,'degree':j,'whole_pair_coefficient':[str(t) for t in weight]})
    rows.append({'name':'entire fourteen lower coefficient phase weights','rows':table})
    eta,M,Q,V=[variable(j) for j in range(4)]
    L3=za(zm(zf(ns(A3,-1)),zv(M)),zm(zf(ns(B3,F(-1,14))),zv(Q)))
    L4=za(zm(zf(ns(A4,-1)),zv(M)),zm(zf(ns(B4,F(-1,14))),zv(Q)))
    lhs=zv(add(scale(eta,8),scale(M,8),scale(add(V,scale(Q,3)),F(1,4))))
    rhs=za(zm(zf(C),zv(eta)),
        zm(zf(w3),za(zv(eta),zs(L3,-1))),zm(zf(w4),za(zv(eta),zs(L4,-1))),
        zv(scale(add(V,Q),changes.get('defect_variance',F(1,4)))))
    zid(rows,'whole physical sharp-defect decomposition before actual slack substitution',lhs,rhs)
    return rows



def scalar_budgets(changes):
    e=F(1,65536);rho=F(1,64);vmax=F(1,512);amin=1-e
    rmin=amin-rho;rmax=1+rho;L=F(1,2);s=rmax+L*vmax;D=changes.get("displacement",F(1,4))
    A={j:F(9,8*j)*comb(8,9-j)*rho**(7-j) for j in range(1,7)};A[7]=F(9,14)
    Cd=sum(j*A[j]*s**(j-1) for j in A)
    div=9*rmin**8-36*s**7*L*vmax-Cd*vmax
    N=2*sum(A[j]*rmax**j for j in A)
    B=4*s**7*D**2/rmin**8+D*Cd/(9*rmin**8)
    H={5:F(63,32),4:F(63,32)*rho,3:F(21,128)*vmax,2:F(9,128)*rho*vmax,1:F(9,4096)*vmax**2}
    high=sum(H[j]*rmin**(j-7) for j in H)
    normal=(1+2*rho)*B+D**2/2+F(2,9)*high
    Lam=1/((amin-F(1,96))*amin**3)
    rows=[]
    def m(name,x):
     x=F(x);rows.append({'name':name,'margin':str(x)})
     if x<=0:raise CertificateError(name+': '+str(x))
    m('full original displacement below V/4',D*div-N)
    m('full linear displacement below V/4',D*9*rmin**8-N)
    m('all phase full normal quadratic budget9/8',changes.get("normal_cap",F(9,8))-normal)
    m('all phase non-T full root quadratic budget1',changes.get('root_quadratic_cap',1)-B-F(2,9)/amin*high)
    m('complete centered objective eta2 budget40',40-8*F(4,5)*(2-e)/amin**2-4*F(169,225)/amin**3-24)
    R3=F(1,2)+F(3,2)*F(4,5)+F(3,2)*F(169,225)+F(13,15)+36
    R4=F(1,2)+2*F(4,5)+2*F(169,225)+F(13,15)*6/4+F(9,8)*36
    m('whole cube leading-normal remainder40eta2',40-R3)
    m('whole fourth-phase leading-normal remainder46eta2',46-R4)
    m('positive sqrt21 enclosure',F(55,12)**2-21)
    m('full sharp-coercivity budget16',changes.get('sharp_cap',16)-252*F(1,256)-F(55,4)*(Lam+F(3,5)/(12*amin)))
    m('R3 below gapbudget/100',F(16,100)-40*F(1,256))
    m('R4 below gapbudget/12',F(16,12)-46*F(1,256)-F(55,48)/amin)
    Mcoef=F(62,651)*F(13,50)+F(128,217)*F(25,12)
    Ycoef=F(24832,32550)*F(13,50)+F(128,217)*F(25,12)
    m('real mean inversion below4gap/3',F(4,3)-Mcoef)
    m('rotated Q inversion below21gap',F(3,2)-Ycoef)
    m('H difference below26gap',16-8*F(169,225)*F(1,256))
    m('full origin real energy below7gap',16-F(384,25)*F(1,256)-4*e*F(1,256)/amin**2)
    m('imag mean sqrt term below1',1-F(1,2)/amin)
    m('imag mean gap term below1',1-F(7,24)/amin)
    m('imag mean eta2 term below44',changes.get('imag_eta2_cap',44)-F(7,6)*37/amin)
    m('root mean/T eta2 aggregate below125',125-88-36-F(896,1395)/amin)
    m('all9 root-motion gap coefficient below8',changes.get('root_gap_cap',8)-F(14,3)-3/amin-(125*F(1,256)+F(55,36)/amin**2)/16)
    m('all9 root-motion sqrt coefficient below3',(changes.get('root_sqrt_cap',3)-2)**2*49*amin**2-48)
    m('sharp uniform slope exceeds111/40',F(826,291)-F(1,16)-F(111,40))
    clo=F(15,16);chi=F(47,50)
    cf=lambda c:8*c**3-6*c-1
    m('selected cosine lower cubic sign',-cf(clo))
    m('selected cosine upper cubic sign',cf(chi))
    m('selected cosine monotone divisor',24*clo**2-6)
    m('w4 below3/5',F(3,5)-F(128,217))
    m('w4 above1/2',F(625,1067)-F(1,2))
    m('w3 above4',F(2,3)*(7-F(31,217))-4)
    m('w3 below23/5',F(23,5)-F(2,3)*(7-F(291,2134)))
    m('whole centered radius below1/96',F(1,96)**2-6*e)
    m('positive full reciprocal tail divisor',amin-F(1,96))
    return rows


def literal_controls(changes):
    def plus(x,y):return (x[0]+y[0],x[1]+y[1])
    def times(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
    def by(x,q):return (x[0]*q,x[1]*q)
    def cpow(x,n):
        out=(F(1),F(0))
        for _ in range(n):out=times(out,x)
        return out
    def squared(x):return x[0]*x[0]+x[1]*x[1]
    def total(xs):
        out=(F(0),F(0))
        for x in xs:out=plus(out,x)
        return out
    def product_roots(xs):
        p=[(F(1),F(0))]
        for x in xs:
            q=[(F(0),F(0)) for _ in range(len(p)+1)]
            for j,c in enumerate(p):
                q[j]=plus(q[j],by(times(c,x),-1));q[j+1]=plus(q[j+1],c)
            p=q
        return p
    cases=[('total zero collision',[(0,0)]*8),
           ('complex total collision',[(0,F(1,128))]*8),
           ('repeated conjugate critical pairs',[(0,F(1,256))]*4+[(0,F(-1,256))]*4),
           ('genuinely nonconjugate criticals',[(F(1,1024),F(1,512)),(F(-1,512),F(1,1024)),
             (F(1,2048),F(-1,1024)),(0,0),(F(1,512),F(-1,2048)),(0,F(1,256)),(F(-1,256),0),(0,0)]),
           ('unequal imaginary amplitudes',[(0,F(k,1024)) for k in (-3,-2,-1,0,0,1,2,3)]),
           ('fixed energy allows a critical outside1/64',[(F(1,32),0)]+[(0,0)]*7)]
    cases=[cases[0],cases[3],cases[5]]
    if changes.get('omit_critical'):
        cases[0]=(cases[0][0],cases[0][1][:-1])
    rows=[];a=1-E
    for name,raw in cases:
        zs=[(F(x),F(y)) for x,y in raw]
        need(len(zs)==8,'literal missing critical multiplicity')
        m=by(total(zs),F(1,8));nu=[plus(z,by(m,-1)) for z in zs]
        V=sum(squared(z) for z in nu);H=sum(squared(z) for z in zs)
        need(H<=F(1,512),'literal fixed critical energy')
        T=total([times(z,z) for z in nu]);u=plus((a,F(0)),by(m,-1))
        need(H==V+8*squared(m),'literal exact complex variance')
        need(V<=F(1,512) and squared(T)<=V*V,'literal variance/trace domain')
        dp=product_roots(zs)
        p=[(F(0),F(0))]+[by(c,F(9,j+1)) for j,c in enumerate(dp)]
        p[0]=by(total([by(p[j],a**j) for j in range(1,10)]),-1)
        need(total([by(p[j],a**j) for j in range(10)])==(F(0),F(0)),'literal actual anchor')
        need(p[8]==by(m,-9),'literal original c8')
        need(p[7]==by(plus(by(times(m,m),56),by(T,-1)),F(9,14)),'literal original c7')
        centered=[total([by(times(p[n],cpow(m,n-j)),F(comb(n,j))) for n in range(j,10)]) for j in range(10)]
        need(centered[8]==(F(0),F(0)) and centered[7]==by(T,F(-9,14)),'literal centered integrated coefficients')
        need(total([times(centered[j],cpow(u,j)) for j in range(10)])==(F(0),F(0)),'literal full translated anchor')
        distances=[squared(plus((a,F(0)),by(z,-1))) for z in zs]
        need(all(x>0 for x in distances),'literal reciprocal denominators')
        encode=lambda x:[str(x[0]),str(x[1])]
        rows.append({'name':name,'all_eight_criticals':[encode(z) for z in zs],
                     'mean':encode(m),'V':str(V),'H':str(H),'T':encode(T),
                     'whole_anchored_original_polynomial':[encode(c) for c in p],
                     'whole_translated_polynomial':[encode(c) for c in centered],
                     'all_marked_distance_squares':[str(d) for d in distances],
                     'original_disk_feasibility':'not asserted by this finite critical control'})
    return rows


DAMAGES=(
 ('wrong integrated centered cubic',{'d6_factor':F(1,2)}),
 ('wrong rotated real-critical energy',{'real_energy_factor':1}),
 ('wrong credited dual weight',{'dual_weight':True}),
 ('wrong actual fourth base mean',{'base_mean':True}),
 ('cancel the fourth-phase cubic',{'fourth_cubic':0}),
 ('omit uncanceled fourth-phase d3',{'omit_d3':True}),
 ('omit uncanceled fourth-phase d6',{'omit_cubic':True}),
 ('wrong sharp physical variance defect',{'defect_variance':F(1,2)}),
 ('too small all-phase displacement',{'displacement':F(1,5)}),
 ('too small fourth-phase normal remainder',{'normal_cap':1}),
 ('too small non-T root remainder',{'root_quadratic_cap':F(9,10)}),
 ('insufficient sharp full remainder15',{'sharp_cap':15}),
 ('insufficient imaginary eta2 bound43',{'imag_eta2_cap':43}),
 ('insufficient whole root-motion gap7',{'root_gap_cap':7}),
 ('insufficient whole root-motion square-root2',{'root_sqrt_cap':2}),
 ('omit one counted critical',{'omit_critical':True}),
)
def core(changes=None):
    changes={} if changes is None else changes
    return {'schema':'sendov-effective-actual-sharp-profile-stability-v1',
        'eta_endpoint':'1/65536','critical_energy_endpoint':'1/512',
        'identities':new_identities(changes),'whole_domain_margins':scalar_budgets(changes),
        'literal_controls':literal_controls(changes),
        'claim':'actualH512: F>8+Ceta-16eta^(3/2)>8+111eta/40; routed low sublevel has explicit actual slack/rotated real-energy, complex moment and all9 original-motion defects',
        'known_sharp_leading_coefficient':'PRIOR8530/8608, not new',
        'mathematical_input':'9620 ordinary unformalized author energy entry; exact baseline reproduced only as validation',
        'ordinary_unformalized_bridges':['actual-root counted labeling and imported9620 hypotheses',
            'entire nonlinear Taylor displacements and actual original normals',
            'Maclaurin/Cauchy and full infinite Legendre reciprocal tail',
            'positive scalar inequalities, convexity, determinants and square-root estimates',
            'arbitrary critical collisions and separate total-collision case']}
def build_record():
    result=core();controls=[]
    for name,damage in DAMAGES:
        try:core(damage)
        except CertificateError as exc:controls.append({'damage':name,'rejected_by':str(exc)})
        else:raise CertificateError('mathematical damage unexpectedly accepted: '+name)
    result['mathematical_damage_controls']=controls
    return result
