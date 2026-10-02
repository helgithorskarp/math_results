"""Independent exact quadratic feedback audit. Ordinary analytic bridges in PROOF.md."""
import json, hashlib, math, sys
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parent))
from polys import Poly, cast, symbol, need
from cosine import C,c,d,x,y,w3,w4,chebyshev


def conj(p):return p.conjugate_coefficients()
def real(p):return (p+conj(p))/2
def imag(p):return (p-conj(p))*cast((0,F(-1,2)))
def norm(p):return p*conj(p)
def phase_reduce(p):return p.reduce_square('h',1-symbol('p')**2)
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()
def strict_json(path):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('duplicate JSON key')
            out[k]=v
        return out
    return json.loads(Path(path).read_text(),object_pairs_hook=pairs)
def poly_digest(p):
    b=canonical(p.record());return {'terms':len(p.terms),'sha256':hashlib.sha256(b).hexdigest()}


def symbolic():
    identities={}
    def eq(name,a,b,phase=False):
        if phase:a,b=phase_reduce(a),phase_reduce(b)
        need(a==b,'whole polynomial identity: '+name)
        identities[name]={'left':poly_digest(a),'right':poly_digest(b)}
    X,Y=symbol('X'),symbol('Y');R=X*X+Y*Y
    eq('signed_reciprocal_cubic_square',F(9,4)*X*X*R*R-(X**3-F(3,2)*X*Y*Y)**2,F(5,4)*X**6+F(15,2)*X**4*Y**2)
    eq('signed_third_moment_square',9*X*X*R*R-(X**3-3*X*Y*Y)**2,8*X**6+24*X**4*Y**2)
    z=[symbol('x'+str(j))+cast((0,1))*symbol('y'+str(j)) for j in range(7)]
    z.append(-sum(z,cast(0)))
    need(len(z)==8,'all eight centered multiplicities')
    V=sum((norm(t) for t in z),cast(0));S4=sum((norm(t)**2 for t in z),cast(0))
    rhs=cast(0)
    for j in range(8):
        others=[k for k in range(8) if k!=j]
        pairdiff=sum((norm(z[k]-z[l]) for n,k in enumerate(others) for l in others[n+1:]),cast(0))
        eq('centered_other_seven_'+str(j),7*V-8*norm(z[j]),pairdiff)
        rhs+=norm(z[j])*pairdiff
    eq('full_centered_quartic_SOS',7*V*V-8*S4,rhs)
    fourth_factor=F(7,8)
    eq('quartic_majorant_coefficient',cast(fourth_factor)*8,cast(7))
    T=sum((t*t for t in z),cast(0));U=sum((t**3 for t in z),cast(0))
    e2=sum((z[j]*z[k] for j in range(8) for k in range(j+1,8)),cast(0))
    e3=sum((z[j]*z[k]*z[l] for j in range(8) for k in range(j+1,8) for l in range(k+1,8)),cast(0))
    eq('all_eight_Newton_e2',2*e2,-T);eq('all_eight_Newton_e3',3*e3,U)
    eq('centered_integrated_d7',F(9,7)*e2,-F(9,14)*T)
    eq('centered_integrated_d6',-F(3,2)*e3,-U/2)
    # Rotation is tested on independent physical X/Y symbols; the zero-sum
    # constraint is not needed for its algebraic identities.
    xs=[symbol('a'+str(j)) for j in range(8)];ys=[symbol('b'+str(j)) for j in range(8)]
    p,h=symbol('p'),symbol('h');unit=p+cast((0,1))*h
    original=[(a+cast((0,1))*b)*unit for a,b in zip(xs,ys)]
    xi=[t*conj(unit) for t in original]
    vr=sum((norm(t) for t in original),cast(0));tr=sum((t*t for t in original),cast(0));ur=sum((t**3 for t in original),cast(0))
    QJ=tr*conj(unit)**2;E=sum((a*a for a in xs),cast(0))
    eq('rotated_real_energy',2*E,vr+real(QJ),True)
    eq('rotated_cubic_all_phases',ur*conj(unit)**3,sum((t**3 for t in xi),cast(0)),True)
    q=sum((a*a-b*b for a,b in zip(xs,ys)),cast(0));j=sum((2*a*b for a,b in zip(xs,ys)),cast(0));vv=sum((a*a+b*b for a,b in zip(xs,ys)),cast(0))
    gram=4*sum(((xs[k]*ys[l]-xs[l]*ys[k])**2 for k in range(8) for l in range(k+1,8)),cast(0))
    eq('whole_eight_Gram',vv*vv-q*q-j*j,gram)
    A=[symbol('A'+str(j)) for j in range(8)];B=[symbol('B'+str(j)) for j in range(8)]
    eq('whole_Cauchy_Lagrange',sum((a*a for a in A),cast(0))*sum((b*b for b in B),cast(0))-sum((a*b for a,b in zip(A,B)),cast(0))**2,sum(((A[k]*B[l]-A[l]*B[k])**2 for k in range(8) for l in range(k+1,8)),cast(0)))
    t,K,v=symbol('t'),symbol('K'),symbol('v')
    eq('physical_square_completion',t*t/4-K*v*t,(t/2-K*v)**2-K*K*v*v)
    eq('objective_absorption_identity',t*t/2-K*v*t+K*K*v*v/2,(t-K*v)**2/2)
    return identities


