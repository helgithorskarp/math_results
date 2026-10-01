"""Exact fixed hypotheses for the ENTIRE closed 1/4 Cell8 collar.

Python3.11 stdlib. See cell8_quarter_proof.md for the universal argument.
Both original receiving triangles and every source branch are covered.
No discovery search, floating predicates, or inherited guard changes.
"""
from pathlib import Path
from fractions import Fraction as F
import copy,hashlib,itertools,json,time,resource
if not __debug__:raise RuntimeError('verification requires assertions; do not use python -O')
import cell8_fifth_certificate as fifth
C=fifth.C;H=C.H;Q=H.Q5;ZERO=H.ZERO;M=C.M;M2=C.M2
parent=fifth.parent;source=fifth.source;ROOT=Path(__file__).parent
B1=fifth.B1;B2=fifth.B2;MIRROR=fifth.MIRROR
clip=fifth.clip;tangent=fifth.tangent;linear=fifth.linear;split=fifth.split
mv=fifth.mv;project=fifth.project
R=F(1,8);T=[F(3707533,250000),F(14830423,1000000)]
A=[F(14141,125000),F(113349,1000000)]
D=[F(15227,200000),F(21027,200000)]
TIP=H.add(H.mul(F(3,4),parent.nine.W),H.mul(F(1,4),parent.U))
TRIANGLES=[[C.N[8],parent.nine.W,TIP],[parent.nine.W,C.N[10],TIP]]
FULL=[C.N[8],C.N[10],TIP]
HEIGHT_INTERVALS=[[[1,'151/160','311/320'],[1,'311/320','1']],[]]
PINS={'cell8_fifth_certificate.py':'2692b0d500794e8901fc72f1b0b9bd52772c0bf7a29cc8b89b9cdd9549100dcc',
      'expected_cell8_fifth.json':'e61abcdd15e9229362588bcab15e2bb07a93ce1bbc6a3857bbcd3c1594ba21c1'}

def pins():
    out=fifth.pins()
    for name,wanted in PINS.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==wanted
    assert parent.R==R and parent.MAX_DEPTH==4 and fifth.SOURCE_DEPTH==1
    assert parent.local.R==F(27,250) and parent.local.MAX_DEPTH==3
    return {**out,**PINS}

def fixture():return json.loads((ROOT/'expected_cell8_quarter.json').read_text())

def receiver_bounds(tri,d):
    envelopes=C.linear_envelopes(tri)
    norms=[C.root_upper(H.dot(project(v,M),project(v,M))) for v in C.V]
    bounds=[]; records=[]; count=0
    for pi,p in enumerate(C.PROBES):
        values=[]
        for j,v in enumerate(C.V):
            gamma=H.dot(p['mu'],v); correction=p['norm_upper']*norms[j]-gamma
            assert correction.sign()>=0
            for side,xi in enumerate((envelopes[pi]['lo'],envelopes[pi]['hi'])):
                values.append((-H.dot(M,v)*xi-(p['H']-gamma)+d*d*correction/4,j,side));count+=1
        bound=max(ZERO,*(z for z,_,_ in values));bounds.append(bound)
        records.append({'probe':pi,'receiver_excess_upper':str(bound),
            'active_vertices_and_sides':[[j,s] for z,j,s in values if z==bound],
            'corner_ratio_lower':str(envelopes[pi]['lo']),'corner_ratio_upper':str(envelopes[pi]['hi'])})
    assert count==1984
    return bounds,records

