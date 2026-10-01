"""Fixed exact hypotheses for all-source deltoidal one-third collar rigidity.

Python3.11+ standard library. Run every listed component plus the pinned
Cell11 source checker; no witness search or parent guard changes.
"""
if not __debug__:raise RuntimeError('verification requires assertions; do not use python -O')
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from math import isqrt
from types import SimpleNamespace
import copy,hashlib,itertools,json,sys,time,resource
ROOT=Path(__file__).parent
MODES=['geometry']+['roll:'+str(s)+':'+str(i) for s in (-1,1) for i in range(8)]
KINDS={'E':'EMPTY_CAP','A':'EMPTY_AREA','L':'LOCAL_CAYLEY','S':'STRICT','P':'CORRELATED_STRICT','C':'CORRELATED_EMPTY'}

def binary(paths,depth=3):
    if not paths or len(paths)!=len(set(paths)) or any(type(p) is not str or len(p)>depth or set(p)-set('01') for p in paths):
        raise ValueError('invalid distinct binary paths')
    wanted=set(paths)
    def visit(p):
        if p in wanted:return
        if len(p)>=depth or not any(x.startswith(p) for x in wanted):raise ValueError('binary cover gap')
        visit(p+'0');visit(p+'1')
    visit('')
    if sum((F(1,2)**len(p) for p in paths),F(0))!=1:raise ValueError('overlapping ancestor paths')

