"""Exact J77 inverse-area and all-source collar reduction.

six-rupert-2, researcher. Python 3.11+, standard library, no floating predicates.
The unformalized continuous bridges and theorem scope are in PROOF.md.
"""
import argparse
import copy
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
def require(ok,message):
    if not ok:raise ValueError(message)
manifest=json.loads((HERE/'dependencies.json').read_text())
require(isinstance(manifest,list) and len(manifest)==2,'two direct parent manifests')
parents=[('convex_geometry/rupert_j77_projection_area','cd0088c8aa1e308657b17d759bc5600c7b8b2b34'),
         ('convex_geometry/rupert_j77_area_axis_roll','86dcf1e10d0eddbc26fc8343b6df4fcc642d47c6')]
for dep,(directory,commit) in zip(manifest,parents):
    require(set(dep)=={'source_directory','source_commit','sha256'} and
            dep['source_directory']==directory and dep['source_commit']==commit and
            len(dep['sha256'])==7,'complete fixed direct parent')
    for name,digest in dep['sha256'].items():
        require(sha256((REPO/directory/name).read_bytes()).hexdigest()==digest,'parent bytes: '+name)
PARENT=REPO/parents[1][0]
spec=importlib.util.spec_from_file_location('j77_inverse_roll_parent',PARENT/'verify.py')
R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
A=R.area
Q,add,sub,dot,cross,scale=A.Q,A.add,A.sub,A.dot,A.cross,A.scale
sg,pos=A.sg,A.positive
sq=lambda x:x*x
e=(Q(1),Q(),Q())
decode=lambda v:tuple(Q(F(x[0]),F(x[1])) for x in v)
enc=R.enc
digest=R.digest

GB={'maximum_excess':'1/10','first_coarse_chord':'1/8','first_linear_factor':'3/7',
    'second_coarse_chord':'3/70','linear_chord_factor':'7/20'}
CB={'physical_chord_lower':'1/500','physical_chord_upper':'1/200','area_excess_upper':'13/500',
    'source_chord_upper':'91/10000','scale_squared_upper':'501/500','outer_error':'1269/40000',
    'remote_half_tangent':'1/20','near_half_tangent':'1/60','principal_full_angle_upper':'1/20',
    'Bernstein_margin_lower':'1/1000'}
RAW=[['1','-1/450','1/900'],['1','-1/300','0'],['1','-1/225','1/450']]
MAX2=['280834381/3240080','31130667/810020']

def configuration(fixture):
    require(set(fixture)=={'global_budget','raw_triangle','collar_bounds',
                           'maximum_physical_area_squared','roll'},'certificate keys')
    require(fixture['global_budget']==GB,'stated global budget and factors')
    require(fixture['collar_bounds']==CB,'stated physical collar and motion bounds')
    require(fixture['raw_triangle']==RAW,'actual closed raw receiving triangle')
    require(fixture['maximum_physical_area_squared']==MAX2,'stated exact area maximum')
    return tuple(tuple(Q(F(x)) for x in row) for row in fixture['raw_triangle'])

def inverse_area_gates():
    parent=json.loads((REPO/parents[0][0]/'expected.json').read_text())
    A0=Q(F(parent['complete_area_zonotope']['minimum_area'][0]),
         F(parent['complete_area_zonotope']['minimum_area'][1]))
    A12=Q(*map(F,parent['complete_area_zonotope']['next_distinct_facet_distance_squared']))
    rho2=Q(*map(F,parent['global_source_localization']['tangent_inradius_squared']))
    require(A0==Q(49,25)/8 and A12==Q(725)/8+Q(0,F(1621,40)) and
            rho2==Q(169)/32+Q(0,F(359,160)),'freshly replayed original area constants')
    require(A0*A0+rho2-A12==1,'entire sublevel radical and monotone branch gap')
    gates={'next_polar_level_below_tangent_peak':A0*A0+rho2-A12,
      'minimum_area_lower13':A0-13,'minimum_area_upper105_over8':Q(105)/8-A0,
      'tangent_radius_lower16_over5':rho2-sq(Q(16)/5),
      'tenth_budget_below_next_polar_level':A12-sq(A0+Q(1)/10),
      'polar_chord_one_eighth':A0-(1-Q(1)/128)*(A0+Q(1)/10),
      'first_sine_lower':1-Q(1)/256-sq(Q(499)/500),
      'first_linear_source_ratio':Q(16)/5*Q(499)/500-Q(105)/128-Q(7)/3,
      'second_sine_lower':1-sq(Q(3)/70)/4-sq(Q(999)/1000),
      'second_linear_source_ratio':Q(16)/5*Q(999)/1000-Q(105)/8*Q(3)/140-Q(20)/7}
    for name,value in gates.items():pos(value,name)
    return A0,A12,rho2,gates