class Enclosure:
    def __init__(self,a,t,bounds):
        assert 0<a<F(1,4) and t>0 and len(bounds)==16
        self.a=a; self.t=t; self.bounds=tuple(bounds)
        self.cos=1-a*a/2; self.cap2=M2*(1/self.cos**2-1)
        self.l_lo=Q(self.cos)/M2; self.l_hi=1/M2
        self.b_lo=Q(self.cos**2/(1+self.cos))/M2; self.b_hi=1/(2*M2)
        self.l_mid=(self.l_lo+self.l_hi)/2; self.l_err=(self.l_hi-self.l_lo)/2
        self.b_mid=(self.b_lo+self.b_hi)/2; self.b_err=(self.b_hi-self.b_lo)/2
        self.rnorm=C.root_upper(self.cap2)
        assert self.l_lo.sign()>0 and self.b_lo.sign()>0
        assert self.l_err.sign()>0 and self.b_err.sign()>0
        self.cache={}

    def source_polygons(self):
        g11,g12,g22=H.dot(B1,B1),H.dot(B1,B2),H.dot(B2,B2)
        det=g11*g22-g12*g12;assert det.sign()>0
        bx=C.root_upper(self.cap2*g22/det);by=C.root_upper(self.cap2*g11/det)
        base=[(Q(-bx),Q(-by)),(Q(bx),Q(-by)),(Q(bx),Q(by)),(Q(-bx),Q(by))]
        cuts=[]
        for x,y in [(1,0),(0,1),(1,1),(1,-1),(2,1),(2,-1),(1,2),(1,-2)]:
            d=H.add(H.mul(x,B1),H.mul(y,B2)); assert H.dot(d,M)==ZERO
            bound=C.root_upper(self.cap2*H.dot(d,d))
            for sg in (-1,1):cuts.append((Q(bound),sg*H.dot(d,B1),sg*H.dot(d,B2)))
        for row in cuts:base=clip(base,row)
        assert len(base)>=3
        def coordinates(w):
            h1,h2=H.dot(w,B1),H.dot(w,B2)
            return ((g22*h1-g12*h2)/det,(g11*h2-g12*h1)/det)
        records=[]
        for row in C.P['cell_certificates']:
            corners=[C.N[j] for j in row['corner_indices']]
            sides=[H.cross(u,corners[(i+1)%len(corners)]) for i,u in enumerate(corners)]
            poly=base[:]
            for e in sides:poly=clip(poly,linear(e))
            av=H.vec(map(C.parse,row['area_vector'])); ar=linear(av)
            bound=Q(self.t*fifth.MH/self.cos)
            poly=clip(poly,(bound-ar[0],-ar[1],-ar[2]))
            records.append((0,row['cell'],poly))
            reflected=[coordinates(mv(MIRROR,tangent(xy))) for xy in poly]
            assert all(tangent(xy)==mv(MIRROR,tangent(old)) for xy,old in zip(reflected,poly))
            records.append((1,row['cell'],reflected))
        return records,{'coordinate_bounds':[str(bx),str(by)],'linear_chord_cuts':len(cuts),
            'base_polygon_corners':len(base),'source_area_linear_upper':str(self.t*fifth.MH/self.cos)}

    def tighten(self,poly,fold,cell):
        av=H.vec(map(C.parse,C.P['cell_certificates'][cell]['area_vector']))
        if fold:av=mv(MIRROR,av)
        ar=linear(av)
        for _ in range(2):
            if not poly:break
            maximum=max(H.dot(tangent(xy),tangent(xy)) for xy in poly)
            norm=C.root_upper(M2+min(maximum,self.cap2)); bound=Q(self.t*norm)
            poly=clip(poly,(bound-ar[0],-ar[1],-ar[2]))
        return poly

    def rank_affine_max(self,poly,p,v):
        if not poly:return ZERO
        h=H.dot(M,p); w=[tangent(xy) for xy in poly]
        vals=[(self.l_mid*h+self.b_mid*H.dot(p,a))*H.dot(v,a) for a in w]
        for a,b in zip(w,w[1:]+w[:1]):
            d=H.sub(b,a);pa=self.l_mid*h+self.b_mid*H.dot(p,a);pd=self.b_mid*H.dot(p,d)
            va,vd=H.dot(v,a),H.dot(v,d);aa=pd*vd;bb=pa*vd+pd*va;cc=pa*va
            if aa.sign()<0:
                t=-bb/(2*aa)
                if t.sign()>=0 and (1-t).sign()>=0:vals.append(cc-bb*bb/(4*aa))
        return max(vals)

    def parameters(self,lo,hi,pi,wi,sign):
        key=(lo,hi,pi,wi,sign)
        if key in self.cache:return self.cache[key]
        p=C.POINTS[wi][0];probe=C.PROBES[pi];mu=probe['mu'];z=H.cross(M,mu)
        assert H.dot(mu,M)==H.dot(z,M)==ZERO
        h=H.dot(M,p);h=h if h.sign()>=0 else -h
        pp=project(p,M);rp=C.root_upper(H.dot(pp,pp));rz=C.root_upper(H.dot(z,z));eta=probe['norm_upper']
        error=self.l_err*h*(1+hi*hi)*eta*self.rnorm+self.b_err*rp*(1+hi*hi)*eta*self.cap2
        error+=(self.l_hi*h+self.b_hi*rp*self.rnorm)*Q(2*hi*fifth.IE*rz*self.rnorm)
        assert error.sign()>=0
        vectors=[H.sub(H.mul(1-lo*lo,mu),H.mul(2*sign*lo*fifth.IM,z)),
            H.sub(H.mul(1-lo*hi,mu),H.mul(sign*(lo+hi)*fifth.IM,z)),
            H.sub(H.mul(1-hi*hi,mu),H.mul(2*sign*hi*fifth.IM,z))]
        gamma=C.DATA[pi][wi]['d'];tau=C.DATA[pi][wi]['tau'][sign]
        coef=(gamma-probe['H']-self.bounds[pi],Q(2*tau),-gamma-probe['H']-self.bounds[pi])
        assert coef[2].sign()<=0
        self.cache[key]=(p,vectors,error,coef)
        return self.cache[key]

    def witness(self,poly,lo,hi,pi,wi,sign):
        p,vectors,error,coef=self.parameters(lo,hi,pi,wi,sign)
        upper=max(self.rank_affine_max(poly,p,v) for v in vectors)+error
        margins=[coef[0]+coef[1]*x+coef[2]*x*x-upper for x in (lo,hi)]
        return all(x.sign()>0 for x in margins),{'probe':pi,'point':wi,
            'source_loss_numerator_upper':str(upper),'strict_endpoint_margins':list(map(str,margins))}


