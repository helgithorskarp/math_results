"""Exact Cell11 source exclusion for the closed deltoidal 1/3 receiver collar.

Python3.11+ stdlib. See cell8_third_source_proof.md for the continuous proof.
Fixed original-vertex witnesses; no discovery or parent-guard mutation.
The whole 1/3 receiving exclusion and global Rupert decision remain OPEN.
"""
if not __debug__:
    raise RuntimeError('verification requires assertions; do not use python -O')
from pathlib import Path
from fractions import Fraction as F
import copy,hashlib,json,sys,time,resource
ROOT=Path(__file__).parent

def closed_table(payload):
    if type(payload) is not dict or set(payload)!=set(('roll','expected')):
        raise ValueError('fixture must have exactly roll and expected fields')
    rows=payload['roll']
    if type(payload['expected']) is not dict or type(rows) is not list or len(rows)!=32:
        raise ValueError('32 fixed closed source/roll patches required')
    addresses=[(sg,i,f) for sg in (-1,1) for i in range(8) for f in (0,1)]
    for row,address in zip(rows,addresses):
        if type(row) is not list or len(row)!=5 or any(type(x) is not int for x in row):
            raise ValueError('each patch has five exact integer controls')
        if tuple(row[:3])!=address or not 0<=row[3]<16 or not 0<=row[4]<62:
            raise ValueError('closed signed roll/source cover or original vertex index invalid')
    return rows

# Malformed controls and optimized execution fail before mathematical imports.
if len(sys.argv)>2:
    raise ValueError('at most one fixture path')
FIXTURE_PATH=Path(sys.argv[1]) if len(sys.argv)==2 else ROOT/'expected_cell8_third_source.json'
PAYLOAD=json.loads(FIXTURE_PATH.read_text())
TABLE=closed_table(PAYLOAD)
import cell8_quarter_certificate as quarter
C=quarter.C;H=C.H;Q=H.Q5;ZERO=H.ZERO;M=C.M;M2=C.M2
source=quarter.source;fifth=quarter.fifth
T=F(927669,62500);A=F(13441,50000);A_MINUS=F(268819,1000000)
D=(F(82447,1000000),F(21027,200000))
ML=F(21199,20000);MH=F(1059951,1000000)
TIP=H.add(H.mul(F(2,3),quarter.parent.nine.W),H.mul(F(1,3),quarter.parent.U))
TRIANGLES=([C.N[8],quarter.parent.nine.W,TIP],[quarter.parent.nine.W,C.N[10],TIP])
tangent=quarter.tangent
PINS={'cell8_quarter_certificate.py': '9a9f8fe631284af34762609a177cb1b2567d316f4ea67a8f7067d29ea4258b61', 'expected_cell8_quarter.json': '401920a61c7a32a3145400955ecd7dd49c11dc251977f86a8d7e7aa1cacc6268'}


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

class SourceBands(quarter.Enclosure):
    def __init__(self,bounds):
        # NEW explicitly proved acute source scope; inherited constructor is untouched.
        assert 0<A<F(1,3) and T>0 and len(bounds)==16
        assert (M2-Q(ML*ML)).sign()>0 and (Q(MH*MH)-M2).sign()>0
        self.a=A;self.t=T;self.bounds=tuple(bounds);self.cos=1-A*A/2
        assert self.cos>F(17,18)
        self.cap2=M2*(1/self.cos**2-1)
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
            pp=quarter.project(p,M);self.point_cache[wi]=C.root_upper(H.dot(pp,pp))
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


def pins():
    out=quarter.pins()
    for name,wanted in PINS.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==wanted
    assert quarter.A==[F(14141,125000),F(113349,1000000)]
    assert quarter.fifth.SOURCE_DEPTH==1 and quarter.parent.R==F(1,8)
    return {**out,**PINS}

def controls(rows):
    def payload(r):return {'roll':r,'expected':{}}
    cases=[]
    cases.extend(([],rows[:-1],rows+[rows[0]],list(reversed(rows))))
    r=copy.deepcopy(rows);r[1]=r[0][:];cases.append(r)
    r=copy.deepcopy(rows);r[0]=r[0][:-1];cases.append(r)
    r=copy.deepcopy(rows);r[0].append(0);cases.append(r)
    for pos,values in ((0,(0,1,True,'-1')),(1,(-1,1,True,0.0,'0')),
                       (2,(-1,1,True)),(3,(-1,16,True,'3')),(4,(-1,62,True,'57'))):
        for value in values:
            r=copy.deepcopy(rows);r[0][pos]=value;cases.append(r)
    r=copy.deepcopy(rows);r[0]=tuple(r[0]);cases.append(r)
    malformed=[payload(r) for r in cases]
    malformed.extend(({'roll':rows},{'roll':rows,'expected':[]},
                      {'roll':rows,'expected':{},'extra':0},None))
    for bad in malformed:
        try:closed_table(bad)
        except ValueError:pass
        else:raise AssertionError('malformed control accepted')
    return len(malformed)

