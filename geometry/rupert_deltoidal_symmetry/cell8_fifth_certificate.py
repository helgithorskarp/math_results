"""Exact fixed hypotheses for the ENTIRE closed 1/5 Cell8 collar.

Python3.11 stdlib. See cell8_fifth_proof.md for the continuous proof.
No floating predicates, adaptive search, or parent guard changes.
"""
from pathlib import Path
from fractions import Fraction as F
import copy,hashlib,itertools,json,time,resource
if not __debug__:raise RuntimeError('verification requires assertions; do not use python -O')
import cell8_collar_certificate as parent
from source_extrema_certificate import reflection,WALLS,mv
from verify import project
C=parent.C;H=C.H;Q=H.Q5;ZERO=H.ZERO;source=parent.source
ROOT=Path(__file__).parent;R=F(1,8);RECEIVER_D=F(7237,100000)
TRI=[C.N[8],parent.nine.W,parent.TIPS[1]]
GLO=F(311,320);GHI=F(631,640);SOURCE_DEPTH=1
PINS={'cell8_collar_certificate.py':'f508909a0c1872ad95d27b15cf758293e6e0d0c675c3104a9b40b7288e2865f5',
      'expected_cell8_collar.json':'b7c13ff22329748b1cc179fe931e84e6ab790fb12871e94cf86db507c7a8f300'}
def pins():
    out=parent.pins()
    for name,wanted in PINS.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==wanted
    assert parent.R==R and parent.MAX_DEPTH==4 and parent.local.R==F(27,250) and parent.local.MAX_DEPTH==3
    return {**out,**PINS}
def fixture():return json.loads((ROOT/'expected_cell8_fifth.json').read_text())
M=C.M;M2=C.M2;B1=H.vec((1,0,-M[0]));B2=H.vec((0,1,-M[1]))
A=F(10739,100000);T=F(2964457,200000);COS=1-A*A/2
CAP2=M2*((1-COS*COS)/(COS*COS))
ML=C.root_upper(M2)-F(1,10**6);MH=ML+F(1,10**6)
assert Q(ML*ML)<M2<Q(MH*MH) and COS>0
IL,IH=1/MH,1/ML;IM=(IL+IH)/2;IE=(IH-IL)/2

def point(xy):return H.add(M,H.add(H.mul(xy[0],B1),H.mul(xy[1],B2)))
def tangent(xy):return H.add(H.mul(xy[0],B1),H.mul(xy[1],B2))
def linear(v):return (H.dot(v,M),H.dot(v,B1),H.dot(v,B2))
def linvalue(row,xy):return row[0]+row[1]*xy[0]+row[2]*xy[1]
def clip(poly,row):
    """Intersection with a CLOSED affine half-plane, retaining point/edge cases."""
    if not poly:return []
    out=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        fa,fb=linvalue(row,a),linvalue(row,b)
        if fa.sign()>=0:out.append(a)
        if fa.sign()*fb.sign()<0:
            t=fa/(fa-fb)
            out.append(tuple(a[j]+t*(b[j]-a[j]) for j in range(2)))
    clean=[]
    for a in out:
        if not clean or clean[-1]!=a:clean.append(a)
    if len(clean)>1 and clean[0]==clean[-1]:clean.pop()
    assert all(linvalue(row,a).sign()>=0 for a in clean)
    return clean

