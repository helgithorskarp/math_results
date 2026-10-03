"""Whole quadrant anchor, interior vertex and residual denominator signs."""
import json
from pathlib import Path
from shift_signs import polynomial,shifted
from literal_check import require
P=Path(__file__).resolve().parent

def main():
    rec=json.loads((P/'optimization-polynomials.json').read_text());cert={}
    for name in ('M_denominator','H_leading','H_determinant','vertex_denominator','vertex_lower','vertex_upper','R_denominator'):
        p=polynomial(rec[name]);c=shifted(p)
        require(all(v>0 for v in c.values()) and c.get((0,0),0)>0,'complete quadrant sign '+name)
        cert[name]={'variables':['x','u'],'degree':max(sum(e) for e in c),'coefficients':[[list(e),str(c[e])] for e in sorted(c,reverse=True)]}
        print(name,len(c),'strictly positive coefficients',flush=True)
    out=dict(status='H positive/interior t/R positive denominator on ENTIRE quadrant',certificates=cert,
             trust='complete field/minor identities unformalized; nonfixed/odd/recovery premises remain credited9980')
    (P/'optimization-signs.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
