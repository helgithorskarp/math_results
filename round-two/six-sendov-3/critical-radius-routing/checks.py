"""Finite exact corroboration of PROOF.md; not the ordinary analytic bridges.

Sparse polynomials use twenty commuting indeterminates and arbitrary-precision
rational coefficients. Each identity compares its entire coefficient map.
The unchanged sparse-polynomial/cube-field kernel is credited to author six-sendov-3, source38e2ad4bbdb3abf015805b49022a1c075435c947, coefficient-chamber/checks.py. New target identities and budgets follow below. This reuse is not independent review.
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


def finite_identities(changes):
    rows=[]
    roots=[gp(variable(j), variable(j+8)) for j in range(8)]
    mean=gscale(gadd(*roots), F(1, changes.get('mean_divisor',8)))
    centered=[gadd(x,gscale(mean,-1)) for x in roots]
    gid(rows,'all centered criticals sum to zero',gadd(*centered),gp({},{}))
    variance=add(*(norm(x) for x in centered))
    total=add(*(norm(x) for x in roots))
    identity(rows,'whole complex mean and variance',total,
             add(variance,scale(norm(mean),8)))
    original_trace=gadd(*(gmul(x,x) for x in roots))
    center_trace=gadd(*(gmul(x,x) for x in centered))
    gid(rows,'whole complex second trace',original_trace,
        gadd(center_trace,gscale(gmul(mean,mean),8)))
    pairs=gadd(*(gmul(roots[j],roots[k]) for j in range(8) for k in range(j)))
    gid(rows,'original c7 from centered data',gscale(pairs,F(9,7)),
        gscale(gadd(gscale(gmul(mean,mean),changes.get('mean_c7',56)),
                    gscale(center_trace,-1)),F(9,14)))
    gid(rows,'centered c7 is -9T/14',
        gscale(gadd(*(gmul(centered[j],centered[k]) for j in range(8) for k in range(j))),F(9,7)),
        gscale(center_trace,F(-9,14)))
    x,y,q,j=[variable(k) for k in range(4)]
    rotated=gmul(gp(q,j),gmul(gp(x,scale(y,-1)),gp(x,scale(y,-1))))
    identity(rows,'entire rotation preserves complex trace modulus after clearing r4',
             norm(rotated),multiply(add(power(q,2),power(j,2)),power(add(power(x,2),power(y,2)),2)))

    M,D,a,t,Q,J=[variable(k) for k in range(6)]
    square=add(power(M,2),power(D,2))
    radial=add(power(add(a,scale(M,-1)),2),power(D,2))
    pair=add(scale(add(power(a,2),constant(-1)),F(1,2)),
             scale(multiply(a,M),F(-3,2)),scale(square,F(3,2)))
    identity(rows,'whole centered base pair-normal identity',pair,
             scale(add(scale(radial,3),scale(power(a,2),-1),constant(-2),
                       scale(square,changes.get('base_square',3))),F(1,4)))
    def reduce_sqrt3(p):
        out={}
        for monomial,c in p.items():
            e=list(monomial); k=e[3]//2; e[3]%=2
            out[tuple(e)]=out.get(tuple(e),F(0))+c*3**k
        return {m:c for m,c in out.items() if c}
    for sign in (1,-1):
        sine=scale(t,F(sign,2))
        real=add(scale(a,F(-1,2)),scale(M,F(3,2)),multiply(D,sine))
        imag=add(multiply(a,sine),scale(D,F(3,2)),scale(multiply(M,sine),-1))
        actual=reduce_sqrt3(scale(add(power(real,2),power(imag,2),constant(-1)),F(1,2)))
        rhs=add(pair,scale(multiply(multiply(t,a),D),F(sign,2)))
        identity(rows,'individual base original normal sign'+str(sign),actual,rhs)
        normal=add(actual,scale(Q,F(-3,28)),scale(multiply(t,J),F(-sign,28)))
        identity(rows,'individual complex T contribution sign'+str(sign),normal,
                 add(pair,scale(Q,F(-3,28)),
                     scale(multiply(t,add(multiply(a,D),scale(J,F(-1,14)))),F(sign,2))))
    table=[]
    w=(F(0),F(1)); wb=(F(-1),F(-1))
    for k in range(1,8):
        wk=field_power(w,k); bk=field_power(wb,k)
        avg=tuple((v+b)/2 for v,b in zip(wk,bk))
        expected=F(0) if k%3==0 else F(-3,2)
        if k==6:expected=changes.get('c6_cube_weight',expected)
        need(avg==(expected+1,F(0)), 'cube cancellation coefficient '+str(k))
        # bar omega / omega^8 equals1 at BOTH cube roots.
        need(field_power(w,9)==(F(1),F(0)) and field_power(wb,9)==(F(1),F(0)), 'cube denominator phase')
        table.append({'j':k,'average_minus1':[str(avg[0]-1),str(avg[1])],
                      'ubar_linear_denominator_phase':'1'})
    rows.append({'name':'whole cube-root coefficient/denominator table','rows':table})

    V,Q,eta,mm,err,tail=[variable(k) for k in range(6)]
    lhs=add(scale(eta,F(8,3)),scale(power(eta,2),F(-4,3)),scale(mm,4),
            scale(Q,F(-4,7)),scale(err,F(-16,3)),
            scale(add(V,scale(Q,3)),F(1,4)),scale(tail,-1))
    identity(rows,'signed radial/objective combination',lhs,
             add(scale(eta,F(8,3)),scale(power(eta,2),F(-4,3)),scale(mm,4),
                 scale(V,F(1,4)),scale(Q,changes.get('signed_Q',F(5,28))),
                 scale(err,F(-16,3)),scale(tail,-1)))
    identity(rows,'joint trace conic complete square',
             add(power(add(scale(eta,12),scale(Q,-5)),2),scale(power(Q,2),-49)),
             add(scale(power(eta,2),294),scale(power(add(Q,scale(eta,F(5,2))),2),
                         -changes.get('conic_square',24))))
    a=add(constant(1),scale(eta,-1)); ac=power(a,3)
    slack=add(eta,scale(power(eta,2),F(-1,2)),scale(multiply(ac,eta),F(-15,16)),
              scale(mm,F(-3,4)),scale(multiply(ac,add(V,scale(Q,3))),F(-3,64)),
              scale(Q,F(3,28)),scale(multiply(multiply(ac,eta),V),F(3,4)),
              scale(multiply(ac,tail),F(3,16)),err)
    identity(rows,'entire individual-slack decomposition',slack,
             add(scale(eta,F(1,16)),scale(V,F(-3,64)),scale(Q,F(-15,448)),
                 scale(mm,F(-3,4)),scale(multiply(add(constant(1),scale(ac,-1)),eta),F(15,16)),
                 scale(power(eta,2),F(-1,2)),
                 scale(multiply(add(constant(1),scale(ac,-1)),add(V,scale(Q,3))),F(3,64)),
                 scale(multiply(multiply(ac,eta),V),F(3,4)),scale(multiply(ac,tail),F(3,16)),err))
    identity(rows,'complex mean cap square',constant(F(4,5)**2+F(1,3)**2),constant(F(13,15)**2))
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




def scalar_budgets(changes):
    eta = F(1,changes.get("eta_denominator",65536)); rho = F(1,64); vmax = 8*rho*rho
    amin = 1-eta; rmin = amin-rho; rmax = 1+rho
    L=changes.get("original_scale",F(1,2)); D=changes.get("cube_scale",F(1,6)); upper=rmax+L*vmax
    caps = {j:F(9,8*j)*comb(8,9-j)*rho**(7-j) for j in range(1,7)}
    caps[7]=F(9,14)
    derivative=sum(j*caps[j]*upper**(j-1) for j in caps)
    cube=(1,2,4,5,7)
    numerator=F(7,4)*sum(caps[j]*rmax**j for j in cube)
    denominator=9*rmin**8-36*upper**7*L*vmax-derivative*vmax
    motion=4*upper**7*D*D/rmin**8+D*derivative/(9*rmin**8)
    quadratic_caps={5:F(63,32),4:F(63,32)*rho,2:F(9,128)*rho*vmax,1:F(9,4096)*vmax**2}
    higher=sum(quadratic_caps[j]*rmin**(j-7) for j in quadratic_caps)/6
    error_coefficient=(1+2*rho)*motion+D*D/2+higher
    records=[]
    def check(name, margin):
        margin=F(margin)
        records.append({'name':name,'strict_margin':str(margin)})
        if margin<=0:
            raise CertificateError(name+' failed: '+str(margin))
    check('nine counted original circles',9*rmin**8*L-36*upper**7*L*L*vmax-sum(caps[j]*(upper**j+rmax**j) for j in caps))
    check('disjoint original circles',F(4,9)*rmin-2*L*vmax)
    check('positive root motion divisor',denominator)
    check('cube displacement below V/6',D*denominator-numerator)
    check('cube linear displacement below V/6',D*9*rmin**8-numerator)
    check('full pair remainder E<=|mean|V/6+V^2',changes.get('pair_V2_cap',F(1))-error_coefficient)
    individual_error=(1+2*rho)*motion+D*D/2+F(6,5)*higher
    check('full individual remainder E<=|mean|V/6+V^2',changes.get('pair_V2_cap',F(1))-individual_error)
    check('sqrt3/9<1/5',F(1,25)-F(1,27))
    tau0=F(17,384)
    check("whole centered critical radius from fixed energy",tau0**2-vmax)
    check("marked reciprocal denominators finite from fixed energy",amin**2-vmax)
    def tail(tau, radial): return tau/((radial-tau)*radial**3)
    check('initial lower objective >=8/r-3V/5',F(3,5)-F(1,2)/rmin**3-tail(tau0,rmin))
    r0=F(6399,6400)
    check('low F gives r>6399/6400',1-(3*eta+F(3,5)*vmax)/8-r0)
    check('positive signed variance coefficient',F(3,4)/rmax**3-F(4,7))
    C=F(4,7)-F(1,2)/r0**3
    def energy(name,mcap,vcap,tau,target):
        coef=C-tail(tau,r0)-F(16,3)*(mcap/6+vcap)
        check(name+' positive divisor',coef)
        check(name+' gives V<'+str(target)+'eta',target*coef-(F(1,3)+F(4,3)*eta))
    energy('first bootstrap',rho,vmax,tau0,changes.get('first_variance_cap',700))
    check('retained mean square below eta/11',F(1,11)-F(1,12)-eta/3)
    check('mean modulus below1/800',F(1,800)**2-eta/11)
    check('V<26eta permits max centered radius1/50',F(1,50)**2-26*eta)
    energy('second bootstrap',F(1,800),vmax,tau0,changes.get('second_variance_cap',26))
    check('V<8eta permits max centered radius1/90',F(1,90)**2-8*eta)
    energy('third bootstrap',F(1,800),26*eta,F(1,50),changes.get('third_variance_cap',8))
    energy('fourth bootstrap',F(1,800),8*eta,F(1,90),changes.get('fourth_variance_cap',6))
    check('final V<6eta permits max centered radius1/96',F(1,96)**2-6*eta)
    check('mean real part strictly negative',amin**2/F(10)-1/(22*amin))
    ecoeff=F(1,800)+36*eta
    check('V<6eta yields r<1+eta',2-F(6,7)-F(4,3)*ecoeff)
    check('V<6eta yields r>1-eta',1-F(33,40))
    check('whole |r^-3-1|<=4eta',4-3/amin**4)
    T=tail(F(1,96),amin)
    check('joint constraint 7V+5Q<12eta',changes.get('joint_cap',12)-F(28,3)-F(112,3)*eta-28*(24*eta+6*T)-F(448,3)*ecoeff)
    check('cube pair slack below eta/12',F(1,12)-F(1,16)-F(171,16)*eta-F(9,8)*T-ecoeff)
    check('2/sqrt3<7/6',F(49,36)-F(4,3))
    check('sqrt6<5/2',F(25,4)-6)
    check('real mean above -4eta/5',changes.get('real_mean_cap',F(4,5))-(F(2,3)+F(1,14)+F(2,3)*ecoeff)/amin)
    check('imaginary mean modulus below eta/3',changes.get('imag_mean_cap',F(1,3))-(F(5,28)+F(7,72))/amin)
    check('mean modulus13eta/15 routes c8 below8eta',8-9*F(13,15))
    check('c7 below4eta',4-F(9,14)*(6+56*F(169,225)*eta))
    check('critical energy H below7eta',7-6-8*F(169,225)*eta)
    check('direct uniform first-power slope exceeds13/5',F(8,3)-F(4,3)*eta-F(13,5))
    for j in range(1,7):
        m=9-j
        # Square removes the possible half-integral power at the positive endpoint.
        check('Maclaurin c'+str(j)+' below8eta',64-(F(9,j)*comb(8,m))**2*F(7,8)**m*eta**(m-2))
    return records


DAMAGES=(
 ("wrong mean multiplicity", {"mean_divisor":7}),
 ("wrong original c7 translation", {"mean_c7":64}),
 ("retain canceled c6 cube weight", {"c6_cube_weight":F(-3,2)}),
 ("drop positive mean square", {"base_square":2}),
 ("wrong signed variance coefficient", {"signed_Q":F(1,4)}),
 ("wrong trace conic square", {"conic_square":25}),
 ("insufficient original root circle", {"original_scale":F(1,10)}),
 ("insufficient cube displacement budget", {"cube_scale":F(1,10)}),
 ("insufficient individual normal remainder", {"pair_V2_cap":F(1,2)}),
 ("invalid first variance substitution", {"first_variance_cap":20}),
 ("invalid second variance substitution", {"second_variance_cap":6}),
 ("invalid third variance substitution", {"third_variance_cap":5}),
 ("invalid fourth variance substitution", {"fourth_variance_cap":5}),
 ("insufficient joint trace budget", {"joint_cap":10}),
 ("insufficient negative real mean budget", {"real_mean_cap":F(7,10)}),
 ("insufficient imaginary mean budget", {"imag_mean_cap":F(1,4)}),
 ("omit an actual counted critical", {"omit_critical":True}),
)


def core(changes=None):
    changes={} if changes is None else changes
    return {"schema":"sendov-actual-fixed-critical-energy-routing-exact-v1",
            "eta_endpoint":str(E),"critical_energy_endpoint":"1/512","included_radius_corollary":"1/64",
            "identities":finite_identities(changes),
            "whole_domain_margins":scalar_budgets(changes),
            "literal_controls":literal_controls(changes),
            "claim":"actual disk-rooted anchored H<=1/512 gives F>8+8eta/3-4eta2/3; its F<=8+3eta sublevel enters strict cap8, H<7eta; radius<=1/64 is an included corollary",
            "ordinary_unformalized_bridges":["Rouche root counting, including separate V0 case",
                "whole Taylor/root displacement and ACTUAL original normals",
                "nonnegative Maclaurin/Cauchy and variance positivity",
                "complete infinite Legendre generating tail",
                "convexity and monotone whole-window positive-divisor substitutions",
                "mean imaginary control from both ACTUAL individual originals",
                "both first-power bound and routing self-contained;9533/9572 context only"]}


def build_record():
    result=core();controls=[]
    for name,damage in DAMAGES:
        try:core(damage)
        except CertificateError as exc:controls.append({"damage":name,"rejected_by":str(exc)})
        else:raise CertificateError("mathematical damage unexpectedly accepted: "+name)
    result["mathematical_damage_controls"]=controls
    return result