def first_chamber_polygons():
    g11,g12,g22=H.dot(B1,B1),H.dot(B1,B2),H.dot(B2,B2)
    det=g11*g22-g12*g12;assert det.sign()>0
    bx=C.root_upper(CAP2*g22/det);by=C.root_upper(CAP2*g11/det)
    base=[(Q(-bx),Q(-by)),(Q(bx),Q(-by)),(Q(bx),Q(by)),(Q(-bx),Q(by))]
    cuts=[]
    directions=[(1,0),(0,1),(1,1),(1,-1),(2,1),(2,-1),(1,2),(1,-2)]
    for x,y in directions:
        d=H.add(H.mul(x,B1),H.mul(y,B2));assert H.dot(d,M)==ZERO
        bound=C.root_upper(CAP2*H.dot(d,d))
        for sg in (-1,1):cuts.append((Q(bound),sg*H.dot(d,B1),sg*H.dot(d,B2)))
    for row in cuts:base=clip(base,row)
    assert len(base)>=3
    records=[]
    for row in C.P['cell_certificates']:
        corners=[C.N[j] for j in row['corner_indices']]
        sides=[H.cross(u,corners[(i+1)%len(corners)]) for i,u in enumerate(corners)]
        poly=base[:]
        for e in sides:poly=clip(poly,linear(e))
        av=H.vec(map(C.parse,row['area_vector']));bound=Q(T*MH/COS)
        ar=linear(av);poly=clip(poly,(bound-ar[0],-ar[1],-ar[2]))
        records.append((row['cell'],poly))
    return records,{'coordinate_bounds':[str(bx),str(by)],'linear_chord_cuts':len(cuts),
                    'base_polygon_corners':len(base),'source_area_linear_upper':str(T*MH/COS)}

MIRROR=reflection(WALLS[2]);assert mv(MIRROR,M)==M
LOKL=Q(COS)/M2;HIKL=1/M2;MIDKL=(LOKL+HIKL)/2;EKL=(HIKL-LOKL)/2
LOKQ=Q(COS*COS/(1+COS))/M2;HIKQ=1/(2*M2)
MIDKQ=(LOKQ+HIKQ)/2;EKQ=(HIKQ-LOKQ)/2
RNORM=C.root_upper(CAP2)
assert LOKL.sign()>0 and LOKQ.sign()>0 and EKL.sign()>0 and EKQ.sign()>0

def source_polygons():
    """24 closed necessary polygons covering both actual proper-gauge copies."""
    original,geometry=first_chamber_polygons()
    # Reflect the complete enclosure; no invariance of the chord polygon is assumed.
    polygons=[]
    g11,g12,g22=H.dot(B1,B1),H.dot(B1,B2),H.dot(B2,B2)
    det=g11*g22-g12*g12
    def coordinates(w):
        h1,h2=H.dot(w,B1),H.dot(w,B2)
        return ((g22*h1-g12*h2)/det,(g11*h2-g12*h1)/det)
    for cell,poly in original:
        polygons.append((0,cell,poly))
        reflected=[coordinates(mv(MIRROR,tangent(xy))) for xy in poly]
        assert all(tangent(xy)==mv(MIRROR,tangent(old)) for xy,old in zip(reflected,poly))
        polygons.append((1,cell,reflected))
    return polygons,geometry

def tighten(poly,fold,cell):
    """Two NEW exact necessary area cuts using the current polygon norm bound.

    Every true source remains inside. This is not a guard/depth/resource change.
    """
    av=H.vec(map(C.parse,C.P['cell_certificates'][cell]['area_vector']))
    if fold:av=mv(MIRROR,av)
    ar=linear(av)
    for _ in range(2):
        if not poly:break
        maximum=max(H.dot(tangent(xy),tangent(xy)) for xy in poly)
        norm=C.root_upper(M2+min(maximum,CAP2))
        bound=Q(T*norm)
        poly=clip(poly,(bound-ar[0],-ar[1],-ar[2]))
    return poly

def rank_affine_max(poly,p,v):
    """Exact edge maximum of (MIDKL*M.p+MIDKQ*p.w)*(v.w).

    Along a tangent direction perpendicular to p this function is affine.
    Thus a compact polygon maximum is attained on its boundary, even when
    its maximum is negative. Negative maxima preserve a useful height gain.
    """
    if not poly:return ZERO
    h=H.dot(M,p);w=[tangent(xy) for xy in poly]
    vals=[(MIDKL*h+MIDKQ*H.dot(p,a))*H.dot(v,a) for a in w]
    for a,b in zip(w,w[1:]+w[:1]):
        d=H.sub(b,a);pa=MIDKL*h+MIDKQ*H.dot(p,a);pd=MIDKQ*H.dot(p,d)
        va,vd=H.dot(v,a),H.dot(v,d);aa=pd*vd;bb=pa*vd+pd*va;cc=pa*va
        if aa.sign()<0:
            t=-bb/(2*aa)
            if t.sign()>=0 and (1-t).sign()>=0:vals.append(cc-bb*bb/(4*aa))
    return max(vals)

