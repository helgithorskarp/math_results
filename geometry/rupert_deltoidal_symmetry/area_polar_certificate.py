"""Exact deltoidal projection-area body and a global small-excess source bound.

Python3.11+ standard library, exact Q(sqrt5)/Fraction proof predicates.
See area_polar_proof.md; every field matches expected_area_polar.json.
"""
import argparse, json, hashlib, re
from pathlib import Path
from fractions import Fraction as F
from collections import deque
from math import isqrt
from contextlib import contextmanager
if not __debug__:
    raise RuntimeError('verification requires assertions; do not use python -O')
from global_area_certificate import mm,mv,transpose,reflection,I,WALLS,QMIN
from global_area_certificate import check as check_parent, root_gap_greater
from stable_certificate import canonical_ray
from orientation_certificate import determinant
from verify import Q5,ZERO,vec,dot,cross,sub,add,mul,vertices,convex_hull_2d
ROOT=Path(__file__).parent
PINS={'verify.py': 'e23592cbd492df323add8b6c3ab80d2084c0c9f9cf3f11b05b1d9c05d42d5f52', 'local_certificate.py': 'd958dd248f97147267c8733f199b8b050e0b28b94aa679cdbe92ea7bc31b094b', 'orientation_certificate.py': '2e750e95edac9380016aa1c71886d0e7034cc1913c0e69fee37c9d53289ed012', 'stable_certificate.py': '21c6c255d851e7375d5a82cf8d5d521f62e12fbb7fe0445e1ca7d520bfdb2a1d', 'stable_data.py': '82e9b2d6826a34f2bbb670cfaba07a65ca51c0e341392dae04e0aa151d81f38a', 'global_area_certificate.py': '9006644d9e2623648e7c0905c5f9a9f691021d53e6e39286d097a512d2af75d2', 'expected_global_area.json': '22196b0e3e6449841ac3686cc518aa51d354d41e743ff7599c77f1b6ff39dd32'}

def parse(s):
    match=re.fullmatch(r'\(([^()]+)\) \+ \(([^()]+)\)\*sqrt\(5\)',s)
    assert match is not None, 'malformed field encoding'
    return Q5(F(match[1]),F(match[2]))

def pins():
    for name,expected in PINS.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected, name
    return dict(PINS)

def verify_formula(Bs,Cs,N,cells,denominator=2):
    assert len(Bs)==30 and len(set(Bs))==30
    assert len(N)==14 and len(Cs)==len(cells)==12
    assert [r['cell'] for r in cells]==list(range(12))
    comparisons=0
    for ci,cell in enumerate(cells):
        u=[N[i] for i in cell['corner_indices']]
        C=vec((0,0,0))
        for b in Bs:
            dots=[dot(b,x) for x in u]
            sgn=next(d.sign() for d in dots if d.sign())
            assert all(d.sign() in (0,sgn) for d in dots)
            C=add(C,mul(F(sgn,denominator),b));comparisons+=len(dots)
        assert C==Cs[ci], ('incorrect physical area gradient',ci)
    return comparisons

def verify_pair(Bs,i,j,polar_vertices,u=None,denominator=2):
    assert 0<=j<i<len(Bs)
    raw=cross(Bs[i],Bs[j]);assert dot(raw,raw).sign()>0
    if u is None:u=canonical_ray(raw)
    assert u==canonical_ray(raw)
    dots=[dot(x,u) for x in Bs]
    assert [t for t,d in enumerate(dots) if d==ZERO]==[j,i]
    H=sum((d if d.sign()>=0 else -d for d in dots),ZERO)/denominator
    assert H.sign()>0
    p=mul(1/H,u)
    assert p in polar_vertices and mul(-1,p) in polar_vertices
    q=H*H/dot(u,u);assert dot(p,p)==1/q
    return H,p,q

def verify_source_constants(rho2,eta=F(1,1000),alpha=F(3,250),
                            radius=F(63,100),rate=F(15,8),radical_lower=F(9999,10000)):
    assert 0<eta<=F(1,100) and alpha>0 and rate>0 and radius>0
    QSECOND=(236425+105595*Q5(0,1))/2178
    root_gap_greater(QSECOND,QMIN,F(1,100))
    assert QMIN>Q5(14**2) and QMIN<Q5(15**2)
    assert rho2>Q5(radius*radius)
    coarse=1-alpha*alpha/2
    assert 0<coarse<1
    assert (1-coarse)**2*QMIN>Q5(coarse*coarse*eta*eta)
    assert radical_lower**2<1-alpha*alpha/4
    assert radical_lower>0
    linear_lower=radius*radical_lower-15*alpha/2
    assert linear_lower>1/rate
    return linear_lower

