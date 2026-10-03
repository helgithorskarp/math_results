"""Exact chart, positive-normal, derivative-box and local-gate certificate.

Actual author six-tammes-2, researcher. Python3.11+, standard library.
This is same-author computational checking; ordinary proof is unformalized.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product,combinations
import argparse,hashlib,json,signal
import field as f
from interval import I,A,S
from exact import E
from frame import points

HERE=Path(__file__).resolve().parent
CORE=(0,1,2,4,5,6,7,8,9,10,11,12)
CASES=(('p3',(1,4,7)),('p13',(2,8,9)),('q',(8,9,11)),('p14',(0,3,6)),('c14',(3,4,6)))
CONTACTS=((0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),(2,4),(2,8),(2,10),(4,8),(5,7),(5,9),(5,11),(6,11),(7,12),(9,10),(9,11),(10,12))
FROZEN=('INPUT.json','PLAN.json','field.py','interval.py','exact.py','frame.py','check.py')
def require(ok,message):
    if not ok:raise ValueError(message)
def norm(v,H):return f.dot(v,f.matvec(H,v))
def cramer(rows,rhs):
    D=f.det(rows)
    U=tuple(f.det([[rhs[i] if j==k else rows[i][j] for j in range(3)] for i in range(3)]) for k in range(3))
    f.require(all(f.dot(rows[i],U)==f.mul(rhs[i],D) for i in range(3)),'homogeneous Cramer identities')
    return U,D
def divide(U,D):
    inverse=f.inverse(D)
    return tuple(f.mul(x,inverse) for x in U)
def absmax(v):return Q(max(abs(v.l),abs(v.h)),S)
def layout(data,plan):
    require(data['format']=='fixed-twelve-three-completion-v1','credited exact fixture format')
    require(data['core_labels']==list(CORE),'exact twelve retained labels')
    require(data['root_bracket']==['0.59260590292507377809642492233275','0.59260590292507377809642492233276'],'distinguished root')
    require(plan['format']=='twelve-core-local-gate-v1','complete target format')
    require(plan['fixed_reference_labels']==list(CORE) and plan['basis_old']==[0,5,11] and plan['basis_new']==[1,2,4],'exact reference and bases')
    require(plan['original_twenty_contacts']==[list(e) for e in CONTACTS],'literal original20 contact hypothesis')
    require(plan['z0_coefficients']==['-115/16','-4','215/8','-37/2','637/16'],'exact recovered chart polynomial')
    require(plan['unit_cases']==[{'name':n,'contact_labels':list(ls)} for n,ls in CASES],'all five original positive-normal cases')
    constants={'lambda_strict_lower':'2/15','lambda_sum_strict_upper':'17/10','normal_cube_squared_norm_strict_upper':'9',
       'coarse_point_distance_max':'21/1000','point_stability_constant':'600/13','sharp_three_stability_constant':'1400',
       'sharp_delta_max':'1/100000000','coefficient_derivative_l1_t_strict_upper':'15','coefficient_derivative_l1_z_strict_upper':'2',
       'physical_frame_lipschitz_t':'24','physical_frame_lipschitz_z':'3','subcritical_parameter_gate':'1/10000000000'}
    require(all(plan[k]==v for k,v in constants.items()),'exact advertised stability/derivative/gate constants')
    require(plan['no_actual_thirteenth_point'] is True and plan['all_three_added_points_arbitrary'] is True,'full arbitrary-three scope')
    require(plan['closed_parameter_box']['padding']=='1/1000000','chosen complete closed derivative rectangle')
    h=Q(1,10**6);lo,hi=map(Q,plan['z0_rational_bracket'])
    require(list(map(Q,plan['closed_parameter_box']['t']))==[f.LO-h,f.HI+h] and list(map(Q,plan['closed_parameter_box']['z']))==[lo-h,hi+h],'unmodified complete rectangle endpoints')
    require(lo<hi and hi-lo<Q(1,10**25),'compact exact chart bracket')
    return constants

def calibrate(data,plan):
    require(f.F==tuple(map(Q,(-1,-3,2,6,-1,13))),'exact quintic coefficients')
    require(f.evaluate(f.F,f.LO)<0<f.evaluate(f.F,f.HI) and f.interval(tuple(i*f.F[i] for i in range(1,6)))[0]>0,'root isolation and uniqueness in bracket')
    H=tuple(tuple(f.ONE if i==j else f.T for j in range(3)) for i in range(3))
    V=[tuple(f.readpoly(poly) for poly in row) for row in data['vectors']]
    require(len(V)==15 and all(len(v)==3 and norm(v,H)==f.ONE for v in V),'all fifteen exact unit references')
    contacts=[]
    for i,j in combinations(range(15),2):
        v=f.dot(V[i],f.matvec(H,V[j]))
        if v==f.T:contacts.append([i,j])
        else:require(f.interval(v)[1]<Q(17,40),'strict prior reference noncontacts')
    require(len(contacts)==30,'credited thirty-contact asymmetric reference')
    M=tuple(tuple(V[i][j] for i in (1,2,4)) for j in range(3));det=f.det(M)
    require(det==f.scalar(-1),'exact orientation-reversing change of basis')
    for i in range(3):
        for j in range(3):require(f.dot(tuple(M[k][i] for k in range(3)),f.matvec(H,tuple(M[k][j] for k in range(3))))==H[i][j],'exact changed anchor Gram matrix')
    B=[]
    for v in V:
        U,D=cramer(M,v);b=divide(U,D);require(f.matvec(M,b)==v,'all fifteen exact inverse mappings');B.append(b)
    for k,i in enumerate((1,2,4)):require(B[i]==tuple(f.ONE if j==k else f.ZERO for j in range(3)),'unit coordinate B anchors')
    product=f.dot(B[7],f.matvec(H,B[1]));den=f.sub(f.ONE,product)
    require(f.sign(den)>0,'nonpole chart denominator')
    z0=f.mul(f.det((B[7],B[12],B[1])),f.inverse(den))
    require(z0==f.readpoly(plan['z0_coefficients']),'exact chart recovery formula')
    zlo,zhi=map(Q,plan['z0_rational_bracket']);a,b=f.interval(z0)
    require(zlo<=a<=b<=zhi,'exact z0 root-polynomial enclosure in rational bracket')
    D=f.mul(f.mul(f.sub(f.ONE,f.T),f.sub(f.ONE,f.T)),f.add(f.ONE,f.scale(f.T,2)))
    q0=f.scale(f.mul(D,f.det((B[9],B[7],B[10]))),-1)
    require(f.sign(q0)>0,'positive radical orientation')
    E.positive_root=q0
    P,regularity=points(E(f.T,1,0),E(z0,0,1))
    for i in CORE:
        require(tuple(x.v for x in P[i])==B[i],'exact specialization of every original twelve-point vector')
    require(all(f.dot(B[i],f.matvec(H,B[j]))==f.T for i,j in CONTACTS),'exact original20 reference contacts')
    # The exact jet separately checks the positive-root square identity inside E.sqrt.
    require(all(f.sign(v)>0 for v in regularity.values()),'strict base chart/Gram/denominator/radical positivity')
    q=divide(*cramer([f.matvec(H,V[i]) for i in (8,9,11)],[f.T]*3))
    last=tuple(f.readpoly(poly) for poly in data['alternate_last'])
    require(norm(q,H)==f.ONE and norm(last,H)==f.ONE,'both alternative references exactly unit')
    units={'p3':V[3],'p13':V[13],'q':q,'p14':V[14],'c14':last}
    return H,V,B,z0,P,units

def normal_case(H,V,unit,labels,lambda_lower=Q(2,15),cube_norm_upper=Q(9)):
    neighbors=[V[i] for i in labels];columns=[[neighbors[j][i] for j in range(3)] for i in range(3)]
    weights=divide(*cramer(columns,unit))
    require(f.matvec(columns,weights)==unit,'exact positive contact-normal representation')
    require(all(f.sign(f.sub(w,f.scalar(lambda_lower)))>0 for w in weights),'all three weights above selected positive lower bound')
    require(f.sum_field(weights)==f.inverse(f.T),'exact contact-weight sum1/tau')
    require(f.sign(f.sub(f.scalar(Q(17,10)),f.sum_field(weights)))>0,'strict weight-sum upper bound')
    require(all(f.dot(n,f.matvec(H,unit))==f.T for n in neighbors),'all selected normals are actual reference contacts')
    rows=[f.matvec(H,n) for n in neighbors];corner_bounds=[]
    for signs in product((-1,1),repeat=3):
        u=divide(*cramer(rows,[f.scalar(s) for s in signs]))
        require(f.matvec(rows,u)==tuple(f.scalar(s) for s in signs),'exact inverse-normal cube corner')
        n2=norm(u,H)
        require(f.sign(f.sub(f.scalar(cube_norm_upper),n2))>0,'strict selected physical inverse norm at every cube corner')
        corner_bounds.append([list(signs),[str(a) for a in n2]])
    return {'contact_labels':list(labels),'positive_weights':[[str(a) for a in w] for w in weights],'corner_norms':corner_bounds,'cube_corners_actually_checked':8}

def scalar_bridge(plan):
    lo=Q(plan['lambda_strict_lower']);total=Q(plan['lambda_sum_strict_upper']);K=3
    alpha=max(Q(1),(total-lo)/lo);beta=1/(2*lo)
    require(alpha==Q(47,4) and beta==Q(15,4),'point contact-slack scalar coefficients')
    d=Q(plan['coarse_point_distance_max']);C=Q(plan['point_stability_constant'])
    require(K*beta*d<1 and K*alpha/(1-K*beta*d)==C,'coarse-radius point bound exactly600/13')
    delta=Q(plan['sharp_delta_max']);require(2100000*delta==d and delta<=Q(1,10**7),'enter coarse complete triple theorem')
    require(C*(1+C)<2200,'first sharp bootstrap triple bound below2200delta')
    d2=2200*delta
    require(K*beta*d2<1 and K*alpha/(1-K*beta*d2)<36,'second point bound below36eps')
    require(36*(1+36)==1332<1400==Q(plan['sharp_three_stability_constant']),'final three-point distance below1400delta')
    require(Q(9,4)>1+2*Q(593,1000) and Q(407,1000)>Q(25,64),'square-root metric norm and derivative bounds')
    require(1+2*Q(14,25)>Q(25,16),'second metric eigenvalue derivative bound')
    require(Q(3,2)*15+Q(32,25)<24 and Q(3,2)*2==3,'physical frame Lipschitz constants24and3')
    gate=Q(plan['subcritical_parameter_gate'])
    require(gate<=delta and 10*1400*gate<Q(1,400000) and 1400*gate<Q(1,100),'complete O3/gauge/local-exclusion domains')
    return {'point_bound':'600/13 eps','first_bootstrap':'2200delta','second_point_bound':'36eps','sharp_three_bound':'1400delta','sharp_delta_max':str(delta),'parameter_error':'24|t-tau|+3|z-z0|','subcritical_gate':str(gate),'gauged_distance_max':str(10*1400*gate),'local_radius':'1/400000'}

def derivative_box(plan,exact_points):
    ta,tb=map(Q,plan['closed_parameter_box']['t']);za,zb=map(Q,plan['closed_parameter_box']['z'])
    require(Q(14,25)<ta<tb<Q(593,1000) and Q(-5,2)<za<zb<Q(5,2),'entire rectangle lies in original source domain')
    interval_points,regularity=points(A(I(ta,tb),1,0),A(I(za,zb),0,1))
    require(all(v.l>0 for v in regularity.values()),'strict entire-rectangle Gram/denominator/root/chart positivity')
    records=[]
    for i in CORE:
        row=interval_points[i];dt=sum(absmax(x.dt) for x in row);dz=sum(absmax(x.dz) for x in row)
        require(dt<15 and dz<2,'whole-rectangle component derivative l1 bounds')
        records.append({'label':i,'derivative_t_l1_upper':str(dt),'derivative_z_l1_upper':str(dz),'all_six_coordinate_derivative_enclosures':[[str(Q(v.l,S)),str(Q(v.h,S))] for x in row for v in (x.dt,x.dz)]})
    zlo,zhi=map(Q,plan['z0_rational_bracket']);point,point_reg=points(A(I(f.LO,f.HI),1,0),A(I(zlo,zhi),0,1));checks=0
    for i in CORE:
        for j in range(3):
            for attr in ('v','dt','dz'):
                exact_value=getattr(exact_points[i][j],attr);a,b=f.interval(exact_value);v=getattr(point[i][j],attr)
                require(Q(v.l,S)<=a<=b<=Q(v.h,S),'separate exact jet specialization enclosed by interval jet');checks+=1
    return {'closed_parameter_box':plan['closed_parameter_box'],'point_specialization_enclosures_actually_checked':checks,'coordinate_derivatives_enclosed_over_entire_rectangle':72,'derivative_rows':records,'regularity_bounds':{k:[str(Q(v.l,S)),str(Q(v.h,S))] for k,v in regularity.items()},'no_feasible_subset_clipping_used':True}

def run(data,plan):
    layout(data,plan);H,V,B,z0,specialized,units=calibrate(data,plan)
    normals=[{'unit':name}|normal_case(H,V,units[name],labels) for name,labels in CASES]
    bridge=scalar_bridge(plan);derivatives=derivative_box(plan,specialized)
    return {'actual_agent':'six-tammes-2','role':'researcher','status':'CHECKED_EXACT_CHART_NORMAL_AND_DERIVATIVE_LOCAL_GATE','ordinary_geometry_formalized':False,'independent_new_result_review':'pending','all3_added_points_arbitrary':True,'new_global_bound':False,'exact_z0':[str(a) for a in z0],'all12_original_frame_specializations_checked':True,'positive_normal_cases':normals,'all40_inverse_normal_cube_corners_actually_checked':True,'scalar_bridge':bridge,'derivative_certificate':derivatives,'source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in FROZEN},'external_logical_dependencies':[9774,9828,7123,8704],'external_executable_or_private_data_runtime_input':False}

if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('50-second new-certificate guard')));signal.alarm(50)
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=run(json.loads((HERE/'INPUT.json').read_text()),json.loads((HERE/'PLAN.json').read_text()))
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('positive_normal_cases','derivative_certificate')},sort_keys=True))
