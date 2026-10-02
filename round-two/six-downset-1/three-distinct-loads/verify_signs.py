"""Reconstruct all twelve uniform signs with exact standard-library code.

No private saved polynomials, interpolation, floating point or CAS inputs
are used. The final determinant is formed as separate polynomials in each
power of Q. Every polynomial and coefficient operation retains the prior
30000-term,32MiB packing and60s stage guards.
"""
from pathlib import Path
from fractions import Fraction as F
from math import prod
import argparse,hashlib,json,random,resource,signal,time
import polynomial as engine
import coefficients as coeff
import symbolic as formula
import verify_generic
P,R,require=engine.P,engine.R,engine.require
CP=coeff.P
def fingerprint_Q(parts):
    small=[[j,p.fingerprint()] for j,p in sorted(parts.items())]
    return hashlib.sha256(json.dumps(small,separators=(',',':')).encode()).hexdigest()
def add_Q(a,b):
    out=dict(a)
    for j,p in b.items():
        z=out.get(j,CP())+p
        if z:out[j]=z
        else:out.pop(j,None)
    return out
def multiply_Q(a,b):
    if not a or not b:return {}
    out={}
    for j in range(min(a)+min(b),max(a)+max(b)+1):
        signal.alarm(60);z=CP()
        for i,p in a.items():
            if j-i in b:z=z+p*b[j-i]
        if z:out[j]=z
        signal.alarm(0)
    return out
def evaluate_Q(parts,Q,loads):return sum((F(Q)**j*coeff.evaluate(p,loads) for j,p in parts.items()),F(0))
def convolution_controls():
    rng=random.Random(202610021)
    for repeat in range(9):
        a=P({tuple(rng.randrange(3) for _ in range(4)):rng.randrange(-13,14) for _ in range(8)},7)
        b=P({tuple(rng.randrange(3) for _ in range(4)):rng.randrange(-13,14) for _ in range(7)},11)
        require(multiply_Q(coeff.split_Q(a),coeff.split_Q(b))==coeff.split_Q(engine.reference_mul(a,b)),'separate Q product/schoolbook control')
    require(multiply_Q({}, {0:CP(1)})=={},'zero separate Q product')
def certify_Q(parts):
    rows=[]
    for j,p in sorted(parts.items()):
        signal.alarm(60);shifted=coeff.load_shifts(p)
        require(all(c>=0 for c in shifted.a.values()),'negative shifted final coefficient')
        if j==0:require(shifted.positive(),'strict final Q0 coefficient')
        for point in [(0,0,0),(1,2,3)]:
            B,T,V=point;v=V+1;t=v+T+1;D=t+B+1
            require(coeff.evaluate(shifted,point)==coeff.evaluate(p,(D,t,v)),'final triangular exact point control')
        rows.append({'Q_power':j,'raw_terms':len(p.a),'raw_degree':p.degree(),'raw_sha256':p.fingerprint(),'terms':len(shifted.a),'degree':shifted.degree(),'constant':str(F(shifted.a.get(coeff.ZERO,0),shifted.den)),'sha256':shifted.fingerprint(),'nonnegative_coefficients':True})
        signal.alarm(0)
        print(json.dumps({'final_Q_coefficient':j,'terms':len(shifted.a)}),flush=True)
    require(rows and rows[0]['Q_power']==0,'missing strict final Q0 coefficient')
    return {'representation':'separate raw Q coefficients; no raw4 expanded numerator','raw_Q_fingerprints_sha256':fingerprint_Q(parts),'raw_degree':max(j+p.degree() for j,p in parts.items()),'raw_total_coefficient_terms':sum(len(p.a) for p in parts.values()),'Q_coefficients':rows,'total_shifted_coefficient_terms':sum(r['terms'] for r in rows),'strictly_positive_on_nonnegative_domain':True}
