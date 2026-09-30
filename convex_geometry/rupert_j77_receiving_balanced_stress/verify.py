"""Exact finite hypotheses for a receiving-balanced J77 mirror reduction.

Author six-rupert-2, researcher. Python3.11+, standard library, Q(sqrt5).
The whole1/1000cap has a necessary bilinear reduction, NOT a passage decision.
The continuous matrix, projection and stress arguments are in PROOF.md.
"""
import argparse
import copy
import importlib.util
import json
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    out = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(out)
    return out

deps = json.loads((HERE/'dependencies.json').read_text())
require(len(deps) == 1 and deps[0]['source_directory'] ==
        'convex_geometry/rupert_j77_bilinear_mirror_cap' and
        deps[0]['source_commit'] == 'f7c01b343c4eb0141d0eefd3e794cb4394087795',
        'one declared bilinear finite-input parent')
require(set(deps[0]['sha256']) == {'.gitignore','README.md','PROOF.md','verify.py',
        'multivariate.py','certificates.json','dependencies.json','expected.json'},
        'all eight direct parent files pinned')
for name, digest in deps[0]['sha256'].items():
    require(sha256((REPO/deps[0]['source_directory']/name).read_bytes()).hexdigest() == digest,
            'changed direct finite source input: '+name)
BIL = module('j77_receiving_balanced_input',REPO/deps[0]['source_directory']/'verify.py')
M, MV, Q, V = BIL.M, BIL.MV, BIL.Q, BIL.V
dot, cross, add, sub, scale = M.dot, M.cross, M.add, M.sub, M.scale
pos, nonneg, absq, norm1, enc, decode = M.pos, M.nonneg, M.absq, M.norm1, M.enc, M.decode
CAP, CR = F(1,1000), F(1001,1000)

def matmul(a,b):
    return [[dot(row,col) for col in zip(*b)] for row in a]

def matrix_inverse(a):
    require(len(a) == 4 and all(len(row) == 4 for row in a), 'four exact balance coordinates')
    columns = [M.P.solve(a,[Q(int(i==j)) for i in range(4)]) for j in range(4)]
    result = [list(row) for row in zip(*columns)]
    require(matmul(a,result) == [[Q(int(i==j)) for j in range(4)] for i in range(4)],
            'exact balance inverse product')
    require(matmul(result,a) == [[Q(int(i==j)) for j in range(4)] for i in range(4)],
            'exact balance reverse inverse product')
    return result

def coverage(data):
    require(data['agent'] == 'six-rupert-2' and data['role'] == 'researcher', 'actual author and role')
    require(type(data['receiver_cap_denominator']) is int and data['receiver_cap_denominator'] == 1000,
            'whole stated physical cap')
    ids = [c['parent'] for c in data['cases']]
    require(len(ids) == len(set(ids)) == 7 and set(ids) == {21,23,28,30,31,32,33},
            'all seven closed receiving strata')

