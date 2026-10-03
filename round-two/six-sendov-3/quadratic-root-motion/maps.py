"""Exact all-nine quartic drift and its real one-parameter norm envelope.

Standard-library rational arithmetic in Q[w]/(w^6+w^3+1).  This is
same-author finite corroboration, not a formal proof of the analytic
budget-to-root reduction.  No floating-point value is a proof input.
"""
from pathlib import Path
from math import comb
import json
from arithmetic import F,N0,N1,NW,na,ns,nm,np,ni,nc,need,canonical,sha256

def ef(a): return [str(v) for v in a]
def cf(c,a,b=0,d=0): return na(ns(N1,F(a)),ns(c,F(b)),ns(np(c,2),F(d)))
def rf(c,a):
    d=4*a[1];b=-2*a[4];aa=a[0]-d/2
    need(cf(c,aa,b,d)==a,'whole real cubic normal form')
    return [str(aa),str(b),str(d)]
def ev(p,w):
    out=N0
    for a in reversed(p): out=na(nm(out,w),a)
    return out
def pd(p): return [ns(p[j],j) for j in range(1,len(p))]
def freal(a): return ns(na(a,nc(a)),F(1,2))
def eq(rows,name,a,b):
    need(a==b,'whole field identity '+name)
    rows.append({'name':name,'all_coefficients':[ef(t) for t in a],
                 'nonzero_residual_coefficients':0})
def ja(*ps):
    out={}
    for p in ps:
        for key,a in p.items(): out[key]=na(out.get(key,N0),a)
    return {k:a for k,a in out.items() if a!=N0}
def js(p,q): return {key:ns(a,q) for key,a in p.items() if ns(a,q)!=N0}
def jm(p,q):
    out={}
    for (r,j),a in p.items():
        for (s,k),b in q.items():
            if r+s<=3: out[r+s,j+k]=na(out.get((r+s,j+k),N0),nm(a,b))
    return {key:a for key,a in out.items() if a!=N0}
def jp(p,n):
    out={(0,0):N1}
    for _ in range(n): out=jm(out,p)
    return out
def je(p,c): return [[list(key),rf(c,a)] for key,a in sorted(p.items())]
def interval_poly(p,lo,hi):
    # Outward EXACT rational interval operations, no machine rounding.
    low=high=F(0)
    for a in reversed(p):
        products=(low*lo,low*hi,high*lo,high*hi)
        low,high=min(products)+a,max(products)+a
    return low,high