def field_records():
    out={}
    def eq(name,a,b):
        need(a==b,'whole cosine-field identity: '+name);out[name]=a.record()
    eq('selected_cubic',8*c**3-6*c-1,C(0))
    eq('dual_A',w3*C(F(3,2))+w4*(1+c),C(8))
    eq('dual_B',w3*C(F(3,2))+w4*(1-d),C(7))
    eq('dual_C',8-w3-w4,C(F(8,3))+y)
    eq('profile_cube',C(F(3,2))*(x+y),C(1))
    eq('profile_four',(1+c)*x+(1-d)*y,C(1))
    eq('determinant',C(F(3,2))*(1-d)-(1+c)*C(F(3,2)),-F(3,2)*(c+d))
    eq('weight_monotonic_form',w3,2*(16*c-9)/(3*(2*c-1)))
    phases=[]
    for k in range(9):
        A=1-chebyshev(2*k);B=1-chebyshev(4*k);cubic=(chebyshev(6*k)-1)/18
        need(chebyshev(18+k)==chebyshev(k),'all ninth-root phases retained')
        phases.append({'k':k,'A':A.record(),'B':B.record(),'paired_cubic_coefficient':cubic.record()})
    need(C(phases[3]['paired_cubic_coefficient'])==0,'actual cube cubic cancels')
    need(C(phases[4]['paired_cubic_coefficient'])==F(-1,12),'actual fourth cubic retained')
    need(F(3,2)*(F(15,16)+2*F(15,16)**2-1)==F(651,256),'whole Cramer endpoint equality')
    need(2-2*F(15,16)**2==F(31,128),'whole B4 endpoint equality')
    need(1+F(47,50)==F(97,50),'whole A4 endpoint equality')
    out['strict_bounds_from_open_monotone_branch']={'determinant_lower_endpoint':'651/256','B4_upper_endpoint':'31/128','A4_upper_endpoint':'97/50','endpoint_equalities_not_strict':True}
    out['all_nine_physical_phase_rows']=phases
    return out


def ap(a,b):
    w=[F(0)]*max(len(a),len(b))
    for j,x in enumerate(a):w[j]+=x
    for j,x in enumerate(b):w[j]+=x
    while len(w)>1 and not w[-1]:w.pop()
    return w

def mul(a,b):
    w=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):w[i+j]+=x*y
    return ap(w,[])
def powp(a,n):
    w=[F(1)]
    for _ in range(n):w=mul(w,a)
    return w


