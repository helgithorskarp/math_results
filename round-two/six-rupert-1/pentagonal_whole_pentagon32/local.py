#!/usr/bin/env python3
"""Rebuild the actual solid and certify one complete closed receiving cell.

Standard library only. Every mathematical guard is active under Python -O.
A timeout, undecided sign or failed certificate yields no theorem.
"""
import os
for _key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
             'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[_key]='1'
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,resource,time
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'round-two/six-rupert-1/pentagonal_closed_horizon_cell'))
import geometry as H
import polynomial as E
B=E.B
HERE=Path(__file__).resolve().parent

def decode(encoded):
    H.require(len(encoded)==3 and all(len(q)==2 and all(type(s)==str for s in q)for q in encoded),'literal cubic-field coefficient encoding')
    return H.K(tuple(H.V.Q(a,b)for a,b in encoded))

def turn(a,b,c):return (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])

def prepare(certificate,data,deadline):
    H.require(certificate['schema']=='pentagonal-closed-horizon-cell-v5-pentagon-fan','certificate schema')
    H.require(type(certificate['remainder_constant'])==int and certificate['remainder_constant']==4,'stated quadratic remainder constant')
    H.require(certificate['named_model_source_commit']=='86ab225fb8becbe66601a5da0b5b017e872e1833','published actual named-model premise')
    points,normals,root=data['points'],data['normals'],data['root']
    phase=certificate['facet_signs'];polygon=[tuple(decode(z)for z in p)for p in certificate['polygon']]
    H.require(len(phase)==60 and all(type(s)==int and s in(-1,1)for s in phase),'complete sixty-facet phase')
    H.require(len(polygon)==5 and all(len(p)==2 for p in polygon),'five complete closed-cell vertices')
    target_raw=(HERE/'target.json').read_bytes()
    config=json.loads((HERE/'configuration.json').read_text())
    H.require(hashlib.sha256(target_raw).hexdigest()==config['target_sha256'],'frozen literal whole pentagon target')
    target=json.loads(target_raw)
    H.require(certificate['polygon']==target['exact_polygon'] and phase==target['exact_facet_signs'],'literal frozen whole pentagon32 and actual sixty-facet sign inventory')
    constraints=[(H.Z,H.O,H.Z),(H.Z,H.Z,H.O),(H.O,-H.phi,-H.phi*H.phi)]
    constraints += [tuple(side*z for z in n)for side,n in zip(phase,normals)]
    comparisons=0
    for s,t in polygon:
        for c in constraints:
            H.require(H.sign(c[0]+c[1]*s+c[2]*t,root)>=0,'closed chamber/actual facet-phase inequality')
            comparisons+=1
    walls=[]
    for edge,(a,b)in enumerate(zip(polygon,polygon[1:]+polygon[:1])):
        for j,c in enumerate(polygon):
            if j not in(edge,(edge+1)%len(polygon)):
                H.require(H.sign(turn(a,b,c),root)>0,'every other vertex is strictly left of every polygon side')
        wall=[i for i,c in enumerate(constraints)
              if c[0]+c[1]*a[0]+c[2]*a[1]==H.Z and c[0]+c[1]*b[0]+c[2]*b[1]==H.Z]
        H.require(bool(wall),'every polygon side is a genuine defining halfspace wall')
        walls.append(wall)
    H.require(walls==[[12],[62],[13],[55],[61]],'five true original closed pentagon32 walls')
    centroid=tuple(sum((p[d]for p in polygon),H.Z)/len(polygon)for d in range(2))
    twice_area=sum((a[0]*b[1]-a[1]*b[0]for a,b in zip(polygon,polygon[1:]+polygon[:1])),H.Z)
    H.require(H.sign(twice_area,root)>0,'strictly positive exact raw cell area')
    depth=certificate['receiver_depth'];H.require(type(depth)==int and 0<=depth<=2,'zero, one or two complete midpoint refinements of all three closed fan triangles')
    paths=['0','1','2']
    for _ in range(depth):paths=[p+str(j)for p in paths for j in range(4)]
    H.require([(d['receiver_path'],d['coordinate'],d['sign'])for d in certificate['duals']]==[(p,j,s)for p in paths for j in range(3)for s in(-1,1)],'every closed receiver piece has all six signed rotation-coordinate duals, once')
    contacts=[c for dual in certificate['duals']for c in dual['contacts']]
    for contact in contacts:
        H.require(len(contact)==4 and all(type(v)==int for v in contact),'literal dyadic endpoint contact')
        a,b,v,k=contact
        H.require(0<=a<92 and 0<=b<92 and a!=b and v in(a,b)and -12<=k<=12,'actual endpoint indices and dyadic scale')
    p2=max(sum(z.interval(root).square().hi for z in p)for p in points)
    unique=sorted(set(map(tuple,contacts)));edges=sorted({(a,b,k)for a,b,v,k in unique})
    support_rows={};support_count=0;ties=0;offendpoint_ties=0;tie_example=None;m2=F(0);height_lower=None
    for a,b,k in edges:
        d=H.M.sub(points[b],points[a]);gamma=F(2)**k
        for vertex,(s,t)in enumerate(polygon):
            if time.monotonic()>=deadline:raise TimeoutError('exact original support deadline incomplete')
            r=(H.O,s,t);m=tuple(gamma*z for z in H.M.cross(d,r));h=H.M.dot(m,points[a])
            H.require(H.M.dot(m,r)==H.Z and H.M.dot(m,d)==H.Z,'exact perpendicular and endpoint identities')
            H.require(H.sign(h,root)>0,'positive actual support height even at every closed boundary')
            hlo=h.interval(root).lo;height_lower=hlo if height_lower is None else min(height_lower,hlo)
            m2=max(m2,sum(z.interval(root).square().hi for z in m))
            for index,p in enumerate(points):
                gap=h-H.M.dot(m,p);direction=H.sign(gap,root)
                H.require(direction>=0,'every actual original lies in every closed-vertex support halfspace')
                support_count+=1;ties+=(direction==0)
                if direction==0 and index not in(a,b):
                    offendpoint_ties+=1
                    if tie_example is None:tie_example=dict(edge=[a,b],exponent=k,polygon_vertex=vertex,original=index)
    basis=[tuple(H.O if i==j else H.Z for i in range(3))for j in range(3)]
    for a,b,v,k in unique:
        d=H.M.sub(points[b],points[a]);values=[]
        for raw in basis:
            m=tuple((F(2)**k)*z for z in H.M.cross(d,raw))
            values.append(tuple(H.M.cross(points[v],m))+(m[1],m[2]))
        support_rows[(a,b,v,k)]=[tuple(B.interval(values[j][i].interval(root))for j in range(3))for i in range(5)]
    H.require(4*p2*m2<16 and m2<4,'uniform remainder strictly below4 and physical support norm below2')
    triangles,centers=receiver_pieces(polygon,depth,root)
    record_pieces=[dict(path=p,vertices=[[H.encode(z)for z in v]for v in triangle])for p,triangle in exact_receiver_pieces(polygon,depth).items()]
    record=dict(closed_cell_halfspace_vertex_checks=comparisons,exact_polygon_edge_wall_indices=walls,
                exact_raw_chart_area=H.encode(twice_area/2),distinct_contact_rows=len(unique),
                distinct_directed_support_edges=len(edges),closed_support_original_comparisons=support_count,
                exact_closed_support_ties=ties,exact_offendpoint_grazing_ties=offendpoint_ties,grazing_tie_example=tie_example,
                actual_original_squared_norm_upper=str(p2),actual_support_squared_norm_upper=str(m2),
                actual_support_height_lower=str(height_lower),uniform_cayley_polynomial_remainder_constant=4,
                actual_translation='b=pi_r(alpha*e_y+beta*e_z), r_x=1; wrench translation entries are m_y,m_z',
                facet_phase=''.join('+'if s>0 else '-'for s in phase))
    record.update(closed_midpoint_receiver_piece_count=len(triangles),closed_receiver_refinement_depth=depth,closed_receiver_fan_triangle_indices=[[0,1,2],[0,2,3],[0,3,4]],receiver_exact_pieces=record_pieces)
    return support_rows,triangles,centers,root,record

