#!/usr/bin/env python3
"""Identity corruption checks and the indispensable exceptional relaxation."""
from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path
import exact as X

HERE=Path(__file__).resolve().parent


def reject(name,certificate,keys):
    try:X.check_identities(certificate,keys)
    except ValueError:return name
    raise ValueError(name+': corrupt certificate accepted')


def diagonal_mod_quadratic(poly):
    # U=V=t, 4t^2+t+1=0, coefficients in Q(omega).
    values={}
    for (i,j),c in poly.items():values[i+j]=X.add(values.get(i+j,X.ZERO),c)
    while values and max(values)>=2:
        degree=max(values);a,b=values.pop(degree);quot=(Fraction(a)/4,Fraction(b)/4)
        for k in (degree-2,degree-1):
            values[k]=X.add(values.get(k,X.ZERO),(-quot[0],-quot[1]))
            if values[k]==X.ZERO:del values[k]
    return values


def run():
    cert=json.loads((HERE/'certificate.json').read_text())
    keys=[tuple(tuple(tuple(d) for d in row) for row in e['normalized_rows']) for e in cert['normal_forms']]
    X.need(X.check_identities(cert,keys)==33,'positive identity control')
    changed=deepcopy(cert);changed['normal_forms'][1]['identities'][0]['multipliers'][0][0][2]+=1
    rejected=[reject('wrong_Eisenstein_multiplier',changed,keys)]
    changed=deepcopy(cert);changed['normal_forms'].pop()
    rejected.append(reject('missing_normal_form',changed,keys))
    changed=deepcopy(cert);changed['normal_forms'][0]['identities']=deepcopy(cert['normal_forms'][1]['identities'])
    rejected.append(reject('erased_exceptional_power_step',changed,keys))
    changed=deepcopy(cert);changed['normal_forms'][4]['identities'][0]['multipliers']=[[],[],[]]
    rejected.append(reject('zero_identity_witness',changed,keys))
    X.need(all(not diagonal_mod_quadratic(g) for g in X.equations(keys[0])),'exceptional two-vector relaxation really has solutions')
    X.need(diagonal_mod_quadratic(X.D2),'exceptional solutions have nonzero denominator')
    X.need(all(4**(j-i)!=1 for i in range(1,5) for j in range(i+1,5)),'all six distinct exponent pairs give contradiction')
    return {'passed':True,'rejected_corruptions':rejected,'exceptional_relaxation_retained':True,'power_compatibility_needed':True}


if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
