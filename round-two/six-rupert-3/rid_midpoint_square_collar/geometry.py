"""Fresh original RID and paired-square physical width certificate."""
from itertools import product
from fractions import Fraction as Q
from primitives import F,Z,O,phi,vertices,rotate,dot,cross,encode,need,digest,matrix_det

def verify(cert):
    V=vertices()
    need(len(V)==60 and set(V)=={tuple(-a for a in v) for v in V},
         'actual original named RID or centrality differs')
    vertex_hash=digest(list(map(encode,V)))
    need(vertex_hash=='fc20f041ee0dd3cb289807af1feb564186d66cc713bf256acc520c93aa26e1b1',
         'actual original named vertex ordering differs')
    c=tuple(F(*a) for a in cert['source_cayley']);M=[rotate(c,v) for v in V]
    basis=[tuple(O if i==j else Z for i in range(3)) for j in range(3)]
    cols=[rotate(c,v) for v in basis];R=tuple(zip(*cols))
    need(all(dot(a,b)==(O if i==j else Z) for i,a in enumerate(cols) for j,b in enumerate(cols)),
         'actual original source orthogonality fails')
    need(matrix_det(R)==O and sum((R[i][i] for i in range(3)),Z)==1+phi,
         'actual original source is not the proper36-degree midpoint')
    need(list(map(encode,R))==cert['parent_rotation_matrix'],
         'declared original proper source matrix differs')
    U=tuple(F(*a) for a in cert['face_axis']);h=F(*cert['face_height'])
    need(U==(Z,O,Z) and h==phi**3,'stated original face axis or height differs')
    rho=F(Q(cert['left_Cayley_radius']));need(Z<rho<O,'physical closed source radius invalid')
    origin_span=[(O,O,h),(-O,O,h),(O,-O,h)]
    need(all(v in V and tuple(-a for a in v) in V for v in origin_span)
         and matrix_det(origin_span)!=Z,'original origin-interior witness differs')
    need(len(cert['faces'])==2,'paired square certificate is incomplete')
    records=[]
    for fi,(name,body) in enumerate([('original_receiving',V),('actual_midpoint_moving',M)]):
        claimed=cert['faces'][fi]
        need(claimed['body']==name,'stated original paired-face body differs')
        gaps=[h-sign*dot(U,v) for sign in (-1,1) for v in body]
        need(all(a>=Z for a in gaps),'actual original paired-square support fails')
        plus=[i for i,v in enumerate(body) if dot(U,v)==h]
        minus=[i for i,v in enumerate(body) if dot(U,v)==-h]
        need(len(plus)==len(minus)==4 and plus==claimed['positive_original_labels']
             and minus==claimed['negative_original_labels'],
             'full actual paired-square face labels differ')
        centroid=tuple(sum((body[i][j] for i in plus),Z)/4 for j in range(3))
        need(centroid==tuple(h*a for a in U),'actual square centroid differs')
        u,v=[tuple(F(*a) for a in q) for q in claimed['orthonormal_square_half_edges']]
        need(dot(u,u)==dot(v,v)==O and dot(u,v)==Z and dot(U,u)==dot(U,v)==Z,
             'actual square half-edges not orthonormal in the face plane')
        corners={tuple(centroid[j]+a*u[j]+b*v[j] for j in range(3))
                 for a,b in product((-1,1),repeat=2)}
        need(corners=={body[i] for i in plus}
             and {tuple(-a for a in w) for w in corners}=={body[i] for i in minus},
             'literal original positive/negative squares differ')
        need(cross(u,v) in (U,tuple(-a for a in U)),
             'actual square frame has the wrong perpendicular normal')
        records.append({'body':name,'all120_actual_paired_support_gaps':encode(gaps),
            'positive_original_labels':plus,'negative_original_labels':minus,
            'centroid':encode(centroid),'orthonormal_half_edges':[encode(u),encode(v)],
            'all4_positive_original_face_points':list(map(encode,(body[i] for i in plus))),
            'all4_negative_original_face_points':list(map(encode,(body[i] for i in minus)))})
    gamma_squared=F(*cert['square_inradius_squared'])
    need(gamma_squared==O,'stated square inradius is not its actual unit inradius')
    gap=gamma_squared-h*h*rho*rho;cosine=(O-rho*rho)/(O+rho*rho)
    need(h*h==5+8*phi and gap>Z and cosine>Z,
         'full closed physical paired-square width cusp is not valid')
    trace=3-4*rho*rho/(O+rho*rho);distance=8*rho*rho/(O+rho*rho)
    need(trace==F(*cert['physical_trace_gate'])
         and distance==F(*cert['physical_squared_Frobenius_gate']),
         'original physical trace or Frobenius gate differs')
    data={'agent':'six-rupert-3','role':'researcher','actual_original_named_vertex_sha256':vertex_hash,
          'original_source_cayley':encode(c),'original_proper_source_matrix':list(map(encode,R)),
          'original_origin_interior_span':list(map(encode,origin_span)),
          'unit_world_axis':encode(U),'actual_support_height':h.encode(),
          'complete_actual_paired_square_faces':records,'all_original_face_support_controls':240,
          'actual_square_inradius_squared':gamma_squared.encode(),
          'closed_physical_left_Cayley_radius':cert['left_Cayley_radius'],
          'strict_cusp_squared_margin':gap.encode(),'strict_positive_cosine_lower':cosine.encode(),
          'physical_trace_gate':trace.encode(),'physical_squared_Frobenius_gate':distance.encode(),
          'ordinary_axis_conclusion':'For EVERY nonzero r perpendicular to U and original t/lambda>=1, fit in the displayed closed physical left gate forces delta=zU,lambda1,U.t0. Remaining z and original fullt are closed separately.'}
    return {'V':V,'M':M,'c':c,'U':U,'h':h,'rho':rho,'data':data}