def reject(name,job,records):
    try:job()
    except (AssertionError,StopIteration):records.append(name)
    else:raise AssertionError('malformed certificate accepted: '+name)

def negative_controls(Bs,Cs,N,cells,polar_vertices,rho2,center_offset):
    records=[]
    reject('missing area generator',lambda:verify_formula(Bs[:-1],Cs,N,cells),records)
    reject('duplicate area generator',lambda:verify_formula(Bs[:-1]+[Bs[0]],Cs,N,cells),records)
    reject('missing closed area cell',lambda:verify_formula(Bs,Cs,N,cells[:-1]),records)
    reject('false physical-area factor',lambda:verify_formula(Bs,Cs,N,cells,3),records)
    false=Cs.copy();false[0]=add(false[0],vec((1,0,0)))
    reject('false area gradient',lambda:verify_formula(Bs,false,N,cells),records)
    false=Bs.copy();false[1]=false[0]
    reject('parallel generator pair',lambda:verify_pair(false,1,0,polar_vertices),records)
    false=Bs.copy();false[2]=add(false[0],false[1])
    reject('third coplanar generator',lambda:verify_pair(false,1,0,polar_vertices),records)
    reject('false pair support height',lambda:verify_pair(Bs,1,0,polar_vertices,denominator=3),records)
    reject('missing polar vertex set',lambda:verify_pair(Bs,1,0,set()),records)
    reject('unsupported area excess',lambda:verify_source_constants(rho2,eta=F(1,10)),records)
    reject('false coarse source chord',lambda:verify_source_constants(rho2,alpha=F(1,100)),records)
    reject('unsupported tangent radius',lambda:verify_source_constants(rho2,radius=F(2,3)),records)
    reject('unsupported linear source rate',lambda:verify_source_constants(rho2,rate=F(3,2)),records)
    def false_center():
        assert center_offset==vec((0,0,0)), 'minimum facet is not centered at A0*m'
    reject('false minimum-facet centering',false_center,records)
    return records

@contextmanager
def audit_signs():
    """Independently enclose sqrt5 for every executed Q5 sign decision.

    The original kernel still decides each sign. This temporary wrapper only
    audits it; it restores the class method on every exit, and changes no
    geometric input, mathematical guard, source bytes or resource setting.
    """
    original=Q5.sign;cache={};record={'sign_calls':0,'distinct_enclosure_audits':0,
                                  'maximum_decimal_enclosure_digits':0}
    def checked(q):
        record['sign_calls']+=1;actual=original(q)
        if q not in cache:
            if q==ZERO:verified=0;digits=0
            else:
                digits=8
                while True:
                    assert digits<=256, 'independent sign enclosure unresolved'
                    scale=10**digits;root=isqrt(5*scale*scale)
                    lo,hi=F(root,scale),F(root+1,scale)
                    assert lo*lo<5<hi*hi
                    lower=q.a+q.b*(lo if q.b>=0 else hi)
                    upper=q.a+q.b*(hi if q.b>=0 else lo)
                    if lower>0:verified=1;break
                    if upper<0:verified=-1;break
                    digits*=2
            assert verified==actual, 'Q5 sign disagrees with rational enclosure'
            cache[q]=verified;record['distinct_enclosure_audits']+=1
            record['maximum_decimal_enclosure_digits']=max(record['maximum_decimal_enclosure_digits'],digits)
        assert cache[q]==actual
        return actual
    Q5.sign=checked
    try:yield record
    finally:Q5.sign=original

