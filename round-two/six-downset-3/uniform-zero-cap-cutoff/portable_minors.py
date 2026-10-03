"""Regenerate canonical cap minors with stdlib integer polynomial arithmetic.

No CAS-generated minor is a premise. Jacobi cancellations are exact
polynomial divisions with full multiplied-back identities. Positivity
of the unreduced denominators follows from the earlier fullspace cap.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,time
import portable_frame as f
import portable_fields as fields
import ipoly as z
require=f.require
Q,K={(1,0):1},{(0,1):1}
C=lambda value:{(0,0):int(value)} if value else {}
A,M,S=z.add,z.mul,z.scale


def decode(xs):
    poly=f.decode(xs)
    require(all(v.denominator==1 for v in poly.values()),'ENTIRE input integer polynomial encoding')
    return {power:int(value) for power,value in poly.items()}


def matrix_decode(rows):return [[decode(v) for v in row] for row in rows]
def record(poly):return [[list(power),str(value)] for power,value in sorted(poly.items())]
def matrix_record(G):return [[record(v) for v in row] for row in G]


def divide(num,den):
    require(bool(den),'whole polynomial denominator nonzero')
    rest=dict(num);out={};power,leading=max(den.items())
    while rest:
        position,value=max(rest.items())
        delta=position[0]-power[0],position[1]-power[1]
        require(min(delta)>=0,'ENTIRE exact integer polynomial monomial division')
        coefficient,remainder=divmod(value,leading)
        require(remainder==0,'ENTIRE exact integer polynomial coefficient division')
        out[delta]=out.get(delta,0)+coefficient
        for (i,j),number in den.items():
            target=i+delta[0],j+delta[1]
            next_value=rest.get(target,0)-coefficient*number
            if next_value:rest[target]=next_value
            elif target in rest:del rest[target]
    out=z.clean(out)
    require(M(out,den)==num,'EVERY coefficient of multiplied-back whole division identity')
    return out


def data(bound=False):
    raw=f.generated()|fields.generated()
    # Full exact source binding, not merely an input digest.
    frame=f.verify(raw)
    fields.fields(raw)
    d=decode(raw['complete_seven_determinant'])
    H=matrix_decode(raw['complete_four_short_numerator'])
    W=matrix_decode(frame['complete_border_minors_divided_by_original_determinant'])
    nn,nd=(decode(raw['nu_U'][side]) for side in ('numerator','denominator'))
    an,ad=(decode(raw['a0'][side]) for side in ('numerator','denominator'))
    for i in range(3):
        for j in range(3):
            require(M(W[i][j],d)==A(M(H[i][j],H[3][3]),S(M(H[i][3],H[j][3]),-1)),
                    'EVERY complete supplied target-border division coefficient')
    T=A(S(M(M(M(Q,d),K),nn),4),M(M(A(Q,S(K,-1)),H[3][3]),nd))
    P=[[A(S(M(M(M(Q,K),nn),H[i][j]),4),M(M(A(Q,S(K,-1)),nd),W[i][j])) for j in range(3)] for i in range(3)]
    repair=[[{},S(an,2),{}],[S(an,2),A(S(an,-3),S(ad,2)),S(an,-2)],[{},S(an,-2),{}]]
    MM=[[A(M(ad,P[i][j]),S(M(T,repair[i][j]),-1)) for j in range(3)] for i in range(3)]
    require(all(MM[i][j]==MM[j][i] for i in range(3) for j in range(3)),'ENTIRE canonical even cap reciprocity')
    # Complete normalization controls, including a failed-cap point.
    controls=[]
    for q,k in ((21,7),(28,7),(100,20)):
        a0=f.cap.v.zero_coefficients(q,k)[0]
        direct=f.cap.direct(q,k,a0/4,-3*a0/8+F(1,4))
        common=4*z.evaluate(ad,q,k)*z.evaluate(T,q,k)
        require(common>0,'positive entire canonical cap denominator controls')
        actual=[[F(z.evaluate(MM[i][j],q,k),common) for j in range(3)] for i in range(3)]
        require(actual==direct,'ALL9 complete independently original23 cap entries')
        controls.append({'q':q,'k':k,'canonical_even_equals_original':True})
    return {'d':d,'H':H,'W':W,'T':T,'P':P,'ad':ad,'M':MM,'controls':controls,
            'bound':bound}


def numerator(data,order):
    MM,T,ad=data['M'],data['T'],data['ad']
    if order==1:return data['P'][0][0],S(T,4)
    first=divide(A(M(MM[0][0],MM[1][1]),S(M(MM[0][1],MM[0][1]),-1)),T)
    if order==2:return first,S(M(M(ad,ad),T),16)
    require(order==3,'whole minor order')
    other=divide(A(M(MM[0][0],MM[2][2]),S(M(MM[0][2],MM[0][2]),-1)),T)
    cross=divide(A(M(MM[0][0],MM[1][2]),S(M(MM[0][1],MM[0][2]),-1)),T)
    final=divide(A(M(first,other),S(M(cross,cross),-1)),M(MM[0][0],ad))
    # Ordinary 3x3 Jacobi identity gives detM=T^2 ad*final.
    return final,S(M(M(ad,ad),T),64)


def whole_sign(num):
    # Only these twelve integer k are needed below the radical tail.
    finite=[z.fixed_k(num,z.cutoff(k),k) for k in range(7,19)]
    require(all(row['negative_count']==0 and row['positive_constant'] for row in finite),
            'EVERY coefficient of all twelve full-q shifted polynomials positive')
    tail=z.curve_certificate(num,19,4,1)
    require(tail['is_completed_certificate'],
            'EVERY coefficient of the entire quadratic-field radical tail lower bound positive')
    # Establish the two radical bounds algebraically at k=19+x.
    require(z.surd_sign(180,-68)>0,'17/5 lower envelope slope below sqrt discriminant')
    require(81*25-17**2>0,'strict lower envelope constant')
    require(z.surd_sign(-36,16)>0 and z.surd_sign(-749,304)>0,
            'whole upper4 envelope has positive slope and constant at19')
    require(all(z.cutoff(k)>=3*k for k in range(7,19)),
            'each finite cutoff respects original count domain')
    # For real k>=19, the radical curve is >=3k:
    # P>17/5+2sqrt7*k>29; qcurve-3k=(P-29)/2>0.
    require(z.surd_sign(17-29*5,19*10)>0,'radical tail curve lies inside q>=3k')
    return {'finite_integer_k_whole_q_certificates':finite,'all_k19_plus_radical_tail':tail,
            'tail_ordinary_domain':'ALL realk>=19,u>=0 with q=(6k-29+sqrt(28k^2+36k+81))/2+u',
            'whole_coverage':'ALL integerk>=7,q>=ceil((6k-25+sqrt(28k^2+36k+81))/2)-2',
            'radical_bounds_checked_exactly':True,'all_domain_count_constraints_checked':True}


def verify(order=1,bound=False):
    value=data(bound);n,d=numerator(value,order)
    sign=whole_sign(n)
    return {'actual_agent':'six-downset-3','role':'researcher','minor_order':order,
            'CAS_minor_not_a_premise':True,'full_original_field_binding_performed':bound,
            'complete_regenerated_minor_numerator':record(n),
            'numerator_degrees':[max(i for i,j in n),max(j for i,j in n)],
            'numerator_count':len(n),'whole_sign_certificate':sign,
            'positive_denominator':'4T for1; 16ad^2T for2;64ad^2T for3. ad>0,T>0 by complete field/source binding and ordinary untouched cap premise',
            'every_polynomial_division_multiplied_back':True,'source_only_regeneration':True,
            'whole_original_controls':value['controls'],'independent_person_review':False}


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--order',type=int,required=True);ap.add_argument('--bound',action='store_true');ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    start=time.monotonic();value=verify(args.order,args.bound);args.out.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'order':args.order,'whole_all_counts_cutoff_sign':True,'numerator_count':value['numerator_count'],'seconds':time.monotonic()-start}))
