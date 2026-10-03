"""Exact full real moment jets, third cost and repaired all-nine witness.

Finite SAME-AUTHOR corroboration only. Uniform analytic concentration,
normalization, pair averaging and actual root containment are unformalized.
"""
from pathlib import Path
from math import comb
import json
from arithmetic import (F,N0,N1,NW,na,ns,nm,np,ni,nc,need,canonical,sha256,
    constant,variable,add,scale,multiply,power,encoded,identity)

def ef(a):return [str(t) for t in a]
def cf(c,a,b=0,d=0):return na(ns(N1,F(a)),ns(c,F(b)),ns(np(c,2),F(d)))
def rf(c,a):
    d=4*a[1];b=-2*a[4];aa=a[0]-d/2
    need(a==cf(c,aa,b,d),'whole real cubic normal form')
    return [str(aa),str(b),str(d)]
def real(a):return ns(na(a,nc(a)),F(1,2))
def feq(rows,name,a,b):
    need(a==b,'whole field identity '+name)
    rows.append({'name':name,'all_coefficients':[ef(t) for t in a],'nonzero_residual_coefficients':0})
def qa(*ps):
    out={}
    for p in ps:
        for key,a in p.items():out[key]=na(out.get(key,N0),a)
    return {key:a for key,a in out.items() if a!=N0}
def qs(p,q):return {key:ns(a,q) for key,a in p.items() if ns(a,q)!=N0}
def qm(p,q,order):
    out={}
    for (r,j),a in p.items():
        for (s,k),b in q.items():
            if r+s<=order:out[r+s,j+k]=na(out.get((r+s,j+k),N0),nm(a,b))
    return {key:a for key,a in out.items() if a!=N0}
def qp(p,n,order):
    out={(0,0):N1}
    for _ in range(n):out=qm(out,p,order)
    return out
def primitive(derivative,order):
    p={(r,j+1):ns(a,F(1,j+1)) for (r,j),a in derivative.items()}
    out=dict(p)
    for (r,j),a in p.items():
        for s in range(min(order-r,j)+1):out=qa(out,{(r+s,0):ns(a,-comb(j,s)*(-1)**s)})
    return out
def blocks(p,order):return [[p.get((r,j),N0) for j in range(10)] for r in range(order+1)]
def serial_jet(p,c):return [[list(key),rf(c,a)] for key,a in sorted(p.items())]
def rja(*ps):
    out={}
    for p in ps:
        for key,a in p.items():out[key]=add(out.get(key,{}),a)
    return {key:a for key,a in out.items() if a}
def rjs(p,q):return {key:scale(a,q) for key,a in p.items() if scale(a,q)}
def rjm(p,q):
    out={}
    for (r,j),a in p.items():
        for (s,k),b in q.items():
            if r+s<=3:out[r+s,j+k]=add(out.get((r+s,j+k),{}),multiply(a,b))
    return {key:a for key,a in out.items() if a}
def eval_rational(p,values):
    out=N0
    for monomial,a in p.items():
        val=ns(N1,a)
        for j,n in enumerate(monomial):
            if n:val=nm(val,np(values[j],n))
        out=na(out,val)
    return out
def generic_real_jet(damage=None):
    # Ten formal real moments: U0,H,W,D,J21,J4,U3,J22,J41,J6.
    U,H,W,D,J21,J4,U3,J22,J41,J6=[variable(j) for j in range(10)]
    P=[{}, {(1,0):U,(2,0):W},{(1,0):scale(H,-1),(2,0):D},
       {(2,0):scale(J21,-3),(3,0):U3},{(2,0):J4,(3,0):scale(J22,-6)},
       {(3,0):scale(J41,5)},{(3,0):scale(J6,1 if damage=='wrong_sixth_moment_sign' else -1)},{},{}]
    elementary=[{(0,0):constant(1)}]
    for m in range(1,9):
        elementary.append(rjs(rja(*(rjs(rjm(elementary[m-i],P[i]),(-1)**(i-1)) for i in range(1,m+1))),F(1,m)))
    derivative={}
    for m,e in enumerate(elementary):
        derivative=rja(derivative,{(r,8-m):scale(a,9*(-1)**m) for (r,j),a in e.items()})
    prim={(r,j+1):scale(a,F(1,j+1)) for (r,j),a in derivative.items()};anchored=dict(prim)
    anchor=-2 if damage=='wrong_anchor' else -1
    for (r,j),a in prim.items():
        for s in range(min(3-r,j)+1):anchored=rja(anchored,{(r+s,0):scale(a,-comb(j,s)*anchor**s)})
    return anchored
