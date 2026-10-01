"""Fixed exact certificate for the entire deltoidal receiving area cell9.

Python3.11+ standard library. See cell9_coupled_proof.md for the continuous
all-original-source argument. No search or floating proof decisions occur here.
"""
from pathlib import Path
from fractions import Fraction as F
import copy,hashlib,itertools,json,time,resource
if not __debug__:raise RuntimeError('verification requires assertions; do not use python -O')
import cayley_wedge_certificate as local
import rank_transport_wedge_certificate as C
import source_extrema_certificate as source
from verify import project
H=C.H;Q=H.Q5;ZERO=H.ZERO;ROOT=Path(__file__).parent;V=C.V
FULL=[C.N[j] for j in C.P['cell_certificates'][9]['corner_indices']]
W=C.triangle(F(1))[1];LEFT=[C.M,C.N[8],W]
T=F(739431,50000);A=F(85407,1000000);D=F(14389,250000)
R=F(27,250);THETA=F(212461,1000000);CONTACT_IDS=list(range(12));MAX_DEPTH=3
PINS={
 'cayley_wedge_certificate.py':'962dafc0ffabed4b838bc5613d7ed36862276f1c751cfca99dabbc3718e0ba75',
 'expected_cayley_wedge.json':'b20aa67068e284befe86876222bf26861e48ee753746417ed094f116622ba31f',
}

def pins():
    checked=local.pins()
    for name,wanted in PINS.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==wanted
    assert local.R==R and local.MAX_DEPTH==MAX_DEPTH
    return {**checked,**PINS}

def fixture():return json.loads((ROOT/'expected_cell9_coupled.json').read_text())

def closed_roll_cover(rows):
    assert isinstance(rows,list) and rows
    assert rows==sorted(rows,key=lambda r:(r[0],F(r[1])))
    assert {r[0] for r in rows}=={-1,1}
    for sign in (-1,1):
        selected=[r for r in rows if r[0]==sign]
        assert F(selected[0][1])==F(1,10) and F(selected[-1][2])==1
        for r in selected:
            assert len(r)==5 and F(r[1])<F(r[2])
            assert isinstance(r[3],int) and 0<=r[3]<16
            assert isinstance(r[4],int) and 0<=r[4]<74
        assert all(F(a[2])==F(b[1]) for a,b in zip(selected,selected[1:]))

