#!/usr/bin/env python3
"""Whole exact joint-cubic maps and budgets; ordinary bridges in PROOF.md.

Actual six-sendov-3 / researcher. Credited same-author arithmetic reuse;
this is proof corroboration, not independent review or a formal kernel.
"""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from arithmetic import (F,CertificateError,need,canonical,sha256,
  constant,variable,add,scale,multiply,power,identity,
  gp,gadd,gscale,gmul,norm,gid,
  N0,N1,NW,na,ns,nm,np,ni,nc,za,zs,zm,zv,zf,zid)
from budgets import budgets,ETA_MAX,A_MIN,V_MAX,BETA_CAP,PHYSICAL_ERROR


def variance_maps():
    rows=[]
    # Seven FREE real coordinates and all eight FREE f-values. This full
    # Lagrange map is universal; f's are substituted only in later maps.
    xs=[variable(j) for j in range(7)]
    xs.append(scale(add(*xs),-1))
    fs=[variable(j+7) for j in range(8)]
    bar=scale(add(*fs),F(1,8))
    centered=[add(f,scale(bar,-1)) for f in fs]
    energy=add(*(power(x,2) for x in xs))
    variance=add(*(power(f,2) for f in centered))
    R=add(*(multiply(x,f) for x,f in zip(xs,fs)))
    identity(rows,'entire zero-sum8 real coordinates',add(*xs),{})
    identity(rows,'entire centered8 f values',add(*centered),{})
    identity(rows,'entire centered Cauchy numerator',R,
             add(*(multiply(x,f) for x,f in zip(xs,centered))))
    identity(rows,'whole8 centered Lagrange nonnegative square sum',
      add(multiply(energy,variance),scale(power(R,2),-1)),
      add(*(power(add(multiply(xs[j],centered[k]),
                     scale(multiply(xs[k],centered[j]),-1)),2)
            for j in range(8) for k in range(j+1,8))))
    identity(rows,'whole8 centered scalar variance',variance,
      add(add(*(power(f,2) for f in fs)),scale(power(add(*fs),2),F(-1,8))))
    # FREE eight complex coordinates, A,beta: full substitution and all
    # quartic remainder terms. No centering assumption is used for these.
    xx=[variable(j) for j in range(8)]
    yy=[variable(j+8) for j in range(8)]
    A=variable(16);B=variable(17)
    ff=[add(multiply(A,power(x,2)),scale(multiply(B,power(y,2)),-1))
        for x,y in zip(xx,yy)]
    E=add(*(power(x,2) for x in xx)); V=add(E,add(*(power(y,2) for y in yy)))
    S4=add(*(power(add(power(x,2),power(y,2)),2) for x,y in zip(xx,yy)))
    X4=add(*(power(x,4) for x in xx))
    XY=add(*(multiply(power(x,2),power(y,2)) for x,y in zip(xx,yy)))
    sumf=add(*ff); sumf2=add(*(power(f,2) for f in ff))
    identity(rows,'whole joint cubic polynomial substitution',
      add(*(multiply(x,f) for x,f in zip(xx,ff))),
      add(multiply(A,add(*(power(x,3) for x in xx))),
          scale(multiply(B,add(*(multiply(x,power(y,2)) for x,y in zip(xx,yy)))),-1)))
    identity(rows,'whole centered quadratic feedback mean',sumf,
      add(multiply(add(A,B),E),scale(multiply(B,V),-1)))
    identity(rows,'whole retained quartic feedback expansion',sumf2,
      add(multiply(power(B,2),S4),
          scale(multiply(add(power(B,2),scale(power(A,2),-1)),X4),-1),
          scale(multiply(multiply(B,add(A,B)),XY),-2)))
    identity(rows,'whole8 squared-coordinate variance identity',
      add(scale(X4,8),scale(power(E,2),-1)),
      add(*(power(add(power(xx[j],2),scale(power(xx[k],2),-1)),2)
            for j in range(8) for k in range(j+1,8))))
    actual_var=add(sumf2,scale(power(sumf,2),F(-1,8)))
    kernel=add(scale(multiply(power(B,2),power(V,2)),F(3,4)),
      scale(multiply(multiply(B,add(A,B)),multiply(E,add(V,scale(E,-1)))),F(1,4)))
    slack=add(multiply(power(B,2),add(scale(power(V,2),F(7,8)),scale(S4,-1))),
      multiply(add(power(B,2),scale(power(A,2),-1)),add(X4,scale(power(E,2),F(-1,8)))),
      scale(multiply(multiply(B,add(A,B)),XY),2))
    identity(rows,'whole retained variance kernel and three nonnegative remainders',
             add(kernel,scale(actual_var,-1)),slack)
    # CREDIT9845 universal zero-sum complex quartic; all seven independent
    # complex coordinates and the dependent eighth are expanded WHOLE.
    zz=[gp(variable(j),variable(j+7)) for j in range(7)]
    zz.append(gscale(gadd(*zz),-1))
    gid(rows,'whole8 centered complex multiplicity sum',gadd(*zz),gp({},{}))
    norms=[norm(z) for z in zz]; ZV=add(*norms)
    total={}
    for j in range(8):
        others=[k for k in range(8) if k!=j]
        pairs=add(*(norm(gadd(zz[k],gscale(zz[l],-1)))
                     for pos,k in enumerate(others) for l in others[pos+1:]))
        identity(rows,'whole other-seven norm identity '+str(j),
          add(scale(ZV,7),scale(norms[j],-8)),pairs)
        total=add(total,multiply(norms[j],pairs))
    identity(rows,'whole complex zero-sum quartic SOS credited9845',
      add(scale(power(ZV,2),7),scale(add(*(power(n,2) for n in norms)),-8)),total)
    # Both genuinely different absorption routes keep all polynomial terms.
    E,V=variable(0),variable(1); b=budgets()
    k=F(b['k']); q=F(b['q']); vmax=F(b['V_endpoint'])
    for route in b['routes']:
        d=F(route['delta']); lam=F(route['lambda'])
        a0=F(route['a0']); b0=F(route['b0'])
        left=add(power(add(scale(E,d),scale(power(V,2),lam)),2),
          scale(multiply(E,add(scale(power(V,2),k),scale(multiply(E,V),q))),-1))
        right=add(scale(power(add(E,scale(power(V,2),b0/a0)),2),a0),
          scale(power(V,4),lam*lam-b0*b0/a0),
          scale(multiply(add(constant(vmax),scale(V,-1)),power(E,2)),q))
        identity(rows,'whole '+route['name']+' positive determinant completion',left,right)
        # The optional negative qE^3 was discarded, not silently reversed.
        retained=add(scale(power(V,2),k),scale(multiply(E,add(V,scale(E,-1))),q))
        relaxed=add(scale(power(V,2),k),scale(multiply(E,V),q))
        identity(rows,'whole '+route['name']+' nonnegative qE3 relaxation',
          multiply(E,add(relaxed,scale(retained,-1))),scale(power(E,3),q))
    return rows


