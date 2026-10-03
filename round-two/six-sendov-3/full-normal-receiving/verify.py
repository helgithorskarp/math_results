#!/usr/bin/env python3
"""Entire polynomial maps, all9 phases and exact local receiving budgets.

Actual six-sendov-3 / researcher; credited same-author arithmetic reuse.
These checks corroborate the ordinary unformalized PROOF.md.
"""
import argparse
from functools import reduce
from itertools import combinations
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from arithmetic import (F,CertificateError,need,canonical,sha256,comb,
 constant,variable,add,scale,multiply,power,derivative,identity,
 gp,gadd,gscale,gmul,norm,gid,
 N0,N1,NW,na,ns,nm,np,ni,nc,pc,pv,
 za,zs,zm,zc,zn,zreal,zf,zv,zid)
from budgets import budgets
from bootstrap import bootstrap_budgets


def gpow(z,n):
    out=gp(constant(1),{})
    for _ in range(n):out=gmul(out,z)
    return out


def complete_polynomial_maps():
    rows=[]
    w=gp(variable(0),variable(1));u=gp(variable(2),variable(3))
    ds={j:gp(variable(2*j+2),variable(2*j+3)) for j in range(1,8)}
    P=gadd(gpow(w,9),gscale(gpow(u,9),-1),
      *(gmul(ds[j],gadd(gpow(w,j),gscale(gpow(u,j),-1))) for j in ds))
    Pd=gp(derivative(P[0],0),derivative(P[1],0))
    desired=gadd(gscale(gpow(w,8),9),*(gscale(gmul(ds[j],gpow(w,j-1)),j) for j in ds))
    gid(rows,'ENTIRE anchored degree9 derivative',Pd,desired)
    # Eight complex centered points, seven independent complex variables.
    zz=[gp(variable(j),variable(j+7)) for j in range(7)]
    zz.append(gscale(gadd(*zz),-1))
    gid(rows,'whole centered8 sum',gadd(*zz),gp({},{}))
    T=gadd(*(gpow(z,2) for z in zz));U3=gadd(*(gpow(z,3) for z in zz))
    e2=gadd(*(gmul(zz[j],zz[k]) for j,k in combinations(range(8),2)))
    e3=gadd(*(gmul(gmul(zz[j],zz[k]),zz[l]) for j,k,l in combinations(range(8),3)))
    gid(rows,'whole8 Newton integrated d7',gscale(e2,F(9,7)),gscale(T,F(-9,14)))
    gid(rows,'whole8 Newton integrated d6',gscale(e3,F(-3,2)),gscale(U3,F(-1,2)))
    V=add(*(norm(z) for z in zz));sos={}
    for j in range(8):
        others=[k for k in range(8) if k!=j]
        pairs=add(*(norm(gadd(zz[k],gscale(zz[l],-1))) for k,l in combinations(others,2)))
        identity(rows,'whole other-seven centered norm '+str(j),add(scale(V,7),scale(norm(zz[j]),-8)),pairs)
        sos=add(sos,multiply(norm(zz[j]),pairs))
    identity(rows,'credited9845 ENTIRE centered quartic SOS',
      add(scale(power(V,2),7),scale(add(*(power(norm(z),2) for z in zz)),-8)),sos)
    x,d=variable(0),variable(1)
    for n in range(1,10):
        telescoping=multiply(d,add(*(multiply(power(add(x,d),j),power(x,n-1-j)) for j in range(n))))
        identity(rows,'whole monomial displacement '+str(n),add(power(add(x,d),n),scale(power(x,n),-1)),telescoping)
        if n>=2:
            remainder=add(power(add(x,d),n),scale(power(x,n),-1),scale(multiply(power(x,n-1),d),-n))
            integral=add(*(scale(multiply(power(x,n-2-j),power(d,j+2)),F(n*(n-1)*comb(n-2,j),(j+1)*(j+2))) for j in range(n-1)))
            identity(rows,'whole two-integral Taylor remainder '+str(n),remainder,integral)
    return rows


