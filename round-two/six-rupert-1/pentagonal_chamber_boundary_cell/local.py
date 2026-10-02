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
    H.require(certificate['schema']=='pentagonal-closed-horizon-cell-v2-triangle','certificate schema')
    H.require(type(certificate['remainder_constant'])==int and certificate['remainder_constant']==4,'stated quadratic remainder constant')
    H.require(certificate['named_model_source_commit']=='86ab225fb8becbe66601a5da0b5b017e872e1833','published actual named-model premise')
    points,normals,root=data['points'],data['normals'],data['root']
    phase=certificate['facet_signs'];polygon=[tuple(decode(z)for z in p)for p in certificate['polygon']]
    H.require(len(phase)==60 and all(type(s)==int and s in(-1,1)for s in phase),'complete sixty-facet phase')
    H.require(len(polygon)==3 and all(len(p)==2 for p in polygon),'three complete closed-cell vertices')
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
    centroid=tuple(sum((p[d]for p in polygon),H.Z)/len(polygon)for d in range(2))
    twice_area=sum((a[0]*b[1]-a[1]*b[0]for a,b in zip(polygon,polygon[1:]+polygon[:1])),H.Z)
    H.require(H.sign(twice_area,root)>0,'strictly positive exact raw cell area')
    H.require([(d['coordinate'],d['sign'])for d in certificate['duals']]==[(j,s)for j in range(3)for s in(-1,1)],'all six distinct signed rotation-coordinate duals')
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
    polygon_bounds=[[B.interval(z.interval(root))for z in p]for p in polygon]
    triangles=[[polygon_bounds[0],polygon_bounds[i],polygon_bounds[i+1]]for i in range(1,len(polygon)-1)]
    record=dict(closed_cell_halfspace_vertex_checks=comparisons,exact_polygon_edge_wall_indices=walls,
                exact_raw_chart_area=H.encode(twice_area/2),distinct_contact_rows=len(unique),
                distinct_directed_support_edges=len(edges),closed_support_original_comparisons=support_count,
                exact_closed_support_ties=ties,exact_offendpoint_grazing_ties=offendpoint_ties,grazing_tie_example=tie_example,
                actual_original_squared_norm_upper=str(p2),actual_support_squared_norm_upper=str(m2),
                actual_support_height_lower=str(height_lower),uniform_cayley_polynomial_remainder_constant=4,
                actual_translation='b=pi_r(alpha*e_y+beta*e_z), r_x=1; wrench translation entries are m_y,m_z',
                facet_phase=''.join('+'if s>0 else '-'for s in phase))
    return support_rows,triangles,centroid,root,record

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
        records.append(dict(triangle=tno,vertex_indices=[0,tno+1,tno+2],
                            determinant_bernstein_bounds=[str(F(min(z.lo for z in denominator),E.SCALE)),str(F(max(z.hi for z in denominator),E.SCALE))],
                            numerator_bernstein_bounds=[[str(F(min(z.lo for z in bc),E.SCALE)),str(F(max(z.hi for z in bc),E.SCALE))]for bc in numerators],
                            common_degree5_coefficients=21,dual_weight_sum_upper=str(upper)))
    return dict(coordinate=coordinate,sign=sign,contacts=contacts,common_determinant_orientation=orientation,
                triangle_records=records,uniform_weight_sum_upper=str(constant))

def close_bounds(certificate,dual_constant):
    mass=certificate['dual_sum_bound']
    H.require(type(mass)==int and mass>0 and dual_constant<mass,'strict uniform dual mass below chosen exact integer bound')
    eta=F(certificate['closed_cayley_infinity_radius']);gap=F(certificate['physical_gap_coefficient'])
    H.require(eta>0 and 6*mass*eta<1,'closed motion contraction6*mass*eta<1')
    physical=(2-12*mass*eta)/(2*mass*(1+3*eta*eta))
    H.require(gap>0 and physical>gap,'physical support-distance bound, with actual support normal length')
    return dict(uniform_dual_weight_sum_upper=str(dual_constant),simple_dual_sum_bound=mass,
                closed_relative_cayley_infinity_radius=str(eta),contraction_product=str(6*mass*eta),
                physical_support_gap_coefficient=str(gap),proved_physical_coefficient_lower=str(physical))

def compute(certificate,data,deadline):
    rows,triangles,centroid,root,record=prepare(certificate,data,deadline)
    duals=[certify_dual(d,rows,triangles,centroid,root,deadline)for d in certificate['duals']]
    closure=close_bounds(certificate,max(F(d['uniform_weight_sum_upper'])for d in duals))
    return dict(actual_agent='six-rupert-1',role='researcher',
                status='EXACT_WHOLE_CLOSED_CELL13_CONDITIONAL_LOCAL_RIGIDITY_AND_PHYSICAL_GAP_PASSED',
                complete_named_geometry_record=data['record'],closed_cell_geometry=record,duals=duals,**closure,
                fixedpoint_outward_denominator=str(E.SCALE),certificate_sha256=hashlib.sha256(json.dumps(certificate,sort_keys=True).encode()).hexdigest(),
                mathematical_scope='Complete closed receiving facet-phase cell; relative source motion must already satisfy the stated proper-body Cayley bound. Actual translation is arbitrary and scale>=1. Global Rupert property remains open.')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--certificate',type=Path,default=HERE/'local_certificate.json');p.add_argument('--seconds',type=float,default=45.)
    p.add_argument('--geometry-output',type=Path,default=HERE/'.generated/named_geometry.json');p.add_argument('--output',type=Path);p.add_argument('--compare',type=Path)
    args=p.parse_args();started=time.monotonic();deadline=started+args.seconds
    certificate=json.loads(args.certificate.read_text());data=H.build(deadline)
    record=compute(certificate,data,deadline)
    cache=dict(root_interval=[str(data['root'].lo),str(data['root'].hi)],exact_original_points=[[H.encode(z)for z in p]for p in data['points']],outward_facet_normals=[[H.encode(z)for z in p]for p in data['normals']],record=data['record'])
    args.geometry_output.write_text(json.dumps(cache,indent=2,sort_keys=True)+'\n')
    raw=(json.dumps(record,sort_keys=True,indent=2)+'\n').encode()
    if args.compare:H.require(raw==args.compare.read_bytes(),'whole exact mathematical record agrees')
    if args.output:args.output.write_bytes(raw)
    print(json.dumps(dict(status=record['status'],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
                          elapsed_seconds=time.monotonic()-started,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                          actual_agent='six-rupert-1',role='researcher',threads=1)))

if __name__=='__main__':main()
