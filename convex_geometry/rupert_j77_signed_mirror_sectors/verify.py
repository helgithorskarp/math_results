"""Exact finite hypotheses for J77's two full-radius closed mirror sectors.

Author six-rupert-2, researcher. Python3.11+, stdlib, Q(sqrt5).
The continuous signed-coordinate argument is in PROOF.md.
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
require(len(deps)==1 and deps[0]['source_directory']=='convex_geometry/rupert_j77_receiving_balanced_stress'
        and deps[0]['source_commit']=='41ad5faf8d88b8c5a30358023e0c47168551da96','one declared receiving-balanced parent')
require(set(deps[0]['sha256'])=={'.gitignore','README.md','PROOF.md','verify.py','certificates.json','dependencies.json','expected.json'},
        'all seven direct parent files pinned')
for name,digest in deps[0]['sha256'].items():
    require(sha256((REPO/deps[0]['source_directory']/name).read_bytes()).hexdigest()==digest,'changed direct input: '+name)
PB=module('j77_signed_sectors_balanced_input',REPO/deps[0]['source_directory']/'verify.py')
M,MV,Q,V=PB.M,PB.MV,PB.Q,PB.V
ALG=module('j77_signed_sectors_algebra',HERE/'algebra.py')
dot,cross,add,sub,scale=M.dot,M.cross,M.add,M.sub,M.scale
pos,nonneg,absq,norm1,decode,enc=M.pos,M.nonneg,M.absq,M.norm1,M.decode,M.enc
D=F(1,1000);CR=F(1001,1000);DMAX=1+10*CR*D*D
AMIN=F(7,10);AMAX=F(39,50);KF=F(51,50)


def coverage(data):
    require(data['agent']=='six-rupert-2' and data['role']=='researcher','actual author and role')
    require(type(data['receiver_cap_denominator']) is int and data['receiver_cap_denominator']==1000,
            'whole stated physical radius')
    require(len(data['cases'])==2 and {c['parent'] for c in data['cases']}=={30,31},'both closed sectors, no other sector claimed')
    for c in data['cases']:
        require(len(c['cone_duals'])==2 and {r['coordinate'] for r in c['cone_duals']}=={0,1},'both coordinate inequalities')


def mdot(a,H,b):
    return sum((a[i]*H[i][j]*b[j] for i in range(2) for j in range(2)),Q())


def dual_geometry(case,fixture,permutation,rays):
    k=fixture['coordinate'];ids=fixture['basis'];cs=decode(fixture['coefficients'])
    require(len(ids)==len(cs)==4 and len(set(ids))==4 and all(type(i) is int and 0<=i<32 for i in ids),
            'four distinct actual original contact rows')
    for c in cs:
        nonneg(c,'nonnegative original-contact combination')
    contacts=[(permutation[b],permutation[a],permutation[j]) for a,b,j in case['contacts']]
    selected=[contacts[i] for i in ids];vv=[V[t[2]] for t in selected];mm=[];kk=[];gg=[]
    for a,b,j in selected:
        edge=sub(V[b],V[a]);h=dot(cross(edge,M.E),V[j]);pos(h,'positive critical support offset')
        m=scale(1/h,cross(edge,M.E));ki=edge[0]/h
        require(m[0]==0 and dot(m,V[a])==dot(m,V[b])==dot(m,V[j])==1,'original normalized contact')
        for dr in [(Q(),Q(1),Q()),(Q(),Q(),Q(1))]:
            require(scale(1/h,cross(edge,dr))==add(scale(-dot(m,dr),M.E),scale(ki,cross(M.E,dr))),
                    'full affine original-edge normal, including noncommon contacts')
        mm.append(m);kk.append(ki);gg.append(cross(V[j],m))
    rows=[[g[0],dot(g,rays[0]),dot(g,rays[1]),m[1],m[2]] for g,m in zip(gg,mm)]
    require(all(sum((c*row[j] for c,row in zip(cs,rows)),Q())==-int(j==k+1) for j in range(5)),
            'full five-coordinate negative-coefficient dual identity')
    c0=sum(cs,Q())
    b=[sum((c*v[0]*m[j+1] for c,v,m in zip(cs,vv,mm)),Q()) for j in range(2)]
    S=[[sum((c*v[i+1]*m[j+1] for c,v,m in zip(cs,vv,mm)),Q()) for j in range(2)] for i in range(2)]
    B=tuple(sum((c*ki*v[j] for c,ki,v in zip(cs,kk,vv)),Q()) for j in range(3))
    K=sum((c*ki for c,ki in zip(cs,kk)),Q())
    require(S[0][1]==S[1][0] and S[0][0]+S[1][1]==c0,'symmetric critical tangent moment with trace c0')
    require(all(dot((Q(),-b[1],b[0]),a)==-int(i==k) for i,a in enumerate(rays)),
            'actual negative-coordinate covector equals Jb')
    pos(3-norm1(b),'both coordinate covector norms below3')
    pos((7 if k==0 else 15)-c0,'critical mass upper bound')
    pos((8 if k==0 else 12)-norm1(B[1:]),'tangent receiving moment upper bound')
    if k==0:pos(2-absq(K),'first receiving translation moment below2')
    else:require(K==0,'second receiving translation moment exactly zero')
    J=[[Q(),Q(-1)],[Q(1),Q()]]
    H=[[c0*int(i==j)-S[i][j]+B[0]*J[i][j] for j in range(2)] for i in range(2)]
    corners=[[mdot(a[1:],H,bb[1:]) for bb in rays] for a in rays]
    stated=[[[Q(0,F(3,5)),Q(-3,1)],[Q(3,-1),Q()]],
            [[Q(),Q(0,F(1,5))],[Q(0,F(-1,5)),Q(F(-1,2),F(3,2))]]][k]
    require(corners==stated,'entire exact signed corner matrix stated in the proof')
    require(corners[1-k][1-k]==0,'opposite diagonal exactly zero')
    nonneg(corners[1-k][k],'favorable one-sided opposite row')
    nonneg(1-corners[1-k][k],'opposite off-diagonal at most1')
    identity=ALG.identities(M,MV,selected,cs,c0,b,S,B,K)
    return {'coordinate':k,'basis':ids,'original_contacts':selected,'coefficients':cs,
            'c0':c0,'b':b,'coordinate_covector_l1':norm1(b),'S':S,'B':B,'K':K,'bilinear_matrix':H,'bilinear_corners':corners,
            'universal_original_contact_identity':identity}


def quantitative_gates():
    d,cr,dm=D,CR,DMAX
    chi=F(3)
    def error(L,beta,cc,c0,bn,kn):
        return (chi+bn)*(dm*L*L+beta*cr*L*L*d*d)+chi*beta*L+bn*beta*cr \
            +bn*beta*beta*cr*L*d*d+c0*dm*beta*beta*L*d+kn*cr*cc+chi*chi*beta*cr*L*d
    e1=[error(F(10),144,459,7,8,2),error(F(10),144,459,15,12,0)]
    e2=[error(F(6,5),63,197,7,8,2),error(F(6,5),63,197,15,12,0)]
    mu,mr=F(807,100),F(374,100)
    bootfront=KF*AMAX/AMIN*cr*(1+10*d+100*d*d)
    bootfactor=KF*(AMAX+AMAX*AMAX/AMIN)
    rayfactor=KF*AMAX
    signedlower=F(1,100)*(1/(rayfactor*rayfactor)-4700*d*d/rayfactor)-F(7,50)*6*4700*d*d
    gates={
        'strict_interpolant_from_same_orthant':1-2*AMIN*AMIN,
        'initial_coupling_absorption':1-12*dm*10*d,
        'first_error_below9000':9000-e1[0],'second_error_below10700':10700-e1[1],
        'first_four_negative_parts_below45000_delta_squared_min':45000*(1-12*dm*10*d)-2*sum(e1),
        'unconditional_Cayley_sum_below6_5_delta':F(6,5)*(1-bootfactor*45000*d*d/2)-bootfront,
        'fresh_common_error_below15_delta_eta':15-(12+F(23,10)*F(6,5)),
        'fresh_own_C_below196_delta_eta':196*(1-9*mu*d)-F(3,2)*mu*15,
        'fresh_pair_C_below197_delta_min':197-196*(1+100*d*d),
        'fresh_own_rho_below61_delta_eta':61-mr*(15+6*196*d),
        'fresh_pair_rho_below63_delta_min':63-dm*(61+cr),
        'refined_coupling_absorption':1-12*dm*F(6,5)*d,
        'refined_first_error_below1200':1200-e2[0],'refined_second_error_below1100':1100-e2[1],
        'refined_four_negative_parts_below4700_delta_squared_min':4700*(1-12*dm*F(6,5)*d)-2*sum(e2),
        'both_positive_parts_nonzero':1/rayfactor-4700*d*d,
        'final_strict_signed_bilinear_gap':signedlower-F(101,100)*(63*d)**2,
    }
    for name,gap in gates.items():pos(Q(gap),'strict full-radius signed-sector gate: '+name)
    return {'initial_negative_branch_errors':e1,'refined_negative_branch_errors':e2,
            'rational_gates':gates,'signed_bilinear_lower':signedlower,'axial_bilinear_upper':F(101,100)*(63*d)**2}


def stratum(case,fixture,permutation,finite,balanced):
    rays=[scale(1/norm1(M.rotate(decode(a)[:3])),M.rotate(decode(a)[:3])) for a in case['extreme_motions']]
    require(len(rays)==2 and M.det2(*rays)!=0,'two independent actual tangent rays')
    require(all(a[0]==0 and norm1(a)==1 for a in rays),'normalized actual tangent rays')
    for a in rays:
        nonneg(a[1],'same closed tangent orthant: y>=0');nonneg(-a[2],'same closed tangent orthant: z<=0')
        pos(Q(AMAX*AMAX)-dot(a,a),'each actual ray norm below39/50')
    duals=[dual_geometry(case,c,permutation,rays) for c in sorted(fixture['cone_duals'],key=lambda r:r['coordinate'])]
    cc=[r['bilinear_corners'] for r in duals]
    coupling=[]
    for k in range(2):
        t=sum(((absq(cc[k][k][j])+cc[1-k][k][j])*duals[j]['coordinate_covector_l1'] for j in range(2)),Q())
        pos(12-t,'total four-inequality coupling column below12')
        coupling.append(t)
    rr=finite['receiver_rays'];receivers=[decode(r) for r in rr]
    for dual in duals:
        for r in receivers:
            nonneg(-dot(dual['b'],r[1:]),'mirror Cayley vector has nonnegative critical coordinates on whole closed sector')
    require([enc(r) for r in rays]==balanced['actual_tangent_rays'],'same rays in actual receiving-balanced stress')
    for row,lossrow in zip(balanced['critical_bilinear_corners'],balanced['receiving_bilinear_corner_loss_bounds']):
        for value,loss in zip(row,lossrow):
            pos(Q(F(7,50))-Q(*value)-Q(*loss),'all actual receiving-stress corners below7/50')
    return {'parent':case['parent'],'actual_motion_rays':rays,'actual_receiver_rays':receivers,
            'two_coordinate_duals':duals,'coupling_column_constants':coupling,
            'receiving_stress_corner_interval':['1/100','7/50'],
            'closed_equality_classification':'lambda1,t0,Qh=I or M_nM_q; ALL actual signed coordinates covered'}


def malformed(data,old,permutation,finite,balanced,records):
    bad=copy.deepcopy(data);bad['cases'].pop()
    neg=copy.deepcopy(data['cases'][0]);neg['cone_duals'][0]['coefficients'][0]=['-1','0']
    wrong=copy.deepcopy(data['cases'][0]);wrong['cone_duals'][0]['coordinate']=1
    dup=copy.deepcopy(data['cases'][0]);dup['cone_duals'][0]['basis']=[6,6,10,13]
    attempts=[lambda:coverage(bad),lambda:stratum(old[30],neg,permutation,finite[30],balanced[30]),
              lambda:stratum(old[30],wrong,permutation,finite[30],balanced[30]),
              lambda:stratum(old[30],dup,permutation,finite[30],balanced[30])]
    r=next(r for r in records if r['parent']==30)['two_coordinate_duals'][0]
    attempts.append(lambda:ALG.identities(M,MV,r['original_contacts'],r['coefficients'],
                    r['c0'],r['b'],r['S'],r['B'],r['K'],wrong_sign=True))
    for f in attempts:
        try:f()
        except (ValueError,KeyError,IndexError,TypeError,ZeroDivisionError):continue
        raise ValueError('malformed signed-sector certificate accepted')
    return len(attempts)


def check(self_test):
    inherited=PB.check(True);b=(json.dumps(inherited,indent=1)+'\n').encode()
    require(b==(REPO/deps[0]['source_directory']/'expected.json').read_bytes(),'EVERY complete receiving-balanced parent expected byte')
    old={c['parent']:c for c in json.loads((REPO/'convex_geometry/rupert_j77_uniform_local_exclusion/certificates.json').read_text())['cases']}
    finite={c['parent']:c for c in json.loads((REPO/'convex_geometry/rupert_j77_effective_mirror_cap/expected.json').read_text())['stratum_records']}
    balanced={c['parent']:c for c in inherited['stratum_records']}
    index={v:i for i,v in enumerate(V)};permutation=[index[M.rotate(v)] for v in V]
    data=json.loads((HERE/'certificates.json').read_text());coverage(data)
    gates=quantitative_gates()
    records=[stratum(old[c['parent']],c,permutation,finite[c['parent']],balanced[c['parent']]) for c in data['cases']]
    by={r['parent']:r for r in records}
    require(by[30]['actual_motion_rays']==by[31]['actual_motion_rays'],'same critical tangent cone on both sectors')
    require(by[30]['actual_receiver_rays'][1]==by[31]['actual_receiver_rays'][0],'actual shared closed boundary')
    require(cross(M.E,by[30]['actual_receiver_rays'][0])==by[30]['actual_motion_rays'][1]
            and cross(M.E,by[31]['actual_receiver_rays'][1])==by[30]['actual_motion_rays'][0],
            'actual exterior receiving rays map to the two critical tangent rays')
    for r in by[30]['two_coordinate_duals']:
        pos(-dot(r['b'],by[30]['actual_receiver_rays'][1][1:]),'shared ray strictly inside tangent cone')
    negative=malformed(data,old,permutation,finite,balanced,records) if self_test else 0
    for pair,sign in tuple(M.area.SIGNS.items()):
        require(M.area.interval_sign(pair)==sign,'independent rational positive-sqrt5 sign enclosure')
    return enc({'agent':'six-rupert-2','role':'researcher','target':'original55vertex unit-edge J77',
        'proof_status':'author-checked exact finite hypotheses and universal original-contact identities plus unformalized continuous signed-coordinate proof',
        'physical_receiver_radius':'1/1000','closed_receiving_sectors':[30,31],
        'all_original_proper_Q_full_roll_t_lambda_ge1':True,
        'strict_passage_excluded_on_these_two_closed_sectors':True,
        'whole_1_1000_cap_excluded':False,'global_Rupert_resolved':False,'independent_review_asserted':False,
        'first_four_negative_parts_bound':'45000delta^2min(eta,etatilde)',
        'unconditional_Cayley_sum_bound':'6delta/5',
        'refined_pair_translation_and_axial_bounds':['197delta min','63delta min'],
        'refined_four_negative_parts_bound':'4700delta^2min(eta,etatilde)',
        'closed_classification':'lambda1,t0,Qh=I or M_nM_q with actual RIGHT C5body factor',
        'quantitative_bounds':gates,'stratum_records':records,'malformed_controls':negative,
        'fixture_sha256':M.digest(data),'whole_receiving_balanced_parent_expected_bytes':len(b),
        'whole_receiving_balanced_parent_expected_sha256':sha256(b).hexdigest(),
        'distinct_independent_sign_enclosures_including_prerequisites':len(M.area.SIGNS),
        'remaining_frontier':'other5closedsectors of1/1000cap and globalreceivingcomplement OPEN'})


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--self-test',action='store_true')
    a=ap.parse_args();out=(json.dumps(check(a.self_test),indent=1)+'\n').encode()
    require(out==(HERE/'expected.json').read_bytes(),'EVERY expected output byte; invoke with --self-test')
    print(out.decode(),end='')