def parameters(lo,hi,pi,wi,sign,receiver):
    p=C.POINTS[wi][0];probe=C.PROBES[pi];mu=probe['mu'];z=H.cross(M,mu)
    assert H.dot(mu,M)==ZERO and H.dot(z,M)==ZERO
    rawh=H.dot(M,p);h=rawh if rawh.sign()>=0 else -rawh
    pp=C.project(p,M);rp=C.root_upper(H.dot(pp,pp))
    rz=C.root_upper(H.dot(z,z));eta=probe['norm_upper']
    error=EKL*h*(1+hi*hi)*eta*RNORM+EKQ*rp*(1+hi*hi)*eta*CAP2
    error+=(HIKL*h+HIKQ*rp*RNORM)*Q(2*hi*IE*rz*RNORM)
    assert error.sign()>=0
    vectors=[H.sub(H.mul(1-lo*lo,mu),H.mul(2*sign*lo*IM,z)),
             H.sub(H.mul(1-lo*hi,mu),H.mul(sign*(lo+hi)*IM,z)),
             H.sub(H.mul(1-hi*hi,mu),H.mul(2*sign*hi*IM,z))]
    gamma=C.DATA[pi][wi]['d'];tau=C.DATA[pi][wi]['tau'][sign]
    coef=(gamma-probe['H']-receiver[pi],Q(2*tau),-gamma-probe['H']-receiver[pi])
    assert coef[2].sign()<=0
    return p,vectors,error,coef

def witness(poly,lo,hi,pi,wi,sign,cache,receiver):
    key=(lo,hi,pi,wi,sign)
    if key not in cache:cache[key]=parameters(*key,receiver)
    p,vectors,error,coef=cache[key]
    upper=max(rank_affine_max(poly,p,v) for v in vectors)+error
    margins=[coef[0]+coef[1]*x+coef[2]*x*x-upper for x in (lo,hi)]
    return all(x.sign()>0 for x in margins),{
        'probe':pi,'point':wi,'source_loss_numerator_upper':str(upper),
        'strict_endpoint_margins':list(map(str,margins))}

def split(poly):
    xs=[p[0] for p in poly];ys=[p[1] for p in poly]
    axis=0 if max(xs)-min(xs)>=max(ys)-min(ys) else 1
    vals=xs if axis==0 else ys;middle=(min(vals)+max(vals))/2
    if min(vals)==max(vals):return []
    row=(-middle,Q(axis==0),Q(axis==1))
    return [clip(poly,row),clip(poly,tuple(-x for x in row))]

def closed_source_cover(records):
    assert isinstance(records,list) and records
    groups={(f,c):[] for f in (0,1) for c in range(12)}
    for row in records:
        assert isinstance(row,list) and len(row)==5
        fold,cell,path,pi,wi=row
        assert type(fold) is int and fold in (0,1) and type(cell) is int and 0<=cell<12
        assert isinstance(path,str) and len(path)<=SOURCE_DEPTH and set(path)<=set('01')
        assert type(pi) is int and type(wi) is int
        assert (pi==wi==-1) or (0<=pi<16 and 0<=wi<74)
        groups[fold,cell].append(path)
    for paths in groups.values():
        wanted=set(paths);assert paths and len(wanted)==len(paths)
        seen=[]
        def visit(path):
            if path in wanted:seen.append(path);return
            assert len(path)<SOURCE_DEPTH and any(p.startswith(path) for p in wanted)
            for child in '01':visit(path+child)
        visit('');assert set(seen)==wanted and sum((F(1,2)**len(p) for p in paths),F(0))==1

