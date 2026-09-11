"""Recompute every stored bound, without trusting the stored search history."""
import json,sys
from pathlib import Path
from fractions import Fraction
from math import comb
from envelope import certify
out=[]
for i,z in enumerate(json.loads(Path(__file__).with_name('certificates.json').read_text())):
 N,L=z['N'],z['L'];rows=tuple(map(tuple,z['rows']));B=Fraction(z['bound'])
 assert (B*comb(N,L)).denominator==1
 result=certify(N,L,rows,B+Fraction(1,comb(N,L)))
 assert result['status']=='certified',result
 assert Fraction(result['bound'])<=B,result
 out.append(result)
 print('certificate',i+1,'verified',file=sys.stderr,flush=True)
print(json.dumps(out,indent=2,sort_keys=True))
