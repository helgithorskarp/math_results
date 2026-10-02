"""Exact whole-window budgets for moment entry and a feasible imbalance family.

Analytic arguments and the meaning of the quantities are in PROOF.md.
Native solver libraries and floating point arithmetic are unnecessary.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from math import comb, factorial
import json, sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'normalized-neighborhood'))
import bounds as prior

E = F(1, 65536)
M = prior.M
BASELINE_HASH = 'fccc5f467ca924daa99abaa164cbd230b947931d52a42165477c0763e256b749'

def require(test, label):
    if not test:
        raise RuntimeError(label)

def sixfold_family(damage=None):
    checks=[]
    def check(value,label):
        require(value,label);checks.append(label)
    u=F(1,2**310);eta_circle=F(1,1024);nu_circle=F(1,2048)
    root_circle=F(1,16);X=F(9,8);Y=F(5,4);T=F(25,16)
    weight=32;nu_max=E**6*u**6
    check(F(9,8)+weight*nu_circle<=Y,'sixfold whole complex real-center majorant')
    major={}
    for k in range(1,9):
        value=F(0)
        if k<=6:value+=comb(6,k)*X**k*eta_circle**(k-1)
        if 0<=k-1<=6:value+=comb(6,k-1)*X**(k-1)*2*Y*eta_circle**(k-1)
        if 0<=k-2<=6:value+=comb(6,k-2)*X**(k-2)*(T*eta_circle**(k-2)+Y**2*eta_circle**(k-1))
        if k==8:value+=nu_circle
        major[str(k)]=str(value)
    zz=1+root_circle;az=1+eta_circle
    P=9*az**8+sum((F(9,9-k)*F(major[str(k)])*(zz**(9-k)+az**(9-k)) for k in range(1,9)),F(0))
    check(P<64,'sixfold complete anchored eta-nu polynomial majorant')
    check(64*eta_circle<F(1,4),'sixfold all nine unique original-root sections')
    check(9*F(29,32)**8>4,'actual branch original derivative lower bound four')
    check(F(18,4)<5,'constant-impulse actual radial derivative below five')
    check(-F(weight,3)+5<-4,'sixfold all four active originals move inward')
    first=2**11/(nu_circle/2);second=factorial(2)*2**11/(nu_circle/2)**2
    if damage=='sixfold-cauchy':second=2**35
    check(first==2**23 and second==2**36,'sixfold full first and second divided-normal derivatives')
    check(nu_max<nu_circle/2 and nu_max<F(1,2**36),'sixfold real path fits the whole inward Cauchy region')
    check(first*nu_max<F(1,8),'sixfold inactive originals retain strict half-slack')
    check(F(2**35)*nu_max<1,'sixfold active radial Taylor remainder')
    lam_factor=2 if damage!='sixfold-circle' else 1
    check(lam_factor**6/4>2,'sixfold small critical circle defeats the constant impulse')
    check(2*E*u<F(1,32),'sixfold critical circles lie below modulus one sixteenth')
    check(E*X<F(1,32) and E*Y<F(1,32),'sixfold circle critical factors below one eighth')
    check(1+F(64,8**7)+F(1024,8**6)*E*nu_max<2,'sixfold whole critical perturbation below twice eta-nu')
    check(64*F(1,256)**5*u**5<1,'sixfold heavy critical circles defeat the impulse')
    check(2*F(1,256)*u<F(1,4),'sixfold critical clusters remain separated')
    check(32*E*u*u<F(1,16),'sixfold own critical matching beats wrong clusters')
    check(X+Y+u/2<3,'sixfold real-root test center bound')
    check(T+9*E<2,'sixfold real-root test opening bound')
    check(F(2,64)<1 and 64>1,'sixfold real critical lies between eta-u over two and twice eta-u')
    radius=F(1,2**321) if damage!='sixfold-free-box' else u
    check(u/2>radius,'sixfold real critical leaves the displayed free Euclidean ball')
    root_bound=2*root_circle/(eta_circle*nu_circle)
    check(root_bound==2**18,'sixfold doubly removable original displacement bound')
    check(8*root_bound**2==2**39,'sixfold complete original energy upper bound')
    check(F(9,8)*2*weight==72 and F(72**2,8)==648,'sixfold coefficient trace and original energy lower bounds')
    check(200**2*2**39<2**56,'sixfold all-coefficient eta7 upper bound')
    original_power=14 if damage!='original-energy-power' else 13
    check(2*(1+6)==original_power,'sixfold sharp original energy exponent')
    check(2*(1+6)==2*7,'sixfold coefficient power seven')
    check(8*2**2==32,'sixfold critical energy upper constant')
    return dict(checks=checks,u=str(u),nu_max=str(nu_max),eta_complex_radius=str(eta_circle),nu_complex_radius=str(nu_circle),
        elementary_div_eta_majorants=major,anchored_polynomial_div_eta_majorant=str(P),
        divided_normal_first_bound=str(first),divided_normal_second_bound=str(second),
        critical_energy_bounds=['eta^2*u^2/4','32*eta^2*u^2'],
        original_energy_bounds=['648*eta^14*u^12','2^39*eta^14*u^12'],
        coefficient_distance_bounds=['72*eta^7*u^6','2^28*eta^7*u^6'],
        trace='Im(sum critical)=0',free_metric='D>=u^2/4>R^2')

def budgets(inputs, damage=None):
    radial, box, limit, c = inputs
    checks = []
    def scalar(test, label):
        require(test, label)
        checks.append(label)
    def covered(m, label, upper=1, strict=False):
        scalar(m.c >= 0 and m.e >= 0 and m.g >= 0 and
               (2*m.e).denominator == 1,
               label+' nonnegative exact eta/delta powers')
        value = m.c * F(1,256)**int(2*m.e) * F(1,2)**m.g
        scalar(value < upper if strict else value <= upper,
               label+' whole-window comparison')
        return str(value)

    t = M(F(1,2**322), 0, 1)
    b = F(1,2**227)
    lam = M(1,1)*t/1024
    den = 128 if damage != 'rouche-count' else 32
    coef = M(1,1)*lam**6/den
    exponent = 7 if damage != 'coefficient-exponent' else 8
    scalar(coef.same(M(F(1,2**1999), exponent, 6)),
           'eta7 coefficient radius exact identity')
    covered(lam/M(F(1,4),1), 'critical circles smaller than eta over four', strict=True)
    scalar(F(36,den) < 1, 'all eight derivative coefficient perturbations in Rouche')
    covered(lam**5/M(F(9,64),F(5,2)), 'heavy circle lower bound exceeds small circle floor', strict=True)
    scalar(4*E*E+2*E < F(1,1024), 'branch critical moduli below one thirty-second')
    covered(lam, 'three critical circles contained in unit disk', upper=F(1,64), strict=True)
    scalar(F(8,9)*F(9,8) == 1, 'first critical Newton sum coefficient')
    second = F(14,9) if damage != 'newton-factor' else F(7,9)
    scalar(second*F(9,7)/2 == 1, 'second critical Newton sum coefficient')
    covered(coef/M(1,1), 'coefficient radius smaller than eta', strict=True)
    scalar(F(14,9)+F(8,9)*33*E < 2, 'full second Newton sum perturbation below twice coefficient norm')
    # |S1^0|<=16eta, |Delta S1|<=8C/9<C<eta.
    trace_to_raw = coef/M(1,F(3,2))/t
    covered(trace_to_raw, 'total imaginary trace recovery', upper=F(1,1024), strict=True)
    covered(trace_to_raw, 'total mixed moment recovery', upper=F(1,1024), strict=True)
    scalar(5 < 1024, 'heavy squared imaginary moment recovery')
    scalar(F(1,1024) < 1, 'each free h and u and heavy y lies in raw box')
    scalar(F(1,4)-F(33,16)*E > F(1,8), 'quarter curvature positive uniform gap')
    scalar(2**1999*8**6 == 2**2017, 'quarter eta7 coefficient constant')
    scalar(8*70**2 < 200**2, 'eight original-root coefficient telescoping constant')
    scalar(200**2 < 2**16, 'simple eta14 original-root energy constant')

    critical_energy = M(1,3)*t**2/(2**20)
    balanced_energy = M(1,2)*t**2/(2**20)
    if damage == 'energy-without-trace':
        critical_energy = balanced_energy
    scalar(critical_energy.same(M(F(1,2**664),3,2)), 'eta3 unconditional critical energy')
    scalar(balanced_energy.same(M(F(1,2**664),2,2)), 'eta2 separately balanced critical energy')
    scalar(8 < 1024 and 40 < 1024, 'literal total V and mixed M raw recovery budgets')
    scalar(2**664*8**2 == 2**670, 'quarter critical energy constant')
    scalar(2*2017+16 == 4050, 'quarter original energy constant')
    # Their ratio is eta^-6: eta7 strictly enlarges9373's eta13 ball.
    covered(M(1,6), 'old eta13 ball divided by new eta7 ball', strict=True)

    xbound, y0bound, ybound, tbound = F(9,8),F(9,8),F(5,4),F(25,16)
    eta_circle, xi_circle, root_circle = F(1,1024), F(1,64), F(1,16)
    for j in (0,1):
        scalar(box[j].lo > prior.I(-xbound).hi and box[j].hi < prior.I(xbound).lo,
               'actual branch center '+str(j)+' below nine eighths')
    scalar(box[2].lo > prior.I(1).hi and box[2].hi < prior.I(tbound).lo,
           'actual opening in one to twenty-five sixteenths')
    scalar(y0bound+8*xi_circle == ybound, 'whole complex family y majorant')
    family_linear = 2*ybound+xi_circle
    family_constant = ybound*ybound+xi_circle*ybound+xi_circle*xi_circle/2
    majors = {}
    for k in range(1,9):
        value = F(0)
        if k <= 6:
            value += comb(6,k)*xbound**k*eta_circle**(k-1)
        if 0 <= k-1 <= 6:
            value += comb(6,k-1)*xbound**(k-1)*family_linear*eta_circle**(k-1)
        if 0 <= k-2 <= 6:
            value += comb(6,k-2)*xbound**(k-2)*(tbound*eta_circle**(k-2)+family_constant*eta_circle**(k-1))
        majors[str(k)] = str(value)
    zz, az = 1+root_circle, 1+eta_circle
    P = 9*az**8 + sum((F(9,9-k)*F(majors[str(k)])*(zz**(9-k)+az**(9-k)) for k in range(1,9)),F(0))
    scalar(P < 64, 'entire complex eta-xi anchored polynomial majorant')
    floor = 9*root_circle-36*(1+root_circle)**7*root_circle**2
    scalar(floor > F(1,4), 'nine fixed root circles baseline floor')
    scalar(64*eta_circle < F(1,4), 'all family root sections on complete polydisk')
    scalar(2*root_circle < F(1,2), 'all nine original-root sections distinct')
    scalar(((1+root_circle)**2+1)/2 < 2, 'holomorphic companion half-normal bound')
    scalar(2/eta_circle == 2**11, 'removable alpha divided by eta bound')
    first = 2**11/(xi_circle/2)
    second_bound = factorial(2)*2**11/(xi_circle/2)**2
    if damage == 'family-cauchy':
        second_bound = 2**20
    scalar(first == 2**18 and second_bound == 2**26, 'family first and second Cauchy derivatives')
    jfloor = F(-1,3) if damage != 'radial-y-floor' else F(-1,2)
    scalar(all(F(row[0][1]) < jfloor for row in radial['even_radial_div_eta']),
           'both actual branch inward-y radial slopes below minus one third')
    scalar(all(max(abs(F(v[0])),abs(F(v[1]))) < 1 for rows in
               (radial['even_radial_div_eta'],radial['odd_radial_div_eta3half_sine'])
               for row in rows for v in row), 'all branch normalized entries below one')
    inward = 8 if damage != 'inward-y-weight' else 1
    scalar(inward*jfloor+1+E*y0bound < F(-3,2), 'four active original derivatives strictly inward')
    scalar(F(1,800)-E*y0bound > F(1,1024), 'nonzero odd V slope after mixed-moment correction')
    scalar(F(2)/F(1,16) == 32 and F(2)/F(1,100)*4 == 800,
           'credited four-tail inverse implies V-column lower bound')
    v = F(2**12)*b if damage != 'imbalance-box' else F(2**9)*b
    xi_max = F(1,256)*v
    scalar(v > t.c/2, 'family V outside raw t box for every gap')
    scalar(v < F(1,2**50), 'family second normalized normal remainder')
    scalar(8*F(1,256) < 1 and E*ybound < 1,
           'literal maximum raw family displacement equals v')
    scalar(v < F(1,256), 'complete raw family segment in inner joint domain')
    scalar(xi_max < xi_circle/2 and xi_max < F(1,2**26), 'entire real family interval inside Cauchy inward region')
    scalar(first*xi_max < F(1,8), 'all inactive originals stay strictly interior')
    scalar(F(2**25)*xi_max < F(1,2), 'four active inward Taylor signs retained')
    scalar(8*F(1,256)**3 < 1, 'higher mixed moment term included in second remainder')
    scalar(F(2**39)*v < F(1,2048), 'odd normal Taylor error below half linear margin')
    scalar(v/2048 >= 2*b, 'actual normalized gamma strictly outside b box')
    scalar(E*E*v*v/4 < F(1,4), 'family heavy opening positive and separated')
    scalar(9*E*v < F(1,4), 'heavy matched displacements below sqrt eta over four')
    scalar(129*E*E*v*v < F(1,16), 'own critical matching beats every cross-cluster match')
    energy_hi = 129 if damage != 'family-energy' else 128
    scalar(F(257,2)+E*E*v*v/8 < energy_hi, 'family critical energy upper bound')
    scalar(2*64+F(1,2) == F(257,2), 'exact heavy-pair squared displacement leading coefficient')
    scalar((2*root_circle)/(eta_circle*xi_circle) == 2**13,
           'doubly removable original-root displacement majorant')
    scalar(8*(2**13)**2 == 2**29, 'all eight original-root energy upper bound')
    scalar(F(9,8)**2*257/8 == F(20817,512), 'original trace energy lower bound')
    scalar(F(9,8)*16 == 18, 'explicit original coefficient displacement scale')

    second_family=sixfold_family(damage)
    checks.extend(second_family.pop('checks'))
    return {
        'schema':'six-sendov-3-moment-entry-v2','actual_agent':'six-sendov-3','role':'researcher',
        'eta_interval':['0 exclusive',str(E)],'kappa_range':'0<=k<1/2-33eta/16',
        'delta_definition':'1/2-33eta/16-k','unchanged_raw_radius':t.record(),
        'critical_rouche_radius':lam.record(),'coefficient_entry_radius':coef.record(),
        'quarter_coefficient_radius':M(F(1,2**2017),7).record(),
        'critical_energy_entry':critical_energy.record(),
        'balanced_critical_energy_entry':balanced_energy.record(),
        'balanced_trace_condition':'abs(Im(sum critical))<=eta^(3/2)*t/128',
        'quarter_critical_energy_entry':M(F(1,2**670),3).record(),
        'original_energy_entry':'Eoriginal<=coefficient_entry_radius^2/40000',
        'quarter_original_energy_entry':M(F(1,2**4050),14).record(),
        'first_Newton_sum':'-8*c8/9','second_Newton_sum':'64*c8^2/81-14*c7/9',
        'literal_V':'Im(first_Newton_sum)/eta^(3/2)',
        'literal_M':'Im(second_Newton_sum)/(2eta^(3/2))',
        'family_v':str(v),'family_normal_box':str(b),
        'family_definition':{'y':'y0+8*sqrt(eta)*v','T':'T0','V':'v','M':'eta*v*y','six_free_pairs':'h=0,u=x0'},
        'family_eta_complex_radius':str(eta_circle),'family_xi_complex_radius':str(xi_circle),
        'family_root_disk_radius':str(root_circle),'family_elementary_div_eta_majorants':majors,
        'family_anchored_polynomial_div_eta_majorant':str(P),
        'family_alpha_div_eta_bound':2**11,'family_alpha_first_xi_bound':str(first),
        'family_alpha_second_xi_bound':str(second_bound),
        'family_gamma_lower_bound':'max(abs(gamma3),abs(gamma4))>v/2048=2b',
        'family_critical_energy_bounds':['(257/2)*eta^3*v^2','129*eta^3*v^2'],
        'family_original_energy_bounds':['(20817/512)*eta^3*v^2','2^29*eta^3*v^2'],
        'sixfold_real_family':second_family,
        'sharp_scope':'coefficient power7, original matching energy power14, critical matching energy power3, separately balanced critical energy power2 for uniform entry into fixed displayed collar; constants not optimal',
        'unproved':'global concentration/minimum; optimal entry constants or larger domains; unrestricted first-power conjecture',
        'checks':checks,
        'proof_trust_boundary':'ordinary root-section/max-modulus/divisibility/Cauchy/Taylor/Rouche/multiset arguments unformalized'
    }

DAMAGES = ('rouche-count','coefficient-exponent','newton-factor','energy-without-trace',
           'family-cauchy','radial-y-floor','inward-y-weight','imbalance-box','family-energy',
           'sixfold-cauchy','sixfold-circle','sixfold-free-box','original-energy-power')

def build():
    baseline = prior.build()
    digest = sha256(json.dumps(baseline,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    require(digest == BASELINE_HASH, 'unchanged full9373 mathematical record')
    inputs = prior.input_data()
    result = budgets(inputs)
    rejected = []
    for damage in DAMAGES:
        try:
            budgets(inputs, damage)
        except RuntimeError:
            rejected.append(damage)
    require(rejected == list(DAMAGES), 'all semantic mathematical damages reject')
    result['credited_baseline_sha256'] = digest
    result['credited_baseline_predicates'] = len(baseline['checks'])
    result['mathematical_damage_rejections'] = rejected
    return result
