"""Stdlib exact binomial shift certificate for the physical rank-two cap form.

Substitute q=3k+u first, then k=7+x. No sample or CAS positivity test.
"""
import json,math
from fractions import Fraction as F
from pathlib import Path
from parse_exact import rational
from literal_check import require
P=Path(__file__).resolve().parent

def polynomial(text):
    a,b=rational(text)
    require(set(b)=={(0,0)},'constant polynomial denominator')
    return {e:c/b[(0,0)] for e,c in a.items()}

def shifted(a):
    den=math.lcm(*(c.denominator for c in a.values()))
    ints={e:c.numerator*(den//c.denominator) for e,c in a.items()}
    middle={};out={};qweights={};kweights={}
    for (i,j),c in ints.items():
        if i not in qweights:qweights[i]=[math.comb(i,l)*3**(i-l) for l in range(i+1)]
        for l,w in enumerate(qweights[i]):
            e=(i-l+j,l);middle[e]=middle.get(e,0)+c*w
    for (i,j),c in middle.items():
        if not c:continue
        if i not in kweights:kweights[i]=[math.comb(i,t)*7**(i-t) for t in range(i+1)]
        for t,w in enumerate(kweights[i]):
            e=(t,j);out[e]=out.get(e,0)+c*w
    return {e:F(c,den) for e,c in out.items() if c}

def main():
    psi=json.loads((P/'psi-polynomials.json').read_text());vec=json.loads((P/'cap-vector-polynomials.json').read_text())
    data={}
    for name,text in [('psi_leading',psi['raw_leading']),('psi_determinant',psi['reduced_determinant']),
                       ('vector_denominator',vec['denominator']),('standard_denominator',vec['standard_denominator'])]:
        c=shifted(polynomial(text))
        require(all(v>=0 for v in c.values()) and c.get((0,0),F(0))>0,'whole quadrant sign '+name)
        data[name]={'variables':['x','u'],'degree':max(sum(e) for e in c),'coefficients':[[list(e),str(c[e])] for e in sorted(c,reverse=True)],
                    'strict_constant':str(c[(0,0)])}
        print(name,len(c),'nonzero positive coefficients',flush=True)
    out={'status':'full physical rank-two Psi cap certificate, whole q>=3k,k>=7','certificates':data,
         'scope':'Delta_cap + s0s0^T/(2q^4) positive on two relevant directions; no vertex/R/Pell verdict',
         'CAS_used_for_signs':False,'finite_samples_used_as_uniformity':False}
    (P/'cap-signs.json').write_text(json.dumps(out,indent=2)+'\n')
    print('all cap signs saved',flush=True)

if __name__=='__main__':main()
