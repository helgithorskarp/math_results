"""Finite exact corroboration of the uniform moving-budget proof.

Same-author unchanged rational/ninth-cyclotomic arithmetic. No ordinary
analytic uniformity, concentration, IFT or supremum argument is formalized.
"""
from pathlib import Path
import json
from arithmetic import (F,N0,N1,NW,na,ns,nm,np,ni,nc,need,constant,
 variable,add,scale,multiply,power,derivative,encoded,identity,margin,canonical,sha256)

def ef(x):return [str(a) for a in x]
def cf(a,b=0,d=0,c=None):return na(ns(N1,F(a)),ns(c,F(b)),ns(np(c,2),F(d)))
def plus(*ps):
    n=max(map(len,ps),default=0)
    return [na(*(p[j] if j<len(p) else N0 for p in ps)) for j in range(n)]
def times(p,q):
    out=[N0]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]=na(out[i+j],nm(a,b))
    return out
def scaled(p,a):return [nm(x,a) for x in p]
def pd(p):return [ns(p[j],j) for j in range(1,len(p))]
def equality(rows,name,lhs,rhs):
    n=max(len(lhs),len(rhs));lhs=lhs+[N0]*(n-len(lhs));rhs=rhs+[N0]*(n-len(rhs))
    need(lhs==rhs,'whole field identity '+name)
    rows.append({'name':name,'all_coefficients':[ef(a) for a in lhs],
                 'nonzero_residual_coefficients':0})