def closed_roll_cover(case,rows):
    assert type(case) is int and case in (0,1) and isinstance(rows,list) and rows
    for row in rows:
        assert isinstance(row,list) and len(row)==5
        sign,lo,hi,pi,wi=row
        assert type(sign) is int and sign in (-1,1) and F(1,10)<=F(lo)<F(hi)<=1
        assert type(pi) is int and 0<=pi<16 and type(wi) is int and 0<=wi<74
    for sign in (-1,1):
        intervals=[(F(lo),F(hi)) for s,lo,hi,_,_ in rows if s==sign]
        intervals += [(F(lo),F(hi)) for s,lo,hi in HEIGHT_INTERVALS[case] if s==sign]
        intervals.sort();assert intervals and intervals[0][0]==F(1,10) and intervals[-1][1]==1
        assert all(a[1]==b[0] for a,b in zip(intervals,intervals[1:]))

def closed_piece(case,piece):
    assert isinstance(piece,dict) and set(piece)=={'roll','source_covers','axes'}
    closed_roll_cover(case,piece['roll']);parent.closed_covers(piece['axes'])
    assert isinstance(piece['source_covers'],list) and len(piece['source_covers'])==len(HEIGHT_INTERVALS[case])
    for records in piece['source_covers']:fifth.closed_source_cover(records)