def phase_maps(damage=None):
    rows=[];tables=[]
    u=zv(variable(0),variable(1));ub=zc(u)
    def zp(z,n):
        out=zf(N1)
        for _ in range(n):out=zm(out,z)
        return out
    ds={j:zv(variable(2*j),variable(2*j+1)) for j in range(1,8)}
    u8b=zp(ub,8);u9b=zp(ub,9)
    for k in range(9):
        w=np(NW,k);wb=nc(w)
        full=za(*(zm(zm(ds[j],zp(u,j)),zf(na(np(w,j),ns(N1,-1)))) for j in range(1,8) if not (damage=='forget_d3' and j==3)))
        delta=zs(zm(zm(full,u8b),zf(np(w,(-8)%9))),F(-1,9))
        principal=zreal(zm(zm(ub,zf(wb)),delta))
        direct=zs(zreal(za(*(zm(zm(zm(ds[j],zp(u,j)),u9b),zf(na(np(w,j),ns(N1,-1)))) for j in range(1,8)))),F(-1,9))
        zid(rows,'ENTIRE all7 coefficient normal phase '+str(k),principal,direct)
        opposite_full=za(*(zm(zm(ds[j],zp(u,j)),zf(na(np(wb,j),ns(N1,-1)))) for j in range(1,8)))
        opposite_delta=zs(zm(zm(opposite_full,u8b),zf(np(wb,(-8)%9))),F(-1,9))
        opposite_normal=zreal(zm(zm(ub,zf(w)),opposite_delta))
        pair=zs(za(principal,opposite_normal),F(1,2))
        pair_direct=za(*(zm(zreal(zm(zm(ds[j],zp(u,j)),u9b)),
          zf(ns(na(np(w,j),np(wb,j),ns(N1,-2)),F(-1,18)))) for j in range(1,8)))
        zid(rows,'ENTIRE all7 paired coefficient normal phase '+str(k),pair,pair_direct)
        field_rows=[]
        for j in range(1,8):
            displacement=ns(na(np(w,(j-8)%9),ns(w,-1)),F(-1,9))
            paired=ns(na(np(w,j),np(wb,j),ns(N1,-2)),F(-1,18))
            if k==3 and j in (3,6):need(displacement==N0 and paired==N0,'cube whole d3/d6 cancellation')
            if k==3 and j in (1,2,4,5,7):need(paired==ns(N1,F(1,6)),'complete paired cube coefficient1/6')
            if k==4 and j==3:need(paired==ns(N1,F(1,6)),'phase-four d3 MUST be retained')
            field_rows.append({'degree':j,'complete_displacement_field':[str(q) for q in displacement],'complete_pair_normal_field':[str(q) for q in paired]})
        tables.append({'phase':k,'all_seven_lower_degrees':field_rows})
    eta,M,D=variable(0),variable(1),variable(2)
    a=add(constant(1),scale(eta,-1)); m=zv(M,D); ua=zv(add(a,scale(M,-1)),scale(D,-1))
    for k in range(9):
        w=np(NW,k);wb=nc(w);Z=za(m,zm(ua,zf(w)))
        Zopp=za(m,zm(ua,zf(wb)))
        lhs=zs(za(zn(Z),zn(Zopp),zs(zf(N1),-2)),F(1,4))
        Ak=na(N1,ns(na(w,wb),F(-1,2)))
        rhs=za(zv(add(scale(eta,-1),scale(power(eta,2),F(1,2)))),
          zm(zf(Ak),zv(add(scale(multiply(a,M),-1),power(M,2),power(D,2)))))
        zid(rows,'ENTIRE paired actual base normal phase '+str(k),lhs,rhs)
        sine=zm(zf(na(w,ns(wb,-1))),zv({},constant(F(-1,2))))
        individual=zs(za(zn(Z),zs(zf(N1),-1)),F(1,2))
        zid(rows,'ENTIRE individual actual base normal phase '+str(k),individual,
          za(rhs,zm(sine,zv(multiply(a,D)))))
    # Principal T and U3 signed normals as WHOLE maps, cleared only by r2/r4.
    u=zv(variable(0),variable(1));ub=zc(u);T=zv(variable(2),variable(3));U3=zv(variable(4),variable(5))
    Trot=zm(T,zm(ub,ub)); Q=zs(za(Trot,zc(Trot)),F(1,2))
    J=zs(zm(za(Trot,zs(zc(Trot),-1)),zv({},constant(-1))),F(1,2))
    for k in range(9):
        w=np(NW,k);wb=nc(w)
        DT=zs(zm(zm(T,ub),zf(na(np(w,(-1)%9),ns(w,-1)))),F(1,14))
        NT=zreal(zm(zm(ub,zf(wb)),DT))
        Bk=na(N1,ns(na(np(w,2),np(wb,2)),F(-1,2)))
        sin2=zm(zf(na(np(w,2),ns(np(wb,2),-1))),zv({},constant(F(-1,2))))
        target=zs(za(zm(zf(Bk),zs(Q,-1)),zm(sin2,J)),F(1,14))
        zid(rows,'ENTIRE signed principal T normal phase '+str(k),NT,target)
    for k in (3,4):
        w=np(NW,k);wb=nc(w)
        coeff=ns(na(np(w,(-3)%9),np(wb,(-3)%9),ns(N1,-2)),F(1,36))
        want=N0 if k==3 else ns(N1,F(1,12) if damage=='wrong_cubic_sign' else F(-1,12))
        need(coeff==want,'ENTIRE signed paired U3 coefficient')
        rows.append({'name':'paired U3 SIGN phase '+str(k),'all6_field_coefficients':[str(q) for q in coeff]})
    return {'whole_maps':rows,'whole_nine_phase_tables':tables}


