"""Exact finite hypotheses for J77's unconditional complete 1/1000 mirror cap.

Author six-rupert-2, researcher. Python3.11+, standard library, Q(sqrt5).
The directed negative-part and continuous projection proof is in PROOF.md.
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
    if not ok:
        raise ValueError(message)

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    out=importlib.util.module_from_spec(spec);spec.loader.exec_module(out)
    return out

deps=json.loads((HERE/'dependencies.json').read_text())
require(len(deps)==1 and deps[0]['source_directory']=='convex_geometry/rupert_j77_signed_mirror_sectors'
        and deps[0]['source_commit']=='843712820fd1ee1496cc82228794a8d7fe4f0fa3','one declared complete signed-sector input')
require(set(deps[0]['sha256'])=={'.gitignore','README.md','PROOF.md','verify.py','algebra.py',
        'certificates.json','dependencies.json','expected.json'},'all eight direct source files pinned')
for name,digest in deps[0]['sha256'].items():
    require(sha256((REPO/deps[0]['source_directory']/name).read_bytes()).hexdigest()==digest,'changed direct source: '+name)
SIGNED=module('j77_complete_signed_input',REPO/deps[0]['source_directory']/'verify.py')
PB,M,MV,Q,V=SIGNED.PB,SIGNED.M,SIGNED.MV,SIGNED.Q,SIGNED.V
dot,cross,add,sub,scale=M.dot,M.cross,M.add,M.sub,M.scale
pos,nonneg,absq,norm1,decode,enc=M.pos,M.nonneg,M.absq,M.norm1,M.decode,M.enc
D,CR=F(1,1000),F(1001,1000)
DMAX=1+10*CR*D*D
L0,BETA0,CC0=F(151,20),121,386
KF,AMIN=F(51,50),F(7,10)
MU,MR=F(807,100),F(374,100)
PARENTS={21,23,28,30,31,32,33}

def gate(gap,message):
    pos(Q(gap),message)
    return gap

def coverage(data):
    require(data['agent']=='six-rupert-2' and data['role']=='researcher','actual author and role')
    require(type(data['receiver_cap_denominator']) is int and data['receiver_cap_denominator']==1000,
            'whole stated physical chord radius')
    require(len(data['cases'])==7 and {r['parent'] for r in data['cases']}==PARENTS,'all seven CLOSED receiving sectors')
    for case in data['cases']:
        require(type(case['parent']) is int,'integer original stratum id')
        require(len(case['coordinate_duals'])==2 and {c['coordinate'] for c in case['coordinate_duals']}=={0,1},
                'both critical coordinate inequalities')
        require(all(type(c['coordinate']) is int for c in case['coordinate_duals']),'integer coordinate labels')

def mdot(a,h,b):
    return sum((a[i]*h[i][j]*b[j] for i in range(2) for j in range(2)),Q())

def group_and_initial_gates():
    axes=[(Q(1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1))]
    require(M.AXIS==(Q(),Q(F(1,2),F(1,2)),Q(1)),'actual standard C5 body axis')
    matrices=[];images=axes[:];originals=list(V);index=set(V)
    cosines=[]
    for j in range(5):
        require(set(originals)==index,'actual original vertex permutation under each proper body factor')
        require([[dot(images[i],images[k]) for k in range(3)] for i in range(3)]
                ==[[Q(int(i==k)) for k in range(3)] for i in range(3)],'actual body matrices orthogonal')
        require(dot(images[0],cross(images[1],images[2]))==1,'actual body matrices proper')
        matrices.append([list(row) for row in zip(*images)])
        if j:
            co=(sum((images[i][i] for i in range(3)),Q())-1)/2
            gate(Q(F(1,2))-co,'each nonidentity proper C5 factor has principal angle above1')
            cosines.append(co)
        images=[M.rotate(v) for v in images]
        originals=[M.rotate(v) for v in originals]
    require(images==axes and originals==list(V),'actual order-five group closure')
    gaps={
        'companion_angle_before_sharpening':18-(15+2*CR),
        'unique_companion_right_gauge':1-33*D,
        'both_Cayley_norms_below151_over20_delta':L0*(1-F(225,8)*D*D)-F(15,2),
        'fresh_initial_own_C385':385*(1-9*MU*D)-F(3,2)*MU*(12+F(23,10)*L0),
        'fresh_initial_pair_C386':386-385*(1+100*D*D),
        'fresh_initial_own_rho119':119-MR*(12+F(23,10)*L0+6*385*D),
        'fresh_initial_pair_rho121':121-DMAX*(119+CR),
        'unconditional_tangent_norm_factor51_over50':KF*KF*(1-(BETA0*D)**2)-1,
        'whole_raw_chart_denominator_lower':1-10*CR*D*D,
    }
    for name,gap in gaps.items():gate(gap,'whole-cap initial gate: '+name)
    return {'actual_C5_matrices':matrices,'nonidentity_principal_cosines':cosines,'rational_gates':gaps}

def geometry(case,permutation):
    rays=[scale(1/norm1(M.rotate(decode(a)[:3])),M.rotate(decode(a)[:3])) for a in case['extreme_motions']]
    require(len(rays)==2 and M.det2(*rays)!=0,'independent actual critical tangent rays')
    rows,contacts,ms=[],[],[]
    for ox,oy,oj in case['contacts']:
        a,b,j=permutation[oy],permutation[ox],permutation[oj]
        edge=sub(V[b],V[a]);h=dot(cross(edge,M.E),V[j]);pos(h,'original positive critical support')
        m=scale(1/h,cross(edge,M.E));g=cross(V[j],m)
        require(m[0]==0 and dot(m,V[a])==dot(m,V[b])==dot(m,V[j])==1,'full original contact normalization')
        for dr in [(Q(),Q(1),Q()),(Q(),Q(),Q(1))]:
            require(scale(1/h,cross(edge,dr))==add(scale(-dot(m,dr),M.E),scale(edge[0]/h,cross(M.E,dr))),
                    'full affine original-edge normal, with noncommon source coordinates')
        rows.append([g[0],dot(g,rays[0]),dot(g,rays[1]),m[1],m[2]])
        contacts.append((a,b,j));ms.append(m)
    require(len(rows)==32 and len(case['common_indices'])==6,'all original contact rows and six common originals')
    return rays,rows,contacts,ms

def moments(coordinate,fixture,rays,rows,contacts,ms,balanced,finite):
    ids=fixture['basis'];base=decode(fixture['coefficients']);sigma=fixture['common_stress_multiplier']
    require(type(coordinate) is int and coordinate in (0,1),'integer coordinate')
    require(len(ids)==len(base)==4 and len(set(ids))==4 and
            all(type(i) is int and 0<=i<32 for i in ids),'four distinct original base rows')
    require(type(sigma) is int and sigma>=0,'nonnegative exact common stress repair')
    weights=[Q() for _ in contacts]
    for i,c in zip(ids,base):
        nonneg(c,'nonnegative base contact weight');weights[i]+=c
    common=balanced['common_original_contacts'];omega=decode(balanced['critical_weights'])
    require(len(common)==len(omega)==6,'six actual critical common weights')
    for triple,w in zip(common,omega):
        triple=tuple(triple);pos(w,'positive original critical common stress')
        require(V[triple[2]][0]==0,'original mirror-fixed common source')
        weights[contacts.index(triple)]+=sigma*w
    for c in weights:nonneg(c,'augmented positive original contact weight')
    require(all(sum((c*row[j] for c,row in zip(weights,rows)),Q())==-int(j==coordinate+1)
                for j in range(5)),'all five critical coordinate identities after repair')
    chosen=[i for i,w in enumerate(weights) if w!=0]
    cs=[weights[i] for i in chosen];cc=[contacts[i] for i in chosen]
    vv=[V[t[2]] for t in cc];mm=[ms[i] for i in chosen];kk=[]
    for a,b,j in cc:
        edge=sub(V[b],V[a]);kk.append(edge[0]/dot(cross(edge,M.E),V[j]))
    mass=sum(cs,Q())
    b=[sum((c*v[0]*m[j+1] for c,v,m in zip(cs,vv,mm)),Q()) for j in range(2)]
    s=[[sum((c*v[i+1]*m[j+1] for c,v,m in zip(cs,vv,mm)),Q()) for j in range(2)] for i in range(2)]
    bv=tuple(sum((c*k*v[j] for c,k,v in zip(cs,kk,vv)),Q()) for j in range(3))
    kd=sum((c*k for c,k in zip(cs,kk)),Q())
    require(s[0][1]==s[1][0] and s[0][0]+s[1][1]==mass,'symmetric critical stress with full trace')
    require(all(dot((Q(),-b[1],b[0]),a)==-int(j==coordinate) for j,a in enumerate(rays)),
            'unchanged actual coordinate covector after common-stress repair')
    jmat=[[Q(),Q(-1)],[Q(1),Q()]]
    h=[[mass*int(i==j)-s[i][j]+bv[0]*jmat[i][j] for j in range(2)] for i in range(2)]
    corners=[[mdot(a[1:],h,bb[1:]) for bb in rays] for a in rays]
    for j in range(2):nonneg(corners[1-coordinate][j],'entire opposite row favorable after repair')
    for raw in [decode(ray) for ray in finite['receiver_rays']]:
        nonneg(-dot(b,raw[1:]),'mirror coordinate nonnegative on the ENTIRE closed receiving sector')
    identity=SIGNED.ALG.identities(M,MV,cc,cs,mass,b,s,bv,kd)
    return {'coordinate':coordinate,'common_stress_multiplier':sigma,'basis':chosen,'coefficients':cs,
            'original_contacts':cc,'mass':mass,'b':b,'chi':norm1(b),'S':s,'B':bv,'K':kd,
            'bn':norm1(bv[1:]),'kn':absq(kd),'bilinear_matrix':h,'corners':corners,
            'universal_original_contact_identity':identity}

def directed_bound(duals,L,beta,cc,W,label):
    chis=[r['chi'] for r in duals];cmat=[];errors=[]
    for k,dual in enumerate(duals):
        l=1-k;h=dual['corners'];chi,bn,c,kn=dual['chi'],dual['bn'],dual['mass'],dual['kn']
        own=sum((absq(h[k][j])*chis[j] for j in range(2)),Q())
        other=h[l][k]*chis[k]+2*h[l][l]*chis[l]
        row=[Q(),Q()];row[k]=D*DMAX*L*own;row[l]=D*DMAX*L*other;cmat.append(row)
        error=(chi+bn)*(DMAX*L*L+beta*CR*L*L*D*D)+chi*beta*L+bn*beta*CR \
            +bn*beta*beta*CR*L*D*D+c*DMAX*beta*beta*L*D+kn*CR*cc \
            +h[l][k]*chis[l]*chi*beta*CR*L*D
        errors.append(error)
    a,d=1-cmat[0][0],1-cmat[1][1];b,c=cmat[0][1],cmat[1][0];det=a*d-b*c
    nonneg(b,label+' nonnegative offdiagonal0');nonneg(c,label+' nonnegative offdiagonal1')
    gaps={'diagonal0':a,'diagonal1':d,'determinant':det}
    for name,gap in gaps.items():gate(gap,label+' inverse gate: '+name)
    inverse=[[d/det,b/det],[c/det,a/det]]
    matrix=[[a,-b],[-c,d]]
    require([[sum((matrix[i][k]*inverse[k][j] for k in range(2)),Q()) for j in range(2)] for i in range(2)]
            ==[[Q(1),Q()],[Q(),Q(1)]],'EXACT directed inverse product')
    require([[sum((inverse[i][k]*matrix[k][j] for k in range(2)),Q()) for j in range(2)] for i in range(2)]
            ==[[Q(1),Q()],[Q(),Q(1)]],'EXACT directed reverse inverse product')
    bounds=[2*(d*errors[0]+b*errors[1])/det,2*(c*errors[0]+a*errors[1])/det]
    gap=gate(Q(W)-sum(bounds,Q()),label+' strict total negative-part upper bound')
    return {'L':L,'beta':beta,'cc':cc,'coupling_matrix':cmat,'errors':errors,'inverse_gaps':gaps,
            'nonnegative_inverse':inverse,'negative_parts_coordinate_bounds':bounds,
            'declared_total_U_upper':W,'total_bound_margin':gap}

def stratum(case,fixture,permutation,finite,balanced):
    parent=case['parent'];require(parent==fixture['parent'],'same original stratum')
    rays,rows,contacts,ms=geometry(case,permutation)
    require([enc(r) for r in rays]==balanced['actual_tangent_rays'],'same original receiving-balanced rays')
    amax=F(fixture['ray_norm_upper']);require(0<amax<=1,'positive stated ray norm upper')
    for ray in rays:nonneg(Q(amax*amax)-dot(ray,ray),'actual ray norm bound, unit endpoint equality allowed')
    difference=sub(rays[1],rays[0]);q=dot(difference,difference);pos(q,'distinct actual normalized rays')
    parameter=-dot(rays[0],difference)/q
    candidates=[dot(a,a) for a in rays]
    if M.sg(parameter)>=0 and M.sg(1-parameter)>=0:
        vector=add(rays[0],scale(parameter,difference));candidates.append(dot(vector,vector))
    for value in candidates:gate(value-AMIN*AMIN,'ALL convex ray interpolants have norm above7/10')
    duals=[moments(k,sorted(fixture['coordinate_duals'],key=lambda r:r['coordinate'])[k],
                   rays,rows,contacts,ms,balanced,finite) for k in range(2)]
    firstW=fixture['initial_U_upper'];refinedW=fixture['refined_U_upper']
    require(type(firstW) is int and type(refinedW) is int and firstW>0 and refinedW>0,'positive integer strip bounds')
    initial=directed_bound(duals,L0,BETA0,CC0,firstW,f'parent{parent} initial')
    L=F(fixture['motion_sum_ratio']);require(L>0,'positive improved motion sum bound')
    front=KF*amax/AMIN*CR*(1+L0*D+L0*L0*D*D)
    factor=KF*(amax+amax*amax/AMIN)
    bootstrap_gaps={'denominator':1-factor*firstW*D*D/2,
                    'sum_ratio':L*(1-factor*firstW*D*D/2)-front}
    for name,gap in bootstrap_gaps.items():gate(gap,f'parent{parent} UNCONDITIONAL bootstrap '+name)
    bounds=fixture['refined_common_bounds']
    require(set(bounds)=={'ownC','pairC','ownrho','pairrho'} and
            all(type(x) is int and x>0 for x in bounds.values()),'all four fresh common bounds')
    ownC,cc,ownrho,beta=[bounds[k] for k in ['ownC','pairC','ownrho','pairrho']]
    error=12+F(23,10)*L
    normal_gaps={
        'own_translation':ownC*(1-9*MU*D)-F(3,2)*MU*error,
        'same_physical_translation_pair':cc-ownC*(1+100*D*D),
        'own_axial':ownrho-MR*(error+6*ownC*D),
        'both_inverse_axial_directions':beta-DMAX*(ownrho+CR),
    }
    for name,gap in normal_gaps.items():gate(gap,f'parent{parent} fresh common bound '+name)
    refined=directed_bound(duals,L,beta,cc,refinedW,f'parent{parent} refined')
    lower,upper=map(F,fixture['receiving_corner_interval'])
    require(0<lower<upper,'positive whole receiving-stress corner interval')
    corners=[list(decode(row)) for row in balanced['critical_bilinear_corners']]
    losses=[list(decode(row)) for row in balanced['receiving_bilinear_corner_loss_bounds']]
    for i in range(2):
        for j in range(2):
            gate(corners[i][j]-losses[i][j]-lower,'fresh actual receiving-stress lower corner')
            gate(upper-corners[i][j]-losses[i][j],'fresh actual receiving-stress upper corner')
    alpha=KF*amax;positive_ratio=(1+amax*refinedW*D*D)/AMIN
    positive_gap=gate(1/alpha-refinedW*D*D,'both positive source-coordinate sums survive')
    signedlower=lower*(1/(alpha*alpha)-refinedW*D*D/alpha)-upper*positive_ratio*refinedW*D*D
    axialupper=F(101,100)*(beta*D)**2
    finalgap=gate(signedlower-axialupper,f'parent{parent} strict all-signed final bilinear contradiction')
    uniformgap=gate(finalgap-F(1,100),'uniform final contradiction coefficient above1/100')
    return {'parent':parent,'actual_tangent_rays':rays,'actual_receiver_rays':[decode(r) for r in finite['receiver_rays']],
            'convex_interpolant_minimum_candidates':candidates,'ray_norm_upper':amax,'interpolant_norm_lower':AMIN,
            'two_augmented_coordinate_duals':duals,'initial':initial,'unconditional_motion_sum_ratio':L,
            'bootstrap_gaps':bootstrap_gaps,'refined_common_bounds':bounds,'fresh_normal_gaps':normal_gaps,
            'refined':refined,'actual_receiving_corner_interval':[lower,upper],
            'positive_part_ratio_upper':positive_ratio,'positive_part_gap':positive_gap,
            'signed_bilinear_lower':signedlower,'axial_bilinear_upper':axialupper,'strict_contradiction_gap':finalgap,
            'uniform_contradiction_coefficient_margin_above1_over100':uniformgap}

def malformed(data,old,permutation,finite,balanced,records):
    missing=copy.deepcopy(data);missing['cases'].pop()
    missingcoord=copy.deepcopy(data);missingcoord['cases'][0]['coordinate_duals'].pop()
    base=next(c for c in data['cases'] if c['parent']==28)
    negative=copy.deepcopy(base);negative['coordinate_duals'][0]['coefficients'][0]=['-1','0']
    duplicate=copy.deepcopy(base);duplicate['coordinate_duals'][0]['basis']=[7,7,11,12]
    unrepaired=copy.deepcopy(base);unrepaired['coordinate_duals'][0]['common_stress_multiplier']=0
    smallW=copy.deepcopy(base);smallW['initial_U_upper']=1
    smallL=copy.deepcopy(base);smallL['motion_sum_ratio']='1/10'
    falsecorner=copy.deepcopy(base);falsecorner['receiving_corner_interval']=['1','2']
    attempts=[lambda:coverage(missing),lambda:coverage(missingcoord)]
    for item in [negative,duplicate,unrepaired,smallW,smallL,falsecorner]:
        attempts.append(lambda item=item:stratum(old[28],item,permutation,finite[28],balanced[28]))
    r=next(r for r in records if r['parent']==28)['two_augmented_coordinate_duals'][0]
    attempts.append(lambda:SIGNED.ALG.identities(M,MV,r['original_contacts'],r['coefficients'],
                    r['mass'],r['b'],r['S'],r['B'],r['K'],wrong_sign=True))
    for test in attempts:
        try:test()
        except (ValueError,KeyError,IndexError,TypeError,ZeroDivisionError):continue
        raise ValueError('Malformed whole-cap certificate accepted')
    return len(attempts)

def check(self_test):
    # Replay before adding ANY new registered signs; its full expected count is fixed.
    inherited=SIGNED.check(True);data_bytes=(json.dumps(inherited,indent=1)+'\n').encode()
    require(data_bytes==(REPO/deps[0]['source_directory']/'expected.json').read_bytes(),'EVERY complete signed-sector parent expected byte')
    old={r['parent']:r for r in json.loads((REPO/'convex_geometry/rupert_j77_uniform_local_exclusion/certificates.json').read_text())['cases']}
    finite={r['parent']:r for r in json.loads((REPO/'convex_geometry/rupert_j77_effective_mirror_cap/expected.json').read_text())['stratum_records']}
    balanced={r['parent']:r for r in json.loads((REPO/'convex_geometry/rupert_j77_receiving_balanced_stress/expected.json').read_text())['stratum_records']}
    index={v:i for i,v in enumerate(V)};permutation=[index[M.rotate(v)] for v in V]
    data=json.loads((HERE/'certificates.json').read_text());coverage(data)
    initial=group_and_initial_gates()
    records=[stratum(old[c['parent']],c,permutation,finite[c['parent']],balanced[c['parent']]) for c in data['cases']]
    negative=malformed(data,old,permutation,finite,balanced,records) if self_test else 0
    for pair,sign in tuple(M.area.SIGNS.items()):
        require(M.area.interval_sign(pair)==sign,'independent rational positive-sqrt5 sign enclosure')
    return enc({'agent':'six-rupert-2','role':'researcher','target':'original55unit-edge asymmetric J77',
        'proof_status':'author-checked exact finite hypotheses and universal original-contact identities plus unformalized continuous directed-negative-part proof',
        'physical_receiver_chord_radius':'1/1000','closed_receiving_sectors':sorted(PARENTS),
        'all_original_proper_Q_full_roll_translation_lambda_ge1':True,
        'whole_1_1000_mirror_cap_strict_passage_excluded':True,'global_J77_Rupert_resolved':False,
        'independent_review_asserted':False,
        'closed_classification':'lambda1,t0,Qh=I or M_nM_q, actual RIGHT C5 body factor, nearest signed mirror axis',
        'two_motion_same_gauge_prerequisites':initial,'stratum_records':records,'malformed_controls':negative,
        'fixture_sha256':M.digest(data),'complete_signed_sector_parent_expected_bytes':len(data_bytes),
        'complete_signed_sector_parent_expected_sha256':sha256(data_bytes).hexdigest(),
        'distinct_registered_independent_sign_enclosures_including_prerequisites':len(M.area.SIGNS),
        'remaining_frontier':'global receiving complement, larger complete physical caps and global J77 decision remain OPEN'})

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--self-test',action='store_true')
    a=ap.parse_args();out=(json.dumps(check(a.self_test),indent=1)+'\n').encode()
    require(out==(HERE/'expected.json').read_bytes(),'EVERY expected output byte; invoke with --self-test')
    print(out.decode(),end='')
