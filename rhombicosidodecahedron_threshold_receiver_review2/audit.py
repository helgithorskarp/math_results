#!/usr/bin/env python3
"""Independent RID threshold audit by six-reviewer-2, stdlib only.

Imports the pinned previously published reviewer2 arithmetic kernel only.
Reconstructs the full body group, two threshold orbits and hulls. Certifies
complete roll arcs by degree-two Bernstein coefficients, with dyadic roots.
No target Python imports, sampled-angle premise, or numerical solver.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from fractions import Fraction as F
from functools import cmp_to_key
from itertools import combinations
from pathlib import Path

BASE_SHA='1ce270a559c9b86582ff7bae580763490a10468d6cd5367a70927c7f269ac456'
ZERO=(0,0);ONE=(1,0)

def load_kernel(path):
    require(hashlib.sha256(path.read_bytes()).hexdigest()==BASE_SHA,'reviewer2 kernel pin changed')
    spec=importlib.util.spec_from_file_location('reviewer2_exact_kernel',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    globals().update({n:getattr(module,n) for n in ['add','sub','neg','mul','sc','div','sign','dot','va','vs','vc','cross','det','act','mm','identity','rational_ray','sum_field','PH','enc']})
    return module

def require(condition,message='independent threshold audit failed'):
    if not condition:raise ValueError(message)
def minimum(xs):return min(xs,key=cmp_to_key(lambda x,y:sign(sub(x,y))))
def vcmp(v,w):return next((s for x,y in zip(v,w) if (s:=sign(sub(x,y)))),0)
def field_vector_encode(v):return [enc(x) for x in v]
def scaled(v,q):return tuple(mul(x,q) for x in v)

def proper(M):
    require(mm(M,tuple(zip(*M)))==identity() and det(*M)==ONE,'improper spatial matrix')

def body_group(V):
    a=V[0];b=max((v for v in V if v!=a),key=cmp_to_key(lambda v,w:sign(sub(dot(a,v),dot(a,w)))))
    c=cross(a,b);volume=det(a,b,c)
    inverse=tuple(tuple(div(x,volume) for x in v) for v in (cross(b,c),cross(c,a),cross(a,b)))
    G=set();candidates=0
    for aa in V:
        for bb in V:
            if dot(aa,bb)!=dot(a,b):continue
            candidates+=1;cols=(aa,bb,cross(aa,bb))
            M=tuple(tuple(sum_field(mul(cols[k][i],inverse[k][j]) for k in range(3)) for j in range(3)) for i in range(3))
            proper(M)
            if {act(M,v) for v in V}==set(V):G.add(M)
    require(candidates==240 and len(G)==60,'full ordered-pair body classification changed')
    return G

def project(v,n):return vs(v,scaled(n,div(dot(v,n),dot(n,n))))

def shadow(V,n,corners):
    require(n[0]==ZERO,'chart requires x-axis tangent')
    e2=cross(n,(ONE,ZERO,ZERO));S={project(v,n) for v in V}
    coordinates=lambda p:(p[0],dot(p,e2))
    points=sorted(S,key=cmp_to_key(lambda p,q:vcmp(coordinates(p),coordinates(q))))
    def turn(a,b,c):
        x=vs(coordinates(b),coordinates(a));y=vs(coordinates(c),coordinates(a))
        return sign(sub(mul(x[0],y[1]),mul(x[1],y[0])))
    lower=[];upper=[]
    for p in points:
        while len(lower)>=2 and turn(lower[-2],lower[-1],p)<=0:lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper)>=2 and turn(upper[-2],upper[-1],p)<=0:upper.pop()
        upper.append(p)
    H=lower[:-1]+upper[:-1]
    normals=[cross(vs(q,p),n) for p,q in zip(H,H[1:]+H[:1])]
    require(len(S)==60 and len(H)==corners,'complete shadow hull counts')
    require(all(sign(dot(m,vs(p,v)))>=0 for m,p in zip(normals,H) for v in V),'actual original supporting inequality')
    area_vec=vc(tuple(sum_field(cross(p,q)[j] for p,q in zip(H,H[1:]+H[:1])) for j in range(3)),F(1,2))
    area2=div(mul(dot(area_vec,n),dot(area_vec,n)),dot(n,n))
    require(sign(dot(area_vec,n))>0,'hull orientation')
    radius2=max((dot(p,p) for p in S),key=cmp_to_key(lambda a,b:sign(sub(a,b))))
    circle={p for p in S if dot(p,p)==radius2}
    return {'normal':n,'projections':S,'hull':H,'facets':normals,'area2':area2,'circle':circle,'radius2':radius2}

def active_tangents(V,n,beta):
    N=dot(n,n);heights=[dot(v,n) for v in V];require(all(x!=ZERO for x in heights),'strict sign region')
    c=minimum([x for x in heights if sign(x)>0]);require(div(mul(c,c),N)==beta,'wrong threshold height')
    active=[v for v in V if dot(v,n)==c];require(len(active)==4,'complete four positive contacts')
    y=scaled(n,div(c,N));positive=[]
    for triple in combinations(active,3):
        a,b,d=triple;volume=det(a,b,d)
        if volume==ZERO:continue
        weights=(div(det(y,b,d),volume),div(det(a,y,d),volume),div(det(a,b,y),volume))
        if all(sign(w)>0 for w in weights):
            require(sum_field(weights)==ONE and tuple(sum_field(mul(w,v[j]) for w,v in zip(weights,triple)) for j in range(3))==y,'exact nearest-point balance')
            positive.append((triple,weights))
    require(positive,'threshold optimum not positively balanced')
    tangents=[vs(v,y) for v in active];distances=[]
    for a,b in combinations(tangents,2):
        m=cross(n,vs(b,a));h=dot(m,a);gaps=[sign(sub(dot(m,t),h)) for t in tangents]
        if max(gaps)<=0 or min(gaps)>=0:
            require(h!=ZERO,'origin lies on threshold tangent facet')
            distances.append(div(mul(h,h),dot(m,m)))
    require(len(distances)==4 and all(sign(x)>0 for x in distances),'complete threshold tangent quadrilateral')
    return minimum(distances),len(positive)

def orbit_audit(V,G,refs,beta):
    reps=[v for v in V if sign(next(x for x in v if x!=ZERO))>0]
    keys=set();rays=set();summary=[]
    for n in refs:
        directed={act(g,n) for g in G};axes={rational_ray(v) for v in directed}
        require(len(directed)==60 and len(axes)==30 and not rays&axes,'threshold orbit coverage')
        require({vc(v,-1) for v in directed}==directed,'directed reversal omitted')
        require(sum(act(g,n)==n for g in G)==1 and sum(rational_ray(act(g,n))==rational_ray(n) for g in G)==2,'stabilizers')
        rr,balances=active_tangents(V,n,beta)
        for k in axes:
            sigma=tuple(sign(dot(v,k)) for v in reps);key=min(sigma,tuple(-s for s in sigma))
            require(key not in keys and 0 not in key,'distinct strict threshold regions')
            keys.add(key);radius,_=active_tangents(V,k,beta);require(radius==rr,'orbit tangent inradius changed')
        rays|=axes
        summary.append({'reference_ray':field_vector_encode(n),'projective_axes':30,'directed_normals':60,'positive_three_contact_balances_at_reference':balances,
                        'sharp_positive_active_tangent_disk_radius_squared':enc(rr)})
    require(len(keys)==60 and len(rays)==60,'all threshold maxima accounted for')
    return summary

# Independent outward dyadic square-root and rational interval kernel.
def ia(x,y):return (x[0]+y[0],x[1]+y[1])
def ins(x):return (-x[1],-x[0])
def isu(x,y):return ia(x,ins(y))
def im(x,y):
    values=[a*b for a in x for b in y];return(min(values),max(values))
def isc(x,k):return (x[0]*k,x[1]*k) if k>=0 else (x[1]*k,x[0]*k)
def idi(x,y):
    require(y[0]>0,'interval divisor is not strictly positive')
    return im(x,(1/y[1],1/y[0]))
ROOTS={};DEN=2**80
def sqrt_field(q):
    if q in ROOTS:return ROOTS[q]
    require(sign(q)>0,'positive square root required')
    lo=0;hi=DEN
    while sign(sub((F(hi,DEN)**2,0),q))<0:hi*=2
    while hi-lo>1:
        mid=(lo+hi)//2
        if sign(sub((F(mid,DEN)**2,0),q))<=0:lo=mid
        else:hi=mid
    l,h=F(lo,DEN),F(hi,DEN)
    require(sign(sub(q,(l*l,0)))>=0 and sign(sub((h*h,0),q))>=0 and h-l==F(1,DEN),'invalid dyadic root enclosure')
    ROOTS[q]=(l,h);return ROOTS[q]
def enclose(q):return ia((F(q[0]),F(q[0])),isc(sqrt_field((5,0)),q[1]))

def coefficients(source,target):
    B=source['normal'];n=target['normal'];ex=(ONE,ZERO,ZERO)
    e_source=cross(B,ex);e_target=cross(n,ex)
    Nb=sqrt_field(dot(B,B));Nn=sqrt_field(dot(n,n));coords=[(enclose(p[0]),idi(enclose(dot(p,e_source)),Nb)) for p in source['hull']]
    result=[]
    for m,p in zip(target['facets'],target['hull']):
        length=sqrt_field(dot(m,m));mx=idi(enclose(m[0]),length);my=idi(idi(enclose(dot(m,e_target)),Nn),length)
        support=idi(enclose(dot(m,p)),length);require(support[0]>0,'nonpositive physical receiver support')
        for px,py in coords:result.append((ia(im(mx,px),im(my,py)),isu(im(my,px),im(mx,py)),support))
    require(len(result)==192,'complete physical facet/corner coefficients')
    return result

def bernstein_lower(A,D,b,l,h,gap):
    p0=isu(isu(A,b),(gap,gap));p1=isc(D,2);p2=isu(isu(ins(A),b),(gap,gap))
    def combine(x,y):return ia(ia(p0,isc(p1,x)),isc(p2,y))[0]
    return (combine(l,l*l),combine((l+h)/2,l*h),combine(h,h*h))

def validate_runs(runs,grid=128):
    cells=set()
    for quarter,start,end,witness in runs:
        require(quarter in range(4) and 0<=start<end<=grid and witness in range(192),'invalid closed-arc run')
        for j in range(start,end):
            require((quarter,j) not in cells,'overlapping closed-arc runs')
            cells.add((quarter,j))
    require(cells=={(q,j) for q in range(4) for j in range(grid)},'incomplete closed-circle interval cover')

def closed_arc_cover(source,target,grid=128,gap=F(1,16)):
    require(grid==128 and gap==F(1,16),'fixed independent certificate parameters')
    terms=coefficients(source,target);rows=[];runs=[];mincoeff=None;evaluations=0
    for quarter in range(4):
        rotated=[]
        for A,D,b in terms:
            for _ in range(quarter):A,D=D,ins(A)
            rotated.append((A,D,b))
        run=None
        for j in range(grid):
            l,h=F(j,grid),F(j+1,grid);best=None
            for k,(A,D,b) in enumerate(rotated):
                lows=bernstein_lower(A,D,b,l,h,gap);lower=min(lows);evaluations+=1
                if best is None or lower>best[0]:best=(lower,k,lows)
            require(best[0]>0,('uncovered closed roll arc',quarter,j,best[0]))
            rows.append([quarter,j,best[1],[str(x) for x in best[2]]])
            if mincoeff is None or best[0]<mincoeff:mincoeff=best[0]
            if run is not None and run[2]==best[1]:run[1]=j+1
            else:
                run=[j,j+1,best[1]];runs.append([quarter,run])
    digest=hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()
    compressed=[[q,*run] for q,run in runs];validate_runs(compressed)
    margin=gap-F(2687,96000);require(margin==F(3313,96000) and margin>F(1,30),'closed-arc transport margin')
    return {'closed_quarters':4,'intervals_per_quarter':128,'entire_closed_roll_arcs':512,'all_facet_corner_arc_candidates':evaluations,
            'all_selected_Bernstein_coefficients_strictly_positive':True,'minimum_selected_Bernstein_coefficient_lower':str(mincoeff),
            'uniform_physical_reference_support_gap_lower':str(gap),'actual_source_transport_error_upper':'2687/96000',
            'uniform_actual_winning_source_support_separation_lower':str(margin),'full_generated_closed_arc_record_sha256':digest,
            'compressed_closed_arc_witness_runs':compressed}

def alignments(G):
    a=(0,F(1,5));M=((ONE,ZERO,ZERO),(ZERO,a,sc(a,-2)),(ZERO,sc(a,-2),neg(a)))
    H=tuple(tuple(neg(x) for x in row) for row in M);L=((ONE,ZERO,ZERO),(ZERO,(-1,0),ZERO),(ZERO,ZERO,(-1,0)))
    R=mm(H,L);require(det(*M)==(-1,0) and L in G,'signed alignment premise');proper(H);proper(R)
    u=(ZERO,PH,(-1,0));c=sc(PH,F(1,2));s=sc(sub(PH,ONE),F(1,2));N=dot(u,u)
    skew=((ZERO,neg(u[2]),u[1]),(u[2],ZERO,neg(u[0])),(neg(u[1]),u[0],ZERO))
    C=tuple(tuple(add(add(mul(c,identity()[i][j]),div(mul(sub(ONE,c),mul(u[i],u[j])),N)),mul(s,skew[i][j])) for j in range(3)) for i in range(3))
    proper(C);power=identity();powers=[]
    for _ in range(5):power=mm(C,power);powers.append(power)
    require(C not in G and powers[1] in G and powers[3] in G and powers[4]==R,'36-degree coset construction')
    require({mm(C,g) for g in G}=={mm(R,g) for g in G}=={mm(H,g) for g in G},'left body coset representatives')
    return R,C

def circle_rolls(V,shadows,R):
    result=[]
    for si,ti in ((0,0),(0,1),(1,0),(1,1)):
        source,target=shadows[si],shadows[ti];alignment=identity() if si==ti else R
        n=target['normal'];N=dot(n,n);radius2=target['radius2'];mapped={act(alignment,p) for p in source['circle']}
        require(mapped==target['circle'],'proper circle alignment failed')
        pivot=next(iter(mapped));valid=[]
        for q in target['circle']:
            c=div(dot(pivot,q),radius2);s=div(dot(n,cross(pivot,q)),mul(N,radius2))
            require(add(mul(c,c),mul(N,mul(s,s)))==ONE,'circle rotation normalization')
            rotate=lambda p:va(scaled(p,c),scaled(cross(n,p),s))
            if {rotate(p) for p in mapped}!=target['circle']:continue
            points={rotate(act(alignment,p)) for p in source['projections']}
            gaps=[dot(m,vs(p,w)) for m,p in zip(target['facets'],target['hull']) for w in points]
            lo=minimum(gaps);contained=sign(lo)>=0;equal=contained and set(target['hull'])<=points
            valid.append({'cosine':enc(c),'scaled_axial_sine':enc(s),'contained':contained,'equal':equal,'minimum_original_support_gap':enc(lo)})
        require(len(valid)==2 and {tuple(v['cosine']) for v in valid}=={('1','0'),('-1','0')} and all(v['scaled_axial_sine']==['0','0'] for v in valid),'complete circle roll classifier')
        require(all(v['contained']==(si<=ti) and v['equal']==(si==ti) for v in valid),'threshold containment classification')
        result.append({'source_orbit':si,'receiver_orbit':ti,'all_circle_correspondences':8,'surviving_rolls':sorted(valid,key=lambda x:x['cosine'])})
    return result

def cosets(G,C,refs):
    result=[]
    for i,n in enumerate(refs):
        J=tuple(tuple(sub(div(sc(mul(n[j],n[k]),2),dot(n,n)),identity()[j][k]) for k in range(3)) for j in range(3));proper(J)
        bases=[identity(),J] if i==0 else [identity(),J,C,mm(J,C)]
        sets=[{mm(b,g) for g in G} for b in bases]
        require(all(len(s)==60 for s in sets) and all(not a&b for a,b in combinations(sets,2)),'coset sizes/disjointness')
        allQ=set().union(*sets);reversal=next(g for g in G if act(g,n)==vc(n,-1))
        require({mm(reversal,Q) for Q in allQ}==allQ,'normal reversal or representative ambiguity changes classification')
        result.append({'reference_orbit':i,'disjoint_left_cosets':len(sets),'proper_closed_orientations':len(allQ),'equal_orientations':120,'unequal_orientations':120*i,'normal_reversal_set_invariance_verified':True})
    return result

def controls():
    good=[[q,0,128,0] for q in range(4)];validate_runs(good)
    failures=[lambda:validate_runs(good[:-1]),lambda:validate_runs(good+[[0,0,1,0]]),lambda:validate_runs([[0,0,128,192]]+good[1:]),
              lambda:idi((F(1),F(2)),(F(0),F(1))),lambda:sqrt_field((-1,0)),
              lambda:require(bernstein_lower((F(0),F(0)),(F(0),F(0)),(F(1),F(1)),F(0),F(1),F(0))[0]>0,'false positive polynomial')]
    for f in failures:
        try:f()
        except ValueError:pass
        else:raise ValueError('malformed control accepted')
    require(ia((F(-1),F(2)),(F(3),F(4)))==(F(2),F(6)) and isc((F(-1),F(2)),-3)==(F(-6),F(3)),'signed interval controls')
    return len(failures)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base-audit',type=Path,required=True);p.add_argument('--output',type=Path);args=p.parse_args()
    kernel=load_kernel(args.base_audit);tests=controls();V2=kernel.original_vertices();V=[vc(v,F(1,2)) for v in V2]
    G=body_group(V);global_data,_=kernel.global_audit(V2);kernel.boundary_geometry(V2)
    beta=div(sub((19,0),sc(PH,8)),(29,0));refs=((ZERO,ONE,sc(add(ONE,PH),-3)),(ZERO,ONE,div(sub(sc(PH,3),ONE),(11,0))))
    orbits=orbit_audit(V,G,refs,beta);B=kernel.chart()[1];source=shadow(V,B,12);shadows=[shadow(V,n,16) for n in refs]
    for h in shadows:require(len(h['circle'])==8 and h['radius2']==sub((11,4),beta),'threshold maximum circle')
    require(len(source['circle'])==12 and source['radius2']==sub((11,4),(F(1,3),0)),'threefold maximum circle')
    for corner in source['hull']:
        preimages=[v for v in V if project(v,B)==corner]
        require(len(preimages)==1 and sc(mul(dot(preimages[0],B),dot(preimages[0],B)),3)==dot(B,B),'unique actual corner preimage and original axial height')
    rho6=sub(add(sc(PH,4),(F(8,3),0)),(9,0));require(sign(rho6)>0,'winning tangent disk exceeds radius3')
    # On the positive hemisphere sin is increasing with chord a in [0,sqrt2].
    # At a>=1/24, f<=c0-3*sin(a), which is already below sqrt(beta).
    c0=sqrt_field((F(1,3),0));sin_cut=sqrt_field((F(2303,2304),0));beta_root=sqrt_field(beta)
    require(c0[1]-F(1,8)*sin_cut[0]<beta_root[0],'global winning-source chord bound')
    radius=sqrt_field((11,4));eta=F(2687,96000)
    require(c0[1]/24+radius[1]/1152<eta,'actual original corner transport error bound')
    covers=[closed_arc_cover(source,t) for t in shadows];R,C=alignments(G)
    nearest=lambda n:scaled(n,div(minimum([dot(v,n) for v in V if sign(dot(v,n))>0]),dot(n,n)))
    require(act(R,nearest(refs[0]))==nearest(refs[1]) and act(R,nearest(refs[1]))==nearest(refs[0]),'proper positive normal alignment')
    rolls=circle_rolls(V,shadows,R);orientations=cosets(G,C,refs)
    area_expected=[div(add((137984,0),sc(PH,223232)),(145,0)),div(add((29056,0),sc(PH,45888)),(29,0))]
    require([h['area2'] for h in shadows]==area_expected and sign(sub(area_expected[1],area_expected[0]))>0,'exact physical areas')
    third=(F(1,7),0);scores=global_data['regional_maximum_squared_spectrum_sqrt5_basis']
    other=[tuple(map(F,x)) for x,count in scores if tuple(map(F,x)) not in [(F(1,3),F(0)),beta]]
    require(minimum([sub(third,x) for x in other])==ZERO,'next regional gap is not1/7')
    result={'agent':'six-reviewer-2','role':'independent mathematical reviewer','target_python_modules_imported':False,
            'arithmetic':'Q(sqrt5) coefficient pairs with independently bracketed80-bit dyadic square roots; rational outward intervals',
            'previous_reviewer2_kernel_sha256':BASE_SHA,'global_regions_reconstructed':436,'full_proper_group_by_ordered_vertex_images':60,
            'threshold_orbits_and_exact_tangent_inradii':orbits,'full_threshold_corners':[len(h['hull']) for h in shadows],
            'full_threshold_maximum_circle_points':[len(h['circle']) for h in shadows],'original_target_support_checks':1920,'original_source_support_checks':720,
            'closed_arc_winning_source_separation':covers,'all_threshold_circle_and_original_support_comparisons':rolls,
            'all_surviving_roll_original_support_checks':7680,'closed_threshold_orientation_cosets':orientations,
            'exact_proper36degree_matrix_sqrt5_basis':[field_vector_encode(row) for row in C],
            'squared_physical_shadow_areas_sqrt5_basis':[enc(x) for x in area_expected],
            'proved_next_regional_source_class_gap_squared':'1/7','positive_dyadic_roots_verified':len(ROOTS),
            'malformed_interval_or_coverage_controls_rejected':tests,'global_non_rupert_proved':False,'continuous_bridges':'Written audit in REVIEW.md; not formalized.'}
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
if __name__=='__main__':main()