def universal_factorization(wrong_axial_sign=False):
    """Nine independent variables, no evaluation or point sampling.

    Ssym has trace1. The axial balance is encoded by
    S=Ssym+(B.r/2)J, where J(y,z)=(-z,y).
    """
    R = MV.Ring(Q,9)
    zero, one = R.zero, R.one
    ry,rz,rho,py,pz,x,y,by,bz = [R.variable(i) for i in range(9)]
    r,p,bv = (ry,rz),(py,pz),(by,bz)
    w,w0 = (rho,py,pz),(R.neg(rz),ry)
    t = R.scale(F(1,2),R.dot(bv,r))
    ss = [[x,y],[y,R.subtract(one,x)]]
    S = [[x,R.subtract(y,t)],[R.add(y,t),R.subtract(one,x)]]
    h = R.add(one,R.dot(bv,w0))
    A = [[R.add(h if i==j else zero,R.neg(ss[i][j]),
          R.scale(F(-1,2),R.add(R.multiply(bv[i],w0[j]),R.multiply(w0[i],bv[j]))))
          for j in range(2)] for i in range(2)]
    sr = [R.dot(row,r) for row in S]
    g = (R.neg(sr[1]),sr[0])
    # Direct moment expansion: G.w + w^T(sum omega v m(u)^T)w - h||w||^2.
    actual = R.add(R.dot(g,p),R.neg(R.multiply(rho,R.dot(p,sr))),
        *(R.multiply(R.multiply(p[i],S[i][j]),p[j]) for i in range(2) for j in range(2)),
        R.multiply(R.dot(p,bv),R.dot(w0,p)),R.neg(R.multiply(R.dot(w,w),h)))
    Nt = [R.add(w0[i],R.neg(p[i]),R.multiply(rho,r[i])) for i in range(2)]
    Nx = R.add(rho,R.dot(r,p))
    axial = R.multiply(R.multiply(h,rho),Nx)
    expected = R.add(*(R.multiply(R.multiply(p[i],A[i][j]),Nt[j])
                    for i in range(2) for j in range(2)),
                    axial if wrong_axial_sign else R.neg(axial))
    require(actual == expected,'universal receiving-balanced stress factorization')
    return {'independent_variables':9,'nonzero_monomials':len(actual),
            'total_degree':max(map(sum,actual)),'polynomial_sha256':M.digest(R.terms(actual))}

def quantitative_gates():
    d,cr = CAP,CR
    mu,mr = F(807,100),F(374,100)
    # First use the full all-source Cayley bound. Then, only under BOTH
    # exact critical-cone hypotheses, improve the motion bound and repeat.
    # Every constant is recomputed on1/1000, not copied from the old1e-5 proof.
    gates = {
        'physical_chord_to_raw_chart':cr*(1-d*d/2)-1,
        'whole_receiving_parent_covered':F(1,4)-4*d,
        'mirror_axis_angle_ratio':1-F(1,2000)**2-F(1000,1001)**2,
        'both_full_angles_below_18_delta':18-(15+2*cr),
        'both_Cayley_norms_below_10_delta':10*(1-81*d*d/2)-9,
        'positive_reflected_denominator':1-10*cr*d*d,
        'common_quadratic_remainder_below_23_10':F(23,10)-F(9,4)*(1+6*d),
        'whole_cap_common_translation_absorption':1-9*mu*d,
        'initial_own_C_below_458_delta_eta':458*(1-9*mu*d)-F(3,2)*mu*35,
        'initial_pair_C_below_459_delta_min_eta':459-458*(1+100*d*d),
        'initial_own_rho_below_142_delta_eta':142-mr*(35+6*458*d),
        'initial_pair_rho_below_144_delta_min_eta':144-(1+10*cr*d*d)*(142+cr),
        'initial_tangent_norm_controls_Cayley_by_51_50':F(51,50)**2*(1-(144*d)**2)-1,
        'both_exact_cones_imply_Cayley_sum_below_21_10_delta':
             F(21,10)-2*F(51,50)*cr*(1+10*d+100*d*d),
        'conditional_common_contact_error_below_17_delta_eta':17-(12+F(23,10)*F(21,10)),
        'conditional_own_C_below_223_delta_eta':223*(1-9*mu*d)-F(3,2)*mu*17,
        'conditional_pair_C_below_224_delta_min_eta':224-223*(1+100*d*d),
        'conditional_own_rho_below_69_delta_eta':69-mr*(17+6*223*d),
        'conditional_pair_rho_below_71_delta_min_eta':71-(1+10*cr*d*d)*(69+cr),
        'conditional_bilinear_strict_contradiction':
             F(1,100)*(1-(71*d)**2)-F(101,100)*(71*d)**2
    }
    for name,gap in gates.items():
        pos(Q(gap),'strict whole-cap rational gate: '+name)
    return gates

