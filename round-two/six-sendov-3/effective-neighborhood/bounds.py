"""Exact scalar hypotheses for the unformalized analytic proof in PROOF.md.

All eta/delta comparisons below are covered monomial bounds, not samples.
Only unchanged, hash-bound radial arithmetic is imported as a computation.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from math import comb, factorial
import json,sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'radial-slack'))
from radial import certificate as radial_certificate
from sector import exact,embedding,enclose,I

E=F(1,65536)

def require(test,label):
    if not test:raise RuntimeError(label)

class M:
    """Positive monomial coefficient * eta**eta_power * delta**delta_power."""
    def __init__(self,c=1,e=0,g=0):self.c,self.e,self.g=F(c),int(e),int(g)
    def __mul__(self,other):
        if not isinstance(other,M):other=M(other)
        return M(self.c*other.c,self.e+other.e,self.g+other.g)
    __rmul__=__mul__
    def __truediv__(self,other):
        if not isinstance(other,M):other=M(other)
        return M(self.c/other.c,self.e-other.e,self.g-other.g)
    def __pow__(self,k):return M(self.c**k,self.e*k,self.g*k)
    def same(self,other):return (self.c,self.e,self.g)==(other.c,other.e,other.g)
    def record(self):return {'coefficient':str(self.c),'eta_power':self.e,'delta_power':self.g}

def input_data():
    r=radial_certificate()
    values,_,_,_,_=exact();c=embedding()
    box=[enclose(v,c)+I.bounds(-F(1,1024),F(1,1024)) for v in values]
    return r,box

def budgets(r,box,damage=None):
    rho=F(1,2**60) if damage!='raw-analytic-domain' else F(1,16)
    rroot=F(1,2**16) if damage!='original-root-disks' else F(1,1024)
    nvars=16 if damage!='cauchy-dimension' else 1
    inverse_c=2**10 if damage!='inverse-majorant' else 1
    mu_floor=F(9,32) if damage!='radial-margin' else F(3,10)
    second_bound=128 if damage!='original-second-derivative' else 64
    coeff_den=2**7 if damage!='coefficient-rouche' else 32
    free_norm=4 if damage!='free-euclidean-metric' else 2
    checks=[]
    def scalar(test,label):require(test,label);checks.append(label)
    def covered(m,label,limit=1,strict=False):
        scalar(m.c>=0 and m.e>=0 and m.g>=0,label+' nonnegative monomial exponents')
        upper=m.c*E**m.e*F(1,2)**m.g
        scalar(upper<limit if strict else upper<=limit,label+' whole eta/delta bound')
        return str(upper)

    scalar(nvars==12+4,'all sixteen raw and target variables retained')
    scalar(all(max(abs(F(v[0])),abs(F(v[1])))<1 for rows in (r['even_radial_div_eta'],r['odd_radial_div_eta3half_sine']) for row in rows for v in row),'all eight Jacobian entries below one')
    scalar(F(r['even_determinant'][0])>F(1,16),'even determinant input')
    scalar(F(r['odd_determinant'][1])<-F(1,100),'odd determinant input')
    scalar(all(F(v[0])>F(1,4) for v in r['upper_root_sines']),'both original-root sine inputs')
    scalar(all(F(v[0])>mu_floor for v in r['individual_root_multipliers']),'individual half-normal gradient margins')
    scalar(all(v.lo>I(-2).hi and v.hi<I(2).lo for v in box[:2]),'both branch centers below two')
    scalar(box[2].lo>I(1).hi and box[2].hi<I(2).lo,'opening in one to two')
    scalar(4*E*E+2*E<F(1,1024),'all eight branch critical moduli below one thirty-second')
    # ||A^-1|| <=800 eta^-3/2. Divide by L and use eta<=E.
    scalar(F(800,inverse_c)**2*E<1,'actual raw tail inverse bounded by L')
    scalar(F(2)/(F(1,16))==32 and F(2)/(F(1,100))*4==800,'two inverse row bounds and conjugate normalization')

    scalar(rho+16*rho*rho<2*rho and 2*rho<F(1,2),'heavy radicand analytic disk')
    scalar(2+rho<3 and F(1+6*3+8*3,2)<22,'literal heavy moment numerator bound')
    scalar(45+6<64 and F(1,32)+64*rho<F(1,16),'all complex critical displacements')
    S=sum((F(9,9-k)*comb(8,k)*F(1,32)**k for k in range(1,9)),F(0))
    scalar((1-E)**9-S>F(1,2),'marked anchor gives constant modulus above one-half')
    scalar(9*F(15,32)**8>F(1,64),'all original-root derivatives above one sixty-fourth')
    scalar(2*rroot<F(1,2**13),'nine disjoint original-root disks')
    scalar(72*(1+rroot+F(1,32))**7<second_bound,'original polynomial second derivative bound')
    scalar(F(second_bound,2)*rroot<F(1,128),'linear Rouche remainder margin')
    scalar(3*9*8*64*3**7<2**26,'anchored eight-factor perturbation majorant')
    scalar(2**26*rho<rroot/128,'all nine original-root Rouche circles')
    scalar(((1+rroot)**2+1)/2<2,'holomorphic half-normal modulus bound')
    scalar(1-E-F(1,32)>F(15,16),'all branch reciprocal distances')
    scalar(64*(4+64*rho)<2**9 and 2**9*rho<F(1,4),'analytic companion-distance disks')
    scalar(F(15,16)**2-F(1,4)>F(1,4),'eight reciprocal square-root domains')
    scalar(8*2<32,'holomorphic objective modulus bound')
    B1=M(2**70);B2=M(2**136);L=M(inverse_c,-2)
    scalar(32*(2*nvars/rho)==B1.c,'raw first Cauchy operator bound')
    scalar(factorial(2)*32*(2*nvars/rho)**2==B2.c,'raw second Cauchy operator bound')
    s=M(1)/(8*L*B2);d=M(1)/(64*L**2*B1*B2)
    scalar(s.same(M(F(1,2**149),2)) and d.same(M(F(1,2**232),4)),'derived raw tail and complete target radii')
    covered(s/M(rho/2),'entire tail ball in analytic inner domain',strict=True)
    covered(d/s,'free and normal target product fits raw tail domain',strict=True)
    scalar((L*B2*s).same(M(F(1,8))),'off-branch tail Jacobian contraction')
    scalar((L*M(B1.c+1)*d/s).c<F(1,4),'contraction center displacement below one quarter')
    covered(B1*s/M(F(1,8),1),'all inactive-root half-normal variations',strict=True)
    scalar(F(1,2)-5*rho>F(1,4),'heavy pair and heavy-small separation')
    K2=M(2**16)/d**2;K3=M(2**23)/d**3
    scalar(factorial(2)*32*(2*nvars)**2==2**16,'completely eliminated second Cauchy bound')
    scalar(factorial(3)*32*(2*nvars)**3<2**23,'completely eliminated third Cauchy bound')
    b=d**2/(2**22);R=M(1,2,1)*d**3/(2**23);t=R/4
    scalar(R.same(M(F(1,2**719),14,1)) and t.same(M(F(1,2**721),14,1)),'explicit eta/kappa radius exponents')
    covered(b/(d/2),'radial box in eliminated Cauchy inner domain',strict=True)
    covered(R/b,'free Euclidean ball in radial box',strict=True)
    scalar((K2*b).same(M(F(1,64))),'each actual radial gradient variation')
    scalar(mu_floor-F(1,64)>=F(17,64)>F(1,4),'signed feasible individual-root integration')
    scalar((K3*R/M(1,2,1)).same(M(1)),'eliminated zero-slack Taylor budget')
    scalar(free_norm**2>12,'literal twelve-coordinate Euclidean norm')
    scalar(t.same(R/free_norm),'raw box implies Euclidean free radius')
    covered(B1*t/b,'raw box implies actual four-normal radius',strict=True)
    covered(t/s,'raw tail in complete uniqueness ball',strict=True)
    ccrit=M(1,2)*t/(2**10);ccoef=M(1,1)*ccrit**6/coeff_den
    target=M(F(1,2**4393),97,6)
    if damage=='coefficient-radius-exponent':target=M(F(1,2**4393),98,6)
    scalar(ccoef.same(target),'literal polynomial-coefficient radius exponents')
    covered(ccrit/M(F(1,4),1),'critical disks smaller than eta over four',strict=True)
    scalar(F(1,1024)<F(9,64),'heavy critical Rouche comparison after nonnegative eta deflation')
    scalar(F(36,coeff_den)<1,'all eight criticals accounted for by coefficient Rouche')
    scalar(5<1024 and 8<1024 and 40<1024,'heavy T V M recovery in raw neighborhood')
    scalar(F(1,4)-F(33,16)*E>F(1,8),'explicit quarter-curvature gap')
    scalar((2**4393)*8**6==2**4411,'quarter-curvature coefficient-ball exponent')
    if damage=='negative-eta-comparison':covered(M(1,-1),'invalid covered comparison')
    radial_bytes=json.dumps(r,sort_keys=True,separators=(',',':')).encode()
    return {'schema':'six-sendov-3-effective-neighborhood-v1','actual_agent':'six-sendov-3','role':'researcher',
            'eta_interval':['0 exclusive',str(E)],'coefficient_range':'0<=k<1/2-33eta/16',
            'delta_definition':'1/2-33eta/16-k','delta_interval':['0 exclusive','1/2 inclusive'],
            'raw_dimension':16,'free_metric_dimension':12,'normal_metric':'(|Z_i|^2-1)/2',
            'radial_input_record_sha256':sha256(radial_bytes).hexdigest(),
            'branch_covering_cube_radius':'1/1024','raw_complex_radius':str(rho),'original_root_disk_radius':str(rroot),
            'original_coefficient_sum_majorant':str(S),'raw_first_derivative_bound':str(B1.c),'raw_second_derivative_bound':str(B2.c),
            'tail_inverse_majorant':L.record(),'tail_ball':s.record(),'full_target_polydisk':d.record(),
            'radial_box':b.record(),'free_Euclidean_ball':R.record(),'all_feasible_raw_box':t.record(),
            'critical_entry_disks':ccrit.record(),'all_feasible_coefficient_ball':ccoef.record(),
            'quarter_curvature_coefficient_ball':M(F(1,2**4411),97).record(),
            'eliminated_second_derivative_majorant':K2.record(),'eliminated_third_derivative_majorant':K3.record(),
            'certified_slack_coefficient':'17/64','stated_slack_coefficient':'1/4','checks':checks,
            'coverage':'whole positive eta interval and whole positive explicit kappa gap; no eta samples',
            'proof_trust_boundary':'ordinary complexification/Cauchy/contraction/Rouche/Taylor proof remains unformalized'}

DAMAGES=('raw-analytic-domain','original-root-disks','cauchy-dimension','inverse-majorant',
         'radial-margin','original-second-derivative','coefficient-rouche','free-euclidean-metric',
         'coefficient-radius-exponent','negative-eta-comparison')

def build():
    r,box=input_data();out=budgets(r,box);rejected=[]
    for name in DAMAGES:
        try:budgets(r,box,name)
        except RuntimeError:rejected.append(name)
    require(rejected==list(DAMAGES),'all mathematical damaged budgets reject')
    out['mathematical_damage_rejections']=rejected
    return out