def axis_norm(path):
    x=y=F(-1);dx=dy=F(2)
    for char in path:
        i=int(char);dx/=2;dy/=2
        if i in (1,3):x+=dx
        if i in (2,3):y+=dy
    least=lambda a,b:min(a*a,b*b) if a*b>0 else F(0)
    q=1+least(x,x+dx)+least(y,y+dy)
    return F(isqrt(q.numerator*10**12//q.denominator),10**6)

def closed_table(payload):
    if type(payload) is not dict or set(payload)!=set(('source_roll','axes','expected')):raise ValueError('fixture fields')
    rows=payload['source_roll']
    if type(rows) is not list or not rows or type(payload['expected']) is not dict or set(payload['expected'])!=set(MODES):
        raise ValueError('complete component fixture required')
    groups={(s,i,f,c):{} for s in (-1,1) for i in range(8) for f in (0,1) for c in range(11)}
    for row in rows:
        if type(row) is not list or len(row)!=9:raise ValueError('nine exact source/roll controls required')
        s,i,f,c,r,p,k,pi,wi=row
        if any(type(x) is not int for x in (s,i,f,c,pi,wi)) or (s,i,f,c) not in groups:raise ValueError('original root address')
        if type(r) is not str or type(p) is not str or len(r)>3 or len(p)>3 or set(r+p)-set('01'):raise ValueError('binary address')
        if type(k) is not str or k not in KINDS:raise ValueError('leaf kind')
        if k in ('S','P'):
            if not 0<=pi<16 or not 0<=wi<74:raise ValueError('original facet/checked source point')
        elif (pi,wi)!=(-1,-1):raise ValueError('non-support leaf indices')
        groups[s,i,f,c].setdefault(r,[]).append(p)
    if rows!=sorted(rows,key=lambda x:tuple(x[:6])):raise ValueError('canonical fixed table order')
    for rolls in groups.values():
        binary(list(rolls))
        for r,paths in rolls.items():
            binary(paths)
            if len(r)<3 and paths!=['']:raise ValueError('source split precedes complete roll subdivision')
    axes=payload['axes']
    if type(axes) is not list or len(axes)!=2:raise ValueError('two receiving local covers required')
    for cover in axes:
        if type(cover) is not list or len(cover)!=6:raise ValueError('six signed local faces required')
        for face,address in zip(cover,itertools.product(range(3),(-1,1))):
            if type(face) is not dict or set(face)!=set(('axis','sign','leaves')):raise ValueError('local face fields')
            if type(face['axis']) is not int or type(face['sign']) is not int or (face['axis'],face['sign'])!=address:raise ValueError('local face address')
            leaves=face['leaves']
            if type(leaves) is not list or not leaves:raise ValueError('local leaves')
            paths=[]
            for leaf in leaves:
                if type(leaf) is not list or len(leaf)!=3:raise ValueError('local leaf controls')
                p,j,ell=leaf
                if type(p) is not str or len(p)>4 or set(p)-set('0123') or type(j) is not int or not 0<=j<20 or type(ell) is not str:
                    raise ValueError('local leaf address')
                if F(ell)!=axis_norm(p):raise ValueError('false local norm bound')
                paths.append(p)
            wanted=set(paths)
            if len(wanted)!=len(paths):raise ValueError('duplicate local leaf')
            def visit(p):
                if p in wanted:return
                if len(p)>=4 or not any(x.startswith(p) for x in wanted):raise ValueError('local cover gap')
                for c in '0123':visit(p+c)
            visit('')
            if sum((F(1,4)**len(p) for p in paths),F(0))!=1:raise ValueError('local cover overlap')
    return rows

if len(sys.argv) not in (2,3) or sys.argv[1] not in MODES:raise ValueError('select geometry or roll:SIGN:BIN')
MODE=sys.argv[1]
FIXTURE=Path(sys.argv[2]) if len(sys.argv)==3 else ROOT/'expected_cell8_third.json'
PAYLOAD=json.loads(FIXTURE.read_text());TABLE=closed_table(PAYLOAD)
# Complete original-source and local cover grammar is checked BEFORE math imports.
import cell8_quarter_certificate as quarter
C=quarter.C;H=C.H;Q=H.Q5;ZERO=H.ZERO;M=C.M;M2=C.M2
source=quarter.source;fifth=quarter.fifth;base=quarter
tangent=quarter.tangent;clip=quarter.clip;linear=quarter.linear;split=quarter.split
ML=F(21199,20000);MH=F(1059951,1000000);R=F(1,8);T=F(927669,62500)
CENTRAL={0,1,2,3,4,5,6,7,9};WIDE=F(13441,50000);NEAR=F(113081,1000000)
TIP=H.add(H.mul(F(2,3),quarter.parent.nine.W),H.mul(F(1,3),quarter.parent.U))
TRIANGLES=([C.N[8],quarter.parent.nine.W,TIP],[quarter.parent.nine.W,C.N[10],TIP])
D=(F(82447,1000000),F(21027,200000))

PINS={'cell8_quarter_certificate.py': '9a9f8fe631284af34762609a177cb1b2567d316f4ea67a8f7067d29ea4258b61', 'expected_cell8_quarter.json': '401920a61c7a32a3145400955ecd7dd49c11dc251977f86a8d7e7aa1cacc6268', 'cell8_third_source_certificate.py': 'dfe45f16dfdf02e7a36bb4b38a75223801a085026cd79a5c151da2b256ed78e4', 'expected_cell8_third_source.json': 'dad0d2b85c9abac45534a1ffcbec995ee07bd20821f4757f9398f340e522f7ab'}

def norm_extrema(poly):
    assert poly
    ws=[tangent(xy) for xy in poly]
    vals=[H.dot(w,w) for w in ws]
    maximum=max(vals)
    for a,b in zip(ws,ws[1:]+ws[:1]):
        d=H.sub(b,a);d2=H.dot(d,d)
        if d2==ZERO:continue
        assert d2.sign()>0
        t=-H.dot(a,d)/d2
        if t.sign()>=0 and (1-t).sign()>=0:
            w=H.add(a,H.mul(t,d));vals.append(H.dot(w,w))
    area=sum((a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])),ZERO)
    if area!=ZERO:
        sg=area.sign()
        if all((sg*(a[0]*b[1]-a[1]*b[0])).sign()>=0 for a,b in zip(poly,poly[1:]+poly[:1])):
            vals.append(ZERO)
    minimum=min(vals)
    assert minimum.sign()>=0 and maximum>=minimum
    return minimum,maximum

