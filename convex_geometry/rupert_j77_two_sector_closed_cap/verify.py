"""Exact finite hypotheses for two entire closed J77 receiving sectors.

six-rupert-2, researcher. Python3.11+ standard library, positive Q(sqrt5).
Complete author-checked continuous intermediate proof: PROOF.md.
Unformalized, independently unreviewed; global J77 remains OPEN.
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
PARENT='convex_geometry/rupert_j77_sector23_closed_cap'
COMMIT='e233e7a1a11a0d1e71057bc4ffc97a07491f0c54'
manifest=json.loads((HERE/'dependencies.json').read_text())
require(len(manifest)==1,'one complete mathematical parent')
dep=manifest[0]
require(set(dep)=={'source_directory','source_commit','sha256'} and dep['source_directory']==PARENT
        and dep['source_commit']==COMMIT and set(dep['sha256'])=={'.gitignore','README.md','PROOF.md',
        'verify.py','certificates.json','dependencies.json','expected.json'},'complete source pins')
for name,digest in dep['sha256'].items():
    require(sha256((REPO/PARENT/name).read_bytes()).hexdigest()==digest,'changed complete parent '+name)
spec=importlib.util.spec_from_file_location('j77_two_sector_exact_parent',REPO/PARENT/'verify.py')
S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
P,A,R,Q=S.P,S.A,S.R,S.Q
PB,M,MV,V=P.PB,P.M,P.MV,P.V
dot,cross,add,sub,scale=A.dot,A.cross,A.add,A.sub,A.scale
sg,pos,nonneg,enc,digest=A.sg,P.pos,P.nonneg,P.enc,P.M.digest
e=(Q(1),Q(),Q())
D,CR,E,B,MARGIN=F(1,200),F(1001,1000),F(373,10000),F(1,20),F(1,1000)
AMIN,KF=F(7,10),F(51,50)
G,MD,Z,MU,MR=P.G,P.MD,P.Z,P.MU,P.MR
KT,THETA,L0=F(7,2),F(1033,100),F(517,100)
DMAX=1+L0*CR*D*D
RAW=[[['1','0'],['0','0'],['0','0']],
     [['1','0'],['-1/50','0'],['0','0']],
     [['1','0'],['-1/100','-1/500'],['-1/100','1/500']]]
BOUNDS={'physical_chord_upper':'1/200','outer_error':'373/10000','outer_coefficient_sum':'1/50',
        'remote_half_tangent':'1/20','Bernstein_margin':'1/1000','Gamma':'33/5',
        'source_chord_ratio':'231/100','Hausdorff_ratio':'2979/400','near_roll_ratio':'7/2',
        'full_angle_ratio':'1033/100','Cayley_ratio':'517/100'}
def gate(value,label):pos(Q(value),label);return value
def configuration(data):
    require(set(data)=={'agent','role','closed_receiving_sectors','new_receiving_sector','bounds',
        'raw_outer_triangle','roll','coordinate_duals','coordinate_covector_norms','direct_own_row_norms',
        'bootstrap_stages','receiving_corner_interval'},'complete two-sector certificate grammar')
    require(data['agent']=='six-rupert-2' and data['role']=='researcher'
        and data['closed_receiving_sectors']==[23,28] and data['new_receiving_sector']==28,
        'actual author, old/new sectors and complete stated union')
    require(data['bounds']==BOUNDS and data['raw_outer_triangle']==RAW,'fresh entire closed sector28 domain')
    require(len(data['bootstrap_stages'])==4 and data['bootstrap_stages'][0]['L']=='517/100','four complete new signed stages')
    require(len(data['coordinate_duals'])==2 and {r['coordinate'] for r in data['coordinate_duals']}=={0,1},'both original-coordinate constructions')
    return tuple(tuple(Q(*map(F,x)) for x in row) for row in RAW)

def geometry(raw):
    V,core,axis,lift,integer_vertices=A.originals()
    require(tuple(V)==tuple(P.V),'identical actual original55 vertices')
    d0=(Q(),Q(-1),Q());d1=(Q(),Q(F(-1,2),F(-1,10)),Q(F(-1,2),F(1,10)))
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
    require(C==(Q(49,25)/8,Q(-23)/8-Q(0,F(57,40)),Q(-5)/4-Q(0,F(3,5))),'fresh physical area vector')
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
    require(d0==(Q(),Q(-1),Q()),'actual shared closed wall with old receiving-sector23')
    return {'raw_outer_triangle':raw,'actual_receiver_rays':[d0,d1],
        'entire_receiving_segment_norm_squared_candidates':candidates,'segment_stationary_parameter':parameter,
        'whole_sector_enclosure_gates':gates,'complete_original_facets':len(facets),
        'original_hull_counts':dict(counts),'area_fan_corner_gates':fan,
        'physical_area_vector':C,'independent_actual_shadow_hull':ids,
        'complete_actual_shadow_support_comparisons':support_count},C

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
    gamma,cs,hc,kt=F(33,5),F(231,100),F(2979,400),KT
    require(cs==F(7,20)*gamma and hc==F(9,4)*(1+cs),'actual inverse-area and original pairing constants')
    gates={'actual_area_tangent_norm':Q(gamma*gamma)-C[1]*C[1]-C[2]*C[2],
           'whole_sector_area_inside_global_tenth_budget':Q(F(1,10)-gamma*D),
           'new_uniform_error_strictly_contains_moving_error':Q(E-hc*D),
           'source_chord_inside_new_arcsine_domain':Q(F(1,80)-cs*D),
           'receiving_chord_inside_new_arcsine_domain':Q(F(1,80)-D),
           'fresh_arcsine_derivative_domain':Q(CR*CR*(1-F(1,160)**2)-1),
           'moving_near_threshold_inside_remote_guard':Q(B-kt*D),
           'full_spatial_angle_below1033over100delta':Q(THETA-CR*(1+cs)-2*kt),
           'actual_Cayley_radius_below517over100delta':Q(L0*(1-THETA*THETA*D*D/8)-THETA/2),
           'same_actual_companion_right_body_gauge':Q(1-(2*THETA+2*CR)*D),
           'positive_actual_companion_denominator':Q(1-L0*CR*D*D),
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
            'full_spatial_angle_ratio':THETA,'Cayley_ratio':L0,'scalar_gates':gates,
            'all45_signed_axis_squared_separations':separations,'actual_body_matrices':matrices,
            'actual_nonidentity_cosines':cosines,'whole_sector_absolute91over10000_bound_used':False}

def fresh_geometry(case,permutation,raw,stress,data):
    rays,rows,contacts,ms=P.A.geometry(case,permutation)
    require(rays==stress['actual_motion_rays'],'same actual original critical motion rays')
    comparisons=0;offsets=[]
    for a,b,j in contacts:
        edge=sub(V[b],V[a]);h0=dot(cross(edge,M.E),V[j]);pos(h0,'original critical positive offset')
        for u in raw:
            m=scale(1/h0,cross(edge,u));off=dot(m,V[a]);pos(off,'actual receiving positive support')
            require(dot(m,V[j])==off,'selected source original remains an actual receiving contact')
            for v in V:nonneg(off-dot(m,v),'original receiving edge versus every original vertex');comparisons+=1
            offsets.append(off)
    common=[]
    for a,b,j in stress['common_original_contacts']:
        edge=sub(V[b],V[a]);v=V[j];h0=dot(cross(edge,M.E),v);m=scale(1/h0,cross(edge,M.E))
        md=[scale(1/h0,cross(edge,dr)) for dr in [(Q(),Q(1),Q()),(Q(),Q(),Q(1))]]
        gd=[cross(v,x) for x in md]
        msq=sum((dot(x,x) for x in md),Q());gsq=sum((dot(x,x) for x in gd),Q())
        gates={'probe_norm':Q(F(49,100)**2)-dot(m,m),'probe_drift':Q(MD*MD)-CR*CR*msq,
               'torque_drift':Q(G*G)-CR*CR*gsq}
        for name,z in gates.items():gate(z,'original common '+name)
        common.append({'original_contact':[a,b,j],'critical_probe_norm2':dot(m,m),'probe_drift_Frobenius_norm2':msq,
                       'torque_drift_Frobenius_norm2':gsq,'exact_gates':gates})
    quadratic=gate(Z-F(9,4)*(F(49,100)+MD*D),'fresh common quadratic bound')
    for ray in rays:nonneg(1-dot(ray,ray),'actual unit ray bound, equality allowed')
    difference=sub(rays[1],rays[0]);den=dot(difference,difference);pos(den,'distinct actual motion rays')
    t=-dot(rays[0],difference)/den;candidates=[dot(a,a) for a in rays]
    if M.sg(t)>=0 and M.sg(1-t)>=0:candidates.append(dot(add(rays[0],scale(t,difference)),add(rays[0],scale(t,difference))))
    for v in candidates:gate(v-Q(AMIN*AMIN),'entire actual motion segment norm above7over10')
    old_balanced={'common_original_contacts':stress['common_original_contacts'],'critical_weights':enc(stress['critical_weights'])}
    finite=next(r for r in json.loads((REPO/'convex_geometry/rupert_j77_effective_mirror_cap/expected.json').read_text())['stratum_records'] if r['parent']==28)
    duals=[P.A.moments(k,next(r for r in data['coordinate_duals'] if r['coordinate']==k),rays,rows,contacts,ms,old_balanced,finite) for k in range(2)]
    chis=[F(x) for x in data['coordinate_covector_norms']];norms=[F(x) for x in data['direct_own_row_norms']]
    require(len(chis)==len(norms)==2 and all(x>0 for x in chis+norms),'both positive declared Euclidean norms')
    normgates=[];mirror_slack_corners=[]
    for k,dual in enumerate(duals):
        nonneg(Q(chis[k]*chis[k])-dot(dual['b'],dual['b']),'full actual coordinate covector Euclidean bound')
        ht=[sum((rays[k][i+1]*dual['bilinear_matrix'][i][j] for i in range(2)),Q()) for j in range(2)]
        z=gate(Q(norms[k]*norms[k])-dot(ht,ht),'direct own-row Euclidean norm bound');normgates.append(z)
        slack=[-dot(dual['b'],sub(u,M.E)[1:]) for u in raw]
        for x in slack:nonneg(x,'actual mirror slack on all closed new receiving corners')
        mirror_slack_corners.append(slack)
    return duals,chis,norms,{'original_contacts':contacts,'closed_corner_offsets':offsets,'complete_support_comparisons':comparisons,
            'actual_motion_rays':rays,'segment_minimum_candidates':candidates,'segment_stationary_parameter':t,
            'common_contact_drift':common,'fresh_quadratic_gate':quadratic,'own_row_norm_gates':normgates,
            'actual_closed_receiving_mirror_slack_corners':mirror_slack_corners}

def stage(record,duals,chis,norms):
    l=F(record['L']);oc,cc,orr,beta,w=[record[k] for k in ['ownC','pairC','ownrho','beta','W']]
    require(all(type(x)is int and x>0 for x in [oc,cc,orr,beta,w]),'positive integral stage bounds')
    error=G+Z*l
    gates={'ownC':oc*(1-F(3,2)*MU*MD*D)-F(3,2)*MU*error,
           'pairC':cc-oc*(1+L0*L0*D*D),'ownrho':orr-MR*(error+MD*oc*D),
           'pairrho':beta-DMAX*(orr+CR)}
    for name,z in gates.items():gate(z,'fresh simultaneous common '+name)
    coupling=[];errors=[]
    for k,dual in enumerate(duals):
        other=1-k;h=dual['corners'];chi,bn,mass,kn=chis[k],dual['bn'],dual['mass'],dual['kn']
        off=h[other][k]*chis[k]+2*h[other][other]*chis[other]
        row=[Q(),Q()];row[k]=D*DMAX*l*norms[k];row[other]=D*DMAX*l*off;coupling.append(row)
        errors.append((chi+bn)*(DMAX*l*l+beta*CR*l*l*D*D)+chi*beta*l+bn*beta*CR
          +bn*beta*beta*CR*l*D*D+mass*DMAX*beta*beta*l*D+kn*CR*cc
          +h[other][k]*chis[other]*chi*beta*CR*l*D)
    a,d=1-coupling[0][0],1-coupling[1][1];b,c=coupling[0][1],coupling[1][0];det=a*d-b*c
    for name,z in [('diagonal0',a),('diagonal1',d),('determinant',det)]:gates[name]=gate(z,'fresh directed inverse '+name)
    nonneg(b,'nonnegative offdiagonal0');nonneg(c,'nonnegative offdiagonal1')
    inverse=[[d/det,b/det],[c/det,a/det]];matrix=[[a,-b],[-c,d]]
    for order in [(matrix,inverse),(inverse,matrix)]:
        require([[sum((order[0][i][k]*order[1][k][j] for k in range(2)),Q()) for j in range(2)] for i in range(2)]
             ==[[Q(int(i==j)) for j in range(2)] for i in range(2)],'both exact directed inverse products')
    for row in inverse:
        for x in row:nonneg(x,'all inverse entries nonnegative')
    bounds=[2*(d*errors[0]+b*errors[1])/det,2*(c*errors[0]+a*errors[1])/det]
    gates['negative_parts']=gate(Q(w)-sum(bounds,Q()),'strict total signed negative-part bound')
    factor=KF*(1+1/AMIN);den=1-factor*w*D*D/2
    front=KF/AMIN*CR*(1+L0*D+L0*L0*D*D);nextl=F(record['next_motion_sum_ratio'])
    gates['bootstrap_absorption']=gate(den,'fresh norm absorption')
    gates['next_motion_sum']=gate(nextl*den-front,'fresh entire paired motion bound')
    return {'L':l,'ownC':oc,'pairC':cc,'ownrho':orr,'beta':beta,'W':w,'next_motion_sum_ratio':nextl,
            'common_error_ratio':error,'coupling_matrix':coupling,'remainder_constants':errors,
            'nonnegative_inverse':inverse,'coordinate_negative_part_bounds':bounds,'exact_gates':gates}

def chain(data,duals,chis,norms,stress):
    records=[];previous=None
    for fixture in data['bootstrap_stages']:
        if previous is not None:require(F(fixture['L'])==previous,'entire successive motion chain')
        records.append(stage(fixture,duals,chis,norms));previous=F(fixture['next_motion_sum_ratio'])
    gate(KF*KF*(1-(records[0]['beta']*D)**2)-1,'unconditional tangent controls Cayley norm')
    lo,hi=[F(x) for x in data['receiving_corner_interval']]
    require(0<lo<hi,'positive ordered receiving corner interval')
    cornergates=[]
    for i in range(2):
        for j in range(2):
            base=stress['critical_corners'][i][j];loss=stress['corner_losses'][i][j]
            cornergates.extend([gate(base-loss-Q(lo),'whole receiving lower corner'),gate(Q(hi)-base-loss,'whole receiving upper corner')])
    w,beta=records[-1]['W'],records[-1]['beta'];kappa=w*D*D;positive_ratio=(1+kappa)/AMIN
    gate(1/KF-kappa,'both positive coefficient sums have a positive lower bound')
    lower=lo*(1/(KF*KF)-kappa/KF)-hi*positive_ratio*kappa;upper=F(101,100)*(beta*D)**2
    gap=gate(lower-upper,'strict signed bilinear contradiction')
    return {'four_exact_stages':records,'receiving_corner_gates':cornergates,'final_kappa':kappa,
            'positive_sum_ratio':positive_ratio,'signed_bilinear_lower':lower,'axial_bilinear_upper':upper,'final_positive_gap':gap}

def malformed(data,geo,duals,chis,norms,stress,case,permutation):
    tests=[]
    for change in ['domain','error','radius','sector','union','stages','coordinate']:
        bad=copy.deepcopy(data)
        if change=='domain':bad['raw_outer_triangle'][1][1]=['-1/7','0']
        elif change=='error':bad['bounds']['outer_error']='353/10000'
        elif change=='radius':bad['bounds']['physical_chord_upper']='1/100'
        elif change=='sector':bad['new_receiving_sector']=27
        elif change=='union':bad['closed_receiving_sectors']=[23]
        elif change=='stages':bad['bootstrap_stages'].pop()
        else:bad['coordinate_duals'].pop()
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
    for field in ['ownC','pairC','ownrho','beta','W']:
        bad=copy.deepcopy(data['bootstrap_stages'][0]);bad[field]=1
        tests.append(lambda bad=bad:stage(bad,duals,chis,norms))
    wrong=copy.deepcopy(data);wrong['bootstrap_stages'][1]['L']='3'
    tests.append(lambda:chain(wrong,duals,chis,norms,stress))
    bad=copy.deepcopy(data);bad['receiving_corner_interval']=['9/20','23/50']
    tests.append(lambda bad=bad:chain(bad,duals,chis,norms,stress))
    for field in ['coordinate_covector_norms','direct_own_row_norms']:
        bad=copy.deepcopy(data);bad[field][0]='1'
        tests.append(lambda bad=bad:fresh_geometry(case,permutation,configuration(data),stress,bad))
    for change in ['negative_weight','duplicate_basis','missing_repair']:
        bad=copy.deepcopy(data)
        if change=='negative_weight':bad['coordinate_duals'][0]['coefficients'][0]=['-1','0']
        elif change=='duplicate_basis':bad['coordinate_duals'][0]['basis'][0]=bad['coordinate_duals'][0]['basis'][1]
        else:bad['coordinate_duals'][0]['common_stress_multiplier']=0
        tests.append(lambda bad=bad:fresh_geometry(case,permutation,configuration(data),stress,bad))
    for number,test in enumerate(tests):
        try:test()
        except (ValueError,KeyError,IndexError,TypeError,ZeroDivisionError):continue
        raise ValueError('Malformed new two-sector certificate accepted: '+str(number))
    return len(tests)

def check(self_test):
    # All original parent evidence BEFORE any new predicate enters either registry.
    old=S.check(True);old_bytes=(json.dumps(old,indent=1)+'\n').encode()
    require(old_bytes==(REPO/PARENT/'expected.json').read_bytes(),'EVERY complete direct-parent byte')
    require(old['whole_closed_sector23_cap_strict_passage_excluded']
        and old['all_original_sources_full_roll_arbitrary_translation_scale_ge1'],
        'old whole-sector23 containment branch retained')
    require(P.D==D and P.CR==CR,'identical generic raw receiving-stress budget, old guards unchanged')
    data=json.loads((HERE/'certificates.json').read_text());raw=configuration(data)
    area_geometry,C=geometry(raw);geo=R.geometry();roll_record=roll(data['roll'],geo)
    moving=moving_and_gauge(C,roll_record['signed_near_records'])
    case=next(r for r in json.loads((REPO/'convex_geometry/rupert_j77_uniform_local_exclusion/certificates.json').read_text())['cases'] if r['parent']==28)
    index={v:j for j,v in enumerate(V)};permutation=[index[M.rotate(v)] for v in V]
    balance=next(r for r in json.loads((REPO/'convex_geometry/rupert_j77_receiving_balanced_stress/certificates.json').read_text())['cases'] if r['parent']==28)
    critical=next(r for r in json.loads((REPO/'convex_geometry/rupert_j77_bilinear_mirror_cap/certificates.json').read_text())['cases'] if r['parent']==28)
    critical_originals=PB.BIL.stratum(case,critical,permutation,PB.BIL.reflection_algebra())
    stress=P.receiving_stress(case,balance,critical,permutation)
    duals,chis,norms,contacts=fresh_geometry(case,permutation,raw,stress,data)
    require(duals[1]['corners'][0]==[Q(),Q()] and duals[1]['B']==(Q(),Q(),Q())
        and duals[1]['K']==0,'actual second coordinate has zero opposite row and source-normal moments')
    result=chain(data,duals,chis,norms,stress)
    require(len(result['four_exact_stages'])==4,'four fully verified signed stages')
    for r in result['four_exact_stages']:
        require(r['coupling_matrix'][1][0]==0,'fresh directed coupling really is triangular')
    universal=PB.universal_factorization()
    controls=malformed(data,geo,duals,chis,norms,stress,case,permutation) if self_test else 0
    for registry in [M.area,P.C.A]:
        for pair,sign in tuple(registry.SIGNS.items()):require(registry.interval_sign(pair)==sign,'independent positive-sqrt5 rational sign enclosure')
    return enc({'agent':'six-rupert-2','role':'researcher','target':'original asymmetric55vertex unit-edge J77',
        'proof_status':'complete author-checked written continuous intermediate proof with exact finite hypotheses; unformalized',
        'independent_review_asserted':False,'global_J77_Rupert_resolved':False,
        'whole_closed_receiving_sectors':[23,28],'physical_chord_upper':'1/200',
        'new_closed_sector28_strict_passage_excluded':True,
        'all_original_sources_full_roll_arbitrary_physical_translation_scale_ge1':True,
        'closed_classification':'lambda1,t0,Qh=I or M_nM_q; actual RIGHT C5 body factor; both equal shadows',
        'whole_one_over200_mirror_cap_proved':False,
        'complete_direct_parent_replay':{'directory':PARENT,'bytes':len(old_bytes),'sha256':sha256(old_bytes).hexdigest()},
        'fresh_sector28_area_and_enclosure':area_geometry,'fresh_complete_O2_roll_cover':roll_record,
        'fresh_moving_and_same_gauge':moving,'fresh_original_common_duals':critical_originals,
        'fresh_receiving_stress':stress,'fresh_original_contact_geometry':contacts,
        'fresh_positive_coordinate_stresses':duals,'coordinate_covector_norms':chis,'direct_own_row_norms':norms,
        'actual_second_opposite_row_zero':True,'all_four_directed_couplings_triangular':True,
        'directed_signed_chain':result,'universal_receiving_balanced_factorization':universal,
        'malformed_controls':controls,'fixture_sha256':digest(data),
        'registered_independent_sign_counts_by_parent_registry':[len(M.area.SIGNS),len(P.C.A.SIGNS)],
        'remaining_frontier':'five other primitive receiving sectors, a complete larger mirror cap, and global J77 remain OPEN'})

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--self-test',action='store_true');parser.add_argument('--emit',action='store_true')
    args=parser.parse_args();result=check(args.self_test);encoded=(json.dumps(result,indent=1)+'\n').encode()
    if not args.emit:require(encoded==(HERE/'expected.json').read_bytes(),'EVERY expected byte; use --self-test')
    print(encoded.decode(),end='')
