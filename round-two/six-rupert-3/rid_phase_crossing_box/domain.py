"""Whole closed receiving phase box, true supports and actual conditional collars."""
from copy import deepcopy
import hashlib,json
from geometry import build,F,Q,Z,O,phi,dot,cross,sub,need,encode,act
from triangles import make_extension


def clip(poly,side):
    result=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        fa,fb=side(a),side(b)
        if fa>=Z:result.append(a)
        if fa*fb<Z:
            t=fa/(fa-fb);result.append(tuple(x+t*(y-x) for x,y in zip(a,b)))
    cleaned=[]
    for r in result:
        if not cleaned or r!=cleaned[-1]:cleaned.append(r)
    if cleaned and cleaned[0]==cleaned[-1]:cleaned.pop()
    return cleaned


def canonical_cycle(cycle):
    return min(tuple(cycle[i:]+cycle[:i]) for i in range(len(cycle)))


def hull(V,r):
    chart=sorted((v[0]-r[0]*v[2],v[1]-r[1]*v[2],i) for i,v in enumerate(V))
    def turn(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    lower=[];upper=[]
    for p in chart:
        while len(lower)>1 and turn(lower[-2],lower[-1],p)<=Z:lower.pop()
        lower.append(p)
    for p in reversed(chart):
        while len(upper)>1 and turn(upper[-2],upper[-1],p)<=Z:upper.pop()
        upper.append(p)
    return [p[2] for p in lower[:-1]+upper[:-1]]


def make_box(data,denominator=1000):
    V=data['V'];oldring=list(data['ring']);newring=oldring[:8]+[19]+oldring[8:]+[40]
    need(len(newring)==18 and V[40]==tuple(-x for x in V[19]),'true phase insertions differ')
    q=(F(Q(3,50),Q(2,25)),F(Q(1,25),Q(1,50)),O)
    face=cross(sub(V[18],V[19]),sub(V[11],V[18]))
    need(face==(2*(1-phi),2*phi,Z),'actual phase wall differs')
    def ell(r):return dot(face,r)
    need(ell(q)==Z,'box center is not on actual wall')
    eps=F(Q(1,denominator))
    box=[(q[0]+sx*eps,q[1]+sy*eps,O) for sx,sy in [(-1,-1),(1,-1),(1,1),(-1,1)]]
    need(any(ell(r)>Z for r in box) and any(ell(r)<Z for r in box),'box does not cross actual wall')
    phases=[];roots=None
    for sign,ring in [(1,oldring),(-1,newring)]:
        poly=clip(box,lambda r:sign*ell(r));need(len(poly)==4,'closed phase polygon is not a quadrilateral')
        observations=[];support_controls=0;height_controls=0
        edges=list(zip(ring,ring[1:]+ring[:1]))
        for r in poly:
            expected=oldring if ell(r)==Z else ring;actual=hull(V,r)
            need(canonical_cycle(actual)==canonical_cycle(expected),'full original hull differs at phase corner')
            ties=[]
            for j,(a,b) in enumerate(edges):
                m=cross(sub(V[b],V[a]),r);h=dot(m,V[a]);need(h>Z,'true support height failed')
                height_controls+=1
                for i,v in enumerate(V):
                    gap=dot(m,sub(V[a],v));need(gap>=Z,'true phase support misses original')
                    support_controls+=1
                    if gap==Z and i not in [a,b]:ties.append([j,i])
            observations.append({'receiver':encode(r),'actual_hull':actual,'offendpoint_ties':ties})
        local=deepcopy(data);local['r']=q;local['ring']=ring
        if sign==-1:
            selected=[list(p) for p in zip(oldring,oldring[1:]+oldring[:1])]
            selected[7]=[18,19];selected[15]=[41,40]
            local['actual_supports']=[{'endpoints':p} for p in selected]
        triangles=[(poly[0],poly[j],poly[j+1]) for j in range(1,3)]
        records=[];supports=None
        for triangle in triangles:
            dom=make_extension(local,triangle);record=dom['record']
            record['source_cover_checked_separately']=False
            record['actual_full_boundary_edges']=len(ring)
            record['selected_valid_physical_supports']=16
            record['area_uses_true_full_phase_ring']=True
            if roots is None:roots=dom['roots']
            else:need(roots==dom['roots'],'phase pieces use different closed source roots')
            records.append(record);supports=dom['supports']
        for sup in supports:
            sup['raw']=[cross(sup['E'],r) for r in poly]
            sup['H']=[dot(m,V[sup['source_endpoints'][0]]) for m in sup['raw']]
        phase_record={'sign':sign,'actual_ring':ring,'closed_polygon':[encode(r) for r in poly],
                      'all_corner_support_comparisons':support_controls,'strict_height_controls':height_controls,
                      'actual_corner_hulls':observations,'whole_fan_local_records':records}
        phases.append({'R':poly,'supports':supports,'record':phase_record})
    # A false old support must fail on the new side even arbitrarily near q.
    wrong=cross(sub(V[11],V[18]),box[1])
    need(dot(wrong,sub(V[18],V[19]))<Z,'obsolete old phase support accepted on new half')
    # Retain the ENTIRE parent9517 quadrilateral in the union theorem; the
    # new receiver must be outside every signed/projective parent body image.
    r0=(F(9)/100,(3+2*phi)/100,O);r1=(F(11)/100,(3+2*phi)/100,O)
    r2=(O/10,(5+2*phi)/100,O);omega=[r0,r1,q,r2]
    probe=(q[0]+eps/2,q[1],O);matches=0
    def turn(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    for g in data['G']:
        transpose=tuple(tuple(g[j][i] for j in range(3)) for i in range(3));u=act(transpose,probe)
        if u[2]==Z:continue
        raw=tuple(x/u[2] for x in u)
        if all(turn(a,b,raw)>=Z for a,b in zip(omega,omega[1:]+omega[:1])):matches+=1
    need(matches==0,'new receiver already covered by a parent receiving image')
    record={'agent':'six-rupert-3','role':'researcher','raw_center':encode(q),
            'raw_halfwidth':'1/'+str(denominator),'closed_box':[encode(r) for r in box],
            'wall_coefficients':encode(face),'closed_partition':'box intersect ell>=0 and box intersect ell<=0; entire seam included',
            'actual_phase_corner_counts':[16,18],'selected_supports_per_piece':16,
            'new_half_support_replacements':{'7':[18,19],'15':[41,40]},
            'phase_records':[p['record'] for p in phases],
            'source_alpha':'1/11','source_roots':108,
            'root_geometry_sha256':hashlib.sha256(json.dumps([[encode(v) for v in T] for T in roots],separators=(',',':')).encode()).hexdigest(),
            'uniform_closed_euclidean_Cayley_collar':'1/25','source_cover_not_inferred_from_prerequisites':True,
            'obsolete_old_support_rejected_on_new_half':True,'retained_closed_parent_quad':[encode(r) for r in omega],
            'strict_new_receiving_probe':encode(probe),'probe_matches_in_all60_signed_parent_images':matches}
    return {'q':q,'box':box,'phases':phases,'roots':roots,'record':record}