def replay_source(enclosure,records,interval):
    fifth.closed_source_cover(records)
    sign,slo,shi=interval;lo,hi=F(slo),F(shi)
    polygons,geometry=enclosure.source_polygons()
    roots={(fold,cell):enclosure.tighten(poly,fold,cell) for fold,cell,poly in polygons}
    digest=hashlib.sha256();empty=0;positive=0;negative=0;summaries=[]
    for fold,cell,path,pi,wi in records:
        poly=roots[fold,cell]
        for child in path:
            pieces=split(poly);assert len(pieces)==2
            poly=enclosure.tighten(pieces[int(child)],fold,cell)
        if pi==-1:
            assert not poly;empty+=1
            record={'fold':fold,'cell':cell,'path':path,'empty':True}
        else:
            assert poly
            okay,data=enclosure.witness(poly,lo,hi,pi,wi,sign);assert okay
            margins=list(map(C.parse,data['strict_endpoint_margins']))
            assert all(x>Q(F(1,100000)) for x in margins)
            positive+=len(margins)
            if C.parse(data['source_loss_numerator_upper']).sign()<0:negative+=1
            record={'fold':fold,'cell':cell,'path':path,'empty':False,
                'polygon_corners':[list(map(str,a)) for a in poly],**data}
        digest.update(json.dumps(record,sort_keys=True,separators=(',',':')).encode())
        summaries.append({k:v for k,v in record.items() if k not in
            ('polygon_corners','strict_endpoint_margins','source_loss_numerator_upper')})
    return {'source_chamber_copies':2,'closed_fan_cells_per_copy':12,
        'closed_interval':[slo,shi],'sign':sign,'geometry':geometry,
        'factor_midpoints':list(map(str,(enclosure.l_mid,enclosure.b_mid))),
        'factor_halfwidths':list(map(str,(enclosure.l_err,enclosure.b_err))),
        'source_tangent_norm_squared_upper':str(enclosure.cap2),'tangent_norm_upper':str(enclosure.rnorm),
        'minimum_axis_length_enclosure':list(map(str,(fifth.ML,fifth.MH))),
        'inverse_length_midpoint':str(fifth.IM),'inverse_length_error':str(fifth.IE),
        'fixed_source_depth':1,'closed_leaves':len(records),'empty_leaves':empty,
        'strict_support_leaves':len(records)-empty,'strict_endpoint_margins':positive,
        'every_endpoint_margin_greater_than':'1/100000','uniform_negative_height_gains':negative,
        'entrywise_polygon_and_support_sha256':digest.hexdigest(),'witnesses':summaries}

def phase(case,rows,bounds):
    closed_roll_cover(case,rows)
    a,d=A[case],D[case];c=1-a*a/4
    norms=[C.root_upper(H.dot(project(p,M),project(p,M))) for p,_ in C.POINTS]
    def coefficients(sign,pi,wi):
        p,row=C.PROBES[pi],C.DATA[pi][wi]
        error=p['norm_upper']*row['source_height_upper']*a+a*a*p['norm_upper']*norms[wi]/4+bounds[pi]
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
    product=(1-a*a/4)*(1-d*d/4)*(1-roll*roll/4);X2=(a+d)**2+roll*roll
    assert product>F(99,100)**2 and F(99,100)-a*d/4>0 and X2<=F(1,9)
    beta=next(F(j,1000) for j in range(1001,1020) if F(j,1000)**2*(1-X2/4)>1)
    theta=C.grid_upper(lambda x:Q(x*x)>Q(beta*beta*X2),F(1,3))
    gate=R*(1-theta*theta/8)-theta/2;assert gate>0
    return {'near_zero_gates':gates,'standard_closed_roll_intervals':intervals,
        'standard_interval_count':len(rows),'height_aware_interval_count':len(HEIGHT_INTERVALS[case]),
        'roll_chord_upper':str(roll),'full_spatial_angle_upper':str(theta),
        'composition_squared_upper':str(X2),'angle_derivative_beta':str(beta),
        'quaternion_product_margin':str(product-F(99,100)**2),
        'angle_derivative_margin':str(beta*beta*(1-X2/4)-1),
        'angle_to_cayley_radius1_8_gate':str(gate)}