def geometry(case, permutation):
    contacts = [(permutation[b],permutation[a],permutation[j]) for a,b,j in case['contacts']]
    rays = []
    for a in case['extreme_motions']:
        a = M.rotate(decode(a)[:3])
        rays.append(scale(1/norm1(a),a))
    require(len(rays)==2 and all(a[0]==0 for a in rays) and M.det2(*rays)!=0,
            'original independent normalized tangent motion rays')
    common = case['common_indices']
    require(len(contacts)==32 and len(common)==len(set(common))==6,
            'all parent contacts and six distinct persistent mirror-fixed preimages')
    mm,vv,kk,gx = [],[],[],[]
    ey,ez = (Q(),Q(1),Q()),(Q(),Q(),Q(1))
    for i in common:
        a,b,j = contacts[i]
        edge = sub(V[b],V[a]);v = V[j]
        h = dot(cross(edge,M.E),v);pos(h,'positive original critical support offset')
        m = scale(1/h,cross(edge,M.E));k = edge[0]/h
        require(v[0]==0 and m[0]==0 and dot(v,m)==1,
                'mirror-fixed original source and normalized critical contact')
        require(cross(v,m)[1:] == (Q(),Q()),'common critical tangent torque vanishes')
        for dr in (ey,ez):
            actual = scale(1/h,cross(edge,dr))
            expect = add(scale(-dot(m,dr),M.E),scale(k,cross(M.E,dr)))
            require(actual==expect,'entire affine receiving-normal formula from original edge')
            require(cross(v,actual)[0] == k*dot(v,dr),'entire axial receiving-torque formula')
        mm.append(m);vv.append(v);kk.append(k);gx.append(cross(v,m)[0])
    balance = [[Q(1)]*6,gx,[m[1] for m in mm],[m[2] for m in mm]]
    return contacts,common,rays,mm,vv,kk,balance

def critical_corner(a,b,v,m):
    return dot(a,b)-(dot(a,v)*dot(m,b)+dot(b,v)*dot(m,a))/2

def receiving_corner(a,b,v,k,dr):
    jdr = cross(M.E,dr)
    return k*(dot(v,jdr)*dot(a,b)-(dot(a,v)*dot(jdr,b)+dot(a,jdr)*dot(v,b))/2)