def signed_maps():
    rows=[]
    x,y,g,h,w=[variable(j) for j in range(5)]
    p=add(power(x,3),scale(multiply(x,power(y,2)),F(-3,2)))
    u3=add(power(x,3),scale(multiply(x,power(y,2)),-3))
    A=add(g,scale(multiply(w,h),F(-1,12)))
    B=add(scale(g,F(3,2)),scale(multiply(w,h),F(-1,4)))
    identity(rows,'whole paired signed cubic combined BEFORE absolute values',
      add(multiply(g,p),scale(multiply(multiply(w,h),u3),F(-1,12))),
      multiply(x,add(multiply(A,power(x,2)),scale(multiply(B,power(y,2)),-1))))
    phase=[]
    for k in range(1,5):
        root=np(NW,k);bar=nc(root)
        coeff=ns(na(np(root,6),np(bar,6),ns(N1,-2)),F(1,36))
        if k==3:need(coeff==N0,'third-phase whole cubic cancels')
        if k==4:need(coeff==ns(N1,F(-1,12)),'fourth-phase whole cubic NEGATIVE1/12')
        phase.append({'phase':k,'all6_field_coefficients':[str(q) for q in coeff]})
    rows.append({'name':'whole paired cubic ninth-root phase coefficients','rows':phase})
    c=ns(na(np(NW,4),np(NW,5)),F(-1,2));d=na(ns(np(c,2),2),ns(N1,-1))
    w4=ni(na(c,d));w3=ns(na(ns(N1,7),ns(nm(na(N1,ns(d,-1)),w4),-1)),F(2,3))
    yy=ns(ni(na(N1,c)),F(1,3));xx=na(ns(N1,F(2,3)),ns(yy,-1));C=na(ns(N1,F(8,3)),yy)
    for name,lhs,rhs in (
      ('credited exact mean dual',na(ns(w3,F(3,2)),nm(w4,na(N1,c))),ns(N1,8)),
      ('credited exact trace dual',na(ns(w3,F(3,2)),nm(w4,na(N1,ns(d,-1)))),ns(N1,7)),
      ('credited exact sharp slope',na(ns(N1,8),ns(w3,-1),ns(w4,-1)),C),
      ('credited exact optimal third normal',ns(na(xx,yy),F(3,2)),N1),
      ('credited exact optimal fourth normal',na(nm(na(N1,c),xx),nm(na(N1,ns(d,-1)),yy)),N1)):
        need(lhs==rhs,name);rows.append({'name':name,'all6_field_coefficients':[str(q) for q in lhs]})
    eta,M,Q,V,realU,P,R3,R4,h,g=[variable(j) for j in range(10)]
    L3=za(zm(zf(ns(N1,F(-3,2))),zv(M)),zm(zf(ns(N1,F(-3,28))),zv(Q)))
    L4=za(zm(zf(ns(na(N1,c),-1)),zv(M)),
           zm(zf(ns(na(N1,ns(d,-1)),F(-1,14))),zv(Q)))
    s3=za(zv(eta),zs(L3,-1),zs(zv(R3),-1))
    s4=za(zv(eta),zs(L4,-1),zv(scale(multiply(h,realU),F(1,12))),zs(zv(R4),-1))
    rhs=za(zm(zf(C),zv(eta)),zm(zf(w3),s3),zm(zf(w4),s4),
      zv(scale(add(V,Q),F(1,4))),
      zs(zm(zf(w4),zv(multiply(h,realU))),F(-1,12)),zv(multiply(g,P)),
      zm(zf(w3),zv(R3)),zm(zf(w4),zv(R4)))
    lhs=zv(add(scale(eta,8),scale(M,8),scale(add(V,scale(Q,3)),F(1,4)),multiply(g,P)))
    zid(rows,'whole leading physical substitution WITH signed fourth normal and full residuals',lhs,rhs)
    return rows


