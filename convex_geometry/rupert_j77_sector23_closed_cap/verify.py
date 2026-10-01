"""Exact finite hypotheses for the whole closed J77 sector23 cap.

six-rupert-2, researcher. Python3.11+ standard library, Q(sqrt5).
Unformalized continuous source-roll and containment bridges are in PROOF.md.
"""
import argparse
import copy
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
def require(ok,message):
    if not ok:raise ValueError(message)
manifest=json.loads((HERE/'dependencies.json').read_text())
PARENT='convex_geometry/rupert_j77_closed_collar_rigidity'
COMMIT='8557209a7f59ae37f3e51ab8bac2ebb7fe349b77'
require(len(manifest)==1,'one complete mathematical parent')
dep=manifest[0]
require(set(dep)=={'source_directory','source_commit','sha256'} and dep['source_directory']==PARENT and
        dep['source_commit']==COMMIT and set(dep['sha256'])=={'.gitignore','README.md','PROOF.md','verify.py',
        'certificates.json','dependencies.json','expected.json'},'complete original parent pins')
for name,digest in dep['sha256'].items():
    require(sha256((REPO/PARENT/name).read_bytes()).hexdigest()==digest,'changed original parent '+name)
spec=importlib.util.spec_from_file_location('j77_sector23_rigidity_parent',REPO/PARENT/'verify.py')
P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
A,R,Q=P.C.A,P.C.R,P.Q
dot,cross,add,sub,scale=A.dot,A.cross,A.add,A.sub,A.scale
sg,pos,nonneg,enc,digest=A.sg,P.pos,P.nonneg,P.enc,P.M.digest
e=(Q(1),Q(),Q())
D,CR,E,B,MARGIN=F(1,200),F(1001,1000),F(353,10000),F(1,20),F(1,1000)
AMIN=F(7,10)
RAW=[['1','0','0'],['1','-1/75','1/150'],['1','-1/50','0']]
BOUNDS={'physical_chord_upper':'1/200','outer_error':'353/10000','outer_coefficient_sum':'1/50',
        'remote_half_tangent':'1/20','Bernstein_margin':'1/1000','Gamma':'61/10',
        'near_roll_ratio':'10/3','full_angle_ratio':'10','Cayley_ratio':'501/100'}
def gate(value,label):pos(Q(value),label);return value
def configuration(data):
    require(set(data)=={'agent','role','receiving_sector','bounds','raw_outer_triangle','roll'},'complete new certificate keys')
    require(data['agent']=='six-rupert-2' and data['role']=='researcher' and data['receiving_sector']==23,'original author and receiving sector')
    require(data['bounds']==BOUNDS and data['raw_outer_triangle']==RAW,'whole closed cap and explicit outer domain')
    return tuple(tuple(Q(F(x)) for x in row) for row in RAW)