def phase(rows):
    closed_roll_cover(rows)
    probes,points,data=C.reference.reference()
    assert (probes,points,data)==(C.PROBES,C.POINTS,C.DATA)
    vector=H.vec(map(C.parse,C.P['cell_certificates'][9]['area_vector']))
    q,area=C.area_maximum(vector,LEFT)
    assert q==Q(F(4886285,44649),F(2181775,44649)) and Q(T*T)>q
    assert C.root_upper(q)==T and 0<A<F(1,5) and 0<D<F(1,4)
    assert all(C.chord_less(u,D) for u in LEFT)
    envelopes=C.linear_envelopes(LEFT)
    vertex_perp=[C.root_upper(H.dot(project(v,C.M),project(v,C.M))) for v in V]
    point_perp=[C.root_upper(H.dot(project(p,C.M),project(p,C.M))) for p,_ in points]
    receiver=[];records=[];comparisons=0
    for pi,p in enumerate(probes):
        values=[]
        for j,v in enumerate(V):
            gamma=H.dot(p['mu'],v);correction=p['norm_upper']*vertex_perp[j]-gamma
            assert correction.sign()>=0
            for side,xi in enumerate((envelopes[pi]['lo'],envelopes[pi]['hi'])):
                z=-H.dot(C.M,v)*xi-(p['H']-gamma)+D*D*correction/4
                values.append((z,j,side));comparisons+=1
        bound=max(ZERO,*(v for v,_,_ in values));receiver.append(bound)
        records.append({'probe':pi,'receiver_excess_upper':str(bound),
            'active_vertices_and_sides':[[j,s] for v,j,s in values if v==bound],
            'corner_ratio_lower':str(envelopes[pi]['lo']),'corner_ratio_upper':str(envelopes[pi]['hi'])})
    c=1-A*A/4;assert c>0
    def coefficients(sign,pi,wi):
        p,row=probes[pi],data[pi][wi]
        error=p['norm_upper']*row['source_height_upper']*A+A*A*p['norm_upper']*point_perp[wi]/4+receiver[pi]
        result=(c*row['d']-p['H']-error,Q(2*c*row['tau'][sign]),-c*row['d']-p['H']-error)
        assert result[2].sign()<0
        return result
    def value(coef,x):return coef[0]+coef[1]*x+coef[2]*x*x
    gates=[]
    for sign,pi in ((-1,3),(1,4)):
        p,row=probes[pi],data[pi][45]
        assert H.dot(C.M,V[45])==ZERO and row['d']==p['H'] and row['tau'][sign]>0
        coef=coefficients(sign,pi,45);quadratic=lambda x:-value(coef,x)
        assert quadratic(F(0)).sign()>0 and quadratic(F(1,10)).sign()<0
        xu=C.grid_upper(lambda x:quadratic(x).sign()<0,F(1,10))
        assert quadratic(xu).sign()<0 and quadratic(xu-F(1,10**6)).sign()>=0
        gates.append({'sign':sign,'probe':pi,'point':45,'coefficients':list(map(str,coef)),
            'q_zero':str(quadratic(F(0))),'q_b':str(quadratic(F(1,10))),
            'small_root_upper':str(xu),'q_upper':str(quadratic(xu)),
            'q_predecessor':str(quadratic(xu-F(1,10**6))),'roll_chord_upper':str(2*xu)})
    remote=[]
    for sign,lo,hi,pi,wi in rows:
        coef=coefficients(sign,pi,wi);margins=[value(coef,F(x)) for x in (lo,hi)]
        assert all(m.sign()>0 for m in margins)
        remote.append({'sign':sign,'interval':[lo,hi],'probe':pi,'point':wi,
            'original_source_point_certificate':points[wi][1],
            'coefficients':list(map(str,coef)),'strict_endpoint_margins':list(map(str,margins))})
    r=max(F(g['roll_chord_upper']) for g in gates)
    product=(1-A*A/4)*(1-D*D/4)*(1-r*r/4);X2=(A+D)**2+r*r
    beta=F(1003,1000)
    assert product>F(99,100)**2 and F(99,100)-A*D/4>0 and X2<=F(1,9)
    assert beta*beta*(1-X2/4)>1
    theta=C.grid_upper(lambda x:Q(x*x)>Q(beta*beta*X2),F(1,3))
    assert theta==F(150811,10**6)<THETA
    gate=R*(1-theta*theta/8)-theta/2;assert gate>0
    return {'physical_area_maximum_squared':str(q),'physical_area_maximum':area,
        'strict_source_area_upper':str(T),'source_chord_upper':str(A),'receiver_chord_upper':str(D),
        'original_reference_facets':16,'original_facet_support_comparisons':992,
        'actual_convex_source_points':74,'receiver_vertex_and_side_comparisons':comparisons,
        'perpendicular_norm_bounds_sha256':H.digest([list(map(str,vertex_perp)),list(map(str,point_perp))]),
        'rank_receiver_envelopes':records,'near_zero_gates':gates,'closed_remote_intervals':remote,
        'remote_interval_count':len(remote),'remote_intervals_per_sign':[sum(r[0]==s for r in rows) for s in (-1,1)],
        'roll_chord_upper':str(r),'composition_squared_upper':str(X2),
        'quaternion_product_margin':str(product-F(99,100)**2),
        'angle_derivative_beta':str(beta),'angle_derivative_margin':str(beta*beta*(1-X2/4)-1),
        'full_angle_upper':str(theta),'angle_to_radius27_250_gate':str(gate)}

