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

E_MAX = F(1, 65536)
A_MIN = 1-E_MAX
TAU = F(1, 96)
ERROR = F(390)


def budgets(error=ERROR):
    a=A_MIN
    G=1/((a-TAU)*a**4)
    K=F(3,2)/a**4+F(3,20)/a
    rows=[]
    def positive(name,q):
        q=F(q);need(q>0,'budget: '+name)
        rows.append({'name':name,'strict_margin':str(q)})
    positive('all centered criticals inside complete tail radius',TAU**2-6*E_MAX)
    positive('positive infinite-tail denominator',a-TAU)
    positive('quadratic objective after complete square absorption',error-252-36*(G+K*K))
    positive('uniform 14/5 slope after high-objective split',F(17,6)-error*E_MAX-F(14,5))
    positive('sqrt390 greater than19',error-19**2)
    positive('cube residual plus slack below3gap/8',F(3,8)-F(1,4)-40/error)
    positive('fourth residual including signed cubic belowgap/2',F(1,2)-46/error-3/(19*a))
    M=F(62,651)*F(3,8)+F(128,217)*F(5,2)
    Y=F(24832,32550)*F(3,8)+F(128,217)*F(5,2)
    positive('real mean inversion below8gap/5',F(8,5)-M)
    positive('negative rotated trace inversion below9gap/5',F(9,5)-Y)
    positive('rotated trace difference below26gap',26-14*F(9,5))
    positive('critical energy difference below35gap',35-34-8*F(169,225)/error)
    positive('unrotated real energy below13gap',13-12-F(384,25)/error-4*E_MAX/(error*a*a))
    positive('imaginary mean sqrt coefficient below1',196*a*a-96)
    positive('imaginary mean gap coefficient below1',1-F(7,24)/a)
    positive('imaginary mean eta2 coefficient below44',44-F(259,6)/a)
    positive('original motion eta2 aggregate below125',125-88-36-F(896,1395)/a)
    positive('all9 original motion gap coefficient below10',10-F(26,5)-F(26,7)/a-125/error)
    positive('all9 original motion sqrt coefficient below4',4-2-F(10,7)/a-F(55,684)/(a*a))
    positive('sqrt96 below10',100-96)
    positive('complete cubic absolute norm coefficient',F(9,4)-1)
    positive('full noncubic40 plus40w3 plus46w4 below252',252-40-40*F(23,5)-46*F(3,5))
    R3=F(1,2)+F(3,2)*F(4,5)+F(3,2)*F(169,225)+F(13,15)+36
    R4=F(1,2)+2*F(4,5)+2*F(169,225)+F(13,15)*6/4+F(9,8)*36
    positive('credited complete cube remainder40',40-R3)
    positive('credited complete fourth remainder46 without cubic',46-R4)
    positive('credited objective normal conversion40',40-8*F(4,5)*(2-E_MAX)/a**2-4*F(169,225)/a**3-24)
    positive('strict selected cosine lower sign',-(8*F(15,16)**3-6*F(15,16)-1))
    positive('strict selected cosine upper sign',8*F(47,50)**3-6*F(47,50)-1)
    positive('positive Cramer determinant lower floor',F(651,256))
    return {'G':str(G),'K':str(K),'eta_endpoint':str(E_MAX),'error':str(error),'rows':rows}


def whole_maps():
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
    b=budgets();K=F(b['K']);t,v=variable(18),variable(19)
    identity(rows,'complete nonnegative-square absorption',
        add(scale(power(t,2),F(1,4)),scale(multiply(t,v),-K)),
        add(power(add(scale(t,F(1,2)),scale(v,-K)),2),scale(power(v,2),-K*K)))
    eta=variable(0);G=F(b['G'])
    identity(rows,'whole quadratic defect after square completion',
        add(scale(power(t,2),F(1,2)),scale(multiply(t,v),-K),scale(power(v,2),-G),scale(power(eta,2),-252)),
        add(scale(power(t,2),F(1,4)),power(add(scale(t,F(1,2)),scale(v,-K)),2),scale(power(v,2),-(G+K*K)),scale(power(eta,2),-252)))
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
        raise CertificateError('mathematical damage accepted: '+name)
    x,y=variable(0),variable(1)
    right=add(power(x,3),scale(multiply(x,power(y,2)),F(-3,2)))
    rejected('wrong full Legendre cubic sign',lambda:identity([],'P3 sign',add(power(x,3),scale(multiply(x,power(y,2)),F(3,2))),right))
    rejected('absolute cubic coefficient1 is insufficient',lambda:need(F(23)**2<=F(17)**2,'P3 coefficient1 fails at(1,4)'))
    rejected('real-third coefficient2 is insufficient',lambda:need(F(242)**2<=4*F(82)**2,'ReU3 coefficient2 fails at(1,9)'))
    rejected('cancel fourth paired cubic',lambda:need(ns(N1,F(-1,12))==N0,'nonzero fourth cubic'))
    rejected('replace newDelta in oldR3 budget',lambda:need(40/ERROR<F(1,100),'oldR3 gap budget does not transfer'))
    rejected('replace newDelta in oldR4 budget',lambda:need(46/ERROR<F(1,12),'oldR4 gap budget does not transfer'))
    rejected('too small uniform quadratic error350',lambda:budgets(F(350)))
    rejected('eta endpoint fourfold without fresh centered radius',lambda:need(TAU**2>24*E_MAX,'extended endpoint violates complete-tail radius'))
    return rows


def build_record():
    return {'agent':'six-sendov-3','role':'researcher',
        'scope':'ordinary unformalized all9 CLOSED original disk degree9,0<eta<=2^-16,all8 critical multiplicities;9731 suppliesH512 BEFORE9620/9671 local use',
        'claim':'F>8+Ceta-390eta2>8+14eta/5; lowF and near-slopeDelta2 give positive actual slack/E/4 and fresh moment/all9 original-motion constants',
        'whole_maps':whole_maps(),'legendre_finite_corroboration':legendre_routes(),
        'budgets':budgets(),'complete_critical_controls':literal_controls(),
        'mathematical_damage_rejections':damages(),
        'ordinary_bridges':['imported actual energy entry and counted original labels',
            'ALLdegree Laplace integral and absolute convergence, NOT inferred from finite coefficients',
            'Cauchy and all-degree geometric majorant','complete actual nonlinear normals from9671',
            'square completion and all-parameter coverage','fresh moment and original-root inequalities']}


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