def dual_and_absorption_maps():
    rows=[];b=budgets()
    c=ns(na(np(NW,4),np(NW,5)),F(-1,2)); d=na(ns(np(c,2),2),ns(N1,-1))
    w4=ni(na(c,d));w3=ns(na(ns(N1,7),ns(nm(na(N1,ns(d,-1)),w4),-1)),F(2,3))
    y=ns(ni(na(N1,c)),F(1,3));x=na(ns(N1,F(2,3)),ns(y,-1));C=na(ns(N1,F(8,3)),y)
    for name,lhs,rhs in (
      ('credited dual mean',na(ns(w3,F(3,2)),nm(w4,na(N1,c))),ns(N1,8)),
      ('credited dual trace',na(ns(w3,F(3,2)),nm(w4,na(N1,ns(d,-1)))),ns(N1,7)),
      ('credited sharp C',na(ns(N1,8),ns(w3,-1),ns(w4,-1)),C),
      ('credited cube profile',ns(na(x,y),F(3,2)),N1),
      ('credited fourth profile',na(nm(na(N1,c),x),nm(na(N1,ns(d,-1)),y)),N1)):
        need(lhs==rhs,name);rows.append({'name':name,'all6_field_coefficients':[str(q) for q in lhs]})
    eta,M,Q,V,P,U,r4inv,rinv=[variable(j) for j in range(8)]
    A3=ns(N1,F(3,2));B3=A3;A4=na(N1,c);B4=na(N1,ns(d,-1))
    L3=za(zm(zf(ns(A3,-1)),zv(M)),zm(zf(ns(B3,F(-1,14))),zv(Q)))
    L4=za(zm(zf(ns(A4,-1)),zv(M)),zm(zf(ns(B4,F(-1,14))),zv(Q)))
    lhs=zv(add(scale(eta,8),scale(M,8),scale(add(V,scale(Q,3)),F(1,4)),multiply(P,r4inv)))
    rhs=za(zm(zf(C),zv(eta)),zm(zf(w3),za(zv(eta),zs(L3,-1))),
      zm(zf(w4),za(zv(eta),zs(L4,-1),zv(scale(multiply(U,rinv),F(1,12))))),
      zv(scale(add(V,Q),F(1,4))),zv(multiply(P,r4inv)),
      zm(zf(w4),zv(scale(multiply(U,rinv),F(-1,12)))))
    zid(rows,'ENTIRE actual joint dual signed cubic',lhs,rhs)
    E,V=variable(0),variable(1);k=F(b['joint_k']);q=F(b['joint_q']);v=F(b['V_endpoint'])
    for route in b['routes']:
        d=F(route['delta']);lam=F(route['lambda']);a0=F(route['a0']);b0=F(route['b0'])
        left=add(power(add(scale(E,d),scale(power(V,2),lam)),2),scale(multiply(E,add(scale(power(V,2),k),scale(multiply(E,V),q))),-1))
        right=add(scale(power(add(E,scale(power(V,2),b0/a0)),2),a0),scale(power(V,4),lam*lam-b0*b0/a0),scale(multiply(add(constant(v),scale(V,-1)),power(E,2)),q))
        identity(rows,'fresh COMPLETE '+route['name']+' determinant square',left,right)
    return rows