def geometry():
    assert C.P['cell_certificates'][9]['corner_indices']==[10,9,8]
    ratio=Q(F(17,57),F(4,57));assert ratio.sign()>0 and (1-ratio).sign()>0
    assert W==H.add(H.mul(1-ratio,C.N[8]),H.mul(ratio,C.N[10]))
    old=C.triangle(F(1))
    assert all(C.weak_inside(u,FULL) for u in LEFT+old)
    assert C.area_twice(FULL)==C.area_twice(LEFT)+C.area_twice(old)
    area_ratio=Q(F(3,2),F(3,20))
    assert C.area_twice(FULL)==area_ratio*C.area_twice(old)
    weights=[F(1,10),F(5,6),F(1,15)];assert min(weights)>0 and sum(weights)==1
    witness=H.vec(sum((weights[j]*LEFT[j][k] for j in range(3)),ZERO) for k in range(3))
    sign=C.area_twice(LEFT).sign()
    assert all((H.cross(H.sub(b,a),H.sub(witness,a))[2]*sign).sign()>0 for a,b in zip(LEFT,LEFT[1:]+LEFT[:1]))
    ray=lambda j,t:H.add(C.M,H.mul(t,H.sub(C.N[j],C.M)))
    regions=[[C.M,ray(3,F(1,8)),ray(4,F(1,4))],
        [C.M,ray(4,F(1,4)),C.N[7]],[C.M,C.N[7],C.N[8]],
        [C.M,C.N[8],ray(10,F(1,6))],C.triangle(F(2,5)),C.triangle(F(1,2)),
        C.triangle(F(2,3)),C.triangle(F(3,4)),old]
    images=C.orbit(witness);assert len(images)==60
    for u in images:
        for a,b,c in regions:
            det=C.determinant(a,b,c);assert det.sign()!=0
            coordinates=[C.determinant(u,b,c)/det,C.determinant(a,u,c)/det,C.determinant(a,b,u)/det]
            assert not(all(x.sign()>=0 for x in coordinates) or all(x.sign()<=0 for x in coordinates))
    centers=C.orbit(C.M);assert len(centers)==30
    cosine=1-F(1,50)**2/2
    for v in centers:assert (Q(cosine*cosine)*H.dot(witness,witness)*H.dot(v,v)-H.dot(witness,v)**2).sign()>0
    walls=[source.reflection(w) for w in source.WALLS];group={source.I};pending=[source.I]
    generators=[source.mm(walls[0],walls[1]),source.mm(walls[1],walls[2])]
    while pending:
        g=pending.pop()
        for h in generators:
            x=source.mm(h,g)
            if x not in group:group.add(x);pending.append(x);assert len(group)<=60
    assert len(group)==60
    for g in group:
        assert source.mm(g,tuple(zip(*g)))==source.I and C.determinant(*g)==Q(1)
        assert {source.mv(g,v) for v in V}==set(V)
    J=tuple(tuple(2*C.M[i]*C.M[j]/C.M2-Q(int(i==j)) for j in range(3)) for i in range(3))
    separation=min(sum(((J[i][j]-g[i][j])**2 for i in range(3) for j in range(3)),ZERO) for g in group)
    assert separation==Q(F(106,29),F(-36,29))
    d=F(21027,200000);assert all(C.chord_less(u,d) for u in FULL)
    assert separation>Q(8*d*d)
    return {'full_original_corner_indices':[10,9,8],'full_receiver_rays':[list(map(str,u)) for u in FULL],
        'left_receiver_rays':[list(map(str,u)) for u in LEFT],'partition_ratio':str(ratio),
        'closed_partition_full_cell9_equals_D1_union_left':True,
        'unit_z_chart_area_ratio_over_D1':str(area_ratio),'spherical_area_ratio_claimed':False,
        'new_strict_interior_receiver_witness':list(map(str,witness)),
        'witness_left_barycentric_weights':list(map(str,weights)),
        'projective_witness_images':60,'old_closed_triangular_cones_per_image':9,
        'old_closed_cone_membership_tests':540,'witness_images_in_old_closed_regions':0,
        'minimum_projective_axes_checked':30,'witness_chord_lower':'1/50 > 1/64',
        'actual_proper_body_rotations':60,'original_vertex_permutation_checks':3720,
        'full_cell9_chord_upper_for_coset_separation':str(d),
        'receiver_halfturn_separation_squared_at_m':str(separation),
        'full_cell9_halfturn_separation_margin':str(separation-Q(8*d*d))}