def stratum(case, fixture, parent, permutation):
    require(fixture['input_common_weights']==parent['input_common_weights'],
            'identical positive critical weights from byte-pinned finite input')
    ww = decode(fixture['input_common_weights'])
    contacts,common,rays,mm,vv,kk,balance = geometry(case,permutation)
    require(len(ww)==6 and all(dot(row,ww)==int(j==0) for j,row in enumerate(balance)),
            'normalized full four-coordinate critical balance')
    for w in ww:
        nonneg(w-Q(F(1,20)),'positive critical common weight floor')
    ids = fixture['balance_basis']
    require(len(ids)==len(set(ids))==4 and all(type(i) is int and 0<=i<6 for i in ids),
            'four distinct original common balance columns')
    H0 = [[row[i] for i in ids] for row in balance]
    inv = matrix_inverse(H0)
    B = [sum((w*k*v[j] for w,k,v in zip(ww,kk,vv)),Q()) for j in (1,2)]
    K = dot(ww,kk)
    Hy = [[Q()]*6,[k*v[1] for k,v in zip(kk,vv)],[Q()]*6,kk]
    Hz = [[Q()]*6,[k*v[2] for k,v in zip(kk,vv)],[-k for k in kk],[Q()]*6]
    rhs = [[Q(),Q()],[-B[0],-B[1]],[Q(),K],[-K,Q()]]
    Ay = matmul(inv,[[row[i] for i in ids] for row in Hy])
    Az = matmul(inv,[[row[i] for i in ids] for row in Hz])
    br = matmul(inv,rhs)
    qr = [sum((absq(y)+absq(z) for y,z in zip(ry,rz)),Q()) for ry,rz in zip(Ay,Az)]
    bb = [norm1(row) for row in br]
    q = max(qr);radius=Q(CR*CAP)
    pos(1-q*radius,'uniform invertibility on the entire raw receiving ball')
    tmax = max(bb)*radius/(1-q*radius)
    ts = [Q()]*6
    for i,b,qi in zip(ids,bb,qr):
        ts[i] = b*radius+qi*radius*tmax
    lower = [w-t for w,t in zip(ww,ts)]
    for w in lower:
        pos(w-Q(F(1,25)),'every receiving-dependent weight exceeds1/25 on the whole cap')
    S = [[sum((w*v[i+1]*m[j+1] for w,v,m in zip(ww,vv,mm)),Q()) for j in range(2)] for i in range(2)]
    require(S[0][1]==S[1][0] and S[0][0]+S[1][1]==1,
            'critical symmetric trace-one stress')
    ey,ez=(Q(),Q(1),Q()),(Q(),Q(),Q(1))
    pairs,losses,lowers = [],[],[]
    for a in rays:
        pp,ll,lo = [],[],[]
        for b in rays:
            critical = [critical_corner(a,b,v,m) for v,m in zip(vv,mm)]
            base = dot(ww,critical)
            # sum of the four corrected weights is zero, so a center may be subtracted.
            middle = (max(critical[i] for i in ids)+min(critical[i] for i in ids))/2
            weightloss = sum((ts[i]*absq(critical[i]-middle) for i in ids),Q())
            ly = [receiving_corner(a,b,v,k,ey) for v,k in zip(vv,kk)]
            lz = [receiving_corner(a,b,v,k,ez) for v,k in zip(vv,kk)]
            receivingloss = radius*(absq(dot(ww,ly))+absq(dot(ww,lz)))
            receivingloss += radius*sum((t*(absq(y)+absq(z)) for t,y,z in zip(ts,ly,lz)),Q())
            loss = weightloss+receivingloss
            pos(base-loss-Q(F(1,100)),'every actual receiving-stress ray pairing exceeds1/100')
            pp.append(base);ll.append(loss);lo.append(base-loss)
        pairs.append(pp);losses.append(ll);lowers.append(lo)
    Bbound = norm1(B)+sum((t*absq(k)*norm1(v[1:]) for t,k,v in zip(ts,kk,vv)),Q())
    hlo,hhi = 1-radius*Bbound,1+radius*Bbound
    pos(hlo-Q(F(99,100)),'actual receiving stress height greater than99/100')
    pos(Q(F(101,100))-hhi,'actual receiving stress height less than101/100')
    return {'parent':case['parent'],'common_original_contacts':[contacts[i] for i in common],
            'actual_tangent_rays':rays,'critical_weights':ww,'balance_basis':ids,
            'critical_balance_matrix':balance,'critical_balance_inverse':inv,
            'inverse_matrix_y':Ay,'inverse_matrix_z':Az,'inverse_right_hand_side':br,
            'row_Neumann_constants':qr,'row_rhs_constants':bb,'uniform_Neumann_gap':1-q*radius,
            'corrected_weight_change_bounds':ts,'receiving_weight_lower_bounds':lower,
            'critical_stress_S':S,'critical_stress_B':B,'critical_stress_K':K,
            'critical_bilinear_corners':pairs,'receiving_bilinear_corner_loss_bounds':losses,
            'receiving_bilinear_corner_lower_bounds':lowers,
            'receiving_stress_height_lower_bound':hlo,'receiving_stress_height_upper_bound':hhi,
            'data_identity_sha256':M.digest([contacts,common,rays,mm,vv,kk,balance,inv])}

def malformed(data, old, parents, permutation):
    attempts=[]
    bad=copy.deepcopy(data);bad['cases'].pop();attempts.append(lambda:coverage(bad))
    badcap=copy.deepcopy(data);badcap['receiver_cap_denominator']=100
    attempts.append(lambda:coverage(badcap))
    dup=copy.deepcopy(data['cases'][0]);dup['balance_basis']=[0,0,1,2]
    attempts.append(lambda:stratum(old[dup['parent']],dup,parents[dup['parent']],permutation))
    changed=copy.deepcopy(data['cases'][0]);changed['input_common_weights'][0]=[0,0]
    attempts.append(lambda:stratum(old[changed['parent']],changed,parents[changed['parent']],permutation))
    attempts.append(lambda:universal_factorization(wrong_axial_sign=True))
    for fail in attempts:
        try:
            fail()
        except (ValueError,KeyError,IndexError,TypeError,ZeroDivisionError):
            continue
        raise ValueError('malformed proof data or axial algebra accepted')
    return len(attempts)

