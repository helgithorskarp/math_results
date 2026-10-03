"""Independent expanded substitution and monic long division in QQ[k,m]."""
import json,math,sys
from pathlib import Path
from fractions import Fraction as F
from shift_signs import polynomial
from literal_check import require
P=Path(__file__).resolve().parent
def cleaned(p):return {e:c for e,c in p.items() if c}
def univariate_shift_back(p):
    out={}
    for i,c in p.items():
        for j in range(i+1):out[j]=out.get(j,F(0))+c*math.comb(i,j)*(-48)**(i-j)
    return cleaned(out)
def expanded(p,c):
    out={}
    for (i,j),v in p.items():
        for m in range(i+1):
            for k in range(i-m+1):
                e=(j+k,m);cc=v*math.comb(i,m)*math.comb(i-m,k)*3**k*c**(i-m-k)
                out[e]=out.get(e,F(0))+cc
    return cleaned(out)
def divide(original):
    rem=dict(original);quot={}
    for m in range(max(e[1] for e in rem),1,-1):
        for (k,j),c in list(rem.items()):
            if j!=m:continue
            del rem[(k,j)];quot[(k,j-2)]=quot.get((k,j-2),F(0))+c
            for e,v in (((k+2,j-2),7*c),((k,j-2),c)):rem[e]=rem.get(e,F(0))+v
        rem=cleaned(rem)
    multiply=dict(rem)
    for (k,m),c in quot.items():
        for e,v in (((k,m+2),c),((k+2,m),-7*c),((k,m),-c)):multiply[e]=multiply.get(e,F(0))+v
    require(cleaned(multiply)==original,'ENTIRE quotient-times-divisor plus remainder identity')
    require(all(m in (0,1) for k,m in rem),'complete monic remainder')
    return rem,cleaned(quot)
def rational_pair_sign(a,b):
    # Independent comparison by interval/rational squaring, no producer sign function.
    if a>=0 and b>=0:return 1 if a or b else 0
    if a<=0 and b<=0:return -1
    if a>0:return 1 if a*a>7*b*b else -1
    return 1 if 7*b*b>a*a else -1
def main():
    raw=json.loads((P/'optimization-polynomials.json').read_text());proof=json.loads((P/'pell-result.json').read_text())['data'];N=polynomial(raw['R_numerator']);counts={}
    if '--damage' in sys.argv:proof['minus']['A'][len(proof['minus']['A'])//2][1]=str(F(proof['minus']['A'][len(proof['minus']['A'])//2][1])+1)
    for label,c,wanted in (('minus',-14,-1),('plus',-13,1)):
        original=expanded(N,c);rem,quot=divide(original);rec=proof[label]
        A={e:F(v) for e,v in rec['A']};H={e:F(v) for e,v in rec['H']}
        expected={(k,0):v for k,v in A.items()};expected.update({(k,1):v for k,v in H.items()})
        require(rem==expected,'ALL independent Pell remainder coefficients '+label)
        hs={e:F(v) for e,v in rec['H_shift']};require(univariate_shift_back(hs)==H and all(wanted*v>0 for v in hs.values()) and wanted*hs[0]>0,'whole H shift identity/sign')
        aa={e:F(a) for e,a,b in rec['quadratic_shift'] if F(a)};bb={e:F(b) for e,a,b in rec['quadratic_shift'] if F(b)}
        require(univariate_shift_back(aa)==A and univariate_shift_back(bb)=={e+1:v for e,v in H.items()},'ALL quadratic shift identities')
        require(all(rational_pair_sign(F(a),F(b))==wanted for e,a,b in rec['quadratic_shift']) and rational_pair_sign(aa[0],bb[0])==wanted,'ALL independent quadratic signs')
        counts[label]=dict(expanded_terms=len(original),quotient_terms=len(quot),remainder_terms=len(rem),H_shift_terms=len(hs),quadratic_shift_terms=len(rec['quadratic_shift']))
        print(label,counts[label],flush=True)
    (P/'pell-division-result.json').write_text(json.dumps(dict(status='entire different-algorithm Pell quotient and shifted coefficients verified',counts=counts,CAS_imported=False),indent=2)+'\n')
if __name__=='__main__':main()