def complete_bootstrap_maps():
    rows=[];b=bootstrap_budgets()
    t,V,z,w=variable(0),variable(1),variable(2),variable(3)
    identity(rows,'ENTIRE retained broad mean square',
      add(scale(power(t,2),4),scale(multiply(t,V),F(-16,15)),scale(power(V,2),F(-64,15))),
      add(scale(power(add(t,scale(V,F(-2,15))),2),4),scale(power(V,2),F(-976,225))))
    for stage in b['two_square_forward_stages']:
        K=F(stage['whole_K'])
        identity(rows,'ENTIRE real-energy square '+stage['prior_V_cap']+'to'+stage['new_V_cap'],
          add(scale(power(z,2),F(5,14)),scale(multiply(w,z),-K)),
          add(scale(power(add(z,scale(w,F(-7,5)*K)),2),F(5,14)),scale(power(w,2),F(-7,10)*K*K)))
    Q,eta=variable(4),variable(5)
    identity(rows,'ENTIRE retained variance plus real energy',
      add(scale(V,F(1,4)),scale(Q,F(3,4)),scale(Q,F(-4,7))),
      add(scale(V,F(1,14)),scale(add(V,Q),F(5,28))))
    identity(rows,'ENTIRE final13eta conic',
      scale(add(power(add(scale(eta,13),scale(Q,-5)),2),scale(power(Q,2),-49)),F(1,49)),
      add(scale(power(eta,2),F(169,24)),scale(power(add(Q,scale(eta,F(65,24))),2),F(-24,49))))
    return rows


def ga(x=0,y=0):return (F(x),F(y))
def aa(*z):return (sum(w[0] for w in z),sum(w[1] for w in z))
def ss(z,q):return (z[0]*q,z[1]*q)
def mm(z,w):return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def pp(z,n):
    w=ga(1)
    for _ in range(n):w=mm(w,z)
    return w
def cc(z):return (z[0],-z[1])
def ii(z):
    n=z[0]*z[0]+z[1]*z[1];need(n>0,'literal Gaussian divisor');return ss(cc(z),1/n)
def enc(z):return [str(q) for q in z]
def zlit(z):return zs(zv(constant(z[0]),constant(z[1])),1)
def field_enc(z):
    zero=(0,)*20
    need(all(all(m==zero for m in p) for side in z for p in side),
      'literal control must have constant ENTIRE field coefficient maps')
    # All twelve coordinates, INCLUDING zeros. Constant maps need no
    # repeated20-zero exponent encoding; no coefficient is dropped.
    return [[str(p.get(zero,F(0))) for p in side] for side in z]


