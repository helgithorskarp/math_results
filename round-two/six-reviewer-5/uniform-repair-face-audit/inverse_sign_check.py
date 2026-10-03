"""Different-algorithm whole positivity checker: invert both binomial shifts."""
import json,math,sys
from pathlib import Path
from fractions import Fraction as F
from shift_signs import polynomial
from literal_check import require
P=Path(__file__).resolve().parent
def unshift(p):
    den=math.lcm(*(c.denominator for c in p.values()));ints={e:c.numerator*(den//c.denominator) for e,c in p.items()}
    mid={};out={};xweights={};uweights={}
    # x=k-7, then u=q-3k. This is the inverse of the generator.
    for (i,j),c in ints.items():
        if i not in xweights:xweights[i]=[math.comb(i,t)*(-7)**(i-t) for t in range(i+1)]
        for t,w in enumerate(xweights[i]):mid[(t,j)]=mid.get((t,j),0)+c*w
    for (i,j),c in mid.items():
        if not c:continue
        if j not in uweights:uweights[j]=[math.comb(j,t)*(-3)**(j-t) for t in range(j+1)]
        for t,w in enumerate(uweights[j]):out[(t,i+j-t)]=out.get((t,i+j-t),0)+c*w
    return {e:F(c,den) for e,c in out.items() if c}
def main():
    kind=sys.argv[1];records=json.loads((P/('cap-signs.json' if kind=='cap' else 'optimization-signs.json')).read_text())['certificates']
    if kind=='cap':
        psi=json.loads((P/'psi-polynomials.json').read_text());v=json.loads((P/'cap-vector-polynomials.json').read_text())
        expressions=dict(psi_leading=psi['raw_leading'],psi_determinant=psi['reduced_determinant'],vector_denominator=v['denominator'],standard_denominator=v['standard_denominator'])
    else:expressions=json.loads((P/'optimization-polynomials.json').read_text())
    if '--damage' in sys.argv:
        r=records[next(iter(records))]['coefficients'];r[len(r)//2][1]=str(F(r[len(r)//2][1])+1)
    counts={}
    for name,rec in records.items():
        coeff={}
        for ee,cc in rec['coefficients']:
            e=tuple(ee);c=F(cc);require(e not in coeff and len(e)==2 and all(type(v) is int and v>=0 for v in e),'entire coefficient schema')
            require(c>0,'every listed coefficient positive');coeff[e]=c
        require(coeff.get((0,0),F(0))>0,'strict constant')
        require(unshift(coeff)==polynomial(expressions[name]),'ENTIRE inverse coefficient identity '+name)
        counts[name]=len(coeff);print(name,len(coeff),flush=True)
    (P/('inverse-'+kind+'-result.json')).write_text(json.dumps(dict(status='entire inverse shift identities verified',counts=counts,total_coefficients=sum(counts.values()),CAS_imported=False),indent=2)+'\n')
if __name__=='__main__':main()