def supports():
    q=H.pdot(local.X,local.X);den=H.padd(local.ONE,q);minus=H.psub(local.ONE,q)
    skew=local.transpose([H.pcross(local.X,local.pvec(v)) for v in H.UNITS])
    numerator=[[H.sum_polys([minus if i==j else {},H.pscale(H.pmul(local.X[i],local.X[j]),2),
        H.pscale(skew[i][j],2)]) for j in range(3)] for i in range(3)]
    gram=local.mm(local.transpose(numerator),numerator)
    assert all(gram[i][j]==(H.psquare(den) if i==j else {}) for i in range(3) for j in range(3))
    assert local.determinant(numerator)==H.pmul(H.psquare(den),den)
    contacts=[];comparisons=identities=0
    for a,b,j in H.CONTACTS:
        assert a!=b and j in (a,b);rows=[]
        for u in FULL:
            mu=H.cross(H.sub(V[b],V[a]),u);height=H.dot(mu,V[j]);torque=H.cross(V[j],mu)
            assert H.dot(mu,u)==ZERO and height.sign()>0 and H.dot(mu,mu).sign()>0
            for v in V:assert H.dot(mu,H.sub(V[j],v)).sign()>=0;comparisons+=1
            linear=H.pdot(local.pvec(torque),local.X)
            quadratic=H.psub(H.pmul(H.pdot(local.pvec(V[j]),local.X),H.pdot(local.pvec(mu),local.X)),H.pscale(q,height))
            polynomial=H.padd(linear,quadratic)
            nv=[H.sum_polys([H.pscale(numerator[i][k],V[j][k]) for k in range(3)]) for i in range(3)]
            difference=[H.psub(nv[i],H.pscale(den,V[j][i])) for i in range(3)]
            assert H.pdot(local.pvec(mu),difference)==H.pscale(polynomial,2);identities+=1
            rows.append((torque,V[j],mu,height))
        contacts.append(rows)
    return contacts,{'original_support_comparisons':comparisons,'persistent_original_contact_identities':identities,
        'matrix_orthogonality_polynomial_identities':9,'matrix_determinant_polynomial_identities':1,
        'all_original_contacts':list(map(list,H.CONTACTS))}

def closed_axis_face(record):
    assert set(record)=={'axis','sign','leaves'} and record['axis'] in range(3) and record['sign'] in (-1,1)
    leaves=record['leaves'];assert isinstance(leaves,list) and leaves
    for row in leaves:
        assert isinstance(row,list) and len(row)==3
        path,j,l=row
        assert isinstance(path,str) and len(path)<=MAX_DEPTH and set(path)<=set('0123')
        assert isinstance(j,int) and j in CONTACT_IDS
        assert F(l)==local.norm_lower(local.box_bounds(path))
    paths=[r[0] for r in leaves];wanted=set(paths);assert len(paths)==len(wanted)
    seen=[];nodes=0
    def visit(path):
        nonlocal nodes
        nodes+=1
        if path in wanted:seen.append(path);return
        assert len(path)<MAX_DEPTH and any(p.startswith(path) for p in wanted)
        for child in '0123':visit(path+child)
    visit('');assert set(seen)==wanted and sum((F(1,4)**len(p) for p in paths),F(0))==1
    return nodes

def closed_axis_covers(records):
    assert len(records)==6
    assert [(r['axis'],r['sign']) for r in records]==list(itertools.product(range(3),(-1,1)))
    return [closed_axis_face(r) for r in records]