def build(damage=None):
    rows=[];fields=[];bounds=[]
    c=ns(na(np(NW,4),np(NW,5)),F(-1,2))
    if damage=='wrong_embedding':c=ns(c,-1)
    need(c[4]==F(-1,2) and c[5]==F(-1,2),'physical cosine embedding')
    need(na(ns(np(c,3),8),ns(c,-6),ns(N1,-1))==N0,'cosine cubic')
    y=ns(ni(na(N1,c)),F(1,3));x=na(ns(N1,F(2,3)),ns(y,-1))
    H=ns(y,14);U0=ns(x,-8);C=na(ns(N1,F(8,3)),y)
    k=ns(na(N1,ns(c,2)),F(-7,18));rho=ns(na(c,ns(N1,-5)),F(1,3))
    alpha=cf(F(-527,360),F(41,90),F(13,90),c)
    tau=ns(np(na(k,rho),2),F(1,2))
    kappa=na(tau,ns(alpha,F(10,27)))
    gamma=na(tau,ns(alpha,F(5,9)))
    Bstar=cf(F(2311,108),F(4934,27),F(-1976,9),c)
    KE=cf(F(6653,324),F(23915,486),F(-15839,243),c)
    K1=na(Bstar,ns(nm(alpha,np(H,2)),F(-1,2)))
    P=[N0,na(ns(alpha,30),ns(tau,81)),na(ns(alpha,-840),ns(tau,-3024)),ns(tau,28224)]
    g2=[N0,ns(N1,81),ns(N1,-3024),ns(N1,28224)]
    q4=[ns(N1,F(1,2)),ns(N1,30),ns(N1,-840)]
    equality(fields,'whole physical cost curve',plus([K1],scaled(q4,nm(alpha,np(H,2))),scaled(g2,nm(tau,np(H,2)))),
             plus([Bstar],scaled(P,np(H,2))))
    lower=plus(pd(P),scaled(pd(g2),ns(gamma,-1)))
    equality(fields,'lower secant derivative factor',lower,
             scaled(times([N1,ns(N1,-56)],[N1,ns(N1,-56)]),ns(alpha,-14 if damage=='wrong_lower_factor' else -15)))
    upper=plus(scaled(pd(g2),kappa),scaled(pd(P),ns(N1,-1)))
    equality(fields,'upper secant derivative factor',upper,
             scaled(times([N0,N1],[N1,ns(N1,-56)]),ns(alpha,-559 if damage=='wrong_upper_factor' else -560)))
    equality(fields,'exact near-minimum difference',plus(P,scaled(g2,ns(kappa,-1))),
             scaled(times([N0,N0,N1],[N1,ns(N1,F(-112,3))]),ns(alpha,280)))
    endpoint=F(1,56)
    val=lambda p:na(*(ns(a,endpoint**j) for j,a in enumerate(p)))
    equality(fields,'whole endpoint cost',[na(Bstar,nm(np(H,2),val(P)))],[KE])
    equality(fields,'endpoint cubic squared',[val(g2)],[ns(N1,F(9,14))])
    lo=F(15,16);hi=F(47,50);f=lambda t:8*t**3-6*t-1
    ap=lambda t:F(-527,360)+F(41,90)*t+F(13,90)*t*t
    tp=lambda t:F(1369,648)+F(74,81)*t+F(8,81)*t*t
    margin(bounds,'physical bracket left',-f(lo));margin(bounds,'physical bracket right',f(hi))
    margin(bounds,'minus alpha positive',-ap(hi));margin(bounds,'alpha greater than minus one',ap(lo),-1)
    margin(bounds,'tau greater than three',tp(lo),3)
    margin(bounds,'gamma greater than 22/9',tp(lo)+F(5,9)*(-1),F(22,9),strict=False)
    need(na(gamma,ns(kappa,-1),ns(alpha,F(-5,27)))==N0,'gamma versus kappa')

    # Full eight-coordinate polynomial identity BEFORE imposing constraints.
    # Multiplication by 16H^2 clears every denominator; H is a formal variable.
    hs=[variable(j) for j in range(8)];us=[variable(j+8) for j in range(8)]
    HH,UU,rr,kk=[variable(j) for j in range(16,20)]
    sumh=add(*hs);sumu=add(*us);normh=add(*(power(h,2) for h in hs))
    j3=add(*(power(h,3) for h in hs));T=add(UU,multiply(rr,HH))
    bnum=multiply(add(kk,rr),j3)
    gs=[add(u,multiply(rr,power(h,2))) for h,u in zip(hs,us)]
    normg=add(*(power(g,2) for g in gs))
    ep=add(*(multiply(h,u) for h,u in zip(hs,us)),scale(multiply(kk,j3),-1))
    wn=[add(scale(multiply(HH,g),8),scale(multiply(HH,T),-1),scale(multiply(bnum,h),-8)) for g,h in zip(gs,hs)]
    lhs=add(scale(multiply(power(HH,2),normg),8),scale(multiply(power(HH,2),power(T,2)),-1),
            scale(multiply(HH,power(bnum,2)),-8),scale(add(*(power(w,2) for w in wn)),F(-1,8)),
            scale(multiply(multiply(HH,bnum),ep),-15 if damage=='wrong_mixed_term' else -16))
    nh=add(normh,scale(HH,-1))
    rhs=add(scale(multiply(multiply(power(HH,2),T),add(sumu,scale(UU,-1),multiply(rr,nh))),2),
            scale(multiply(multiply(multiply(HH,T),bnum),sumh),-1 if damage=='wrong_balance_defect' else -2),
            scale(multiply(power(bnum,2),nh),-8))
    identity(rows,'entire eight-vector projection with every constraint defect',lhs,rhs)
    # Direct scalar reciprocal first-power Taylor coefficients.
    u,h,a,s,t=[variable(j) for j in range(5)]
    linear=add(power(h,2),scale(add(constant(1),u),-2))
    quad=power(add(constant(1),u),2)
    coeff1=scale(linear,F(-1,2));coeff2=add(scale(quad,F(-1,2)),scale(power(linear,2),F(3,8)))
    identity(rows,'whole first reciprocal coefficient',coeff1,add(constant(1),u,scale(power(h,2),F(-1,2))))
    identity(rows,'whole second reciprocal coefficient',coeff2,
             add(constant(1),scale(u,2),power(u,2),scale(power(h,2),F(-3,2)),
                 scale(multiply(power(h,2),u),F(-3,2)),scale(power(h,4),F(1,4) if damage=='wrong_scalar_jet' else F(3,8))))
    # Quadratic upper-envelope inversion, with s>=0 and t=sqrt(eta)>=0.
    shift=add(s,multiply(a,t))
    identity(rows,'exact additive square-root bound',
             add(power(shift,2),scale(power(s,2),-1),scale(multiply(multiply(a,t),shift),-1)),
             multiply(multiply(a,t),s))
    identity(rows,'whole budget-gap cubic scale',
             add(power(add(s,scale(t,-1)),2),scale(power(s,2),-1)),
             add(scale(multiply(s,t),-2),power(t,2)))

    harmonics=[]
    forms=[(0,0,0),(F(13,324),F(13,162),F(4,81)),
           (F(4,81),F(25,162),F(10,81)),(F(1,36),F(1,9),F(1,9)),(F(4,81),F(8,81),F(4,81))]
    for j in range(8 if damage=='missing_ninth_harmonic' else 9):
        w=np(NW,j);wi=np(w,8)
        W=ns(na(nm(na(ns(N1,3),ns(c,4)),w),ns(nm(na(N1,ns(c,2)),na(N1,wi)),-1),ns(np(wi,2),-1)),F(1,18))
        n=nm(W,nc(W));need(n==cf(*forms[min(j,9-j)],c),'entire physical norm '+str(j))
        d=4*n[1];b=-2*n[4];aa=n[0]-d/2;need(n==cf(aa,b,d,c),'entire real normal form')
        harmonics.append({'label':j,'W':[ef(N0),ef(W)],'squared_norm':[ef(n),ef(N0)],'real_cubic_normal_form':[str(aa),str(b),str(d)]})
    need(len(harmonics)==9,'all nine motion harmonics')
    pc=[[[0,0,0,0,0,0,0],[ef(K1),ef(N0)]],[[0,1,0,0,0,0,0],[ef(alpha),ef(N0)]],[[2,0,0,0,0,0,0],[ef(nm(tau,ni(H))),ef(N0)]]]
    return {'agent':'six-sendov-3','role':'researcher','schema':1,
        'ordinary_analytic_bridges_unformalized':True,'independent_review':False,
        'constants':{n:ef(v) for n,v in [('c',c),('H',H),('U0',U0),('C',C),('alpha',alpha),('tau',tau),('kappa',kappa),('gamma',gamma),('Bstar',Bstar),('KE',KE)]},
        'rational_polynomial_identities':rows,'field_polynomial_identities':fields,'rational_sign_bounds':bounds,
        'cost_curve_coefficients':[ef(a) for a in P],'cubic_squared_curve_coefficients':[ef(a) for a in g2],
        'whole_prior_least_profile_cost':pc,'all_nine_harmonics':harmonics,
        'closed_z_interval':['0','1/56'],'uniform_envelope_error':'O(sqrt(eta))',
        'joint_budget_scale':'delta(eta)/eta -> infinity','unresolved_layer':'delta=O(eta)'}

def compare_baselines(root,record):
    row=next(r for r in json.loads((Path(__file__).parent/'dependencies.json').read_text())['files']
             if r['height']==10090 and r['path'].endswith('/EXPECTED.json'))
    raw=(Path(root)/row['path']).read_bytes()
    need(len(raw)==row['bytes'] and sha256(raw).hexdigest()==row['sha256'],'whole baseline source pin10090')
    old=json.loads(raw)
    for k in ('cost_curve_coefficients','whole_prior_least_profile_cost','all_nine_harmonics'):
        need(old[k]==record[k],'every coefficient of prior baseline '+k)
    for k in ('c','H','U0','C','alpha','tau','kappa','Bstar','KE'):
        need(old['constants'][k]==record['constants'][k],'whole prior physical constant '+k)
    return [{'source_commit':row['source_commit'],'path':row['path'],'whole_file_sha256':row['sha256'],
             'comparison':'ENTIRE cost curve/least-profile cost, ALL9 complete harmonic/norm maps and9 physical constants',
             'same_author_not_independent':True,'prior_theorem_replay':False}]