def replay_source(records,receiver):
    closed_source_cover(records);polygons,geometry=source_polygons()
    roots={(fold,cell):tighten(poly,fold,cell) for fold,cell,poly in polygons}
    digest=hashlib.sha256();empty=0;positive=0;negative_gains=0;cache={}
    summaries=[]
    for fold,cell,path,pi,wi in records:
        poly=roots[fold,cell]
        for child in path:
            pieces=split(poly);assert len(pieces)==2
            poly=tighten(pieces[int(child)],fold,cell)
        if pi==-1:
            assert not poly;empty+=1
            record={'fold':fold,'cell':cell,'path':path,'empty':True}
        else:
            assert poly
            okay,data=witness(poly,GLO,GHI,pi,wi,1,cache,receiver);assert okay
            margins=list(map(C.parse,data['strict_endpoint_margins']))
            assert all(x>Q(F(1,100000)) for x in margins)
            positive+=len(margins)
            if C.parse(data['source_loss_numerator_upper']).sign()<0:negative_gains+=1
            record={'fold':fold,'cell':cell,'path':path,'empty':False,
                'polygon_corners':[list(map(str,a)) for a in poly],**data}
        digest.update(json.dumps(record,sort_keys=True,separators=(',',':')).encode())
        summaries.append({k:v for k,v in record.items() if k not in ('polygon_corners','strict_endpoint_margins','source_loss_numerator_upper')})
    return {'source_chamber_copies':2,'closed_fan_cells_per_copy':12,
        'closed_interval':['311/320','631/640'],'sign':1,'geometry':geometry,
        'factor_midpoints':list(map(str,(MIDKL,MIDKQ))),
        'factor_halfwidths':list(map(str,(EKL,EKQ))),
        'minimum_axis_length_enclosure':list(map(str,(ML,MH))),
        'inverse_length_midpoint':str(IM),'inverse_length_error':str(IE),
        'source_tangent_norm_squared_upper':str(CAP2),'tangent_norm_upper':str(RNORM),
        'fixed_source_depth':SOURCE_DEPTH,'closed_leaves':len(records),'empty_leaves':empty,
        'strict_support_leaves':len(records)-empty,'strict_endpoint_margins':positive,
        'every_endpoint_margin_greater_than':'1/100000','uniform_negative_height_gains':negative_gains,
        'entrywise_polygon_and_support_sha256':digest.hexdigest(),'witnesses':summaries}

def closed_roll_cover(rows):
    assert isinstance(rows,list) and rows
    for row in rows:
        assert isinstance(row,list) and len(row)==5
        sign,lo,hi,pi,wi=row
        assert type(sign) is int and sign in (-1,1) and F(1,10)<=F(lo)<F(hi)<=1
        assert type(pi) is int and 0<=pi<16 and type(wi) is int and 0<=wi<74
    for sign in (-1,1):
        intervals=[(F(lo),F(hi)) for s,lo,hi,_,_ in rows if s==sign]
        if sign==1:intervals.append((GLO,GHI))
        intervals.sort();assert intervals and intervals[0][0]==F(1,10) and intervals[-1][1]==1
        assert all(a[1]==b[0] for a,b in zip(intervals,intervals[1:]))

def receiver_bounds():
    envelopes=C.linear_envelopes(TRI)
    norms=[C.root_upper(H.dot(project(v,M),project(v,M))) for v in C.V]
    bounds=[];records=[];count=0
    for pi,p in enumerate(C.PROBES):
        values=[]
        for j,v in enumerate(C.V):
            gamma=H.dot(p['mu'],v);correction=p['norm_upper']*norms[j]-gamma
            assert correction.sign()>=0
            for side,xi in enumerate((envelopes[pi]['lo'],envelopes[pi]['hi'])):
                values.append((-H.dot(M,v)*xi-(p['H']-gamma)+RECEIVER_D**2*correction/4,j,side));count+=1
        bound=max(ZERO,*(z for z,_,_ in values));bounds.append(bound)
        records.append({'probe':pi,'receiver_excess_upper':str(bound),
            'active_vertices_and_sides':[[j,s] for z,j,s in values if z==bound],
            'corner_ratio_lower':str(envelopes[pi]['lo']),'corner_ratio_upper':str(envelopes[pi]['hi'])})
    assert count==1984
    return bounds,records

