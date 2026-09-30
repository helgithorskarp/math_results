"""Fixed signed Cayley certificate for every receiver in closed D1.

Python3.11+ standard library; exact Q(sqrt5)/Fraction only. Every axis
is covered by six CLOSED cube faces and fixed complete dyadic square covers.
The continuous bridge and all-source scope are in cayley_wedge_proof.md.
"""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt,comb
import copy,itertools,json,hashlib,time,resource
if not __debug__:raise RuntimeError('verification requires assertions; do not use python -O')
import rank_transport_wedge_certificate as C
H=C.H;Q=H.Q5;ZERO=H.ZERO;V=C.V;ROOT=Path(__file__).parent
R=F(27,250);THETA=F(212461,1000000);TRI=C.triangle(F(1))
CANDIDATES=[1,4,5,6,7,10];MAX_DEPTH=3
ONE={(0,0,0):Q(1)}
X=[{tuple(int(i==k) for i in range(3)):Q(1)} for k in range(3)]
PINS={
    'rank_transport_wedge_certificate.py':'2b6d690a5dbbe214ab97ef067e84ffadec8598f7397b3f4010797438c31d3be2',
    'expected_rank_transport_wedge.json':'f6312a4fead973a153c4e0a320e446db4c3d5161bc48286abde5b7aa7a5a1c7c',
}
def pins():
    checked=C.pins()
    for name,wanted in PINS.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==wanted
    return {**checked,**PINS}
def fixture():return json.loads((ROOT/'expected_cayley_wedge.json').read_text())

def const(q):return {(0,0,0):Q.coerce(q)} if q!=ZERO else {}

def pvec(v):return [const(q) for q in v]

def mm(a,b):return [[H.sum_polys([H.pmul(a[i][k],b[k][j]) for k in range(3)]) for j in range(3)] for i in range(3)]

def transpose(a):return list(map(list,zip(*a)))

def determinant(a):return H.pdot(a[0],H.pcross(a[1],a[2]))

def prerequisites():
    assert 0<THETA<F(1,4) and 1-THETA*THETA/8>0
    gate=R*(1-THETA*THETA/8)-THETA/2;assert gate>0
    q=H.pdot(X,X);den=H.padd(ONE,q);minus=H.psub(ONE,q)
    skew=[H.pcross(X,pvec(v)) for v in H.UNITS]
    skew=transpose(skew)
    N=[[H.sum_polys([minus if i==j else {},H.pscale(H.pmul(X[i],X[j]),2),H.pscale(skew[i][j],2)]) for j in range(3)] for i in range(3)]
    gram=mm(transpose(N),N)
    assert all(gram[i][j]==(H.psquare(den) if i==j else {}) for i in range(3) for j in range(3))
    assert determinant(N)==H.pmul(H.psquare(den),den)
    contacts=[];supports=identities=0
    for contact,(a,b,j) in enumerate(H.CONTACTS):
        assert a!=b and j in (a,b)
        rows=[]
        for u in TRI:
            mu=H.cross(H.sub(V[b],V[a]),u);h=H.dot(mu,V[j]);T=H.cross(V[j],mu)
            assert H.dot(mu,u)==ZERO and h.sign()>0 and H.dot(mu,mu).sign()>0
            for v in V:assert H.dot(mu,H.sub(V[j],v)).sign()>=0;supports+=1
            first=H.pdot(pvec(T),X)
            second=H.psub(H.pmul(H.pdot(pvec(V[j]),X),H.pdot(pvec(mu),X)),H.pscale(q,h))
            cayley=H.padd(first,second)
            nv=[H.sum_polys([H.pscale(N[i][k],V[j][k]) for k in range(3)]) for i in range(3)]
            difference=[H.psub(nv[i],H.pscale(den,V[j][i])) for i in range(3)]
            assert H.pdot(pvec(mu),difference)==H.pscale(cayley,2);identities+=1
            rows.append((T,V[j],mu,h))
        contacts.append(rows)
    return contacts,{'angle_to_cayley_positive_gate':str(gate),'matrix_orthogonality_polynomial_identities':9,
        'matrix_determinant_polynomial_identities':1,'original_support_comparisons':supports,
        'persistent_original_contact_identities':identities,'all_original_contacts':list(map(list,H.CONTACTS))}