def geometry():
    quad=[C.N[j] for j in (6,11,10,8)]
    assert C.P['cell_certificates'][8]['corner_indices']==[6,11,10,8]
    assert C.P['cell_certificates'][11]['corner_indices']==[11,13,12]
    assert H.mul(F(1,4),tuple(sum((u[k] for u in quad),ZERO) for k in range(3)))==quarter.parent.U
    sides=[H.cross(u,quad[(i+1)%4]) for i,u in enumerate(quad)]
    assert all(H.dot(e,u).sign()>=0 for e in sides for tri in TRIANGLES for u in tri)
    assert all(H.dot(e,TIP).sign()>0 for e in sides)
    assert C.area_twice([C.N[8],C.N[10],TIP])==sum((C.area_twice(tri) for tri in TRIANGLES),ZERO)
    axis=source.nearest_axis()
    mirrors=[]
    for w in source.WALLS:
        mat=source.reflection(w)
        assert source.determinant(*mat)==Q(-1)
        assert {source.mv(mat,v) for v in C.V}==set(C.V)
        mirrors.append(mat)
    assert mirrors[2]==quarter.MIRROR and source.mv(mirrors[2],M)==M
    assert all(H.mul(-1,v) in C.V for v in C.V)
    return {'closed_receiver_triangles':[[list(map(str,u)) for u in tri] for tri in TRIANGLES],
        'entire_collar_partition_checked':True,'collar_parameter':'1/3',
        'original_cell11_corners':[11,13,12],'nearest_axis_certificate':axis,
        'original_reflection_vertex_comparisons':3*62,'central_symmetry_vertices':62,
        'proper_gauge_source_chambers':['H','SH'],'third_reflection_fixes_M':True}

def norm_regressions():
    b1,b2=quarter.B1,quarter.B2
    g11,g12,g22=H.dot(b1,b1),H.dot(b1,b2),H.dot(b2,b2)
    segment=[(Q(-1),Q(0)),(Q(1),Q(0))]
    assert norm_extrema(segment)==(ZERO,g11)
    assert norm_extrema([(Q(0),Q(0))])==(ZERO,ZERO)
    square=[(Q(-1),Q(-1)),(Q(1),Q(-1)),(Q(1),Q(1)),(Q(-1),Q(1))]
    assert norm_extrema(square)[0]==ZERO
    assert norm_extrema(list(reversed(square)))==norm_extrema(square)
    triangle=[(Q(1),Q(-1)),(Q(1),Q(1)),(Q(2),Q(0))]
    minimum,maximum=norm_extrema(triangle)
    assert (g22-g12*g12/g11).sign()>0 and (g11-g12*g12/g22).sign()>0
    assert minimum==g11-g12*g12/g22
    assert maximum==max(H.dot(tangent(xy),tangent(xy)) for xy in triangle)
    assert norm_extrema(list(reversed(triangle)))==(minimum,maximum)
    return 6

