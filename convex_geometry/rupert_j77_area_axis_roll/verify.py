"""Exact complete O(2) roll and full-angle reduction near J77 area axes.

Author: six-rupert-2, researcher. Python 3.11+, standard library only.
Fixed original-vertex witnesses, complete closed trees, Q(sqrt5) signs.
The continuous arbitrary-translation and proper-frame bridges are in PROOF.md.
"""
import argparse
import copy
import importlib.util
import json
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
def require(ok,message):
    if not ok:raise ValueError(message)
manifest=json.loads((HERE/'dependencies.json').read_text())
require(set(manifest)=={'source_directory','source_commit','sha256'},'dependency manifest keys')
require(manifest['source_directory']=='convex_geometry/rupert_j77_projection_area'
        and manifest['source_commit']=='cd0088c8aa1e308657b17d759bc5600c7b8b2b34','direct area parent')
PARENT=REPO/manifest['source_directory']
for name,digest in manifest['sha256'].items():
    require(sha256((PARENT/name).read_bytes()).hexdigest()==digest,'dependency changed: '+name)
require(len(manifest['sha256'])==7,'all seven direct source files pinned')
spec=importlib.util.spec_from_file_location('j77_roll_area_parent',PARENT/'verify.py')
area=importlib.util.module_from_spec(spec)
spec.loader.exec_module(area)
Q=area.Q
dot=area.dot
def sg(x):return area.sg(x)
def pos(x,message):require(sg(x)>0,message)
def det(u,v):return u[0]*v[1]-u[1]*v[0]
def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,(list,tuple)):return [enc(t) for t in x]
    if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
    return area.enc(x)