class BranchEnclosure(base.Enclosure):

    def __init__(self,a,t,bounds,near):
        assert 0<near<a<F(1,3) and t>0 and len(bounds)==16
        assert (M2-Q(ML*ML)).sign()>0 and (Q(MH*MH)-M2).sign()>0
        self.a=a;self.t=t;self.bounds=tuple(bounds);self.cos=1-a*a/2
        assert self.cos>F(17,18)
        self.cap2=M2*(1/self.cos**2-1)
        self.near=near;self.near2=M2*(1/(1-near*near/2)**2-1)
        self.factor_cache={};self.point_cache={};self.probe_cache={};self.cache={}

    def factors(self,poly):
        key=tuple(poly)
        if key in self.factor_cache:return self.factor_cache[key]
        minimum,maximum=norm_extrema(poly)
        if minimum>self.cap2:
            self.factor_cache[key]=None;return None
        upper=min(maximum,self.cap2)
        ru=C.root_upper(M2+upper);rl=C.root_upper(M2+minimum)-F(1,10**6)
        assert rl>0 and (M2+minimum-Q(rl*rl)).sign()>=0
        assert (Q(ru*ru)-M2-upper).sign()>0
        cl=max(self.cos,ML/ru);ch=min(F(1),MH/rl)
        assert 0<cl<=ch<=1
        ll,lh=Q(cl)/M2,Q(ch)/M2
        bl,bh=Q(cl*cl/(1+cl))/M2,Q(ch*ch/(1+ch))/M2
        rw=C.root_upper(upper)
        result=((ll+lh)/2,(lh-ll)/2,(bl+bh)/2,(bh-bl)/2,lh,bh,rw,upper,
            minimum,maximum,cl,ch)
        assert result[1].sign()>=0 and result[3].sign()>=0
        self.factor_cache[key]=result;return result

    def rank_max(self,poly,p,v,lmid,bmid):
        ws=[tangent(xy) for xy in poly];height=H.dot(M,p)
        vals=[(lmid*height+bmid*H.dot(p,w))*H.dot(v,w) for w in ws]
        for a,b in zip(ws,ws[1:]+ws[:1]):
            d=H.sub(b,a);pa=lmid*height+bmid*H.dot(p,a);pd=bmid*H.dot(p,d)
            va,vd=H.dot(v,a),H.dot(v,d);aa=pd*vd;bb=pa*vd+pd*va;cc=pa*va
            if aa.sign()<0:
                t=-bb/(2*aa)
                if t.sign()>=0 and (1-t).sign()>=0:vals.append(cc-bb*bb/(4*aa))
        return max(vals)

    def fixed(self,lo,hi,pi,wi,sign):
        key=(lo,hi,pi,wi,sign)
        if key in self.cache:return self.cache[key]
        p=C.POINTS[wi][0];probe=C.PROBES[pi];mu=probe['mu'];z=H.cross(M,mu)
        if wi not in self.point_cache:
            pp=base.project(p,M);self.point_cache[wi]=C.root_upper(H.dot(pp,pp))
        if pi not in self.probe_cache:self.probe_cache[pi]=C.root_upper(H.dot(z,z))
        rp=self.point_cache[wi];rz=self.probe_cache[pi];eta=probe['norm_upper']
        assert H.dot(mu,M)==H.dot(z,M)==ZERO
        vectors=[H.sub(H.mul(1-lo*lo,mu),H.mul(2*sign*lo*fifth.IM,z)),
            H.sub(H.mul(1-lo*hi,mu),H.mul(sign*(lo+hi)*fifth.IM,z)),
            H.sub(H.mul(1-hi*hi,mu),H.mul(2*sign*hi*fifth.IM,z))]
        gamma=C.DATA[pi][wi]['d'];tau=C.DATA[pi][wi]['tau'][sign]
        co=(gamma-probe['H']-self.bounds[pi],Q(2*tau),-gamma-probe['H']-self.bounds[pi])
        assert co[2].sign()<=0
        out=(p,vectors,co,rp,rz,eta);self.cache[key]=out;return out

    def witness(self,poly,lo,hi,pi,wi,sign):
        fm=self.factors(poly);assert fm is not None
        lm,le,bm,be,lh,bh,rw,u,*_=fm
        p,vectors,co,rp,rz,eta=self.fixed(lo,hi,pi,wi,sign)
        h=H.dot(M,p);h=h if h.sign()>=0 else -h
        error=le*h*(1+hi*hi)*eta*rw+be*rp*(1+hi*hi)*eta*u
        error+=(lh*h+bh*rp*rw)*Q(2*hi*fifth.IE*rz*rw)
        assert error.sign()>=0
        upper=max(self.rank_max(poly,p,v,lm,bm) for v in vectors)+error
        margins=[co[0]+co[1]*x+co[2]*x*x-upper for x in (lo,hi)]
        return all(x.sign()>0 for x in margins),{'probe':pi,'point':wi,
            'source_loss_numerator_upper':str(upper),'strict_endpoint_margins':list(map(str,margins)),
            'local_cosine_factor_interval':list(map(str,fm[-2:])),
            'local_norm_squared_extrema':list(map(str,fm[-4:-2]))}

b=SimpleNamespace(C=C,H=H,Q5=Q,M=M,M2=M2,ML=ML,MH=MH,base=base,tangent=tangent,clip=clip,linear=linear,split=split,norm_extrema=norm_extrema,BranchEnclosure=BranchEnclosure)
def root_interval(q):
    hi=C.root_upper(q);lo=hi-F(1,10**6)
    assert lo>=0 and (q-Q(lo*lo)).sign()>=0 and (Q(hi*hi)-q).sign()>0
    return lo,hi

def lower_grid(q):
    hi=C.grid_upper(lambda x:Q(x)>q,F(20))
    lo=hi-F(1,10**6)
    assert Q(lo)<=q<Q(hi)
    return lo

