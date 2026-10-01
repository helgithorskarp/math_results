#!/usr/bin/env python3
"""Standalone finite exact audit of the reduced continuation and C5.

The ordinary analytic proof and universal-competitor coverage are in
PROOF.md and the cited structural parent8921. This checker verifies finite
identities, not the implicit function theorem or a positive collar width.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

BASE=Path(__file__).resolve().parent


def load(name):
    spec=importlib.util.spec_from_file_location(name,BASE/(name+'.py'))
    obj=importlib.util.module_from_spec(spec)
    sys.modules[name]=obj
    spec.loader.exec_module(obj)
    return obj


ar=load('arithmetic');series=load('series');red=load('reduction');root=load('root_audit')
K,Z,require,AlgebraError=ar.K,ar.Z,ar.require,ar.AlgebraError


class Audit:
    def __init__(self):
        self.checks=[]
        self.damages=[]

    def check(self,ok,label):
        require(ok,label)
        self.checks.append(label)

    def reject(self,function,label):
        try:
            function()
        except AlgebraError:
            self.damages.append(label)
        else:
            raise AlgebraError('mathematical damage accepted: '+label)


def embedding():
    lo,hi=F(3,4),F(1)
    f=lambda x:8*x*x*x-6*x-1
    require(f(lo)<0<f(hi),'real cubic embedding bracket')
    for _ in range(120):
        mid=(lo+hi)/2
        if f(mid)<0:
            lo=mid
        else:
            hi=mid
    require(f(lo)<0<f(hi) and 24*lo*lo>6,'unique cubic embedding interval')
    return lo,hi


def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':')).encode()


def evaluate(poly,value):
    result=type(value)(0)
    for row in reversed(poly):
        result=result*value+row
    return result


def run():
    audit=Audit();C=red.constants();c=C['c'];d=C['d']
    lo,hi=embedding()
    audit.check(8*c**3-6*c-1==0,'exact cubic relation')
    norm=[[-K(F(3,2))/4,K(F(3,2))/7],[-(1+c)/4,(1-d)/7]]
    det=norm[0][0]*norm[1][1]-norm[0][1]*norm[1][0]
    audit.check(det==3*(c+d)/56,'displayed two-normal scaled determinant')
    audit.check(det.interval(lo,hi)[0]>0,'scaled normal determinant strictly positive')
    obj,params,trace=red.solve(5,[C['uz'],C['alpha']],audit=audit)
    S=type(obj);eta=S([0,1])
    sparse=red.polynomial(eta,params['u0'],params['u1'],params['T'])
    direct=root.factor_integrate(eta,params['u0'],params['u1'],params['T'])
    for j in range(10):
        audit.check(sparse[j]==direct[j],'independent factor/integrate polynomial coefficient z^'+str(j))
    audit.check(evaluate(direct,1-eta)==0,'exact marked-root anchoring through fifth order')
    known=[K(8),K(F(8,3))+C['H']/14,
        K((F(2311,108),F(4934,27),-F(1976,9))),
        K((-F(60800959,17496),-F(307083769,17496),F(10980067,486))),
        K((F(340367352475,839808),F(808137564635,419904),-F(1052841914857,419904)))]
    for j,coefficient in enumerate(known):
        audit.check(obj.a[j]==coefficient,'prior objective coefficient eta^'+str(j)+' reproduced')
    C5=K((-F(8304485822364161,181398528),-F(6510273073800785,30233088),F(2123849893841477,7558272)))
    audit.check(obj.a[5]==C5,'displayed exact fifth objective coefficient')
    bound=C5.interval(lo,hi)
    audit.check(F(-3636117842,10**6)<bound[0]<=bound[1]<F(-3636117840,10**6),
        'certified fifth coefficient enclosure')
    audit.check(bound[1]<0,'fifth coefficient strictly negative')

    # Parameter derivatives use a separate dual-number variable. No finite
    # difference or fitted numerical derivative is used.
    Dual2=series.series_ring(2,K)
    g0,_,_=red.solve(2,[Dual2([C['uz'],1])],coefficient=Dual2)
    audit.check(g0.a[2].a==(known[2],K(0),K(12)),
        'reduced leading finite cost Bstar+12*(u0-uz)^2')
    Dual1=series.series_ring(1,K)
    g1,_,_=red.solve(3,[Dual1([C['uz'],1])],coefficient=Dual1)
    audit.check(g1.a[3].a[0]==known[3],'reduced cubic cost at the base profile')
    l1=K((F(79312,81),F(902885,162),-F(187712,27)))
    audit.check(g1.a[3].a[1]==l1,'complete reduced cubic derivative')
    audit.check(l1==-24*C['alpha'],'known first minimizing jet recovered from scalar stationarity')
    shifted,_,_=red.solve(5,[C['uz'],C['alpha'],1])
    audit.check(shifted.a==obj.a,'second small-real jet cancels through the complete fifth objective coefficient')
    nonoptimal,_,_=red.solve(4,[C['uz'],C['alpha']+1])
    audit.check(nonoptimal.a[4]==known[4]+12,'off-stationary first jet has exact fourth-order penalty12')

    root_records=[]
    for k,cosine,q,sine in [(3,K(-F(1,2)),K(3),F(1,2)),
                           (4,-c,1-c*c,F(1))]:
        omega=Z((cosine,0,0,sine),q=q)
        audit.check(omega**9==1,'active ninth root omega_'+str(k))
        z,radius=root.residual_root(direct,omega,5,audit=audit)
        audit.check(all(x==0 for x in radius),'independently saturated actual root radial through eta5 k'+str(k))
        real=[]
        for item in z.a:
            value=(item+item.conj())/2
            audit.check(value.a[1]==value.a[2]==value.a[3]==0,
                'active actual root real part descends k'+str(k)+' coefficient'+str(len(real)))
            real.append(value.a[0])
        audit.check(tuple(real)==params['t'+str(k)].a,
            'direct actual-root abscissa equals independent Chebyshev phase k'+str(k))
        root_records.append({'index':k,'root':z.record(),'half_radial':[x.record() for x in radius]})
    slopes=[]
    for k,cosine in [(1,d),(2,2*d*d-1)]:
        q=1-cosine*cosine
        omega=Z((cosine,0,0,1),q=q)
        audit.check(omega**9==1,'inactive ninth root omega_'+str(k))
        _,radius=root.residual_root(direct,omega,1)
        audit.check(radius[1].interval(lo,hi)[1]<0,'strict inactive original-root radial slope k'+str(k))
        slopes.append({'index':k,'half_radial_slope':radius[1].record()})
    audit.check(C['H'].interval(lo,hi)[0]>0,'positive pair opening at the reference point')

    # Damages change mathematics, not only labels or hashes.
    audit.reject(lambda:require(C5+1==obj.a[5],'changed fifth coefficient'),
        'unit change in fifth coefficient')
    broken=list(direct);broken[8]=broken[8]+eta
    audit.reject(lambda:require(broken==sparse,'changed primitive coefficient'),
        'changed sparse primitive coefficient')
    audit.reject(lambda:require(evaluate(direct,1-2*eta)==0,'wrong marked anchor'),
        'wrong marked-root anchor')
    audit.reject(lambda:require(-det==3*(c+d)/56,'reversed normal Jacobian'),
        'reversed scaled-normal determinant')
    audit.reject(lambda:require(l1==-24*(C['alpha']+1),'changed minimizing first jet'),
        'unit change in first minimizing jet')
    audit.reject(lambda:require(nonoptimal.a[4]==known[4],'nonoptimal fourth value'),
        'off-stationary first-jet value labeled minimal')
    badphase=params['t4'].with_coefficient(0,c)
    _,badreal=red.circle(sparse,badphase)
    audit.reject(lambda:require(badreal.a[0]==0,'wrong fourth unit-root branch'),
        'wrong fourth unit-root branch')
    badu1=params['u1'].with_coefficient(4,params['u1'].a[4]+1)
    badpoly=root.factor_integrate(eta,params['u0'],badu1,params['T'])
    omega=Z((-c,0,0,1),q=1-c*c)
    _,badradius=root.residual_root(badpoly,omega,5)
    audit.reject(lambda:require(badradius[5]==0,'missing fifth normal correction'),
        'unit change in fifth original-root normal correction')

    return {'agent':'six-sendov-3','role':'researcher','exact_checks':audit.checks,
        'rejected_mathematical_damages':audit.damages,'objective':obj.record(),
        'parameters':{key:value.record() for key,value in params.items()},'normal_trace':trace,
        'scaled_normal_determinant':det.record(),'embedding_interval':[str(lo),str(hi)],
        'C5_interval':[str(bound[0]),str(bound[1])],
        'leading_reduced_cost':g0.a[2].record(),'reduced_cubic_derivative':l1.record(),
        'active_direct_root_records':root_records,'inactive_slopes':slopes}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--fixture',type=Path,default=BASE/'expected.json')
    parser.add_argument('--emit-fixture',type=Path)
    args=parser.parse_args()
    actual=run()
    if args.emit_fixture is not None:
        args.emit_fixture.write_text(json.dumps(actual,indent=2)+'\n')
    else:
        expected=json.loads(args.fixture.read_text())
        require(canonical(expected)==canonical(actual),'complete expected fixture including JSON types')
    print('PASS',len(actual['exact_checks']),'exact checks;',len(actual['rejected_mathematical_damages']),
        'mathematical damages rejected; full-record SHA256',sha256(canonical(actual)).hexdigest())


if __name__=='__main__':
    main()