def build(damage=None):
    ids=[];signs=[]
    c=ns(na(np(NW,4),np(NW,5)),F(-1,2))
    if damage=='wrong_embedding': c=ns(c,-1)
    need(c[4]==F(-1,2) and c[5]==F(-1,2),'physical cosine embedding')
    need(na(ns(np(c,3),8),ns(c,-6),ns(N1,-1))==N0,'cosine cubic')
    y=ns(ni(na(N1,c)),F(1,3));x=na(ns(N1,F(2,3)),ns(y,-1))
    H=ns(y,14);U0=ns(x,-8);C=na(ns(N1,F(8,3)),y)
    k=ns(na(N1,ns(c,2)),F(-7,18));rho=ns(na(c,ns(N1,-5)),F(1,3))
    uz=ns(na(U0,nm(rho,H)),F(1,8));up=na(uz,ns(nm(rho,H),F(-1,2)))
    Wstar=cf(c,F(2512,27),F(5840,9),F(-21392,27))
    Dstar=cf(c,F(-4270,27),F(-29492,27),F(4012,3))
    gamma=cf(c,F(13,36),F(1253,72),F(-50,3))
    Bstar=cf(c,F(2311,108),F(4934,27),F(-1976,9))
    J21=nm(H,up);J4=ns(np(H,2),F(1,2))
    U2=na(ns(np(uz,2),6),ns(np(up,2),2))
    eq(ids,'known mean real minimum',[na(ns(uz,6),ns(up,2))],[U0])
    eq(ids,'known second-moment repair',[gamma],[ns(nm(na(U2,ns(Dstar,-1)),ni(H)),F(1,2))])

    g2=[N0]*10;g2[8]=ns(x,9);g2[7]=ns(y,9)
    g2[0]=na(ns(N1,9),ns(g2[8],-1),ns(g2[7],-1))
    g4=[N0]*10;g4[8]=ns(Wstar,F(-9,8))
    g4[7]=ns(na(np(U0,2),ns(Dstar,-1)),F(9,14))
    g4[6]=na(ns(nm(U0,H),F(-3,4)),ns(J21,F(1) if damage=='wrong_quartic_factor' else F(3,2)))
    g4[5]=na(ns(np(H,2),F(9,40)),ns(J4,F(-9,20)))
    g4[0]=na(ns(N1,-36),ns(U0,-9),ns(H,F(9,2)),*(ns(g4[j],-1) for j in range(1,10)))
    need(g4[5]==N0,'least-profile z5 cancellation')

    # A separate defining-factor derivation, through the THIRD eta order.
    w2=ns(Wstar,F(1,8));M=100
    def linear(u): return {(0,1):N1,(1,0):ns(u,-1),(2,0):ns(w2,-1),(3,0):ns(N1,-M)}
    realfactor=linear(uz);pair=ja(jp(linear(up),2),
        {(1,0):ns(H,F(1,2)),(2,0):nm(H,gamma),(3,0):ns(nm(H,np(gamma,2)),F(1,2))})
    derivative=js(jm(jp(realfactor,6),pair),9)
    primitive={(r,j+1):ns(a,F(1,j+1)) for (r,j),a in derivative.items()}
    anchor=-2 if damage=='wrong_anchor' else -1
    anchored=dict(primitive)
    for (r,j),a in primitive.items():
        for s in range(min(3-r,j)+1):
            anchored=ja(anchored,{(r+s,0):ns(a,-comb(j,s)*anchor**s)})
    blocks=[[anchored.get((r,j),N0) for j in range(10)] for r in range(4)]
    eq(ids,'whole first primitive jet: moments versus factors',g2,blocks[1])
    eq(ids,'whole second primitive jet: moments versus factors',g4,blocks[2])

    # Reciprocal first power, not the quadratic Sendov inequality.
    az=na(N1,uz);ap=na(N1,up)
    q1=na(ns(ap,-2),ns(H,F(1,2)))
    q2=na(np(ap,2),ns(w2,-2),nm(H,gamma))
    q3=na(ns(nm(ap,w2),2),ns(N1,-2*M),ns(nm(H,np(gamma,2)),F(1,2)))
    sq={(0,0):N1,(1,0):q1,(2,0):q2,(3,0):q3}
    minusone=ja(sq,{(0,0):ns(N1,-1)})
    paired=ja({(0,0):ns(N1,2)},js(minusone,-1),js(jp(minusone,2),F(3,4)),js(jp(minusone,3),F(-5,8)))
    zdef={(1,0):az,(2,0):w2,(3,0):ns(N1,M)}
    real=js(ja({(0,0):N1},zdef,jp(zdef,2),jp(zdef,3)),6)
    Fjet=ja(real,paired)
    T100=na(ns(N1,6*M),ns(nm(az,w2),12),ns(np(az,3),6),ns(q3,-1),
        ns(nm(q1,q2),F(3,2)),ns(np(q1,3),F(-4,8) if damage=='wrong_objective_third' else F(-5,8)))
    eq(ids,'whole objective through eta3: scalar versus series',
       [Fjet.get((r,0),N0) for r in range(4)],[ns(N1,8),C,Bstar,T100])

    # Every original label; i is external to the ninth-cyclotomic field.
    # W_j=i*t_j; d_j itself belongs to Q(w).
    Qreal=[N0]*10
    Qreal[8]=Qreal[7]=ns(na(N1,ns(c,2)),F(1,2));Qreal[6]=ns(N1,F(1,2))
    Qreal[0]=ns(na(Qreal[8],Qreal[7],Qreal[6]),-1)
    anti=na(np(NW,4),ns(np(NW,5),-1)) # 2i sin(pi/9)
    rows=[];ds=[];ts=[];Ls=[];active=[]
    for j in range(8 if damage=='missing_original' else 9):
        w=np(NW,j);L=na(ns(w,F(-1,3)),ns(x,-1),ns(nm(y,np(w,8)),-1))
        d=ns(nm(na(ev(g4,w),nm(ev(pd(g2),w),L),
                  ns(nm(np(w,7),np(L,2)),35 if damage=='wrong_root_curvature' else 36)),w),F(-1,9))
        t=ns(na(nm(na(ns(N1,3),ns(c,4)),w),
            ns(nm(na(N1,ns(c,2)),na(N1,np(w,8))),-1),ns(np(w,7),-1)),F(1,18))
        eq(ids,'all-column first root equation '+str(j),[na(nm(ns(np(w,8),9),L),ev(g2,w))],[N0])
        eq(ids,'all-column second root equation '+str(j),
            [na(nm(ns(np(w,8),9),d),ev(g4,w),nm(ev(pd(g2),w),L),ns(nm(np(w,7),np(L,2)),36))],[N0])
        eq(ids,'all-column cubic harmonic '+str(j),[nm(ns(np(w,8),9),t)],[ns(ev(Qreal,w),-1)])
        e=ns(nm(na(ev(blocks[3],w),nm(ev(pd(g4),w),L),nm(ev(pd(g2),w),d),
             ns(nm(ev(pd(pd(g2)),w),np(L,2)),F(1,2)),
             ns(nm(np(w,7),nm(L,d)),72),ns(nm(np(w,6),np(L,3)),84)),w),F(-1,9))
        normal1=freal(nm(L,np(w,8)))
        normal2=na(freal(nm(d,np(w,8))),ns(nm(L,nc(L)),F(1,2)))
        normal3=na(freal(nm(e,np(w,8))),freal(nm(L,nc(d))))
        norm=nm(d,nc(d));tnorm=nm(t,nc(t))
        cross=nm(na(nm(t,nc(d)),ns(nm(d,nc(t)),-1)),ni(anti))
        cross=ns(cross,2 if damage=='wrong_cross_sign' else -2)
        # Reconstruction of i*(t*bar(d)-d*bar(t))=-2 sin(pi/9)*cross/(-2).
        eq(ids,'whole affine norm cross reconstruction '+str(j),
            [ns(nm(cross,anti),F(-1,2))],[na(nm(t,nc(d)),ns(nm(d,nc(t)),-1))])
        row={'label':j,'L':ef(L),'d':ef(d),'W':[ef(N0),ef(t)],
             'd_squared_norm':rf(c,norm),'W_squared_norm':rf(c,tnorm),
             'lambda_cross_over_sine':rf(c,cross),'witness_third_root':ef(e),
             'witness_half_normals':[rf(c,z) for z in (normal1,normal2,normal3)]}
        rows.append(row);ds.append(d);ts.append(t);Ls.append(L)
        if j in (3,4): active.append({'label':j,'half_squared_modulus_eta3':rf(c,normal3)})
    need(len(rows)==9,'all nine original labels')
    eq(ids,'marked root has exact canonical motion',[Ls[0],ds[0],ts[0]],[ns(N1,-1),N0,N0])
    eq(ids,'quartic Vieta trace',[na(*ds)],[ns(Wstar,F(9,8))])
    eq(ids,'skew Vieta trace',[na(*ts)],[ns(k,F(9,7))])
    for j in range(1,5):
        # W_{9-j}=-conj(W_j), since the external i also conjugates.
        eq(ids,'entire reflected original pair '+str(j),[ds[9-j],ts[9-j]],[nc(ds[j]),nc(ts[j])])
    for j in (3,4,5,6):
        need(rows[j]['witness_half_normals'][0]==['0','0','0'],'active first normal zero')
        need(rows[j]['witness_half_normals'][1]==['0','0','0'],'active second normal zero')

    lo=F(15,16);hi=F(47,50);f=lambda t:8*t**3-6*t-1
    need(f(lo)<0<f(hi) and 24*lo**2-6>0,'unique physical cubic bracket')
    for _ in range(48):
        mid=(lo+hi)/2
        if f(mid)>0:hi=mid
        else:lo=mid
    def positive(name,a):
        p=[F(t) for t in rf(c,a)];lb,ub=interval_poly(p,lo,hi)
        need(lb>0,'exact positive sign '+name)
        signs.append({'name':name,'whole_real_polynomial':[str(t) for t in p],
                      'rational_lower':str(lb),'rational_upper':str(ub)})
    target=1 if damage=='wrong_pair_choice' else 2
    norms=[nm(d,nc(d)) for d in ds];wnorms=[nm(t,nc(t)) for t in ts]
    crosses=[cf(c,*(F(t) for t in r['lambda_cross_over_sine'])) for r in rows]
    positive('quartic motion floor',norms[target])
    for j in (1,2,3):positive('negative forward cross '+str(j),ns(crosses[j],-1))
    positive('positive forward cross 4',crosses[4])
    absolute_cross=[N0]+[ns(crosses[j],-1) for j in (1,2,3)]+[crosses[4]]
    for j in (0,1,3,4):
        positive('all-real-lambda constant dominance over '+str(j),na(norms[target],ns(norms[j],-1)))
        positive('all-real-lambda cross dominance over '+str(j),na(absolute_cross[target],ns(absolute_cross[j],-1)))
        positive('all-real-lambda quadratic dominance over '+str(j),na(wnorms[target],ns(wnorms[j],-1)))
    for j in (0,1,2,7,8):positive('witness inactive first inward normal '+str(j),ns(cf(c,*(F(t) for t in rows[j]['witness_half_normals'][0])),-1))
    for j in (3,4,5,6):positive('witness active third inward normal '+str(j),ns(cf(c,*(F(t) for t in rows[j]['witness_half_normals'][2])),-1))
    # Explicit closed coefficient maps, checked against the reconstructed roots.
    aa=cf(c,F(-13638695,972),F(-16011613,243),F(20901119,243))
    beta=cf(c,F(1448,243),F(6982,243),F(-8224,243))
    qq=cf(c,F(4,81),F(25,162),F(10,81))
    eq(ids,'closed entire quadratic-envelope coefficients',[norms[2],absolute_cross[2],wnorms[2]],[aa,beta,qq])
    return {'agent':'six-sendov-3','role':'researcher','schema':1,
       'ordinary_analytic_bridges_unformalized':True,'independent_review':False,
       'constants':{name:ef(a) for name,a in [('c',c),('x',x),('y',y),('H',H),('U0',U0),('C',C),('k',k),('rho',rho),('u_zero',uz),('u_pair',up),('Wstar',Wstar),('Dstar',Dstar),('gamma',gamma),('Bstar',Bstar),('T100',T100)]},
       'g2_all_columns':[ef(a) for a in g2],'g4_all_columns':[ef(a) for a in g4],
       'Q_without_i_all_columns':[ef(a) for a in Qreal],
       'witness_derivative_terms_through_eta3':len(derivative),
       'witness_primitive_terms_through_eta3':len(anchored),
       'witness_whole_primitive_through_eta3':je(anchored,c),
       'witness_objective_through_eta3':je(Fjet,c),'witness_active_third_normals':active,
       'field_polynomial_identities':ids,'all_nine_roots':rows,
       'physical_cosine_interval':[str(lo),str(hi)],'rational_sign_bounds':signs,
       'envelope':{'A':rf(c,aa),'cross_over_sine':rf(c,beta),'q_squared':rf(c,qq),
                   'max_labels_positive_negative_zero':[[7],[2],[2,7]]}}