def receiving_polygon(tri):
    out=[]
    for u in tri:
        den=H.dot(M,u);assert den.sign()>0
        v=H.sub(H.mul(M2/den,u),M)
        assert H.dot(v,M)==ZERO and b.tangent((v[0],v[1]))==v
        out.append((v[0],v[1]))
    # Projective weights proportional to positive M.u preserve convex hull.
    return out

def source_area_lower(poly,cell,fold=0):
    assert fold in (0,1)
    av=H.vec(map(C.parse,C.P['cell_certificates'][cell]['area_vector']))
    if fold:av=b.base.mv(b.base.MIRROR,av)
    corners=[]
    for xy in poly:
        q=H.add(M,b.tangent(xy));area=H.dot(av,q)
        assert area.sign()>0
        ru=root_interval(H.dot(q,q))[1]
        corners.append(area/ru)
    lo=lower_grid(min(corners));assert lo>0
    return lo,{'fold':fold,'corner_lower_bounds':list(map(str,corners)),
        'physical_source_area_lower':str(lo),'cell_area_vector':list(map(str,av))}

def area_clip(poly,area_lower,rounds=2):
    av=H.vec(map(C.parse,C.P['cell_certificates'][8]['area_vector']))
    records=[]
    for iteration in range(rounds):
        if not poly:break
        anchors=poly[:]
        center=tuple(sum((xy[k] for xy in poly),ZERO)/len(poly) for k in (0,1))
        anchors.append(center)
        for xy in anchors:
            u=H.add(M,b.tangent(xy));ru=root_interval(H.dot(u,u))[1]
            vec=H.sub(av,H.mul(area_lower/ru,u))
            row=b.linear(vec)
            poly=b.clip(poly,row)
            records.append({'iteration':iteration,'anchor':list(map(str,xy)),
                'anchor_norm_upper':str(ru),'necessary_area_halfplane':list(map(str,row))})
            if not poly:break
    return poly,records

def factors(poly,cap2=None):
    lo2,hi2=b.norm_extrema(poly)
    if cap2 is not None:hi2=min(hi2,cap2)
    assert hi2>=lo2
    rlo=root_interval(M2+lo2)[0];rhi=root_interval(M2+hi2)[1]
    flo=1/(rhi+MH);fhi=1/(rlo+ML)
    assert 0<flo<=fhi
    rw=root_interval(hi2)[1]
    return flo,fhi,rw,lo2,hi2

def gate(source,receiver,roll_upper,source_cap2=None):
    assert 0<=roll_upper<=F(1,8)
    sl,sh,sw,*_=factors(source,source_cap2)
    rl,rh,rw,*_=factors(receiver)
    ws=[b.tangent(xy) for xy in source];vs=[b.tangent(xy) for xy in receiver]
    d2=max(H.dot(H.sub(w,v),H.sub(w,v)) for w in ws for v in vs)
    dotlo=min(H.dot(w,v) for w in ws for v in vs)
    # Squared distance is separately convex and dot product separately affine.
    du=root_interval(d2)[1]
    mismatch=max(abs(rh-sl),abs(sh-rl))
    delta=sh*du+mismatch*rw
    source_cayley=sh*sw
    norm_factor=root_interval(Q(1+source_cayley*source_cayley))[1]
    denom=1+sl*rl*dotlo if dotlo.sign()>=0 else 1+sh*rh*dotlo
    assert denom.sign()>0
    relative=Q(delta*norm_factor)/denom
    assert relative.sign()>=0 and (1-relative*roll_upper).sign()>0
    triangle_total=(relative+roll_upper)/(1-relative*roll_upper)
    # Direct signed quaternion product retains the orthogonality of roll
    # and tilt. Its numerator/normalization identity is audited separately.
    absdot=max(absval(H.dot(w,v)) for w in ws for v in vs)
    cross2=max(H.dot(M,H.cross(w,v))**2/M2 for w in ws for v in vs)
    crossup=sh*rh*root_interval(cross2)[1]
    dotabsup=sh*rh*absdot
    recv_cayley=rh*rw
    direct_den=1+(sl*rl*dotlo if dotlo.sign()>=0 else sh*rh*dotlo)-roll_upper*crossup
    assert direct_den.sign()>0
    numerator2=Q(delta*delta*(1+source_cayley*source_cayley))
    numerator2+=roll_upper*roll_upper*(1+source_cayley*source_cayley+recv_cayley*recv_cayley+dotabsup*dotabsup)
    numerator2+=2*roll_upper*crossup*(1+dotabsup)
    direct_num=C.root_upper(numerator2)
    direct_total=direct_num/direct_den
    total=min(triangle_total,direct_total)
    margin=R-total
    return {'source_cayley_factor_interval':list(map(str,(sl,sh))),
        'receiver_cayley_factor_interval':list(map(str,(rl,rh))),
        'source_tangent_norm_upper':str(sw),'receiver_tangent_norm_upper':str(rw),
        'paired_tangent_distance_squared_upper':str(d2),'paired_tangent_distance_upper':str(du),
        'paired_tangent_dot_lower':str(dotlo),'factor_mismatch_upper':str(mismatch),
        'source_receiver_cayley_vector_distance_upper':str(delta),
        'source_cayley_norm_upper':str(source_cayley),'norm_factor_upper':str(norm_factor),
        'relative_quaternion_scalar_lower':str(denom),
        'unrolled_relative_cayley_upper':str(relative),'roll_tangent_upper':str(roll_upper),
        'triangle_angle_cayley_upper':str(triangle_total),
        'paired_cayley_cross_upper':str(crossup),'paired_cayley_absolute_dot_upper':str(dotabsup),
        'direct_quaternion_scalar_lower':str(direct_den),
        'direct_quaternion_vector_squared_upper':str(numerator2),
        'direct_quaternion_vector_norm_upper':str(direct_num),
        'direct_quaternion_cayley_upper':str(direct_total),
        'actual_rolled_cayley_upper':str(total),'radius1_8_margin':str(margin),
        'certified_radius1_8':margin.sign()>0}