def phase(rows,bounds):
    closed_roll_cover(rows);norms=[C.root_upper(H.dot(project(p,M),project(p,M))) for p,_ in C.POINTS]
    c=1-A*A/4
    def coefficients(sign,pi,wi):
        p,row=C.PROBES[pi],C.DATA[pi][wi]
        error=p['norm_upper']*row['source_height_upper']*A+A*A*p['norm_upper']*norms[wi]/4+bounds[pi]
        co=(c*row['d']-p['H']-error,Q(2*c*row['tau'][sign]),-c*row['d']-p['H']-error)
        assert co[2].sign()<0;return co
    value=lambda co,x:co[0]+co[1]*x+co[2]*x*x
    gates=[]
    for sign,pi in ((-1,3),(1,4)):
        assert H.dot(M,C.V[45])==ZERO and C.DATA[pi][45]['d']==C.PROBES[pi]['H']
        co=coefficients(sign,pi,45);quad=lambda x:-value(co,x)
        assert quad(0).sign()>0 and quad(F(1,10)).sign()<0
        upper=C.grid_upper(lambda x:quad(x).sign()<0,F(1,10))
        assert quad(upper).sign()<0 and quad(upper-F(1,10**6)).sign()>=0
        gates.append({'sign':sign,'probe':pi,'point':45,'coefficients':list(map(str,co)),
            'small_root_upper':str(upper),'roll_chord_upper':str(2*upper),
            'q_zero':str(quad(0)),'q_b':str(quad(F(1,10))),
            'q_upper':str(quad(upper)),'q_predecessor':str(quad(upper-F(1,10**6)))})
    intervals=[]
    for sign,lo,hi,pi,wi in rows:
        co=coefficients(sign,pi,wi);margins=[value(co,F(x)) for x in (lo,hi)]
        assert all(x.sign()>0 for x in margins)
        intervals.append({'sign':sign,'interval':[lo,hi],'probe':pi,'point':wi,
            'coefficients':list(map(str,co)),'strict_endpoint_margins':list(map(str,margins))})
    roll=max(F(g['roll_chord_upper']) for g in gates)
    product=(1-A*A/4)*(1-RECEIVER_D**2/4)*(1-roll*roll/4);X2=(A+RECEIVER_D)**2+roll*roll
    assert product>F(99,100)**2 and F(99,100)-A*RECEIVER_D/4>0 and X2<=F(1,9)
    beta=next(F(j,1000) for j in range(1001,1020) if F(j,1000)**2*(1-X2/4)>1)
    theta=C.grid_upper(lambda x:Q(x*x)>Q(beta*beta*X2),F(1,3));gate=R*(1-theta*theta/8)-theta/2
    assert gate>0
    return {'near_zero_gates':gates,'standard_closed_roll_intervals':intervals,
        'standard_interval_count':len(rows),'height_aware_interval_count':1,
        'roll_chord_upper':str(roll),'full_spatial_angle_upper':str(theta),
        'composition_squared_upper':str(X2),'angle_derivative_beta':str(beta),
        'quaternion_product_margin':str(product-F(99,100)**2),
        'angle_derivative_margin':str(beta*beta*(1-X2/4)-1),
        'angle_to_cayley_radius1_8_gate':str(gate)}

