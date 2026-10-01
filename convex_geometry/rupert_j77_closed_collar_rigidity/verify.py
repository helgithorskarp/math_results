"""Exact finite hypotheses for J77 closed collar rigidity.

six-rupert-2, researcher. Python3.11+, standard library, Q(sqrt5).
Continuous original-shadow and signed-motion bridges are in PROOF.md.
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
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj
manifest=json.loads((HERE/'dependencies.json').read_text())
PARENTS=[('convex_geometry/rupert_j77_complete_signed_mirror_cap','46410a3250dea5bb32ec5d3acaae4f1ca3bc906d'),
         ('convex_geometry/rupert_j77_inverse_area_collar','6345acdb4574fe0100230e6c04235892f4cfb13d')]
require(len(manifest)==2,'two declared mathematical parents')
for dep,(directory,commit) in zip(manifest,PARENTS):
    require(set(dep)=={'source_directory','source_commit','sha256'} and dep['source_directory']==directory
            and dep['source_commit']==commit and set(dep['sha256'])=={'.gitignore','README.md','PROOF.md','verify.py',
                'certificates.json','dependencies.json','expected.json'},'complete pinned direct parent')
    for name,digest in dep['sha256'].items():
        require(sha256((REPO/directory/name).read_bytes()).hexdigest()==digest,'changed parent '+name)
A=module('j77_closed_collar_cap_parent',REPO/PARENTS[0][0]/'verify.py')
C=module('j77_closed_collar_inverse_parent',REPO/PARENTS[1][0]/'verify.py')
PB,M,MV,Q,V=A.PB,A.M,A.MV,A.Q,A.V
dot,cross,add,sub,scale=M.dot,M.cross,M.add,M.sub,M.scale
pos,nonneg,absq,norm1,decode,enc=M.pos,M.nonneg,M.absq,M.norm1,M.decode,M.enc
sq=lambda x:x*x
D,CR,L0,KF,AMIN=F(1,200),F(1001,1000),F(501,100),F(51,50),F(7,10)
DMAX=1+L0*CR*D*D
G,MD,Z=F(19,10),F(27,25),F(9,8)
MU,MR=F(807,100),F(374,100)
RAW=[['1','-1/450','1/900'],['1','-1/300','0'],['1','-1/225','1/450']]
def gate(value,label):pos(Q(value),label);return value
def configuration(data):
    require(data['agent']=='six-rupert-2' and data['role']=='researcher' and data['parent']==23,'author and exact sector')
    require(data['raw_triangle']==RAW and data['physical_chord_upper']=='1/200','whole actual closed collar')
    require(data['moving_constants']=={'Gamma':'61/10','half_tangent_ratio':'10/3','full_angle_ratio':'10','Cayley_ratio':'501/100'},'moving statement constants')
    require(data['contact_constants']=={'critical_probe_norm_upper':'49/100','torque_drift_ratio':'19/10',
            'probe_drift_ratio':'27/25','quadratic_error_ratio':'9/8'},'fresh common statement constants')
    require(len(data['bootstrap_stages'])==6,'complete six-stage chain')
    require(data['bootstrap_stages'][0]['L']=='501/100','unconditional entry motion bound')
    require(len(data['coordinate_duals'])==2 and {r['coordinate'] for r in data['coordinate_duals']}=={0,1},'both exact coordinate constructions')
    return tuple(tuple(Q(F(x)) for x in row) for row in data['raw_triangle'])

def moving_and_gauge(collar):
    cv=decode(collar['new_closed_receiving_collar']['physical_area_vector'])
    gamma=F(61,10);cs=F(7,20)*gamma;hc=F(9,4)*(1+cs);kt=F(10,3)
    gates={'area_tangent_norm':Q(gamma*gamma)-cv[1]*cv[1]-cv[2]*cv[2],
           'moving_area_in_global_budget':Q(F(1,10)-gamma*D),
           'moving_near_inside_remote_guard':Q(F(1,20)-kt*D),
           'full_angle_below10delta':Q(10-CR*(1+cs)-2*kt),
           'Cayley_below501over100delta':Q(L0*(1-F(25,2)*D*D)-5),
           'physical_to_raw_ratio':Q(CR*(1-D*D/2)-1),
           'same_companion_right_gauge':Q(1-(20+2*CR)*D),
           'positive_reflected_denominator':Q(1-L0*CR*D*D)}
    for row in collar['fresh_all_source_full_roll_reduction']['signed_near_records']:
        height=Q(*map(F,row['physical_contact_height']));n=Q(*map(F,row['norm_upper']));l=Q(*map(F,row['directed_torque']))
        tag=str(row['sign']);b=F(1,20)
        gates['moving_near_lower_'+tag]=kt*l-hc*n-kt*kt*(2*height+hc*n*D)*D
        gates['moving_near_guard_'+tag]=l*b-(2*height+hc*n*D)*b*b-hc*n*D
    axes=[];x=M.E
    for j in range(5):axes.extend([x,scale(-1,x)]);x=M.rotate(x)
    require(x==M.E and len(set(axes))==10,'all ten distinct signed actual axes')
    separation=[]
    for i,a in enumerate(axes):
        for b in axes[i+1:]:
            z=dot(sub(a,b),sub(a,b));gate(z-Q(F(9,25)),'signed actual axis separation')
            separation.append(z)
    gates['both_source_budgets_inside_unique_axis_ball']=Q(F(1,80)-cs*D)
    gates['absolute_budget_inside_unique_axis_ball']=Q(F(1,80)-F(91,10000))
    gates['unique_axis_balls_disjoint']=Q(F(3,5)-F(2,80))
    base=[(Q(1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1))]
    images=base[:];vertices=list(V);matrices=[];cosines=[]
    for j in range(5):
        require(set(vertices)==set(V),'actual proper body vertex permutation')
        require([[dot(a,b) for b in images] for a in images]==[[Q(int(i==k)) for k in range(3)] for i in range(3)],'body orthogonality')
        require(dot(images[0],cross(images[1],images[2]))==1,'body proper orientation')
        matrices.append([list(row) for row in zip(*images)])
        if j:
            co=(sum((images[i][i] for i in range(3)),Q())-1)/2
            gate(Q(F(1,2))-co,'actual nonidentity body angle exceeds1');cosines.append(co)
        images=[M.rotate(v) for v in images];vertices=[M.rotate(v) for v in vertices]
    require(images==base and vertices==list(V),'actual order-five closure')
    require(set(((-v[0],v[1],v[2]) for v in V))==set(V),'actual original body mirror')
    for name,z in gates.items():gate(z,'moving/gauge '+name)
    return {'Gamma':gamma,'source_chord_ratio':cs,'paired_original_error_ratio':hc,'half_tangent_ratio':kt,
            'full_angle_ratio':10,'Cayley_ratio':L0,'scalar_gates':gates,
            'signed_axis_squared_separations':separation,'actual_body_matrices':matrices,'nonidentity_cosines':cosines}

def receiving_stress(case,fixture,parent,permutation):
    """Fresh uniform inverse on the raw ball CR/200; old radius is not changed."""
    require(fixture['input_common_weights']==parent['input_common_weights'],'same exact original critical common construction')
    weights=decode(fixture['input_common_weights'])
    contacts,common,rays,ms,vs,ks,h=PB.geometry(case,permutation)
    require(len(weights)==6 and all(dot(row,weights)==int(i==0) for i,row in enumerate(h)),'all critical balance coordinates')
    for w in weights:nonneg(w-Q(F(1,20)),'critical positive weight floor')
    ids=fixture['balance_basis'];require(len(ids)==len(set(ids))==4 and all(type(i)is int and 0<=i<6 for i in ids),'four distinct receiving balance columns')
    inv=PB.matrix_inverse([[row[i] for i in ids] for row in h])
    b=[sum((w*k*v[j] for w,k,v in zip(weights,ks,vs)),Q()) for j in (1,2)]
    k0=dot(weights,ks)
    hy=[[Q()]*6,[k*v[1] for k,v in zip(ks,vs)],[Q()]*6,ks]
    hz=[[Q()]*6,[k*v[2] for k,v in zip(ks,vs)],[-k for k in ks],[Q()]*6]
    rhs=[[Q(),Q()],[-b[0],-b[1]],[Q(),k0],[-k0,Q()]]
    ay=PB.matmul(inv,[[row[i] for i in ids] for row in hy]);az=PB.matmul(inv,[[row[i] for i in ids] for row in hz]);br=PB.matmul(inv,rhs)
    qr=[sum((absq(y)+absq(z) for y,z in zip(ry,rz)),Q()) for ry,rz in zip(ay,az)]
    bb=[norm1(row) for row in br];radius=Q(CR*D);q=max(qr)
    gap=gate(1-q*radius,'fresh receiving Neumann gap');tmax=max(bb)*radius/gap
    tau=[Q()]*6
    for i,bi,qi in zip(ids,bb,qr):tau[i]=bi*radius+qi*radius*tmax
    floors=[w-t for w,t in zip(weights,tau)]
    for w in floors:gate(w-Q(F(1,25)),'fresh receiving positive weight on entire raw ball')
    ey,ez=(Q(),Q(1),Q()),(Q(),Q(),Q(1));pairs=[];losses=[]
    for a in rays:
        row=[];lossrow=[]
        for c in rays:
            vals=[PB.critical_corner(a,c,v,m) for v,m in zip(vs,ms)]
            middle=(max(vals[i] for i in ids)+min(vals[i] for i in ids))/2
            change=sum((tau[i]*absq(vals[i]-middle) for i in ids),Q())
            ly=[PB.receiving_corner(a,c,v,k,ey) for v,k in zip(vs,ks)];lz=[PB.receiving_corner(a,c,v,k,ez) for v,k in zip(vs,ks)]
            change+=radius*(absq(dot(weights,ly))+absq(dot(weights,lz)))
            change+=radius*sum((t*(absq(y)+absq(z)) for t,y,z in zip(tau,ly,lz)),Q())
            row.append(dot(weights,vals));lossrow.append(change)
        pairs.append(row);losses.append(lossrow)
    bbound=norm1(b)+sum((t*absq(k)*norm1(v[1:]) for t,k,v in zip(tau,ks,vs)),Q())
    hlo,hhi=1-radius*bbound,1+radius*bbound
    gate(hlo-Q(F(99,100)),'fresh physical stress height lower');gate(Q(F(101,100))-hhi,'fresh physical stress height upper')
    return {'common_original_contacts':[contacts[i] for i in common],'actual_motion_rays':rays,'critical_weights':weights,
            'balance_basis':ids,'critical_balance_matrix':h,'critical_balance_inverse':inv,'matrix_y':ay,'matrix_z':az,
            'inverse_rhs':br,'row_Neumann_constants':qr,'row_rhs_constants':bb,'raw_radius':radius,'Neumann_gap':gap,
            'weight_change_bounds':tau,'positive_weight_lower_bounds':floors,'critical_corners':pairs,'corner_losses':losses,
            'stress_height_bounds':[hlo,hhi],'critical_B':b,'critical_K':k0}

def fresh_geometry(case,permutation,raw,stress,data):
    rays,rows,contacts,ms=A.geometry(case,permutation)
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
    finite=next(r for r in json.loads((REPO/'convex_geometry/rupert_j77_effective_mirror_cap/expected.json').read_text())['stratum_records'] if r['parent']==23)
    duals=[A.moments(k,next(r for r in data['coordinate_duals'] if r['coordinate']==k),rays,rows,contacts,ms,old_balanced,finite) for k in range(2)]
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
            'actual_closed_collar_mirror_slack_corners':mirror_slack_corners}

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
    return {'six_exact_stages':records,'receiving_corner_gates':cornergates,'final_kappa':kappa,
            'positive_sum_ratio':positive_ratio,'signed_bilinear_lower':lower,'axial_bilinear_upper':upper,'final_positive_gap':gap}

def malformed(data,duals,chis,norms,stress,raw,case,permutation):
    tests=[]
    for change in ['stage','domain','Gamma','coordinate']:
        bad=copy.deepcopy(data)
        if change=='stage':bad['bootstrap_stages'].pop()
        elif change=='domain':bad['raw_triangle'][0][1]='-1/45'
        elif change=='Gamma':bad['moving_constants']['Gamma']='6'
        else:bad['coordinate_duals'].pop()
        tests.append(lambda bad=bad:configuration(bad))
    for field in ['ownC','pairC','ownrho','beta','W']:
        bad=copy.deepcopy(data['bootstrap_stages'][0]);bad[field]=1
        tests.append(lambda bad=bad:stage(bad,duals,chis,norms))
    wrong=copy.deepcopy(data);wrong['bootstrap_stages'][1]['L']='3'
    tests.append(lambda:chain(wrong,duals,chis,norms,stress))
    for field in ['coordinate_covector_norms','direct_own_row_norms']:
        bad=copy.deepcopy(data);bad[field][0]='1'
        tests.append(lambda bad=bad:fresh_geometry(case,permutation,raw,stress,bad))
    for field in ['negative_weight','duplicate_row']:
        bad=copy.deepcopy(data)
        if field=='negative_weight':bad['coordinate_duals'][0]['coefficients'][0]=['-1','0']
        else:bad['coordinate_duals'][0]['basis'][0]=bad['coordinate_duals'][0]['basis'][1]
        tests.append(lambda bad=bad:fresh_geometry(case,permutation,raw,stress,bad))
    bad=copy.deepcopy(data);bad['receiving_corner_interval']=['9/20','23/50']
    tests.append(lambda:chain(bad,duals,chis,norms,stress))
    for test in tests:
        try:test()
        except (ValueError,KeyError,IndexError,TypeError,ZeroDivisionError):continue
        raise ValueError('Malformed new closed-collar certificate accepted')
    return len(tests)

def check(self_test):
    # Each complete parent is replayed before any new predicate enters its registry.
    parent_cap=A.check(True);cap_bytes=(json.dumps(parent_cap,indent=1)+'\n').encode()
    require(cap_bytes==(REPO/PARENTS[0][0]/'expected.json').read_bytes(),'EVERY complete signed-cap parent byte')
    parent_collar=C.check(True);collar_bytes=(json.dumps(parent_collar,indent=1)+'\n').encode()
    require(collar_bytes==(REPO/PARENTS[1][0]/'expected.json').read_bytes(),'EVERY complete inverse-area/roll collar parent byte')
    require(tuple(V)==tuple(C.R.geometry()[0]),'same original55 source labels in both mathematical parents')
    data=json.loads((HERE/'certificates.json').read_text());raw=configuration(data)
    moving=moving_and_gauge(parent_collar)
    case=next(r for r in json.loads((REPO/'convex_geometry/rupert_j77_uniform_local_exclusion/certificates.json').read_text())['cases'] if r['parent']==23)
    idx={v:i for i,v in enumerate(V)};permutation=[idx[M.rotate(v)] for v in V]
    balance_fixture=next(r for r in json.loads((REPO/'convex_geometry/rupert_j77_receiving_balanced_stress/certificates.json').read_text())['cases'] if r['parent']==23)
    critical_parent=next(r for r in json.loads((REPO/'convex_geometry/rupert_j77_bilinear_mirror_cap/certificates.json').read_text())['cases'] if r['parent']==23)
    stress=receiving_stress(case,balance_fixture,critical_parent,permutation)
    duals,chis,norms,geometry=fresh_geometry(case,permutation,raw,stress,data)
    universal=PB.universal_factorization()
    result=chain(data,duals,chis,norms,stress)
    negative=malformed(data,duals,chis,norms,stress,raw,case,permutation) if self_test else 0
    for area in [M.area,C.A]:
        for pair,sign in tuple(area.SIGNS.items()):require(area.interval_sign(pair)==sign,'independent rational positive-sqrt5 enclosure')
    return enc({'agent':'six-rupert-2','role':'researcher','target':'original asymmetric55vertex unit-edge J77',
        'proof_status':'complete author-checked written intermediate proof and exact finite hypotheses; unformalized',
        'independent_review_asserted':False,'global_J77_Rupert_resolved':False,'closed_collar_strict_passage_excluded':True,
        'raw_receiving_triangle':raw,'physical_chord_band':['1/500','1/200'],
        'entire_original_source_full_roll_translation_scale_ge1':True,
        'closed_classification':'lambda1,t0,Qh=I or M_nM_q; actual RIGHT C5 factor; both equal shadows',
        'complete_direct_parent_replays':[{'directory':PARENTS[0][0],'bytes':len(cap_bytes),'sha256':sha256(cap_bytes).hexdigest()},
                                         {'directory':PARENTS[1][0],'bytes':len(collar_bytes),'sha256':sha256(collar_bytes).hexdigest()}],
        'moving_and_same_gauge':moving,'fresh_receiving_stress':stress,'fresh_original_contact_geometry':geometry,
        'two_positive_coordinate_stresses':duals,'coordinate_covector_norms':chis,'direct_own_row_norms':norms,
        'receiving_balanced_universal_factorization':universal,'directed_signed_chain':result,
        'malformed_controls':negative,'fixture_sha256':M.digest(data),
        'registered_independent_sign_counts_by_parent_registry':[len(M.area.SIGNS),len(C.A.SIGNS)],
        'remaining_frontier':'larger receiving collars, other receiving sectors and the global named-solid decision remain OPEN'})

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--self-test',action='store_true');p.add_argument('--emit',action='store_true')
    args=p.parse_args();result=check(args.self_test);encoded=(json.dumps(result,indent=1)+'\n').encode()
    if not args.emit:require(encoded==(HERE/'expected.json').read_bytes(),'EVERY expected output byte; use --self-test')
    print(encoded.decode(),end='')
