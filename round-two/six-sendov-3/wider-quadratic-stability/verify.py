#!/usr/bin/env python3
"""Finite exact corroboration; all analytic bridges remain in PROOF.md.

Actual six-sendov-3/researcher. No sampled original-disk inference.
The rational/Gaussian/ninth-root kernel is credited in arithmetic.py.
"""
import argparse
import copy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from arithmetic import (F, CertificateError, need, canonical, sha256, comb,
    constant, variable, add, scale, multiply, power, identity, encoded,
    gp, gadd, gscale, gmul, norm, gid,
    N0, N1, NW, na, ns, nm, np, ni, nc,
    za, zs, zm, zv, zf, zid)

from budgets import budgets, E_MAX, A_MIN, TAU, ERROR, OBJECTIVE_ERROR


def credited_complete_maps():
    rows=[]
    roots=[gp(variable(j),variable(j+8)) for j in range(8)]
    mean=gscale(gadd(*roots),F(1,8))
    nu=[gadd(z,gscale(mean,-1)) for z in roots]
    V=add(*(norm(z) for z in nu))
    T=gadd(*(gmul(z,z) for z in nu))
    U3=gadd(*(gmul(gmul(z,z),z) for z in nu))
    e3=gadd(*(gmul(gmul(nu[i],nu[j]),nu[k]) for i in range(8) for j in range(i) for k in range(j)))
    gid(rows,'whole8-centered Newton integrated d6',gscale(e3,F(-3,2)),gscale(U3,F(-1,2)))
    ur,ui=variable(16),variable(17)
    ub=gp(ur,scale(ui,-1));r2=add(power(ur,2),power(ui,2))
    rotated=[gmul(z,ub) for z in nu]
    Trot=gmul(T,gmul(ub,ub))
    identity(rows,'whole rotated real energy after clearing r2',
        scale(add(*(power(z[0],2) for z in rotated)),2),
        add(multiply(V,r2),Trot[0]))
    real3=add(*(add(power(z[0],3),scale(multiply(z[0],power(z[1],2)),-3)) for z in rotated))
    identity(rows,'whole signed rotated ReU3 after clearing r3',real3,gmul(U3,gmul(gmul(ub,ub),ub))[0])
    p3=add(*(add(power(z[0],3),scale(multiply(z[0],power(z[1],2)),F(-3,2))) for z in rotated))
    definition=scale(add(*(add(scale(power(z[0],3),5),scale(multiply(z[0],norm(z)),-3)) for z in rotated)),F(1,2))
    identity(rows,'full signed LegendreP3 rotated numerator',p3,definition)
    x,y=variable(18),variable(19);S=add(power(x,2),power(y,2))
    C3=add(power(x,3),scale(multiply(x,power(y,2)),F(-3,2)))
    R3=add(power(x,3),scale(multiply(x,power(y,2)),-3))
    lhs=add(scale(multiply(power(x,2),power(S,2)),F(9,4)),scale(power(C3,2),-1))
    rhs=add(scale(power(x,6),F(5,4)),scale(multiply(power(x,4),power(y,2)),F(15,2)))
    identity(rows,'all-variable pointwise P3 Cauchy majorant',lhs,rhs)
    need(all(q>=0 for q in rhs.values()),'positive P3 coefficient majorant')
    lhs=add(scale(multiply(power(x,2),power(S,2)),9),scale(power(R3,2),-1))
    rhs=add(scale(power(x,6),8),scale(multiply(power(x,4),power(y,2)),24))
    identity(rows,'all-variable pointwise ReU3 Cauchy majorant',lhs,rhs)
    need(all(q>=0 for q in rhs.values()),'positive ReU3 coefficient majorant')
    # Whole fourth norm identity is reconstructed without centering: each
    # squared norm is nonnegative before the Cauchy bridge.
    rawN=[norm(z) for z in roots];rawV=add(*rawN)
    identity(rows,'full8 fourth norm dominance identity',
        add(power(rawV,2),scale(add(*(power(z,2) for z in rawN)),-1)),
        scale(add(*(multiply(rawN[i],rawN[j]) for i in range(8) for j in range(i))),2))
    # Reviewer9845's UNIVERSAL centered quartic SOS, reconstructed from all
    # eight arbitrary complex variables after centering. No eta/domain is
    # involved, and positivity comes from the displayed products of norms.
    centered_norms=[norm(z) for z in nu]
    sos={}
    for j in range(8):
        others=[k for k in range(8) if k!=j]
        pairsum=add(*(norm(gadd(nu[k],gscale(nu[l],-1)))
            for i,k in enumerate(others) for l in others[i+1:]))
        identity(rows,'whole other-seven centered pair identity '+str(j),
            add(scale(V,7),scale(centered_norms[j],-8)),pairsum)
        sos=add(sos,multiply(centered_norms[j],pairsum))
    identity(rows,'whole centered quartic SOS credited9845',
        add(scale(power(V,2),7),scale(add(*(power(z,2) for z in centered_norms)),-8)),sos)
    b=budgets();K=F(b['K']);t,v=variable(18),variable(19)
    identity(rows,'complete nonnegative-square absorption',
        add(scale(power(t,2),F(1,4)),scale(multiply(t,v),-K)),
        add(power(add(scale(t,F(1,2)),scale(v,-K)),2),scale(power(v,2),-K*K)))
    eta=variable(0);G=F(b['G'])
    identity(rows,'whole quadratic defect after square completion',
        add(scale(power(t,2),F(1,2)),scale(multiply(t,v),-K),scale(power(v,2),-G),scale(power(eta,2),-190)),
        add(scale(power(t,2),F(1,4)),power(add(scale(t,F(1,2)),scale(v,-K)),2),scale(power(v,2),-(G+K*K)),scale(power(eta,2),-190)))
    # Here v represents W_c=sqrt(7/8)*V; retaining physical E/4 and
    # spending all E/2 for the unconditional objective are different routes.
    identity(rows,'whole unconditional square completion',
        add(scale(power(t,2),F(1,2)),scale(multiply(t,v),-K),scale(power(v,2),-G),scale(power(eta,2),-190)),
        add(scale(power(add(t,scale(v,-K)),2),F(1,2)),scale(power(v,2),-(G+K*K/2)),scale(power(eta,2),-190)))
    # Ninth-root coefficients of actual paired third moments, all phases.
    phase=[]
    for k in range(1,5):
        w=np(NW,k);wb=nc(w)
        coeff=ns(na(np(w,-3%9),np(wb,-3%9),ns(N1,-2)),F(1,36))
        target=N0 if k==3 else ns(N1,F(-1,12)) if k==4 else coeff
        need(coeff==target,'entire paired cubic coefficient')
        phase.append({'phase':k,'all6_field_coefficients':[str(q) for q in coeff]})
    rows.append({'name':'entire actual paired cubic phase coefficient table','rows':phase})
    c=ns(na(np(NW,4),np(NW,5)),F(-1,2));d=na(ns(np(c,2),2),ns(N1,-1))
    w4=ni(na(c,d));w3=ns(na(ns(N1,7),ns(nm(na(N1,ns(d,-1)),w4),-1)),F(2,3))
    yy=ns(ni(na(N1,c)),F(1,3));xx=na(ns(N1,F(2,3)),ns(yy,-1));CC=na(ns(N1,F(8,3)),yy)
    for name,lhs,rhs in (
        ('prior exact mean dual',na(nm(w3,ns(N1,F(3,2))),nm(w4,na(N1,c))),ns(N1,8)),
        ('prior exact trace dual',na(nm(w3,ns(N1,F(3,2))),nm(w4,na(N1,ns(d,-1)))),ns(N1,7)),
        ('prior exact sharp slope',na(ns(N1,8),ns(w3,-1),ns(w4,-1)),CC),
        ('prior exact optimal cube',na(ns(xx,F(3,2)),ns(yy,F(3,2))),N1),
        ('prior exact optimal fourth',na(nm(na(N1,c),xx),nm(na(N1,ns(d,-1)),yy)),N1)):
        need(lhs==rhs,name);rows.append({'name':name,'all6_field_coefficients':[str(q) for q in lhs]})
    eta,M,Q,V=[variable(j) for j in range(4)]
    A3=ns(N1,F(3,2));B3=A3;A4=na(N1,c);B4=na(N1,ns(d,-1))
    L3=za(zm(zf(ns(A3,-1)),zv(M)),zm(zf(ns(B3,F(-1,14))),zv(Q)))
    L4=za(zm(zf(ns(A4,-1)),zv(M)),zm(zf(ns(B4,F(-1,14))),zv(Q)))
    lhs=zv(add(scale(eta,8),scale(M,8),scale(add(V,scale(Q,3)),F(1,4))))
    rhs=za(zm(zf(CC),zv(eta)),zm(zf(w3),za(zv(eta),zs(L3,-1))),
           zm(zf(w4),za(zv(eta),zs(L4,-1))),zv(scale(add(V,Q),F(1,4))))
    zid(rows,'complete physical defect before signed normal substitution',lhs,rhs)
    return rows