def compute(rows,captures=None):
    start=time.monotonic();checked_pins=pins()
    with C.audit_signs() as qa,source.audit_radicals() as ra:
        geometric=geometry();nr=norm_regressions()
        av=H.vec(map(C.parse,C.P['cell_certificates'][8]['area_vector']))
        receivers=[];receiver_bounds=[]
        for case,tri in enumerate(TRIANGLES):
            maximum,strata=C.area_maximum(av,tri)
            assert C.root_upper(maximum)==T and (Q(T*T)-maximum).sign()>0
            assert strata['active_strata']==['corner2']
            assert max(C.grid_upper(lambda d:C.chord_less(u,d),F(1,5)) for u in tri)==D[case]
            _,original=quarter.parent.supports(tri)
            bounds,records=quarter.receiver_bounds(tri,D[case])
            receiver_bounds.append(bounds)
            receivers.append({'case':case,'maximum_physical_area_squared':str(maximum),
                'complete_area_strata':strata,'strict_source_area_upper':str(T),
                'receiver_chord_upper':str(D[case]),'original_support_geometry':original,
                'receiver_vertex_and_side_comparisons':1984,'signed_receiver_bounds':records})
        combined=[max(receiver_bounds[0][i],receiver_bounds[1][i]) for i in range(16)]
        assert all(combined[i]>=r[i] for r in receiver_bounds for i in range(16))
        critical=source.certify(T,A)
        assert critical['counts']=={'generated':212,'corner':40,'sphere_stationary':24,
            'area_stationary':18,'edge_stationary':80,'area_edge_intersection':50,'feasible':65}
        assert critical['minimum_occurrences']==[[11,'area_edge_intersection',0]]
        raw=critical['sharp_minimum_witness']['objective']
        f=source.Rad(C.parse(raw['a']),C.parse(raw['b']),C.parse(raw['radicand']))
        assert (f*f-Q((1-A_MINUS*A_MINUS/2)**2)*M2).sign()<0
        assert A_MINUS>F(1,5)
        model=SourceBands(combined)
        all_polygons,outer=model.source_polygons()
        polygons={fold:model.tighten(poly,fold,cell) for fold,cell,poly in all_polygons if cell==11}
        assert set(polygons)==set((0,1)) and all(polygons.values())
        factors={fold:model.factors(poly) for fold,poly in polygons.items()}
        assert all(v is not None for v in factors.values())
        assert norm_extrema(polygons[0])==norm_extrema(polygons[1])
        records=[];negative=0
        for sign,index,fold,pi,wi in rows:
            lo,hi=F(index,8),F(index+1,8)
            okay,record=model.witness(polygons[fold],lo,hi,pi,wi,sign)
            assert okay
            margins=[C.parse(v) for v in record['strict_endpoint_margins']]
            assert all((v-Q(F(1,100000))).sign()>0 for v in margins)
            if C.parse(record['source_loss_numerator_upper']).sign()<0:negative+=1
            records.append({'sign':sign,'bin':index,'fold':fold,
                'closed_interval':list(map(str,(lo,hi))),**record})
        assert len(records)==32
        polygon_records=[{'fold':fold,'polygon_corners':[list(map(str,xy)) for xy in poly],
            'local_factors':list(map(str,factors[fold]))} for fold,poly in sorted(polygons.items())]
    result={'pins':checked_pins,'receiver_geometry':geometric,'receivers':receivers,
        'global_source_critical_strata':critical,'sharp_global_source_chord_window':[str(A_MINUS),str(A)],
        'false_area_only_one_fifth_cap':True,'combined_receiver_bounds':list(map(str,combined)),
        'source_outer_geometry':outer,'cell11_root_polygon_records':polygon_records,
        'original_vertex_height_patches':32,'strict_endpoint_comparisons':64,
        'strict_endpoint_lower':'1/100000','fixed_roll_bins_per_sign':8,'source_subdivisions':0,
        'negative_signed_loss_upper_bounds_retained':negative,
        'height_record_sha256':hashlib.sha256(json.dumps(records,separators=(',',':')).encode()).hexdigest(),
        'norm_extrema_regressions':nr,'malformed_controls_rejected':controls(rows),
        'Q5_sign_audits':qa,'radical_sign_audits':ra}
    if captures is not None:
        captures.update(height_records=records,source_polygons=polygon_records,receivers=receivers,
            critical_strata=critical,elapsed_seconds=time.monotonic()-start)
    return result

def main():
    start=time.monotonic();actual=compute(TABLE)
    assert actual==PAYLOAD['expected'],'fresh exact fields do not match compact fixture'
    print(json.dumps({'agent':'six-rupert-1','role':'researcher',
        'claim':'Cell11 source orbit cannot pass into the closed original 1/3 receiver collar',
        'whole_1_3_receiver_exclusion':'OPEN','global_Rupert_property':'OPEN',
        'all_expected_fields_match':True,'original_vertex_height_patches':32,
        'strict_endpoint_comparisons':64,'malformed_controls_rejected':actual['malformed_controls_rejected'],
        'pinned_dependency_count':len(actual['pins']),'Q5_sign_audits':actual['Q5_sign_audits'],
        'radical_sign_audits':actual['radical_sign_audits'],
        'elapsed_seconds':time.monotonic()-start,
        'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))

if __name__=='__main__':main()