def replay_face(contacts,record):
    axis,sign=record['axis'],record['sign'];nodes=closed_axis_face(record)
    data={j:[local.face_coeff(row,axis,sign) for row in contacts[j]] for j in CONTACT_IDS}
    audits=sum(local.audit_face_coeffs(row,axis,sign,*la) for j in CONTACT_IDS for row,la in zip(contacts[j],data[j]))
    digest=hashlib.sha256();count=direct=0
    for path,j,saved_l in record['leaves']:
        box=local.box_bounds(path);ell=local.norm_lower(box);assert ell==F(saved_l)
        witnesses=[local.coeffs(L,B,box,ell) for L,B in data[j]]
        assert len(witnesses)==3 and all(w is not None for w in witnesses)
        for row,(L,B),witness in zip(contacts[j],data[j],witnesses):
            first,bern=witness;count+=len(first)+len(bern)
            digest.update(json.dumps(list(map(str,first+bern)),separators=(',',':')).encode())
            direct+=local.leaf_direct_audits(row,axis,sign,L,B,box,ell,witness)
    return {'axis':axis,'sign':sign,'nodes':nodes,'closed_leaves':len(record['leaves']),
        'max_depth':max(len(r[0]) for r in record['leaves']),
        'strict_positive_linear_and_quadratic_coefficients':count,'coefficient_sha256':digest.hexdigest(),
        'original_face_polynomial_audits':audits,'leaf_direct_vector_and_Bernstein_audits':direct}

def controls(rows,covers,sharp):
    rejected=[]
    def reject(name,job):
        try:job()
        except AssertionError:rejected.append(name)
        else:raise AssertionError('malformed evidence accepted: '+name)
    def changed(job):
        r=copy.deepcopy(covers);job(r);return r
    reject('missing closed roll interval',lambda:closed_roll_cover(rows[:-1]))
    reject('duplicate closed roll interval',lambda:closed_roll_cover(rows+[rows[-1]]))
    reject('missing signed roll half',lambda:closed_roll_cover([r for r in rows if r[0]==1]))
    bad=copy.deepcopy(rows);bad[0][1]='1/9'
    reject('gapped roll endpoint',lambda:closed_roll_cover(bad))
    badpoint=copy.deepcopy(rows);badpoint[0][4]=74
    reject('unknown original source point',lambda:closed_roll_cover(badpoint))
    reject('missing closed axis face',lambda:closed_axis_covers(covers[:-1]))
    reject('duplicate closed axis face',lambda:closed_axis_covers(changed(lambda r:r.__setitem__(1,copy.deepcopy(r[0])))))
    reject('missing closed axis leaf',lambda:closed_axis_covers(changed(lambda r:r[0]['leaves'].pop())))
    reject('duplicate closed axis leaf',lambda:closed_axis_covers(changed(lambda r:r[0]['leaves'].append(copy.deepcopy(r[0]['leaves'][0])))))
    reject('overlapping axis ancestor',lambda:closed_axis_covers(changed(lambda r:r[0]['leaves'].append(['',1,'1']))))
    reject('invalid axis subdivision',lambda:closed_axis_covers(changed(lambda r:r[0]['leaves'][0].__setitem__(0,'4'))))
    reject('excess axis depth',lambda:closed_axis_covers(changed(lambda r:r[0]['leaves'][0].__setitem__(0,'0000'))))
    reject('unknown original contact',lambda:closed_axis_covers(changed(lambda r:r[0]['leaves'][0].__setitem__(1,12))))
    reject('false axis norm lower',lambda:closed_axis_covers(changed(lambda r:r[0]['leaves'][0].__setitem__(2,'2'))))
    reject('wrong tensor mixed term',lambda:local.bernstein_identity_audits(F(1,2)))
    lo=F(sharp['sharp_minimum_witness']['chord_rational_enclosure'][0])
    def require(x):assert x
    reject('false smaller source cap85406/1e6',lambda:require(lo<F(85406,10**6)))
    q,_=C.area_maximum(H.vec(map(C.parse,C.P['cell_certificates'][9]['area_vector'])),LEFT)
    reject('false receiving area upper',lambda:require(Q((T-F(1,10**6))**2)>q))
    incomplete=copy.deepcopy(C.P);incomplete['cell_certificates'].pop()
    reject('missing closed global area cell',lambda:source.structure(incomplete))
    reject('insufficient Cayley radius1/10',lambda:require(F(1,10)*(1-THETA*THETA/8)-THETA/2>0))
    reject('nonstrict axis coefficient',lambda:require(all(x.sign()>0 for x in (Q(1),ZERO))))
    return rejected

