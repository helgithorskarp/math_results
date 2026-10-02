"""Whole closed grazing receiver geometry and actual positive contact cubics."""
from itertools import product
from math import factorial
import hashlib,json
from geometry import build,OUT,F,Q,Z,O,phi,dot,cross,sub,need,encode,dec,act

def triple_coefficients(product_value):
    polynomial={}
    for a,b,c in product(range(3),repeat=3):
        ex=tuple([a,b,c].count(i) for i in range(3))
        polynomial[ex]=polynomial.get(ex,Z)+product_value(a,b,c)
    return {ex:value/(factorial(3)//(factorial(ex[0])*factorial(ex[1])*factorial(ex[2])))
            for ex,value in sorted(polynomial.items())}


def make_extension(data,R):
    r=data['r'];R=list(R)
    V,Ns=data['V'],data['Ns'];old={'actual_supports':data['actual_supports'],'ring':data['ring']}
    supports=[];minimum_gap=None;minimum_norm=None
    for row,N in zip(old['actual_supports'],Ns):
        vi,vj=row['endpoints'];E=sub(V[vj],V[vi]);raw=[cross(E,x) for x in R];H=[dot(a,V[vi]) for a in raw]
        need(all(x>Z for x in H),'whole receiving triangle crosses an actual support-height zero')
        gaps=[dot(a,sub(V[vi],v)) for a in raw for k,v in enumerate(V) if k not in [vi,vj]]
        need(all(x>=Z for x in gaps),'new closed triangle has an invalid actual support')
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
            'agent':'six-rupert-3','role':'researcher','receiving_raw_vertices':[encode(x) for x in R],'literal_raw_triangle':True,
            'actual_supports':16,'original_offendpoint_linear_signs':2784,'polar_norm_quadratic_coefficients':96,
            'receiving_area_squared_minus_A2_squared_degree2_coefficients':[x.encode() for x in area],
            'all_receivers_beyond_A2':True,'minimum_raw_offendpoint_gap':minimum_gap.encode(),
            'minimum_quadratic_polar_norm_margin':minimum_norm.encode(),'six_degree3_duals':dual_bounds,
            'local_collar_closed_Cayley_euclidean_radius':'1/25','uniform_coordinate_masses':[10,16,6],
            'uniform_quadratic_torque_constant':'9/8','uniform_squared_local_closure':'3969/5000',
            'source_shell_alpha':'1/11','source_shell_roots':108,'whole_inner_core_in_new_collar':True,
            'source_root_abs_determinant_sum':volume.encode(),
            'root_geometry_sha256':hashlib.sha256(json.dumps([[encode(v) for v in T] for T in roots],separators=(',',':')).encode()).hexdigest(),
            'whole_triangle_includes_named_point':False,
            'source_cover_checked_separately':True}
    return {'R':R,'supports':supports,'S':S,'roots':roots,'record':record}