def family(c,H,uz,up,w2,gamma,m,G2,M4,order):
    def linear(u):return {(0,1):N1,(1,0):ns(u,-1),(2,0):ns(w2,-1),(3,0):ns(m,-1),(4,0):ns(N1,-M4)}
    realfactor={key:a for key,a in linear(uz).items() if key[0]<=order}
    pair=qa(qp({key:a for key,a in linear(up).items() if key[0]<=order},2,order),
       {(1,0):ns(H,F(1,2)),(2,0):nm(H,gamma),
        (3,0):ns(nm(H,na(np(gamma,2),ns(G2,2))),F(1,2))},
       {(4,0):nm(nm(H,gamma),G2)} if order==4 else {})
    derivative=qs(qm(qp(realfactor,6,order),pair,order),9)
    p=primitive(derivative,order)
    return derivative,p,blocks(p,order)
def series_times(a,b,n):
    out=[N0]*(n+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if i+j<=n:out[i+j]=na(out[i+j],nm(x,y))
    return out
def root_equation(p,root,n):
    out=[N0]*(n+1);powers=[[N1]+[N0]*n]
    for j in range(1,10):powers.append(series_times(powers[-1],root,n))
    for r,poly in enumerate(p):
        if r>n:continue
        for j,a in enumerate(poly):
            for l in range(n-r+1):out[r+l]=na(out[r+l],nm(a,powers[j][l]))
    return out
def roots_and_normals(p,order,ids,label_limit=9):
    rows=[]
    for j in range(label_limit):
        omega=np(NW,j);root=[omega]+[N0]*order
        for r in range(1,order+1):
            root[r]=ns(nm(root_equation(p,root,r)[r],omega),F(-1,9))
            feq(ids,'whole original root equation '+str(order)+'/'+str(j)+'/'+str(r),root_equation(p,root,r),[N0]*(r+1))
        normals=series_times(root,[nc(a) for a in root],order);normals[0]=na(normals[0],ns(N1,-1));normals=[ns(a,F(1,2)) for a in normals]
        rows.append({'label':j,'root':root,'normals':normals})
    need(len(rows)==9,'all nine original labels')
    return rows
def objective(c,H,uz,up,w2,gamma,m,G2):
    az=na(N1,uz);ap=na(N1,up)
    q1=na(ns(ap,-2),ns(H,F(1,2)))
    q2=na(np(ap,2),ns(w2,-2),nm(H,gamma))
    q3=na(ns(nm(ap,w2),2),ns(m,-2),ns(nm(H,na(np(gamma,2),ns(G2,2))),F(1,2)))
    direct=[ns(N1,8),na(ns(az,6),ns(q1,-1)),
       na(ns(na(np(az,2),w2),6),ns(q2,-1),ns(np(q1,2),F(3,4))),
       na(ns(m,6),ns(nm(az,w2),12),ns(np(az,3),6),ns(q3,-1),ns(nm(q1,q2),F(3,2)),ns(np(q1,3),F(-5,8)))]
    zdef={(1,0):az,(2,0):w2,(3,0):m};qdef={(1,0):q1,(2,0):q2,(3,0):q3}
    total=qa(qs(qa({(0,0):N1},zdef,qp(zdef,2,3),qp(zdef,3,3)),6),
       {(0,0):ns(N1,2)},qs(qdef,-1),qs(qp(qdef,2,3),F(3,4)),qs(qp(qdef,3,3),F(-5,8)))
    return direct,[total.get((r,0),N0) for r in range(4)]
def interval_poly(p,lo,hi):
    low=high=F(0)
    for a in reversed(p):
        values=(low*lo,low*hi,high*lo,high*hi);low,high=min(values)+a,max(values)+a
    return low,high

def build(damage=None):
    ids=[];rids=[];signs=[]
    c=ns(na(np(NW,4),np(NW,5)),F(-1,2))
    if damage=='wrong_embedding':c=ns(c,-1)
    need(c[4]==F(-1,2) and c[5]==F(-1,2),'physical cosine embedding')
    need(na(ns(np(c,3),8),ns(c,-6),ns(N1,-1))==N0,'cosine cubic')
    y=ns(ni(na(N1,c)),F(1,3));x=na(ns(N1,F(2,3)),ns(y,-1));H=ns(y,14);U0=ns(x,-8);C=na(ns(N1,F(8,3)),y)
    k=ns(na(N1,ns(c,2)),F(-7,18));rho=ns(na(c,ns(N1,-5)),F(1,3))
    uz=ns(na(U0,nm(rho,H)),F(1,8));up=na(uz,ns(nm(rho,H),F(-1,2)))
    W=cf(c,F(2512,27),F(5840,9),F(-21392,27));D=cf(c,F(-4270,27),F(-29492,27),F(4012,3))
    gamma=cf(c,F(13,36),F(1253,72),F(-50,3));w2=ns(W,F(1,8))
    Bstar=cf(c,F(2311,108),F(4934,27),F(-1976,9))
    alpha=cf(c,F(-527,360),F(41,90),F(13,90));tau=ns(np(na(k,rho),2),F(1,2))
    kappa=na(tau,ns(alpha,F(10,27)));sigma=na(alpha,ns(np(rho,2),F(1,2)))
    U2=na(ns(np(uz,2),6),ns(np(up,2),2));U3=na(ns(np(uz,3),6),ns(np(up,3),2))
    J21=nm(H,up);J4=ns(np(H,2),F(1,2));J22=nm(H,np(up,2));J41=nm(J4,up);J6=ns(np(H,3),F(1,4))
    generic=generic_real_jet(damage)
    target_values=[U0,H,W,D,J21,J4,U3,J22,J41,J6]+[N0]*10
    target={key:eval_rational(a,target_values) for key,a in generic.items()};target={key:a for key,a in target.items() if a!=N0}
    target_blocks=blocks(target,3)
    g2=[N0]*10;g2[8]=ns(x,9);g2[7]=ns(y,9);g2[0]=na(ns(N1,9),ns(g2[8],-1),ns(g2[7],-1))
    g4=[N0]*10;g4[8]=ns(W,F(-9,8));g4[7]=ns(na(np(U0,2),ns(D,-1)),F(9,14))
    g4[6]=na(ns(nm(U0,H),F(-3,4)),ns(J21,F(3,2)));g4[5]=na(ns(np(H,2),F(9,40)),ns(J4,F(-9,20)))
    g4[0]=na(ns(N1,-36),ns(U0,-9),ns(H,F(9,2)),*(ns(g4[j],-1) for j in range(1,10)))
    feq(ids,'whole first generic moment coefficient',target_blocks[1],g2)
    feq(ids,'whole second generic moment coefficient',target_blocks[2],g4)
    # Different defining-factor derivation. Its MOVING fourth jet is retained.
    old_deriv,old_primitive,old_blocks=family(c,H,uz,up,w2,gamma,ns(N1,100),N0,0,3)
    D1=na(ns(nm(U0,w2),2),ns(nm(H,np(gamma,2)),-1))
    J21_1=na(nm(H,w2),ns(nm(nm(H,gamma),up),2));J4_1=ns(nm(np(H,2),gamma),2)
    shift=[N0]*10;shift[8]=ns(N1,-900);shift[7]=ns(D1,F(-9,14));shift[6]=ns(J21_1,F(3,2));shift[5]=ns(J4_1,F(-9,20))
    shift[0]=ns(na(*shift[1:]),-1)
    feq(ids,'whole sixth real jet: Newton versus factor and moving fourth-jet subtraction',
        target_blocks[3],[na(old_blocks[3][j],ns(shift[j],-1)) for j in range(10)])
    fixed=roots_and_normals(target_blocks,3,ids)
    old_roots=roots_and_normals(old_blocks,3,ids)
    w4=ni(na(c,na(ns(np(c,2),2),ns(N1,-1))))
    w3=ns(na(ns(N1,7),ns(nm(na(ns(N1,2),ns(np(c,2),-2)),w4),-1)),F(2,3))
    if damage=='wrong_dual_weight':w3=na(w3,ns(N1,F(1,1000)))
    A3=ns(N1,F(3,2));B3=A3;A4=na(N1,c);B4=na(ns(N1,2),ns(np(c,2),-2))
    feq(ids,'first positive dual row',[na(nm(A3,w3),nm(A4,w4))],[ns(N1,8)])
    feq(ids,'second positive dual row',[na(nm(B3,w3),nm(B4,w4))],[ns(N1,7)])
    def f3(u,h2):
        a=na(N1,u)
        return na(np(a,3),ns(nm(np(a,2),h2),-3),ns(nm(a,np(h2,2)),F(15,8)),ns(np(h2,3),F(-5,16)))
    scalar=na(ns(W,2),ns(U2,F(-3,2)),ns(D,F(3,2)),ns(f3(uz,N0),6),ns(f3(up,ns(H,F(1,2))),2))
    normalization=na(nm(uz,W),nm(na(nm(rho,up),nm(sigma,H)),na(U2,ns(D,-1))))
    if damage=='wrong_normalization_offset':normalization=nm(uz,W)
    Tstar=na(scalar,nm(w3,fixed[3]['normals'][3]),nm(w4,fixed[4]['normals'][3]),normalization)
    closedT=cf(c,F(-60800959,17496),F(-307083769,17496),F(10980067,486))
    feq(ids,'whole closed third-order boundary coefficient',[Tstar],[closedT])
    old_obj,old_obj_series=objective(c,H,uz,up,w2,gamma,ns(N1,100),N0)
    feq(ids,'whole prior witness reciprocal jet: direct versus series',old_obj,old_obj_series)
    feq(ids,'old witness cost offset and every active radial payment',[old_obj[3]],
       [na(Tstar,ns(nm(w3,old_roots[3]['normals'][3]),-1),ns(nm(w4,old_roots[4]['normals'][3]),-1))])
    # Explicit simultaneous third-normal repair, followed by a fixed fourth inward step.
    n3=na(old_roots[3]['normals'][3],ns(A3,100));n4=na(old_roots[4]['normals'][3],ns(A4,100))
    matrix=[(ns(A3,-1),ns(nm(B3,H),F(1,7))),(ns(A4,-1),ns(nm(B4,H),F(1,7)))]
    det=na(nm(matrix[0][0],matrix[1][1]),ns(nm(matrix[1][0],matrix[0][1]),-1))
    m=nm(na(ns(nm(n3,matrix[1][1]),-1),nm(n4,matrix[0][1])),ni(det))
    G2=nm(na(ns(nm(matrix[0][0],n4),-1),nm(matrix[1][0],n3)),ni(det))
    feq(ids,'whole common real third repair',[m],[cf(c,F(-17403419,34992),F(-45702565,17496),F(180635,54))])
    feq(ids,'whole imaginary second repair',[G2],[cf(c,F(-1162307,23328),F(-5484833,11664),F(52426519,93312))])
    if damage=='wrong_repair':G2=na(G2,N1)
    deriv,new_primitive,new_blocks=family(c,H,uz,up,w2,gamma,m,G2,100,4)
    actual=roots_and_normals(new_blocks,4,ids,8 if damage=='missing_ninth_root' else 9)
    for j in range(9):
        feq(ids,'known first/quartic root drift retained '+str(j),actual[j]['root'][1:3],old_roots[j]['root'][1:3])
    for j in (3,4,5,6):feq(ids,'all three individual active half-normals vanish '+str(j),actual[j]['normals'][:4],[N0]*4)
    obj,obj_series=objective(c,H,uz,up,w2,gamma,m,G2)
    feq(ids,'whole new attained reciprocal jet',[ns(N1,8),C,Bstar,Tstar],obj)
    feq(ids,'whole new scalar/series reciprocal agreement',obj,obj_series)
    feq(ids,'minimum real-gradient identity',[na(up,ns(nm(rho,H),F(1,2)))],[uz])

    # Complete rational identities for the generic scalar and balanced chart.
    u,h=[variable(j) for j in (0,1)];a=add(constant(1),u)
    q1=add(power(h,2),scale(a,-2));q2=power(a,2)
    from_binomial=add(scale(multiply(q1,q2),F(3,4)),scale(power(q1,3),F(-5,16)))
    explicit=add(power(a,3),scale(multiply(power(a,2),power(h,2)),-3),
       scale(multiply(a,power(h,4)),F(15,8)),scale(power(h,6),F(-4,16) if damage=='wrong_scalar_third' else F(-5,16)))
    identity(rids,'entire third reciprocal-FIRST-power polynomial',from_binomial,explicit)
    ts=[variable(j) for j in range(6)];HH,aa,tt=[variable(j) for j in (6,7,8)]
    rr=scale(add(*ts),F(-1,2));TT=add(*(power(t,2) for t in ts));qSquared=add(scale(HH,F(1,2)),scale(TT,F(-1,2)),scale(power(rr,2),-1))
    J3chart=add(scale(power(rr,3),2),scale(multiply(rr,qSquared),6),*(power(t,3) for t in ts))
    J4chart=add(scale(power(rr,4),2),scale(multiply(power(rr,2),qSquared),12),scale(power(qSquared,2),2),*(power(t,4) for t in ts))
    identity(rids,'whole balanced third moment chart',J3chart,
       add(scale(multiply(HH,rr),3),scale(multiply(rr,TT),-3),scale(power(rr,3),-4),*(power(t,3) for t in ts)))
    identity(rids,'whole balanced fourth moment and remainder',
       add(J4chart,scale(power(HH,2),F(-1,2)),scale(multiply(HH,add(scale(power(rr,2),4),scale(TT,-1))),-1)),
       add(scale(power(TT,2),F(1,2)),scale(multiply(TT,power(rr,2)),-4),scale(power(rr,4),-8),*(power(t,4) for t in ts)))
    KK=add(tt,scale(aa,F(11,27) if damage=='wrong_skew_coefficient' else F(10,27)))
    transverse=add(*(power(add(t,scale(rr,F(1,3))),2) for t in ts))
    identity(rids,'whole tangent cost minus necessary cubic-square payment',
       add(multiply(HH,add(scale(multiply(aa,TT),-1),multiply(add(scale(tt,9),scale(aa,4)),power(rr,2)))),
           scale(multiply(multiply(HH,KK),power(rr,2)),-9)),
       scale(multiply(multiply(aa,HH),transverse),-1))
    lo=F(15,16);hi=F(47,50);f=lambda z:8*z**3-6*z-1
    need(f(lo)<0<f(hi) and 24*lo**2-6>0,'unique physical embedding interval')
    for _ in range(48):
        mid=(lo+hi)/2
        if f(mid)>0:hi=mid
        else:lo=mid
    def positive(name,v):
        p=list(map(F,rf(c,v)));lb,ub=interval_poly(p,lo,hi);need(lb>0,'positive physical sign '+name)
        signs.append({'name':name,'whole_real_polynomial':[str(t) for t in p],'rational_lower':str(lb),'rational_upper':str(ub)})
    for name,v in [('H',H),('minus alpha',ns(alpha,-1)),('kappa',kappa),('dual w3',w3),('dual w4',w4),('repair determinant',det),('Tstar greater than -19',na(Tstar,ns(N1,19))),('Tstar less than -18',na(ns(N1,-18),ns(Tstar,-1)))]:positive(name,v)
    for row in actual:
        j=row['label'];positive('all-nine strict witness inward '+str(j),ns(row['normals'][4 if j in (3,4,5,6) else 1],-1))
    def output_roots(rows):return [{'label':r['label'],'all_root_coefficients':[ef(a) for a in r['root']],
                                  'all_half_normals':[rf(c,a) for a in r['normals']]} for r in rows]
    return {'agent':'six-sendov-3','role':'researcher','schema':1,
      'ordinary_analytic_bridges_unformalized':True,'independent_review':False,
      'constants':{name:ef(a) for name,a in [('c',c),('x',x),('y',y),('H',H),('U0',U0),('C',C),('k',k),('rho',rho),('u_zero',uz),('u_pair',up),('Wstar',W),('Dstar',D),('gamma',gamma),('Bstar',Bstar),('alpha',alpha),('tau',tau),('kappa',kappa),('Tstar',Tstar),('normalization_offset',normalization),('scalar_third_offset',scalar),('m3',m),('Gamma2',G2),('repair_determinant',det)]},
      'generic_real_primitive_through_eta3':[[list(key),encoded(p)] for key,p in sorted(generic.items())],
      'target_real_primitive_all_columns_through_eta3':[[ef(a) for a in p] for p in target_blocks],
      'fixed_all_nine_third_normals':[rf(c,r['normals'][3]) for r in fixed],
      'new_witness_all_primitive_columns_through_eta4':[[ef(a) for a in p] for p in new_blocks],
      'new_witness_objective_through_eta3':[rf(c,a) for a in obj],
      'all_nine_roots':output_roots(actual),'field_polynomial_identities':ids,'rational_polynomial_identities':rids,
      'physical_cosine_interval':[str(lo),str(hi)],'rational_sign_bounds':signs,
      'prior_baseline':{'derivative_terms':len(old_deriv),'primitive_terms':len(old_primitive),
          'whole_primitive_through_eta3':serial_jet(old_primitive,c),
          'objective_through_eta3':[[[j,0],rf(c,a)] for j,a in enumerate(old_obj)],
          'all_nine_roots':output_roots(old_roots)},'new_witness_fourth_inward':100}

def compare_baselines(root,record):
    metadata=json.loads((Path(__file__).parent/'dependencies.json').read_text());reports=[]
    row=next(r for r in metadata['files'] if r['height']==10113 and r['path'].endswith('/EXPECTED.json'))
    raw=(Path(root)/row['path']).read_bytes()
    need(len(raw)==row['bytes'] and sha256(raw).hexdigest()==row['sha256'],'whole pinned10113 baseline')
    old=json.loads(raw);prior=record['prior_baseline']
    for a,b in [('derivative_terms','witness_derivative_terms_through_eta3'),('primitive_terms','witness_primitive_terms_through_eta3'),('whole_primitive_through_eta3','witness_whole_primitive_through_eta3'),('objective_through_eta3','witness_objective_through_eta3')]:
        need(prior[a]==old[b],'whole prior witness baseline '+a)
    for a,b in zip(prior['all_nine_roots'],old['all_nine_roots']):
        need(a['label']==b['label'] and a['all_root_coefficients'][1:]==[b['L'],b['d'],b['witness_third_root']],'all prior root coefficients')
        need(a['all_half_normals'][1:]==b['witness_half_normals'],'all prior half-normal coefficients')
    need(len(prior['all_nine_roots'])==len(old['all_nine_roots'])==9,'all prior labels')
    for name in ('c','x','y','H','U0','C','k','rho','u_zero','u_pair','Wstar','Dstar','gamma','Bstar'):
        need(record['constants'][name]==old['constants'][name],'whole prior physical constant '+name)
    reports.append({'source_commit':row['source_commit'],'path':row['path'],'whole_file_sha256':row['sha256'],
        'comparison':'ENTIRE fixed100 factor primitive/objective through eta3, ALL9 full original jets/half-normals through eta3 and fourteen constants',
        'same_author_not_independent':True,'prior_analytic_theorem_replay':False})
    return reports
