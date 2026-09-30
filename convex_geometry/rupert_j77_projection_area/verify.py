"""Exact J77 physical area, polar source budget and minimum-shadow checker.

Author: six-rupert-2, researcher. Python 3.11+, standard library, no floats.
Continuous Cauchy/polar/coercivity/containment bridges are in PROOF.md.
Both ordinary and optimized Python check every expected output byte.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from math import isqrt, lcm
from pathlib import Path
import json
import sys

HERE=Path(__file__).resolve().parent
DEPENDENCIES=json.loads((HERE/'dependencies.json').read_text())
BASE=HERE.parent/'rupert_j77_projection_diameter'
def require(ok,message):
    if not ok: raise ValueError(message)
require(DEPENDENCIES['source_directory']=='convex_geometry/rupert_j77_projection_diameter','dependency path')
for name,digest in DEPENDENCIES['sha256'].items():
    require(sha256((BASE/name).read_bytes()).hexdigest()==digest,'dependency changed: '+name)
sys.path.insert(0,str(BASE))
import model
from q5 import Q, add, cross, dot, scale, sub

ZERO=(0,0)
SIGNS={}
SIGN_CALLS=0
def ra(x,y): return (x[0]+y[0],x[1]+y[1])
def rn(x): return (-x[0],-x[1])
def rs(x,y): return (x[0]-y[0],x[1]-y[1])
def rm(x,y): return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def sign(x):
    global SIGN_CALLS
    SIGN_CALLS+=1
    a,b=x
    if not a: s=(b>0)-(b<0)
    elif not b: s=(a>0)-(a<0)
    elif (a>0)==(b>0): s=(a>0)-(a<0)
    else:
        d=a*a-5*b*b
        s=((d>0)-(d<0))*((a>0)-(a<0))
    SIGNS[x]=s
    return s
def sg(x):
    x=Q(x); d=lcm(x.a.denominator,x.b.denominator)
    return sign((int(d*x.a),int(d*x.b)))
def positive(x,message): require(sg(x)>0,message)
def vd(u,v): return tuple(rs(x,y) for x,y in zip(u,v))
def vn(u): return tuple(rn(x) for x in u)
def rd(u,v): return ra(ra(rm(u[0],v[0]),rm(u[1],v[1])),rm(u[2],v[2]))
def rc(u,v):
    return (rs(rm(u[1],v[2]),rm(u[2],v[1])),
            rs(rm(u[2],v[0]),rm(u[0],v[2])),
            rs(rm(u[0],v[1]),rm(u[1],v[0])))
def qv(u): return tuple(Q(*x) for x in u)
def absq(x): return x if sg(x)>=0 else -x
def enc(x):
    if isinstance(x,Q): return [str(x.a),str(x.b)]
    if isinstance(x,(tuple,list)): return [enc(t) for t in x]
    if isinstance(x,dict): return {str(k):enc(v) for k,v in x.items()}
    return x
def canonical(u):
    p=next(Q(*x) for x in u if x!=ZERO)
    return tuple(Q(*x)/p for x in u)
def canonical_q(u):
    p=next(x for x in u if x!=0)
    return tuple(x/p for x in u)
def digest(data):
    return sha256(json.dumps(enc(data),sort_keys=True,separators=(',',':')).encode()).hexdigest()

def interval_sign(pair):
    """Independent rational sqrt5 enclosure; no conjugate-sign formula."""
    a,b=pair
    if not a and not b:return 0
    for bits in (16,32,64,128,256,512,1024,2048):
        den=1<<bits; lo=isqrt(5*den*den); hi=lo+1
        left,right=sorted((a*den+b*lo,a*den+b*hi))
        if left>0:return 1
        if right<0:return -1
    raise ValueError('independent sign enclosure unresolved')

def field_controls():
    require(Q(0,1)*Q(0,1)==5,'field square')
    require((1+Q(0,1))*(1-Q(0,1))==-4,'field conjugate')
    require((1+Q(0,1))/(1+Q(0,1))==1,'field quotient')
    values=[ZERO,(2,0),(-2,0),(-2,1),(2,-1),(0,-1)]
    x=(1,0)
    for _ in range(60):
        x=rm(x,(9,-4));values.extend((x,rn(x)))
    for x in values: require(sign(x)==interval_sign(x),'Pell sign control')
    return len(values)

def originals():
    V=model.VERTICES
    require(len(V)==55 and len(set(V))==55,'original vertex count')
    R2=Q(11,4)/4
    require(all(dot(v,v)==R2 for v in V),'common original sphere')
    original,core,cap,gyrated,axis=model.cupola_construction()
    require(tuple(map(len,(original,core,cap,gyrated)))==(60,50,5,5),'independent cupola counts')
    require(core|gyrated==set(V) and core.isdisjoint(gyrated),'named-solid construction')
    require({scale(-1,v) for v in core}==core,'antipodal core')
    require(all(scale(-1,V[i])==V[j] for i,j in ((0,7),(8,15),(16,20))),'interior antipodes')
    require(dot(cross(V[0],V[8]),V[16])!=0,'interior rank')
    S=lcm(*(x.a.denominator for v in V for x in v),*(x.b.denominator for v in V for x in v))
    W=tuple(tuple((int(S*x.a),int(S*x.b)) for x in v) for v in V)
    require(all(qv(w)==scale(S,v) for w,v in zip(W,V)),'integer lift')
    return V,core,axis,S,W

def all_facets(V,S,W):
    planes={};counts=Counter()
    for i,j,k in combinations(range(len(V)),3):
        counts['triples']+=1
        n=rc(vd(W[j],W[i]),vd(W[k],W[i]))
        if n==(ZERO,ZERO,ZERO): counts['collinear']+=1;continue
        h=rd(n,W[i]);sides=set();zeros=[]
        for t,w in enumerate(W):
            s=sign(rs(rd(n,w),h));counts['side_comparisons']+=1
            if s:sides.add(s)
            else:zeros.append(t)
            if len(sides)==2:break
        if len(sides)==2:counts['nonsupporting']+=1;continue
        require(len(sides)==1,'full-dimensional hull')
        counts['supporting_triples']+=1
        if 1 in sides:n,h=vn(n),rn(h)
        require(sign(h)==1,'outward signed height')
        key=tuple(zeros)
        if key in planes:
            oldn,oldh=planes[key]
            require(all(rm(x,oldh)==rm(y,h) for x,y in zip(n,oldn)),'exact plane deduplication')
        else:planes[key]=(n,h)
    require(counts['triples']==26235,'incomplete triple enumeration')
    require(set(planes)==set(tuple(sorted(f)) for f in model.FACES),'proposed/actual hull equality')
    records=[];B=[];edges=Counter()
    cosine={3:Q(-1)/2,4:Q(),5:Q(-1,1)/4,10:Q(1,1)/4}
    for face in model.FACES:
        require(len(face)==len(set(face)),'repeated face vertex')
        n,h=planes[tuple(sorted(face))];b=(ZERO,ZERO,ZERO)
        for i,j in zip(face,face[1:]+face[:1]):b=tuple(ra(x,y) for x,y in zip(b,rc(W[i],W[j])))
        if sign(rd(n,b))<0:face=tuple(reversed(face));b=vn(b)
        require(sign(rd(n,b))==1 and rc(n,b)==(ZERO,ZERO,ZERO),'outward physical area')
        t=face.index(min(face));face=face[t:]+face[:t]
        for i,j in zip(face,face[1:]+face[:1]):
            edges[tuple(sorted((i,j)))]+=1
            for k in face:
                if k in (i,j):continue
                require(sign(rd(n,rc(vd(W[j],W[i]),vd(W[k],W[i]))))==1,'entire cyclic edge order')
                counts['cyclic_edge_gates']+=1
        # Fresh unit-edge and polygon-turn checks, rather than parent verify().
        ee=[sub(V[j],V[i]) for i,j in zip(face,face[1:]+face[:1])]
        require(all(dot(e,e)==1 for e in ee),'unit original face edges')
        require(all(dot(e,ee[(i+1)%len(ee)])==cosine[len(face)] for i,e in enumerate(ee)),'regular original turns')
        nq,hq=qv(n),Q(*h)
        for i,v in enumerate(V):
            q=dot(nq,scale(S,v))-hq;r=rs(rd(n,W[i]),h)
            require(q==Q(*r) and q.sign()==sign(r),'Fraction/ring support audit')
            counts['fraction_support_audits']+=1
        aq=scale(Q(1)/(2*S*S),qv(b))
        ref=scale(Q(1)/2,tuple(sum((cross(V[i],V[j])[t] for i,j in zip(face,face[1:]+face[:1])),Q()) for t in range(3)))
        require(aq==ref,'independent physical half-area normalization')
        records.append({'vertices':face,'plane':scale(S/hq,nq),'area_vector':aq});B.append(b)
    require(set(edges.values())=={2} and 55-len(edges)+len(records)==2,'edge/Euler diagnostics')
    require(tuple(sum((r['area_vector'][t] for r in records),Q()) for t in range(3))==(Q(),Q(),Q()),'closed vector surface sum')
    rank=next((c for c in combinations(range(len(B)),3) if rd(rc(B[c[0]],B[c[1]]),B[c[2]])!=ZERO),None)
    require(rank is not None,'full-dimensional area zonotope')
    return records,B,counts,len(edges),rank

def brightness(V,core,S,records,B):
    candidates={};parallel=0
    for i,j in combinations(range(len(B)),2):
        d=rc(B[i],B[j])
        if d==(ZERO,ZERO,ZERO):parallel+=1;continue
        candidates.setdefault(canonical(d),{'pair':(i,j),'ray_ring':d})
    spectrum=[]
    for k,rec in candidates.items():
        d=rec['ray_ring'];total=ZERO
        for b in B:
            z=rd(b,d)
            if sign(z)<0:z=rn(z)
            total=ra(total,z)
        num=rm(total,total);den=rm((16*S**4,0),rd(d,d))
        require(sign(den)==1,'candidate positive squared norm')
        A2=Q(*num)/Q(*den)
        qtotal=sum((absq(dot(r['area_vector'],k)) for r in records),Q())
        require(A2==qtotal*qtotal/(4*dot(k,k)),'all candidate physical formula audits')
        f2=min(dot(v,k)*dot(v,k) for v in core)/dot(k,k)
        spectrum.append({'pair':rec['pair'],'ray':k,'area_squared':A2,'core_height_squared':f2})
    # Exact sorting of field values is audited separately via sg differences.
    levels=sorted(set(r['area_squared'] for r in spectrum))
    require(all(sg(b-a)>0 for a,b in zip(levels,levels[1:])),'ordered area spectrum')
    best=levels[0];second=levels[1]
    winners=[r for r in spectrum if r['area_squared']==best]
    require(all(sg(r['area_squared']-best)>=0 for r in spectrum),'complete minimum comparison')
    require(all(r['area_squared']==best or sg(r['area_squared']-second)>=0 for r in spectrum),'complete nonminimal comparison')
    return spectrum,winners,best,second,parallel

def body_rotation(axis,v):
    c=Q(-1,1)/4
    return add(add(scale(c,v),scale((1-c)*dot(axis,v)/dot(axis,axis),axis)),scale(Q(1)/2,cross(axis,v)))

def area_data(V,axis,records,winners,best,second):
    E=(Q(1),Q(),Q());A0=Q(49,25)/8
    require(best==A0*A0 and second==Q(725)/8+Q(0,1621)/40,'claimed global area levels')
    basis=((Q(1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)))
    cols=tuple(body_rotation(axis,e) for e in basis)
    require(all(dot(cols[i],cols[j])==int(i==j) for i in range(3) for j in range(3)),'actual R orthogonal')
    require(dot(cross(cols[0],cols[1]),cols[2])==1,'actual R proper')
    require({body_rotation(axis,v) for v in V}==set(V),'actual original R symmetry')
    for e in basis:
        u=e
        for _ in range(5):u=body_rotation(axis,u)
        require(u==e,'actual R fifth power on full spatial basis')
    orbit=[];u=E
    for _ in range(5):orbit.append(u);u=body_rotation(axis,u)
    require(u==E and len(set(canonical_q(u) for u in orbit))==5,'five projective area axes')
    require(set(canonical_q(r['ray']) for r in winners)==set(canonical_q(u) for u in orbit),'ALL area minimum axes')
    zero=[];C=(Q(),Q(),Q())
    for i,r in enumerate(records):
        a=r['area_vector'];s=sg(a[0])
        if s:C=add(C,scale(Q(s)/2,a))
        else:zero.append((i,a))
    require(C==scale(A0,E),'actual global nonzero-area lower support')
    tangent=[]
    for i,a in zero:
        require(a!=(Q(),Q(),Q()) and a[0]==0,'actual nonzero tangent generator')
        m=cross(E,a)
        for s in (-1,1):
            u=scale(s,m)
            h=sum((absq(dot(b,u)) for j,b in zero),Q())/2
            positive(h,'centered tangent support branch')
            tangent.append({'face':i,'sign':s,'ray':u,'height':h,'distance_squared':h*h/dot(u,u)})
    require(any(cross(a,b)!=(Q(),Q(),Q()) for i,a in zero for j,b in zero),'tangent zonotope rank')
    rho2=min(r['distance_squared'] for r in tangent)
    require(rho2==Q(169)/32+Q(0,359)/160,'sharp tangent centered disk')
    require(all(sg(r['distance_squared']-rho2)>=0 for r in tangent),'all tangent inradius comparisons')
    # A strict, elementary outward bound for the complete tangent surface sum.
    upper={10:F(31,4),5:F(7,4),4:F(1),3:F(7,16)}
    terms=[]
    for i,a in zero:
        B=Q(upper[len(records[i]['vertices'])]);gap=B*B-dot(a,a)
        require(sg(gap)>=0,'outward tangent generator norm')
        terms.append({'face':i,'norm_upper':str(upper[len(records[i]['vertices'])]),'squared_gap':gap})
    L=sum((upper[len(records[i]['vertices'])] for i,a in zero),F())/2
    require(L==F(277,32) and any(sg(t['squared_gap'])>0 for t in terms),'strict tangent norm-sum bound')
    delta=F(1,1000);sign_gates=[]
    for i,r in enumerate(records):
        a=r['area_vector']
        if a[0]==0:continue
        gap=a[0]*a[0]-delta*delta*dot(a,a)
        positive(gap,'all nonzero receiving area signs persist')
        sign_gates.append({'face':i,'squared_gap':gap})
    return A0,E,orbit,C,zero,tangent,rho2,L,terms,sign_gates

def shadow(V,A0):
    pts=sorted(set((v[1],v[2]) for v in V))
    def det(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    low=[];up=[]
    for p in pts:
        while len(low)>1 and sg(det(low[-2],low[-1],p))<=0:low.pop()
        low.append(p)
    for p in reversed(pts):
        while len(up)>1 and sg(det(up[-2],up[-1],p))<=0:up.pop()
        up.append(p)
    H=low[:-1]+up[:-1]
    require(len(H)==10 and len(set(H))==10,'actual minimum-area shadow vertices')
    support_gates=0
    for a,b in zip(H,H[1:]+H[:1]):
        for p in pts:
            require(sg(det(a,b,p))>=0,'all original shadow support sides');support_gates+=1
        for p in H:
            if p not in (a,b):positive(det(a,b,p),'all minimum-shadow vertices strictly extreme')
    area=sum((a[0]*b[1]-a[1]*b[0] for a,b in zip(H,H[1:]+H[:1])),Q())/2
    require(area==A0,'independent projected shoelace area')
    distances={(i,j):sum(((a-b)*(a-b) for a,b in zip(H[i],H[j])),Q()) for i in range(10) for j in range(10)}
    accepted=[];blockers=[]
    for orientation in (-1,1):
        for shift in range(10):
            perm=[(shift+orientation*i)%10 for i in range(10)]
            bad=next(((i,j) for i in range(10) for j in range(10) if distances[i,j]!=distances[perm[i],perm[j]]),None)
            if bad is None:accepted.append((orientation,shift))
            else:
                i,j=bad;gap=distances[i,j]-distances[perm[i],perm[j]]
                require(sg(gap)!=0,'exact polygon isometry blocker')
                blockers.append({'orientation':orientation,'shift':shift,'pair':bad,'distance_gap':gap})
    require(accepted==[(1,0)] and len(blockers)==19,'complete O(2) shadow symmetry exhaustion')
    return {'projected_originals':len(pts),'vertices':H,'area':area,'original_support_side_checks':support_gates,
            'cyclic_isometry_candidates':20,'accepted_isometries':accepted,'blockers':blockers}

def validate_claim(fixture,data):
    expected_keys={'minimum_area','next_facet_distance_squared','tangent_inradius_squared','area_budget_excess',
      'coarse_source_chord','receiver_chord','source_chord','tangent_radius_lower','tangent_sqrt_factor_lower',
      'area_lower_slope','receiver_area_lipschitz_upper','local_passage_scale_squared_upper'}
    require(set(fixture)==expected_keys,'claim fixture keys')
    A0=data['A0'];rho2=data['rho2'];second=data['second']
    require(Q(*fixture['minimum_area'])==A0,'minimum-area fixture')
    require(Q(*fixture['next_facet_distance_squared'])==second,'next-facet fixture')
    require(Q(*fixture['tangent_inradius_squared'])==rho2,'tangent disk fixture')
    eta=F(fixture['area_budget_excess']);a=F(fixture['coarse_source_chord'])
    delta=F(fixture['receiver_chord']);cap=F(fixture['source_chord'])
    r=F(fixture['tangent_radius_lower']);b=F(fixture['tangent_sqrt_factor_lower'])
    slope=F(fixture['area_lower_slope']);L=F(fixture['receiver_area_lipschitz_upper'])
    scale2=F(fixture['local_passage_scale_squared_upper'])
    require(0<eta<=F(9,1000) and 0<a<=F(1,20),'positive source budget/range')
    require(0<delta<=F(1,1000) and 0<cap<=F(1,300),'receiving/source cap range')
    require(r>0 and b>0 and slope>0,'positive coercivity factors')
    positive(second-(A0+eta)*(A0+eta),'polar nonminimal vertex exclusion')
    positive(A0-(1-a*a/2)*(A0+eta),'positive polar coarse-cap branch')
    positive(rho2-r*r,'tangent radius lower bound')
    require(b*b<1-a*a/4,'tangent square-root factor')
    positive(Q(105)/8-A0,'outward A0 upper bound')
    require(r*b-F(105,8)*a/2>slope,'strict linear area coercivity')
    require(L>=data['L'] and L*delta<=eta,'entire receiving area budget')
    require(eta/slope<cap,'derived source cap')
    positive(A0-13,'A0 lower bound for scale')
    positive((scale2-1)*A0-L*delta,'derived passage scale squared')
    return {'maximum_area_excess':str(eta),'coarse_source_chord':str(a),'receiver_chord':str(delta),
            'source_chord':str(cap),'source_chord_strict_from_budget':str(eta/slope),
            'global_positive_excess_to_chord_factor':str(1/slope),'linear_lower_slope':str(slope),
            'receiver_area_lipschitz_upper':str(L),'local_passage_scale_squared_upper':str(scale2)}

def malformed_controls(fixture,data):
    mutations=[('minimum_area',['49/8','0']),('next_facet_distance_squared',['725/8','0']),
      ('tangent_inradius_squared',['169/32','0']),('area_budget_excess','1/100'),
      ('coarse_source_chord','1/100'),('receiver_chord','1/100'),('source_chord','1/1000'),
      ('tangent_radius_lower','13/4'),('tangent_sqrt_factor_lower','1'),('area_lower_slope','3'),
      ('receiver_area_lipschitz_upper','8'),('local_passage_scale_squared_upper','3001/3000')]
    for key,value in mutations:
        bad=dict(fixture);bad[key]=value
        try:validate_claim(bad,data)
        except ValueError:continue
        raise ValueError('malformed claim accepted: '+key)
    bad=dict(fixture);bad['unsupported_source_branch']='all proper gauges already near identity'
    try:validate_claim(bad,data)
    except ValueError:pass
    else:raise ValueError('unsupported branch accepted')
    return len(mutations)+1

def check(self_test):
    controls=field_controls()
    V,core,axis,S,W=originals()
    records,B,counts,edges,rank=all_facets(V,S,W)
    spectrum,winners,best,second,parallel=brightness(V,core,S,records,B)
    A0,E,orbit,C,zero,tangent,rho2,L,terms,sign_gates=area_data(V,axis,records,winners,best,second)
    minimum_shadow=shadow(V,A0)
    data={'A0':A0,'rho2':rho2,'second':second,'L':L}
    fixture=json.loads((HERE/'certificates.json').read_text())
    bounds=validate_claim(fixture,data)
    bad=malformed_controls(fixture,data) if self_test else 0
    # Compare against the previous diameter reference from original coordinates.
    D=(Q(),Q(-1),Q(7,1)/2)
    darea=sum((absq(dot(r['area_vector'],D)) for r in records),Q())/2
    Darea2=darea*darea/dot(D,D)
    CD=(Q(),Q(),Q())
    south=(Q(),-D[2],Q(-1))
    require(dot(D,south)==0,'old-axis true tangent direction')
    for r in records:
        b=r['area_vector'];s=sg(dot(b,D))
        if s:CD=add(CD,scale(Q(s)/2,b))
        else:require(dot(b,south)==0,'old-axis tangent remains in zero walls')
    positive(-dot(CD,south),'old-axis negative south area derivative')
    require(all(r['core_height_squared']==0 for r in winners),'area and diameter axes differ')
    require(sg(Darea2-best)>0,'strict area-vs-diameter-axis comparison')
    for pair,expected in tuple(SIGNS.items()):
        require(interval_sign(pair)==expected,'independent rational sign audit')
    return enc({'agent':'six-rupert-2','role':'researcher','proof_status':'author-checked written intermediate proof; unformalized',
      'global_Rupert_resolved':False,'independent_review_asserted':False,'coefficient_field':'Q(sqrt5), sqrt5 positive',
      'original_vertices':55,'original_antipodal_core':50,'unit_edge_named_cupola_construction_replayed':True,
      'pinned_dependency_files':len(DEPENDENCIES['sha256']),'integer_vertex_scale':S,
      'complete_original_hull':{'facets':len(records),'edges':edges,'face_sizes':dict(Counter(len(r['vertices']) for r in records)),
          'counts':dict(counts),'rank_witness':rank,'ordered_physical_face_records_sha256':digest(records)},
      'complete_area_zonotope':{'original_area_generators':52,'generator_pairs':1326,'parallel_pairs':parallel,
          'projective_facet_normals':len(spectrum),'directed_polar_vertices':2*len(spectrum),
          'all_physical_candidate_audits':len(spectrum),'full_area_spectrum_sha256':digest(spectrum),
          'minimum_area':A0,'minimum_squared':best,'next_distinct_facet_distance_squared':second,
          'minimum_rays':winners,'actual_proper_C5_minimum_orbit':orbit},
      'global_source_localization':{'nonzero_area_lower_support':C,'zero_area_faces':[i for i,a in zero],
          'all_directed_tangent_supports':len(tangent),'tangent_inradius_squared':rho2,
          'tangent_support_records_sha256':digest(tangent),'tangent_generator_upper_bounds':terms,
          'entire_receiver_sign_gates':len(sign_gates),'receiver_sign_gate_records_sha256':digest(sign_gates),
          'bounds':bounds,'requires_no_diameter_or_central_symmetry_hypothesis':True,
          'full_proper_roll_or_receiver_cap_classification_asserted':False},
      'minimum_shadow':minimum_shadow,
      'minimum_axis_closed_containment':{'scale':1,'translation':0,'proper_rotations':'R^k, k=0,...,4',
          'source_rotations_translations_scales_unrestricted':True},
      'old_diameter_reference_area_squared':Darea2,
      'old_axis_area_diagnostic':{'south_tangent':south,'area_numerator_derivative':dot(CD,south),'unit_area_derivative_sign':-1},
      'old_diameter_or_signed_region_enumerations_replayed':False,
      'canonical_claim_fixture_sha256':digest(fixture),'malformed_controls_with_self_test':bad,
      'kernel_control_signs':controls,'sign_calls':SIGN_CALLS,'distinct_independent_sign_audits':len(SIGNS)})

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    result=check(args.self_test)
    encoded=(json.dumps(result,indent=2)+'\n').encode()
    expected=HERE/'expected.json'
    require(expected.exists(),'expected fixture missing')
    require(encoded==expected.read_bytes(),'EVERY expected output byte must match; use --self-test')
    sys.stdout.buffer.write(encoded)