def absval(q):
    return q if q.sign()>=0 else -q

def correlated_bounds(source,cell,fold,receiver):
    area_lower,area=source_area_lower(source,cell,fold)
    clipped,cuts=area_clip(receiver,area_lower)
    if not clipped:return None,{'empty':True,'area':area,'cuts':cuts,'receiver_polygon':[]}
    raw=[H.add(M,b.tangent(xy)) for xy in clipped]
    d=max(C.grid_upper(lambda x:C.chord_less(u,x),F(1,5)) for u in raw)
    bounds,records=b.base.receiver_bounds(raw,d)
    return bounds,{'empty':False,'area':area,'cuts':cuts,
        'receiver_polygon':[list(map(str,p)) for p in clipped],
        'receiver_chord_upper':str(d),'signed_receiver_bounds':records}

def correlated_model(poly,cell,fold,receivers,cap):
    records=[];bounds=[]
    for case,receiver in enumerate(receivers):
        bd,record=correlated_bounds(poly,cell,fold,receiver)
        records.append({'case':case,**record})
        if bd is not None:bounds.append(bd)
    if not bounds:return None,{'paired_receivers':records,'all_receivers_empty':True}
    combined=[max(row[i] for row in bounds) for i in range(16)]
    model=b.BranchEnclosure(cap,F(927669,62500),combined,F(1,16))
    return model,{'paired_receivers':records,'all_receivers_empty':False,
                  'combined_correlated_receiver_bounds':list(map(str,combined))}
def fixed_leaf(sign,index,l,receivers,roots):
    fold,cell=l['fold'],l['cell'];poly,model=roots[fold,cell]
    lo,hi=F(index,8),F(index+1,8)
    poly=model.tighten(poly,fold,cell)
    for bit in l['roll_path']:
        mid=(lo+hi)/2
        lo,hi=(lo,mid) if bit=='0' else (mid,hi)
        poly=model.tighten(poly,fold,cell)
    for bit in l['source_path']:
        children=b.split(poly);assert len(children)==2
        poly=model.tighten(children[int(bit)],fold,cell)
    label={'fold':fold,'cell':cell,'source_path':l['source_path'],'roll_path':l['roll_path'],
           'closed_interval':list(map(str,(lo,hi)))}
    fm=model.factors(poly) if poly else None
    if l['kind']=='EMPTY_CAP':
        assert not poly or fm is None
        actual={**label,'kind':'EMPTY_CAP'}
    else:
        assert poly and fm is not None
        area_lower,area=source_area_lower(poly,cell,fold)
        if l['kind']=='EMPTY_AREA':
            assert area_lower>F(927669,62500)
            actual={**label,'kind':'EMPTY_AREA','area':area}
        elif l['kind'] in ('CORRELATED_STRICT','CORRELATED_EMPTY'):
            paired_model,geometry=correlated_model(poly,cell,fold,receivers,model.a)
            if l['kind']=='CORRELATED_EMPTY':
                assert paired_model is None
                actual={**label,'kind':l['kind'],'source_polygon':[list(map(str,p)) for p in poly],**geometry}
            else:
                assert paired_model is not None
                okay,proof=paired_model.witness(poly,lo,hi,l['probe'],l['point'],sign);assert okay
                actual={**label,'kind':l['kind'],'source_polygon':[list(map(str,p)) for p in poly],**geometry,**proof}
        elif l['kind']=='STRICT':
            okay,proof=model.witness(poly,lo,hi,l['probe'],l['point'],sign);assert okay
            actual={**label,'kind':'STRICT','source_polygon':[list(map(str,p)) for p in poly],**proof}
        else:
            assert hi<=F(1,8)
            local=[]
            for case,receiver in enumerate(receivers):
                clipped,cuts=area_clip(receiver,area_lower)
                gate_record=gate(poly,clipped,hi,model.cap2) if clipped else None
                assert not clipped or gate_record['certified_radius1_8']
                local.append({'case':case,'empty':not clipped,'area':area,'cuts':cuts,
                    'receiver_polygon':[list(map(str,p)) for p in clipped],'gate':gate_record})
            actual={**label,'kind':'LOCAL_CAYLEY','source_polygon':[list(map(str,p)) for p in poly],
                    'paired_receivers':local}
    return actual