def turn(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def make_domain(data):
    r0=(F(9)/100,(3+2*phi)/100,O)
    r1=(F(11)/100,(3+2*phi)/100,O)
    r2=(O/10,(5+2*phi)/100,O)
    q=(F(3)/50+2*phi/25,O/25+phi/50,O)
    R=[r1,r2,q];quad=[r0,r1,q,r2]
    need(all(turn(a,b,c)>Z for a,b in zip(quad,quad[1:]+quad[:1])
             for c in quad if c not in [a,b]),'whole closed receiving quadrilateral is not strictly convex')
    need(turn(r1,r2,r0)>Z and turn(r1,r2,q)<Z,'old/new receiving pieces do not share the internal diagonal')
    result=make_extension(data,R)
    V=data['V'];ring=data['ring'];start=data['r'];direction=(O,Z,Z)
    constraints=[];thresholds=[];grazing=[]
    for si,(i,j) in enumerate(zip(ring,ring[1:]+ring[:1])):
        E=sub(V[j],V[i])
        for kind,vi,a in [('height',i,cross(V[i],E))]+[
              ('offendpoint',vi,cross(sub(V[i],v),E)) for vi,v in enumerate(V) if vi not in [i,j]]:
            value=dot(a,start);slope=dot(a,direction)
            need(value>Z,'first-wall starting receiver is not strict phase interior')
            if slope<Z:thresholds.append(value/(-slope))
            at=dot(a,q);need(at>=Z,'literal first-wall actual support is false')
            if at==Z:grazing.append([si,kind,vi])
            constraints.append([si,kind,vi,a])
    tau=(2*phi-1)/25
    need(len(constraints)==944 and min(thresholds)==tau and
         tuple(start[j]+tau*direction[j] for j in range(3))==q,'first actual horizon wall differs')
    need(grazing==[[7,'offendpoint',19],[15,'offendpoint',40]],'literal actual grazing inventory differs')
    E=sub(V[ring[8]],V[ring[7]])
    beyond=(q[0]+F(Q(1,1000)),q[1],O);raw=cross(E,beyond)
    need(dot(raw,sub(V[ring[7]],V[19]))<Z,'false continuation past the actual horizon wall was accepted')
    # This affine chart has kernel exactly the viewing direction. It preserves
    # convex shadow incidence, while no Euclidean area is inferred from it.
    points={}
    for i,v in enumerate(V):
        xy=(v[0]-q[0]*v[2],v[1]-q[1]*v[2]);points.setdefault(xy,[]).append(i)
    ordered=sorted(points);lower=[];upper=[]
    for p in ordered:
        while len(lower)>=2 and turn(lower[-2],lower[-1],p)<=Z:lower.pop()
        lower.append(p)
    for p in reversed(ordered):
        while len(upper)>=2 and turn(upper[-2],upper[-1],p)<=Z:upper.pop()
        upper.append(p)
    hull=lower[:-1]+upper[:-1]
    need(len(points)==60 and len(hull)==16 and
         {i for p in hull for i in points[p]}==set(ring),'all-original wall shadow differs from actual16-ring')
    need(all(turn(a,b,p)>=Z for a,b in zip(hull,hull[1:]+hull[:1]) for p in ordered),
         'all-original grazing shadow support fails')
    # A new raw point alone need not enlarge an orbit-saturated domain. Check
    # all actual parent receiver images, including both projective signs.
    old_triangle=[r0,r1,r2];parent_image_matches=0
    for g in data['G']:
        transpose=tuple(tuple(g[j][i] for j in range(3)) for i in range(3))
        u=act(transpose,q)
        if u[2]==Z:continue
        raw=tuple(x/u[2] for x in u)
        if all(turn(a,b,raw)>=Z for a,b in zip(old_triangle,old_triangle[1:]+old_triangle[:1])):
            parent_image_matches+=1
    need(parent_image_matches==0,'new wall receiver was already covered by a parent body image')
    result['record'].update({
        'status':'exact whole closed grazing-triangle receiver and conditional local prerequisites; source entry checked separately',
        'closed_old_receiver_triangle':list(map(encode,old_triangle)),
        'closed_joined_receiver_quad':list(map(encode,quad)),
        'strict_convex_quad_global_turns':8,'shared_diagonal_opposite_side_checks':2,
        'closed_two_triangle_union':'old triangle r0,r1,r2 and new triangle r1,r2,q',
        'first_raw_ray_direction':[1,0,0],'first_wall_tau':tau.encode(),
        'all_original_ray_support_height_constraints':944,
        'actual_wall_grazing_constraints':grazing,
        'false_receiver_continuation_rejected':True,
        'wall_original_projection_classes':60,'wall_actual_hull_corners':16,
        'wall_global_convexity_checks':960,
        'new_wall_matches_among_all60_signed_parent_body_images':parent_image_matches,
        'strict_parent_receiving_image_extension':True,
        'formal_old_piece_dependency':'RID lemma9459, sourceb80366e395725934a83c5d0d5d0825939de60c83'})
    return result