def geometry(raw):
    V,core,axis,lift,integer_vertices=A.originals()
    require(tuple(V)==tuple(P.V),'identical actual original55 vertices')
    d0=(Q(),Q(-2)/3,Q(1)/3);d1=(Q(),Q(-1),Q())
    require(raw==(e,add(e,scale(Q(1)/50,d0)),add(e,scale(Q(1)/50,d1))),'actual receiver rays and enclosing triangle')
    difference=sub(d1,d0);den=dot(difference,difference);gate(den,'distinct actual receiving rays')
    parameter=-dot(d0,difference)/den
    candidates=[dot(d,d) for d in (d0,d1)]
    if sg(parameter)>=0 and sg(1-parameter)>=0:
        point=add(d0,scale(parameter,difference));candidates.append(dot(point,point))
    for value in candidates:gate(value-AMIN*AMIN,'whole actual receiving ray segment norm above7over10')
    for ray in (d0,d1):nonneg(1-dot(ray,ray),'actual receiving rays have norm at most1')
    gates={'physical_to_raw_ratio':CR*(1-D*D/2)-1,
           'entire_sector_outer_coefficient_sum':4*AMIN-CR,
           'strict_outer_triangle_enclosure':F(1,50)*AMIN-CR*D,
           'raw_radius_inside_parent_stress_domain':Q(P.CR*P.D)-Q(CR*D)}
    # Equality of the two raw-ball budgets, never an extrapolation.
    require(gates.pop('raw_radius_inside_parent_stress_domain')==0,'same certified receiving stress radius')
    for name,value in gates.items():gate(value,name)
    facets,generators,counts,edges,rank=A.all_facets(V,lift,integer_vertices)
    middle=scale(Q(1)/3,tuple(sum((u[j] for u in raw),Q()) for j in range(3)))
    signs=[];fan=[]
    for record in facets:
        vector=record['area_vector'];sign=sg(dot(vector,middle))
        require(sign!=0,'generic sector interior not on original physical area wall')
        corners=[sign*dot(vector,u) for u in raw]
        for value in corners:nonneg(value,'entire outer triangle in one closed actual physical area cell')
        signs.append(sign);fan.append(corners)
    C=scale(Q(1)/2,tuple(sum((row['area_vector'][j]*sign for row,sign in zip(facets,signs)),Q()) for j in range(3)))
    require(C==(Q(49,25)/8,Q(-23)/8-Q(0,F(57,40)),Q(3)/4-Q(0,F(3,5))),'fresh physical area vector')
    for u in raw:gate(dot(C,u),'physical area numerator positive on entire outer triangle')
    # Independent area reconstruction from the actual perturbed shadow hull.
    f1=(-middle[1],Q(1),Q());f2=(-middle[2],Q(),Q(1))
    require(cross(f1,f2)==middle,'actual positive projection chart')
    labels={}
    for j,v in enumerate(V):labels.setdefault((dot(f1,v),dot(f2,v)),j)
    points=sorted(labels)
    def hull_chain(items):
        out=[]
        for point in items:
            while len(out)>=2:
                a,b=out[-2:]
                turn=(b[0]-a[0])*(point[1]-a[1])-(b[1]-a[1])*(point[0]-a[0])
                if sg(turn)>0:break
                out.pop()
            out.append(point)
        return out
    hull=hull_chain(points)[:-1]+hull_chain(list(reversed(points)))[:-1]
    ids=[labels[point] for point in hull];cycle=list(zip(ids,ids[1:]+ids[:1]))
    C2=scale(Q(1)/2,tuple(sum((cross(V[a],V[b])[j] for a,b in cycle),Q()) for j in range(3)))
    require(C2==C,'actual original shadow cycle and Cauchy physical area agree')
    support_count=0
    for a,b in cycle:
        for u in raw:
            normal=cross(sub(V[b],V[a]),u)
            for v in V:
                nonneg(dot(normal,sub(V[a],v)),'every original receiving support on complete outer triangle')
                support_count+=1
    old_raw=[tuple(Q(F(x)) for x in row) for row in json.loads((REPO/PARENT/'certificates.json').read_text())['raw_triangle']]
    barycentric=[]
    for u in old_raw:
        r=sub(u,e);s0=3*r[2];s1=-r[1]-2*r[2]
        weights=[1-50*(s0+s1),50*s0,50*s1]
        for weight in weights:nonneg(weight,'old collar inside actual new sector triangle')
        require(sum(weights,Q())==1 and tuple(sum((weight*v[j] for weight,v in zip(weights,raw)),Q()) for j in range(3))==u,
                'exact old collar barycentric inclusion')
        barycentric.append(weights)
    return {'raw_outer_triangle':raw,'actual_receiver_rays':[d0,d1],
        'entire_receiving_segment_norm_squared_candidates':candidates,'segment_stationary_parameter':parameter,
        'whole_sector_enclosure_gates':gates,'complete_original_facets':len(facets),
        'original_hull_counts':dict(counts),'area_fan_corner_gates':fan,
        'physical_area_vector':C,'independent_actual_shadow_hull':ids,
        'complete_actual_shadow_support_comparisons':support_count,
        'prior_closed_collar_barycentric_inclusion':barycentric},C