def literal_controls():
    controls=[[(F(0),F(0))]*8,
      [(F(0),F(1,100))]*7+[(F(0),F(-7,100))],
      [(F(1,100),F(0))]*7+[(F(-7,100),F(0))],
      [(F(1,120),F(1,90))]*4+[(F(-1,120),F(-1,90))]*4,
      [(F(j-3,130),F((j*j)%7-3,140)) for j in range(7)]]
    controls[-1].append(tuple(-sum(z[j] for z in controls[-1]) for j in range(2)))
    rows=[]
    def powerz(z,n):
        out=(F(1),F(0))
        for _ in range(n):out=(out[0]*z[0]-out[1]*z[1],out[0]*z[1]+out[1]*z[0])
        return out
    for index,zs in enumerate(controls):
        # Gaussian unit phase (3+4i)/5, without sqrt or approximate rotation.
        if index==4:zs=[((3*x-4*y)/5,(4*x+3*y)/5) for x,y in zs]
        need(len(zs)==8 and all(sum(z[j] for z in zs)==0 for j in range(2)),'whole8 zero-sum control')
        E=sum(x*x for x,y in zs); V=sum(x*x+y*y for x,y in zs)
        S4=sum((x*x+y*y)**2 for x,y in zs)
        A=F(19,20); B=F(27,20); fs=[A*x*x-B*y*y for x,y in zs]
        R=sum(x*f for (x,y),f in zip(zs,fs)); fbar=sum(fs)/8
        variance=sum((f-fbar)**2 for f in fs)
        need(R*R<=E*variance,'literal centered Cauchy')
        kernel=F(3,4)*B*B*V*V+B*(A+B)*E*(V-E)/4
        need(variance<=kernel,'literal retained variance kernel')
        need(S4<=F(7,8)*V*V,'literal credited quartic')
        need(sum(powerz(z,3)[0] for z in zs)==sum(x**3-3*x*y*y for x,y in zs),'literal rotated complex cubic')
        rows.append({'index':index,'complete_critical_multiset':[[str(x),str(y)] for x,y in zs],
          'V':str(V),'E':str(E),'A':str(A),'beta':str(B),'R':str(R),
          'centered_f_variance':str(variance),'retained_variance_kernel':str(kernel),
          'S4':str(S4),'original_disk_feasibility_or_objective_cut_asserted':False})
    return rows