def geometry():
    assert C.P['cell_certificates'][8]['corner_indices']==[6,11,10,8]
    edges=[H.cross(u,parent.QUAD[(i+1)%4]) for i,u in enumerate(parent.QUAD)]
    assert all(H.dot(e,u).sign()>=0 for e in edges for u in FULL)
    assert all(H.dot(e,TIP).sign()>0 for e in edges)
    ratio=Q(F(17,57),F(4,57));assert ratio.sign()>0 and (1-ratio).sign()>0
    assert parent.nine.W==H.add(H.mul(1-ratio,C.N[8]),H.mul(ratio,C.N[10]))
    assert C.area_twice(FULL)==sum((C.area_twice(tri) for tri in TRIANGLES),ZERO)
    assert fifth.parent.LARGE==[C.N[8],C.N[10],fifth.TRI[2]]
    assert all(C.weak_inside(u,FULL) for u in parent.LARGE)
    sep=C.parse(parent.fixture()['expected']['receiver_geometry']['moving_halfturn_separation_squared_at_m'])
    assert sep>Q(8*max(D)**2)
    newpoint=H.mul(F(1,11),H.add(H.add(TRIANGLES[0][0],TRIANGLES[0][1]),H.mul(9,TIP)))
    assert C.weak_inside(newpoint,TRIANGLES[0]) and not C.weak_inside(newpoint,parent.LARGE)
    ray=lambda j,t:H.add(M,H.mul(t,H.sub(C.N[j],M)))
    old=[[M,ray(3,F(1,8)),ray(4,F(1,4))],[M,ray(4,F(1,4)),C.N[7]],
        [M,C.N[7],C.N[8]],[M,C.N[8],ray(10,F(1,6))]]
    old += [C.triangle(t) for t in (F(2,5),F(1,2),F(2,3),F(3,4),F(1))]
    old += [parent.nine.FULL]+parent.TRIANGLES+[fifth.TRI]
    images=C.orbit(newpoint);assert len(images)==60 and len(old)==13
    for u in images:
        for a,b,c in old:
            det=C.determinant(a,b,c);assert det.sign()!=0
            coordinates=[C.determinant(u,b,c)/det,C.determinant(a,u,c)/det,C.determinant(a,b,u)/det]
            assert not(all(x.sign()>=0 for x in coordinates) or all(x.sign()<=0 for x in coordinates))
    cosine=1-F(1,50)**2/2;centers=C.orbit(M);assert len(centers)==30
    for u in centers:assert Q(cosine*cosine)*H.dot(newpoint,newpoint)*H.dot(u,u)>H.dot(newpoint,u)**2
    return {'entire_closed_collar_parameter':'1/4','original_cell8_corners':[6,11,10,8],
        'closed_receiver_triangles':[[list(map(str,u)) for u in tri] for tri in TRIANGLES],
        'whole_collar':[list(map(str,u)) for u in FULL],
        'whole_old1_5_collar_retained':True,'second1_4_triangle_freshly_proved':True,
        'moving_halfturn_separation_squared_at_m':str(sep),
        'moving_halfturn_separation_margin':str(sep-Q(8*max(D)**2)),
        'strict_new_receiving_witness':list(map(str,newpoint)),
        'proper_projective_witness_images':60,'prior_cones_per_image':13,
        'exact_prior_cone_tests':780,'witness_images_in_prior_cones':0,
        'minimum_projective_axes':30,'new_witness_chord_lower':'1/50 > 1/64'}

def identities():
    inherited=fifth.identity_audits();count=0
    for sign,slo,shi in HEIGHT_INTERVALS[0]:
        lo,hi=F(slo),F(shi)
        for s in (F(0),F(1),F(1,3)):
            x=lo+(hi-lo)*s
            for mu in (C.PROBES[3]['mu'],C.PROBES[4]['mu']):
                z=H.cross(M,mu)
                vectors=[H.sub(H.mul(1-lo*lo,mu),H.mul(2*sign*lo*fifth.IM,z)),
                    H.sub(H.mul(1-lo*hi,mu),H.mul(sign*(lo+hi)*fifth.IM,z)),
                    H.sub(H.mul(1-hi*hi,mu),H.mul(2*sign*hi*fifth.IM,z))]
                actual=H.sub(H.mul(1-x*x,mu),H.mul(2*sign*x*fifth.IM,z))
                expected=H.add(H.add(H.mul((1-s)**2,vectors[0]),H.mul(2*s*(1-s),vectors[1])),H.mul(s*s,vectors[2]))
                assert actual==expected;count+=3
    enclosure=Enclosure(A[0],T[0],[ZERO]*16)
    assert enclosure.rank_affine_max([H.vec((F(1,10),0))],M,H.mul(-1,B1)).sign()<0
    return {'inherited_universal_identity_regressions':inherited,
        'new_roll_Bernstein_component_identities':count,'new_budget_negative_gain_retained':True}

