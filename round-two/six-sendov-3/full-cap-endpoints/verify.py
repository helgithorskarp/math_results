"""Exact finite support for sharp full ACTUAL equality-cap endpoint deduction.

The complete old cost and higher dual are credited8841/8883. This checker
validates their coordinate use; it does not reprove uniform entry/IFT bridges.
"""
from pathlib import Path
import argparse, hashlib, json
def source_gate():
    directory = Path(__file__).resolve().parent
    manifest = json.loads((directory/'SOURCE.json').read_text())
    if set(manifest['mathematical_files']) != {'arithmetic.py','verify.py'}:
        raise RuntimeError('pre-import mathematical source set')
    for name,pin in manifest['mathematical_files'].items():
        if hashlib.sha256((directory/name).read_bytes()).hexdigest() != pin:
            raise RuntimeError('pre-import source hash: '+name)


source_gate()
from arithmetic import C,P,F,require,cubic_root_interval,interval

DEFECTS = ('mean-axis','imaginary-axis','real-transverse','imaginary-transverse',
           'cubic-factor','second-tangent','third-real-sign','third-imag-sign',
           'slack-weight','fourth-constant','kappa-sign','normal-factor')


def calculate(defect=None):
    require(defect is None or defect in DEFECTS,'unknown mathematical defect')
    c = C(0,1)
    H = 14/(3*(1+c)); b2 = H/2
    rho = (c-5)/3; k = -7*(1+2*c)/18
    alpha = C(F(-527,360),F(41,90),F(13,90))
    kappa = (k+rho)**2/2+10*alpha/27
    if defect == 'kappa-sign':
        kappa = -kappa
    U0 = -8*(F(2,3)-1/(3*(1+c)))
    uz = (U0+rho*H)/8; up = uz-rho*H/2
    Wstar = C(F(2512,27),F(5840,9),F(-21392,27))
    Dstar = C(F(-4270,27),F(-29492,27),F(4012,3))
    Gamma = (6*uz**2+2*up**2-Dstar)/(2*H)
    Gstar = C(F(183619658945,2519424),F(444829186913,1259712),F(-288729410449,629856))
    Lmean = C(F(-101920,243),F(-1218245,486),F(251888,81))
    mustar = -3*Lmean/8
    Gmean = Gstar-3*Lmean**2/16
    stated_Gmean = C(F(340367352475,839808),F(808137564635,419904),F(-1052841914857,419904))
    if defect == 'fourth-constant':
        stated_Gmean += F(1,1000)
    ellold = C(F(50960,243),F(1218245,972),F(-125944,81))
    aT = C(F(-11564,405),F(-20482,81),F(123284,405))
    bT = C(F(49,180),F(-105889,486),F(305123,1215))
    cosines = [C(1),2*c**2-1,1+c-2*c**2,C(F(-1,2)),-c,-c,
               C(F(-1,2)),1+c-2*c**2,2*c**2-1]
    A3,B3 = C(F(3,2)),C(F(3,2))
    A4,B4 = 1+c,2-2*c**2
    w4 = 1/(c+2*c**2-1)
    w3 = F(2,3)*(7-B4*w4)
    if defect == 'slack-weight':
        w4 = -w4
    ids = []

    def eq(name, lhs, rhs):
        lhs,rhs = P(lhs),P(rhs)
        require(lhs==rhs,'whole identity: '+name)
        ids.append({'name':name,'lhs':lhs.record(),'rhs':rhs.record()})

    eq('entire physical cubic relation',8*c**3-6*c-1,0)
    for j in range(1,10):
        eq('entire physical nine-root cosine recurrence '+str(j),
           cosines[j%9],2*cosines[1]*cosines[(j-1)%9]-cosines[(j-2)%9])
    eq('credited fourth constant',Gmean,stated_Gmean)
    eq('credited real mean linear coefficient',-2*ellold,Lmean)
    eq('physical even dual first response',(w3*A3+w4*A4)/8,1)
    eq('physical even dual second response',(w3*B3+w4*B4)/7,1)
    eq('credited imaginary residual weight',aT,-alpha*H*b2)
    eq('credited common imaginary weight',F(2,3)*aT+4*bT,9*kappa*H*b2)

    mu,q = P.variable('mu'),P.variable('q_over_b')
    rr = [P.variable('r'+str(i)) for i in range(5)]
    vv = [P.variable('v_over_b'+str(i)) for i in range(5)]
    rr += [-sum(rr,P(0))];vv += [-sum(vv,P(0))]
    q_for_chart = 2*q if defect == 'imaginary-axis' else q
    mu_for_chart = 2*mu if defect == 'mean-axis' else mu
    old_i = [v-q_for_chart/3 for v in vv]
    old_r = [r-mu_for_chart/3 for r in rr]
    R,S = sum(old_r,P(0)),sum(old_i,P(0))
    R2,V2 = sum((r*r for r in rr),P(0)),sum((v*v for v in vv),P(0))
    eq('all six real residuals zero sum',sum(rr,P(0)),0)
    eq('all six imaginary residuals zero sum',sum(vv,P(0)),0)
    eq('old real mean channel',R,-2*mu)
    eq('old imaginary mean channel',S,-2*q)
    oldcost = (P(Gstar)+R*ellold+sum((v*v for v in old_i),P(0))*aT+S*S*bT+
               sum((r*r for r in old_r),P(0))/2+R*R/4)
    t_over_b = q*(3*H)
    t2 = t_over_b*t_over_b*b2
    realweight = F(1,3) if defect == 'real-transverse' else F(1,2)
    imagweight = alpha*H*b2 if defect == 'imaginary-transverse' else -alpha*H*b2
    axiscost = P(Gmean)+(mu-mustar)**2*F(4,3)+t2*(kappa/H)+R2*realweight+V2*imagweight
    eq('ENTIRE twelve-dimensional old cost to axis cost',oldcost,axiscost)
    xihat = [P(Gamma)+q,-P(Gamma)+q]+[v-q/3 for v in vv]
    nu = [P(Wstar/8)+mu+q*(b2*(rho+3*k)),P(Wstar/8)+mu-q*(b2*(rho+3*k))]
    nu += [P(Wstar/8)-mu/3+r for r in rr]
    eq('full first imaginary mean',sum(xihat,P(0)),0)
    eq('full first imaginary norm',b2*(xihat[0]-xihat[1]),H*Gamma)
    eq('full first real mean',sum(nu,P(0)),Wstar)
    eq('full first mixed affine closure',nu[0]-nu[1],(xihat[0]+xihat[1])*(b2*(rho+3*k)))
    eta = P.variable('eta')
    chi = [P.variable('chi'+str(i)) for i in range(8)]
    leading = [1,-1]+[0]*6
    entire_cube = sum(((P(a)+eta*x+eta*eta*y)**3 for a,x,y in zip(leading,xihat,chi)),P(0))*b2
    eq('complete cubic constant, all eight slots',entire_cube.coefficient('eta',0),0)
    cubic_scale = F(1,2) if defect == 'cubic-factor' else 1
    eq('complete cubic first jet, all eight slots',entire_cube.coefficient('eta',1),t_over_b*cubic_scale)

    # Complete13-dimensional second tangent:6 free imaginary,7 free real.
    small = [P.variable('tau'+str(i)) for i in range(6)]
    common = -sum(small,P(0))/2
    tau = [common,common]+small
    if defect == 'second-tangent':
        tau[0] += P.variable('omitted_tau')
    varsigma = [P.variable('varsigma'+str(i)) for i in range(7)]
    varsigma += [-sum(varsigma,P(0))]
    eq('all second imaginary means',sum(tau,P(0)),0)
    eq('all second imaginary normal differential',b2*(tau[0]-tau[1]),0)
    eq('all second real means',sum(varsigma,P(0)),0)
    eq('ENTIRE thirteen-dimensional second cost differential',
       (tau[0]-tau[1])*(2*k*b2)+sum(varsigma,P(0))*uz,0)

    # Complete16-dimensional third correction, psi=b*psi_scaled.
    psi = [P.variable('psi_over_b'+str(i)) for i in range(8)]
    ups = [P.variable('upsilon'+str(i)) for i in range(8)]
    sumup = sum(ups,P(0)); hpsi = (psi[0]-psi[1])*b2
    p8 = sumup*F(-9,8);p7 = hpsi*F(9,7)
    if defect == 'third-real-sign':
        p8 = -p8
    if defect == 'third-imag-sign':
        p7 = -p7
    primitive = [P(0) for _ in range(10)]
    primitive[8],primitive[7] = p8,p7
    primitive[0] = -p8-p7
    expected_derivative = [P(0) for _ in range(9)]
    expected_derivative[7],expected_derivative[6] = -9*sumup,9*hpsi
    for j in range(9):
        eq('entire higher primitive derivative column '+str(j),(j+1)*primitive[j+1],expected_derivative[j])
    eq('entire higher primitive limiting anchor',sum(primitive,P(0)),0)
    rows = []
    for j in range(9):
        row = -sum((value*cosines[(j*n)%9] for n,value in enumerate(primitive)),P(0))/9
        rows.append(row)
        expected = -sumup*((1-cosines[j])/8)+hpsi*((1-cosines[(2*j)%9])/7)
        eq('ENTIRE individual original-root higher normal '+str(j),row,expected)
    eq('ENTIRE sixteen-dimensional third scalar-plus-dual trace',sumup-hpsi+rows[3]*w3+rows[4]*w4,0)
    # Half-normal convention: each paired slack pays each individual one.
    n = [P.variable('minus_N'+str(i)) for i in (3,4,5,6)]
    normal_divisor = 1 if defect == 'normal-factor' else 2
    slack = (n[0]+n[3])*(w3/normal_divisor)+(n[1]+n[2])*(w4/normal_divisor)
    eq('actual half-normal slack normalization',slack,(n[0]+n[3])*(w3/2)+(n[1]+n[2])*(w4/2))

    A = C(F(-13638695,972),F(-16011613,243),F(20901119,243))
    Bsin = C(F(1448,243),F(6982,243),F(-8224,243))
    Q = C(F(8,162),F(25,162),F(20,162))
    ell2 = -H*Gmean/kappa
    values = {'H':H,'b_squared':b2,'kappa':kappa,'minus_Gmean':-Gmean,
              'minus_alpha':-alpha,'old_aT':aT,'old_aT_plus6bT':aT+6*bT,
              'transverse_imaginary_weight':-alpha*H,'w3':w3,'w4':w4,
              'ell_squared':ell2,'motion_A':A,'motion_B_over_positive_sin':Bsin,'motion_Q':Q}
    bracket = cubic_root_interval()
    signs = []
    for name,value in values.items():
        lo,hi = interval(value,bracket)
        require(lo>0,'strict physical sign: '+name)
        signs.append({'name':name,'cubic':value.record(),'lower':str(lo),'upper':str(hi)})
    return {'schema':'full-cap-endpoints-v1','agent':'six-sendov-3','role':'researcher',
            'scope':'Exact prior-cost coordinate and full higher differential support; uniform actual comparison is a credited ordinary analytic premise.',
            'axis_dimension':12,'second_tangent_dimension':13,'third_correction_dimension':16,
            'critical_slots':8,'original_labels':9,'whole_identities':ids,
            'whole_prior_cost':oldcost.record(),'whole_axis_cost':axiscost.record(),
            'whole_eight_slot_cubic':entire_cube.record(),
            'whole_third_primitive':[v.record() for v in primitive],
            'individual_third_normals':[r.record() for r in rows],
            'physical_c_bracket':[str(x) for x in bracket], 'positive_signs':signs,
            'constants':{n:v.record() for n,v in {'Gmean':Gmean,'ell_squared':ell2,'mu_star':mustar,
                'motion_A':A,'motion_B_over_sin':Bsin,'motion_Q':Q}.items()}}


def encoded(record):
    return json.dumps(record,sort_keys=True,separators=(',',':')).encode()+b'\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    parser.add_argument('--defect',choices=DEFECTS)
    parser.add_argument('--without-expected',action='store_true')
    args = parser.parse_args()
    record = calculate(args.defect);data = encoded(record)
    summary = {'schema':record['schema'],'whole_bytes':len(data),'whole_sha256':hashlib.sha256(data).hexdigest(),
               'whole_identities':len(record['whole_identities']),'positive_signs':len(record['positive_signs']),
               'axis_dimension':12,'second_tangent_dimension':13,'third_correction_dimension':16}
    if not args.without_expected:
        expected = json.loads((Path(__file__).parent/'EXPECTED.json').read_text())
        require(summary==expected,'complete canonical record agreement')
    if args.output:
        args.output.write_bytes(data)
    print(json.dumps({'status':'PASS',**summary},sort_keys=True),flush=True)


if __name__ == '__main__':
    main()