def strata(t):
    cells,nodes=source.structure(C.P)
    assert nodes==C.N
    records=[]; total=Counter()
    for row in C.P['cell_certificates']:
        ci=row['cell']; corners=[nodes[j] for j in row['corner_indices']]
        av=H.vec(map(C.parse,row['area_vector'])); av2=H.dot(av,av)
        sides=[H.cross(u,corners[(i+1)%len(corners)]) for i,u in enumerate(corners)]
        assert av2.sign()>0
        assert all(H.dot(e,e).sign()>0 for e in sides)
        assert all(H.dot(e,u).sign()>=0 for e in sides for u in corners)
        assert all(H.dot(C.M,u).sign()>0 and u[2].sign()>0 for u in corners)
        candidates=[]
        def put(kind,edge,n,active_area=False,active_edge=False):
            norm=sum((x*x for x in n),0)
            assert norm.sign()==1 and (norm-1).sign()==0
            if active_area:assert (source.rdot(av,n)-t).sign()==0
            if active_edge:assert source.rdot(sides[edge],n).sign()==0
            cone=[source.rdot(e,n).sign() for e in sides]
            feasible=n[2].sign()>0 and all(s>=0 for s in cone) and (source.rdot(av,n)-t).sign()<=0
            rec={'kind':kind,'edge':edge,'n':n,'feasible':feasible,'cone_signs':cone}
            if feasible:
                objective=source.rdot(C.M,n);assert objective.sign()>0
                rec['objective']=objective
                total['feasible']+=1
            candidates.append(rec);total['generated']+=1;total[kind]+=1
        for i,u in enumerate(corners):put('corner',i,source.normalized(u))
        for sg in (-1,1):put('sphere_stationary',None,source.normalized(C.M,sg))
        proj=H.sub(C.M,H.mul(H.dot(C.M,av)/av2,av)); proj2=H.dot(proj,proj)
        assert proj2.sign()>0
        r2=1-t*t/av2
        if r2.sign()>=0:
            a=H.mul(t/av2,av)
            for sg in (-1,1):put('area_stationary',None,source.candidate(a,H.mul(sg,proj),r2/proj2),True)
        for ei,e in enumerate(sides):
            e2=H.dot(e,e); me=H.sub(C.M,H.mul(H.dot(C.M,e)/e2,e))
            assert H.dot(me,me).sign()>0
            for sg in (-1,1):put('edge_stationary',ei,source.normalized(me,sg),False,True)
            cp=H.sub(av,H.mul(H.dot(av,e)/e2,e)); cp2=H.dot(cp,cp)
            assert cp2.sign()>0
            r2=1-t*t/cp2
            if r2.sign()>=0:
                b=H.cross(e,cp);b2=H.dot(b,b);assert b2.sign()>0
                a=H.mul(t/cp2,cp)
                for sg in (-1,1):put('area_edge_intersection',ei,source.candidate(a,H.mul(sg,b),r2/b2),True,True)
        records.append({'cell':ci,'candidates':candidates})
    return records,total

def radius(f):
    ml,mh=source.qinterval(C.M2,128)
    ml,mh=source.sqrti(ml,128)[0],source.sqrti(mh,128)[1]
    fl,fh=source.interval(f,128)
    lo=source.sqrti(2-2*fh/ml,96)[0]
    hi=source.sqrti(2-2*fl/mh,96)[1]
    return lo,hi