def whole_maps():
    # Prior own9801 Gaussian/ninth-root identities are reconstructed whole;
    # the following new post-entry identities are added before finite checks.
    rows=credited_complete_maps()
    t,v,z=variable(0),variable(1),variable(2)
    identity(rows,'whole retained broad mean square',
        add(scale(power(t,2),4),scale(multiply(t,v),F(-16,15)),scale(power(v,2),F(-16,3))),
        add(scale(power(add(t,scale(v,F(-2,15))),2),4),scale(power(v,2),F(-1216,225))))
    identity(rows,'whole stronger paired mean square',
        add(scale(power(t,2),4),scale(multiply(t,v),F(-16,15)),scale(power(v,2),F(-64,15))),
        add(scale(power(add(t,scale(v,F(-2,15))),2),4),scale(power(v,2),F(-976,225))))
    K=F(budgets()['variance_K'])
    identity(rows,'whole real-energy square in V5 bootstrap',
        add(scale(power(z,2),F(5,14)),scale(multiply(z,v),-K),scale(power(v,2),F(7,10)*K*K)),
        scale(power(add(z,scale(v,F(-7,5)*K)),2),F(5,14)))
    Q=variable(3)
    identity(rows,'whole cube variance and real-energy decomposition',
        add(scale(v,F(1,4)),scale(Q,F(3,4)),scale(Q,F(-4,7))),
        add(scale(v,F(1,14)),scale(add(v,Q),F(5,28))))
    eta=variable(4)
    identity(rows,'whole joint trace conic after12eta constraint',
        add(power(add(scale(eta,12),scale(Q,-5)),2),scale(power(Q,2),-49)),
        add(scale(power(eta,2),294),scale(power(add(Q,scale(eta,F(5,2))),2),-24)))
    # The full early/final individual-slack substitution uses independently
    # variable a^3/r^3. No narrow radial box is assumed by this identity.
    av,eta,t2,V,Q,rinv,Tail=[variable(j) for j in range(7)]
    acube=power(av,3);ratio=multiply(acube,rinv)
    inserted_M=add(scale(multiply(acube,eta),F(-15,16)),scale(t2,F(3,4)),
                   scale(multiply(ratio,add(V,scale(Q,3))),F(-3,64)),
                   scale(multiply(acube,Tail),F(3,16)))
    lhs=add(eta,scale(power(eta,2),F(-1,2)),inserted_M,scale(t2,F(-3,2)),scale(Q,F(3,28)))
    rhs=add(eta,scale(power(eta,2),F(-1,2)),scale(multiply(acube,eta),F(-15,16)),
            scale(t2,F(-3,4)),scale(V,F(-3,64)),scale(Q,F(-15,448)),
            scale(multiply(add(constant(1),scale(ratio,-1)),add(V,scale(Q,3))),F(3,64)),
            scale(multiply(acube,Tail),F(3,16)))
    identity(rows,'whole individual slack after objective substitution',lhs,rhs)
    return rows