def legendre():
    seq=[[F(1)],[F(0),F(1)]];out=[]
    for n in range(2,17):
        seq.append([v/n for v in ap([F(0)]+[(2*n-1)*v for v in seq[-1]],[-(n-1)*v for v in seq[-2]])])
    for n in range(17):
        rodrigues=[F(0)]*(n+1)
        for k in range(n//2+1):rodrigues[n-2*k]=F((-1)**k*math.factorial(2*n-2*k),2**n*math.factorial(k)*math.factorial(n-k)*math.factorial(n-2*k))
        laplace=[F(0)]
        for j in range(n//2+1):
            term=[F(0)]*(n-2*j)+[F((-1)**j*math.comb(n,2*j)*math.comb(2*j,j),4**j)]
            laplace=ap(laplace,mul(term,powp([F(1),F(0),F(-1)],j)))
        need(seq[n]==ap(rodrigues,[])==laplace,'entire Legendre coefficient map '+str(n))
        geo=[F(1)]*(n+1)
        need(mul([F(1),F(-1)],geo)==[F(1)]+[F(0)]*n+[F(-1)],'entire finite telescoping control')
        out.append({'degree':n,'whole_coefficients':list(map(str,seq[n]))})
    need(seq[3]==[F(0),F(-3,2),F(0),F(5,2)],'signed cubic Legendre coefficient')
    return out


def budgets():
    e=F(1,65536);a=1-e;G=1/((a-F(1,96))*a**4);K=F(3,2)/a**4+F(3,20)/a
    out={}
    def gap(name,left,right):
        left,right=F(left),F(right);need(left<right,'strict rational budget: '+name)
        out[name]={'left':str(left),'right':str(right),'margin':str(right-left)}
    cubic=lambda t:8*t**3-6*t-1
    gap('cosine_lower_sign',cubic(F(15,16)),0);gap('cosine_upper_sign',0,cubic(F(47,50)))
    gap('cosine_monotonicity',0,24*F(15,16)**2-6)
    gap('weight_w3_lower',4,F(2,3)*(7-(1-(2*F(15,16)**2-1))/(F(15,16)+2*F(15,16)**2-1)))
    gap('weight_w3_upper',2*(16*F(47,50)-9)/(3*(2*F(47,50)-1)),F(23,5))
    gap('weight_w4_lower',F(1,2),1/(F(47,50)+2*F(47,50)**2-1))
    gap('weight_w4_upper',1/(F(15,16)+2*F(15,16)**2-1),F(3,5))
    gap('tail_ratio',6*e,F(1,96)**2)
    gap('whole_radius_moment_conversion',(3-3*e+e*e)/a**3,4)
    need(1/(3*(1+F(15,16)))==F(16,93),'exact y endpoint equality; strict actual bound uses c>15/16')
    gap('local_energy_after_global_entry',64*e,F(1,512))
    gap('mean_radius_conversion',8*F(4,5)*(2-e)/a**2+4*F(169,225)/a**3+24,40)
    gap('whole_cube_noncubic',F(1,2)+F(3,2)*F(4,5)+F(3,2)*F(169,225)+F(13,15)+36,40)
    gap('whole_four_noncubic',F(1,2)+2*F(4,5)+2*F(169,225)+F(13,10)+F(9,8)*36,46)
    gap('normal_dual_cost',40+40*F(23,5)+46*F(3,5),252)
    gap('target_quadratic390',252+36*(G+K*K),390)
    gap('centered_objective327',252+F(63,2)*(G+K*K/2),327)
    gap('centered_physical370',252+F(63,2)*(G+K*K),370)
    gap('sharp_slope_lower',F(17,6),F(826,291))
    gap('new_uniform_slope17over6',F(17,6),F(826,291)-327*e)
    gap('target_uniform_slope14over5',F(14,5),F(17,6)-390*e)
    for b in [390,370]:
        gap(str(b)+'_sqrt_budget',19**2,b)
        gap(str(b)+'_R3',F(1,4)+F(40,b),F(3,8))
        gap(str(b)+'_R4',F(46,b)+3/(19*a),F(1,2))
        gap(str(b)+'_H',8*F(169,225)/b,1)
        gap(str(b)+'_physical_real_energy',(F(384,25)+4*e/a**2)/b,1)
        gap(str(b)+'_motion_Delta',F(26,5)+26/(7*a)+F(125,b),10)
        gap(str(b)+'_motion_sqrt',2+10/(7*a)+55/(684*a**2),4)
    gap('Cramer_M',F(62,651)*F(3,8)+F(128,217)*F(5,2),F(8,5))
    gap('Cramer_Q',F(24832,32550)*F(3,8)+F(128,217)*F(5,2),F(9,5))
    gap('Q26',14*F(9,5),26)
    gap('physical_D_sqrt_squared',96,196*a*a)
    gap('physical_D_linear',7/(24*a),1)
    gap('physical_D_eta2',259/(6*a),44)
    gap('centering_mu3_squared',F(7,8)*6**3,F(55,4)**2)
    gap('whole_motion_eta2',88+36+896/(1395*a),125)
    # Whole all-phase nonlinear normal and actual motion imports, independently
    # reconstructed from their written formulas rather than source execution.
    rho=F(1,64);v=F(1,512);rm=a-rho;rp=1+rho;s=rp+v/2
    A={j:F(9,8*j)*math.comb(8,9-j)*rho**(7-j) for j in range(1,7)};A[7]=F(9,14)
    Cd=sum(j*A[j]*s**(j-1) for j in A);N=2*sum(A[j]*rp**j for j in A)
    Bd=9*rm**8-18*s**7*v-Cd*v;Bn=s**7/(4*rm**8)+Cd/(36*rm**8)
    B={5:F(63,32),4:F(63,32)*rho,3:F(21,128)*v,2:F(9,128)*rho*v,1:F(9,4096)*v*v}
    gap('all_phase_root_quarter',N,Bd/4);gap('all_phase_linear_quarter',N,9*rm**8/4)
    gap('all_phase_nonlinear_normal',(1+2*rho)*Bn+F(1,32)+F(2,9)*sum(B[j]*rm**(j-7) for j in B),F(9,8))
    gap('all_nine_displacement_remainder',Bn+2/(9*a)*sum(B[j]*rm**(j-7) for j in B),1)
    return out


def record():
    return {'domain':{'degree':9,'critical_multiplicity_count':8,'closed_original_disk':True,'eta_max':'1/65536','low_sublevel_for_physical_stability':'F<=8+3eta','additional_near_slope_cut_for_moments':'F<=8+Ceta+epsilon*eta; epsilon>=0','original_label_count':9},'symbolic':symbolic(),'cosine_field':field_records(),'finite_Legendre_controls':legendre(),'rational_budgets':budgets(),'refinements':{'objective_quadratic':327,'physical_quadratic':370,'uniform_slope':'17/6','stability_Delta':'epsilon*eta+370*eta^2','actual_original_error':'10*Delta+4*sqrt(eta*Delta)','centered_fourth_factor':'7/8','ordinary_unformalized':True,'imported_actual_entry_and_counted_roots':True}}

if __name__=='__main__':
    emit=len(sys.argv)==2 and sys.argv[1]=='--emit'
    if not emit:
        need(len(sys.argv)<=2,'only optional external fixture path')
        expected=strict_json(sys.argv[1] if len(sys.argv)==2 else Path(__file__).with_name('EXPECTED.json'))
    r=record();raw=canonical(r)
    if emit:print(json.dumps(r,sort_keys=True,separators=(',',':')))
    else:
        need(type(expected)==dict and canonical(expected)==raw,'entire typed independent mathematical record')
        print(json.dumps({'record_sha256':hashlib.sha256(raw).hexdigest(),'record_bytes':len(raw),'whole_polynomial_identities':len(r['symbolic']),'strict_rational_budgets':len(r['rational_budgets']),'Legendre_degrees':len(r['finite_Legendre_controls']),'original_labels':9,'refinements':r['refinements']},sort_keys=True))