def compare_baselines(root,record):
    metadata=json.loads((Path(__file__).parent/'dependencies.json').read_text())
    reports=[]
    def load(height):
        row=next(r for r in metadata['files'] if r['height']==height and r['path'].endswith('/EXPECTED.json' if height!=8619 else '/expected.json'))
        raw=(Path(root)/row['path']).read_bytes()
        need(len(raw)==row['bytes'] and sha256(raw).hexdigest()==row['sha256'],'whole pinned baseline '+str(height))
        return row,json.loads(raw)
    row,old=load(8619)
    family=old['explicit_family']
    need(family['M']==100,'prior family inward correction')
    for ours,theirs in [('witness_derivative_terms_through_eta3','derivative_terms_through_eta3'),
                       ('witness_primitive_terms_through_eta3','primitive_terms_through_eta3'),
                       ('witness_whole_primitive_through_eta3','primitive')]:
        need(record[ours]==family[theirs],'whole prior explicit family '+ours)
    need(record['witness_objective_through_eta3']==old['explicit_objective_jet'],'entire prior reciprocal objective jet')
    need([{'half_squared_modulus_eta3':r['half_squared_modulus_eta3']} for r in record['witness_active_third_normals']]==family['active_pairs'],'whole prior active third normals')
    c=tuple(F(t) for t in record['constants']['c'])
    for ours,theirs in [('c','c'),('x','x'),('y','y'),('H','H'),('U0','U0'),('C','C'),('k','L'),('rho','mixed'),('u_zero','u_zero'),('u_pair','u_pair'),('Wstar','W'),('Dstar','D'),('gamma','gamma'),('Bstar','Bstar')]:
        need(rf(c,tuple(F(t) for t in record['constants'][ours]))==old['constants'][theirs],'whole prior physical constant '+ours)
    reports.append({'source_commit':row['source_commit'],'path':row['path'],'whole_file_sha256':row['sha256'],
        'comparison':'ENTIRE prior defining-factor primitive and reciprocal objective through eta3, both active third normals, fourteen physical constants',
        'same_author_not_independent':True,'prior_theorem_replay':False})
    row,old=load(10097)
    for oldr,newr in zip(old['all_nine_harmonics'],record['all_nine_roots']):
        need(oldr['label']==newr['label'] and oldr['W']==newr['W'],'entire prior all-nine cubic harmonic')
        n=nm(tuple(F(t) for t in newr['W'][1]),nc(tuple(F(t) for t in newr['W'][1])))
        need(oldr['squared_norm']==[ef(n),ef(N0)] and oldr['real_cubic_normal_form']==newr['W_squared_norm'],'whole prior harmonic norm')
    need(len(old['all_nine_harmonics'])==len(record['all_nine_roots'])==9,'whole prior harmonic coverage')
    reports.append({'source_commit':row['source_commit'],'path':row['path'],'whole_file_sha256':row['sha256'],
        'comparison':'ALL9 complete prior cubic harmonics and full norms; no prior analytic theorem replay',
        'same_author_not_independent':True,'prior_theorem_replay':False})
    return reports
