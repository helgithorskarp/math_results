"""Independent Horner arithmetic in QQ[k,m]/(m^2-7k^2-1), no CAS."""
from pathlib import Path
import json,math
from fractions import Fraction as F
from shift_signs import polynomial
from literal_check import require
P=Path(__file__).resolve().parent

def add(a,b):
    out=dict(a)
    for e,c in b.items():out[e]=out.get(e,F(0))+c
    return {e:c for e,c in out.items() if c}
def mul(a,b):
    out={}
    for e,c in a.items():
        for ee,cc in b.items():out[e+ee]=out.get(e+ee,F(0))+c*cc
    return {e:c for e,c in out.items() if c}

def reduce_horner(p,offset):
    byq={}
    for (i,j),c in p.items():byq.setdefault(i,{})[j]=c
    A={};H={};base={0:F(offset),1:F(3)};square={0:F(1),2:F(7)}
    for i in range(max(byq),-1,-1):
        A,H=add(mul(A,base),mul(H,square)),add(A,mul(H,base))
        A=add(A,byq.get(i,{}))
    return A,H

def shift(p):
    out={}
    for n,c in p.items():
        for j in range(n+1):out[j]=out.get(j,F(0))+c*math.comb(n,j)*48**(n-j)
    return {e:c for e,c in out.items() if c}

def sign_quad(a,b):
    if not b:return (a>0)-(a<0)
    if not a:return (b>0)-(b<0)
    sa=(a>0)-(a<0);sb=(b>0)-(b<0)
    if sa==sb:return sa
    n=a*a-7*b*b
    require(n!=0,'irrational sqrt7 norm cannot vanish for nonzero rational pair')
    return sa if n>0 else sb

def ev(p,k):return sum((c*k**e for e,c in p.items()),F(0))

def main():
    raw=json.loads((P/'optimization-polynomials.json').read_text());p=polynomial(raw['R_numerator']);out={}
    for label,offset,wanted in (('minus',-14,-1),('plus',-13,1)):
        A,H=reduce_horner(p,offset);hs=shift(H);a=shift(A);b=shift({n+1:c for n,c in H.items()})
        require(all(wanted*c>0 for c in hs.values()) and wanted*hs.get(0,0)>0,'ENTIRE Pell H coefficient sign '+label)
        pairs=[(n,a.get(n,F(0)),b.get(n,F(0))) for n in sorted(set(a)|set(b),reverse=True)]
        require(all(sign_quad(c,d)==wanted for n,c,d in pairs) and sign_quad(a.get(0,F(0)),b.get(0,F(0)))==wanted,'ENTIRE QQsqrt7 Pell lower/upper coefficient sign '+label)
        # Original q,k numerator evaluations at three actual Pell solutions.
        controls=[];m,k=8,3
        for n in range(2,5):
            m,k=8*m+21*k,3*m+8*k;q=3*k+offset+m
            value=sum((c*q**i*k**j for (i,j),c in p.items()),F(0))
            require(value==ev(A,k)+m*ev(H,k) and ((value>0)-(value<0))==wanted,'original Pell quotient/control binding')
            controls.append(dict(n=n,m=m,k=k,q=q,value=str(value)))
        out[label]=dict(offset=offset,A=[[e,str(A[e])] for e in sorted(A,reverse=True)],H=[[e,str(H[e])] for e in sorted(H,reverse=True)],
                       H_shift=[[e,str(hs[e])] for e in sorted(hs,reverse=True)],quadratic_shift=[[e,str(c),str(d)] for e,c,d in pairs],controls=controls)
        print(label,'H coefficients',len(hs),'QQsqrt7 coefficients',len(pairs),flush=True)
    (P/'pell-result.json').write_text(json.dumps(dict(status='EVERY n>=2 adjacent Pell numerator signs',data=out,
       trust='positive original R denominator and criterion checked separately; ordinary Pell/quotient bridge unformalized',CAS_imported=False),indent=2)+'\n')

if __name__=='__main__':main()
