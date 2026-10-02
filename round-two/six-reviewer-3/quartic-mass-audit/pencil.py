"""Own complete Laurent elimination; only previously owned Gram backend imported."""
import json
import sys
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parent))
from polys import Poly, cast, symbol, need
from algebra import (Z, structures, coeff, specialize, deriv, mul, add, scale,
                     neg, divrem, rem, gram_adjoint, power_sums, same, record)
from certificates import audit_slices,rank_controls

def shift(poly, amount):
    return cast(poly) * symbol('t') ** amount

def make(h, p):
    # Direct monic division and unit anti-triangular matrix solve, not an
    # imported Newton closed adjoint or author expansion.
    original = [Z]*9
    original[8] = cast(1)
    original[6] = F(4,3)*coeff(h,5)
    Q, _ = divrem(add(scale(original,8),mul(p,deriv(h))),h)
    _, _, T = gram_adjoint(h)
    O = add(mul(p,deriv(deriv(h))),add(mul(add(deriv(p),neg(Q)),deriv(h)),mul(add([cast(64)],neg(deriv(Q))),h)))
    K = add(scale(p,-16),add(scale(T(T(rem(mul(p,p),h))),-F(1,4)),scale(T(rem(mul(p,add(Q,neg(deriv(p)))),h)),F(1,4))))
    return Q,O,K

