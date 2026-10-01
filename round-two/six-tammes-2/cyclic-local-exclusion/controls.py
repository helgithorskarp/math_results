#!/usr/bin/env python3
"""Reject perturbations that destroy the mathematical certificate."""
import copy
from fractions import Fraction as Q
import json
from pathlib import Path
import audit
import check

def controls():
    original=json.loads(Path(__file__).with_name('certificate.json').read_text())
    cases=[]
    d=copy.deepcopy(original)
    for edge in d['orbits'][0]:
        k=d['edges'].index(edge)
        d['weights'][k][0]=str(Q(d['weights'][k][0])+Q(1,1000))
    cases.append(('positive_but_nonequilibrium_orbit',d))
    d=copy.deepcopy(original)
    d['weights']=[[str(-Q(x)) for x in w] for w in d['weights']]
    cases.append(('negative_equilibrium_stress',d))
    d=copy.deepcopy(original)
    d['vectors'][14][0][0]=str(Q(d['vectors'][14][0][0])+Q(1,1000))
    cases.append(('changed_cyclic_point',d))
    d=copy.deepcopy(original);d['inverse_numerators']=[[0]*45 for _ in range(45)]
    cases.append(('zero_inverse',d))
    d=copy.deepcopy(original);d['inverse_numerators'][0][0]+=d['inverse_scale']
    cases.append(('inverse_unit_entry_error',d))
    d=copy.deepcopy(original);d['selected_edges'][0]=d['selected_edges'][1]
    cases.append(('duplicate_contact_row',d))
    rejected=[]
    for name,d in cases:
        for label,verify in (('primary',lambda x:check.verify(x,False)),('audit',audit.audit)):
            try:verify(d)
            except ValueError:pass
            else:raise ValueError(label+' accepted damaged certificate '+name)
        rejected.append(name)
    return {'status':'VERIFIED','rejected_by_both':rejected,'negative_controls':len(rejected)}

if __name__=='__main__':
    print(json.dumps(controls(),sort_keys=True))
