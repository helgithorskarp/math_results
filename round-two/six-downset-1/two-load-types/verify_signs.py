"""Uniform exact eight-sign reconstruction for two pendant load types."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,resource,signal,time
import polynomial as engine
P,R=engine.P,engine.R
require,atom,denominator,det=engine.require,engine.atom,engine.denominator,engine.det
ZERO=engine.ZERO
def variables(kind):
    def x(i):return kind(P({tuple(int(i==j) for j in range(5)):1}))
    q=x(0)+4;t=x(1);D=x(2);a=x(3);u=x(4)
    return q,t,D,a,u
def seed_factors():
    q,t,D,a,u=variables(P);m=a+u;w=q+D-1;h=2*q+2*m-1
    factors=[t,D,a,u,m-2,m-1,m,m+1,h,h-2*D,h-q-D,
             (m-1)*w-1+D,(m-1)*w-1+t,(h-q-1)*(h-D)-D*(q-1)]
    for p in factors:atom(p)
    return len(factors)
def scalars():
    q,t,D,a,u=variables(R);m=a+u;w=q+D-1;h=2*q+2*m-1
    ch=m*(w-D-m-1)/((m+1)*((m-1)*w-1+D))
    cl=m*(w-t-m-1)/((m+1)*((m-1)*w-1+t))
    normK=w+m*(q+D)-a*D-u*t-2*m
    csquare=ch**2*a*q+cl**2*u*(q+D-t)
    kc=ch*a*(q-1)+cl*u*(w-t)
    def eta(ci,di):
        return w-normK/(m+1)**2-ci**2*w+2*ci**2*(q+D-di)/m-csquare/m**2+2*ci*(w-di)/(m+1)-2*kc/(m*(m+1))
    eh,el=eta(ch,D),eta(cl,t);totaleta=a*eh+u*el
    zh=m/(m-2)*(eh-totaleta/(m*(m-1)))
    zl=m/(m-2)*(el-totaleta/(m*(m-1)))
    signs={'zeta_heavy':zh,'zeta_light':zl,'heavy_within_slack':1-ch**2*(q+D)/(h-q-D)-zh/h,'light_within_slack':1-cl**2*(q+D)/(h-q-D)-zl/h}
    return signs,{'q':q,'t':t,'D':D,'a':a,'u':u,'m':m,'w':w,'h':h,'ch':ch,'cl':cl,'eta_heavy':eh,'eta_light':el,'alpha':u*(u*zh+a*zl)/(a*m**2)}
def budget_formulas(s):
    q,t,D,a,u,m,h,ch,cl,alpha=(s[k] for k in ['q','t','D','a','u','m','h','ch','cl','alpha'])
    d0=(h-q-1)*(h-D)-D*(q-1)
    metric=[[R() for _ in range(6)] for _ in range(6)]
    metric[0][0]=(q-1)*(h-D)/d0;metric[0][1]=metric[1][0]=D*(q-1)/d0;metric[1][1]=D*(h-q-1)/d0
    metric[2][2]=D*(q*D/a-1)/(h-2*D);metric[2][3]=metric[3][2]=-D/(h-2*D)
    metric[3][3]=D*(q*t/u-1)/(h-2*D)
    metric[4][4]=(q+D)*(1/t-1/D)*t/(u*h);metric[5][5]=alpha/h
    vectors=[[R(),1/D,1/D,R(),R(),R()], [R(),1/D,R(),1/D,R(1),R()], [R(1),m/D-1,a/D,u/D,u,R()], [R(),u*(ch-cl)/(m*D),u*ch/(m*D),-u*cl/(m*D),-u*cl/m,R(1)]]
    inverse_weights=[1/a,1/u,m+1,u/(a*m)]
    return [[inverse_weights[i]*int(i==j)-sum((vectors[i][b]*metric[b][c]*vectors[j][c] for b in range(6) for c in range(6)),R()) for j in range(4)] for i in range(4)]
def structural_last(A,s,d3):
    C00=A[1][1]*A[2][2]-A[1][2]*A[2][1]
    C11=A[0][0]*A[2][2]-A[0][2]*A[2][0]
    C01=A[0][2]*A[1][2]-A[0][1]*A[2][2]
    u,m,a,h,ch,cl,alpha=(s[k] for k in ['u','m','a','h','ch','cl','alpha'])
    b=[u*ch/m,-u*cl/m,R()];expected=[-u*ch/(a*m),cl/m,R()]
    for i in range(3):
        transformed=A[i][3]-sum((A[i][j]*b[j] for j in range(3)),R())
        require(not (transformed-expected[i]).num,'exact congruence border identity')
    corner=A[3][3]-2*sum((b[i]*A[i][3] for i in range(3)),R())+sum((b[i]*A[i][j]*b[j] for i in range(3) for j in range(3)),R())
    expected_corner=u/(a*m)-alpha/h+u**2*ch**2/(a*m**2)+u*cl**2/m**2
    require(not (corner-expected_corner).num,'exact congruence corner identity')
    return (u/(a*m)-alpha/h)*d3+u**2*ch**2/m**2*(d3/a-C00/a**2)+cl**2/m**2*(u*d3-C11)+2*u*ch*cl/(a*m**2)*C01

def stable(record):return {k:v for k,v in record.items() if k not in ['elapsed_seconds','peak_RSS_KiB']}
def main():
    import coefficients as coeff
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',type=Path);p.add_argument('--expected',type=Path)
    args=p.parse_args();start=time.monotonic();rows=[];factor_cache={}
    signal.alarm(60)
    engine.multiplication_controls();coeff.engine.multiplication_controls();coeff.shift_controls()
    hints=seed_factors();signs,s=scalars();signal.alarm(0)
    signal.alarm(60);budget=budget_formulas(s);signal.alarm(0);minors={}
    def add(name,value):
        numerator=coeff.certify(value.num);den=[]
        for key,power in sorted(value.den.items()):
            factor=engine.ATOMS[key];fingerprint=factor.fingerprint()
            if fingerprint not in factor_cache:factor_cache[fingerprint]=coeff.certify(factor)
            den.append({'factor_sha256':fingerprint,'power':power})
        rows.append({'name':name,'numerator':numerator,'denominator_factors':den,'strictly_positive_rational_function':True})
        print(json.dumps({'completed_sign':name,'elapsed_seconds':time.monotonic()-start}),flush=True)
    for name,value in signs.items():add(name,value)
    for size in range(1,5):
        signal.alarm(60)
        answer=det([row[:size] for row in budget[:size]]) if size<4 else structural_last(budget,s,minors[3])
        minors[size]=answer;signal.alarm(0);add('invariant_minor_'+str(size),answer)
    final=minors[4].num
    require((final+1).fingerprint()!=final.fingerprint(),'changed coefficient rejected')
    negative=dict(final.a)
    # At Q=T=B=V=U=0, the unshifted tuple is t=1,D=2,a=4,u=1.
    # Force the translated constant to -1/final.den; changing an
    # unshifted constant alone to -1 need not invalidate positivity.
    constant=sum(c*2**ex[2]*4**ex[3] for ex,c in final.a.items() if ex[0]==0)
    negative[ZERO]=negative.get(ZERO,0)-constant-1
    try:coeff.certify(P(negative,final.den))
    except ValueError:pass
    else:raise ValueError('damaged last numerator was accepted')
    out={'agent':'six-downset-1','role':'researcher','status':'all eight rational functions strictly positive','raw_field':'QQ(Q,t,D,a,u),q=Q+4','sign_domain':'Q,T,B,V,U>=0;t=T+1,D=t+B+1,a=2D+V,u=t+U','positive_functions':rows,'denominator_factor_certificates':[{**factor_cache[key],'factor_sha256':key} for key in sorted(factor_cache)],'positive_rational_functions':8,'numerator_Q_coefficient_lemmas':sum(len(row['numerator']['Q_coefficients']) for row in rows),'shifted_numerator_terms':sum(row['numerator']['total_shifted_coefficient_terms'] for row in rows),'positive_factor_hints':hints,'first_three_determinant_permutations':[1,2,6],'last_minor_method':'four exact congruence identities and three cofactors;separate Q-coefficient positivity','exact_congruence_identities':4,'multiplication_controls':36,'direct_power_shift_controls':3,'shift_point_controls_per_nonzero_Q_coefficient':2,'changed_coefficient_rejected':True,'negative_coefficient_rejected':True,'full_shifted_five_variable_polynomial_constructed':False,'per_polynomial_term_guard':30000,'packing_bytes_guard':32*1024*1024,'stage_seconds_guard':60,'CAS_imports':False,'elapsed_seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.expected:require(stable(out)==stable(json.loads(args.expected.read_text())['signs']),'frozen exact sign certificate mismatch')
    if args.write:args.write.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