def controls(pieces):
    rejected=[]
    def reject(name,job):
        try:job()
        except (AssertionError,ValueError):rejected.append(name)
        else:raise AssertionError('malformed evidence accepted: '+name)
    for case,piece in enumerate(pieces):
        rows=piece['roll']
        reject(f'case{case} missing signed roll half',lambda:closed_roll_cover(case,[r for r in rows if r[0]==1]))
        reject(f'case{case} missing roll interval',lambda:closed_roll_cover(case,rows[:-1]))
        reject(f'case{case} duplicate roll interval',lambda:closed_roll_cover(case,rows+[rows[-1]]))
        bad=copy.deepcopy(rows);bad[0][1]='1/9'
        reject(f'case{case} gapped endpoint',lambda:closed_roll_cover(case,bad))
        bad=copy.deepcopy(rows);bad[0][4]=74
        reject(f'case{case} unknown source point',lambda:closed_roll_cover(case,bad))
    bad=copy.deepcopy(pieces[0]);bad['source_covers'].pop()
    reject('missing height interval cover',lambda:closed_piece(0,bad))
    bad=copy.deepcopy(pieces[1]);bad['source_covers']=[pieces[0]['source_covers'][0]]
    reject('unsupported case1 height cover',lambda:closed_piece(1,bad))
    records=pieces[0]['source_covers'][0]
    reject('missing reflected source chamber',lambda:fifth.closed_source_cover([r for r in records if r[0]==0]))
    reject('missing closed source fan cell',lambda:fifth.closed_source_cover([r for r in records if r[1]!=8]))
    reject('missing source leaf',lambda:fifth.closed_source_cover(records[:-1]))
    reject('duplicate source leaf',lambda:fifth.closed_source_cover(records+[records[-1]]))
    bad=copy.deepcopy(records);bad[0][2]='2'
    reject('invalid source path',lambda:fifth.closed_source_cover(bad))
    bad=copy.deepcopy(records);bad[0][4]=74
    reject('false empty source witness',lambda:fifth.closed_source_cover(bad))
    root=next(r for r in records if r[2]);bad=records+[root[:2]+['',3,57]]
    reject('overlapping source ancestor',lambda:fifth.closed_source_cover(bad))
    axes=pieces[0]['axes']
    reject('missing signed cube face',lambda:parent.closed_covers(axes[:-1]))
    bad=copy.deepcopy(axes);bad[0]['leaves'].pop()
    reject('missing cube leaf',lambda:parent.closed_covers(bad))
    bad=copy.deepcopy(axes);bad[0]['leaves'].append(bad[0]['leaves'][0])
    reject('duplicate cube leaf',lambda:parent.closed_covers(bad))
    bad=copy.deepcopy(axes);bad[0]['leaves'][0][1]=20
    reject('unknown original contact',lambda:parent.closed_covers(bad))
    bad=copy.deepcopy(axes);bad[0]['leaves'][0][2]='2'
    reject('false cube norm lower',lambda:parent.closed_covers(bad))
    reject('wrong mixed Bernstein coefficient',lambda:parent.local.bernstein_identity_audits(F(1,2)))
    bad=copy.deepcopy(C.P);bad['cell_certificates'].pop()
    reject('missing global physical-area cell',lambda:source.structure(bad))
    return rejected