def certify_dual(dual,rows,triangles,centroid,root,deadline):
    coordinate,sign,contacts=dual['coordinate'],dual['sign'],dual['contacts']
    H.require(type(coordinate)==type(sign)==int and coordinate in(0,1,2)and sign in(-1,1),'signed rotation target')
    H.require(len(contacts)==5 and len(set(map(tuple,contacts)))==5,'five distinct rows')
    columns=[rows[tuple(c)]for c in contacts];center=[B.interval(z.interval(root))for z in centroid]
    A0=[[{(0,0):c[0]+c[1]*center[0]+c[2]*center[1]}for c in [col[i]for col in columns]]for i in range(5)]
    reference=E.determinant(A0,deadline).get((0,0),E.ZERO)
    H.require(reference.lo>0 or reference.hi<0,'strict reference determinant sign')
    orientation=1 if reference.lo>0 else -1;records=[];constant=F(0)
    for tno,triangle in enumerate(triangles):
        A=[[E.affine_triangle(col[i],triangle)for col in columns]for i in range(5)]
        determinant=E.determinant(A,deadline)
        if orientation<0:determinant=E.neg(determinant)
        denominator=E.bernstein(determinant,5)
        H.require(min(z.lo for z in denominator)>0,'every denominator Bernstein coefficient is strictly positive')
        numerators=[]
        for j in range(5):
            replaced=[[({(0,0):E.ONE.ratio(sign)}if i==coordinate else {})if k==j else A[i][k]
                       for k in range(5)]for i in range(5)]
            numerator=E.determinant(replaced,deadline)
            if orientation<0:numerator=E.neg(numerator)
            bc=E.bernstein(numerator,5)
            H.require(min(z.lo for z in bc)>0,'every Cramer numerator Bernstein coefficient is strictly positive')
            numerators.append(bc)
        coefficient_sums=[sum((numerators[j][i]for j in range(5)),E.ZERO)for i in range(21)]
        upper=max(F(n.hi,d.lo)for n,d in zip(coefficient_sums,denominator));constant=max(constant,upper)
        records.append(dict(triangle=tno,explicit_closed_piece=True,
                            denominator_degree5_integer_intervals=[[z.lo,z.hi]for z in denominator],
                            cramer_degree5_integer_intervals=[[[z.lo,z.hi]for z in bc]for bc in numerators],
                            determinant_bernstein_bounds=[str(F(min(z.lo for z in denominator),E.SCALE)),str(F(max(z.hi for z in denominator),E.SCALE))],
                            numerator_bernstein_bounds=[[str(F(min(z.lo for z in bc),E.SCALE)),str(F(max(z.hi for z in bc),E.SCALE))]for bc in numerators],
                            common_degree5_coefficients=21,dual_weight_sum_upper=str(upper)))
    return dict(coordinate=coordinate,sign=sign,contacts=contacts,common_determinant_orientation=orientation,
                triangle_records=records,uniform_weight_sum_upper=str(constant))