def digest(x):return sha256(json.dumps(enc(x),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def val(c,t):return c[0]+t*c[1]+t*t*c[2]
def bernstein(c,a,b):
    return (val(c,a),val(c,a)+(b-a)*(c[1]+2*a*c[2])/2,val(c,b))

def geometry():
    V=area.model.VERTICES
    S=area.shadow(V,Q(49,25)/8)['vertices']
    labels=tuple(min(i for i,v in enumerate(V) if v[1:]==p) for p in S)
    M=[];H=[]
    for p,q in zip(S,S[1:]+S[:1]):
        m=(q[1]-p[1],p[0]-q[0]);h=dot(m,p)
        pos(h,'actual outward signed shadow height')
        for v in V:require(sg(h-dot(m,v[1:]))>=0,'all 55 original shadow support tests')
        M.append(m);H.append(h)
    require(len(S)==len(M)==10,'actual ten-vertex shadow')
    require({(-v[0],v[1],v[2]) for v in V}==set(V),'actual x-plane body reflection')
    fixed=tuple(i for i,v in enumerate(V) if v[0]==0)
    require(fixed==(22,23,24),'actual mirror fixed vertices')
    axis=(Q(),Q(1,1)/2,Q(1))
    e=(Q(1),Q(),Q());u=e
    for _ in range(4):u=area.body_rotation(axis,u)
    E0=(Q(5,-3),Q(5,-1),Q(0,-2));factor=Q(10,-2)
    pos(factor,'critical-axis positive projective factor')
    require(E0==area.scale(-factor,u),'area axis is prior critical mirror axis')
    return V,S,labels,M,H,fixed,E0,factor

def balanced(ids,M):
    require(isinstance(ids,list) and len(ids) in (2,3) and len(set(ids))==len(ids)
            and all(type(i) is int and 0<=i<10 for i in ids),'balanced edge ids')
    if len(ids)==2:
        a,b=(M[i] for i in ids)
        require(det(a,b)==0 and sg(dot(a,b))<0,'actual opposite normal pair')
        k=next(j for j in range(2) if a[j]!=0)
        w=(-b[k]/a[k],Q(1))
    else:
        a,b,c=(M[i] for i in ids)
        w=(det(b,c),det(c,a),det(a,b))
        if all(sg(x)<0 for x in w):w=tuple(-x for x in w)
    for x in w:pos(x,'strictly positive stress weight')
    total=sum(w,Q());w=tuple(x/total for x in w)
    require(sum(w,Q())==1,'stress normalization')
    require(all(sum((x*M[i][j] for i,x in zip(ids,w)),Q())==0 for j in range(2)),
            'both components of exact translation balance')
    return w

def source_points(ids,V):
    require(isinstance(ids,list) and all(type(i) is int and 0<=i<55 for i in ids),'actual original source ids')
    return tuple(V[i][1:] for i in ids)

def motion(family,t,p):
    require(type(family) is int and family in range(4),'full O(2) family')
    sigma=1 if family in (0,2) else -1
    epsilon=1 if family in (0,1) else -1
    den=1+t*t
    return (sigma*((1-t*t)*p[0]-2*t*p[1])/den,
            sigma*epsilon*(2*t*p[0]+(1-t*t)*p[1])/den)

def polynomial(family,ids,points,M,H,U,E):
    w=balanced(ids,M)
    require(len(points)==len(ids),'one source point per normal')
    sigma=1 if family in (0,2) else -1
    epsilon=1 if family in (0,1) else -1
    terms=[]
    for i,p in zip(ids,points):
        m=M[i]
        a=sigma*(m[0]*p[0]+epsilon*m[1]*p[1])
        b=sigma*(-2*m[0]*p[1]+2*epsilon*m[1]*p[0])
        terms.append((a-H[i]-E*U[i],b,-a-H[i]-E*U[i]))
    c=tuple(sum((x*term[k] for x,term in zip(w,terms)),Q()) for k in range(3))
    # A degree <=2 identity, independently checked at three distinct points.
    for t in (F(-1),F(0),F(1)):
        direct=(1+t*t)*sum((x*(dot(M[i],motion(family,t,p))-H[i]-E*U[i])
                         for i,x,p in zip(ids,w,points)),Q())
        require(val(c,t)==direct,'direct matrix vs quadratic identity')
    return w,c

def closed_tree(leaves):
    require(isinstance(leaves,list) and bool(leaves),'nonempty complete cover')
    paths=[x['path'] for x in leaves]
    require(all(type(p) is str and set(p)<=set('01') and len(p)<=16 for p in paths),'binary fixed path')
    require(len(paths)==len(set(paths)),'duplicate terminal path')
    pathset=set(paths)
    nodes=0
    def visit(p):
        nonlocal nodes
        nodes+=1
        descendants=[s for s in paths if s.startswith(p)]
        require(bool(descendants),'missing closed child')
        if p in pathset:
            require(len(descendants)==1,'terminal prefix overlaps another terminal')
            return
        visit(p+'0');visit(p+'1')
    visit('')
    require(nodes==2*len(leaves)-1,'full binary tree count')
    return nodes,max(map(len,paths))

def interval(root,path):
    a,b=map(F,root)
    require(a<b,'positive closed root interval')
    for ch in path:
        mid=(a+b)/2
        if ch=='0':b=mid
        else:a=mid
    return a,b

def validate(fixture,geo):
    V,S,labels,M,H,fixed,E0,factor=geo
    require(set(fixture)=={'bounds','norms_upper','covers','near'},'exact certificate keys')
    bd=fixture['bounds']
    require(set(bd)=={'receiver_chord','outer_error','remote_half_tangent','near_roll_ratio','full_angle_ratio'},'bound keys')
    d=F(bd['receiver_chord']);E=F(bd['outer_error']);b=F(bd['remote_half_tangent'])
    cr=F(bd['near_roll_ratio']);angle=F(bd['full_angle_ratio'])
    require(d==F(1,1000) and E==F(39,4000) and b==F(1,50),'stated closed cap and remote budget')
    require(cr>0 and angle>0,'positive moving roll/angle ratios')
    L=F(277,32);Cs=L*F(5,14);radius=F(9,4);C=radius*(1+Cs)
    require(Cs==F(1385,448) and C==F(16497,1792),'derived linear source/error factors')
    pos(radius*radius-Q(11,4)/4,'common original radius strict upper bound')
    require(L*d<F(9,1000) and Cs*d<F(1,300),'inherited area budget and source range')
    require(radius*(d+F(1,300))==E,'uniform necessary error budget')
    require(cr*d<b,'near threshold strictly inside remote roll guard')
    U=tuple(map(F,fixture['norms_upper']))
    require(len(U)==10,'every actual edge normal norm covered')
    for i,(m,h,u) in enumerate(zip(M,H,U)):
        require(u>0,'positive normal norm upper bound')
        require(sg(Q(u*u)-dot(m,m))>=0,'actual squared normal norm upper bound')
    expected_roots=[(0,['-1','-1/50']),(0,['1/50','1'])]+[(i,['-1','1']) for i in (1,2,3)]
    require(len(fixture['covers'])==5,'all five remote roots required')
    records=[];nodes=0;depth=0
    for root_id,(cover,(family,root)) in enumerate(zip(fixture['covers'],expected_roots)):
        require(set(cover)=={'family','interval','leaves'} and cover['family']==family and cover['interval']==root,
                'complete full-circle directed roots and all closed endpoints')
        n,dp=closed_tree(cover['leaves']);nodes+=n;depth=max(depth,dp)
        for leaf in cover['leaves']:
            require(set(leaf)=={'path','edges','source_vertices'},'fixed leaf witness keys')
            a,z=interval(root,leaf['path'])
            points=source_points(leaf['source_vertices'],V)
            w,c=polynomial(family,leaf['edges'],points,M,H,U,E)
            coefficients=bernstein(c,a,z)
            for value in coefficients:pos(value-Q(F(1,50)),'whole-interval Bernstein obstruction margin exceeds 1/50')
            records.append({'root':root_id,'family':family,'path':leaf['path'],'closed_interval':(a,z),
                'edges':leaf['edges'],'original_source_vertices':leaf['source_vertices'],'positive_weights':w,
                'quadratic_coefficients':c,'Bernstein_coefficients':coefficients})
    require(nodes==2*len(records)-5,'complete five-root forest count')
    near=fixture['near']
    require(isinstance(near,list) and len(near)==2,'both signed near rolls')
    near_records=[]
    for branch,expected_sign in zip(near,(1,-1)):
        require(set(branch)=={'sign','edges','source_vertices'} and branch['sign']==expected_sign,'two directed signed near rolls')
        ids=branch['edges'];points=source_points(branch['source_vertices'],V);w=balanced(ids,M)
        require(len(points)==len(ids),'near source count')
        for i,p in zip(ids,points):require(dot(M[i],p)==H[i],'actual zero-roll contact')
        h=sum((x*H[i] for i,x in zip(ids,w)),Q())
        N=sum((x*U[i] for i,x in zip(ids,w)),Q())
        slope=sum((x*expected_sign*(-2*M[i][0]*p[1]+2*M[i][1]*p[0])
                   for i,x,p in zip(ids,w,points)),Q())
        pos(h,'positive weighted contact height');pos(N,'positive weighted norm budget');pos(slope,'positive signed torque')
        # g(x,delta)=slope*x-2h*x^2-C*N*delta*(1+x^2), concave in x.
        lower=cr*slope-C*N-cr*cr*(2*h+C*N*d)*d
        upper=slope*b-(2*h+C*N*d)*b*b-C*N*d
        pos(lower,'every positive delta: g(cr*delta,delta)/delta strict lower bound')
        pos(upper,'whole closed cap: g(b,delta) strict lower bound')
        near_records.append({'sign':expected_sign,'edges':ids,'original_source_vertices':branch['source_vertices'],
             'positive_weights':w,'height':h,'norm_upper':N,'linear_torque':slope,
             'lower_endpoint_scaled_margin':lower,'upper_endpoint_margin':upper})
    beta=F(1001,1000);chord=F(1,300)
    require(d<chord and Cs*d<chord,'all proper transports in derivative range')
    derivative=beta*beta*(1-chord*chord/4)-1
    require(derivative>0,'arcsine derivative positive branch')
    coefficient=beta*(1+Cs)+2*cr
    require(coefficient<angle,'positive principal full-angle composition')
    margins=[(value,i,j) for i,r in enumerate(records) for j,value in enumerate(r['Bernstein_coefficients'])]
    minimum=margins[0]
    for candidate in margins[1:]:
        if sg(candidate[0]-minimum[0])<0:minimum=candidate
    pos(minimum[0]-Q(F(1,50)),'uniform remote Bernstein margin exceeds 1/50')
    return {'records':records,'near_records':near_records,'nodes':nodes,'depth':depth,'minimum':minimum,
      'source_factor':Cs,'Hausdorff_factor':C,'angle_derivative_margin':derivative,'angle_upper_coefficient':coefficient,
      'angle_margin':angle-coefficient,'bounds':bd,'norms_upper':U}

def malformed_controls(fixture,geo):
    cases=[]
    def case(name,modify):
        bad=copy.deepcopy(fixture);modify(bad);cases.append((name,bad))
    case('missing directed reflected root',lambda x:x['covers'].pop())
    case('missing negative proper root',lambda x:x['covers'].pop(2))
    case('open remote endpoint',lambda x:x['covers'][0]['interval'].__setitem__(1,'-1/49'))
    case('incomplete binary cover',lambda x:x['covers'][2]['leaves'].pop())
    case('duplicate terminal',lambda x:x['covers'][0]['leaves'].append(copy.deepcopy(x['covers'][0]['leaves'][0])))
    case('prefix collision',lambda x:x['covers'][0]['leaves'][0].__setitem__('path',''))
    case('nonbinary path',lambda x:x['covers'][0]['leaves'][0].__setitem__('path','a'))
    case('nonoriginal source',lambda x:x['covers'][0]['leaves'][0]['source_vertices'].__setitem__(0,55))
    case('invalid edge',lambda x:x['covers'][0]['leaves'][0]['edges'].__setitem__(0,10))
    case('unbalanced edge pair',lambda x:x['covers'][0]['leaves'][0].__setitem__('edges',[0,4]))
    case('wrong actual source witness',lambda x:x['covers'][0]['leaves'][0].__setitem__('source_vertices',[24,16]))
    case('underestimated normal norm',lambda x:x['norms_upper'].__setitem__(0,'3/2'))
    case('negative normal norm',lambda x:x['norms_upper'].__setitem__(0,'-2'))
    case('unproved receiver range',lambda x:x['bounds'].__setitem__('receiver_chord','1/100'))
    case('undersized error budget',lambda x:x['bounds'].__setitem__('outer_error','1/1000'))
    case('unproved remote restriction',lambda x:x['bounds'].__setitem__('remote_half_tangent','1/250'))
    case('too small moving roll ratio',lambda x:x['bounds'].__setitem__('near_roll_ratio','1'))
    case('too small full angle ratio',lambda x:x['bounds'].__setitem__('full_angle_ratio','14'))
    case('missing negative near roll',lambda x:x['near'].pop())
    case('wrong signed near contact',lambda x:x['near'][1].__setitem__('source_vertices',[24,16]))
    for name,bad in cases:
        try:validate(bad,geo)
        except (ValueError,KeyError,IndexError,TypeError):continue
        raise ValueError('malformed mathematical certificate accepted: '+name)
    return len(cases)

def check(self_test):
    prerequisite=area.check(True)
    encoded=(json.dumps(prerequisite,indent=2)+'\n').encode()
    require(encoded==(PARENT/'expected.json').read_bytes(),'EVERY area prerequisite output byte')
    require(prerequisite['global_source_localization']['bounds']['receiver_area_lipschitz_upper']=='277/32'
            and prerequisite['global_source_localization']['bounds']['global_positive_excess_to_chord_factor']=='5/14',
            'actual parent source coercivity and receiver bound')
    initial_calls=area.SIGN_CALLS
    geo=geometry();fixture=json.loads((HERE/'certificates.json').read_text())
    data=validate(fixture,geo)
    bad=malformed_controls(fixture,geo) if self_test else 0
    for pair,expected in tuple(area.SIGNS.items()):
        require(area.interval_sign(pair)==expected,'independent rational sqrt5 enclosure audit')
    V,S,labels,M,H,fixed,E0,factor=geo
    return enc({'agent':'six-rupert-2','role':'researcher','proof_status':'author-checked written intermediate proof; unformalized',
      'global_Rupert_resolved':False,'independent_review_asserted':False,'whole_receiver_cap_exclusion_asserted':False,
      'coefficient_field':'Q(sqrt5), sqrt5 positive','original_vertices':55,'actual_shadow_vertices':10,
      'shadow_vertices':S,'original_preimage_labels':labels,'actual_outward_normals':M,'signed_support_heights':H,
      'all_original_shadow_support_tests':550,'norm_upper_bounds':data['norms_upper'],
      'actual_mirror_fixed_vertices':fixed,'critical_mirror_axis_identity':{'E0':E0,'factor':factor,'formula':'E0=-(10-2sqrt5)R^4 e'},
      'bounds':data['bounds'],'linear_source_chord_factor':data['source_factor'],
      'linear_necessary_Hausdorff_factor':data['Hausdorff_factor'],
      'complete_full_O2_remote_cover':{'families':4,'closed_roots':5,'both_directed_source_branches':True,
        'leaves':len(data['records']),'nodes':data['nodes'],'maximum_depth':data['depth'],
        'strict_Bernstein_tests':3*len(data['records']),'direct_matrix_identity_audits':3*len(data['records']),
        'minimum_Bernstein_margin':data['minimum'][0],'minimum_record_and_coefficient':data['minimum'][1:],
        'uniform_Bernstein_margin_strict_lower':'1/50',
        'all_fixed_leaf_records_sha256':digest(data['records']),'opposite_directed_source_branch_excluded':True,
        'allowed_family':0,'allowed_open_half_tangent_interval':['-1/50','1/50']},
      'moving_signed_near_roll':data['near_records'],
      'full_proper_angle':{'arcsine_derivative_margin':data['angle_derivative_margin'],
        'upper_coefficient':data['angle_upper_coefficient'],'margin_below_15':data['angle_margin'],
        'at_positive_receiver_distance':'exists actual right body gauge h=R^j: angle(Qh)<15*delta',
        'at_zero_receiver_distance':'lambda=1,t=0,Q in <R>, by the complete area parent'},
      'actual_nearby_equal_shadow_family':'Q0=M_n M_e; t=0,lambda=1; not a strict passage',
      'direct_dependency_files_hash_pinned':7,'area_full_prerequisite_bytes_replayed':len(encoded),
      'area_prerequisite_sha256':sha256(encoded).hexdigest(),
      'old_diameter_region_jobs_replayed':False,'canonical_certificate_sha256':digest(fixture),
      'malformed_controls_with_self_test':bad,'new_sign_calls':area.SIGN_CALLS-initial_calls,
      'distinct_independent_sign_audits_including_parent':len(area.SIGNS)})

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    result=check(args.self_test)
    encoded=(json.dumps(result,indent=2)+'\n').encode()
    require(encoded==(HERE/'expected.json').read_bytes(),'EVERY expected output byte; use --self-test')
    print(encoded.decode(),end='')