def check(pieces):
    checked=pins();assert isinstance(pieces,list) and len(pieces)==2
    for case,piece in enumerate(pieces):closed_piece(case,piece)
    with C.audit_signs() as qa,source.audit_radicals() as ra:
        geom=geometry();nearest=source.nearest_axis()
        probes,points,data=C.reference.reference();assert (probes,points,data)==(C.PROBES,C.POINTS,C.DATA)
        output=[]
        for case,(tri,piece) in enumerate(zip(TRIANGLES,pieces)):
            q,area=C.area_maximum(parent.VECTOR,tri);assert C.root_upper(q)==T[case] and Q(T[case]**2)>q
            assert all(C.chord_less(u,D[case]) for u in tri)
            sharp=source.certify(T[case],A[case])
            lo,hi=map(F,sharp['sharp_minimum_witness']['chord_rational_enclosure'])
            assert A[case]-F(1,10**6)<lo<hi<A[case]
            bounds,receiver=receiver_bounds(tri,D[case]);enclosure=Enclosure(A[case],T[case],bounds)
            covers=[replay_source(enclosure,records,interval) for records,interval in
                zip(piece['source_covers'],HEIGHT_INTERVALS[case])]
            ph=phase(case,piece['roll'],bounds)
            contacts,support=parent.supports(tri);faces=parent.replay(contacts,piece['axes'])
            output.append({'case':case,'receiver_triangle':[list(map(str,u)) for u in tri],
                'maximum_receiving_area_squared':str(q),'maximum_area_strata':area,
                'source_area_upper':str(T[case]),'source_chord_upper':str(A[case]),'receiver_chord_upper':str(D[case]),
                'fresh_source_critical_strata':sharp,'whole_receiver_support_envelopes':receiver,
                'receiver_vertex_side_comparisons':1984,'new_height_aware_source_covers':covers,
                'full_signed_roll_phase':ph,'original_support_and_Cayley_audits':support,
                'signed_axis_faces':faces,'Cayley_radius':str(R),
                'closed_axis_leaves':sum(f['closed_leaves'] for f in faces),
                'strict_axis_coefficients':sum(f['strict_positive_coefficients'] for f in faces),
                'fixed_piece_sha256':H.digest(piece)})
        regression=identities();basis=parent.local.bernstein_identity_audits();rejected=controls(pieces)
    return {'agent':'six-rupert-1','role':'researcher','global_Rupert_property':'OPEN',
        'status':'complete exact finite hypotheses for ENTIRE closed1/4 collar; written continuum proof separate',
        'pins':checked,'entire_closed_collar_parameter':'1/4','receiver_geometry':geom,
        'both_receiver_triangles_freshly_proved':True,'entire_cell8_claimed':False,
        'global_nearest_minimum_axis':nearest,'reference_facets':16,'reference_original_supports':992,
        'actual_original_source_points':74,'pieces':output,'algebra_and_degeneracy_audits':regression,
        'tensor_Bernstein_basis_identities':basis,
        'closed_axis_leaves':sum(p['closed_axis_leaves'] for p in output),
        'strict_axis_coefficients':sum(p['strict_axis_coefficients'] for p in output),
        'fixed_pieces_sha256':H.digest(pieces),'independent_Q5_sign_audits':qa,
        'independent_radical_sign_audits':ra,
        'sign_audit_scope':'main verification phase; imported pinned constructors remain inherited prerequisites',
        'malformed_controls_rejected':rejected}

if __name__=='__main__':
    started=time.monotonic();saved=fixture();assert set(saved)=={'pieces','expected'}
    actual=check(saved['pieces'])
    assert json.loads(json.dumps(actual))==saved['expected'],'every expected mathematical field must match'
    print(json.dumps({'all_expected_fields_match':True,'global_Rupert_property':'OPEN',
        'entire_closed_collar_parameter':'1/4','source_candidates':[p['fresh_source_critical_strata']['counts']['generated'] for p in actual['pieces']],
        'source_feasible_candidates':[p['fresh_source_critical_strata']['counts']['feasible'] for p in actual['pieces']],
        'closed_axis_leaves':actual['closed_axis_leaves'],'strict_axis_coefficients':actual['strict_axis_coefficients'],
        'full_spatial_angle_uppers':[p['full_signed_roll_phase']['full_spatial_angle_upper'] for p in actual['pieces']],
        'malformed_controls_rejected':len(actual['malformed_controls_rejected']),
        'elapsed_seconds':time.monotonic()-started,
        'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))
