#!/usr/bin/env python3
"""six-reviewer-2 independent exact RID audit; no target Python imports.

Uses Z[sqrt(5)] coefficient pairs and primitive integer projective rays.
Author fixtures supply only persistent probe witnesses; all support,
extremality, facet and global optimizer computations are rebuilt.
"""
import argparse
import hashlib
import json
import math
from collections import Counter
from fractions import Fraction as F
from functools import cmp_to_key
from itertools import combinations, product
from pathlib import Path

Z=(0,0); O=(1,0); PH=(F(1,2),F(1,2))
def require(condition,message='independent exact check failed'):
    if not condition: raise ValueError(message)
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def neg(x): return (-x[0],-x[1])
def sub(x,y): return add(x,neg(y))
def mul(x,y): return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def sc(x,k): return (x[0]*k,x[1]*k)
def div(x,y):
    d=y[0]*y[0]-5*y[1]*y[1]
    if not d: raise ValueError('zero field divisor')
    return sc(mul(x,(y[0],-y[1])),F(1,d))
def sign(x):
    a,b=x
    if not b: return (a>0)-(a<0)
    if not a: return (b>0)-(b<0)
    if (a>0)==(b>0): return (a>0)-(a<0)
    return ((a>0)-(a<0))*((a*a>5*b*b)-(a*a<5*b*b))
def eq(x,y): return x==y
def dot(v,w):
    s=Z
    for a,b in zip(v,w): s=add(s,mul(a,b))
    return s
def va(v,w): return tuple(add(a,b) for a,b in zip(v,w))
def vs(v,w): return tuple(sub(a,b) for a,b in zip(v,w))
def vc(v,k): return tuple(sc(a,k) for a in v)
def cross(v,w): return tuple(sub(mul(v[i],w[j]),mul(v[j],w[i])) for i,j in ((1,2),(2,0),(0,1)))
def det(v,w,u): return dot(v,cross(w,u))
def decode(x):
    a,b=map(F,x)
    return (a+b/2,b/2)
