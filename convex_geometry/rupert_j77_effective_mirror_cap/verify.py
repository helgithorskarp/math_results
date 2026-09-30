"""Exact finite gates for a complete J77 critical-mirror receiving cap.

Author six-rupert-2, researcher; Python3.11+, stdlib, no floating arithmetic.
The finite-scale Cayley estimates and projection bridges are in PROOF.md.
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
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

deps=json.loads((HERE/'dependencies.json').read_text())
require([(d['source_directory'],d['source_commit']) for d in deps]==[
 ('convex_geometry/rupert_j77_uniform_local_exclusion','d23b45ee6e2d2704087e42b6a4faef698c53b14d'),
 ('convex_geometry/rupert_j77_area_axis_roll','86dcf1e10d0eddbc26fc8343b6df4fcc642d47c6')],
 'two declared source parents')
require([len(d['sha256']) for d in deps]==[8,7],'all direct parent files pinned')
for d in deps:
    for name,digest in d['sha256'].items():
        require(sha256((REPO/d['source_directory']/name).read_bytes()).hexdigest()==digest,
                'changed direct dependency: '+name)
U=module('j77_effective_uniform_input',REPO/deps[0]['source_directory']/'verify.py')
ROLL=module('j77_effective_full_roll_input',REPO/deps[1]['source_directory']/'verify.py')
area=ROLL.area;P=U.P;Q=area.Q
dot=area.dot;cross=area.cross;sub=area.sub;scale=area.scale;add=area.add
V=area.model.VERTICES
for name in ('model.py','q5.py'):
    require((REPO/'convex_geometry/rupert_j77_fixed_outer_local'/name).read_bytes()==
            (REPO/'convex_geometry/rupert_j77_projection_diameter'/name).read_bytes(),
            'original model/index/field identity: '+name)
require(tuple(U.fixed.VERTICES)==tuple(V),'same original55 vertices in both loaded parents')

def sg(x):return area.sg(x)
def pos(x,message):require(sg(x)>0,message)
def nonneg(x,message):require(sg(x)>=0,message)
def bound(x,y,message):nonneg(Q(y)-x,message)
def absq(x):return x if sg(x)>=0 else -x
def norm1(v):return sum((absq(x) for x in v),Q())
def enc(x):return ROLL.enc(x)
def digest(x):return ROLL.digest(x)
def decode(x):return tuple(Q(*z) for z in x)
E=(Q(1),Q(),Q());AXIS=(Q(),Q(1,1)/2,Q(1))
def rotate(v):return area.body_rotation(AXIS,v)
def det2(a,b):return a[1]*b[2]-a[2]*b[1]
def inverse(matrix):
    n=len(matrix)
    inv=list(map(list,zip(*[P.solve(matrix,[Q(int(k==j)) for k in range(n)]) for j in range(n)])))
    require(all(dot(matrix[i],[inv[k][j] for k in range(n)])==int(i==j)
                for i in range(n) for j in range(n)),'exact inverse product')
    return inv

def family(case,ds,rays,permutation,ms,gs,md,gd):
    a=tuple(P.trim((rays[1][k],rays[0][k]-rays[1][k])) for k in range(3))
    A2=P.pdot(a,a);rows=[];rhs=[];labels=[]
    def put(row,b,label):rows.append(tuple(row));rhs.append(b);labels.append(label)
    # Old edge/preimage order gives a reproducible bridge for the 28 basis IDs.
    # Every tie is rechecked on the actual transformed original vertices.
    for ox,oy in sorted({tuple(c[:2]) for c in case['contacts']}):
        x,y=permutation[oy],permutation[ox];edge=sub(V[y],V[x]);h=dot(cross(edge,E),V[x])
        pos(h,'hidden fixed critical offset');m=scale(1/h,cross(edge,E))
        for oj in range(55):
            j=permutation[oj];v=V[j]
            if dot(m,v)==1:
                r=[P.poly(dot(scale(1/h,cross(edge,d)),sub(v,V[x]))) for d in ds]
                put(r+[P.ZERO]*3,P.pscale(-2,P.pdot(a,tuple(P.poly(x) for x in cross(v,m)))),['hidden',x,y,j])
    for i,(ox,oy,oj) in enumerate(case['contacts']):
        x,y,j=permutation[oy],permutation[ox],permutation[oj];v=V[j]
        if gs[i][1:]!=(Q(),Q()):continue
        r=[P.pdot(a,tuple(P.poly(x) for x in g)) for g in gd[i]]
        b=P.psub(A2,P.pmul(P.pdot(a,tuple(P.poly(x) for x in v)),P.pdot(a,tuple(P.poly(x) for x in ms[i]))))
        put(r+[P.poly(gs[i][0]),P.poly(ms[i][1]),P.poly(ms[i][2])],b,['persistent2',x,y,j])
    for oj in (9,14,54):
        j=permutation[oj];v=V[j];require(v[0]==0,'actual fixed radial source')
        torque=P.pdot(a,tuple(P.poly(x) for x in cross(v,E)))
        r=[P.pscale(-dot(v,d),torque) for d in ds];av=P.pdot(a,tuple(P.poly(x) for x in v))
        put(r+[P.ZERO,P.poly(v[1]),P.poly(v[2])],P.psub(P.pscale(dot(v,v),A2),P.pmul(av,av)),['radial2',j])
    for k in range(2):put([P.poly(-int(j==k)) for j in range(5)],P.ZERO,['receiver_cone',k])
    matrix=[[d[1] for d in ds],[d[2] for d in ds]]
    rm=[P.solve(matrix,scale(-1,cross(E,a))[1:]) for a in rays]
    mirror=tuple(P.trim((rm[1][k],rm[0][k]-rm[1][k])) for k in range(2))+(P.ZERO,)*3
    tight=[i for i,(r,b) in enumerate(zip(rows,rhs)) if P.pdot(r,mirror)==b]
    require(len(rows)==102 and len(tight)==41,'complete transformed polynomial row family')
    for b in U.bernstein_replay(A2,Q(),Q(1)):pos(b-Q(1)/4,'tangent interpolant norm squared >1/4')
    return rows,rhs,labels,mirror,tight

def cover_shape(covers):
    require(len(covers)==4 and {(d['coordinate'],d['sign']) for d in covers}==
            {(k,s) for k in range(2) for s in (1,-1)},'all four coordinate signs')
def coordinate_dual(d,rows,rhs,mirror,tight):
    ids=d['row_indices'];cc=d['coordinate_indices'];n=len(ids)
    require(0<n<=5 and len(set(ids))==n and set(ids)<=set(tight),'distinct tight dual rows')
    require(len(cc)==len(set(cc))==n and set(cc)<=set(range(5)),'dual determinant coordinates')
    target=[d['sign']*int(k==d['coordinate']) for k in range(5)]
    raw=P.determinant([[rows[i][k] for i in ids] for k in cc])
    require(raw and len(raw)<=3,'nonzero raw determinant degree<=2')
    for tau in (Q(),Q(1)/2,Q(1)):
        matrix=[[P.peval(rows[i][k],tau) for i in ids] for k in cc]
        require(P.peval(raw,tau)==U.critical.gaussian_determinant(matrix),'independent determinant replay')
    den,nums=P.cramer(rows,ids,cc,target)
    if sg(P.peval(den,Q(1)/2))<0:den=P.pscale(-1,den);nums=[P.pscale(-1,p) for p in nums]
    db=U.bernstein_replay(den,Q(),Q(1));nb=[U.bernstein_replay(p,Q(),Q(1)) for p in nums]
    for b in db:pos(b,'closed interval positive dual denominator')
    for bs in nb:
        for b in bs:nonneg(b,'closed interval nonnegative dual numerator')
    require(P.pdot(nums,[rhs[i] for i in ids])==P.pscale(d['sign'],P.pmul(den,mirror[d['coordinate']])),
            'full mirror-tight right-hand-side identity')
    lower=min(db);upper=sum((max(bs) for bs in nb),Q())
    pos(100*lower-upper,'sum of nonnegative dual weights <100')
    return {'coordinate':d['coordinate'],'sign':d['sign'],'basis_rows':ids,'determinant_coordinates':cc,
            'basis_size':n,'denominator_degree':len(den)-1,'denominator_Bernstein_min':lower,
            'dual_weight_sum_upper':upper/lower,'Bernstein_coefficients':len(db)+sum(map(len,nb)),
            'identity_sha256':digest([den,nums])}

def exact_samples(ds,rays,fam):
    """Independent direct finite rotation/row checks, not a continuum proof."""
    eps=Q(F(1,10**24));a=scale(Q(1)/2,add(*rays))
    def cayley(v,w):
        return add(v,scale(2/(1+dot(w,w)),add(cross(w,v),cross(w,cross(w,v)))))
    um=add(E,scale(-eps,cross(E,a)));wm=scale(eps,a)
    for v in V:
        reflected=(-v[0],v[1],v[2])
        direct=sub(reflected,scale(2*dot(um,reflected)/dot(um,um),um))
        require(cayley(v,wm)==direct,'Cayley equals direct proper mirror product on every original vertex')
    X=[Q(500),Q(1000),Q(10**6),Q(10**7),Q(-10**7)]
    r=add(scale(X[0],ds[0]),scale(X[1],ds[1]));u=add(E,scale(eps,r))
    k=(X[2],Q(10**8),Q(-10**8));c=(Q(),X[3],X[4]);T=scale(2*eps*eps,c)
    w=add(scale(eps,a),scale(eps*eps,k));factor=(1+dot(w,w))/(2*eps*eps)
    rows,rhs,labels,_,_=fam
    for row,b,label in zip(rows,rhs,labels):
        leading=dot([P.peval(p,Q(1)/2) for p in row],X)-P.peval(b,Q(1)/2)
        if label[0]=='hidden':
            _,x,y,j=label;v=V[j];edge=sub(V[y],V[x]);h=dot(cross(edge,E),V[x])
            m=scale(1/h,cross(edge,u));actual=(dot(m,sub(cayley(v,w),V[x]))+dot(m,T))/eps
        elif label[0]=='persistent2':
            _,x,y,j=label;v=V[j];edge=sub(V[y],V[x]);h=dot(cross(edge,E),v)
            m=scale(1/h,cross(edge,u));actual=factor*(dot(m,sub(cayley(v,w),v))+dot(m,T))
        elif label[0]=='radial2':
            v=V[label[1]];m=sub(v,scale(dot(u,v)/dot(u,u),u))
            actual=factor*(dot(m,sub(cayley(v,w),v))+dot(m,T))
        else:actual=-X[label[1]]
        nonneg(10**13*eps-absq(actual-leading),'direct finite row sample matches the certified remainder scale')
    return {'exact_mirror_vertex_identities':55,'direct_finite_normalized_row_samples':len(rows)}

def geometry(case,fixture,parent,permutation,samples=False):
    old=decode(case['direction']);r=rotate(old);q=-r[0]
    pos(q,'positive critical physical length');require(r==scale(-q,E),'unit critical-axis transfer')
    require(old in parent and len(parent)==3,'old closed parent incidence')
    corners=[];ds=[];lengths=[]
    for v in parent:
        z=rotate(v);s=-z[0];pos(s,'positive whole-parent projective denominator')
        z=scale(-1/s,z);require(z[0]==1,'unit affine chart x=1');corners.append(z)
        if v==old:continue
        d=sub(z,E);length=norm1(d);pos(length-Q(1)/4,'outgoing chart length >1/4')
        ds.append(scale(1/length,d));lengths.append(length)
    require(len(ds)==2 and all(d[0]==0 and norm1(d)==1 for d in ds),'two normalized receiving rays')
    rays=[]
    for v in case['extreme_motions']:
        a=rotate(decode(v)[:3]);require(a[0]==0,'tangent motion transfer')
        rays.append(scale(1/norm1(a),a))
    require(len(rays)==2 and det2(*rays)!=0,'two independent actual tangent rays')
    contacts=[(permutation[b],permutation[a],permutation[j]) for a,b,j in case['contacts']]
    require(len(contacts)==len(set(contacts))==32,'32 distinct original contacts')
    ms=[];gs=[];md=[];gd=[];support_tests=0
    for a,b,j in contacts:
        require(a!=b and all(type(k) is int and 0<=k<55 for k in (a,b,j)),'original contact labels')
        edge=sub(V[b],V[a]);h=dot(cross(edge,E),V[j]);pos(h,'noncollapsed critical support')
        m=scale(1/h,cross(edge,E));ms.append(m);gs.append(cross(V[j],m))
        derivatives=[scale(1/h,cross(edge,d)) for d in ds];md.append(derivatives)
        gd.append([cross(V[j],z) for z in derivatives])
        require(m[0]==0 and dot(m,V[a])==dot(m,V[b])==dot(m,V[j])==1,'critical contact identity')
        for u in corners:
            mu=scale(1/h,cross(edge,u));height=dot(mu,V[j]);pos(height,'positive closed-parent support')
            require(dot(mu,V[a])==dot(mu,V[b])==height and dot(mu,u)==0,'all corner incidences')
            for v in V:nonneg(height-dot(mu,v),'all original closed-parent supports');support_tests+=1
        pos(1-norm1(m),'probe l1 norm <1')
        for v in derivatives:pos(Q(3)/2-norm1(v),'all probe drift l1 <3/2')
        for v in gd[-1]:pos(4-norm1(v),'all torque drift l1 <4')
    common=case['common_indices'];weights=decode(fixture['common_weights'])
    require(common==[i for i,g in enumerate(gs) if g[1:]==(Q(),Q())] and len(common)==6,'all six common rows')
    require(len(weights)==6 and sum(weights,Q())==1,'normalized common weights')
    for w in weights:nonneg(w-Q(1)/20,'positive common weight >=1/20')
    for k in range(3):
        require(sum((w*gs[i][k] for w,i in zip(weights,common)),Q())==0,'full torque balance')
        require(sum((w*ms[i][k] for w,i in zip(weights,common)),Q())==0,'full normal balance')
    rr=case['rank_rows'];require(len(rr)==len(set(rr))==3 and set(rr)<=set(common),'rank-three contact rows')
    matrix=[[gs[i][0],ms[i][1],ms[i][2]] for i in rr];inv=inverse(matrix)
    require(U.critical.determinant(matrix)==U.critical.gaussian_determinant(matrix)!=0,'rank determinant replay')
    for row in inv:pos(9-norm1(row),'inverse row l1 <9')
    for i in common:
        for v in gd[i]:pos(3-norm1(v),'common torque drift l1 <3')
        for v in md[i]:pos(2-norm1(v),'common normal drift l1 <2')
    for g in gs:
        for a in rays:nonneg(-dot(g,a),'necessary tangent cone generators')
    rayinv=inverse([[a[1] for a in rays],[a[2] for a in rays]])
    for row in rayinv:pos(4-norm1(row),'tangent coefficient inverse l1 <4')
    for k,i in enumerate(case['facet_rows']):
        pos(-dot(gs[i],rays[k])-Q(1)/16,'oriented facet magnitude >1/16')
        require(dot(gs[i],rays[1-k])==0,'opposite ray is in the facet')
        pos(1-norm1((gs[i][0],ms[i][1],ms[i][2])),'facet nontangent coefficient l1 <1')
    stressg=[tuple(sum((w*gd[i][k][j] for w,i in zip(weights,common)),Q()) for j in range(3)) for k in range(2)]
    stressm=[tuple(sum((w*md[i][k][j] for w,i in zip(weights,common)),Q()) for j in range(3)) for k in range(2)]
    drift=[[dot(a,g) for g in stressg] for a in rays]
    for row in drift:
        for x in row:pos(x-Q(1)/100,'strict drift >1/100');pos(3-x,'drift <3')
    receiverinv=inverse([[d[1] for d in ds],[d[2] for d in ds]])
    ell=[sum((row[k] for row in receiverinv),Q()) for k in range(2)]
    bound(norm1(ell),2,'receiving coefficient sum functional l1 <=2')
    fam=family(case,ds,rays,permutation,ms,gs,md,gd);cover_shape(fixture['dual_covers'])
    duals=[coordinate_dual(d,fam[0],fam[1],fam[3],fam[4]) for d in fixture['dual_covers']]
    sample_result=exact_samples(ds,rays,fam) if samples else {}
    return {'parent':case['parent'],'receiver_rays':ds,'motion_rays':rays,'parent_corner_lengths':lengths,
            'support_tests':support_tests,'common_weights':weights,'rank_inverse_row_l1':[norm1(r) for r in inv],
            'receiver_sum_functional':ell,'strict_drift':drift,'polynomial_rows':len(fam[0]),
            'mirror_tight_rows':len(fam[4]),'coordinate_duals':duals,'mirror_coordinates':fam[3],
            'independent_exact_samples':sample_result}

def fan(records):
    by={r['parent']:r for r in records};order=[21,23,28,31,30,32,33]
    nodes=[(21,1),(21,0),(23,1),(28,1),(31,0),(30,0),(32,0),(33,0)]
    rays=[by[i]['receiver_rays'][k] for i,k in nodes]
    require(rays[-1]==scale(-1,rays[0]),'opposite fan boundary rays')
    require(dot(AXIS,rays[0])==dot(AXIS,rays[-1])==0,'half-plane fan boundary')
    for d in rays[1:-1]:pos(-dot(AXIS,d),'strict half-plane interior fan ray')
    for k,i in enumerate(order):
        require(set((rays[k],rays[k+1]))==set(by[i]['receiver_rays']),'no omitted adjacent fan region')
        pos(det2(rays[k],rays[k+1]),'strict positive fan determinant')
    return {'ordered_parents':order,'fan_rays':rays,'half_plane':'(0,(1+sqrt5)/2,1).r <=0',
            'closed_ray_coefficient_sum_covered':'Y<=1/4'}

def numeric_gates():
    R=F(9,4);D=F(1,10**9);s=14*D;cap=F(1,10**23);eps=80*cap
    gates={
     'normalized_row_error_below_5_eta':5-(F(9,2)+F(3,100))*(1+F(2,100)),
     'positive_cone_coefficient_sum_above_9_10':1-53820*s-F(9,10),
     'effective_weighted_drift_above_1_200':F(9,1000)-168000*s-F(1,200),
     'critical_kernel_bound_below_2e6_eta':2*10**6-180*(9*1000+5),
     'negative_cone_bound_below_27e6_eta':27*10**6-26100*1001,
     'finite_second_order_vector_bound':4*10**8-(8*10**6+216*10**6),
     'finite_translation_bound':2*10**7-12*10**6,
     'epsilon_below_1e_12':F(1,10**12)-eps,
     'probes_below_norm2':1-3000*eps,
     'radial_support_exposure_margin':F(1,2)-2*R*R*2000*eps,
     'rotation_first_order_remainder_below_2e9':2*10**9-2*R*(4*10**8+4+4*eps),
     'hidden_remainder_below_1e13':10**13-(4*10**9+2*R*3000+4*2*10**7),
     'persistent_remainder_below_1e13':10**13-(R*3000*4*10**8+3*R*4*10**8+4*R*3000+4*2*10**7+2*3000*2*10**7),
     'radial_remainder_below_1e13':10**13-((R*2000)*(R*2000+R*4*10**8+eps*R*2000*4*10**8)
          +(R*2000)*R*2000**2*eps+3*R*R*4*10**8+(R*2000)*4*R+4*R*2*10**7*eps+2*(R*2000)*2*10**7),
     'mirror_Cayley_error_below_3e15':3*10**15-(4*10**8+2*10**15),
     'receiver_lower_bound_epsilon_over_4':F(1,4)-2*10**15*eps,
     'Cayley_difference_below_half':F(1,2)-3*10**15*eps**2,
     'reflected_angle_below_2e16':2*10**16-4*3*10**15,
     'receiver_chord_to_chart_norm':F(1001,1000)**2*(1-D**2/2)**2-(1-D**2/4),
     'receiver_axis_angle_derivative':1-(F(1,1000)/2)**2-F(1000,1001)**2,
     'reflected_angle_ratio_below_18':18-(15+2*F(1001,1000)),
     'Cayley_ratio_below_10':10*(1-81*D**2/2)-9,
     'reflected_Cayley_norm_below_angle':2*(1-81*D**2/2)-1,
     'final_reflection_rate_contradiction':1-16*10**19*eps}
    for name,gap in gates.items():pos(gap,'positive quantitative absorption: '+name)
    return {'receiver_rate_cap':'1/1000000000','rate_motion_angle_ratio':'18',
            'rate_receiver_to_Cayley':'delta <= Y <=1000*eta','kernel_components_after_rate':'abs(alpha_x),abs(b_y),abs(b_z) <2e6*eta',
            'epsilon_range':'eta/2 <= epsilon <=8*eta','receiver_scaled_norm_upper':2000,
            'second_order_rotation_vector_norm_upper':4*10**8,'scaled_translation_norm_upper':2*10**7,
            'all_finite_inequality_remainders_upper':10**13,'all_coordinate_dual_weight_sums_strict_upper':100,
            'mirror_Cayley_error_upper':'3e15*epsilon^2','reflected_angle_upper':'2e16*epsilon^2',
            'receiver_chord_lower':'delta > epsilon/8','positive_gates':gates,
            'chosen_final_cap':'1/100000000000000000000000','larger_1e_22_final_gate':'fails:16e19*(80e-22)=1.28>1; no mathematical counterexample'}

def coverage(data):
    require(data['agent']=='six-rupert-2' and data['role']=='researcher','actual named author and role')
    require(type(data['receiver_cap_denominator']) is int and data['receiver_cap_denominator']==10**23,'proved numerical cap only')
    ids=[c['parent'] for c in data['cases']]
    require(len(ids)==len(set(ids))==7 and set(ids)=={21,23,28,30,31,32,33},'all seven incident closed strata')

def malformed(data,old,parents,permutation):
    failures=[]
    d=copy.deepcopy(data);d['cases'].pop();failures.append(lambda d=d:coverage(d))
    d=copy.deepcopy(data);d['cases'][1]['parent']=d['cases'][0]['parent'];failures.append(lambda d=d:coverage(d))
    d=copy.deepcopy(data);d['receiver_cap_denominator']=10**22;failures.append(lambda d=d:coverage(d))
    c=copy.deepcopy(data['cases'][0]);c['common_weights'][0]=['-1','0'];failures.append(lambda c=c:geometry(old[c['parent']],c,parents[c['parent']],permutation))
    for edit in ('missing_sign','duplicate_row','wrong_coordinate','wrong_sign'):
        c=copy.deepcopy(data['cases'][0])
        if edit=='missing_sign':c['dual_covers'].pop()
        if edit=='duplicate_row':c['dual_covers'][0]['row_indices'][1]=c['dual_covers'][0]['row_indices'][0]
        if edit=='wrong_coordinate':c['dual_covers'][0]['coordinate_indices'][0]=5
        if edit=='wrong_sign':c['dual_covers'][0]['sign']=0
        failures.append(lambda c=c:geometry(old[c['parent']],c,parents[c['parent']],permutation))
    d=copy.deepcopy(data);d['role']='reviewer';failures.append(lambda d=d:coverage(d))
    for invalid in failures:
        try:invalid()
        except (ValueError,KeyError,IndexError,TypeError):continue
        raise ValueError('malformed mathematical fixture accepted')
    return len(failures)

def check(self_test):
    inherited=ROLL.check(True);b=(json.dumps(inherited,indent=2)+'\n').encode()
    require(b==(REPO/deps[1]['source_directory']/'expected.json').read_bytes(),'EVERY full-roll prerequisite output byte')
    original=json.loads((REPO/deps[0]['source_directory']/'certificates.json').read_text())
    old={c['parent']:c for c in original['cases']};require(len(old)==7,'seven old input cases')
    parents=[tuple(decode(u) for u in t) for t in U.partition()['triangles']]
    require(len(parents)==44,'whole original orientation partition')
    index={v:i for i,v in enumerate(V)};permutation=[index[rotate(v)] for v in V]
    require(len(set(permutation))==55 and all(rotate(V[i])==V[j] for i,j in enumerate(permutation)),'proper body rotation transfer')
    fixed=[i for i,v in enumerate(V) if v[0]==0];require(fixed==[22,23,24],'all actual mirror-fixed sources')
    for j in fixed:
        for k,v in enumerate(V):
            if k!=j:nonneg(dot(V[j],sub(V[j],v))-Q(1)/2,'radial support gap >=1/2')
    data=json.loads((HERE/'certificates.json').read_text());coverage(data)
    records=[geometry(old[c['parent']],c,parents[c['parent']],permutation,self_test) for c in data['cases']]
    fan_result=fan(records);gates=numeric_gates();bad=malformed(data,old,parents,permutation) if self_test else 0
    for pair,s in tuple(area.SIGNS.items()):require(area.interval_sign(pair)==s,'independent rational sqrt5 sign enclosure')
    return enc({'agent':'six-rupert-2','role':'researcher','proof_status':'author-checked finite hypotheses plus written finite-scale proof; unformalized',
       'target':'J77 paragyrate diminished rhombicosidodecahedron','global_Rupert_resolved':False,'independent_review_asserted':False,
       'complete_original_source_cap':'dist(n,{+/-R^j e})<=1e-23, original proper Q, all translations,lambda>=1',
       'closed_classification_up_to_actual_right_body_gauge':'lambda1,t0,Qh=I or M_n M_p',
       'strict_passage_excluded_on_stated_cap':True,'larger_1_1000_cap_excluded':False,
       'coefficient_field':'Q(sqrt5), sqrt5 positive','original_vertices':55,'critical_mirror_axes':5,
       'closed_incident_strata':len(records),'actual_mirror_fixed_vertices':fixed,'radial_strict_comparisons':162,
       'new_original_support_tests':sum(r['support_tests'] for r in records),
       'positive_common_weights':42,'full_coordinate_equilibria':7,'rank_three_inverse_bounds':21,
       'strict_receiver_drift_corners':28,'coordinate_duals':28,'finite_scale_remainder_gates':gates,
       'fan_coverage':fan_result,'stratum_records':records,'canonical_fixture_sha256':digest(data),
       'source_input_files_pinned_direct':15,'source_input_files_pinned_transitive':34,
       'whole_full_roll_expected_bytes_replayed':len(b),'whole_full_roll_expected_sha256':sha256(b).hexdigest(),
       'old_global_fixed_receiver_bisection_jobs_replayed':False,
       'malformed_controls_with_self_test':bad,'distinct_independent_sign_audits_including_roll_parent':len(area.SIGNS)})

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--self-test',action='store_true');a=p.parse_args()
    result=check(a.self_test);b=(json.dumps(result,indent=1)+'\n').encode()
    require(b==(HERE/'expected.json').read_bytes(),'EVERY expected byte; invoke with --self-test')
    print(b.decode(),end='')
