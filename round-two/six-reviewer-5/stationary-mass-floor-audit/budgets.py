"""Independent exact closed-domain inequalities; stdlib only, no fixtures.

Each ratio is nonnegative sum c e^a M^b, e <= M^-40, M >=100.
Termwise substitution and monotonicity prove the whole supremum bound.
"""
from fractions import Fraction as F
import json,sys

def need(ok,label):
    if not ok:raise ValueError(label)
def powq(q,n):return F(q)**n
rows=[]
def bound(name,terms,strict=False):
    s=F(0);encoded=[]
    for c,a,b in terms:
        c=F(c);need(c>=0 and a>=0 and b-40*a<=0,name+': lawful monotonic domain')
        s+=c*powq(100,b-40*a);encoded.append([str(c),a,b])
    if '--damage' in sys.argv and name=='resonance residual':s+=1
    need(s<1 if strict else s<=1,name+': whole ratio <=1')
    rows.append(dict(name=name,ratio_terms=encoded,maximum=str(s),strict=strict))
bound('small cubic square',[(F(2,3),18,-178),(F(2,3),0,-2)])
bound('quadratic residual',[(1,20,-198),(1,2,-22),(1,0,-1)])
bound('even residual',[(1,0,-9),(F(4,3),0,-1)])
bound('B zero projection',[(1,0,-9),(F(1,3),0,-1)])
bound('F zero projection',[(1,0,-9),(F(1,5),0,-1)])
bound('small odd B',[(F(1,3),1,7)])
bound('small odd F',[(F(1,5),1,16)])
bound('small odd J',[(F(1,7),0,-3)])
bound('resonance collar size',[(1,1,28)])
bound('resonance residual',[(1,1,-30),(1,0,-1)])
bound('large cubic residual',[(1,4,-41),(1,0,-1)])
bound('large affine distance',[(F(3,5),0,-1)])
bound('large affine residual',[(1,4,-42),(1,0,-1)])
bound('undivided odd factor',[(F(5,3),0,-1),(F(1,12),0,0)])
bound('large odd F estimate',[(F(1,25),0,-1),(F(1,25),5,-36)])
bound('large odd J estimate',[(F(1,21),4,-36),(F(1,21),0,-1),(F(1,21),9,-71)])
bound('large odd B',[(1,8,-84)])
bound('large odd F',[(1,4,-49)])
bound('large odd J',[(1,0,-14)])
bound('exceptional closed collar residual',[(1,13,-126),(3,0,-1)])
bound('exceptional collar heat error',[(F(15,28),1,9)],True)
bound('quadratic residual at most one',[(1,2,-2)])
bound('raw and projected Lipschitz',[(10000,0,-2)])
bound('large cubic pivot',[(F(4,7),0,0)])
scalars={
 'new e to actual odd margin':F(184,15)*F(10)**-24,
 'new resonance distance to six-root margin':F(3125,72900),
 'excluded first quadratic interval to C lower with error':F(-91,50)+1-F(29,7),
 'excluded second quadratic interval to C lower with error':F(-3,2)+1-F(29,7),
 'exceptional heat gap with error':F(-1048,203)+1-F(29,7),
 'pairwise squared-gap norm factor':F(sum(k*k*(8-k) for k in range(1,8)),8),
 'sufficient nonresonant B coefficient':F(35,100),
 'gradient coarse threshold':F(10000,100**2),
}
need(0<scalars['new e to actual odd margin']<1,'new odd margin strict')
need(0<scalars['new resonance distance to six-root margin']<1,'new sextic margin strict')
for k in ('excluded first quadratic interval to C lower with error','excluded second quadratic interval to C lower with error','exceptional heat gap with error'):need(scalars[k]<0,k)
need(scalars['pairwise squared-gap norm factor']==42,'feasible delta squared <=1/42')
a=F(1,6716343447408);c=a*a/(3*2**9*F(1,10**13)*14913669297722925580854623*1814727936*16583*(1+F(180,83)/a))
need(F(1,10**68)<=c<=min(a,F(83,180)*a),'credited9994 c retained constant')
exponents=dict(M=6,e_M=40,p5_M=22*40+208,p5_decimal=2*(22*40+208),p5_delta=6*(22*40+208),moment_decimal=136+190*2*(22*40+208),moment_delta=190*(6*(22*40+208)+6))
need(exponents==dict(M=6,e_M=40,p5_M=1088,p5_decimal=2176,p5_delta=6528,moment_decimal=413576,moment_delta=1241460),'all displayed exponents')
print(json.dumps(dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',domain='M>=100; 0<e<=M^-40; then M=100 delta^-6,e=M^-40,0<delta<=1',ratios=rows,scalar_comparisons={k:str(v) for k,v in scalars.items()},retained_credited9994_c=str(c),exponents=exponents),sort_keys=True,separators=(',',':')))