def maximum_area(C,u):
    area2=lambda v:sq(dot(C,v))/dot(v,v)
    candidates=[{'kind':'corner','id':j,'raw':v,'area_squared':area2(v)} for j,v in enumerate(u)]
    controls=[]
    for i,j in ((0,1),(1,2),(2,0)):
        a=u[i];d=sub(u[j],a);aa,bb=dot(C,a),dot(C,d)
        n0,n1,n2=dot(a,a),dot(a,d),dot(d,d)
        numerator=aa*n1-bb*n0;denominator=bb*n1-aa*n2
        if denominator==0:
            controls.append({'edge':[i,j],'constant_area':numerator==0,
                             'nonzero_derivative_if_not_constant':-numerator})
            continue
        t=numerator/denominator
        feasible=sg(t)>0 and sg(1-t)>0
        controls.append({'edge':[i,j],'stationary_parameter':t,'admitted':feasible})
        if feasible:
            v=add(a,scale(t,d))
            candidates.append({'kind':'edge_stationary','edge':[i,j],'parameter':t,
                               'raw':v,'area_squared':area2(v)})
    pos(C[0],'positive interior critical raw chart')
    stationary=scale(1/C[0],C)
    basis=[sub(u[1],u[0]),sub(u[2],u[0])];rhs=sub(stationary,u[0])
    determinant=dot(e,cross(*basis));require(determinant!=0,'raw triangle nondegenerate')
    coefficients=[dot(e,cross(rhs,basis[1]))/determinant,
                  dot(e,cross(basis[0],rhs))/determinant]
    weights=[1-sum(coefficients,Q()),*coefficients]
    admitted=all(sg(t)>=0 for t in weights)
    if admitted:candidates.append({'kind':'interior_stationary','raw':stationary,'area_squared':area2(stationary)})
    maximum=candidates[0]['area_squared']
    for c in candidates[1:]:
        if sg(c['area_squared']-maximum)>0:maximum=c['area_squared']
    for c in candidates:require(sg(maximum-c['area_squared'])>=0,'every complete maximum candidate compared')
    return {'complete_candidates':candidates,'edge_stationary_admission':controls,
            'interior_stationary_barycentric':weights,'interior_stationary_admitted':admitted,
            'maximum_squared':maximum,'maximizing_candidates':[c for c in candidates if c['area_squared']==maximum]}