def check(self_test):
    inherited = BIL.check(True)
    b = (json.dumps(inherited,indent=1)+'\n').encode()
    require(b==(REPO/deps[0]['source_directory']/'expected.json').read_bytes(),
            'EVERY complete bilinear-parent expected byte')
    old = json.loads((REPO/'convex_geometry/rupert_j77_uniform_local_exclusion/certificates.json').read_text())
    old = {c['parent']:c for c in old['cases']}
    parents = json.loads((REPO/deps[0]['source_directory']/'certificates.json').read_text())
    parents = {c['parent']:c for c in parents['cases']}
    index={v:i for i,v in enumerate(V)}
    permutation=[index[M.rotate(v)] for v in V]
    data=json.loads((HERE/'certificates.json').read_text());coverage(data)
    rational=quantitative_gates()
    universal=universal_factorization()
    records=[stratum(old[c['parent']],c,parents[c['parent']],permutation) for c in data['cases']]
    bad=malformed(data,old,parents,permutation) if self_test else 0
    for pair,sign in tuple(M.area.SIGNS.items()):
        require(M.area.interval_sign(pair)==sign,'independent rational positive-sqrt5 sign enclosure')
    return enc({'agent':'six-rupert-2','role':'researcher',
        'proof_status':'author-checked finite hypotheses and universal identity plus written continuous proof; unformalized',
        'target':'J77 paragyrate diminished rhombicosidodecahedron','original_vertices':55,
        'complete_original_source_receiving_domain':'dist(n,{+/-R^j e})<=1/1000; every original proper Q, all t,lambda>=1',
        'new_conclusion':'necessary exact receiving-balanced bilinear inequality; not a passage decision',
        'receiving_stress_identity':'sum omega F_i=D[p^T A(u) ptilde-h(u) rho rhotilde]',
        'receiving_weight_floor_strict':'1/25','all_four_actual_ray_pairings_strictly_greater_than':'1/100',
        'receiving_stress_height_in_open_interval':['99/100','101/100'],
        'global_Rupert_resolved':False,'whole_1_1000_cap_excluded':False,'independent_review_asserted':False,
        'conditional_whole_cap_conclusion':'if BOTH tangent motions have nonnegative exact critical-cone coordinates, closed containment forceslambda1,t0,Qh=I or M_n M_p',
        'necessary_non_equality_frontier':'every other closed containment on the whole cap has a negative coefficient in at least one of the two tangent motions',
        'translation_and_axial_linear_stress_cancelled':True,'closed_strata':len(records),
        'positive_receiving_weights':42,'strict_bilinear_corner_bounds':28,
        'universal_stress_identity':universal,'whole_cap_rational_gates':rational,'stratum_records':records,
        'malformed_controls_with_self_test':bad,'fixture_sha256':M.digest(data),
        'whole_bilinear_parent_expected_bytes':len(b),'whole_bilinear_parent_expected_sha256':sha256(b).hexdigest(),
        'direct_pinned_input_files':8,'transitive_pinned_input_files':56,
        'distinct_independent_sign_enclosures_including_parents':len(M.area.SIGNS),
        'remaining_obstruction':'actual signed tangent coordinates need finite control; positive critical-ray corners alone do not decide containment'})

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    out=(json.dumps(check(args.self_test),indent=1)+'\n').encode()
    require(out==(HERE/'expected.json').read_bytes(),'EVERY expected output byte; invoke with --self-test')
    print(out.decode(),end='')
