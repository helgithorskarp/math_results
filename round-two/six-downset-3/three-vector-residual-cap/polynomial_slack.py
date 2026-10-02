"""bounded polynomial replacement for timed-out rational cancel.

QQ[q,k], variable order q,k, characteristic zero. All denominator factors
are kept explicitly positive on k>=2,q>=3k. No inverse/gcd/factor job.
"""
from pathlib import Path
import json
import sys
import time
import resource
import residual
import sympy as sp
residual.require(sp.__version__ == '1.14.0', 'optional derivation requires SymPy 1.14.0')
q,k=sp.symbols('q k')
poly=lambda e:sp.Poly(e,q,k,domain=sp.QQ)


def coefficient_list(p):
    return [[list(degrees),str(c)] for degrees,c in sorted(p.terms())]


def build():
    raw=json.loads(Path(__file__).with_name('SYMBOLIC-MOMENTS.json').read_text())
    saved=raw.pop('record_sha256')
    residual.require(residual.digest(raw)==saved=='6b51a5e96ba90f07a78178c2808dd8d012f9a9493ce76f1c1015129813cbb8ea',
                     'full physical symbolic moments pin')
    ell=poly(5*q+4-k)
    d0=poly(q**3*(q-2)*(q-1)**2*(q*q+q+6))*ell
    rn=[]
    for row in raw['residual']:
        new=[]
        for text in row:
            expr=sp.sympify(text,locals={'q':q,'k':k})
            numerator,denominator=sp.fraction(expr)
            # Exact polynomial division, with remainder rejected by exquo.
            new.append(poly(numerator)*d0.exquo(poly(denominator)))
        rn.append(new)
    gap2=poly(q*q+7*q+8-2*k)
    gc2=poly(q*q+q-2*k)
    t2=poly(q)*gap2
    v2=ell*gap2-poly(8*q*(3*q+4))
    aq=poly((2*k+1)*q*q+k*q-2*k)
    c=ell*poly(1-k)
    bq=poly(q*((q-k)*(3*q+4)+3*k)+2*k)
    dn=poly(q*q)*t2*v2-4*bq*bq
    an=2*poly(q)*(v2*aq+2*bq*c)
    bn=2*(poly(q*q)*t2*c+2*bq*aq)
    ww=rn[0][0]*dn*dn-2*an*dn*rn[0][1]-2*bn*dn*rn[0][2]
    ww+=an*an*rn[1][1]+2*an*bn*rn[1][2]+bn*bn*rn[2][2]
    eta=2*poly(q*q)*(v2*rn[1][1]+t2*rn[2][2])+8*poly(q)*bq*rn[1][2]
    # comparison slack g-eta-Rww, EXACT positive denominator 2*d0*Dn².
    numerator=gc2*d0*dn*dn-2*(eta*dn+ww)
    denominator=2*d0*dn*dn
    qn=2*poly(q)*poly((q*q+(13-6*k)*q+2*k*k-10*k+14)/2)*dn-2*an*aq-2*poly(q)*bn*c
    qd=2*poly(q)*dn
    return {'numerator':numerator,'denominator':denominator,'d0':d0,'Dn':dn,
            'Rww_numerator':ww,'eta_numerator':eta,'Q_numerator':qn,'Q_denominator':qd}


def evaluate(p,qq,kk):
    return sum(residual.F(c.p,c.q)*qq**degrees[0]*kk**degrees[1] for degrees,c in p.terms())


def residual_numerators():
    raw=json.loads(Path(__file__).with_name('SYMBOLIC-MOMENTS.json').read_text())
    d0=poly(q**3*(q-2)*(q-1)**2*(q*q+q+6)*(5*q+4-k))
    result={}
    for i,j in ((0,0),(0,1),(0,2),(1,1),(1,2),(2,2)):
        numerator,denominator=sp.fraction(sp.sympify(raw['residual'][i][j],locals={'q':q,'k':k}))
        result[str(i)+str(j)]=coefficient_list(poly(numerator)*d0.exquo(poly(denominator)))
    result['record_sha256']=residual.digest(result)
    return result


def global_certificate(p,minimum=25):
    x,u=sp.symbols('x u')
    shifted=sp.Poly(p.as_expr().subs({q:5*(minimum+x)+u,k:minimum+x}),x,u,domain=sp.QQ)
    return {'scope':f'ALL real k>={minimum},q>=5k; integer physical domain',
            'substitution':f'k={minimum}+x,q=5k+u,x,u>=0',
            'constant':str(shifted.coeff_monomial(1)),
            'coefficient_count':len(shifted.terms()),
            'negative_count':sum(bool(c<0) for degrees,c in shifted.terms()),
            'coefficients':coefficient_list(shifted),
            'passed':shifted.coeff_monomial(1)>0 and all(c>=0 for degrees,c in shifted.terms())}


def run():
    start=time.perf_counter();forms=build()
    print('Bounded common-denominator polynomials formed',time.perf_counter()-start,flush=True)
    checks=[]
    for qq,kk in ((91,18),(125,25),(142,27),(250,50),(1666,297)):
        actual=residual.compare(qq,kk);sv=residual.three_vectors.scalars(qq,kk);R=actual['residual']
        w=[residual.F(1),-sv['a'],-sv['b']]
        ww=sum(R[i][j]*w[i]*w[j] for i in range(3) for j in range(3))
        eta=(sv['V']*R[1][1]-2*sv['B']*R[1][2]+sv['T']*R[2][2])/sv['determinant']
        dn,d0=evaluate(forms['Dn'],qq,kk),evaluate(forms['d0'],qq,kk)
        residual.require(evaluate(forms['Rww_numerator'],qq,kk)/(d0*dn*dn)==ww,'all cleared residual w pairings')
        residual.require(evaluate(forms['eta_numerator'],qq,kk)/(d0*dn)==eta,'all cleared trace bounds')
        residual.require(evaluate(forms['numerator'],qq,kk)/evaluate(forms['denominator'],qq,kk)==residual.F(actual['g'])-eta-ww,'all cleared comparison slacks')
        residual.require(evaluate(forms['Q_numerator'],qq,kk)/evaluate(forms['Q_denominator'],qq,kk)==sv['Q'],'all cleared necessary scalar values')
        checks.append([qq,kk])
    certificate=global_certificate(forms['numerator'])
    result={'agent':'six-downset-3','role':'researcher','status':'exact coefficient certificate',
            'SymPy_version':sp.__version__,'coefficient_ring':'QQ[q,k], characteristic zero',
            'global_slack':certificate,'forms':{name:coefficient_list(p) for name,p in forms.items()},
            'calibrations':checks,'denominator_positivity':'2*d0*Dn²>0; all d0 factors positive and Dn>0 by 9582'}
    result['record_sha256']=residual.digest(result)
    Path(__file__).with_name('POLYNOMIAL-SLACK.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'digest':result['record_sha256'],'seconds':time.perf_counter()-start,
                      'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'global_coefficient_count':certificate['coefficient_count'],
                      'negative_coefficients':certificate['negative_count'],'passed':bool(certificate['passed'])}))


if __name__=='__main__':run()