def check(rows,covers):
    checked=pins();closed_roll_cover(rows);closed_axis_covers(covers)
    with C.audit_signs() as qa,source.audit_radicals() as ra:
        geom=geometry();nearest=source.nearest_axis()
        sharp=source.certify(T,A)
        lo,hi=map(F,sharp['sharp_minimum_witness']['chord_rational_enclosure'])
        assert F(85406,10**6)<lo<hi<A
        left=phase(rows)
        theta,inherited=C.phase(F(1));assert theta==THETA
        assert inherited==C.fixture()['prerequisites']['full_D1_phase']
        gate=R*(1-THETA*THETA/8)-THETA/2;assert gate>0
        contacts,support=supports();basis=local.bernstein_identity_audits()
        faces=[replay_face(contacts,r) for r in covers]
        rejected=controls(rows,covers,sharp)
    assert sum(r['closed_leaves'] for r in faces)==45
    assert sum(r['strict_positive_linear_and_quadratic_coefficients'] for r in faces)==1755
    return {'agent':'six-rupert-1','role':'researcher','global_Rupert_property':'OPEN',
        'status':'complete exact finite hypotheses for whole closed receiving cell9 rigidity',
        'pins':checked,'receiver_geometry':geom,'global_nearest_minimum_axis':nearest,
        'new_complete_global_source_critical_strata':sharp,'new_sharp_radius_window':['85406/1000000','85407/1000000'],
        'left_receiver_coupled_phase':left,'inherited_D1_phase_all_expected_fields_match':True,
        'inherited_D1_phase_sha256':H.digest(inherited),'full_cell9_angle_upper':str(THETA),
        'cayley_radius_upper':str(R),'full_cell9_angle_to_cayley_gate':str(gate),
        'global_physical_area_fan':'inherited and byte-pinned; new source234critical strata freshly enumerated',
        'whole_cell9_original_support_and_Cayley_audits':support,'tensor_Bernstein_basis_identities':basis,
        'full_cell9_axis_faces':faces,'closed_axis_leaves':45,'strict_positive_coefficients':1755,
        'fixed_axis_case_sha256':H.digest(covers),'fixed_roll_case_sha256':H.digest(rows),
        'independent_Q5_sign_audits':qa,'independent_radical_sign_audits':ra,
        'sign_audit_scope':'main verification phase; imported byte-pinned constructors are inherited prerequisites',
        'malformed_controls_rejected':rejected}

if __name__=='__main__':
    started=time.monotonic();saved=fixture()
    assert set(saved)=={'fixed_remote_roll_cover','fixed_axis_covers','expected'}
    actual=check(saved['fixed_remote_roll_cover'],saved['fixed_axis_covers'])
    assert json.loads(json.dumps(actual))==saved['expected'],'every expected mathematical field must match'
    print(json.dumps({'all_expected_fields_match':True,'global_Rupert_property':'OPEN',
        'closed_axis_leaves':actual['closed_axis_leaves'],'strict_positive_coefficients':actual['strict_positive_coefficients'],
        'closed_roll_intervals':actual['left_receiver_coupled_phase']['remote_interval_count'],
        'new_source_critical_strata':actual['new_complete_global_source_critical_strata']['counts']['generated'],
        'malformed_controls_rejected':len(actual['malformed_controls_rejected']),
        'elapsed_seconds':time.monotonic()-started,'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))
