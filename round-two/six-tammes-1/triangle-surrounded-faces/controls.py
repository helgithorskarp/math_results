"""Damaged certificate rejection plus exact known antiprism closures."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as Q
import json
import audit
import check
from poly import divrem

def require(x,m):
    if not x:raise ValueError(m)

data=json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
cases=[]
x=deepcopy(data);x['records'].pop();cases.append(('missing-closure-word',x))
x=deepcopy(data);x['records'][-1]=deepcopy(x['records'][0]);cases.append(('duplicate-closure-word',x))
x=deepcopy(data);x['records'][0]['gaps'][0][0]='123';cases.append(('damaged-transfer-coordinate',x))
x=deepcopy(data);x['records'][0]['bezout'][0][0]=str(Q(x['records'][0]['bezout'][0][0])+1);cases.append(('damaged-Bezout-multiplier',x))
x=deepcopy(data);x['records'][0]['bernstein'][0]=str(-Q(x['records'][0]['bernstein'][0]));cases.append(('opposite-Bernstein-sign',x))
x=deepcopy(data);x['records'][0]['combination']=[];cases.append(('zero-obstruction',x))
x=deepcopy(data);x['records'][0]['hexagonal_exception']=True;cases.append(('unjustified-exception',x))
x=deepcopy(data);x['hexagon']['root_polynomial'][0]='-3';cases.append(('wrong-hexagonal-root',x))
x=deepcopy(data);x['hexagon']['vectors'][0][0]=[];cases.append(('changed-reference-point',x))
x=deepcopy(data);x['hexagon']['gram'][0][6]=['1'];cases.append(('changed-cross-Gram-contact',x))
x=deepcopy(data);x['cap']['rho']='19/20';cases.append(('changed-cap-radius',x))
x=deepcopy(data);x['cap']['total_points_at_most']=15;cases.append(('false-capacity-conclusion',x))
rejected=[]
for name,x in cases:
    try:audit.verify(x)
    except ValueError:rejected.append(name)
    else:raise ValueError('damaged input accepted: '+name)

# A nonzero rescaling of the actual Bezout/sign witness is valid.
valid=deepcopy(data)
row=valid['records'][0]
for key in ('combination','bernstein'):row[key]=[str(2*Q(s)) for s in row[key]]
row['bezout']=[[str(2*Q(s)) for s in p] for p in row['bezout']]
audit.verify(valid)

# Calibration against exact antiprism closures: no sampled real root is used.
calibrations=[]
for n,modulus in ((4,[-1,2,1]),(5,[-1,1,1]),(6,[-2,2,1])):
    h=list(map(Q,modulus));gaps=check.closure((3,)*(n-1))
    require(all(not divrem(g,h)[1] for g in gaps),'known all-three antiprism closure')
    matrix=audit.transfer([3]*n)
    for i in range(3):
        for j in range(3):
            p=[matrix[i][j].get(k,Q(0)) for k in range(max(matrix[i][j],default=-1)+1)]
            if i==j:
                if not p:p=[Q(-1)]
                else:p[0]-=1
            require(not divrem(p,h)[1],'known antiprism full state return')
    calibrations.append({'sides':n,'quadratic':modulus,'all_closure_coordinates_zero_mod_quadratic':True,'entire_state_returns':True})
print(json.dumps({'rejected':rejected,'valid_rescaled_Bezout_and_sign_witness_accepted':True,
                  'known_exact_antiprism_calibrations':calibrations},sort_keys=True))
