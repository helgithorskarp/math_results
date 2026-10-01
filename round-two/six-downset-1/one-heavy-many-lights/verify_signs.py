"""Uniform eight-sign reconstruction for arbitrary equal light mark count.

Credits the9005 polynomial engine; its four-variable adaptation is polynomial.py.
No numerical sign inference and no universal theorem from an incomplete run.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,resource,signal,time
import polynomial as engine
P,R=engine.P,engine.R
require,atom,denominator,det=engine.require,engine.atom,engine.denominator,engine.det
ZERO=engine.ZERO
def seed_factors():
    q=P({(1,0,0,0):1})+4;t=P({(0,1,0,0):1})+1
    D=t+P({(0,0,1,0):1})+1;u=2*t+P({(0,0,0,1):1})
    m=D+u;w=q+D-1;h=2*q+2*m-1
    factors=[t,D,u,m-2,m-1,m,m+1,h,h-2*D,h-q-D,
             (m-1)*w-1+D,(m-1)*w-1+t,(h-q-1)*(h-D)-D*(q-1)]
    for p in factors:
        require(p.positive(),'positive exact factor hint');atom(p)
    return len(factors)

def formulas():
    q=R(P({(1,0,0,0):1}))+4;t=R(P({(0,1,0,0):1}))+1
    D=t+R(P({(0,0,1,0):1}))+1;u=2*t+R(P({(0,0,0,1):1}))
    m=D+u;w=q+D-1;h=2*q+2*m-1
    ch=m*(w-D-m-1)/((m+1)*((m-1)*w-1+D))
    cl=m*(w-t-m-1)/((m+1)*((m-1)*w-1+t))
    normK=w+m*(q+D)-D**2-u*t-2*m
    ky=u/m*(ch*(q-1)-cl*(w-t))
    y2=u**2/m**2*(ch**2*q/D+cl**2*(q+D-t)/u)
    eh=w-normK/(m+1)**2-y2-ch**2*(q+D)*(1-1/D)+2*ky/(m+1)
    el=w-normK/(m+1)**2-ch**2*q*D/m**2-cl**2*w+cl**2*(q+D-t)*(2*D+u)/m**2-2*D*(ch*(q-1)-cl*(w-t))/(m*(m+1))
    totaleta=D*eh+u*el
    zh=m/(m-2)*(eh-totaleta/(m*(m-1)))
    zl=m/(m-2)*(el-totaleta/(m*(m-1)))
    signs={'zeta_heavy':zh,'zeta_light':zl,'heavy_within_slack':1-ch**2*(q+D)/(h-q-D)-zh/h,'light_within_slack':1-cl**2*(q+D)/(h-q-D)-zl/h}
    alpha=u*(u*zh+D*zl)/(D*m**2)
    d0=(h-q-1)*(h-D)-D*(q-1)
    metric=[[R() for _ in range(6)] for _ in range(6)]
    metric[0][0]=(q-1)*(h-D)/d0;metric[0][1]=metric[1][0]=D*(q-1)/d0;metric[1][1]=D*(h-q-1)/d0
    metric[2][2]=D*(q-1)/(h-2*D);metric[2][3]=metric[3][2]=-D/(h-2*D)
    metric[3][3]=D*(q*t/u-1)/(h-2*D)
    metric[4][4]=(q+D)*(1/t-1/D)*t/(u*h);metric[5][5]=alpha/h
    vectors=[[R(),R(1),R(1),R(),R(),R()], [R(),1/D,R(),1/D,R(1),R()], [R(1),u/D,R(1),u/D,u,R()], [R(),u*(ch-cl)/(m*D),u*ch/(m*D),-u*cl/(m*D),-u*cl/m,R(1)]]
    inverse_weights=[D,1/u,m+1,u/(D*m)]
    budget=[[inverse_weights[i]*int(i==j)-sum((vectors[i][a]*metric[a][b]*vectors[j][b] for a in range(6) for b in range(6)),R()) for j in range(4)] for i in range(4)]
    return signs,budget,{'ch':ch,'cl':cl,'eta_heavy':eh,'eta_light':el,'alpha':alpha,'u':u,'m':m,'D':D,'h':h}

def structural_last(budget,scalars,d3):
    # The old component of update4 is a1*v1+a2*v2.  The congruence
    # subtracting a1/a2 columns and rows leaves a bordered determinant.
    # Here p=diag(D,1/u,m+1)*a=(u*ch/m,-cl/m,0).
    A=budget
    C00=A[1][1]*A[2][2]-A[1][2]*A[2][1]
    C11=A[0][0]*A[2][2]-A[0][2]*A[2][0]
    C01=A[0][2]*A[1][2]-A[0][1]*A[2][2]
    u,m,D,h,ch,cl,alpha=(scalars[k] for k in ['u','m','D','h','ch','cl','alpha'])
    a=[u*ch/(m*D),-u*cl/m,R()]
    expected=[-u*ch/m,cl/m,R()]
    for i in range(3):
        transformed=A[i][3]-sum((A[i][j]*a[j] for j in range(3)),R())
        require(not (transformed-expected[i]).num,'exact congruence border identity')
    corner=A[3][3]-2*sum((a[i]*A[i][3] for i in range(3)),R())+sum((a[i]*A[i][j]*a[j] for i in range(3) for j in range(3)),R())
    expected_corner=u/(D*m)-alpha/h+u**2*ch**2/(m**2*D)+u*cl**2/m**2
    require(not (corner-expected_corner).num,'exact congruence corner identity')
    result=(u/(D*m)-alpha/h)*d3
    result=result+u**2*ch**2/m**2*(d3/D-C00)
    result=result+cl**2/m**2*(u*d3-C11)
    result=result+2*u*ch*cl/m**2*C01
    return result

def brief(value):
    den=denominator(value.den)
    require(value.num.positive() and den.positive(),'strict coefficient certificate')
    return {'numerator_terms':len(value.num.a),'denominator_terms':len(den.a),'numerator_degree':value.num.degree(),'denominator_degree':den.degree(),'numerator_constant':str(F(value.num.a[ZERO],value.num.den)),'denominator_constant':str(F(den.a[ZERO],den.den)),'numerator_sha256':value.num.fingerprint(),'denominator_sha256':den.fingerprint(),'positive_constants_and_nonnegative_coefficients':True}

def stable(d):return {k:v for k,v in d.items() if k not in ['elapsed_seconds','peak_RSS_KiB']}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',type=Path);parser.add_argument('--expected',type=Path)
    args=parser.parse_args();start=time.monotonic();signal.alarm(60)
    engine.multiplication_controls();hints=seed_factors()
    signs,budget,scalars=formulas();signal.alarm(0)
    rows=[{'name':name,**brief(value)} for name,value in signs.items()];minors={}
    for k in range(1,5):
        signal.alarm(60)
        answer=det([row[:k] for row in budget[:k]]) if k<4 else structural_last(budget,scalars,minors[3])
        minors[k]=answer;rows.append({'name':'symmetric_minor_'+str(k),**brief(answer)});signal.alarm(0)
    final=minors[4].num;negative=dict(final.a);negative[ZERO]=-1
    require((final+1).fingerprint()!=final.fingerprint(),'changed-coefficient rejection')
    require(not P(negative,final.den).positive(),'negative-coefficient rejection')
    out={'agent':'six-downset-1','role':'researcher','domain':'QQ(Q,T,B,U)','substitution':'q=Q+4,t=T+1,D=t+B+1,u=2t+U;Q,T,B,U>=0','positive_functions':rows,'positive_rational_functions':8,'coefficient_terms':sum(x['numerator_terms']+x['denominator_terms'] for x in rows),'positive_factor_hints':hints,'first_three_determinant_permutations':[1,2,6],'last_minor_method':'congruence and three cofactors,old update4 in span(update1,update2)','exact_congruence_identities':4,'multiplication_controls':18,'changed_coefficient_rejected':True,'negative_coefficient_rejected':True,'CAS_imports':False,'elapsed_seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.expected:require(stable(out)==stable(json.loads(args.expected.read_text())['signs']),'frozen exact coefficient certificate mismatch')
    if args.write:args.write.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
