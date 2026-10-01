#!/usr/bin/env python3
"""Finite exact checks for the unique analytic degree-nine boundary minimizer.

Standard library only. Analyticity, IFT, uniform root-map coverage, global
comparison and symmetry are written proofs in PROOF.md, not formalized here.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('analytic_algebra', BASE/'algebra.py')
alg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alg)
K, Z, Ring, require, AlgebraError = alg.K, alg.Z, alg.Ring, alg.require, alg.AlgebraError


class Audit:
    def __init__(self):
        self.checks = []
        self.damages = []

    def check(self, ok, label):
        require(ok, label)
        self.checks.append(label)

    def reject(self, function, label):
        try:
            function()
        except AlgebraError:
            self.damages.append(label)
        else:
            raise AlgebraError('damaged identity accepted: '+label)


def constants():
    c = K((0,1,0)); d = 2*c*c-1; v = 2*d*d-1
    y = 1/(3*(1+c)); x = F(2,3)-y
    H = 14*y; U = -8*x; rho = (c-5)/3; L = -7*(2*c+1)/18
    uz = (U+rho*H)/8; up = uz-rho*H/2
    w4 = 1/(c+d); w3 = F(2,3)*(7-(1-d)*w4)
    sig = K(F(3,8))-(F(3,2)*w3+(1-v)*w4)/20
    K0 = K((-F(2609,405),-F(2000,81),F(12964,405)))
    B = K((F(2311,108),F(4934,27),-F(1976,9)))
    return dict(c=c,d=d,v=v,y=y,x=x,H=H,U=U,rho=rho,L=L,uz=uz,up=up,
                w3=w3,w4=w4,sig=sig,K0=K0,B=B,C=K(F(8,3))+y)


def isolate():
    lo, hi = F(3,4), F(1)
    f = lambda t: 8*t*t*t-6*t-1
    require(f(lo)<0<f(hi), 'embedding isolating bracket')
    for _ in range(110):
        mid = (lo+hi)/2
        if f(mid)<0:
            lo=mid
        else:
            hi=mid
    require(24*lo*lo-6>0, 'unique increasing real embedding')
    return lo, hi


def generic_jet(scale=9, anchor_damage=False):
    names = ['eps','z','U','H','V','M','J3','J21','J4','W','D']
    r = Ring(names,4,axis=0)
    e,z,U,H,V,M,J3,J21,J4,W,D = [r.variable(n) for n in names]
    add,mul,pow,sc,C = r.add,r.mul,r.power,r.scale,r.constant
    moment = {1:add(mul(pow(e,2),U),sc(mul(pow(e,3),V),0,1),mul(pow(e,4),W)),
              2:add(sc(mul(pow(e,2),H),-1),sc(mul(pow(e,3),M),0,2),mul(pow(e,4),D)),
              3:add(sc(mul(pow(e,3),J3),0,-1),sc(mul(pow(e,4),J21),-3)),
              4:mul(pow(e,4),J4)}
    elementary=[C(1)]
    for n in range(1,9):
        row={}
        for k in range(1,n+1):
            row=add(row,sc(mul(elementary[n-k],moment.get(k,{})),F((-1)**(k-1),n)))
        elementary.append(row)
    primitive={}
    derivative={}
    for n in range(9):
        primitive=add(primitive,sc(mul(elementary[n],pow(z,9-n)),F(scale*(-1)**n,9-n)))
        derivative=add(derivative,sc(mul(elementary[n],pow(z,8-n)),scale*(-1)**n))
    anchor=add(C(1),sc(pow(e,2),-1))
    if anchor_damage:
        anchor=add(anchor,pow(e,3))
    p=add(primitive,sc(r.substitute(primitive,'z',anchor),-1))
    zm = lambda n: add(pow(z,n),C(-1))
    g2=add(C(9),sc(mul(U,zm(8)),-F(9,8)),sc(mul(H,zm(7)),F(9,14)))
    I3=add(sc(mul(V,zm(8)),-F(9,8)),sc(mul(M,zm(7)),-F(9,7)),
           sc(mul(J3,zm(6)),F(1,2)))
    g4=add(C(-36),sc(U,-9),sc(H,F(9,2)),sc(mul(W,zm(8)),-F(9,8)),
           sc(mul(add(pow(U,2),sc(D,-1)),zm(7)),F(9,14)),
           mul(add(sc(mul(U,H),-F(3,4)),sc(J21,F(3,2))),zm(6)),
           mul(add(sc(pow(H,2),F(9,40)),sc(J4,-F(9,20))),zm(5)))
    expected=add(zm(9),mul(pow(e,2),g2),sc(mul(pow(e,3),I3),0,1),mul(pow(e,4),g4))
    return r,p,expected,derivative,anchor


def distance_jet(binomial=F(3,8)):
    r = Ring(['eta','u','h2'],2,axis=0)
    eta,u,h2=[r.variable(n) for n in r.names]
    add,mul,pow,sc,C=r.add,r.mul,r.power,r.scale,r.constant
    v=add(C(1),u)
    squared=add(C(1),sc(mul(eta,v),-2),mul(eta,h2),mul(pow(eta,2),pow(v,2)))
    q=add(squared,C(-1))
    out=add(C(1),sc(q,-F(1,2)),sc(pow(q,2),binomial))
    expected=add(C(1),mul(eta,add(v,sc(h2,-F(1,2)))),
                 mul(pow(eta,2),add(pow(v,2),sc(mul(v,h2),-F(3,2)),sc(pow(h2,2),F(3,8)))))
    return r,out,expected


def tangent(k, mixed_denominator=2, real_weight=F(1,2)):
    names=['t'+str(j) for j in range(6)]+['r'+str(j) for j in range(6)]
    r=Ring(names,2)
    t=[r.variable(n) for n in names[:6]]; dr=[r.variable(n) for n in names[6:]]
    add,mul,pow,sc,C=r.add,r.mul,r.power,r.scale,r.constant
    S=add(*t); T2=add(*(pow(q,2) for q in t)); R=add(*dr)
    mh=sc(S,-F(1,2))
    correction=add(sc(T2,F(1,4)),sc(pow(S,2),F(1,8)))
    sh=add(C(1),sc(correction,-1)); inv_sh=add(C(1),correction)
    hp=add(mh,sh); hm=add(mh,sc(sh,-1))
    hs=[hp,hm]+t
    J3=add(*(pow(q,3) for q in hs))
    mu=add(C(k['up']),sc(R,-F(1,2)))
    usmall=[add(C(k['uz']),q) for q in dr]
    small_mixed=add(*(mul(q,u) for q,u in zip(t,usmall)))
    numerator=add(sc(J3,k['L']*k['H']/2),sc(mul(mh,mu),-2),sc(small_mixed,-1))
    du=sc(mul(numerator,inv_sh),F(1,mixed_denominator))
    us=[add(mu,du),add(mu,sc(du,-1))]+usmall
    Hnorm=add(*(pow(q,2) for q in hs))
    Um=add(*us); mixed=add(*(mul(q,u) for q,u in zip(hs,us)))
    J21=sc(add(*(mul(pow(q,2),u) for q,u in zip(hs,us))),k['H']/2)
    J4=sc(add(*(pow(q,4) for q in hs)),k['H']*k['H']/4)
    U2=add(*(pow(q,2) for q in us))
    cost=add(C(k['K0']),sc(U2,real_weight),sc(J21,k['rho']),sc(J4,k['sig']))
    a=(k['rho']*k['rho']-2*k['sig'])*k['H']*k['H']/4
    D=-(k['rho']+3*k['L'])*k['H']/4
    b=D*D-k['rho']*k['H']*D+k['sig']*k['H']*k['H']/2
    expected=add(C(k['B']),sc(T2,a),sc(pow(S,2),b),
                 sc(add(*(pow(q,2) for q in dr)),F(1,2)),sc(pow(R,2),F(1,4)))
    return dict(ring=r,cost=cost,expected=expected,Hnorm=Hnorm,Um=Um,
                hsum=add(*hs),mixed=mixed,mixed_expected=sc(J3,k['L']*k['H']/2),
                a=a,b=b,dimension=12)


def root_jet(k, omega, curvature_factor=F(1,2)):
    U,H,x,y=k['U'],k['H'],k['x'],k['y']
    g2=Z(9,q=omega.q)-(omega**8-1)*(9*U/8)+(omega**7-1)*(9*H/14)
    g2p=omega**7*(-9*U)+omega**6*(F(9,2)*H)
    t2=-g2*omega/9
    g4=Z(-36-9*U+F(9,2)*H,q=omega.q)+(omega**7-1)*(F(9,14)*U*U) \
       -(omega**6-1)*(F(3,4)*U*H)+(omega**5-1)*(F(9,40)*H*H)
    t4=-(g4+g2p*t2+36*omega**7*t2*t2)*omega/9
    first=(omega.conj()*t2).real_field()
    second=(omega.conj()*t4+curvature_factor*t2*t2.conj()).real_field()
    A=1-omega.real_field(); B=1-(omega**2).real_field()
    C6=1-(omega**6).real_field(); C5=1-(omega**5).real_field()
    T0=4+U-H/2+B*U*U/14-C6*U*H/12+C5*H*H/40
    # Root curvature computed separately from the generic Taylor terms.
    ratio=-1 if A==F(3,2) else -2*k['c']
    sin2=omega.q
    curvature=-(F(7,2)*x*x+6*x*y*ratio+F(5,2)*y*y*ratio*ratio)*sin2
    return dict(first=first,second=second,expected=T0+curvature,A=A,B=B,C6=C6,C5=C5,
                t2=t2,t4=t4,curvature=curvature)


def build(audit):
    k=constants(); lo,hi=isolate(); c=k['c']
    audit.check(8*c**3-6*c-1==0,'cubic embedding polynomial')
    audit.check(k['H'].interval(lo,hi)[0]>0,'positive H0')
    audit.check(6*k['uz']+2*k['up']==k['U'],'optimizer mean')
    audit.check(k['w3']*F(3,2)/8+k['w4']*(1+c)/8==1,'even dual U')
    audit.check(k['w3']*F(3,2)/14+k['w4']*(1-k['d'])/14==F(1,2),'even dual H')
    audit.check(8-k['w3']-k['w4']==k['C'],'first slope dual')
    for name in ('w3','w4'):
        audit.check(k[name].interval(lo,hi)[0]>0,'positive '+name)
    even_rows=[]; odd_rows=[]; root_records={}; T=[]
    for index,cosine in enumerate((k['d'],k['v'],K(-F(1,2)),-c),1):
        q=1-cosine*cosine; omega=Z((cosine,0,0,1),q=q)
        audit.check(omega**9==1,'nonagon branch '+str(index))
        audit.check(q.interval(lo,hi)[0]>0,'positive branch sine '+str(index))
        positive=root_jet(k,omega)
        negative=root_jet(k,omega.conj())
        audit.check(positive['first']==negative['first'],'conjugate first radial '+str(index))
        if index<=2:
            audit.check(positive['first'].interval(lo,hi)[1]<0,'strict inactive root '+str(index))
        else:
            audit.check(positive['first']==0,'zero active first radial '+str(index))
            audit.check(positive['second']==positive['expected'],'active root curvature '+str(index))
            audit.check(negative['second']==positive['second'],'conjugate second radial '+str(index))
            row=(-positive['A']/8,positive['B']/14)
            even_rows.append(row)
            # Divide the leading odd radial by the positive sine, using the
            # s*i coordinate. The V,M,J3 columns are derived from omega powers.
            row3=[]
            for polynomial in (-F(9,8)*(omega**8-1),-F(9,7)*(omega**7-1),F(1,2)*(omega**6-1)):
                audit.check(polynomial.a[2]==0,'odd row has no constant imaginary component')
                row3.append(polynomial.a[3]/9)
            odd_rows.append(tuple(row3))
            T.append(positive)
        for sign,entry in (('+',positive),('-',negative)):
            root_records[str(index)+sign]=entry['first'].record()
    root_records['marked']=K(-1).record()
    audit.check(odd_rows[0]==(K(F(1,8)),K(-F(1,7)),K(0)),'inner odd normalized row')
    audit.check(odd_rows[1]==(K(F(1,8)),-2*c/7,(1-4*c*c)/18),'outer odd normalized row')
    detE=even_rows[0][0]*even_rows[1][1]-even_rows[0][1]*even_rows[1][0]
    detO=odd_rows[0][0]*odd_rows[1][1]-odd_rows[0][1]*odd_rows[1][0]
    audit.check(detE==3*(c+k['d'])/224,'even normal determinant')
    audit.check(detO==(1-2*c)/56,'odd normal determinant')
    audit.check(detE.interval(lo,hi)[0]>0,'even determinant positive')
    audit.check(detO.interval(lo,hi)[1]<0,'odd determinant negative')
    audit.check(k['L']==7*(1-4*c*c)/(18*(2*c-1)),'mixed normal constraint M=LJ3')
    K0=8+2*k['U']-F(3,2)*k['H']+k['w3']*T[0]['second']+k['w4']*T[1]['second']
    rho=-F(3,2)+(k['w3']*T[0]['C6']+k['w4']*T[1]['C6'])/6
    sig=K(F(3,8))-(k['w3']*T[0]['C5']+k['w4']*T[1]['C5'])/20
    audit.check(K0==k['K0'],'finite zero-slack cost constant')
    audit.check(rho==k['rho'],'finite zero-slack mixed coefficient')
    audit.check(sig==k['sig'],'finite zero-slack fourth-moment coefficient')
    jet,p,expected,derivative,anchor=generic_jet()
    audit.check(p==expected,'generic Newton anchored polynomial through epsilon4')
    audit.check(not jet.substitute(p,'z',anchor),'generic exact anchor through epsilon4')
    audit.check(not jet.coefficient(p,'eps',1),'no epsilon first coefficient')
    audit.check(all((e[0]%2==0 and v[1]==0) or (e[0]%2==1 and v[0]==0)
                    for e,v in p.items()),'whole coefficient conjugation parity')
    dr,out,expectedD=distance_jet()
    audit.check(out==expectedD,'exact reciprocal through eta2')
    tangent_data=tangent(k); r=tangent_data['ring']
    audit.check(not tangent_data['hsum'],'finite tangent balance')
    audit.check(tangent_data['Hnorm']==r.constant(2),'finite tangent sphere')
    audit.check(tangent_data['Um']==r.constant(k['U']),'finite tangent real mean')
    audit.check(tangent_data['mixed']==tangent_data['mixed_expected'],'finite tangent mixed constraint')
    audit.check(tangent_data['cost']==tangent_data['expected'],'full twelve-variable finite Hessian')
    audit.check(all(sum(e)!=1 for e in tangent_data['cost']),'zero finite tangent gradient')
    aa,bb=tangent_data['a'],tangent_data['b']
    audit.check(aa==K((-F(11564,405),-F(20482,81),F(123284,405))),'exact transverse imaginary coefficient')
    audit.check(bb==K((F(49,180),-F(105889,486),F(305123,1215))),'exact summed imaginary coefficient')
    audit.check(aa.interval(lo,hi)[0]>0,'positive transverse imaginary eigenvalue')
    audit.check((aa+6*bb).interval(lo,hi)[0]>0,'positive longitudinal imaginary eigenvalue')
    audit.check(F(1,2)>0 and F(1,2)+6*F(1,4)>0,'both real block eigenvalues positive')
    Dh=2*(aa+bb)/k['H']
    audit.check(Dh.interval(lo,hi)[0]>0,'positive exact small-imaginary splitting cost')
    # Meaningful mathematical damage controls; all requirements remain active
    # under Python optimization. They do not formalize the analytic proof.
    audit.reject(lambda:require(generic_jet(scale=8)[1]==generic_jet()[2],'wrong degree normalization'),
                 'derivative normalization8')
    damaged=generic_jet(anchor_damage=True)
    audit.reject(lambda:require(damaged[1]==damaged[2],'wrong anchor jet'),'wrong epsilon3 anchor')
    audit.reject(lambda:require(odd_rows[0][1]/2==K(-F(1,7)),'missing mixed odd half'),'odd mixed moment halved')
    damagedD=distance_jet(F(1,3))
    audit.reject(lambda:require(damagedD[1]==damagedD[2],'wrong reciprocal binomial'),'reciprocal binomial3/8 changed')
    omega3=Z((-F(1,2),0,0,1),q=F(3,4))
    damagedR=root_jet(k,omega3,curvature_factor=0)
    audit.reject(lambda:require(damagedR['second']==damagedR['expected'],'missing root modulus curvature'),
                 'root square curvature omitted')
    damagedT=tangent(k,mixed_denominator=1)
    audit.reject(lambda:require(damagedT['mixed']==damagedT['mixed_expected'],'wrong mixed reconstruction'),
                 'mixed chart denominator changed')
    damagedT2=tangent(k,real_weight=1)
    audit.reject(lambda:require(damagedT2['cost']==damagedT2['expected'],'wrong finite real Hessian'),
                 'finite real square doubled')
    without_sum=r.add(tangent_data['expected'],r.scale(r.power(r.add(*(r.variable('t'+str(j)) for j in range(6))),2),-bb))
    audit.reject(lambda:require(tangent_data['cost']==without_sum,'missing summed imaginary coupling'),
                 'imaginary sum coupling omitted')
    return dict(schema='analytic-boundary-v1',author='six-sendov-3',role='researcher',
                arithmetic='Q[c]/(8c^3-6c-1), largest real embedding; Gaussian quadratic extensions',
                embedding_interval=[str(lo),str(hi)],constants={name:value.record() for name,value in sorted(k.items())},
                even_normal_rows=[[v.record() for v in row] for row in even_rows],
                odd_normal_rows=[[v.record() for v in row] for row in odd_rows],
                even_normal_determinant=detE.record(),odd_normal_determinant=detO.record(),
                full_normal_determinant=(detE*detO).record(),
                first_radials_all_nine=root_records,
                second_active_radials=[entry['second'].record() for entry in T],
                generic_variables=jet.names,generic_polynomial=jet.record(p),generic_derivative=jet.record(derivative),
                generic_polynomial_hash=jet.digest(p),distance_variables=dr.names,distance_jet=dr.record(out),
                tangent_variables=r.names,tangent_quadratic=r.record(tangent_data['cost']),
                tangent_quadratic_hash=r.digest(tangent_data['cost']),
                tangent_a=aa.record(),tangent_b=bb.record(),tangent_longitudinal=(aa+6*bb).record(),
                small_imaginary_split_coefficient=Dh.record(),
                finite_imaginary_dimension=6,finite_real_dimension=6,
                analytic_gap_hessian_lower_bound='1/64 in raw free coordinates, inherited finite1/128 gap',
                proved_by_code='Finite identities and signs only; PROOF.md supplies ordinary analytic arguments.',
                check_labels=audit.checks,damage_labels=audit.damages)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--fixture',type=Path,default=BASE/'expected.json')
    parser.add_argument('--write',action='store_true',help='Development regeneration, not independent verification')
    args=parser.parse_args()
    audit=Audit(); record=build(audit)
    # Normalize tuple/list representations before exact fixture comparison.
    record=json.loads(json.dumps(record))
    raw=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
    if args.write:
        args.fixture.write_bytes(raw)
    else:
        try:
            expected=json.loads(args.fixture.read_text())
        except (OSError,ValueError) as exc:
            raise AlgebraError('missing or malformed expected record') from exc
        require(expected==record,'complete expected record mismatch')
    print(f'PASS: {len(audit.checks)} exact checks; {len(audit.damages)} mathematical damages rejected.')
    print('Record SHA256 '+sha256(raw).hexdigest())
    print('Finite normal inversion and full12-variable positive Hessian; analytic bridges remain written proof.')


if __name__=='__main__':
    main()
