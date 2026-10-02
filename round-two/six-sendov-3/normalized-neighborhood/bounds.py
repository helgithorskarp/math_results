"""Exact hypotheses for the normalized analytic proof; no eta grid.

The positive-monomial bookkeeping and coefficient-entry budgets retain
credit to effective-neighborhood (9315). Radial/cubic arithmetic is imported
unchanged. The new joint-domain/normalized Cauchy estimates are recomputed.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from math import comb, factorial
import json,sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'radial-slack'))
from radial import certificate as radial_certificate
from sector import exact,embedding,enclose,I,K

E=F(1,65536)

def require(test,label):
    if not test:raise RuntimeError(label)

class M:
    """Positive c*eta**e*delta**g; e may be an exact half-integer."""
    def __init__(self,c=1,e=0,g=0):self.c,self.e,self.g=F(c),F(e),int(g)
    def __mul__(self,other):
        if not isinstance(other,M):other=M(other)
        return M(self.c*other.c,self.e+other.e,self.g+other.g)
    __rmul__=__mul__
    def __truediv__(self,other):
        if not isinstance(other,M):other=M(other)
        return M(self.c/other.c,self.e-other.e,self.g-other.g)
    def __pow__(self,k):return M(self.c**k,self.e*k,self.g*k)
    def same(self,other):return (self.c,self.e,self.g)==(other.c,other.e,other.g)
    def record(self):return {'coefficient':str(self.c),'eta_power':str(self.e),'delta_power':self.g}

def input_data():
    r=radial_certificate();values,_,_,_,_=exact();c=embedding()
    limit=[enclose(v,c) for v in values]
    box=[v+I.bounds(-F(1,1024),F(1,1024)) for v in limit]
    return r,box,limit,c

def budgets(r,box,limit,c,damage=None):
    rho=F(1,64) if damage!='raw-domain' else F(1,2)
    eps0=F(1,32) if damage!='epsilon-domain' else F(1,8)
    rr=F(1,16) if damage!='root-disks' else F(1,2)
    nvars=16 if damage!='cauchy-dimension' else 1
    inverse=2**10 if damage!='normalized-inverse' else 1
    e1bound=17 if damage!='first-coefficient' else 1
    pmargin=128 if damage!='polynomial-majorant' else 64
    mu_floor=F(9,32) if damage!='radial-margin' else F(3,10)
    coeff_den=2**7 if damage!='coefficient-rouche' else 32
    free_norm=4 if damage!='free-metric' else 2
    checks=[]
    def scalar(test,label):require(test,label);checks.append(label)
    def covered(m,label,upper=1,strict=False):
        scalar(m.c>=0 and m.e>=0 and m.g>=0 and (2*m.e).denominator==1,label+' nonnegative half-integer eta/delta exponents')
        value=m.c*F(1,256)**int(2*m.e)*F(1,2)**m.g
        scalar(value<upper if strict else value<=upper,label+' whole eta/delta bound')
        return str(value)

    scalar(nvars==12+4,'all sixteen parameters/targets retained')
    scalar(all(max(abs(F(v[0])),abs(F(v[1])))<1 for rows in (r['even_radial_div_eta'],r['odd_radial_div_eta3half_sine']) for row in rows for v in row),'all eight Jacobian entries below one')
    scalar(F(r['even_determinant'][0])>F(1,16),'even determinant input')
    scalar(F(r['odd_determinant'][1])<-F(1,100),'odd determinant input')
    scalar(all(F(v[0])>F(1,4) for v in r['upper_root_sines']),'both sine inputs')
    scalar(all(F(v[0])>mu_floor for v in r['individual_root_multipliers']),'individual actual half-normal gradient margins')
    scalar(all(v.lo>I(-1).hi and v.hi<I(1).lo for v in limit[:2]),'both limiting real centers below one')
    scalar(limit[2].lo>I(1).hi and limit[2].hi<I(F(3,2)).lo,'limiting opening between one and three-halves')
    scalar((1-c*c).lo>I(F(1,16)).hi,'ninth-root separation above one-half')
    scalar(all(v.lo>I(-2).hi and v.hi<I(2).lo for v in box[:2]),'both actual branch centers below two')
    scalar(box[2].lo>I(1).hi and box[2].hi<I(2).lo,'actual opening between one and two')
    scalar((6*box[0]+2*box[1]).hi<I(-1).lo,'nonzero branch coefficient for uncovered benchmark')
    scalar((2*c*c-1).lo>I(0).hi,'positive first ninth-root cosine for uncovered benchmark')
    scalar(4*E*E+2*E<F(1,1024),'all actual branch critical moduli below one thirty-second')
    scalar(F(2)/F(1,16)==32 and F(2)/F(1,100)*4==800,'normalized inverse row bounds')
    scalar(800<inverse,'eta-independent normalized inverse bound')

    ec=eps0**2
    scalar(rho+16*rho*rho<2*rho and 2*rho<F(1,2),'nonvanishing complex heavy radicand')
    scalar(F(3,2)+rho+16*rho*rho<F(9,4),'complex heavy square root below three-halves')
    scalar(F(1)-rho-16*rho*rho>F(1,4),'complex inverse opening below two')
    scalar(1+rho+rho*(1+14*(1+rho))<2,'complex heavy real coordinates below two')
    scalar(4*rho+F(3,2)<2,'complex heavy imaginary coordinates below two')
    l=2*eps0+rho;h=2*eps0+2
    scalar(l==F(5,64) and h==F(33,16),'six-small two-heavy epsilon majorants')
    scalar(8*(1+rho)+eps0*rho<e1bound,'cancelled first elementary coefficient')
    G={k:sum((F(comb(2,i)*comb(6,k-i))*h**i*l**(k-i) for i in range(3) if 0<=k-i<=6),F(0)) for k in range(2,9)}
    a=1+ec;z=1+rr
    P=9*a**8+F(9,8)*e1bound*(z**8+a**8)+sum((F(9,9-k)*G[k]*eps0**(k-2)*(z**(9-k)+a**(9-k)) for k in range(2,9)),F(0))
    root_floor=9*rr-36*(1+rr)**7*rr*rr
    scalar(P<pmargin,'complete anchored polynomial epsilon-square majorant')
    scalar(pmargin*ec<F(1,4),'polynomial perturbation below quarter')
    scalar(root_floor>F(1,4),'all nine fixed ninth-root Rouche circles')
    scalar(2*rr<F(1,2),'nine original-root disks disjoint')
    scalar(((1+rr)**2+1)/2<2,'companion half-normal modulus below two')
    scalar(2/eps0**2==2**11 and 2/eps0**3==2**16,'removable even/odd divided normal majorants')
    scalar(10*ec+9*ec*ec<F(1,2),'all eight reciprocal square-root domains')
    scalar(8*2<32,'joint holomorphic objective bound')
    cc=K((0,1,0));mu0=[K((F(26,9),-F(2,9),-F(4,9))),K((-F(1,3),F(2,3),0))]
    if damage=='deflation-dual':mu0[0]+=F(1,1000)
    ts=[K(-F(1,2)),-cc]
    scalar(-2*sum((mu0[j]*(ts[j]-1)/8 for j in range(2)),K(0))==1,'universal first objective U coefficient cancellation')
    scalar(-2*sum((mu0[j]*(1-ts[j]*ts[j])/7 for j in range(2)),K(0))==-F(1,2),'universal first objective H coefficient cancellation')
    C0=8-2*sum(mu0,K(0));mum=[enclose(v,c) for v in mu0];cv=enclose(C0,c)
    scalar(all(v.lo>I(0).hi for v in mum) and sum((v.hi for v in mum),0)<I(4).lo,'positive limiting duals with sum below four')
    scalar(cv.lo>I(0).hi and cv.hi<I(8).lo,'limiting first coefficient between zero and eight')
    scalar(32+8+ec*(8+2*4*2**11)<64,'joint deflated numerator modulus bound')
    Gbound=2**26 if damage!='deflated-majorant' else 2**20
    scalar(F(64)/ec**2==Gbound,'removable raw objective deflation majorant')
    scalar(19*E<rho/4,'whole actual branch in inner quarter raw domain')
    scalar(F(1,2)-5*rho>F(1,4),'real heavy center remains separated from six small coordinates')

    B1=M(2**27);B2=M(2**39);L=M(inverse)
    scalar(2**16*(2*nvars/rho)==B1.c,'normalized first Cauchy operator bound')
    scalar(factorial(2)*2**16*(2*nvars/rho)**2==B2.c,'normalized second Cauchy operator bound')
    s=M(1)/(8*L*B2);d=M(1)/(64*L**2*B1*B2)
    scalar(s.same(M(F(1,2**52))) and d.same(M(F(1,2**92))),'eta-independent tail and complete target radii')
    covered(s/M(rho/4),'complete tail ball in inner complex domain',strict=True)
    covered(d/s,'free and normal targets inside raw tail ball',strict=True)
    scalar((L*B2*s).same(M(F(1,8))),'whole off-branch tail Jacobian contraction')
    scalar((L*M(B1.c+1)*d/s).c<F(1,4),'contraction center displacement')
    scalar(2*B1.c*s.c<F(1,8),'all inactive-root actual half-normal variations divided by eta')
    K2=M(2**37)/d**2;K3=M(2**44)/d**3
    scalar(factorial(2)*Gbound*(2*nvars)**2==2**37,'completely eliminated deflated second Cauchy bound')
    scalar(factorial(3)*Gbound*(2*nvars)**3<2**44,'completely eliminated deflated third Cauchy bound')
    b=d**2/(2**43);R=M(1,0,1)*d**3/(2**44);t=R/4
    scalar(R.same(M(F(1,2**320),0,1)) and t.same(M(F(1,2**322),0,1)),'eta-independent explicit kappa raw-radius identities')
    covered(b/(d/2),'normalized stability box in Cauchy inner domain',strict=True)
    covered(R/b,'free Euclidean ball inside normalized stability box',strict=True)
    scalar((K2*b).same(M(F(1,64))),'each actual individual radial gradient variation')
    scalar(mu_floor-F(1,64)>=F(17,64)>F(1,4),'signed feasible individual-root integration')
    scalar((K3*R/M(1,0,1)).same(M(1)),'zero-slack deflated Taylor budget')
    scalar(free_norm**2>12,'literal twelve-coordinate Euclidean metric')
    scalar(t.same(R/free_norm),'raw box implies free Euclidean radius')
    covered(B1*t/b,'raw box implies normalized four-normal stability box',strict=True)
    covered(t/s,'raw heavy tail in complete uniqueness ball',strict=True)
    ccrit=M(1,2)*t/(2**10);ccoef=M(1,1)*ccrit**6/coeff_den
    target=M(F(1,2**1999),13,6)
    if damage=='coefficient-radius-exponent':target=M(F(1,2**1999),14,6)
    scalar(ccoef.same(target),'improved coefficient radius exponent identity')
    covered(ccoef/M(F(1,2),1),'uncovered benchmark lies outside coefficient entry',strict=True)
    covered(ccrit/M(F(1,4),1),'all critical-entry circles smaller than eta over four',strict=True)
    scalar(F(1,1024)<F(9,64),'heavy critical Rouche comparison after eta deflation')
    scalar(F(36,coeff_den)<1,'coefficient perturbation counts all eight criticals')
    scalar(5<1024 and 8<1024 and 40<1024,'heavy T V M recovery in raw neighborhood')
    scalar(F(1,4)-F(33,16)*E>F(1,8),'quarter-curvature gap')
    scalar(2**1999*8**6==2**2017,'quarter-curvature coefficient-ball constant')
    covered(M(2**126,12),'new coefficient radius strictly exceeds published eta25 intermediate',strict=True)
    scalar(8*70**2<200**2,'eight-unmarked original energy to coefficient norm')
    scalar(sum((F(9,9-k)*comb(7,k-1) for k in range(1,9)),F(0))==F(2295,8),'anchored critical energy constant sum')
    scalar(3*F(2295,8)<1024,'branch-matched critical energy to coefficient norm')
    if damage=='negative-eta-comparison':covered(M(1,-1),'invalid whole-window comparison')
    return {'schema':'six-sendov-3-normalized-neighborhood-v1','actual_agent':'six-sendov-3','role':'researcher',
        'eta_interval':['0 exclusive',str(E)],'coefficient_range':'0<=k<1/2-33eta/16','delta_definition':'1/2-33eta/16-k',
        'raw_dimension':16,'free_metric_dimension':12,'normal_coordinates':'beta half-sum/eta; gamma half-difference/eta^(3/2)',
        'radial_input_record_sha256':sha256(json.dumps(r,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'complex_epsilon_radius':str(eps0),'complex_eta_radius':str(ec),'raw_complex_radius':str(rho),'fixed_original_root_disk_radius':str(rr),
        'elementary_epsilon_majorants':{str(k):str(v) for k,v in G.items()},'polynomial_epsilon_square_majorant':str(P),'root_circle_lower_bound':str(root_floor),
        'beta_modulus_bound':2**11,'gamma_modulus_bound':2**16,'normalized_first_derivative_bound':B1.record(),'normalized_second_derivative_bound':B2.record(),
        'normalized_tail_inverse_majorant':L.record(),'tail_ball':s.record(),'full_target_polydisk':d.record(),
        'normalized_stability_box':b.record(),'free_Euclidean_ball':R.record(),'all_feasible_raw_box':t.record(),
        'critical_entry_disks':ccrit.record(),'all_feasible_coefficient_ball':ccoef.record(),
        'quarter_curvature_coefficient_ball':M(F(1,2**2017),13).record(),
        'limiting_duals':[v.record() for v in mu0],'limiting_first_objective_coefficient':C0.record(),'raw_and_eliminated_deflated_objective_bound':Gbound,
        'eliminated_second_derivative_majorant':K2.record(),'eliminated_third_derivative_majorant':K3.record(),
        'certified_slack_coefficient':'17/64','stated_slack_coefficient':'1/4','checks':checks,
        'coverage':'whole positive eta and explicit positive kappa gap; fixed complex joint root/normalized normal domain includes eta0',
        'proof_trust_boundary':'ordinary root continuation/divisibility/Cauchy/contraction/Rouche/Taylor proof remains unformalized'}

DAMAGES=('deflation-dual','deflated-majorant','raw-domain','epsilon-domain','root-disks','cauchy-dimension','normalized-inverse',
    'first-coefficient','polynomial-majorant','radial-margin','coefficient-rouche','free-metric',
    'coefficient-radius-exponent','negative-eta-comparison')

def build():
    inputs=input_data();out=budgets(*inputs);rejected=[]
    for name in DAMAGES:
        try:budgets(*inputs,damage=name)
        except RuntimeError:rejected.append(name)
    require(rejected==list(DAMAGES),'all mathematical damaged budgets reject')
    out['mathematical_damage_rejections']=rejected
    return out