def summary(records):
    out=[]
    for row in records:
        feasible=[r for r in row['candidates'] if r['feasible']]
        if not feasible:
            out.append({'cell':row['cell'],'generated':len(row['candidates']),'feasible':0,'empty':True});continue
        winner=feasible[0]
        for r in feasible[1:]:
            if source.compare(r['objective'],winner['objective'])<0:winner=r
        comparisons=[source.compare(r['objective'],winner['objective']) for r in feasible]
        assert all(s>=0 for s in comparisons)
        tied=[r for r,s in zip(feasible,comparisons) if s==0]
        for r in tied:assert all(source.compare(x,y)==0 for x,y in zip(r['n'],winner['n']))
        lo,hi=radius(winner['objective'])
        cap=F((hi*10**6).numerator//(hi*10**6).denominator+1,10**6)
        lower=cap-F(1,10**6);threshold=Q((1-cap*cap/2)**2)*C.M2
        assert 0<cap<1
        assert all((r['objective']*r['objective']-threshold).sign()>0 for r in feasible)
        assert (winner['objective']*winner['objective']-Q((1-lower*lower/2)**2)*C.M2).sign()<0
        out.append({'cell':row['cell'],'generated':len(row['candidates']),'feasible':len(feasible),'empty':False,
            'sharp_chord_window':[str(lower),str(cap)],'chord_rational_enclosure':[str(lo),str(hi)],
            'minimum_occurrences':[[r['kind'],r['edge']] for r in tied],
            'minimum_comparisons':{str(k):v for k,v in Counter(comparisons).items()},
            'objective':winner['objective'].serial(),'direction':[x.serial() for x in winner['n']]})
    return out

def pins():
    out=quarter.pins()
    for name in ('cell8_quarter_certificate.py','expected_cell8_quarter.json','cell8_third_source_certificate.py','expected_cell8_third_source.json'):
        wanted=PINS[name];assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==wanted
        out[name]=wanted
    assert quarter.parent.R==R and quarter.parent.MAX_DEPTH==4
    return out

def setup():
    receivers=[receiving_polygon(tri) for tri in TRIANGLES]
    bounds=[quarter.receiver_bounds(tri,d)[0] for tri,d in zip(TRIANGLES,D)]
    combined=[max(row[i] for row in bounds) for i in range(16)]
    models={False:BranchEnclosure(WIDE,T,combined,F(1,16)),True:BranchEnclosure(NEAR,T,combined,F(1,16))}
    roots={}
    for near,model in models.items():
        polys,_=model.source_polygons()
        for fold,cell,poly in polys:
            if cell<11 and (cell in CENTRAL)==near:roots[fold,cell]=(poly,model)
    assert len(roots)==22
    return receivers,roots

def geometry():
    quad=[C.N[j] for j in (6,11,10,8)]
    assert C.P['cell_certificates'][8]['corner_indices']==[6,11,10,8]
    assert quarter.parent.U==H.mul(F(1,4),tuple(sum((u[k] for u in quad),ZERO) for k in range(3)))
    edges=[H.cross(u,quad[(i+1)%4]) for i,u in enumerate(quad)]
    assert all(H.dot(e,u).sign()>=0 for e in edges for tri in TRIANGLES for u in tri)
    assert all(H.dot(e,TIP).sign()>0 for e in edges)
    full=[C.N[8],C.N[10],TIP]
    assert C.area_twice(full)==sum((C.area_twice(tri) for tri in TRIANGLES),ZERO)
    ratio=Q(F(17,57),F(4,57));assert ratio.sign()>0 and (1-ratio).sign()>0
    assert quarter.parent.nine.W==H.add(H.mul(1-ratio,C.N[8]),H.mul(ratio,C.N[10]))
    assert all(C.weak_inside(u,full) for u in quarter.FULL)
    axis=source.nearest_axis()
    for wall in source.WALLS:
        mat=source.reflection(wall)
        assert source.determinant(*mat)==Q(-1) and {source.mv(mat,v) for v in C.V}==set(C.V)
    assert source.mv(source.reflection(source.WALLS[2]),M)==M
    assert all(H.mul(-1,v) in C.V for v in C.V)
    records,counts=strata(T);cells=summary(records)
    actualcentral={r['cell'] for r in cells if r['empty'] or F(r['sharp_chord_window'][1])<F(1,4)}
    assert actualcentral==CENTRAL
    assert max(F(r['sharp_chord_window'][1]) for r in cells if not r['empty'] and r['cell'] in CENTRAL)==NEAR
    assert max(F(r['sharp_chord_window'][1]) for r in cells if not r['empty'])==WIDE
    assert dict(counts)=={'generated':212,'corner':40,'sphere_stationary':24,'area_stationary':18,'edge_stationary':80,'area_edge_intersection':50,'feasible':65}
    pieces=[];av=H.vec(map(C.parse,C.P['cell_certificates'][8]['area_vector']))
    for case,tri in enumerate(TRIANGLES):
        maximum,active=C.area_maximum(av,tri)
        assert C.root_upper(maximum)==T and (Q(T*T)-maximum).sign()>0 and active['active_strata']==['corner2']
        assert max(C.grid_upper(lambda d:C.chord_less(u,d),F(1,5)) for u in tri)==D[case]
        contacts,support=quarter.parent.supports(tri)
        faces=quarter.parent.replay(contacts,PAYLOAD['axes'][case])
        pieces.append({'case':case,'receiving_rays':[[str(x) for x in u] for u in tri],
            'maximum_physical_area_squared':str(maximum),'complete_area_strata':active,
            'receiver_chord_upper':str(D[case]),'original_support_geometry':support,
            'signed_axis_faces':faces,'fixed_axes_sha256':H.digest(PAYLOAD['axes'][case])})
    sep=Q(F(106,29),F(-36,29));margin=sep-Q(8*max(D)**2);assert margin.sign()>0
    return {'original_cell8_corners':[6,11,10,8],'closed_collar_parameter':'1/3',
        'entire_closed_partition_checked':True,'proper_gauge_chambers':['H','SH'],
        'all_original_source_cells':cells,'complete_critical_counts':dict(counts),
        'central_source_cells':sorted(CENTRAL),'central_source_chord_upper':str(NEAR),
        'wide_source_chord_upper':str(WIDE),'nearest_axis_certificate':axis,'pieces':pieces,
        'moving_halfturn_separation_squared_at_m':str(sep),'moving_halfturn_separation_margin':str(margin),
        'closed_axis_leaves':sum(f['closed_leaves'] for p in pieces for f in p['signed_axis_faces']),
        'strict_positive_coefficients':sum(f['strict_positive_coefficients'] for p in pieces for f in p['signed_axis_faces'])}

def roll(sign,index,captures=None):
    receivers,roots=setup();digest=hashlib.sha256();counts=Counter();records=[];positive=negative=0
    for sg,i,fold,cell,r,p,kind,pi,wi in TABLE:
        if (sg,i)!=(sign,index):continue
        leaf={'fold':fold,'cell':cell,'roll_path':r,'source_path':p,'kind':KINDS[kind]}
        if kind in ('S','P'):leaf.update(probe=pi,point=wi)
        actual=fixed_leaf(sign,index,leaf,receivers,roots)
        record={'sign':sign,'bin':index,**actual};records.append(record)
        digest.update(json.dumps(record,sort_keys=True,separators=(',',':')).encode());counts[actual['kind']]+=1
        if kind in ('S','P'):
            positive+=2;negative+=C.parse(actual['source_loss_numerator_upper']).sign()<0
    assert records
    if captures is not None:captures.extend(records)
    return {'original_roots':22,'closed_interval':[str(F(index,8)),str(F(index+1,8))],
        'sign':sign,'bin':index,'leaf_counts':dict(counts),'strict_endpoint_margins':positive,
        'retained_negative_uniform_losses':negative,'entrywise_record_sha256':digest.hexdigest()}

def compute(mode,captures=None):
    pinned=pins()
    with C.audit_signs() as qa,source.audit_radicals() as ra:
        if mode=='geometry':result=geometry()
        else:
            _,sign,index=mode.split(':');result=roll(int(sign),int(index),captures)
    return {'pins_sha256':H.digest(pinned),'pinned_dependency_count':len(pinned),'component':mode,'result':result,'Q5_sign_audits':qa,'radical_sign_audits':ra,
        'complete_source_roll_table_sha256':H.digest(TABLE),'fixed_axes_sha256':H.digest(PAYLOAD['axes'])}

if __name__=='__main__':
    start=time.monotonic();actual=compute(MODE)
    assert actual==PAYLOAD['expected'][MODE],'fresh component does not match every expected field'
    print(json.dumps({'agent':'six-rupert-1','role':'researcher','component':MODE,
        'status':'COMPLETE fixed exact component; all components and pinned Cell11 proof required',
        'all_expected_fields_match':True,'global_Rupert_property':'OPEN',
        'result':{k:v for k,v in actual['result'].items() if k not in ('pieces','all_original_source_cells')},
        'pinned_dependency_count':actual['pinned_dependency_count'],'Q5_sign_audits':actual['Q5_sign_audits'],
        'radical_sign_audits':actual['radical_sign_audits'],'elapsed_seconds':time.monotonic()-start,
        'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))
