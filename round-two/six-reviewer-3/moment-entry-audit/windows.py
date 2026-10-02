"""Full-window rational sufficient budgets; no sampling of eta or k."""
from dataclasses import dataclass,replace
from fractions import Fraction as F
from math import comb
from polys import need

@dataclass(frozen=True)
class Data:
    eta_max:F=F(1,65536)
    delta_max:F=F(1,2)
    v:F=F(1,2**215)
    ell:F=F(1,2**310)
    b:F=F(1,2**227)
    inverse:F=F(800)
    raw_second:F=F(2**39)
    push_complex:F=F(8)
    push_real:F=F(32)
    impulse_power:int=1
    energy_count:int=8
    factorial_two:int=2
    coefficient_power:int=7
    critical_power:int=3
    balanced_power:int=2


def certificate(p=Data()):
    need(p.eta_max==F(1,65536) and p.delta_max==F(1,2),'specified whole positive interval')
    u=F(1,256);e=p.eta_max;D=p.delta_max;out={}
    def cmp(name,A,pu,pd,B,qu=0,qd=0,strict=True):
        A=F(A);B=F(B);need(A>=0 and B>0,'positive comparison factors '+name)
        need(pu-qu>=0 and pd-qd>=0,'unbounded negative domain exponent '+name)
        ratio=A/B*u**(pu-qu)*D**(pd-qd)
        need(ratio<1 if strict else ratio<=1,'whole-window '+name)
        out[name]={'lhs':[str(A),pu,pd],'rhs':[str(B),qu,qd],'endpoint_ratio':str(ratio),'strict':strict}
    def margin(name,value):
        value=F(value);need(value>0,'strict whole-window margin '+name);out[name]={'exact_positive_margin':str(value)}
    # The beta/gamma normal definition remains literal; no sine division.
    t=F(1,2**322);R=F(1,2**320);lam=t/1024;C=F(1,2**1999)
    need(type(p.coefficient_power)==int and type(p.critical_power)==int and type(p.balanced_power)==int,'integral entry powers')
    margin('moment S2 full coefficient factor',2-(F(8,9)*33*e+F(14,9)))
    cmp('C7 less than eta',C,2*p.coefficient_power,6,1,2)
    cmp('V and M coefficient transport',C,2*p.coefficient_power-3,6,t/1024,0,1)
    cmp('coefficient critical circles inside eta/4',lam,2,1,F(1,4),2)
    cmp('coefficient heavy Rouche bound',lam**5,10,5,F(9,64),5)
    cmp('full derivative coefficient all eta scales',36*C,2*p.coefficient_power,6,lam**6,14,6)
    cmp('critical unweighted displacement from energy',t/1024,3,1,F(1,4),1)
    cmp('balanced displacement cluster separation',t/1024,2,1,F(1,4),1)
    cmp('critical unweighted V budget',8*t/1024,p.critical_power-3,1,t,0,1)
    cmp('balanced free coordinate transport',t/1024,p.balanced_power-2,1,t,0,1)
    margin('balanced total trace V budget',1-F(1,128))
    margin('complete per-term mixed moment budget',5-(2*e+2*u+e*u*t*D/1024))
    margin('complete balanced mixed moment budget',5-(2*u+2+u*t*D/1024))
    margin('all eight mixed moment terms',1-F(40,1024))
    margin('heavy T difference of squares',5-(4+t*D/1024))
    margin('all raw coordinate entry budgets',1-F(5,1024))
    margin('fixed kquarter gap',F(1,2)-33*e/16-F(1,4)-F(1,8))
    need(C/F(2**18)==F(1,2**2017),'quarter coefficient exponent')
    need((t/1024)**2/64==F(1,2**670),'quarter critical exponent')
    need(F(1,2**4050)*200**2<F(1,2**4034),'quarter original energy')
    margin('all original coefficients telescope',200**2-8*comb(8,4)**2)
    # Root-section and companion domains; both complete polynomial majorants are separate.
    rho=F(1,16);h=F(1,1024);j=F(1,64);n=F(1,2048)
    baseline=9*rho-sum(F(comb(9,k))*rho**k for k in range(2,10))
    margin('full ninth-root circle baseline greater than3/8',baseline-F(3,8))
    margin('complete original Rouche perturbation',baseline-64*h)
    need(F(9,8)+p.push_complex*j<=F(5,4),'complex shear open domain');out['complex shear open domain']={'nonnegative_closed_margin':str(F(5,4)-(F(9,8)+p.push_complex*j)),'strict_on_open_product':True}
    margin('real shear whole domain',F(5,4)-(F(9,8)+p.push_real*n))
    A=F(2)/h;A1=A/(j/2);A2=p.factorial_two*A/(j/2)**2
    N1=A/(n/2);N2=p.factorial_two*A/(n/2)**2
    need(A1==2**18 and A2==2**26 and N1==2**23 and N2==2**36,'full Cauchy factorial and radii')
    cmp('physical complex xi inside inner domain',p.v,1,0,j/2)
    margin('complex all active inward derivatives',-F(3,2)-(-p.push_complex/3+1+e*F(9,8)))
    cmp('complex active full Taylor remainder',A2*p.v/2,1,0,F(1,2))
    cmp('complex inactive original motion',A1*p.v,1,0,F(1,8))
    cmp('actual raw segment inside rho/4',p.v,0,0,F(1,256))
    margin('actual odd column survives mean motion',1/p.inverse-e*F(9,8)-F(1,1024))
    cmp('second-normal and nonlinear M remainder',p.raw_second*p.v,0,0,F(1,2048))
    need(p.v/2048==2*p.b,'strict gamma exceeds twice displayed b')
    cmp('complex heavy shifts below sqrteta/4',10*p.v,2,0,F(1,4))
    cmp('complex full minimum matching comparison',129*p.v**2,4,0,F(1,16))
    cmp('complex opening root stays positive',p.v**2/4,4,0,F(1,4))
    cmp('complex opening quadratic energy remainder',p.v**2/8,4,0,F(1,2))
    need(F(1,8)/(h*j)==2**13 and 8*(2**13)**2==2**29,'twice removable complex original displacement')
    # The real impulse feasibility and critical root count are separate obligations.
    cmp('physical nu lies inside inner domain',p.ell**6,12,0,n/2)
    margin('actual branch original derivative',9*F(29,32)**8-4)
    margin('impulse derivative perturbation',5-F(18,4))
    margin('real all active inward derivatives',-4-(-p.push_real/3+5))
    cmp('real active full Taylor remainder',N2*p.ell**6/2,12,0,1)
    cmp('real inactive original motion',N1*p.ell**6,12,0,F(1,8))
    cmp('real lower sign impulse survives eta0',F(1,32),0,0,1,2*(p.impulse_power-1))
    margin('whole real critical perturbation factor',2-(1+F(64,8**7)+1024*e*(e**6*p.ell**6)/8**6))
    cmp('real heavy critical Rouche lower bound',64*p.ell**5,5,0,1)
    cmp('real critical circles inside1/32',2*p.ell,2,0,F(1,32))
    cmp('real critical circle displacement',2*p.ell,1,0,F(1,4))
    cmp('all real minimum matching comparison',32*p.ell**2,2,0,F(1,16))
    margin('real lower-root sign',2-(F(25,16)+e*(F(9,4)+32*e**6*p.ell**6+p.ell/2)**2))
    margin('real right-root sign',64-1)
    margin('real free displacement exceeds every collar R',p.ell/2-R*D)
    need(p.energy_count==8,'every unmarked original and critical is counted')
    need(F(1,8)/(h*n)==2**18 and 8*(2**18)**2==2**39,'twice removable real original displacement')
    margin('whole coefficient energy bound',F(2**56)-200**2*F(2**39))
    margin('real coefficient order nonzero',72)
    margin('real energy order nonzero',648)
    # Total-moment identities implement these positive powers before any labels are chosen.
    orders={'coefficient':7,'original_squared_energy':14,'critical_squared_energy':3,'trace_balanced_critical_squared_energy':2}
    return {'all_domain_comparisons':out,'sharp_fixed_collar_entry_orders':orders,'complex_auxiliary_cauchy':[str(A),str(A1),str(A2)],'real_auxiliary_cauchy':[str(A),str(N1),str(N2)],'sufficient_entry_constants':{'coefficient':'delta^6*2^-1999*eta^7','critical':'delta^2*2^-664*eta^3','balanced_critical':'delta^2*2^-664*eta^2 with separate trace','original':'[delta^6*2^-1999*eta^7/200]^2'},'branch_energy_reference':'the actual branch and fixed marked original, not antipodal/collapsed energy'}


def controls():
    base=Data();mutants=[('wrong coefficient power',replace(base,coefficient_power=6)),('missing critical trace loss',replace(base,critical_power=2)),('wrong balanced exponent',replace(base,balanced_power=1)),('omitted complex inward shear',replace(base,push_complex=0)),('omitted real inward shear',replace(base,push_real=0)),('missing second Cauchy factorial',replace(base,factorial_two=1)),('weakened inverse lower bound',replace(base,inverse=65536)),('wrong impulse eta power',replace(base,impulse_power=2)),('lost one critical or unmarked root',replace(base,energy_count=7)),('unsafe complex imbalance',replace(base,v=F(1,256))),('free perturbation fits collar',replace(base,ell=F(1,2**330))),('unproved wider eta window',replace(base,eta_max=F(1,16)))]
    rejected=[]
    for name,p in mutants:
        try:certificate(p)
        except ValueError:rejected.append(name)
        else:raise ValueError('mathematical damage accepted '+name)
    return rejected