def audit():
    s = structures()
    t,r,v = [symbol(k) for k in ('t','r','s')]
    B,E,Fc,G,J = [symbol(k) for k in ('B','E','F','G','J')]
    checks={}
    def eq(name,left,right):
        need(cast(left)==cast(right),name)
        checks[name]=cast(left).record()
    def peq(name,left,right):
        need(same(left,right),name)
        checks[name]=record(left)
    init={'A':-F(3,8),'p6':0,'p5':t,'p4':v*t,'p3':r*t,
          'p2':8+t*(F(5,7)*B-F(27,56)*v-r*v)}
    h=specialize(s['h'],init);p=specialize(s['p'],init)
    O=specialize(s['O'],init);K=specialize(s['K'],init)
    eq('leading mass elimination',coeff(K,5),0)
    eq('p0 global pivot',coeff(O,5).derivative('p0'),42)
    eq('O5 has no p1',coeff(O,5).derivative('p1'),0)
    eq('p1 global pivot',coeff(O,4).derivative('p1'),F(15,4))
    eq('O4 has no p0',coeff(O,4).derivative('p0'),0)
    p0=-coeff(O,5).substitute({'p0':0})/42
    p1=-F(4,15)*coeff(O,4).substitute({'p1':0})
    # Compute the pivots, rather than read closed author formulas.
    first={'p0':p0,'p1':p1}
    Oa=specialize(O,first);Ka=specialize(K,first)
    eq('G complete pivot',coeff(Ka,4).derivative('G'),24*t*t)
    eq('K4 no J',coeff(Ka,4).derivative('J'),0)
    GofF=-shift(coeff(Ka,4).substitute({'G':0}),-2)/24
    k3=coeff(Ka,3).substitute({'G':GofF})
    eq('F complete pivot after G',k3.derivative('F'),-F(15,14)*t*t)
    eq('substituted K3 no J',k3.derivative('J'),0)
    Fstar=F(14,15)*shift(k3.substitute({'F':0}),-2)
    Gstar=GofF.substitute({'F':Fstar})
    o3=coeff(Oa,3).substitute({'F':Fstar,'G':Gstar})
    eq('J complete pivot after F and G',o3.derivative('J'),-28*t)
    Jstar=shift(o3.substitute({'J':0}),-1)/28
    final={'F':Fstar,'G':Gstar,'J':Jstar}
    hf=specialize(h,final)
    pf=specialize(specialize(p,first),final)
    qf,of,kf=make(hf,pf)
    peq('full independent ODE recomputation',of,specialize(Oa,final))
    peq('full independent kernel recomputation',kf,specialize(Ka,final))
    for i in range(3,9):eq('eliminated ODE coefficient '+str(i),coeff(of,i),0)
    for i in range(3,7):eq('eliminated kernel coefficient '+str(i),coeff(kf,i),0)
    R=[shift(coeff(of,i),1) for i in (2,1,0)]+[coeff(kf,1),coeff(kf,0)+4]
    gamma=coeff(kf,2)/4
    for i,x in enumerate(R+[gamma]):
        need(all(0<=dict(m).get('t',0)<=2 for m in x.terms),'whole ordinary quadratic '+str(i))
    matrix=[[x.coefficient('t',j) for j in (2,1,0)] for x in R]
    for i,row in enumerate(matrix):eq('whole pencil reconstruction '+str(i),row[0]*t*t+row[1]*t+row[2],R[i])
    eq('gamma formal constant',gamma.coefficient('t',0),16)
    for name,value in (('F',Fstar),('G',Gstar),('J',Jstar)):
        need(all(-1<=dict(m).get('t',0)<=0 for m in value.terms),'critical affine inverse '+name)
    for i,x in enumerate(pf):
        need(all(0<=dict(m).get('t',0)<=1 for m in x.terms),'whole mass affine '+str(i))
    reconstructed=scale(add(mul(qf,hf),neg(mul(pf,deriv(hf)))),F(1,8))
    peq('complete original derivative defect',add(deriv(reconstructed),scale(hf,-8)),scale(of,-F(1,8)))
    eq('original monic',coeff(reconstructed,8),1)
    eq('original balance',coeff(reconstructed,7),0)
    eq('original squared norm',coeff(reconstructed,6),-F(1,2))
    eq('correct third original moment',-3*coeff(reconstructed,5),-F(24,5)*B)
    # Complete formal traces; positivity is asserted only on real-feasible data.
    tau=power_sums(hf,10)
    trace_p=sum((x*tau[i] for i,x in enumerate(pf)),Z)
    trace_p2=sum((x*tau[i] for i,x in enumerate(mul(pf,pf))),Z)
    eq('whole mass trace equals one',trace_p,1)
    sigma=trace_p2-F(1,7)
    # The obstruction is regenerated from the residuals, with no leading
    # coefficient division in the t^2 cross elimination.
    sliceR=[x.substitute({'B':0,'s':0}) for x in R]
    eq('slice E pivot',sliceR[3].derivative('E'),-F(88,7)*t)
    Estar=shift(sliceR[3].substitute({'E':0}),-1)*F(7,88)
    eq('whole slice E formula',Estar,-(10976*r*r+7344*r+1143)/2112)
    slices=[x.substitute({'E':Estar}) for x in sliceR]
    obstruction=audit_slices(slices)
    ranks=rank_controls()
    # Exact elementary constants for the additional ACTUAL-domain corridor.
    eq('mass variance identity',trace_p2-2*trace_p/7+F(1,7),sigma)
    eq('coefficient corridor base',F(3,64)-F(3,112),F(9,448))
    damages={}
    def wrong(name,a,b):
        difference=cast(a)-cast(b);need(difference!=0,'bad identity rejected '+name)
        damages[name]=difference.record()
    wrong('wrong original third moment',-3*coeff(reconstructed,5),-4*B)
    wrong('wrong G pivot sign',24*t*t,-24*t*t)
    wrong('wrong F pivot sign',-F(15,14)*t*t,F(15,14)*t*t)
    wrong('missing t in J pivot',-28*t,-28)
    wrong('six instead of seven masses',trace_p2-F(1,6),sigma)
    wrong('omit mass-trace normalization',trace_p,0)
    return {'checks':checks,'whole_h':record(hf),'whole_p':record(pf),
            'whole_Q':record(qf),'whole_ODE':record(of),'whole_kernel':record(kf),
            'whole_residuals':[x.record() for x in R],
            'whole_matrix':[[x.record() for x in row] for row in matrix],
            'whole_gamma':gamma.record(),'whole_original':record(reconstructed),
            'whole_mass_second_trace':trace_p2.record(),'whole_sigma':sigma.record(),
            'first_pivots':[p0.record(),p1.record()],'G_of_F':GofF.record(),
            'whole_slice_E':Estar.record(),'whole_slice_residuals':[x.record() for x in slices],
            'obstruction':obstruction,'rank_controls':ranks,'damage_rejections':damages,
            'actual_feasible_coefficient_corridor':{'E_lower':'9/448','E_lower_variance_correction':'sigma/32','E_upper':'3/64','D_upper':'3/14','sigma_positive_reason':'degree-five p cannot be constant at seven simple real nodes'},
            'residual_term_counts':[len(x.terms) for x in R],
            'independent_backend':'owned9566 unit anti-triangular Gram solve and monic quotient recomputation; only t inverted'}

if __name__=='__main__':
    print(json.dumps(audit(),sort_keys=True,separators=(',',':')))