def face_coeff(row,axis,sg):
    T,v,mu,h=row;others=[k for k in range(3) if k!=axis];a,b=others
    L=(sg*T[axis],T[a],T[b])
    A=(v[axis]*mu[axis]-h,sg*(v[axis]*mu[a]+v[a]*mu[axis]),
       sg*(v[axis]*mu[b]+v[b]*mu[axis]),v[a]*mu[a]-h,
       v[a]*mu[b]+v[b]*mu[a],v[b]*mu[b]-h)
    return L,A

def box_bounds(path):
    x0=y0=F(-1);dx=dy=F(2)
    for c in path:
        assert c in '0123';i=int(c);dx/=2;dy/=2
        if i in (1,3):x0+=dx
        if i in (2,3):y0+=dy
    return x0,y0,dx,dy

def norm_lower(box):
    x0,y0,dx,dy=box
    def least(a,b):return min(a*a,b*b) if a*b>0 else F(0)
    sq=1+least(x0,x0+dx)+least(y0,y0+dy)
    grid=10**6;num=isqrt(sq.numerator*grid*grid//sq.denominator)
    l=F(num,grid)
    assert l>=1 and l*l<=sq and (l+F(1,grid))**2>sq
    return l

def transformed(L,A,box):
    x,y,dx,dy=box;l0,lx,ly=L;a0,ax,ay,axx,axy,ayy=A
    LB=(l0+lx*x+ly*y,lx*dx,ly*dy)
    AB=(a0+ax*x+ay*y+axx*x*x+axy*x*y+ayy*y*y,
        dx*(ax+2*axx*x+axy*y),dy*(ay+axy*x+2*ayy*y),
        axx*dx*dx,axy*dx*dy,ayy*dy*dy)
    return LB,AB

def coeffs(L,A,box,l):
    LB,AB=transformed(L,A,box)
    first=[LB[0]+LB[1]*i+LB[2]*j for i in (0,1) for j in (0,1)]
    if any(x.sign()<=0 for x in first):return None
    P=tuple(l*(LB[k] if k<3 else ZERO)+R*AB[k] for k in range(6))
    bern=[P[0]+F(i,2)*P[1]+F(j,2)*P[2]+(P[3] if i==2 else ZERO)+F(i*j,4)*P[4]+(P[5] if j==2 else ZERO)
          for i in range(3) for j in range(3)]
    if any(x.sign()<=0 for x in bern):return None
    return first,bern

def audit_face_coeffs(row,axis,sg,L,A):
    T,v,mu,h=row
    for x,y in ((F(-1),F(-1)),(F(-1),F(1)),(F(1),F(-1)),(F(1),F(1)),(F(1,3),F(-2,5))):
        z=[F(0)]*3;z[axis]=F(sg);others=[k for k in range(3) if k!=axis];z[others[0]]=x;z[others[1]]=y
        assert L[0]+L[1]*x+L[2]*y==H.dot(T,z)
        assert A[0]+A[1]*x+A[2]*y+A[3]*x*x+A[4]*x*y+A[5]*y*y==H.dot(v,z)*H.dot(mu,z)-h*H.dot(z,z)
    return 10

def validate_cover_geometry(record):
    assert set(record)=={'axis','sign','leaves'}
    assert record['axis'] in range(3) and record['sign'] in (-1,1)
    leaves=record['leaves'];assert leaves
    for row in leaves:
        assert isinstance(row,list) and len(row)==3
        path,j,l=row
        assert isinstance(path,str) and len(path)<=MAX_DEPTH and set(path)<=set('0123')
        assert isinstance(j,int) and j in CANDIDATES
        assert F(l)==norm_lower(box_bounds(path))
    paths=[row[0] for row in leaves];wanted=set(paths)
    assert len(wanted)==len(paths)
    seen=[];nodes=0
    def visit(path):
        nonlocal nodes
        nodes+=1
        if path in wanted:seen.append(path);return
        assert len(path)<MAX_DEPTH and any(p.startswith(path) for p in wanted)
        for i in range(4):visit(path+str(i))
    visit('');assert set(seen)==wanted
    assert sum((F(1,4)**len(p) for p in paths),F(0))==1
    return nodes

def validate_covers(records):
    assert len(records)==6
    assert [(r['axis'],r['sign']) for r in records]==list(itertools.product(range(3),(-1,1)))
    assert CANDIDATES==sorted(set(CANDIDATES))
    return [validate_cover_geometry(r) for r in records]

def bernstein_identity_audits(mixed=F(1,4)):
    # Reconstruct each of the SIX power-basis monomials independently in
    # the tensor Bernstein basis. This is a polynomial identity, not sampling.
    one={(0,0):Q(1)};sx={(1,0):Q(1)};sy={(0,1):Q(1)}
    def power(p,n):
        result=one
        for _ in range(n):result=H.pmul(result,p)
        return result
    bx=[H.pscale(H.pmul(power(sx,i),power(H.psub(one,sx),2-i)),comb(2,i)) for i in range(3)]
    by=[H.pscale(H.pmul(power(sy,j),power(H.psub(one,sy),2-j)),comb(2,j)) for j in range(3)]
    exponents=[(0,0),(1,0),(0,1),(2,0),(1,1),(0,2)]
    for k,exponent in enumerate(exponents):
        P=[Q(int(t==k)) for t in range(6)]
        rebuilt={}
        for i in range(3):
            for j in range(3):
                coefficient=P[0]+F(i,2)*P[1]+F(j,2)*P[2]+(P[3] if i==2 else ZERO)+mixed*i*j*P[4]+(P[5] if j==2 else ZERO)
                rebuilt=H.padd(rebuilt,H.pscale(H.pmul(bx[i],by[j]),coefficient))
        assert rebuilt=={exponent:Q(1)}
    return len(exponents)

def leaf_direct_audits(row,axis,sg,L,A,box,l,witness):
    T,v,mu,h=row;first,bern=witness;LB,AB=transformed(L,A,box);x0,y0,dx,dy=box
    others=[k for k in range(3) if k!=axis]
    for s,t in ((F(0),F(0)),(F(1),F(1)),(F(1,3),F(2,5))):
        x=x0+dx*s;y=y0+dy*t;z=[F(0)]*3;z[axis]=F(sg);z[others[0]]=x;z[others[1]]=y
        actual_first=H.dot(T,z);actual_second=H.dot(v,z)*H.dot(mu,z)-h*H.dot(z,z)
        assert LB[0]+LB[1]*s+LB[2]*t==actual_first
        assert AB[0]+AB[1]*s+AB[2]*t+AB[3]*s*s+AB[4]*s*t+AB[5]*t*t==actual_second
        b_s=[F(comb(2,i))*s**i*(1-s)**(2-i) for i in range(3)]
        b_t=[F(comb(2,j))*t**j*(1-t)**(2-j) for j in range(3)]
        actual=sum((bern[3*i+j]*b_s[i]*b_t[j] for i in range(3) for j in range(3)),ZERO)
        assert actual==l*actual_first+R*actual_second
    return 9

def replay_face(contacts,record):
    axis,sg=record['axis'],record['sign'];nodes=validate_cover_geometry(record)
    data={j:[face_coeff(row,axis,sg) for row in contacts[j]] for j in CANDIDATES}
    face_audits=sum(audit_face_coeffs(row,axis,sg,*la) for j in CANDIDATES for row,la in zip(contacts[j],data[j]))
    hashes=hashlib.sha256();coefficient_count=direct_audits=0
    for path,j,saved_l in record['leaves']:
        box=box_bounds(path);l=norm_lower(box);assert l==F(saved_l)
        witnesses=[coeffs(L,A,box,l) for L,A in data[j]]
        assert len(witnesses)==3 and all(w is not None for w in witnesses)
        for row,(L,A),witness in zip(contacts[j],data[j],witnesses):
            first,bern=witness;coefficient_count+=len(first)+len(bern)
            hashes.update(json.dumps(list(map(str,first+bern)),separators=(',',':')).encode())
            direct_audits+=leaf_direct_audits(row,axis,sg,L,A,box,l,witness)
    return {'axis':axis,'sign':sg,'nodes':nodes,'closed_leaves':len(record['leaves']),
        'max_depth':max(len(row[0]) for row in record['leaves']),
        'strict_positive_linear_and_quadratic_coefficients':coefficient_count,
        'coefficient_sha256':hashes.hexdigest(),'original_face_polynomial_audits':face_audits,
        'leaf_direct_vector_and_Bernstein_audits':direct_audits}

def require(value):assert value

def receiver_geometry():
    cell=[C.N[j] for j in C.P['cell_certificates'][9]['corner_indices']]
    assert C.area_twice(TRI).sign()!=0 and all(C.weak_inside(u,cell) for u in TRI)
    previous=C.triangle(F(3,4));assert all(C.weak_inside(u,TRI) for u in previous)
    assert C.area_twice(TRI)==F(16,9)*C.area_twice(previous)
    weights=[F(1,10),F(1,15),F(5,6)];assert sum(weights)==1 and min(weights)>0
    witness=H.vec(sum((weights[j]*TRI[j][k] for j in range(3)),ZERO) for k in range(3))
    sign=C.area_twice(TRI).sign()
    assert all((H.cross(H.sub(b,a),H.sub(witness,a))[2]*sign).sign()>0 for a,b in zip(TRI,TRI[1:]+TRI[:1]))
    def ray(j,t):return H.add(C.M,H.mul(t,H.sub(C.N[j],C.M)))
    old=[[C.M,ray(3,F(1,8)),ray(4,F(1,4))],
         [C.M,ray(4,F(1,4)),C.N[7]],[C.M,C.N[7],C.N[8]],
         [C.M,C.N[8],ray(10,F(1,6))],C.triangle(F(2,5)),
         C.triangle(F(1,2)),C.triangle(F(2,3)),previous]
    images=C.orbit(witness);assert len(images)==60
    for u in images:
        for a,b,c in old:
            det=C.determinant(a,b,c);assert det.sign()!=0
            coordinates=[C.determinant(u,b,c)/det,C.determinant(a,u,c)/det,C.determinant(a,b,u)/det]
            assert not(all(x.sign()>=0 for x in coordinates) or all(x.sign()<=0 for x in coordinates))
    centers=C.orbit(C.M);assert len(centers)==30;cosine=1-F(1,50)**2/2
    for v in centers:assert (Q(cosine*cosine)*H.dot(witness,witness)*H.dot(v,v)-H.dot(witness,v)**2).sign()>0
    return {'whole_D1_in_actual_closed_cell9':True,'contains_entire_previous_D3_4':True,
        'unit_z_chart_area_ratio_over_previous':'16/9','spherical_area_ratio_claimed':False,
        'new_interior_receiver_witness':list(map(str,witness)),'witness_barycentric_weights':list(map(str,weights)),
        'projective_witness_orbit':60,'old_triangular_cones_per_image':8,
        'old_closed_cone_membership_tests':480,'witness_images_in_old_closed_regions':0,
        'minimum_projective_axes_checked':30,'witness_chord_from_all_signed_minimum_axes_lower':'1/50 > 1/64'}

def malformed_controls(records):
    rejected=[]
    def reject(name,job):
        try:job()
        except AssertionError:rejected.append(name)
        else:raise AssertionError('malformed evidence accepted: '+name)
    def modified(job):
        changed=copy.deepcopy(records);job(changed);return changed
    reject('missing closed axis face',lambda:validate_covers(records[:-1]))
    reject('duplicated closed axis face',lambda:validate_covers(modified(lambda r:r.__setitem__(1,copy.deepcopy(r[0])))))
    reject('missing axis sign',lambda:validate_covers(modified(lambda r:r[0].__setitem__('sign',1))))
    reject('missing closed axis leaf',lambda:validate_covers(modified(lambda r:r[0]['leaves'].pop())))
    reject('duplicate closed axis leaf',lambda:validate_covers(modified(lambda r:r[0]['leaves'].append(copy.deepcopy(r[0]['leaves'][0])))))
    reject('overlapping ancestor leaf',lambda:validate_covers(modified(lambda r:r[0]['leaves'].append(['',1,'1']))))
    reject('invalid subdivision digit',lambda:validate_covers(modified(lambda r:r[0]['leaves'][0].__setitem__(0,'4'))))
    reject('excess fixed-cover depth',lambda:validate_covers(modified(lambda r:r[0]['leaves'][0].__setitem__(0,'0000'))))
    reject('unknown original contact',lambda:validate_covers(modified(lambda r:r[0]['leaves'][0].__setitem__(1,12))))
    reject('false axis norm lower',lambda:validate_covers(modified(lambda r:r[0]['leaves'][0].__setitem__(2,'2'))))
    reject('wrong tensor mixed coefficient',lambda:bernstein_identity_audits(F(1,2)))
    a,b,j=H.CONTACTS[1];mu=H.cross(H.sub(V[a],V[b]),TRI[2])
    reject('reversed original support',lambda:require(all(H.dot(mu,H.sub(V[j],v)).sign()>=0 for v in V)))
    reject('false Cayley radius1/10',lambda:require(F(1,10)*(1-THETA*THETA/8)-THETA/2>0))
    reject('nonstrict first coefficient',lambda:require(all(q.sign()>0 for q in [Q(1),ZERO])))
    mu=H.cross(H.sub(V[b],V[a]),TRI[2]);w=H.vec((F(1,10),F(2,25),F(-1,20)))
    signed=H.dot(w,V[j])*H.dot(w,mu)-H.dot(mu,V[j])*H.dot(w,w)
    reject('discarded signed Cayley quadratic',lambda:require(signed==ZERO))
    return rejected

def check(records):
    checked=pins();validate_covers(records)
    with C.audit_signs() as audit:
        theta,phase=C.phase(F(1));assert theta==THETA
        assert phase==C.fixture()['prerequisites']['full_D1_phase']
        geometry=receiver_geometry()
        contacts,pre=prerequisites();basis=bernstein_identity_audits()
        faces=[replay_face(contacts,row) for row in records]
        controls=malformed_controls(records)
    assert sum(r['closed_leaves'] for r in faces)==57
    assert sum(r['strict_positive_linear_and_quadratic_coefficients'] for r in faces)==2223
    return {'agent':'six-rupert-1','role':'researcher','global_Rupert_property':'OPEN',
        'status':'complete exact signed Cayley hypotheses on the entire closed D1',
        'cayley_radius_upper':str(R),'inherited_full_angle_upper':str(THETA),
        'whole_D1_phase_all_expected_fields_matched':True,'inherited_phase_sha256':H.digest(phase),
        'global_area_and_sharp_source_proofs':'inherited and byte-pinned; not re-enumerated by this checker',
        'receiver_rays':[list(map(str,u)) for u in TRI],
        'receiver_geometry':geometry,
        'fixed_original_contact_ids':CANDIDATES,'pins':checked,'cayley_identity_and_support_audits':pre,
        'tensor_Bernstein_basis_polynomial_identities':basis,'axis_faces':faces,
        'closed_axis_leaf_count':57,'strict_positive_coefficient_count':2223,
        'fixed_cover_case_sha256':H.digest(records),'independent_Q5_sign_audits':audit,
        'malformed_controls_rejected':controls}

if __name__=='__main__':
    started=time.monotonic();saved=fixture();assert set(saved)=={'fixed_axis_covers','expected'}
    actual=check(saved['fixed_axis_covers'])
    assert json.loads(json.dumps(actual))==saved['expected'],'every expected mathematical field must match'
    print(json.dumps({'all_expected_fields_match':True,'global_Rupert_property':'OPEN',
        'closed_axis_leaves':actual['closed_axis_leaf_count'],'strict_positive_coefficients':actual['strict_positive_coefficient_count'],
        'malformed_controls_rejected':len(actual['malformed_controls_rejected']),
        'elapsed_seconds':time.monotonic()-started,'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))