def stable(out):return {k:v for k,v in out.items() if k not in ['elapsed_seconds','peak_RSS_KiB']}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',type=Path);parser.add_argument('--expected',type=Path);args=parser.parse_args();started=time.monotonic();rows=[];factors={}
    generic=verify_generic.check();signal.signal(signal.SIGALRM,engine.alarm)
    signal.alarm(60);engine.multiplication_controls();coeff.engine.multiplication_controls();coeff.shift_controls();signal.alarm(0);convolution_controls()
    signal.alarm(60);hints=formula.seed_factors();signs,s=formula.scalars();signal.alarm(0)
    def save_partial():
        if args.write:args.write.write_text(json.dumps({'agent':'six-downset-1','role':'researcher','status':'partial exact sign reconstruction','positive_functions':rows},indent=2)+'\n')
    def certify_den(den):
        output=[]
        for key,power in sorted(den.items()):
            factor=engine.ATOMS[key];fp=factor.fingerprint()
            if fp not in factors:factors[fp]=coeff.certify(factor)
            output.append({'factor_sha256':fp,'power':power})
        return output
    def add(name,value):
        rows.append({'name':name,'numerator':coeff.certify(value.num),'denominator_factors':certify_den(value.den),'strictly_positive':True})
        save_partial();print(json.dumps({'completed_sign':name,'elapsed_seconds':time.monotonic()-started}),flush=True)
    for name,value in signs.items():add(name,value)
    signal.alarm(60);A=formula.old_budget(s);signal.alarm(0);minors={}
    for size in range(1,5):
        signal.alarm(60);minors[size]=engine.det([row[:size] for row in A[:size]]);signal.alarm(0);add('mean_minor_'+str(size),minors[size])
    signal.alarm(60);X,E=formula.border(s);C=formula.cofactors(A);Y,compound,terms=formula.border_terms(A,minors[4],X,E,C);signal.alarm(0)
    signal.alarm(60);fifth=minors[4]*E[0][0]-Y[0][0];signal.alarm(0);add('mean_minor_5',fifth)
    signal.alarm(60);products,common=formula.common_numerator_factors(terms);signal.alarm(0)
    final={};summands=[]
    for i,product in enumerate(products):
        part={0:CP(1)}
        for factor in product:part=multiply_Q(part,coeff.split_Q(factor))
        final=add_Q(final,part)
        summands.append({'index':i,'Q_coefficients':len(part),'raw_Q_coefficient_terms':sum(len(p.a) for p in part.values()),'largest_load_polynomial_terms':max(len(p.a) for p in part.values()),'Q_fingerprints_sha256':fingerprint_Q(part)})
        print(json.dumps({'completed_final_summand':i,'elapsed_seconds':time.monotonic()-started}),flush=True)
    final_certificate=certify_Q(final)
    rows.append({'name':'mean_minor_6','numerator':final_certificate,'denominator_factors':certify_den(common),'strictly_positive':True});save_partial()
    # These physical evaluations are regression checks, not universal proofs.
    import verify_full as full
    signal.signal(signal.SIGALRM,engine.alarm);points=[]
    for q,loads in [(4,[3,2,1]),(8,[4,3,1]),(16,[5,3,2])]:
        signal.alarm(60);den=F(1);Q=q-4
        for key,power in common.items():den*=sum((F(v,engine.ATOMS[key].den)*prod(F(x)**e for x,e in zip([Q,*loads],ex)) for ex,v in engine.ATOMS[key].a.items()),F(0))**power
        actual=full.scalars(q,loads)['leading_minors'][5]
        require(den>0 and evaluate_Q(final,Q,loads)/den==actual,'full physical sixth determinant point control')
        points.append({'q':q,'loads':loads,'sixth_determinant':str(actual),'equal':True});signal.alarm(0)
    # Fingerprint damage and a genuinely negative translated constant.
    original=final[0];require((original+1).fingerprint()!=original.fingerprint(),'changed final coefficient fingerprint')
    damaged=dict(final);a=dict(original.a);constant=coeff.evaluate(original,(3,2,1))*original.den
    require(constant.denominator==1,'integral translated numerator constant')
    a[coeff.ZERO]=a.get(coeff.ZERO,0)-int(constant)-1;damaged[0]=CP(a,original.den)
    try:certify_Q(damaged)
    except ValueError:pass
    else:raise ValueError('negative final translated Q0 accepted')
    result={'agent':'six-downset-1','role':'researcher','status':'all twelve rational functions strictly positive','raw_field':'QQ(Q,D,t,v),q=Q+4','sign_domain':'Q,B,T,V>=0;D=t+B+1,t=v+T+1,v=V+1','positive_functions':rows,'denominator_factor_certificates':[{**factors[k],'factor_sha256':k} for k in sorted(factors)],'positive_rational_functions':12,'numerator_Q_coefficient_lemmas':sum(len(r['numerator']['Q_coefficients']) for r in rows),'shifted_numerator_terms':sum(r['numerator']['total_shifted_coefficient_terms'] for r in rows),'positive_factor_hints':hints,'first_four_determinant_permutations':[1,2,6,24],'generic_border_audit':stable(generic),'final_factored_summands':summands,'whole_physical_point_controls':points,'Q_convolution_schoolbook_controls':9,'polynomial_schoolbook_controls':36,'direct_power_shift_controls':3,'shift_point_controls_per_coefficient':2,'changed_coefficient_fingerprint_rejected':True,'negative_translated_Q0_rejected':True,'raw4_expanded_sixth_numerator_constructed':False,'external_polynomial_or_cache_inputs':False,'CAS_imports':False,'per_polynomial_term_guard':30000,'packing_bytes_guard':33554432,'stage_or_coefficient_seconds_guard':60,'elapsed_seconds':time.monotonic()-started,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.expected:require(stable(result)==stable(json.loads(args.expected.read_text())['signs']),'frozen universal sign certificate mismatch')
    if args.write:args.write.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