def damages():
    rows=[]
    def rejected(name,work):
        try:work()
        except CertificateError as exc:rows.append({'name':name,'reason':str(exc)});return
        raise CertificateError('damaged certificate accepted: '+name)
    x,y,g,h,w=[variable(j) for j in range(5)]
    p=add(power(x,3),scale(multiply(x,power(y,2)),F(-3,2)))
    u=add(power(x,3),scale(multiply(x,power(y,2)),-3))
    right=add(multiply(g,p),scale(multiply(multiply(w,h),u),F(-1,12)))
    rejected('wrong signed fourth-normal feedback',lambda:identity([],'feedback sign',
      add(multiply(g,p),scale(multiply(multiply(w,h),u),F(1,12))),right))
    fs=[variable(j) for j in range(8)];bar=scale(add(*fs),F(1,8))
    truevar=add(*(power(add(f,scale(bar,-1)),2) for f in fs))
    rejected('wrong eight-count centered coefficient1/7',lambda:identity([],'centered variance',truevar,
      add(add(*(power(f,2) for f in fs)),scale(power(add(*fs),2),F(-1,7)))))
    rejected('wrong scalar fourth-variance coefficient7',lambda:identity([],'counted8',
      add(scale(add(*(power(f,4) for f in fs)),7),scale(power(add(*(power(f,2) for f in fs)),2),-1)),
      add(*(power(add(power(fs[j],2),scale(power(fs[k],2),-1)),2) for j in range(8) for k in range(j+1,8)))))
    rejected('erase fourth-phase cubic',lambda:need(ns(N1,F(-1,12))==N0,'nonzero entire phase-four coefficient'))
    rejected('beta cap27/20 fails the full endpoint',lambda:budgets({'beta_cap':F(27,20)}))
    rejected('physical lambda34/25 fails full determinant',lambda:budgets({'physical_lambda':F(34,25)}))
    rejected('objective lambda17/25 fails full determinant',lambda:budgets({'objective_lambda':F(17,25)}))
    rejected('physical error246 misses full cost',lambda:budgets({'physical_error':246}))
    rejected('objective error229 misses full cost',lambda:budgets({'objective_error':229}))
    rejected('objective230 cannot replace physicalDelta247',lambda:budgets({'physical_error':230}))
    rejected('old sqrt272 lower16 fails for247',lambda:budgets({'sqrt_physical_floor':16}))
    rejected('old R3/100 Delta residual is false',lambda:need(F(29)/PHYSICAL_ERROR<F(1,100),'fresh R3 Delta bound required'))
    rejected('old R4/12 Delta residual is false',lambda:need(F(33)/PHYSICAL_ERROR<F(1,12),'fresh R4 Delta bound required'))
    return rows


def build_record():
    return {'schema':'sendov-joint-cubic-coercivity-v1','agent':'six-sendov-3','role':'researcher',
      'scope':'ALL9 actual originals CLOSED unit disk,complex monic degree9,marked a=1-eta,ALL8 critical multiplicities,EVERY0<eta<=1/16000;9857 genuine entry/local full normals adopted',
      'claim':'joint signed cubic variance kernel; F>8+Ceta-230eta2; lowF<=8+3eta physical247 retains E/4; BOTH cuts,arbitrary epsilon>=0,fresh Delta247 moments/all9 motion',
      'whole_variance_and_absorption_maps':variance_maps(),'whole_signed_and_dual_maps':signed_maps(),
      'budgets':budgets(),'complete_arbitrary_critical_controls':literal_controls(),
      'mathematical_damage_rejections':damages(),
      'ordinary_unformalized_bridges':['9857 actual entry before local bootstrap,all9 counted labels and full nonlinear normals',
        'zero-sum centering,Cauchy,credited9845 quartic SOS and nonnegative discarded terms',
        'full infinite reciprocal expansion with convergence,not finite coefficients alone',
        'positive determinant,legal unsquaring and all zero/high/infinite arms',
        'fresh BOTH-cuts arbitrary epsilon and complete complex/all9 original-root estimates'],
      'independent_review_of_new_leaf':False}


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
      'whole_variance_maps':len(record['whole_variance_and_absorption_maps']),
      'whole_signed_and_dual_maps':len(record['whole_signed_and_dual_maps']),
      'strict_rational_margins':len(record['budgets']['rows']),
      'whole_arbitrary_critical_controls':len(record['complete_arbitrary_critical_controls']),
      'mathematical_damage_rejections':len(record['mathematical_damage_rejections'])},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (CertificateError,ValueError,OSError) as exc:
        print('CHECK FAILED: '+str(exc),file=sys.stderr);sys.exit(1)