def roll(data,geo):
    require(set(data)=={'norms_upper','covers','near'},'roll certificate keys')
    V,S,labels,M,H,fixed,E0,factor=geo
    U=tuple(map(F,data['norms_upper']))
    require(len(U)==10,'all ten actual normal norms')
    for m,u in zip(M,U):
        require(u>0,'positive normal norm bound');nonneg(Q(u*u)-dot(m,m),'whole actual normal Euclidean bound')
    roots=[(0,['-1','-1/20']),(0,['1/20','1'])]+[(family,['-1','1']) for family in (1,2,3)]
    require(len(data['covers'])==5,'all five complete closed O2 roots')
    records=[];nodes=0;depth=0
    for root_id,(cover,(family,root)) in enumerate(zip(data['covers'],roots)):
        require(set(cover)=={'family','interval','leaves'} and cover['family']==family and cover['interval']==root,
                'actual full directed O2 family and exact closed root endpoints')
        count,dp=R.closed_tree(cover['leaves']);nodes+=count;depth=max(depth,dp)
        for leaf in cover['leaves']:
            require(set(leaf)=={'path','edges','source_vertices'},'fixed original leaf witness')
            a,z=R.interval(root,leaf['path']);points=R.source_points(leaf['source_vertices'],V)
            weights,c=R.polynomial(family,leaf['edges'],points,M,H,U,E)
            bern=R.bernstein(c,a,z)
            for value in bern:gate(value-Q(MARGIN),'fresh whole closed roll interval margin')
            records.append({'root':root_id,'family':family,'path':leaf['path'],'closed_interval':[a,z],
                'edges':leaf['edges'],'original_source_vertices':leaf['source_vertices'],
                'positive_translation_balanced_weights':weights,'quadratic':c,'Bernstein':bern})
    require(nodes==2*len(records)-5,'complete five-root full binary forest')
    require(len(data['near'])==2,'both signed near-roll contacts')
    near=[]
    for row,expected_sign in zip(data['near'],(1,-1)):
        require(set(row)=={'sign','edges','source_vertices'} and row['sign']==expected_sign and row['edges']==[0,5],
                'actual two signed near-contact branches')
        ids=row['edges'];points=R.source_points(row['source_vertices'],V);weights=R.balanced(ids,M)
        require(len(points)==2,'both original near contacts')
        for i,point in zip(ids,points):require(dot(M[i],point)==H[i],'actual original zero-roll support equality')
        height=sum((w*H[i] for i,w in zip(ids,weights)),Q())
        norm=sum((w*U[i] for i,w in zip(ids,weights)),Q())
        torque=sum((w*expected_sign*(-2*M[i][0]*point[1]+2*M[i][1]*point[0]) for i,w,point in zip(ids,weights,points)),Q())
        require(height==Q(11,5)/6 and norm==Q(F(769421,375000)),'actual weighted near-contact constants')
        require(torque==Q(8 if expected_sign==1 else 7)/3+Q(0,1),'actual original directed near torque')
        near.append({'sign':expected_sign,'edges':ids,'original_source_vertices':row['source_vertices'],
                     'positive_weights':weights,'physical_contact_height':height,'norm_upper':norm,'directed_torque':torque})
    return {'new_outer_error':E,'closed_remote_guard':B,'closed_full_O2_families':4,'closed_roots':5,
            'leaves':len(records),'nodes':nodes,'maximum_depth':depth,
            'strict_Bernstein_tests':3*len(records),'direct_full_matrix_identity_tests':3*len(records),
            'strict_margin':MARGIN,'minimum_Bernstein_coefficient':min(v for row in records for v in row['Bernstein']),
            'fixed_closed_records':records,'signed_near_records':near}

