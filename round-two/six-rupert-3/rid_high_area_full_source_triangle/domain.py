"""Exact whole-triangle RID receiver prerequisites, polynomial Bernstein signs."""
from itertools import product
from math import factorial
from time import monotonic
import hashlib,json
from geometry import build,OUT,F,Q,Z,O,phi,dot,cross,sub,need,encode,dec


def triple_coefficients(product_value):
    # Exact degree-three simplex Bernstein coefficients from ordered products.
    polynomial={}
    for a,b,c in product(range(3),repeat=3):
        ex=tuple([a,b,c].count(i) for i in range(3))
        polynomial[ex]=polynomial.get(ex,Z)+product_value(a,b,c)
    return {ex:value/(factorial(3)//(factorial(ex[0])*factorial(ex[1])*factorial(ex[2])))
            for ex,value in sorted(polynomial.items())}


def make_domain(data,width=Q(1,100)):
    r=data['r'];R=[(r[0]-width,r[1]-width,O),(r[0]+width,r[1]-width,O),(r[0],r[1]+width,O)]
    V,Ns=data['V'],data['Ns'];old={'actual_supports':data['actual_supports'],'ring':data['ring']}
    supports=[];minimum_gap=None;minimum_norm=None
    for row,N in zip(old['actual_supports'],Ns):
        vi,vj=row['endpoints'];E=sub(V[vj],V[vi]);raw=[cross(E,x) for x in R];H=[dot(a,V[vi]) for a in raw]
        need(all(x>Z for x in H),'whole receiving triangle crosses an actual support-height zero')
        gaps=[dot(a,sub(V[vi],v)) for a in raw for k,v in enumerate(V) if k not in [vi,vj]]
        need(all(x>Z for x in gaps),'whole receiving triangle changes its actual endpoint support inventory')
        m=min(gaps);minimum_gap=m if minimum_gap is None else min(m,minimum_gap)
        # R_body*||N(r)||<5/4, via a homogeneous quadratic.
        polar=[F(Q(25,16))*H[i]*H[j]-(7+8*phi)*dot(raw[i],raw[j]) for i in range(3) for j in range(i,3)]
        need(all(x>Z for x in polar),'whole receiving quadratic polar norm bound5/4 fails')
        m=min(polar);minimum_norm=m if minimum_norm is None else min(m,minimum_norm)
        supports.append({'source_endpoints':[vi,vj],'E':E,'raw':raw,'H':H})
    # Positive ordered projected-area vector of the actual original ring.
    ring=old['ring'];S=tuple(sum((cross(V[i],V[j])[k]/2 for i,j in zip(ring,ring[1:]+ring[:1])),Z) for k in range(3))
    raw_area=[dot(S,x) for x in R]
    need(all(x>Z for x in raw_area),'actual projected receiving area orientation fails')
    A2sq=960+1536*phi
    area=[raw_area[i]*raw_area[j]-A2sq*dot(R[i],R[j]) for i in range(3) for j in range(i,3)]
    need(all(x>Z for x in area),'whole receiving triangle has not been proved beyond the A2 area barrier')
    dual_bounds=[]
    for row in data['duals']:
        cols=[[cross(V[c['source']],a) for a in supports[c['support']]['raw']] for c in row['contacts']]
        D0=[cross(V[c['source']],cross(supports[c['support']]['E'],r)) for c in row['contacts']]
        sign=dot(D0[0],cross(D0[1],D0[2])).sign();need(sign!=0,'named original torque basis is singular')
        determinant=triple_coefficients(lambda a,b,c:sign*dot(cols[0][a],cross(cols[1][b],cols[2][c])))
        target=tuple(F(row['sign']) if j==row['axis'] else Z for j in range(3))
        numerators=[]
        for i,contact in enumerate(row['contacts']):
            j,k=(i+1)%3,(i+2)%3;H=supports[contact['support']]['H']
            num=triple_coefficients(lambda a,b,c:sign*H[a]*dot(target,cross(cols[j][b],cols[k][c])))
            numerators.append(num)
        masses={ex:F([10,16,6][row['axis']])*determinant[ex]-sum((num[ex] for num in numerators),Z)
                for ex in determinant}
        need(all(x>Z for x in determinant.values()),'whole receiving cubic torque determinant sign fails')
        need(all(x>Z for num in numerators for x in num.values()),'whole receiving cubic positive coordinate dual fails')
        need(all(x>Z for x in masses.values()),'whole receiving cubic coordinate mass10,16,6 fails')
        dual_bounds.append({'sign':row['sign'],'axis':row['axis'],'determinant_minimum':min(determinant.values()).encode(),
                            'weight_numerator_minimum':min(x for num in numerators for x in num.values()).encode(),
                            'mass_numerator_minimum':min(masses.values()).encode(),
                            'all_cubic_coefficient_count':50})
    need(Q(9,8)**2*392/625==Q(3969,5000)<1,'whole receiving closed local collar does not close')
    alpha=Q(1,11);roots=[];volume=Z
    for indices in data['record']['face_triangles']:
        A,B,C=[data['D'][i] for i in indices];aA,aB,aC=[tuple(alpha*x for x in v) for v in [A,B,C]]
        group=[(aA,aB,aC,C),(aA,aB,B,C),(aA,A,B,C)]
        vols=[abs(dot(sub(T[1],T[0]),cross(sub(T[2],T[0]),sub(T[3],T[0])))) for T in group]
        need(all(x>Z for x in vols) and sum(vols,Z)==(1-F(alpha)**3)*abs(dot(A,cross(B,C))),
             'fresh whole receiving-domain shell frustum identity fails')
        roots.extend(group);volume+=sum(vols,Z)
    need(len(roots)==108 and (39-24*phi)/121<F(Q(1,625)),'whole receiving-domain core not inside new collar')
    record={'status':'exact whole receiving-triangle supports, area and conditional local rigidity prerequisites',
            'agent':'six-rupert-3','role':'researcher','receiving_raw_vertices':[encode(x) for x in R],'chart_halfwidth':str(width),
            'actual_supports':16,'original_offendpoint_linear_signs':2784,'polar_norm_quadratic_coefficients':96,
            'receiving_area_squared_minus_A2_squared_degree2_coefficients':[x.encode() for x in area],
            'all_receivers_beyond_A2':True,'minimum_raw_offendpoint_gap':minimum_gap.encode(),
            'minimum_quadratic_polar_norm_margin':minimum_norm.encode(),'six_degree3_duals':dual_bounds,
            'local_collar_closed_Cayley_euclidean_radius':'1/25','uniform_coordinate_masses':[10,16,6],
            'uniform_quadratic_torque_constant':'9/8','uniform_squared_local_closure':'3969/5000',
            'source_shell_alpha':'1/11','source_shell_roots':108,'whole_inner_core_in_new_collar':True,
            'source_root_abs_determinant_sum':volume.encode(),
            'root_geometry_sha256':hashlib.sha256(json.dumps([[encode(v) for v in T] for T in roots],separators=(',',':')).encode()).hexdigest(),
            'whole_triangle_includes_named_point':True,
            'source_cover_checked_separately':True}
    return {'R':R,'supports':supports,'S':S,'roots':roots,'record':record}