def enc(x): return [str(x[0]),str(x[1])]
def ray(v):
    z=next((x for x in v if x!=Z),None)
    if z is None: return None
    conj=(z[0],-z[1]); d=mul(z,conj)[0]
    w=tuple(mul(x,conj) for x in v)
    if d<0: w=vc(w,-1)
    require(all((isinstance(a, int) and isinstance(b, int) for a, b in w)))
    g=math.gcd(*(n for x in w for n in x))
    return tuple((a//g,b//g) for a,b in w)
def rational_ray(v):
    L=math.lcm(*(F(x).denominator for a in v for x in a))
    return ray(tuple(tuple(int(x*L) for x in a) for a in v))
def scorecmp(p,q): return sign(sub(mul(p[0],q[1]),mul(q[0],p[1])))
def original_vertices():
    # Coordinates are 2V, so all coefficients are integers in Z[sqrt(5)].
    seeds=[((2,0),(2,0),(4,2)),((3,1),(1,1),(2,2)),((5,1),Z,(3,1))]
    out=set()
    for v in seeds:
        for j in range(3):
            w=v[j:]+v[:j]
            for signs in product((-1,1),repeat=3): out.add(tuple(sc(x,s) for x,s in zip(w,signs)))
    return sorted(out)
def primitive_field_key(x):
    return tuple((F(a).numerator,F(a).denominator,F(b).numerator,F(b).denominator) for a,b in x)
def vcompare(v,w):
    return next((s for a,b in zip(v,w) if (s:=sign(sub(a,b)))),0)
def act(M,v): return tuple(dot(row,v) for row in M)
def mm(M,N): return tuple(tuple(dot(row,col) for col in zip(*N)) for row in M)
def identity(): return tuple(tuple(O if i==j else Z for j in range(3)) for i in range(3))

def group_audit(V,winners):
    # Exhaust ALL proper rotations by images of one ordered nonparallel pair.
    # This gives an upper bound as well as sixty positive symmetry witnesses.
    a=V[0]; b=max((v for v in V if v!=a),key=cmp_to_key(lambda v,w:sign(sub(dot(a,v),dot(a,w)))))
    ab=dot(a,b); c=cross(a,b); volume=det(a,b,c)
    inverse=tuple(tuple(div(x,volume) for x in v) for v in (cross(b,c),cross(c,a),cross(a,b)))
    groups=set(); pair_candidates=0; checks=0; vertex_set=set(V)
    for aa in V:
        for bb in V:
            if dot(aa,bb)!=ab: continue
            pair_candidates+=1; cc=cross(aa,bb); cols=(aa,bb,cc)
            M=tuple(tuple(sum_field(mul(cols[k][i],inverse[k][j]) for k in range(3)) for j in range(3)) for i in range(3))
            require(mm(M, tuple(zip(*M))) == identity() and det(*M) == O)
            valid=True
            for v in V:
                checks+=1
                if act(M,v) not in vertex_set: valid=False; break
            if valid: groups.add(M)
    require(len(groups) == 60)
    A,B,D,U=chart(); centers={act(M,B) for M in groups}; N=dot(B,B)
    projective={rational_ray(v) for v in centers}
    require(len(centers) == 20 and projective == set(winners))
    walls=((O,Z,Z),(Z,O,Z),(neg(PH),neg(mul(PH,PH)),O))
    threshold=div(sub((2,0),PH),(3,0)); margins=[]
    for t in centers:
        if t==B: continue
        negatives=[div(mul(dot(w,t),dot(w,t)),mul(dot(w,w),N)) for w in walls if sign(dot(w,t))<0]
        require(negatives and all((sign(sub(x, threshold)) >= 0 for x in negatives)))
        margins.extend(negatives)
    reflection_checks=0
    for w in walls:
        reflection=tuple(tuple(sub(O if i==j else Z,div(sc(mul(w[i],w[j]),2),dot(w,w))) for j in range(3)) for i in range(3))
        require({act(reflection, v) for v in V} == vertex_set and tuple((tuple((neg(x) for x in row)) for row in reflection)) in groups)
        reflection_checks+=len(V)
    halfturns=0
    for M in groups:
        if sum_field(M[i][i] for i in range(3))!=(-1,0): continue
        axis=next(tuple(add(M[i][j],O if i==j else Z) for i in range(3)) for j in range(3) if any(add(M[i][j],O if i==j else Z)!=Z for i in range(3)))
        require(any((dot(v, axis) == Z for v in V))); halfturns+=1
    require(halfturns == 15)
    return {'ordered_adjacent_vertex_image_pairs_exhausted':pair_candidates,'vertex_membership_checks':checks,
            'entire_proper_body_rotation_group':len(groups),'directed_winning_center_orbit':20,
            'winning_center_orbit_matches_global_enumeration':True,'chamber_wall_vertex_checks':reflection_checks,
            'other_center_negative_wall_margin_squared_lower':enc(threshold),
            'body_halfturns_with_original_zero_height_witness':halfturns}
def sum_field(values):
    total=Z
    for x in values: total=add(total,x)
    return total

def global_audit(V):
    require(len(V) == 60 and all((dot(v, v) == (44, 16) for v in V)))
    A=[v for v in V if sign(next(x for x in v if x!=Z))>0]
    require(len(A) == 30)
    candidates=[]
    candidates.extend(A)
    candidates.extend(va(a,vc(b,s)) for a,b in combinations(A,2) for s in (-1,1))
    candidates.extend(cross(vs(a,vc(b,s)),vs(a,vc(c,t)))
                      for a,b,c in combinations(A,3) for s,t in product((-1,1),repeat=2))
    require(len(candidates) == 17140)
    unique=set(); regions={}; boundary=0; zero=0
    # Deliberately evaluate every raw nonzero candidate, before deduplication.
    for v in candidates:
        k=ray(v)
        if k is None: zero+=1; continue
        unique.add(k)
        dots=[dot(a,k) for a in A]; pattern=tuple(sign(x) for x in dots)
        if 0 in pattern: boundary+=1; continue
        if pattern[0]<0: pattern=tuple(-x for x in pattern)
        squares=[mul(x,x) for x in dots]; lo=squares[0]
        for x in squares[1:]:
            if sign(sub(x,lo))<0: lo=x
        value=(lo,sc(dot(k,k),4))
        if pattern not in regions or scorecmp(value,regions[pattern][0])>0: regions[pattern]=(value,k)
    spectrum=Counter(); winners=[]; boundary_axes=[]
    beta=div(sub((19,0),sc(PH,8)),(29,0))
    for value,k in regions.values():
        s=div(*value); spectrum[tuple(enc(s))]+=1
        if s==(F(1,3),0): winners.append(k)
        elif s==beta: boundary_axes.append(k)
        else: require(sign(sub(beta, s)) > 0)
    require(len(unique) == 4681 and len(regions) == 436 and (len(winners) == 10) and (len(boundary_axes) == 60), (len(unique), len(regions), len(winners), len(boundary_axes), spectrum))
    # At each of the sixty nonwinning maxima, count actual antipodal circle points.
    active_counts=Counter()
    for k in boundary_axes:
        value=next(x for x,j in regions.values() if j==k)
        n=dot(k,k)
        active=[v for v in V if scorecmp((mul(dot(v,k),dot(v,k)),sc(n,4)),value)==0]
        shadows={vs(tuple(mul(x,n) for x in v),tuple(mul(x,dot(v,k)) for x in k)) for v in active}
        require(len(shadows) == len(active) and len(shadows) >= 6)
        active_counts[len(active)]+=1
    pair_checks=0
    for a,b in combinations(V,2):
        two=div(add((44,16),dot(a,b)),(8,0))
        require(two != beta); pair_checks+=1
    return {'vertices':60,'raw_active_set_candidates':len(candidates),'zero_raw_candidates':zero,
            'distinct_projective_candidates':len(unique),'raw_boundary_candidates':boundary,
            'raw_candidate_dot_products':(len(candidates)-zero)*30,'strict_projective_regions':len(regions),
            'regional_maximum_squared_spectrum_sqrt5_basis':sorted([[list(k),v] for k,v in spectrum.items()]),
            'winning_projective_centers':len(winners),'nonwinning_beta_projective_maximizers':len(boundary_axes),
            'beta_source_distinct_maximum_circle_points_histogram':dict(sorted(active_counts.items())),
            'original_vertex_pair_threshold_exclusions':pair_checks},winners

def chart():
    A=(Z,Z,O); B=(Z,sub((2,0),PH),O)
    D=(div(O,mul(PH,add(PH,(2,0)))),div(O,add(PH,(2,0))),O)
    q=F(57,125); s=div(sub(sub(PH,O),(q,0)),PH); t=div(sub(sub(PH,O),(q,0)),sub(PH,O))
    U=(B,va(B,tuple(mul(s,x) for x in vs(A,B))),va(B,tuple(mul(t,x) for x in vs(D,B))))
    return A,B,D,U

def boundary_geometry(V):
    A,B,D,U=chart(); n=dot(B,B); active=[vc(v,F(1,2)) for v in V if sign(dot(v,B))>0 and sc(mul(dot(v,B),dot(v,B)),3)==sc(n,4)]
    require(len(active) == 6)
    tangent=[vs(v,tuple(mul(x,div(dot(v,B),n)) for x in B)) for v in active]
    require(all((sum((x[j][i] for x in tangent)) == 0 for j in range(3) for i in range(2))))
    levels=Counter(); facets=[]
    for i,j in combinations(range(6),2):
        m=cross(B,vs(tangent[j],tangent[i])); h=dot(m,tangent[i]); gaps=[sign(sub(dot(m,x),h)) for x in tangent]
        if max(gaps)<=0 or min(gaps)>=0:
            require(h != Z)
            distance=div(mul(h,h),dot(m,m)); levels[tuple(enc(distance))]+=1; facets.append((i,j))
    require(len(facets) == 6)
    expect=Counter({tuple(enc(add((F(8,3),0),sc(PH,4)))):3,tuple(enc(add((F(17,3),0),sc(PH,8)))):3})
    require(levels == expect)
    cut=((-1,0),(2,1),(-1,0)); require(cut in active)
    ties={}
    for label,u in zip(('A','B','D'),(A,B,D)):
        heights=[dot(v,u) for v in active]; lo=dot(cut,u)
        require(all((sign(sub(x, lo)) >= 0 for x in heights)))
        ties[label]=[active[i] for i,x in enumerate(heights) if x==lo]
    require(len(ties['A']) == len(ties['D']) == 2 and len(set(ties['A']) & set(ties['D'])) == 1)
    require(len(ties['B']) == 6)
    nonactive=[v for v in V if sc(mul(dot(v,B),dot(v,B)),3)!=sc(n,4)]
    sq=[div(mul(dot(v,B),dot(v,B)),sc(n,4)) for v in nonactive]
    require(len(nonactive) == 48 and all((sign(sub(x, (F(5, 3), 0))) >= 0 for x in sq)) and ((F(5, 3), 0) in sq))
    for u in U:
        require(sign(sub((F(27, 25) ** 2, 0), dot(u, u))) > 0)
        require(sign(sub((F(27, 500) ** 2, 0), dot(vs(u, B), vs(u, B)))) > 0)
    return {'active_positive_vertices':6,'full_tangent_hexagon_facets':6,'sharp_tangent_radius_squared':enc(add((F(8,3),0),sc(PH,4))),
            'tangent_edge_distance_spectrum':[[list(k),v] for k,v in sorted(levels.items())],
            'chamber_positive_minimum_ties':{k:len(v) for k,v in ties.items()},'A_D_tie_intersection':1,
            'nonactive_original_vertices':48,'minimum_nonactive_center_height_squared':['5/3','0'],
            'outer_triangle_corner_norm_and_drift_checks':6},U

# Separate sparse homogeneous polynomial arithmetic over INTEGER Z[sqrt(5)].
def padd(p,q):
    out=dict(p)
    for k,v in q.items():
        z=add(out.get(k,Z),v)
        if z==Z: out.pop(k,None)
        else: out[k]=z
    return out
def pscale(p,c): return {k:sc(v,c) for k,v in p.items() if sc(v,c)!=Z}
def pmul(p,q):
    out={}
    for k,a in p.items():
        for l,b in q.items():
            e=tuple(x+y for x,y in zip(k,l)); z=add(out.get(e,Z),mul(a,b))
            if z==Z: out.pop(e,None)
            else: out[e]=z
    return out
def pdot(p,q):
    out={}
    for a,b in zip(p,q): out=padd(out,pmul(a,b))
    return out
def psub(p,q): return tuple(padd(a,pscale(b,-1)) for a,b in zip(p,q))
def pcross(p,q): return tuple(padd(pmul(p[i],q[j]),pscale(pmul(p[j],q[i]),-1)) for i,j in ((1,2),(2,0),(0,1)))
def restriction(p,face): return {k:v for k,v in p.items() if all(k[j]==0 for j in range(3) if j not in face)}
def psign(p,face):
    signs={sign(v) for v in restriction(p,face).values()}
    return next(iter(signs)) if len(signs)==1 else 0
def nonneg(p,face): return all(sign(v)>=0 for v in restriction(p,face).values())
def validate_record_masks(original):
    coverage=original['distance_face_mask']|original['degenerate_face_mask']
    require(original['distance_face_mask']&original['degenerate_face_mask']==0,'overlapping distance/degenerate strata')
    for mask,pos,minus in original['opposite_gap_witnesses']:
        require(coverage&mask==0 and 0<=pos<10 and 0<=minus<10 and 0<mask<=127,'overlapping/invalid opposite strata')
        coverage|=mask
    require(coverage==127,'incomplete seven-stratum cover')
def peval(p,lam):
    out=Z
    for k,v in p.items(): out=add(out,sc(v,math.prod(lam[j]**k[j] for j in range(3))))
    return out

def torque_audit(V,U,input_dir,try_radius=F(51,100)):
    data=json.loads((input_dir/'adaptive_receiver_expected.json').read_text())
    pool=[(tuple(decode(x) for x in p['vertex']),tuple(decode(x) for x in p['edge'])) for p in data['persistent_probes']]
    require(len(pool) == 36 and len(set(pool)) == 36)
    A,B,D,_=chart(); Tor={cross(v,cross(e,B)):(v,e) for v,e in pool}
    require(len(Tor) == 18)
    # Derive center facets WITHOUT using the author's center normals or selector.
    points=list(Tor); planes=set(); supportchecks=0
    for a,b,c in combinations(points,3):
        normal=cross(vs(b,a),vs(c,a))
        if normal==(Z,Z,Z): continue
        h=dot(normal,a); gaps=[sign(sub(dot(normal,t),h)) for t in points]; supportchecks+=len(points)
        if max(gaps)<=0 or min(gaps)>=0:
            require(h != Z); planes.add(tuple(div(x,h) for x in normal))
    require(len(planes) == 15 and all((sign(sub(div(O, dot(p, p)), sub((2, 0), PH))) >= 0 for p in planes)))
    selected=[]
    for t,p in Tor.items():
        act=[f for f in planes if dot(f,t)==O]
        if any(det(*x)!=Z for x in combinations(act,3)): selected.append(p)
    selected.sort(key=cmp_to_key(lambda p,q:vcompare(cross(p[0],cross(p[1],B)),cross(q[0],cross(q[1],B)))))
    require(len(selected) == 10)
    selectedT=[cross(v,cross(e,B)) for v,e in selected]
    positive_stress=any(all(sign(x)==1 for x in cof) or all(sign(x)==-1 for x in cof)
                       for quad in combinations(selectedT,4)
                       for cof in [[sc(det(*(quad[k] for k in range(4) if k!=j)),(-1)**j) for j in range(4)]])
    require(positive_stress)
    vv=set(vc(v,F(1,2)) for v in V); supports=0
    for v,e in selected:
        require(v in vv and dot(e, e) == (4, 0) and (va(v, e) in vv or vs(v, e) in vv))
        for u in (A,B,D)+U:
            m=cross(e,u)
            for w in vv: require(sign(dot(m, vs(v, w))) >= 0); supports+=1
    # Scale coordinates BEFORE constructing polynomials: every coefficient is integer.
    L=math.lcm(*(F(x).denominator for u in U for a in u for x in a))
    chart_int=[tuple(tuple(int(x*L) for x in a) for a in u) for u in U]
    torque_scale=4*L
    units=[tuple(int(i==j) for i in range(3)) for j in range(3)]
    polys=[]
    for v,e in selected:
        vi=tuple(tuple(int(x*2) for x in a) for a in v); ei=tuple(tuple(int(x*2) for x in a) for a in e)
        ts=[cross(vi,cross(ei,u)) for u in chart_int]
        polys.append(tuple({units[j]:ts[j][k] for j in range(3) if ts[j][k]!=Z} for k in range(3)))
    S={x:O for x in units}; S2=pmul(S,S); faces=[c for n in (3,2,1) for c in combinations(range(3),n)]
    counts=Counter(); stronger=Counter(); audit_checks=0; coef_hash=hashlib.sha256(); records=[]
    native=json.loads((input_dir/'winning_receiver_expected.json').read_text())['complete_actual_torque_facet_certificate']
    original_records=native['compressed_stratum_certificates']
    require(native['simplex_strata'] == [list(x) for x in faces] and len(original_records) == 120)
    native_cases=0
    for triple in combinations(range(10),3):
        a,b,c=(polys[i] for i in triple); normal=pcross(psub(b,a),psub(c,a)); H=pdot(normal,a)
        gaps=[padd(pdot(normal,t),pscale(H,-1)) for t in polys]
        H2=pmul(H,H); NS=pmul(pdot(normal,normal),S2)
        P=padd(pscale(H2,4),pscale(NS,-torque_scale**2))
        p,q=try_radius.numerator,try_radius.denominator
        Pstrong=padd(pscale(H2,q*q),pscale(NS,-p*p*torque_scale**2))
        require(all((sum(e) == 6 for e in P)))
        stream=[triple,[[list(e),enc(v)] for e,v in sorted(P.items())]]
        coef_hash.update(json.dumps(stream,separators=(',',':')).encode()+b'\n')
        record={'triple':triple,'cases':[]}
        original=original_records[len(records)]
        require(original['triple'] == list(triple))
        validate_record_masks(original)
        for face_index,face in enumerate(faces):
            signs=[psign(g,face) for g in gaps]
            if 1 in signs and -1 in signs: kind='opposite'; witness=[signs.index(1),signs.index(-1)]
            elif all(not restriction(x,face) for x in normal): kind='degenerate'; witness=[]
            elif nonneg(P,face): kind='distance'; witness=[]
            else: raise AssertionError(('uncovered stratum',triple,face))
            counts[kind]+=1
            record['cases'].append([face,kind,witness])
            stronger[kind if kind!='distance' or nonneg(Pstrong,face) else 'unresolved']+=1
            bit=1<<face_index
            if original['distance_face_mask']&bit: require(nonneg(P, face))
            elif original['degenerate_face_mask']&bit: require(all((not restriction(x, face) for x in normal)))
            else:
                pos,minus=next((p,m) for mask,p,m in original['opposite_gap_witnesses'] if mask&bit)
                require(psign(gaps[pos], face) == 1 and psign(gaps[minus], face) == -1)
            native_cases+=1
        # Arithmetic consistency at four exact nodes; this is NOT the continuum proof.
        for lam in ((1,0,0),(0,1,0),(0,0,1),(1,2,3)):
            tv=[tuple(peval(p,lam) for p in t) for t in polys]
            x,y,z=(tv[i] for i in triple); n=cross(vs(y,x),vs(z,x)); h=dot(n,x)
            require(tuple((peval(t, lam) for t in normal)) == n and peval(H, lam) == h)
            for j,g in enumerate(gaps): require(peval(g, lam) == sub(dot(n, tv[j]), h)); audit_checks+=1
            require(peval(P, lam) == sub(sc(mul(h, h), 4), sc(dot(n, n), torque_scale ** 2 * sum(lam) ** 2))); audit_checks+=2
        records.append(record)
    require(counts == Counter({'opposite': 726, 'distance': 114}))
    return {'persistent_probe_pool':36,'center_distinct_torques':18,'center_facets_independently_enumerated':15,
            'center_ten_extreme_torques_independently_selected':10,'positive_center_interior_stress':positive_stress,
            'center_facet_support_checks':supportchecks,'selected_original_support_checks_ABD_and_outer_triangle':supports,
            'integer_chart_scale':L,'integer_torque_scale':torque_scale,'facet_triples':120,'simplex_strata':7,
            'stratum_classifications':dict(counts),'independent_distance_polynomial_stream_sha256':coef_hash.hexdigest(),
            'original_compressed_strata_independently_verified':native_cases,
            'direct_exact_node_checks':audit_checks,'uniform_torque_radius_squared_original':'1/4',
            'tested_stronger_radius':str(try_radius),'stronger_stratum_classifications':dict(stronger),
            'stronger_radius_certified':stronger.get('unresolved',0)==0,
            'selected_probes_phi_basis':[{'vertex':[[str(a-b),str(2*b)] for a,b in v],'edge':[[str(a-b),str(2*b)] for a,b in e]} for v,e in selected]}

def selftests():
    require(sign((2, -1)) == -1 and sign((-2, 1)) == 1 and (sign((3, -1)) == 1) and (sign((-3, 1)) == -1))
    for x in ((2,1),(-3,2),(1,0)):
        require(div(mul(x, (7, -2)), (7, -2)) == x)
    v=((1,2),(3,-1),(4,2))
    require(ray(tuple((mul(x, (3, -2)) for x in v))) == ray(v))
    p={(2,0,0):(1,0),(0,2,0):(-1,0)}
    require(not nonneg(p, (0, 1)) and psign(p, (0, 1)) == 0 and (psign(p, (0,)) == 1) and (psign({}, (0,)) == 0))
    require(not nonneg({(0, 0, 6): (-1, 0)}, (2,)))
    return 12

def phase_gates():
    beta=div(sub((19,0),sc(PH,8)),(29,0)); d=F(1,24)
    E=(F(13,15)*d+F(3,2)*d*d+F(17,16)*d*d)/(1-d*d/4)
    checks=[sign(sub(beta,(F(57,125)**2,0)))>0,F(1,3)<F(289,500)**2,
            (F(289,500)-F(57,125))/3<F(1,20),F(399,400)>F(199,200)**2,
            F(101,100)**2*F(399,400)>1,F(101,300)*(F(289,500)-F(57,125))<d,
            E==F(267,6580),E<F(77,1000),F(101,100)**2*((2*d)**2+E*E)<F(47,500)**2,
            sign(sub((F(9,2)**2,0),(11,4)))>0,sign(sub((F(17,4),0),(2,1)))>0,
            F(12909,10000)**2<F(5,3),sign(sub((F(42361,10000),0),(2,1)))>0,
            F(9987,10000)**2<F(399,400),F(433,250)**2<3,
            F(12909,10000)*F(9987,10000)/10-F(42361,10000)/200>F(77,1000),
            F(12909,10000)/2-F(42361,10000)*(1-F(433,500))>F(77,1000),
            F(5,4)*F(99,100)-F(17,4)/20==F(41,40),F(101,100)**2*F(63,64)>1,
            F(51,100)-F(9,2)*F(27,25)*F(47,500)==F(1329,25000),F(1329,25000)>F(1,20)]
    require(all(checks),'unsupported source/roll/full-angle phase gate')
    return {'rational_or_field_comparisons':len(checks),'balanced_roll_error_upper':str(E),
            'original_remainder_margin_lower':'1079/25000','improved_remainder_margin_lower':'1329/25000',
            'improved_remainder_margin_exceeds':'1/20'}

def malformed_controls(V):
    failures=[lambda:global_audit(V[:-1]),
              lambda:validate_record_masks({'distance_face_mask':63,'degenerate_face_mask':0,'opposite_gap_witnesses':[]}),
              lambda:validate_record_masks({'distance_face_mask':127,'degenerate_face_mask':1,'opposite_gap_witnesses':[]}),
              lambda:require(psign({(3,0,0):O},(0,))==-1,'reversed strict gap witness'),
              lambda:require(nonneg({(0,0,6):(-1,0)},(2,)),'unsupported squared-distance coefficient')]
    for failure in failures:
        try: failure()
        except ValueError: pass
        else: raise ValueError('malformed control was accepted')
    return len(failures)

def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--input-dir',type=Path,required=True)
    parser.add_argument('--output',type=Path); args=parser.parse_args()
    manifest_path=Path(__file__).with_name('INPUT.json')
    if manifest_path.exists():
        manifest=json.loads(manifest_path.read_text())
        for name,digest in manifest['sha256'].items(): require(hashlib.sha256((args.input_dir/name).read_bytes()).hexdigest()==digest,'pinned source changed: '+name)
    controls=selftests(); V=original_vertices(); negative=malformed_controls(V); phase=phase_gates()
    global_result,winners=global_audit(V); geometry,U=boundary_geometry(V)
    group=group_audit(V,winners)
    torque=torque_audit(V,U,args.input_dir)
    result={'agent':'six-reviewer-2','role':'independent mathematical reviewer','arithmetic':'exact coefficient pairs a+b*sqrt(5), integer polynomial coefficients; stdlib only',
            'target_python_modules_imported':False,'global':global_result,'boundary_geometry':geometry,'proper_symmetries_and_chamber':group,'torque_continuum':torque,'kernel_controls':controls,
            'malformed_controls_rejected':negative,'phase_gates':phase,
            'global_non_rupert_proved':False,'continuous_geometric_bridges':'audited separately in REVIEW.md; not formalized'}
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output: args.output.write_text(text)
    else: print(text,end='')
if __name__=='__main__': main()
