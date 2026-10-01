"""Fixed exact hypotheses for the closed Cell8 collar. Python3.11+ stdlib.

See cell8_collar_proof.md for the all-original-source continuous argument.
No discovery, floating predicates, or modification of parent guards occurs.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import copy,hashlib,itertools,json,time,resource
if not __debug__:raise RuntimeError('verification requires assertions; do not use python -O')
import cell9_coupled_certificate as nine
from verify import convex_hull_2d,project
C=nine.C;H=C.H;Q=H.Q5;ZERO=H.ZERO;V=C.V;local=nine.local;source=nine.source
ROOT=Path(__file__).parent;R=F(1,8);MAX_DEPTH=4
T=[F(7402953,500000),F(14824807,1000000)]
A=[F(24367,250000),F(109189,1000000)]
D=[F(12981,200000),F(21027,200000)]
PINS={'cell9_coupled_certificate.py':'b57ca7f51a9d872fd5f9d908380b84aa67b64680fc5ce27aafd1d18546ab4773',
      'expected_cell9_coupled.json':'2dd4297158e3af60b37613569527cb401f2452a3c71ef056b6e6cb16841a2f4c'}
QUAD=[C.N[j] for j in (6,11,10,8)]
U=H.mul(F(1,4),tuple(sum((u[k] for u in QUAD),ZERO) for k in range(3)))
TIPS=[H.add(H.mul(1-t,nine.W),H.mul(t,U)) for t in (F(1,10),F(1,5))]
TRIANGLES=[[C.N[8],nine.W,TIPS[0]],[nine.W,C.N[10],TIPS[1]]]
FULL=[C.N[8],C.N[10],TIPS[0]]
LARGE=[C.N[8],C.N[10],TIPS[1]]
VECTOR=H.vec(map(C.parse,C.P['cell_certificates'][8]['area_vector']))

def pins():
    checked=nine.pins()
    for name,wanted in PINS.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==wanted
    assert local.R==F(27,250) and local.MAX_DEPTH==3
    return {**checked,**PINS}

def fixture():return json.loads((ROOT/'expected_cell8_collar.json').read_text())

def geometry():
    assert C.P['cell_certificates'][8]['corner_indices']==[6,11,10,8]
    edges=[H.cross(u,QUAD[(i+1)%4]) for i,u in enumerate(QUAD)]
    assert all(H.dot(e,u).sign()>=0 for e in edges for u in QUAD+LARGE+FULL)
    assert all(H.dot(e,tip).sign()>0 for e in edges for tip in TIPS)
    ratio=Q(F(17,57),F(4,57));assert nine.W==H.add(H.mul(1-ratio,C.N[8]),H.mul(ratio,C.N[10]))
    base_right=[nine.W,C.N[10],TIPS[0]]
    assert TIPS[0]==H.mul(F(1,2),H.add(nine.W,TIPS[1]))
    assert C.area_twice(FULL)==C.area_twice(TRIANGLES[0])+C.area_twice(base_right)
    assert all(C.weak_inside(u,TRIANGLES[1]) for u in base_right)
    assert all(C.weak_inside(u,LARGE) for tri in TRIANGLES for u in tri)
    prior=nine.geometry();assert prior==nine.fixture()['expected']['receiver_geometry']
    sep=C.parse(prior['receiver_halfturn_separation_squared_at_m'])
    assert all(C.chord_less(u,D[1]) for tri in TRIANGLES for u in tri) and sep>Q(8*D[1]*D[1])
    witness=H.mul(F(1,3),tuple(sum((u[k] for u in TRIANGLES[0]),ZERO) for k in range(3)))
    sign=C.area_twice(TRIANGLES[0]).sign()
    assert all((H.cross(H.sub(b,a),H.sub(witness,a))[2]*sign).sign()>0 for a,b in zip(TRIANGLES[0],TRIANGLES[0][1:]+TRIANGLES[0][:1]))
    ray=lambda j,t:H.add(C.M,H.mul(t,H.sub(C.N[j],C.M)))
    old=[[C.M,ray(3,F(1,8)),ray(4,F(1,4))],[C.M,ray(4,F(1,4)),C.N[7]],
         [C.M,C.N[7],C.N[8]],[C.M,C.N[8],ray(10,F(1,6))],
         C.triangle(F(2,5)),C.triangle(F(1,2)),C.triangle(F(2,3)),C.triangle(F(3,4)),C.triangle(F(1)),nine.FULL]
    images=C.orbit(witness);assert len(images)==60
    for u in images:
        for a,b,c in old:
            det=C.determinant(a,b,c);assert det.sign()!=0
            coords=[C.determinant(u,b,c)/det,C.determinant(a,u,c)/det,C.determinant(a,b,u)/det]
            assert not(all(x.sign()>=0 for x in coords) or all(x.sign()<=0 for x in coords))
    centers=C.orbit(C.M);assert len(centers)==30
    cosine=1-F(1,50)**2/2
    for u in centers:assert (Q(cosine*cosine)*H.dot(witness,witness)*H.dot(u,u)-H.dot(witness,u)**2).sign()>0
    return {'original_cell8_corners':[6,11,10,8],'collar_parameters':['1/10','1/5'],
        'quad_center':list(map(str,U)),'tips':[list(map(str,tip)) for tip in TIPS],
        'closed_receiver_triangles':[[list(map(str,u)) for u in tri] for tri in TRIANGLES],
        'entire_closed_1_10_collar_in_union':True,'entire_1_5_collar_claimed':False,
        'cell8_cone_support_comparisons':len(edges)*(len(QUAD)+len(LARGE)+len(FULL)),
        'old_cell9_geometry_all_fields_match':True,'old_geometry_sha256':H.digest(prior),
        'moving_halfturn_separation_squared_at_m':str(sep),'separation_margin':str(sep-Q(8*D[1]*D[1])),
        'new_strict_interior_witness':list(map(str,witness)),'projective_witness_images':60,
        'prior_triangular_cones_per_image':10,'exact_prior_cone_tests':600,
        'witness_images_in_prior_cones':0,'minimum_projective_axes':30,'witness_chord_lower':'1/50 > 1/64'}

def phase(case,rows):
    nine.closed_roll_cover(rows);tri=TRIANGLES[case];a=A[case];d=D[case]
    q,area=C.area_maximum(VECTOR,tri)
    assert Q(T[case]*T[case])>q and C.root_upper(q)==T[case]
    assert all(C.chord_less(u,d) for u in tri)
    envelopes=C.linear_envelopes(tri)
    vertex_perp=[C.root_upper(H.dot(project(v,C.M),project(v,C.M))) for v in V]
    point_perp=[C.root_upper(H.dot(project(p,C.M),project(p,C.M))) for p,_ in C.POINTS]
    receiver=[];records=[];comparisons=0
    for pi,p in enumerate(C.PROBES):
        values=[]
        for j,v in enumerate(V):
            gamma=H.dot(p['mu'],v);correction=p['norm_upper']*vertex_perp[j]-gamma
            assert correction.sign()>=0
            for side,xi in enumerate((envelopes[pi]['lo'],envelopes[pi]['hi'])):
                z=-H.dot(C.M,v)*xi-(p['H']-gamma)+d*d*correction/4
                values.append((z,j,side));comparisons+=1
        bound=max(ZERO,*(z for z,_,_ in values));receiver.append(bound)
        records.append({'probe':pi,'receiver_excess_upper':str(bound),
            'active_vertices_and_sides':[[j,s] for z,j,s in values if z==bound],
            'corner_ratio_lower':str(envelopes[pi]['lo']),'corner_ratio_upper':str(envelopes[pi]['hi'])})
    c=1-a*a/4;assert c>0
    def coefficients(sign,pi,wi):
        p,row=C.PROBES[pi],C.DATA[pi][wi]
        error=p['norm_upper']*row['source_height_upper']*a+a*a*p['norm_upper']*point_perp[wi]/4+receiver[pi]
        coef=(c*row['d']-p['H']-error,Q(2*c*row['tau'][sign]),-c*row['d']-p['H']-error)
        assert error.sign()>=0 and coef[2].sign()<0
        return coef
    value=lambda coef,x:coef[0]+coef[1]*x+coef[2]*x*x
    gates=[]
    for sign,pi in ((-1,3),(1,4)):
        p,row=C.PROBES[pi],C.DATA[pi][45]
        assert H.dot(C.M,V[45])==ZERO and row['d']==p['H'] and row['tau'][sign]>0
        coef=coefficients(sign,pi,45);quad=lambda x:-value(coef,x)
        assert quad(0).sign()>0 and quad(F(1,10)).sign()<0
        xu=C.grid_upper(lambda x:quad(x).sign()<0,F(1,10))
        assert quad(xu).sign()<0 and quad(xu-F(1,10**6)).sign()>=0
        gates.append({'sign':sign,'probe':pi,'point':45,'coefficients':list(map(str,coef)),
            'q_zero':str(quad(0)),'q_b':str(quad(F(1,10))),'small_root_upper':str(xu),
            'roll_chord_upper':str(2*xu),'q_upper':str(quad(xu)),'q_predecessor':str(quad(xu-F(1,10**6)))})
    remote=[]
    for sign,lo,hi,pi,wi in rows:
        coef=coefficients(sign,pi,wi);margins=[value(coef,F(x)) for x in (lo,hi)]
        assert all(x.sign()>0 for x in margins)
        remote.append({'sign':sign,'interval':[lo,hi],'probe':pi,'point':wi,
            'coefficients':list(map(str,coef)),'strict_endpoint_margins':list(map(str,margins)),
            'original_source_point_certificate':C.POINTS[wi][1]})
    roll=max(F(g['roll_chord_upper']) for g in gates)
    product=(1-a*a/4)*(1-d*d/4)*(1-roll*roll/4);X2=(a+d)**2+roll*roll
    assert product>F(99,100)**2 and F(99,100)-a*d/4>0 and X2<=F(1,9)
    beta=next(F(j,1000) for j in range(1001,1020) if F(j,1000)**2*(1-X2/4)>1)
    theta=C.grid_upper(lambda x:Q(x*x)>Q(beta*beta*X2),F(1,3));gate=R*(1-theta*theta/8)-theta/2
    assert gate>0
    return {'maximum_area_squared':str(q),'maximum_area':area,'source_area_upper':str(T[case]),
        'source_chord_upper':str(a),'receiver_chord_upper':str(d),
        'receiver_vertex_and_side_comparisons':comparisons,'rank_receiver_envelopes':records,
        'near_zero_gates':gates,'fixed_remote_cover':remote,'remote_interval_count':len(remote),
        'roll_chord_upper':str(roll),'full_angle_upper':str(theta),'composition_squared_upper':str(X2),
        'angle_derivative_beta':str(beta),'quaternion_product_margin':str(product-F(99,100)**2),
        'angle_derivative_margin':str(beta*beta*(1-X2/4)-1),'angle_to_cayley_radius1_8_gate':str(gate)}

def supports(tri):
    u=H.mul(F(1,3),tuple(sum((v[k] for v in tri),ZERO) for k in range(3)))
    e1=H.vec((1,0,-u[0]));e2=H.vec((0,1,-u[1]))
    assert H.dot(e1,u)==H.dot(e2,u)==ZERO and H.cross(e1,e2)==u
    mapping={}
    for j,v in enumerate(V):mapping.setdefault((H.dot(v,e1),H.dot(v,e2)),[]).append(j)
    hull=[mapping[p][0] for p in convex_hull_2d(mapping)]
    cross_sum=H.vec(sum((H.cross(V[a],V[b])[k]/2 for a,b in zip(hull,hull[1:]+hull[:1])),ZERO) for k in range(3))
    assert cross_sum==VECTOR
    contacts=[];triples=[];seen=set();comparisons=identities=0
    q=H.pdot(local.X,local.X);den=H.padd(local.ONE,q);minus=H.psub(local.ONE,q)
    skew=local.transpose([H.pcross(local.X,local.pvec(v)) for v in H.UNITS])
    numerator=[[H.sum_polys([minus if i==j else {},H.pscale(H.pmul(local.X[i],local.X[j]),2),H.pscale(skew[i][j],2)]) for j in range(3)] for i in range(3)]
    gram=local.mm(local.transpose(numerator),numerator)
    assert all(gram[i][j]==(H.psquare(den) if i==j else {}) for i in range(3) for j in range(3))
    assert local.determinant(numerator)==H.pmul(H.psquare(den),den)
    for a,b in zip(hull,hull[1:]+hull[:1]):
        for j in (a,b):
            rows=[]
            for corner in tri:
                mu=H.cross(H.sub(V[b],V[a]),corner);h=H.dot(mu,V[j]);torque=H.cross(V[j],mu)
                assert h.sign()>0 and H.dot(mu,mu).sign()>0 and H.dot(mu,corner)==ZERO
                for v in V:assert H.dot(mu,H.sub(V[j],v)).sign()>=0;comparisons+=1
                rows.append((torque,V[j],mu,h))
            key=tuple(tuple(local.face_coeff(row,0,1)[0])+tuple(local.face_coeff(row,0,1)[1]) for row in rows)
            if key in seen:continue
            seen.add(key);triples.append([a,b,j]);contacts.append(rows)
            for torque,v,mu,h in rows:
                polynomial=H.padd(H.pdot(local.pvec(torque),local.X),H.psub(H.pmul(H.pdot(local.pvec(v),local.X),H.pdot(local.pvec(mu),local.X)),H.pscale(q,h)))
                nv=[H.sum_polys([H.pscale(numerator[i][k],v[k]) for k in range(3)]) for i in range(3)]
                difference=[H.psub(nv[i],H.pscale(den,v[i])) for i in range(3)]
                assert H.pdot(local.pvec(mu),difference)==H.pscale(polynomial,2);identities+=1
    assert len(hull)==20 and len(contacts)==20
    return contacts,{'hull_original_indices':hull,'unique_original_contacts':triples,
        'physical_area_vector_independently_matches_hull':True,'support_comparisons':comparisons,
        'Cayley_displacement_identities':identities,'proper_matrix_Gram_identities':9,'proper_matrix_determinant_identity':1}

def coefficients(L,B,box,ell):
    LB,AB=local.transformed(L,B,box)
    first=[LB[0]+LB[1]*i+LB[2]*j for i in (0,1) for j in (0,1)]
    if any(x.sign()<=0 for x in first):return None
    p=tuple(ell*(LB[k] if k<3 else ZERO)+R*AB[k] for k in range(6))
    bern=[p[0]+F(i,2)*p[1]+F(j,2)*p[2]+(p[3] if i==2 else ZERO)+F(i*j,4)*p[4]+(p[5] if j==2 else ZERO) for i in range(3) for j in range(3)]
    return (first,bern) if all(x.sign()>0 for x in bern) else None

def closed_covers(records):
    assert isinstance(records,list) and len(records)==6
    assert [(r['axis'],r['sign']) for r in records]==list(itertools.product(range(3),(-1,1)))
    for face in records:
        assert set(face)=={'axis','sign','leaves'} and isinstance(face['leaves'],list) and face['leaves']
        paths=[]
        for row in face['leaves']:
            assert isinstance(row,list) and len(row)==3
            path,j,ell=row
            assert isinstance(path,str) and len(path)<=MAX_DEPTH and set(path)<=set('0123')
            assert isinstance(j,int) and 0<=j<20 and F(ell)==local.norm_lower(local.box_bounds(path))
            paths.append(path)
        wanted=set(paths);assert len(wanted)==len(paths)
        def visit(path):
            if path in wanted:return
            assert len(path)<MAX_DEPTH and any(p.startswith(path) for p in wanted)
            for c in '0123':visit(path+c)
        visit('');assert sum((F(1,4)**len(p) for p in paths),F(0))==1

def direct_audits(row,axis,sign,L,B,box,ell,witness):
    torque,v,mu,h=row;first,bern=witness;LB,AB=local.transformed(L,B,box);x0,y0,dx,dy=box
    others=[k for k in range(3) if k!=axis]
    for s,t in ((F(0),F(0)),(F(1),F(1)),(F(1,3),F(2,5))):
        x=x0+dx*s;y=y0+dy*t;z=[F(0)]*3;z[axis]=F(sign);z[others[0]]=x;z[others[1]]=y
        linear=H.dot(torque,z);quadratic=H.dot(v,z)*H.dot(mu,z)-h*H.dot(z,z)
        assert LB[0]+LB[1]*s+LB[2]*t==linear
        assert AB[0]+AB[1]*s+AB[2]*t+AB[3]*s*s+AB[4]*s*t+AB[5]*t*t==quadratic
        bs=[F(comb(2,i))*s**i*(1-s)**(2-i) for i in range(3)]
        bt=[F(comb(2,j))*t**j*(1-t)**(2-j) for j in range(3)]
        assert sum((bern[3*i+j]*bs[i]*bt[j] for i in range(3) for j in range(3)),ZERO)==ell*linear+R*quadratic
    return 9

def replay(contacts,covers):
    closed_covers(covers);faces=[]
    for face in covers:
        axis,sign=face['axis'],face['sign'];data=[[local.face_coeff(row,axis,sign) for row in rows] for rows in contacts]
        audits=sum(local.audit_face_coeffs(row,axis,sign,*co) for rows,cos in zip(contacts,data) for row,co in zip(rows,cos))
        digest=hashlib.sha256();count=direct=0
        for path,j,saved_l in face['leaves']:
            box=local.box_bounds(path);ell=local.norm_lower(box);assert ell==F(saved_l)
            for row,(L,B) in zip(contacts[j],data[j]):
                witness=coefficients(L,B,box,ell);assert witness is not None
                first,bern=witness;count+=len(first)+len(bern)
                digest.update(json.dumps(list(map(str,first+bern)),separators=(',',':')).encode())
                direct+=direct_audits(row,axis,sign,L,B,box,ell,witness)
        faces.append({'axis':axis,'sign':sign,'closed_leaves':len(face['leaves']),
            'max_depth':max(len(r[0]) for r in face['leaves']),'strict_positive_coefficients':count,
            'coefficient_sha256':digest.hexdigest(),'original_face_audits':audits,'leaf_direct_audits':direct})
    return faces

def controls(cases):
    rejected=[]
    def reject(name,job):
        try:job()
        except (AssertionError,ValueError):rejected.append(name)
        else:raise AssertionError('malformed evidence accepted: '+name)
    for case,data in enumerate(cases):
        rows=data['roll'];covers=data['axes']
        reject(f'{case}:missing roll interval',lambda:nine.closed_roll_cover(rows[:-1]))
        reject(f'{case}:missing signed roll half',lambda:nine.closed_roll_cover([r for r in rows if r[0]==1]))
        reject(f'{case}:duplicate roll interval',lambda:nine.closed_roll_cover(rows+[rows[-1]]))
        reject(f'{case}:missing cube face',lambda:closed_covers(covers[:-1]))
        def changed(job):
            r=copy.deepcopy(covers);job(r);return r
        reject(f'{case}:missing cube leaf',lambda:closed_covers(changed(lambda r:r[0]['leaves'].pop())))
        reject(f'{case}:duplicate cube leaf',lambda:closed_covers(changed(lambda r:r[0]['leaves'].append(r[0]['leaves'][0]))))
        reject(f'{case}:unknown original contact',lambda:closed_covers(changed(lambda r:r[0]['leaves'][0].__setitem__(1,20))))
        reject(f'{case}:false norm lower',lambda:closed_covers(changed(lambda r:r[0]['leaves'][0].__setitem__(2,'2'))))
    reject('wrong mixed Bernstein term',lambda:local.bernstein_identity_audits(F(1,2)))
    incomplete=copy.deepcopy(C.P);incomplete['cell_certificates'].pop()
    reject('missing global source fan cell',lambda:source.structure(incomplete))
    return rejected

def check(cases):
    assert isinstance(cases,list) and len(cases)==2
    assert all(set(c)=={'roll','axes'} for c in cases)
    checked=pins()
    for data in cases:nine.closed_roll_cover(data['roll']);closed_covers(data['axes'])
    with C.audit_signs() as qa,source.audit_radicals() as ra:
        geom=geometry();nearest=source.nearest_axis()
        probes,points,data=C.reference.reference();assert (probes,points,data)==(C.PROBES,C.POINTS,C.DATA)
        basis=local.bernstein_identity_audits();pieces=[]
        for i,data in enumerate(cases):
            sharp=source.certify(T[i],A[i]);lo,hi=map(F,sharp['sharp_minimum_witness']['chord_rational_enclosure'])
            assert A[i]-F(1,10**6)<lo<hi<A[i]
            ph=phase(i,data['roll']);contacts,support=supports(TRIANGLES[i]);faces=replay(contacts,data['axes'])
            pieces.append({'source_critical_strata':sharp,'paired_full_roll_phase':ph,
                'original_support_and_Cayley_audits':support,'signed_axis_faces':faces,
                'fixed_roll_sha256':H.digest(data['roll']),'fixed_axes_sha256':H.digest(data['axes'])})
        rejected=controls(cases)
    return {'agent':'six-rupert-1','role':'researcher','global_Rupert_property':'OPEN',
        'status':'complete exact finite hypotheses for the closed Cell8 collar; written bridge is separate',
        'pins':checked,'receiver_geometry':geom,'global_nearest_minimum_axis':nearest,
        'original_reference_facets':16,'original_facet_support_comparisons':992,'actual_source_points':74,
        'new_cayley_radius':'1/8','tensor_Bernstein_basis_identities':basis,'pieces':pieces,
        'closed_axis_leaves':sum(f['closed_leaves'] for p in pieces for f in p['signed_axis_faces']),
        'strict_positive_coefficients':sum(f['strict_positive_coefficients'] for p in pieces for f in p['signed_axis_faces']),
        'independent_Q5_sign_audits':qa,'independent_radical_sign_audits':ra,
        'sign_audit_scope':'main verification phase; imported byte-pinned constructors are inherited prerequisites',
        'malformed_controls_rejected':rejected}

if __name__=='__main__':
    start=time.monotonic();saved=fixture();assert set(saved)=={'cases','expected'}
    actual=check(saved['cases']);assert json.loads(json.dumps(actual))==saved['expected'],'all expected mathematical fields must match'
    print(json.dumps({'all_expected_fields_match':True,'global_Rupert_property':'OPEN',
        'closed_axis_leaves':actual['closed_axis_leaves'],'strict_positive_coefficients':actual['strict_positive_coefficients'],
        'source_critical_candidates':[p['source_critical_strata']['counts']['generated'] for p in actual['pieces']],
        'roll_intervals':[p['paired_full_roll_phase']['remote_interval_count'] for p in actual['pieces']],
        'full_angle_uppers':[p['paired_full_roll_phase']['full_angle_upper'] for p in actual['pieces']],
        'malformed_controls_rejected':len(actual['malformed_controls_rejected']),
        'elapsed_seconds':time.monotonic()-start,'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))