def check():
    pins()
    P=json.loads((ROOT/'expected_global_area.json').read_text())
    N=[vec(map(parse,r['ray'])) for r in P['corner_areas']]
    Cs=[vec(map(parse,r['area_vector'])) for r in P['cell_certificates']]
    walls=[reflection(w) for w in WALLS]
    generators=[mm(walls[0],walls[1]),mm(walls[1],walls[2])]
    group={I};queue=deque([I])
    while queue:
        g=queue.popleft()
        for a in generators:
            h=mm(a,g)
            if h not in group:group.add(h);queue.append(h);assert len(group)<=60
    assert len(group)==60
    V=set(vertices())
    assert all(mm(g,transpose(g))==I and determinant(*g)==Q5(1)
               and {mv(g,v) for v in V}==V for g in group)
    gradients=sorted({mul(s,mv(g,c)) for c in Cs for g in group for s in (-1,1)})
    assert set(gradients)=={mul(-1,c) for c in gradients}
    assert max(dot(c,c) for c in gradients)<Q5(16**2)
    T=F(14803427,1000000)
    reports=[]
    facets=[]
    for i,u in enumerate(N):
        vals=[dot(c,u) for c in gradients];height=max(vals);assert height.sign()>0
        face=[c for c,h in zip(gradients,vals) if h==height]
        differences=[sub(c,face[0]) for c in face[1:]]
        assert all(dot(x,u)==ZERO for x in differences)
        rank=0
        if any(dot(x,x).sign()>0 for x in differences):rank=1
        if any(dot(cross(x,y),cross(x,y)).sign()>0 for j,x in enumerate(differences)
               for y in differences[j+1:]):rank=2
        q=height*height/dot(u,u)
        assert q==parse(P['corner_areas'][i]['physical_area_squared'])
        rec={'corner':i,'exposed_gradient_count':len(face),'affine_rank':rank,
             'is_actual_facet':rank==2,'area_squared':str(q),'below_budget':q<=Q5(T*T),
             'active_gradient_indices':[gradients.index(c) for c in face]}
        reports.append(rec)
        if rank==2:facets.append((q,i))
    facets.sort()
    facet_polar_orbits=[];polar_vertices=set()
    for q,i in facets:
        u=N[i];h=max(dot(c,u) for c in gradients);p=mul(1/h,u)
        orbit={mul(s,mv(g,p)) for g in group for s in (-1,1)}
        assert not orbit&polar_vertices
        polar_vertices.update(orbit)
        assert all(dot(x,x)==1/q for x in orbit)
        facet_polar_orbits.append({'corner':i,'directed_orbit_size':len(orbit),
            'polar_vertex':list(map(str,p)),'norm_squared':str(1/q)})
    M=N[9];height=max(dot(c,M) for c in gradients)
    face=[c for c in gradients if dot(c,M)==height]
    anchor=mul(height/dot(M,M),M)
    translated=[sub(c,anchor) for c in face]
    assert all(dot(x,M)==ZERO for x in translated)
    e1=vec((-M[1],M[0],0));e2=cross(M,e1)
    xy={(dot(x,e1),dot(x,e2)):x for x in translated}
    hull=[xy[p] for p in convex_hull_2d(list(xy))]
    edges=[]
    for j,a in enumerate(hull):
        b=hull[(j+1)%len(hull)];edge=sub(b,a);normal=cross(M,edge)
        margins=[dot(normal,sub(x,a)) for x in hull]
        assert all(x.sign()>=0 for x in margins) and any(x.sign()>0 for x in margins)
        h=dot(normal,mul(-1,a))
        d2=h*h/dot(normal,normal)
        edges.append({'edge':[j,(j+1)%len(hull)],'origin_inward_margin':str(h),
                      'distance_squared':str(d2),'origin_strictly_inside':h.sign()>0})
    rho2=min(parse(r['distance_squared']) for r in edges)
    center=mul(F(1,len(face)),tuple(sum((x[j] for x in face),ZERO) for j in range(3)))
    center_offset=sub(center,anchor)
    assert len(hull)==4 and add(hull[0],hull[2])==add(hull[1],hull[3])
    seed=sub(hull[1],hull[0])
    raw_generators={mv(g,seed) for g in group}
    assert len(raw_generators)==60 and raw_generators=={mul(-1,b) for b in raw_generators}
    Bs=sorted({min(b,mul(-1,b)) for b in raw_generators})
    assert len(Bs)==30
    generator_sign_tests=verify_formula(Bs,Cs,N,P['cell_certificates'])
    pair_normals={};pair_comparisons=0
    for i,b in enumerate(Bs):
        for j in range(i):
            u=cross(b,Bs[j]);assert dot(u,u).sign()>0
            u=canonical_ray(u);assert u not in pair_normals
            H,p,q=verify_pair(Bs,i,j,polar_vertices,u=u)
            pair_normals[u]={'pair':[j,i],'squared_area':str(q)}
            pair_comparisons+=len(Bs)
    assert len(pair_normals)==435 and len(polar_vertices)==870
    assert {q for q,i in facets}=={parse(r['squared_area']) for r in pair_normals.values()}
    eta=F(1,1000);alpha=F(3,250);radical_lower=F(9999,10000)
    linear_lower=verify_source_constants(rho2)
    medium_slope=verify_source_constants(rho2,eta=F(1,100),alpha=F(19,500),
        rate=F(3),radical_lower=F(999,1000))
    out={'agent':'six-rupert-1','role':'researcher',
         'status':'complete exact finite hypotheses; written unformalized area-body and global source proof',
         'proper_group_size':len(group),'gradient_count':len(gradients),
         'gradient_sha256':hashlib.sha256(json.dumps([list(map(str,c)) for c in gradients],separators=(',',':')).encode()).hexdigest(),
         'corner_faces':reports,'actual_facet_chamber_corners':[i for q,i in facets],
         'minimum_actual_facet_squared_area':str(facets[0][0]),
         'next_actual_facet_squared_area':str(next(q for q,i in facets if q!=QMIN)),
         'facet_polar_orbits':facet_polar_orbits,'complete_polar_vertex_count':len(polar_vertices),
         'generator_count':len(Bs),'generator_norm_squared':str(dot(seed,seed)),
         'generator_sha256':hashlib.sha256(json.dumps([list(map(str,b)) for b in Bs],separators=(',',':')).encode()).hexdigest(),
         'whole_cell_generator_sign_comparisons':generator_sign_tests,
         'distinct_projective_generator_pair_normals':len(pair_normals),
         'pair_zero_sign_comparisons':pair_comparisons,
         'pair_record_sha256':hashlib.sha256(json.dumps([{'normal':list(map(str,u)),**rec} for u,rec in sorted(pair_normals.items())],separators=(',',':')).encode()).hexdigest(),
         'area_budget':str(T),'minimum_facet_height':str(height),
         'minimum_facet_anchor':list(map(str,anchor)),
         'minimum_facet_vertex_count':len(face),'minimum_facet_hull_count':len(hull),
         'minimum_facet_translated_hull':[list(map(str,x)) for x in hull],
         'minimum_facet_edge_records':edges,
         'minimum_translated_inradius_squared':str(rho2),
         'minimum_facet_center_offset':list(map(str,center_offset)),
         'minimum_facet_center_offset_squared':str(dot(center_offset,center_offset)),
         'centered_disk_valid':all(r['origin_strictly_inside'] for r in edges),
         'small_excess_global_source_bound':{'maximum_eta':str(eta),
              'coarse_chord_upper':str(alpha),'tangent_radius_lower':'63/100',
              'radical_lower':str(radical_lower),'area_slope_strict_lower':str(linear_lower),
              'source_chord_per_eta':'15/8'},
         'medium_excess_global_source_bound':{'maximum_eta':'1/100',
              'coarse_chord_upper':'19/500','tangent_radius_lower':'63/100',
              'radical_lower':'999/1000','area_slope_strict_lower':str(medium_slope),
              'source_chord_per_eta':'3'},
         'receiving_cap_necessary_bounds':{'positive_chord_budget_upper':'1/16000',
              'global_source_chord_per_receiver_chord':'30',
              'scale_squared_excess_per_receiver_chord':'8/7',
              'full_spatial_angle_or_roll_bound':False},
         'larger_receiving_cap_necessary_bounds':{'positive_chord_budget_upper':'1/1600',
              'global_source_chord_per_receiver_chord':'48',
              'scale_squared_excess_per_receiver_chord':'8/7',
              'full_spatial_angle_or_roll_bound':False},
         'global_Rupert_property':'OPEN'}
    out['malformed_controls_rejected']=negative_controls(Bs,Cs,N,P['cell_certificates'],polar_vertices,rho2,center_offset)
    return out


def prerequisites():
    checked=pins();expected=json.loads((ROOT/'expected_global_area.json').read_text())
    expected.pop('malformed_controls_rejected',None)
    actual=check_parent();assert actual==expected
    return {'agent':'six-rupert-1','role':'researcher','all_parent_fields_matched':True,
            'parent_support_comparisons':actual['whole_cell_support_comparisons'],
            'parent_physical_area_checks':actual['shoelace_Jacobian_area_comparisons'],
            'pins':checked}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prerequisites',action='store_true')
    args=parser.parse_args()
    if args.prerequisites:
        result=prerequisites()
    else:
        with audit_signs() as audit:result=check()
        result['independent_sign_audits']=audit
        expected=json.loads((ROOT/'expected_area_polar.json').read_text())
        assert result==expected, 'complete expected output mismatch'
    print(json.dumps(result,indent=2))