def moving_and_gauge(C,near):
    gamma,cs,hc,kt=F(61,10),F(427,200),F(5643,800),F(10,3)
    require(cs==F(7,20)*gamma and hc==F(9,4)*(1+cs),'actual inverse-area and original pairing constants')
    gates={'actual_area_tangent_norm':Q(gamma*gamma)-C[1]*C[1]-C[2]*C[2],
           'whole_sector_area_inside_global_tenth_budget':Q(F(1,10)-gamma*D),
           'new_uniform_error_strictly_contains_moving_error':Q(E-hc*D),
           'source_chord_inside_new_arcsine_domain':Q(F(1,80)-cs*D),
           'receiving_chord_inside_new_arcsine_domain':Q(F(1,80)-D),
           'fresh_arcsine_derivative_domain':Q(CR*CR*(1-F(1,160)**2)-1),
           'moving_near_threshold_inside_remote_guard':Q(B-kt*D),
           'full_spatial_angle_below10delta':Q(10-CR*(1+cs)-2*kt),
           'actual_Cayley_radius_below501over100delta':Q(P.L0*(1-F(25,2)*D*D)-5),
           'same_actual_companion_right_body_gauge':Q(1-(20+2*CR)*D),
           'positive_actual_companion_denominator':Q(1-P.L0*CR*D*D),
           'unique_nearest_receiving_signed_axis':Q(1-D*D/2-F(81,100)-D)}
    for row in near:
        height,norm,torque=row['physical_contact_height'],row['norm_upper'],row['directed_torque']
        tag=str(row['sign'])
        gates['both_signed_moving_lower_'+tag]=kt*torque-hc*norm-kt*kt*(2*height+hc*norm*D)*D
        gates['both_signed_moving_guard_'+tag]=torque*B-(2*height+hc*norm*D)*B*B-hc*norm*D
    axes=[];v=e
    for j in range(5):
        require(dot(v,v)==1,'actual signed mirror axis norm')
        if j:gate(Q(F(81,100))-A.absq(dot(e,v)),'actual other mirror axis cosine')
        axes.extend([v,scale(-1,v)]);v=P.M.rotate(v)
    require(v==e and len(set(axes))==10,'all ten actual signed mirror axes')
    separations=[]
    for i,a in enumerate(axes):
        for b in axes[i+1:]:
            value=dot(sub(a,b),sub(a,b));gate(value-Q(F(9,25)),'actual signed source-axis separation')
            separations.append(value)
    gates['source_axis_balls_disjoint']=Q(F(3,5)-2*cs*D)
    base=[(Q(1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1))]
    images=base[:];vertices=list(P.V);matrices=[];cosines=[]
    for j in range(5):
        require(set(vertices)==set(P.V),'actual proper body permutes original vertices')
        require([[dot(a,b) for b in images] for a in images]==[[Q(int(i==k)) for k in range(3)] for i in range(3)],'actual body orthogonality')
        require(dot(images[0],cross(images[1],images[2]))==1,'actual proper orientation')
        matrices.append([list(row) for row in zip(*images)])
        if j:
            cosine=(sum((images[i][i] for i in range(3)),Q())-1)/2
            gate(Q(F(1,2))-cosine,'every actual nonidentity body angle exceeds1');cosines.append(cosine)
        images=[P.M.rotate(v) for v in images];vertices=[P.M.rotate(v) for v in vertices]
    require(images==base and vertices==list(P.V),'actual order-five closure')
    require(set((-v[0],v[1],v[2]) for v in P.V)==set(P.V),'original body mirror permutation')
    for name,value in gates.items():gate(value,'fresh entire-sector entry '+name)
    return {'Gamma':gamma,'source_chord_ratio':cs,'paired_original_error_ratio':hc,'near_half_tangent_ratio':kt,
            'full_spatial_angle_ratio':10,'Cayley_ratio':P.L0,'scalar_gates':gates,
            'all45_signed_axis_squared_separations':separations,'actual_body_matrices':matrices,
            'actual_nonidentity_cosines':cosines,'whole_sector_absolute91over10000_bound_used':False}

def malformed(data,geo):
    tests=[]
    for change in ['domain','error','radius','sector']:
        bad=copy.deepcopy(data)
        if change=='domain':bad['raw_outer_triangle'][1][1]='-1/7'
        elif change=='error':bad['bounds']['outer_error']='1269/40000'
        elif change=='radius':bad['bounds']['physical_chord_upper']='1/100'
        else:bad['receiving_sector']=22
        tests.append(lambda bad=bad:configuration(bad))
    for change in ['family','endpoint','missing_child','duplicate','source','balance','norm','near_sign','near_vertex']:
        bad=copy.deepcopy(data['roll'])
        if change=='family':bad['covers'].pop()
        elif change=='endpoint':bad['covers'][0]['interval'][1]='-1/19'
        elif change=='missing_child':bad['covers'][2]['leaves'].pop()
        elif change=='duplicate':bad['covers'][0]['leaves'].append(copy.deepcopy(bad['covers'][0]['leaves'][0]))
        elif change=='source':bad['covers'][0]['leaves'][0]['source_vertices'][0]=55
        elif change=='balance':bad['covers'][0]['leaves'][0]['edges']=[0,4]
        elif change=='norm':bad['norms_upper'][0]='1'
        elif change=='near_sign':bad['near'].pop()
        else:bad['near'][1]['source_vertices']=[24,16]
        tests.append(lambda bad=bad:roll(bad,geo))
    for test in tests:
        try:test()
        except (ValueError,KeyError,IndexError,TypeError,ZeroDivisionError):continue
        raise ValueError('Malformed entire-sector certificate accepted')
    return len(tests)