def literal_controls():
    sets=[
      [ga(F(1,10000),F(1,20000))]*8,
      [ga(0,F(j,6000)) for j in (1,-1,2,-2,0,0,0,0)],
      [ga(F(j,12000),F(k,12000)) for j,k in ((1,2),(2,-1),(3,4),(0,0),(-2,1),(1,-3),(-4,2),(2,0))],
      [ga(F(1,9000),F(1,8000))]*7+[ga(F(-7,9000),F(-7,8000))],
      [ga(F(j,16000),F(k,19000)) for j,k in ((2,1),(2,1),(-1,2),(0,-3),(4,0),(-2,-1),(1,4),(-3,-2))]
    ]
    rows=[];a=F(11999,12000)
    for index,z in enumerate(sets):
        need(len(z)==8,'all eight literal multiplicities')
        mean=ss(aa(*z),F(1,8));nu=[aa(w,ss(mean,-1)) for w in z];u=aa(ga(a),ss(mean,-1))
        need(aa(*nu)==ga(),'literal centered sum')
        V=sum(mm(w,cc(w))[0] for w in nu);T=aa(*(pp(w,2) for w in nu));U3=aa(*(pp(w,3) for w in nu))
        es=[ga(1)]+[aa(*(reduce(mm,(nu[j] for j in ids),ga(1))
          for ids in combinations(range(8),q))) for q in range(1,9)]
        folded=[ga(1)]
        for w in nu:
            old=folded;folded=[ga()]*(len(old)+1)
            for j,b in enumerate(old):
                folded[j]=aa(folded[j],mm(b,ss(w,-1)));folded[j+1]=aa(folded[j+1],b)
        from_es=[ss(es[8-j],(-1)**(8-j)) for j in range(9)]
        need(folded==from_es,'ENTIRE subset and fold product')
        ds={j:ss(from_es[j-1],F(9,j)) for j in range(1,8)}
        need(ds[7]==ss(T,F(-9,14)) and ds[6]==ss(U3,F(-1,2)),'literal BOTH integrated Newton coefficients')
        coeff=[ga()]*10;coeff[9]=ga(1)
        for j in ds:coeff[j]=ds[j]
        coeff[0]=ss(aa(*(mm(coeff[j],pp(u,j)) for j in range(1,10))),-1)
        need(aa(*(mm(coeff[j],pp(u,j)) for j in range(10)))==ga(),'literal FULL anchor')
        derivative_coeff=[ss(coeff[j+1],j+1) for j in range(9)]
        need(derivative_coeff==[ss(w,9) for w in folded],'literal FULL derivative product')
        QJ=mm(mm(T,cc(u)),ii(u));E=(V+QJ[0])/2
        need(E>=0 and E<=V,'literal rotated real energy')
        phases=[]
        for k in range(9):
            w=np(NW,k)
            p0=za(*(zm(zlit(mm(ds[j],pp(u,j))),zf(na(np(w,j),ns(N1,-1)))) for j in ds))
            cleared=zs(zm(zm(p0,zlit(pp(cc(u),8))),zf(np(w,(-8)%9))),F(-1,9))
            direct=za(*(zm(zlit(mm(ds[j],mm(pp(u,j),pp(cc(u),8)))),zf(ns(na(np(w,(j-8)%9),ns(w,-1)),F(-1,9)))) for j in ds))
            need(cleared==direct,'literal ENTIRE linear motion all9')
            phases.append({'phase':k,'FULL_clear_r16_displacement':field_enc(cleared)})
        rows.append({'index':index,'complete_critical_multiset':[enc(w) for w in z],'complete_centered_multiset':[enc(w) for w in nu],
          'mean':enc(mean),'u':enc(u),'centered_energy':str(V),'rotated_real_energy':str(E),'rotated_trace':enc(QJ),
          'whole_T':enc(T),'whole_U3':enc(U3),'complete_centered_primitive':[enc(w) for w in coeff],
          'complete_derivative_product':[enc(w) for w in derivative_coeff],'all_nine_linear_motions':phases,
          'actual_original_disk_feasibility_claimed':False,'receiving_hypotheses_or_objective_cuts_claimed':False})
    return rows