def exact_receiver_pieces(polygon,depth):
    H.require(len(polygon)==5,'three fan triangles require five cyclic vertices')
    pieces={str(j):[polygon[0],polygon[j+1],polygon[j+2]]for j in range(3)}
    for _ in range(depth):
        following={}
        for path,(a,b,c)in pieces.items():
            ab=tuple((x+y)/2 for x,y in zip(a,b));bc=tuple((x+y)/2 for x,y in zip(b,c));ca=tuple((x+y)/2 for x,y in zip(c,a))
            for j,triangle in enumerate(((a,ab,ca),(ab,b,bc),(ca,bc,c),(ab,bc,ca))):following[path+str(j)]=list(triangle)
        pieces=following
    return pieces

def receiver_pieces(polygon,depth,root):
    actual=exact_receiver_pieces(polygon,depth)
    triangles={p:[[B.interval(z.interval(root))for z in v]for v in tri]for p,tri in actual.items()}
    centers={p:tuple(sum((v[j]for v in tri),H.Z)/3 for j in range(2))for p,tri in actual.items()}
    return triangles,centers

def close_bounds(certificate,duals):
    encoded=certificate['coordinate_mass_bounds'];N=certificate['mass_euclidean_upper']
    H.require(len(encoded)==3 and all(type(z)in(int,str)for z in encoded),'three literal rational coordinate masses')
    masses=[F(z)for z in encoded]
    H.require(all(z>0 for z in masses),'three positive strict rational coordinate masses')
    for j in range(3):
        maximum=max(F(d['uniform_weight_sum_upper'])for d in duals if d['coordinate']==j)
        H.require(maximum<masses[j],'whole real receiver signed-coordinate dual mass strictly bounded')
    H.require(type(N)==int and N>0 and sum(m*m for m in masses)<N*N,'strict rational Euclidean mass upper')
    rho=F(certificate['closed_cayley_euclidean_radius']);gap=F(certificate['physical_gap_coefficient'])
    H.require(rho>0 and 2*N*rho<1,'closed Euclidean motion contraction2*N*rho<1')
    physical=(F(1,N)-2*rho)/(1+rho*rho)
    H.require(gap>0 and gap<physical,'positive physical support distance per Euclidean source motion')
    return dict(strict_coordinate_mass_bounds=list(map(str,masses)),mass_euclidean_strict_upper=N,closed_relative_cayley_euclidean_radius=str(rho),contraction_product=str(2*N*rho),squared_coordinate_closure_upper=str(4*sum(m*m for m in masses)*rho*rho),physical_support_gap_coefficient=str(gap),proved_physical_coefficient_lower=str(physical))