def identity_audits():
    # Definition-level matrix-vector Rodrigues check in an orthonormal frame.
    # The written algebra, rather than these regressions, proves all real inputs.
    count=0
    def dt(a,b):return sum(x*y for x,y in zip(a,b))
    def sc(a,v):return tuple(a*x for x in v)
    def ad(a,b):return tuple(x+y for x,y in zip(a,b))
    def cr(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
    ez=(F(0),F(0),F(1))
    def rotation(p,axis,c,s):return ad(ad(sc(c,p),sc(1-c,sc(dt(axis,p),axis))),sc(s,cr(axis,p)))
    for ell,e,t,x,height in itertools.product((F(1),F(2)),((F(1),F(0),F(0)),(F(0),F(1),F(0)),(F(3,5),F(4,5),F(0))),
            (F(0),F(1,50),F(-1,50)),(F(-2,3),F(0),F(3,4)),(F(-1),F(0),F(2))):
        c=(1-t*t)/(1+t*t);s=2*t/(1+t*t);axis=cr(ez,e);w=sc(ell*s/c,e)
        p=(F(3,5),F(4,7),height);mu=(F(2,3),F(-1,4),F(0))
        rt=rotation(p,axis,c,-s);rolled=rotation(rt,ez,(1-x*x)/(1+x*x),2*x/(1+x*x))
        h=ell*height;mut=ad(sc(1-x*x,mu),sc(-2*x,cr(ez,mu)))
        expected=dt(mu,p)*(1-x*x)+2*x*dt(mu,cr(ez,p))
        expected-=(c*h/(ell*ell)+c*c*dt(p,w)/(ell*ell*(1+c)))*dt(mut,w)
        assert (1+x*x)*dt(mu,rolled)==expected;count+=1
    bern=0
    for s in (F(0),F(1),F(1,3)):
        x=GLO+(GHI-GLO)*s
        for mu in (C.PROBES[3]['mu'],C.PROBES[4]['mu']):
            z=H.cross(M,mu)
            vectors=[H.sub(H.mul(1-GLO*GLO,mu),H.mul(2*GLO*IM,z)),
                H.sub(H.mul(1-GLO*GHI,mu),H.mul((GLO+GHI)*IM,z)),
                H.sub(H.mul(1-GHI*GHI,mu),H.mul(2*GHI*IM,z))]
            actual=H.sub(H.mul(1-x*x,mu),H.mul(2*x*IM,z))
            reconstructed=H.add(H.add(H.mul((1-s)**2,vectors[0]),H.mul(2*s*(1-s),vectors[1])),H.mul(s*s,vectors[2]))
            assert actual==reconstructed;bern+=3
    square=[H.vec((0,0)),H.vec((1,0)),H.vec((1,1)),H.vec((0,1))]
    line=clip(clip(square,(ZERO,Q(1),ZERO)),(ZERO,Q(-1),ZERO));assert len(line)==2
    endpoint=clip(line,(ZERO,ZERO,Q(-1)));assert endpoint==[H.vec((0,0))]
    assert not clip(endpoint,(Q(-1),Q(1),ZERO))
    assert rank_affine_max([H.vec((F(1,10),0))],M,H.mul(-1,B1)).sign()<0
    assert C.determinant(*MIRROR)==Q(-1) and source.mm(MIRROR,MIRROR)==source.I
    assert {mv(MIRROR,v) for v in C.V}==set(C.V) and mv(MIRROR,M)==M
    return {'Rodrigues_height_identities':count,'roll_Bernstein_component_identities':bern,
        'closed_clipping_degeneracy_checks':3,'negative_uniform_gain_retained':True,
        'actual_improper_body_vertex_permutation':62,'mirror_fixes_minimum_axis':True}

def controls(rows,records,axes):
    rejected=[]
    def reject(name,job):
        try:job()
        except (AssertionError,ValueError):rejected.append(name)
        else:raise AssertionError('malformed evidence accepted: '+name)
    reject('missing signed roll half',lambda:closed_roll_cover([r for r in rows if r[0]==1]))
    reject('missing roll interval',lambda:closed_roll_cover(rows[:-1]))
    reject('duplicate roll interval',lambda:closed_roll_cover(rows+[rows[-1]]))
    bad=copy.deepcopy(rows);bad[0][1]='1/9';reject('gapped roll endpoint',lambda:closed_roll_cover(bad))
    bad=copy.deepcopy(rows);bad[0][4]=74;reject('unknown original source point',lambda:closed_roll_cover(bad))
    reject('missing reflected source chamber',lambda:closed_source_cover([r for r in records if r[0]==0]))
    reject('missing closed source fan cell',lambda:closed_source_cover([r for r in records if r[1]!=8]))
    reject('missing source leaf',lambda:closed_source_cover(records[:-1]))
    reject('duplicate source leaf',lambda:closed_source_cover(records+[records[-1]]))
    bad=copy.deepcopy(records);bad[0][2]='2';reject('invalid source path',lambda:closed_source_cover(bad))
    bad=copy.deepcopy(records);bad[0][4]=74;reject('false empty source witness',lambda:closed_source_cover(bad))
    root=next(r for r in records if r[2]);bad=records+[root[:2]+['',3,57]]
    reject('overlapping source ancestor',lambda:closed_source_cover(bad))
    reject('missing signed cube face',lambda:parent.closed_covers(axes[:-1]))
    bad=copy.deepcopy(axes);bad[0]['leaves'].pop();reject('missing cube leaf',lambda:parent.closed_covers(bad))
    bad=copy.deepcopy(axes);bad[0]['leaves'].append(bad[0]['leaves'][0]);reject('duplicate cube leaf',lambda:parent.closed_covers(bad))
    bad=copy.deepcopy(axes);bad[0]['leaves'][0][1]=20;reject('unknown original contact',lambda:parent.closed_covers(bad))
    bad=copy.deepcopy(axes);bad[0]['leaves'][0][2]='2';reject('false cube norm lower',lambda:parent.closed_covers(bad))
    reject('wrong mixed Bernstein coefficient',lambda:parent.local.bernstein_identity_audits(F(1,2)))
    incomplete=copy.deepcopy(C.P);incomplete['cell_certificates'].pop()
    reject('missing global physical area cell',lambda:source.structure(incomplete))
    return rejected

def geometry():
    assert C.P['cell_certificates'][8]['corner_indices']==[6,11,10,8]
    edges=[H.cross(u,parent.QUAD[(i+1)%4]) for i,u in enumerate(parent.QUAD)]
    assert all(H.dot(e,u).sign()>=0 for e in edges for u in TRI)
    assert C.area_twice(parent.LARGE)==C.area_twice(TRI)+C.area_twice(parent.TRIANGLES[1])
    sep=C.parse(parent.fixture()['expected']['receiver_geometry']['moving_halfturn_separation_squared_at_m'])
    assert sep>Q(8*RECEIVER_D*RECEIVER_D)
    newpoint=H.mul(F(1,6),H.add(H.add(TRI[0],TRI[1]),H.mul(4,TRI[2])))
    assert C.weak_inside(newpoint,TRI) and not any(C.weak_inside(newpoint,t) for t in parent.TRIANGLES)
    ray=lambda j,t:H.add(M,H.mul(t,H.sub(C.N[j],M)))
    old=[[M,ray(3,F(1,8)),ray(4,F(1,4))],[M,ray(4,F(1,4)),C.N[7]],
        [M,C.N[7],C.N[8]],[M,C.N[8],ray(10,F(1,6))]]
    old += [C.triangle(t) for t in (F(2,5),F(1,2),F(2,3),F(3,4),F(1))]
    old += [parent.nine.FULL]+parent.TRIANGLES
    images=C.orbit(newpoint);assert len(images)==60 and len(old)==12
    for u in images:
        for a,b,c in old:
            det=C.determinant(a,b,c);assert det.sign()!=0
            coordinates=[C.determinant(u,b,c)/det,C.determinant(a,u,c)/det,C.determinant(a,b,u)/det]
            assert not(all(x.sign()>=0 for x in coordinates) or all(x.sign()<=0 for x in coordinates))
    cosine=1-F(1,50)**2/2;centers=C.orbit(M);assert len(centers)==30
    for u in centers:assert Q(cosine*cosine)*H.dot(newpoint,newpoint)*H.dot(u,u)>H.dot(newpoint,u)**2
    return {'entire_closed_collar_parameter':'1/5','original_cell8_corners':[6,11,10,8],
        'first_triangle':[list(map(str,u)) for u in TRI],
        'inherited_second_triangle':[list(map(str,u)) for u in parent.TRIANGLES[1]],
        'whole_collar':[list(map(str,u)) for u in parent.LARGE],
        'moving_halfturn_separation_squared_at_m':str(sep),
        'moving_halfturn_separation_margin':str(sep-Q(8*RECEIVER_D*RECEIVER_D)),
        'strict_new_receiving_witness':list(map(str,newpoint)),
        'proper_projective_witness_images':60,'prior_cones_per_image':12,
        'exact_prior_cone_tests':720,'witness_images_in_prior_cones':0,
        'minimum_projective_axes':30,'new_witness_chord_lower':'1/50 > 1/64'}

def check(rows,records,axes):
    checked=pins();closed_roll_cover(rows);closed_source_cover(records);parent.closed_covers(axes)
    with C.audit_signs() as qa,source.audit_radicals() as ra:
        geom=geometry()
        q,area=C.area_maximum(parent.VECTOR,TRI);assert C.root_upper(q)==T and Q(T*T)>q
        assert all(C.chord_less(u,RECEIVER_D) for u in TRI)
        old=parent.fixture()['expected']['pieces'][1]
        assert old['paired_full_roll_phase']['source_area_upper']=='14824807/1000000'
        nearest=source.nearest_axis();sharp=source.certify(T,A)
        lo,hi=map(F,sharp['sharp_minimum_witness']['chord_rational_enclosure']);assert A-F(1,10**6)<lo<hi<A
        probes,points,data=C.reference.reference();assert (probes,points,data)==(C.PROBES,C.POINTS,C.DATA)
        bounds,receiver=receiver_bounds();directional=replay_source(records,bounds);ph=phase(rows,bounds)
        identities=identity_audits();contacts,support=parent.supports(TRI);faces=parent.replay(contacts,axes)
        basis=parent.local.bernstein_identity_audits();rejected=controls(rows,records,axes)
    return {'agent':'six-rupert-1','role':'researcher','global_Rupert_property':'OPEN',
        'status':'complete exact finite hypotheses for whole closed1/5collar; continuous proof is separate',
        'pins':checked,'entire_closed_collar_parameter':'1/5','new_receiver_triangle':[list(map(str,u)) for u in TRI],
        'receiver_geometry':geom,
        'inherited_second_triangle_byte_pinned':True,'entire_cell8_claimed':False,
        'maximum_receiving_area_squared':str(q),'maximum_area_strata':area,
        'source_area_upper':str(T),'source_chord_upper':str(A),'receiver_chord_upper':str(RECEIVER_D),
        'global_nearest_minimum_axis':nearest,'fresh_source_critical_strata':sharp,
        'reference_facets':16,'reference_original_supports':992,'actual_original_source_points':74,
        'whole_receiver_support_envelopes':receiver,'receiver_vertex_side_comparisons':1984,
        'new_height_aware_source_cover':directional,'full_signed_roll_phase':ph,
        'algebra_and_degeneracy_audits':identities,'original_support_and_Cayley_audits':support,
        'signed_axis_faces':faces,'tensor_Bernstein_basis_identities':basis,'Cayley_radius':'1/8',
        'closed_axis_leaves':sum(f['closed_leaves'] for f in faces),
        'strict_axis_coefficients':sum(f['strict_positive_coefficients'] for f in faces),
        'fixed_roll_sha256':H.digest(rows),'fixed_source_cover_sha256':H.digest(records),'fixed_axes_sha256':H.digest(axes),
        'independent_Q5_sign_audits':qa,'independent_radical_sign_audits':ra,
        'sign_audit_scope':'main verification phase; imported byte-pinned constructors remain inherited prerequisites',
        'malformed_controls_rejected':rejected}

if __name__=='__main__':
    started=time.monotonic();saved=fixture();assert set(saved)=={'roll','source_cover','axes','expected'}
    actual=check(saved['roll'],saved['source_cover'],saved['axes'])
    assert json.loads(json.dumps(actual))==saved['expected'],'all expected mathematical fields must match'
    print(json.dumps({'all_expected_fields_match':True,'global_Rupert_property':'OPEN','entire_closed_collar_parameter':'1/5',
        'source_candidates':actual['fresh_source_critical_strata']['counts']['generated'],
        'source_feasible_candidates':actual['fresh_source_critical_strata']['counts']['feasible'],
        'source_support_leaves':actual['new_height_aware_source_cover']['strict_support_leaves'],
        'source_empty_leaves':actual['new_height_aware_source_cover']['empty_leaves'],
        'closed_axis_leaves':actual['closed_axis_leaves'],'strict_axis_coefficients':actual['strict_axis_coefficients'],
        'full_spatial_angle_upper':actual['full_signed_roll_phase']['full_spatial_angle_upper'],
        'malformed_controls_rejected':len(actual['malformed_controls_rejected']),
        'elapsed_seconds':time.monotonic()-started,'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))