def mathematical_damages():
    rejected=[]
    def reject(name,call,reason):
        try:call()
        except CertificateError as e:
            need(reason in str(e),'wrong rejection: '+name);rejected.append({'name':name,'reason':str(e),'without_fixture':True})
        else:raise CertificateError('damage accepted: '+name)
    for name,change,reason in (
      ('old RMS rho1/160',{'rho':F(1,160)},'centered RMS'),
      ('old tail radius1/60',{'tau':F(1,60)},'centered max norm'),
      ('overstrong pair9/17',{'pair_cap':F(9,17)},'paired cube normal'),
      ('overstrong individual3/5',{'individual_cap':F(3,5)},'individual cube normal'),
      ('overstrong all normal5/6',{'all_normal_cap':F(5,6)},'all9 normal'),
      ('overstrong whole motion4/5',{'motion_cap':F(4,5)},'whole motion'),
      ('omit physical cost192',{'physical':175},'physical error'),
      ('overstrong objective174',{'objective':174},'objective error'),
      ('invalid sqrt192 above14',{'sqrt_physical_floor':14},'sqrt192'),
      ('overstrong entire R3 cap17',{'R3':17},'paired R3'),
      ('overstrong entire R4 cap26',{'R4':26},'paired R4')):
        reject(name,lambda change=change:budgets(change),reason)
    reject('drop phase-four d3 from whole polynomial',lambda:phase_maps('forget_d3'),'all7 coefficient normal')
    reject('reverse signed fourth cubic',lambda:phase_maps('wrong_cubic_sign'),'signed paired U3')
    reject('premature final inverse4 in early box',lambda:bootstrap_budgets({'early_inverse_cost':4}),'earlyinverse11')
    reject('overstrong early37to6 contraction',lambda:bootstrap_budgets({'early_target':6}),'TWO squares 37to6')
    reject('transport old joint12eta trace cap',lambda:bootstrap_budgets({'joint_cap':12}),'joint7V+5Q')
    return rejected


def build_record():
    return {'agent':'six-sendov-3','role':'researcher',
      'scope':'unconditional actual CLOSED-disk degree9 eta<=1/12000 via f785 entry and NEW37to7to5 full complex bootstrap; explicit LC receiving theorem',
      'ordinary_proof_unformalized':True,'independent_review':False,
      'all_original_multiplicities':9,'all_critical_multiplicities':8,
      'whole_polynomial_maps':complete_polynomial_maps(),'whole_phase_maps':phase_maps(),
      'whole_dual_and_absorption_maps':dual_and_absorption_maps(),'fresh_complete_budgets':budgets(),
      'complete_actual_entry_to_LC_maps':complete_bootstrap_maps(),'complete_actual_entry_to_LC_budgets':bootstrap_budgets(),
      'complete_arbitrary_critical_controls':literal_controls(),'mathematical_damage_rejections':mathematical_damages()}


def pairs(items):
    d={}
    for k,v in items:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d

def bad_constant(x):raise CertificateError('nonfinite JSON constant')

def check_fixture(record,path):
    wanted=json.loads(path.read_text(),object_pairs_hook=pairs,parse_constant=bad_constant)
    need(canonical(record)==canonical(wanted),'complete typed record mismatch')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--emit',action='store_true');ap.add_argument('--fixture',type=Path);args=ap.parse_args()
    r=build_record();f=args.fixture or Path(__file__).with_name('EXPECTED.json')
    if args.emit:
        need(args.fixture is None,'emit external fixture forbidden');f.write_bytes(canonical(r)+b'\n')
    else:
        check_fixture(r,f)
    print(json.dumps({'status':'PASS','whole_record_sha256':sha256(canonical(r)).hexdigest(),
      'whole_polynomial_maps':len(r['whole_polynomial_maps']),'whole_phase_maps':len(r['whole_phase_maps']['whole_maps']),
      'whole_dual_and_absorption_maps':len(r['whole_dual_and_absorption_maps']),
      'complete_actual_entry_to_LC_maps':len(r['complete_actual_entry_to_LC_maps']),
      'complete_actual_entry_to_LC_margins':len(r['complete_actual_entry_to_LC_budgets']['all_complete_margins']),
      'strict_rational_margins':len(r['fresh_complete_budgets']['rows']),
      'complete_arbitrary_critical_controls':len(r['complete_arbitrary_critical_controls']),
      'mathematical_damage_rejections':len(r['mathematical_damage_rejections'])},sort_keys=True))

if __name__=='__main__':
    try:main()
    except (CertificateError,ValueError,OSError) as e:
        print('CHECK FAILED: '+str(e),file=sys.stderr);sys.exit(1)