def compute(certificate,data,deadline):
    rows,triangles,centers,root,record=prepare(certificate,data,deadline)
    duals=[]
    for d in certificate['duals']:
        p=d['receiver_path'];z=certify_dual(d,rows,[triangles[p]],centers[p],root,deadline);z['receiver_path']=p;duals.append(z)
    closure=close_bounds(certificate,duals)
    return dict(actual_agent='six-rupert-1',role='researcher',status='EXACT_WHOLE_CLOSED_CELL32_CONDITIONAL_THREE_FAN_LOCAL_RIGIDITY_AND_PHYSICAL_GAP_PASSED',complete_named_geometry_record=data['record'],closed_cell_geometry=record,duals=duals,**closure,fixedpoint_outward_denominator=str(E.SCALE),certificate_sha256=hashlib.sha256(json.dumps(certificate,sort_keys=True).encode()).hexdigest(),mathematical_scope='ENTIRE CLOSED receiving pentagon32 includes all five sides and vertices, and all three full closed fan triangles. Source already in the stated proper-body Euclidean Cayley collar; arbitrary original physical translation and scale>=1 retained. All-source/global status open.')

def verified_cache(raw,expected_sha):
    H.require(hashlib.sha256(raw).hexdigest()==expected_sha,'whole completed fresh named-model cache fingerprint')
    cache=json.loads(raw)
    H.require(len(cache['exact_original_points'])==92 and len(cache['outward_facet_normals'])==60,'all actual points and facet normals in linked cache')
    return dict(root=H.V.I(*[F(q)for q in cache['root_interval']]),
                points=[tuple(decode(z)for z in p)for p in cache['exact_original_points']],
                normals=[tuple(decode(z)for z in p)for p in cache['outward_facet_normals']],record=cache['record'])

def main():
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'local_certificate.json');p.add_argument('--configuration',type=Path,default=HERE/'configuration.json');p.add_argument('--seconds',type=float,default=45.);p.add_argument('--output',type=Path);p.add_argument('--compare',type=Path);p.add_argument('--geometry-output',type=Path,default=HERE/'.generated/named_geometry.json')
    mode=p.add_mutually_exclusive_group();mode.add_argument('--model-only',action='store_true');mode.add_argument('--from-fresh-cache',type=Path)
    args=p.parse_args();started=time.monotonic();deadline=started+args.seconds
    args.geometry_output.parent.mkdir(parents=True,exist_ok=True)
    config=json.loads(args.configuration.read_text())
    dependency=ROOT/'round-two/six-rupert-1/pentagonal_closed_horizon_cell'
    for name,pin in config['local_dependency_pins'].items():H.require(hashlib.sha256((dependency/name).read_bytes()).hexdigest()==pin,'pinned exact model and polynomial source')
    if args.from_fresh_cache:
        data=verified_cache(args.from_fresh_cache.read_bytes(),config['expected_fresh_named_geometry_sha256'])
    else:
        data=H.build(deadline)
        cache=dict(root_interval=[str(data['root'].lo),str(data['root'].hi)],exact_original_points=[[H.encode(z)for z in v]for v in data['points']],outward_facet_normals=[[H.encode(z)for z in v]for v in data['normals']],record=data['record'])
        cache_raw=(json.dumps(cache,indent=2,sort_keys=True)+'\n').encode()
        H.require(hashlib.sha256(cache_raw).hexdigest()==config['expected_fresh_named_geometry_sha256'],'freshly rebuilt whole named geometry matches linked data')
        H.require(time.monotonic()<deadline,'whole model reconstruction finished inside its declared guard')
        args.geometry_output.write_bytes(cache_raw)
    if args.model_only:
        record=dict(actual_agent='six-rupert-1',role='researcher',status='COMPLETE_FRESH_ACTUAL_NAMED_MODEL_RECONSTRUCTION_PASSED',whole_cache_sha256=config['expected_fresh_named_geometry_sha256'],complete_named_geometry_record=data['record'])
    else:
        certificate=json.loads(args.certificate.read_text());record=compute(certificate,data,deadline)
    H.require(time.monotonic()<deadline,'complete declared stage finished inside its guard')
    raw=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
    if args.compare:H.require(raw==args.compare.read_bytes(),'entire ordinary/optimized mathematical record agrees')
    if args.output:args.output.write_bytes(raw)
    print(json.dumps(dict(status=record['status'],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),elapsed_seconds=time.monotonic()-started,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,threads=1)))

if __name__=='__main__':main()
