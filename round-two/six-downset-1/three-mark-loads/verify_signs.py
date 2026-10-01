"""Uniform exact signs for one heavy and two equal lighter pendant loads.

Reuses the credited standard-library rational polynomial engine from9005.
Reconstructs all formulas here; no CAS or saved polynomial corpus is used.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,importlib.util,json,resource,signal,time

ENGINE_PATH=Path(__file__).resolve().parent.parent/'two-unequal-loads'/'verify_signs.py'
spec=importlib.util.spec_from_file_location('two_load_sign_engine',ENGINE_PATH)
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
P,R=engine.P,engine.R
require,atom,denominator,det=engine.require,engine.atom,engine.denominator,engine.det
ZERO=engine.ZERO
FACTOR_HINTS=[[[[0,0,0],"5"],[[0,0,1],"1"],[[0,1,0],"3"]],[[[0,0,0],"16"],[[0,0,1],"9"],[[0,0,2],"1"],[[0,1,0],"19"],[[0,1,1],"4"],[[0,2,0],"3"],[[1,0,0],"3"],[[1,0,1],"1"],[[1,1,0],"3"]],[[[0,0,0],"15"],[[0,0,1],"8"],[[0,0,2],"1"],[[0,1,0],"19"],[[0,1,1],"4"],[[0,2,0],"3"],[[1,0,0],"3"],[[1,0,1],"1"],[[1,1,0],"3"]],[[[0,0,0],"2"],[[0,0,1],"1"],[[0,1,0],"3"]],[[[0,0,0],"3"],[[0,0,1],"1"],[[0,1,0],"3"]],[[[0,0,0],"9"],[[0,0,1],"1"],[[0,1,0],"5"],[[1,0,0],"1"]],[[[0,0,0],"15"],[[0,0,1],"2"],[[0,1,0],"6"],[[1,0,0],"2"]],[[[0,0,0],"11"],[[0,1,0],"4"],[[1,0,0],"2"]],[[[0,0,0],"124"],[[0,0,1],"33"],[[0,0,2],"2"],[[0,1,0],"125"],[[0,1,1],"16"],[[0,2,0],"30"],[[1,0,0],"31"],[[1,0,1],"4"],[[1,1,0],"16"],[[2,0,0],"2"]],[[[0,0,0],"1"],[[0,1,0],"1"]],[[[0,0,0],"2"],[[0,0,1],"1"],[[0,1,0],"1"]],[[[0,0,0],"4"],[[0,0,1],"1"],[[0,1,0],"3"]]]

def formulas():
    q=R(P({(1,0,0):1}))+4;t=R(P({(0,1,0):1}))+1;D=t+R(P({(0,0,1):1}))+1
    m=D+2*t;w=q+D-1;h=2*q+2*m-1
    ch=m*(w-D-m-1)/((m+1)*((m-1)*w-1+D))
    cl=m*(w-t-m-1)/((m+1)*((m-1)*w-1+t))
    normK=w+m*(q+D)-D**2-2*t**2-2*m
    ky=2*t/m*(ch*(q-1)-cl*(w-t))
    y2=4*t**2/m**2*(ch**2*q/D+cl**2*(q+D-t)/(2*t))
    sm2=(q+D-t)/(2*t)
    eh=w-normK/(m+1)**2-y2-ch**2*(q+D)*(1-1/D)+2*ky/(m+1)
    el=w-normK/(m+1)**2-D**2/(4*t**2)*y2-cl**2*sm2-cl**2*(q+D)*(1-1/t)-D/t*ky/(m+1)
    totaleta=D*eh+2*t*el
    zh=m/(m-2)*(eh-totaleta/(m*(m-1)))
    zl=m/(m-2)*(el-totaleta/(m*(m-1)))
    signs={'zeta_heavy':zh,'zeta_light':zl,'heavy_within_slack':1-ch**2*(q+D)/(h-q-D)-zh/h,'light_within_slack':1-cl**2*(q+D)/(h-q-D)-zl/h}
    alpha=2*t*(2*t*zh+D*zl)/(D*m**2)
    d0=(h-q-1)*(h-D)-D*(q-1)
    metric=[[R() for _ in range(6)] for _ in range(6)]
    metric[0][0]=(q-1)*(h-D)/d0;metric[0][1]=metric[1][0]=D*(q-1)/d0;metric[1][1]=D*(h-q-1)/d0
    metric[2][2]=D*(q-1)/(h-2*D);metric[2][3]=metric[3][2]=-D/(h-2*D)
    metric[3][3]=D*(q/2-1)/(h-2*D)
    metric[4][4]=(q+D)*(1/t-1/D)/(2*h);metric[5][5]=alpha/h
    vectors=[[R(),R(1),R(1),R(),R(),R()], [R(),1/D,R(),1/D,R(1),R()], [R(1),2*t/D,R(1),2*t/D,2*t,R()], [R(),2*t*(ch-cl)/(m*D),2*t*ch/(m*D),-2*t*cl/(m*D),-2*t*cl/m,R(1)]]
    inverse_weights=[D,1/(2*t),m+1,2*t/(D*m)]
    budget=[[inverse_weights[i]*int(i==j)-sum((vectors[i][a]*metric[a][b]*vectors[j][b] for a in range(6) for b in range(6)),R()) for j in range(4)] for i in range(4)]
    beta=q/(2*D*(h-2*D))+(q+D)*(1/t-1/D)/(2*h)
    signs['antisymmetric_first']=1-2*t*beta
    signs['antisymmetric_determinant']=(1-2*t*beta)*(1-zl/h)-2*t*cl**2*beta
    return signs,budget,{'ch':ch,'cl':cl,'eta_heavy':eh,'eta_light':el}

def stable(record):return {k:v for k,v in record.items() if k not in ['elapsed_seconds','peak_RSS_KiB']}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',type=Path);parser.add_argument('--expected',type=Path)
    args=parser.parse_args();start=time.monotonic()
    signal.alarm(60);engine.multiplication_controls()
    for hint in FACTOR_HINTS:
        factor=P.decode(hint);require(factor.positive(),'positive denominator optimization hint');atom(factor)
    signs,budget,scalars=formulas();signal.alarm(0)
    for k in range(1,5):
        signal.alarm(60);signs['symmetric_minor_'+str(k)]=det([row[:k] for row in budget[:k]]);signal.alarm(0)
    rows=[]
    for name,value in signs.items():
        den=denominator(value.den)
        require(value.num.positive() and den.positive(),'strict positive coefficient certificate '+name)
        rows.append({'name':name,'numerator_terms':len(value.num.a),'denominator_terms':len(den.a),'numerator_degree':value.num.degree(),'denominator_degree':den.degree(),'numerator_constant':str(F(value.num.a[ZERO],value.num.den)),'denominator_constant':str(F(den.a[ZERO],den.den)),'numerator_sha256':value.num.fingerprint(),'denominator_sha256':den.fingerprint(),'positive_constants_and_nonnegative_coefficients':True})
    final=signs['symmetric_minor_4'].num;changed=final+1;negative=dict(final.a);negative[ZERO]=-1
    require(changed.fingerprint()!=final.fingerprint(),'changed-coefficient rejection')
    require(not P(negative,final.den).positive(),'negative-coefficient rejection')
    out={'agent':'six-downset-1','role':'researcher','domain':'QQ[Q,T,B] and its fraction field','substitution':'q=Q+4,t=T+1,D=t+B+1; Q,T,B>=0','positive_functions':rows,'positive_rational_functions':len(rows),'determinant_permutations':[1,2,6,24],'denominator_hints':len(FACTOR_HINTS),'multiplication_controls':18,'changed_coefficient_rejected':True,'negative_coefficient_rejected':True,'CAS_imports':False,'elapsed_seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.expected:require(stable(out)==stable(json.loads(args.expected.read_text())['signs']),'frozen exact coefficient certificate mismatch')
    if args.write:args.write.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