def check(self_test):
    # Full old evidence before any new predicate enters either sign registry.
    old=P.check(True);old_bytes=(json.dumps(old,indent=1)+'\n').encode()
    require(old_bytes==(REPO/PARENT/'expected.json').read_bytes(),'EVERY complete parent byte')
    require(P.D==D and P.CR==CR,'identical physical/raw budgets in new signed machinery')
    data=json.loads((HERE/'certificates.json').read_text());raw=configuration(data)
    area_geometry,C=geometry(raw);geo=R.geometry();roll_record=roll(data['roll'],geo)
    moving=moving_and_gauge(C,roll_record['signed_near_records'])
    parent_fixture=json.loads((REPO/PARENT/'certificates.json').read_text())
    case=next(row for row in json.loads((REPO/'convex_geometry/rupert_j77_uniform_local_exclusion/certificates.json').read_text())['cases'] if row['parent']==23)
    index={v:j for j,v in enumerate(P.V)};permutation=[index[P.M.rotate(v)] for v in P.V]
    balance=next(row for row in json.loads((REPO/'convex_geometry/rupert_j77_receiving_balanced_stress/certificates.json').read_text())['cases'] if row['parent']==23)
    critical=next(row for row in json.loads((REPO/'convex_geometry/rupert_j77_bilinear_mirror_cap/certificates.json').read_text())['cases'] if row['parent']==23)
    stress=P.receiving_stress(case,balance,critical,permutation)
    duals,chis,norms,contacts=P.fresh_geometry(case,permutation,raw,stress,parent_fixture)
    chain=P.chain(parent_fixture,duals,chis,norms,stress)
    universal=P.PB.universal_factorization()
    controls=malformed(data,geo) if self_test else 0
    for registry in [P.M.area,P.C.A]:
        for pair,sign in tuple(registry.SIGNS.items()):require(registry.interval_sign(pair)==sign,'independent rational positive-sqrt5 enclosure')
    return enc({'agent':'six-rupert-2','role':'researcher','target':'original asymmetric55vertex unit-edge J77',
        'proof_status':'complete author-checked written intermediate proof with exact finite hypotheses; unformalized',
        'independent_review_asserted':False,'global_J77_Rupert_resolved':False,
        'whole_closed_sector23_cap_strict_passage_excluded':True,'physical_chord_upper':'1/200',
        'receiving_sector_definition':'u=e+s0(0,-2/3,1/3)+s1(0,-1,0), s0,s1>=0; n=u/||u||; ||n-e||<=1/200',
        'all_original_sources_full_roll_arbitrary_translation_scale_ge1':True,
        'closed_classification':'lambda1,t0,Qh=I or M_nM_q; actual RIGHT C5 body factor; both equal shadows',
        'axis_case':'delta0 classified by fully replayed complete mirror-cap parent8206',
        'complete_direct_parent_replay':{'directory':PARENT,'bytes':len(old_bytes),'sha256':sha256(old_bytes).hexdigest()},
        'fresh_entire_sector_area_and_enclosure':area_geometry,'fresh_complete_O2_roll_cover':roll_record,
        'fresh_moving_and_same_gauge':moving,'fresh_receiving_stress':stress,
        'fresh_original_contact_geometry':contacts,'fresh_positive_coordinate_stresses':duals,
        'directed_signed_chain':chain,'universal_receiving_balanced_factorization':universal,
        'malformed_controls':controls,'fixture_sha256':digest(data),
        'registered_independent_sign_counts_by_parent_registry':[len(P.M.area.SIGNS),len(P.C.A.SIGNS)],
        'remaining_frontier':'other receiving sectors, larger complete caps and the global named-solid decision remain OPEN'})

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--self-test',action='store_true');parser.add_argument('--emit',action='store_true')
    args=parser.parse_args();result=check(args.self_test);encoded=(json.dumps(result,indent=1)+'\n').encode()
    if not args.emit:require(encoded==(HERE/'expected.json').read_bytes(),'EVERY expected output byte; run --self-test')
    print(encoded.decode(),end='')