def collar_geometry(u,A0):
    V,core,axis,vs,W=A.originals()
    facets,B,counts,edges,rank=A.all_facets(V,vs,W)
    d0=(Q(),Q(-2)/3,Q(1)/3);d1=(Q(),Q(-1),Q())
    require(u==(add(e,scale(Q(1)/300,d0)),add(e,scale(Q(1)/300,d1)),add(e,scale(Q(1)/150,d0))),
            'original explicit receiving rays')
    require(all(t[0]==1 for t in u),'positive normalization chart throughout triangle')
    require(dot(e,cross(sub(u[1],u[0]),sub(u[2],u[0])))!=0,'nondegenerate receiving triangle')
    q=tuple(sub(v,e) for v in u);qmin=dot(q[0],q[0]);qmax=dot(q[2],q[2])
    for t in q:
        require(sg(dot(q[0],sub(t,q[0])))>=0,'whole triangle nearest raw point')
        require(sg(qmax-dot(t,t))>=0,'every raw corner norm compared')
    require(qmin==Q(1)/162000 and qmax==Q(1)/40500,'exact entire raw norm extrema')
    chord_gates={'lower_physical_chord':sq(1-Q(1)/(2*500**2))*(1+qmin)-1,
                 'upper_physical_chord':Q(1)/200**2-qmax,
                 'all_other_signed_axes':1-Q(1)/(2*500**2)-(Q(81)/100+Q(1)/200)}
    for name,value in chord_gates.items():pos(value,name)
    orbit=[];v=e
    for j in range(5):
        require(dot(v,v)==1,'actual mirror axis norm')
        if j:pos(Q(81)/100-A.absq(dot(e,v)),'other mirror axis cosine')
        orbit.append(v);v=A.body_rotation(axis,v)
    require(v==e,'actual body C5 orbit closure')
    require({A.body_rotation(axis,v) for v in core}==core,'actual proper core permutation')
    require({(-v[0],v[1],v[2]) for v in core}==core,'actual reflection core permutation')
    interior=scale(Q(1)/3,tuple(sum((v[t] for v in u),Q()) for t in range(3)))
    signs=[];sign_gates=[]
    for record in facets:
        b=record['area_vector'];sign=sg(dot(b,interior))
        require(sign!=0,'interior not on an area wall')
        gates=[dot(b,t)*sign for t in u]
        require(all(sg(t)>=0 for t in gates),'entire triangle in one closed actual area fan cell')
        signs.append(sign);sign_gates.append(gates)
    C=scale(Q(1)/2,tuple(sum((r['area_vector'][k]*s for r,s in zip(facets,signs)),Q()) for k in range(3)))
    require(C==(A0,Q(-23)/8-Q(0,F(57,40)),Q(3)/4-Q(0,F(3,5))),'physical area vector')
    for t in u:pos(dot(C,t),'positive area numerator throughout triangle')
    # A second physical-area reconstruction from the actual original shadow hull.
    f1=(-interior[1],Q(1),Q());f2=(-interior[2],Q(),Q(1))
    require(cross(f1,f2)==interior,'positive raw projection chart orientation')
    coordinates={}
    for j,v in enumerate(V):coordinates.setdefault((dot(f1,v),dot(f2,v)),j)
    points=sorted(coordinates)
    def chain(items):
        out=[]
        for p in items:
            while len(out)>=2:
                a,b=out[-2:]
                turn=(b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
                if sg(turn)>0:break
                out.pop()
            out.append(p)
        return out
    hull=chain(points)[:-1]+chain(list(reversed(points)))[:-1]
    ids=[coordinates[p] for p in hull]
    cyclic=list(zip(ids,ids[1:]+ids[:1]))
    Ch=scale(Q(1)/2,tuple(sum((cross(V[a],V[b])[k] for a,b in cyclic),Q()) for k in range(3)))
    require(Ch==C,'direct actual shadow hull equals the physical Cauchy area vector')
    support_count=0
    for a,b in cyclic:
        for t in u:
            normal=cross(sub(V[b],V[a]),t)
            for v in V:
                require(sg(dot(normal,sub(V[a],v)))>=0,'all actual receiving supports throughout closed triangle')
                support_count+=1
    maximum=maximum_area(C,u)
    require(maximum['maximum_squared']==Q(*map(F,MAX2)),'complete exact physical area maximum')
    eta=Q(13)/500
    pos(sq(A0+eta)-maximum['maximum_squared'],'strict physical area budget on entire triangle')
    pos(Q(1)/10-eta,'new receiving budget inside new global sublevel theorem')
    require(Q(7)/20*eta==Q(91)/10000,'derived all-source signed chord budget')
    require(1+eta/13==Q(501)/500,'derived strict scale-squared budget')
    # Entire-triangle separation from every explicitly named old receiving region.
    zero_vertex=next(v for v in sorted(core) if v[0]==0)
    require(zero_vertex in V and zero_vertex[0]==0,'actual zero-height core vertex')
    z=Q(7,1)/2;D=(Q(),Q(-1),z);D2=dot(D,D)
    height=min(A.absq(dot(v,D)) for v in core)
    fD2=height*height/D2
    require(fD2==Q(65,10)/596,'actual old diameter-center core height')
    old_gates={'diameter_center_height_gt3_over8':fD2-sq(Q(3)/8),
               'diameter_cap_height_separation':Q(51)/160-Q(9)/800,
               'winning_threshold_separation':Q(1)/12-sq(Q(9)/800)}
    for name,value in old_gates.items():pos(value,name)
    require(Q(3)/8-Q(9)/4/40==Q(51)/160,'entire old diameter-cap Lipschitz separation')
    old_triangles=[[(Q(),Q(-1),z),(Q(),Q(-13)/11,z),(Q(1)/10,Q(-25)/24,z)],
                   [(Q(),Q(-1),z),(Q(),Q(-17)/20,z),(Q(1)/20,Q(-17)/20,z)]]
    cone_records=[]
    for ti,triangle in enumerate(old_triangles):
        for j in range(5):
            for reflect in (False,True):
                cols=[((-v[0],v[1],v[2]) if reflect else v) for v in triangle]
                determinant=dot(cols[0],cross(cols[1],cols[2]))
                require(determinant!=0,'old receiving cone independent rays')
                values=[]
                for t in u:
                    values.append([dot(t,cross(cols[1],cols[2]))/determinant,
                                   dot(cols[0],cross(t,cols[2]))/determinant,
                                   dot(cols[0],cross(cols[1],t))/determinant])
                positive=[k for k in range(3) if all(sg(row[k])>0 for row in values)]
                negative=[k for k in range(3) if all(sg(row[k])<0 for row in values)]
                require(positive and negative,'whole new triangle outside both signs of old receiving cone')
                cone_records.append({'old_triangle':ti,'rotation':j,'reflection':reflect,
                    'barycentric':values,'uniform_positive_coordinate':positive[0],
                    'uniform_negative_coordinate':negative[0]})
            triangle=[A.body_rotation(axis,v) for v in triangle]
    return {'raw_triangle':u,'actual_receiver_rays':[d0,d1],'parent_sector_label':23,
      'raw_norm_minimum_squared':qmin,'raw_norm_maximum_squared':qmax,
      'whole_physical_chord_band':['1/500','1/200'],'nearest_signed_axis':e,
      'chord_gates':chord_gates,'actual_mirror_axis_orbit':orbit,
      'complete_original_facets':len(facets),'original_hull_counts':dict(counts),
      'area_fan_corner_sign_tests':len(sign_gates)*3,'area_fan_sign_records_sha256':digest(sign_gates),
      'actual_original_shadow_hull':ids,'direct_original_support_comparisons':support_count,
      'physical_area_vector':C,'complete_physical_area_maximum':maximum,
      'strict_area_budget_margin_squared':sq(A0+eta)-maximum['maximum_squared'],
      'source_chord_upper':'91/10000','scale_squared_upper':'501/500',
      'older_receiving_separation':{'zero_height_original':V.index(zero_vertex),
       'core_height_upper':'9/800','diameter_center_height_squared':fD2,'diameter_cap_radius':'1/40',
       'winning_height_squared_threshold':'1/12','scalar_gates':old_gates,
       'all20_old_cone_separations':cone_records}},V

def validate_roll(fixture,geo):
    require(set(fixture)=={'norms_upper','covers','near'},'roll certificate keys')
    V,S,labels,M,H,fixed,E0,factor=geo
    U=tuple(map(F,fixture['norms_upper']))
    require(len(U)==10,'all actual shadow normal norms')
    for m,u in zip(M,U):
        require(u>0 and sg(Q(u*u)-dot(m,m))>=0,'actual positive outward normal norm bound')
    E=F(1269,40000);b=F(1,20);x0=F(1,60);margin=Q(F(1,1000))
    require(E==F(9,4)*(F(1,200)+F(91,10000)),'new uniform actual-original Hausdorff error')
    roots=[(0,['-1','-1/20']),(0,['1/20','1'])]+[(j,['-1','1']) for j in (1,2,3)]
    require(len(fixture['covers'])==5,'complete five directed full-circle roots')
    records=[];nodes=0;depth=0
    for root_id,(cover,(family,root)) in enumerate(zip(fixture['covers'],roots)):
        require(set(cover)=={'family','interval','leaves'} and cover['family']==family and
                cover['interval']==root,'all exact closed remote roots and endpoints')
        count,dp=R.closed_tree(cover['leaves']);nodes+=count;depth=max(depth,dp)
        for leaf in cover['leaves']:
            require(set(leaf)=={'path','edges','source_vertices'},'fixed exact leaf witness')
            a,z=R.interval(root,leaf['path'])
            points=R.source_points(leaf['source_vertices'],V)
            weights,c=R.polynomial(family,leaf['edges'],points,M,H,U,E)
            bern=R.bernstein(c,a,z)
            for value in bern:pos(value-margin,'new whole-interval Bernstein margin exceeds1/1000')
            records.append({'root':root_id,'family':family,'path':leaf['path'],'closed_interval':[a,z],
                'edges':leaf['edges'],'original_source_vertices':leaf['source_vertices'],
                'strictly_positive_translation_balanced_weights':weights,'quadratic':c,'Bernstein':bern})
    require(nodes==2*len(records)-5,'complete five-root forest')
    require(len(fixture['near'])==2,'both signed near-roll contacts')
    near_records=[]
    for branch,expected in zip(fixture['near'],(1,-1)):
        require(set(branch)=={'sign','edges','source_vertices'} and branch['sign']==expected,'signed near branch')
        ids=branch['edges'];points=R.source_points(branch['source_vertices'],V)
        require(ids==[0,5] and len(points)==2,'actual opposite near normal pair')
        weights=R.balanced(ids,M)
        for i,p in zip(ids,points):require(dot(M[i],p)==H[i],'actual original zero-roll contacts')
        height=sum((w*H[i] for i,w in zip(ids,weights)),Q())
        N=sum((w*U[i] for i,w in zip(ids,weights)),Q())
        L=sum((w*expected*(-2*M[i][0]*p[1]+2*M[i][1]*p[0])
               for i,w,p in zip(ids,weights,points)),Q())
        pos(height,'positive contact height');pos(N,'positive norm budget');pos(L,'positive directed torque')
        def g(x):return L*x-2*height*x*x-E*N*(1+x*x)
        pos(g(x0),'lower closed near-roll obstruction endpoint')
        pos(g(b),'upper closed near-roll obstruction endpoint')
        near_records.append({'sign':expected,'edges':ids,'original_source_vertices':branch['source_vertices'],
            'weights':weights,'physical_contact_height':height,'norm_upper':N,'directed_torque':L,
            'lower_endpoint_margin':g(x0),'upper_endpoint_margin':g(b)})
    beta=F(1001,1000)
    derivative=beta*beta*(1-F(1,100)**2/4)-1
    require(derivative>0,'arcsine derivative throughout new chord range')
    angle=beta*(F(1,200)+F(91,10000))+F(1,30)
    require(angle<F(1,20),'fresh full principal proper-angle bound')
    minimum=records[0]['Bernstein'][0]
    for r in records:
        for value in r['Bernstein']:
            if sg(value-minimum)<0:minimum=value
    return {'new_outer_error':E,'remote_guard':b,'near_half_tangent':x0,
      'all_original_source_SO3_full_roll_arbitrary_translation':True,'scale_reduced_only_as_necessary':True,
      'closed_full_O2_families':4,'closed_roots':5,'leaves':len(records),'nodes':nodes,'maximum_depth':depth,
      'strict_Bernstein_tests':3*len(records),'direct_matrix_identity_audits':3*len(records),
      'minimum_Bernstein_coefficient':minimum,'strict_margin_lower':'1/1000',
      'complete_fixed_leaf_records':records,'signed_near_records':near_records,
      'opposite_directed_source_branch_excluded':True,'surviving_family':0,
      'arcsine_derivative_margin':derivative,'composed_full_angle_upper':angle,
      'margin_below1_over20':F(1,20)-angle,'proper_right_body_gauge':'h=R^j, j=0,...,4'}

def malformed_controls(fixture,geo):
    controls=[]
    def case(name,change):
        bad=copy.deepcopy(fixture);change(bad);controls.append((name,bad))
    case('extend unproved global budget',lambda x:x['global_budget'].__setitem__('maximum_excess','1'))
    case('understate physical source chord',lambda x:x['collar_bounds'].__setitem__('source_chord_upper','1/1000'))
    case('wrong actual raw vertex',lambda x:x['raw_triangle'][0].__setitem__(1,'1/450'))
    case('understate exact physical area maximum',lambda x:x.__setitem__('maximum_physical_area_squared',['0','0']))
    case('missing reflected full-circle branch',lambda x:x['roll']['covers'].pop())
    case('wrong closed remote endpoint',lambda x:x['roll']['covers'][0]['interval'].__setitem__(1,'-1/19'))
    case('incomplete midpoint tree',lambda x:x['roll']['covers'][2]['leaves'].pop())
    case('duplicate terminal',lambda x:x['roll']['covers'][0]['leaves'].append(copy.deepcopy(x['roll']['covers'][0]['leaves'][0])))
    case('nonoriginal source witness',lambda x:x['roll']['covers'][0]['leaves'][0]['source_vertices'].__setitem__(0,55))
    case('unbalanced receiving pair',lambda x:x['roll']['covers'][0]['leaves'][0].__setitem__('edges',[0,4]))
    case('understate actual norm',lambda x:x['roll']['norms_upper'].__setitem__(0,'1'))
    case('missing negative near roll',lambda x:x['roll']['near'].pop())
    case('false negative near contact',lambda x:x['roll']['near'][1].__setitem__('source_vertices',[24,16]))
    rejected=[]
    for name,bad in controls:
        try:configuration(bad);validate_roll(bad['roll'],geo)
        except (ValueError,KeyError,IndexError,TypeError):rejected.append(name)
        else:raise ValueError('malformed mathematical certificate accepted: '+name)
    return rejected

def check(self_test):
    prerequisite=R.check(True)
    parent_bytes=(json.dumps(prerequisite,indent=2)+'\n').encode()
    require(parent_bytes==(PARENT/'expected.json').read_bytes(),'EVERY full old area/roll prerequisite byte')
    fixture=json.loads((HERE/'certificates.json').read_text())
    u=configuration(fixture)
    A0,A12,rho2,gates=inverse_area_gates()
    geometry,V=collar_geometry(u,A0)
    geo=R.geometry();require(tuple(V)==tuple(geo[0]),'same 55 actual originals in new collar and rolls')
    roll=validate_roll(fixture['roll'],geo)
    bad=malformed_controls(fixture,geo) if self_test else []
    for pair,expected in tuple(A.SIGNS.items()):
        require(A.interval_sign(pair)==expected,'independent rational sqrt5 enclosure')
    return enc({'agent':'six-rupert-2','role':'researcher',
      'proof_status':'complete author-checked written intermediate proof; unformalized',
      'independent_review_asserted':False,'global_J77_Rupert_resolved':False,
      'collar_passage_exclusion_asserted':False,'coefficient_field':'Q(sqrt5), sqrt5 positive',
      'global_inverse_area':{'minimum_area':A0,'next_polar_level_squared':A12,'tangent_inradius_squared':rho2,
       'whole_parameter_domain':'A0<=T<A1',
       'bound':'dist(k,E)^2<=2*(1-(A0*T+rho*sqrt(A0^2+rho^2-T^2))/(A0^2+rho^2))',
       'all_radicals_positive_branches':True,'zero_excess_exact_axis':True,
       'linear_corollary_domain':'0<eta<=1/10','strict_linear_chord_factor':'7/20','exact_scalar_gates':gates},
      'new_closed_receiving_collar':geometry,'fresh_all_source_full_roll_reduction':roll,
      'ordinary_and_optimized_use_explicit_guards':True,'direct_pinned_parent_files':14,
      'distinct_direct_and_transitive_parent_files':21,'complete_area_and_old_roll_prerequisite_bytes':len(parent_bytes),
      'complete_old_roll_prerequisite_sha256':sha256(parent_bytes).hexdigest(),
      'canonical_certificate_sha256':digest(fixture),'malformed_controls':bad,
      'distinct_registered_independent_sign_enclosures_including_parents':len(A.SIGNS)})

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    result=check(args.self_test)
    encoded=(json.dumps(result,indent=1)+'\n').encode()
    require(encoded==(HERE/'expected.json').read_bytes(),'EVERY expected output byte; use --self-test')
    print(encoded.decode(),end='')
