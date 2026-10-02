"""bounded QQ polynomial certificates on P²=28k²+36k+81.

Physical integers only. The positive root branch has
5k+9<=P<=(16k+9)/3 for k>=18. Exact quotient/remainder arithmetic and
coefficient sandwiches prove positivity on the whole branch if they pass.
"""
from pathlib import Path
import json
import time
import resource
import residual
import polynomial_slack as ps
sp,q,k=ps.sp,ps.q,ps.k
P=sp.Symbol('P')


def mean_numerator():
    # Direct published nine row classes, retaining their literal weights.
    den=ps.poly(q*(q-1)*(q-2))
    beta=2*(q-1)/(q*(q-2))
    ww=(2*q*q+2*q-2)/(q*(q-1))
    rows=[(5*q+6-k,1-k),(1,1+2*k+2*k/q),
          (k,(k-1)*ww),(q-k,1+k*ww),
          (k,(k-1)/q),(q-k,1+k/q)]
    for z in range(3):
        choose=lambda n,r:(sp.Integer(1),n,n*(n-1)/2)[r]
        rows.append((choose(k,z)*choose(q-k,2-z),1-z+(k-z)*beta))
    V=ps.poly(0)
    for count,row in rows:
        rn,rd=sp.fraction(sp.cancel(row))
        value=ps.poly(rn)*den.exquo(ps.poly(rd))
        V+=ps.poly(count)*value*value
    E=ps.poly(q*q+(13-6*k)*q+2*k*k-10*k+14)
    n2=ps.poly(q*q+13*q+14-2*k)
    g2=ps.poly(q*q+q-2*k)
    num=E*n2*g2*den*den-4*n2*V+2*E*E*den*den
    denominator=2*n2*g2*den*den
    return num,denominator


def norm_certificate(poly,minimum):
    replaced=sp.Poly(poly.as_expr().subs(q,(6*k+P-25)/2),P,k,domain=sp.QQ)
    relation=sp.Poly(P*P-28*k*k-36*k-81,P,k,domain=sp.QQ)
    # Polynomial long division in P with coefficients in QQ[k].
    quotient,remainder=sp.div(replaced.as_expr(),relation.as_expr(),P)
    residual.require(sp.Poly(quotient*relation.as_expr()+remainder-replaced.as_expr(),P,k,domain=sp.QQ).is_zero,
                     'entire norm quotient/remainder identity')
    rp=sp.Poly(remainder,P)
    residual.require(rp.degree()<=1,'linear reduced norm expression')
    f=rp.coeff_monomial(1)
    g=rp.coeff_monomial(P)
    x=sp.Symbol('x')
    ff=sp.Poly(f.subs(k,minimum+x),x,domain=sp.QQ)
    gg=sp.Poly(g.subs(k,minimum+x),x,domain=sp.QQ)
    positive=sp.Poly.from_dict({p:c for p,c in gg.terms() if c>0},x,domain=sp.QQ)
    negative=sp.Poly.from_dict({p:c for p,c in gg.terms() if c<0},x,domain=sp.QQ)
    low=5*(minimum+x)+9
    high=(16*(minimum+x)+9)/3
    bound=ff+positive*sp.Poly(low,x,domain=sp.QQ)+negative*sp.Poly(high,x,domain=sp.QQ)
    passed=bool(bound.coeff_monomial(1)>0 and all(c>=0 for p,c in bound.terms()))
    return {'minimum_k':minimum,'substitution':'q=(6k+P-25)/2',
            'relation':'P²=28k²+36k+81; P>0',
            'quotient_coefficients':ps.coefficient_list(sp.Poly(quotient,P,k,domain=sp.QQ)),
            'remainder_coefficients':ps.coefficient_list(sp.Poly(remainder,P,k,domain=sp.QQ)),
            'shifted_f':ps.coefficient_list(ff),'shifted_g':ps.coefficient_list(gg),
            'coefficient_sandwich':ps.coefficient_list(bound),
            'negative_bound_coefficients':sum(bool(c<0) for p,c in bound.terms()),
            'bound_constant':str(bound.coeff_monomial(1)),'passed':passed}


def run():
    start=time.perf_counter();forms=ps.build()
    # q,k scalar Q>=1 is sufficient if uniform residual slack passed.
    qclaim=norm_certificate(forms['Q_numerator']-forms['Q_denominator'],25)
    mean,den=mean_numerator()
    mclaim=norm_certificate(-mean,18)
    records=[]
    kk,pp=18,99
    from variance import bound,scalar_record
    for j in range(4):
        qq=(6*kk+pp-25)//2
        residual.require(pp*pp-28*kk*kk-36*kk==81 and pp%2==1,'exact Pell-type norm and parity')
        residual.require(qq==bound(kk)-5,'literal remaining integer order')
        r=residual.compare(qq,kk)
        residual.require(r['comparison_status']=='strict sufficient comparison','new whole-residual positivity diagnostic')
        actual_mean=residual.F(scalar_record(qq,kk)['strict_scalar_margin'])
        residual.require(ps.evaluate(mean,qq,kk)/ps.evaluate(den,qq,kk)==actual_mean<0,'exact old scalar-bound failure')
        residual.require(r['three_vector_necessary_Q']>1,'exact new necessary scalar positive')
        records.append({'j':j,'k':kk,'P':pp,'q':qq,'Q':str(r['three_vector_necessary_Q']),
                        'old_mean_margin':str(actual_mean),'delta':str(r['delta']),'mu':str(r['mu'])})
        kk,pp=8*kk+3*(pp+3)//2,8*pp+42*kk+27
    result={'agent':'six-downset-3','role':'researcher','status':'exact unbounded certificate if coefficient checks pass',
            'SymPy_version':sp.__version__,'coefficient_ring':'QQ[P,k], relation P²-28k²-36k-81',
            'Q_minus_one':qclaim,'negative_old_mean':mclaim,
            'mean_numerator':ps.coefficient_list(mean),'mean_denominator':ps.coefficient_list(den),
            'exact_sequence_diagnostics':records}
    result['record_sha256']=residual.digest(result)
    Path(__file__).with_name('PELL-NORM.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'digest':result['record_sha256'],'seconds':time.perf_counter()-start,
                      'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'Q_certificate_passed':qclaim['passed'],'Q_negative_coefficients':qclaim['negative_bound_coefficients'],
                      'old_margin_certificate_passed':mclaim['passed'],'old_margin_negative_coefficients':mclaim['negative_bound_coefficients'],
                      'sequence':records}))


if __name__=='__main__':run()