def legendre_routes():
    t=variable(0);rows=[];previous=constant(1);current=t
    for n in range(13):
        recurrence=previous if n==0 else current
        laplace={};series={}
        for j in range(n//2+1):
            laplace=add(laplace,scale(multiply(power(t,n-2*j),power(add(constant(1),scale(power(t,2),-1)),j)),F(comb(n,2*j)*comb(2*j,j)*(-1)**j,4**j)))
        for m in range((n+1)//2,n+1):
            j=n-m;series=add(series,scale(power(t,2*m-n),F(comb(2*m,m)*comb(m,j)*2**(2*m-n)*(-1)**j,4**m)))
        identity(rows,'whole Legendre coefficient n'+str(n)+' Laplace/recurrence',laplace,recurrence)
        identity(rows,'whole Legendre coefficient n'+str(n)+' binomial/recurrence',series,recurrence)
        if n>=1:
            previous,current=current,scale(add(scale(multiply(t,current),2*n+1),scale(previous,-n)),F(1,n+1))
    # Complete telescoping controls corroborate the general finite identity.
    # ALL N, convergence and the Legendre bound are proved in PROOF.md;
    # these particular degrees are not a completeness premise.
    z=variable(1)
    for N in (0,1,5,12):
        whole=add(*(power(z,j+4) for j in range(N+1)))
        identity(rows,'whole degree4 geometric telescoping N'+str(N),
            multiply(add(constant(1),scale(z,-1)),whole),
            add(power(z,4),scale(power(z,N+5),-1)))
    return rows


def literal_controls():
    def addz(*xs):return tuple(sum(z[j] for z in xs) for j in range(2))
    def mulz(z,w):return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
    def sz(z,c):return z[0]*c,z[1]*c
    def powerz(z,n):
        out=(F(1),F(0))
        for _ in range(n):out=mulz(out,z)
        return out
    controls=[[(F(0),F(0))]*8,
      [(F(0),F(j-3,100)) for j in range(7)]+[(F(0),F(-sum(j-3 for j in range(7)),100))],
      [(F(j-3,120),F((j*j)%7-3,150)) for j in range(8)],
      [(F(1,100),F(1,90))]*4+[(F(-1,100),F(-1,90))]*4,
      [(F(0),F(1,64))]*7+[(F(0),F(-7,64))]]
    rows=[]
    for index,zs in enumerate(controls):
        mean=sz(addz(*zs),F(1,8));nu=[addz(z,sz(mean,-1)) for z in zs]
        u=(F(7,8),F(0)) if index in (0,1,4) else (F(9,10),F(1,20))
        ub=(u[0],-u[1]);r2=sum(q*q for q in u);rot=[mulz(z,ub) for z in nu]
        V=sum(sum(q*q for q in z) for z in nu)
        T=addz(*(powerz(z,2) for z in nu));U=addz(*(powerz(z,3) for z in nu))
        e3=addz(*(mulz(mulz(nu[i],nu[j]),nu[k]) for i in range(8) for j in range(i) for k in range(j)))
        need(sz(e3,3)==U,'literal complete centered Newton')
        Q,J=sz(mulz(T,powerz(ub,2)),1/r2)
        energy=sum(z[0]**2 for z in rot)/r2
        need(2*energy==V+Q,'literal rotated real energy')
        real3=sum(z[0]**3-3*z[0]*z[1]**2 for z in rot)
        p3=sum(z[0]**3-F(3,2)*z[0]*z[1]**2 for z in rot)
        need(real3==mulz(U,powerz(ub,3))[0],'literal whole rotated ReU3')
        need(p3*p3<=F(9,4)*V*V*energy*r2**3,'literal cubic Cauchy bound')
        need(real3*real3<=9*V*V*energy*r2**3,'literal real-third Cauchy bound')
        rows.append({'index':index,'complete_critical_multiset':[[str(x),str(y)] for x,y in zs],
            'u':[str(x) for x in u],'V':str(V),'E':str(energy),'Q':str(Q),'J':str(J),
            'U3':[str(x) for x in U],'P3_cleared':str(p3),'ReU3_cleared':str(real3),
            'original_disk_or_low_sublevel_asserted':False})
    return rows


def damages():
    rows=[]
    def rejected(name,work):
        try:work()
        except CertificateError as exc:rows.append({'name':name,'reason':str(exc)});return
        raise CertificateError('damaged certificate accepted: '+name)
    x,y=variable(0),variable(1)
    right=add(power(x,3),scale(multiply(x,power(y,2)),F(-3,2)))
    rejected('wrong full Legendre cubic sign',lambda:identity([],'P3 sign',add(power(x,3),scale(multiply(x,power(y,2)),F(3,2))),right))
    rejected('cubic norm coefficient1 is insufficient',lambda:need(F(23)**2<=F(17)**2,'P3 coefficient1 at(1,4)'))
    rejected('real-third coefficient2 is insufficient',lambda:need(F(242)**2<=4*F(82)**2,'ReU3 coefficient2 at(1,9)'))
    rejected('cancel fourth paired cubic',lambda:need(ns(N1,F(-1,12))==N0,'nonzero fourth cubic'))
    rejected('broad pair normal3/4 is insufficient',lambda:budgets(changes={'pair_cap':F(3,4)}))
    rejected('broad individual normal4/5 is insufficient',lambda:budgets(changes={'individual_cap':F(4,5)}))
    rejected('old final inverse-cube box used early',lambda:budgets(changes={'early_inverse_cube':4}))
    rejected('last absolute-tail stage target6 does not close',lambda:budgets(changes={'last_stage_target':6}))
    rejected('all-phase displacement1/10 is insufficient',lambda:budgets(changes={'all_phase_scale':F(1,10)}))
    rejected('old mean1/800 box at new endpoint',lambda:need(F(1,800)**2>E_MAX/9,'mean radius endpoint fails'))
    rejected('old radial6399/6400 at broadH375',lambda:need(1-(3*E_MAX+F(3,5)*F(1,375))/8>F(6399,6400),'old lower radial box fails'))
    rejected('old centered1/96 radius at new V5',lambda:need(F(1,96)**2>F(7,8)*5*E_MAX,'old complete tail radius fails'))
    rejected('discard reviewed centered gain at physical272',lambda:budgets(changes={'quartic_factor':F(1)}))
    rejected('insufficient physical quadratic error270',lambda:budgets(F(270)))
    rejected('insufficient unconditional quadratic error240',lambda:budgets(changes={'objective_error':F(240)}))
    rejected('wrong centered quartic SOS coefficient',lambda:need(F(7)*56**2-9*2408==7*6*64,'centered quartic SOS at seven1 and minus7'))
    rejected('rename newDelta in oldR3/100 budget',lambda:need(29/ERROR<F(1,100),'old R3 Delta budget fails'))
    rejected('rename newDelta in oldR4/12 budget',lambda:need(33/ERROR<F(1,12),'old R4 Delta budget fails'))
    return rows


def build_record():
    return {'agent':'six-sendov-3','role':'researcher',
        'scope':'ordinary unformalized all9 CLOSED original disk degree9,0<eta<=1/16000,all8 critical multiplicities;9818 H42 and retained mean square BEFORE every fresh local use',
        'claim':'F>8+Ceta-243eta2>8+141eta/50; lowF givesV5 and positive actual Psi(E/4) with physical272; BOTH cuts give fresh Delta272 moment/all9 motion bounds',
        'whole_maps':whole_maps(),'legendre_finite_corroboration':legendre_routes(),
        'budgets':budgets(),'complete_critical_controls':literal_controls(),
        'mathematical_damage_rejections':damages(),
        'ordinary_bridges':['adopted9818 genuine actual energy entry and separate retained mean square',
            'broad nine counted roots and entire actual paired/individual normals',
            'separate EARLY radial box and complex mean, seven genuine variance substitutions',
            'ALLdegree Laplace integral and absolute convergence, NOT a finite coefficient inference',
            'TWO signed-cubic variance squares, fine counted roots and full nonlinear all-phase normals',
            'fresh sharp quadratic square and all-parameter case coverage',
            'BOTH cuts, arbitrary epsilon and full complex moment/all9 original-root inequalities']}


def pairs(xs):
    out={}
    for k,v in xs:
        if k in out:raise CertificateError('duplicate JSON key')
        out[k]=v
    return out


def reject_constant(s):raise CertificateError('nonfinite JSON constant '+s)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fixture',type=Path)
    parser.add_argument('--emit',action='store_true');args=parser.parse_args()
    record=build_record();fixture=args.fixture or Path(__file__).with_name('EXPECTED.json')
    if args.emit:
        need(args.fixture is None,'emit cannot target external fixture')
        fixture.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    else:
        wanted=json.loads(fixture.read_text(),object_pairs_hook=pairs,parse_constant=reject_constant)
        need(canonical(record)==canonical(wanted),'complete typed record mismatch')
    print(json.dumps({'status':'PASS','whole_record_sha256':sha256(canonical(record)).hexdigest(),
        'whole_identity_records':len(record['whole_maps']),
        'complete_Legendre_comparisons':len(record['legendre_finite_corroboration']),
        'strict_rational_margins':len(record['budgets']['rows']),
        'complete_arbitrary_critical_controls':len(record['complete_critical_controls']),
        'rejected_mathematical_damages':len(record['mathematical_damage_rejections'])},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (CertificateError,ValueError,OSError) as exc:
        print('CHECK FAILED: '+str(exc),file=sys.stderr);sys.exit(1)
