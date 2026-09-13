#!/usr/bin/env python3
"""Positive free-vector witnesses, essential hypotheses, and corrupt certificates."""
import copy
from fractions import Fraction as Q
import json
from pathlib import Path
import exact as E
import verify as V


def reject(function,message):
    try:function()
    except ValueError as exc:
        E.need(message in str(exc),'wrong corruption rejection: '+str(exc))
    else:raise ValueError('corruption was accepted')


def main():
    cases=[((1,1,1,1,1),(Q(0),Q(1,2),Q(0),Q(1,2)),(Q(1,4),)*3),
           ((-1,-1,-1,-1,-1),(Q(0),Q(1,2),Q(1,2),Q(0)),(Q(3,4),Q(7,4),Q(1,4)))]
    for signs,point,norms in cases:
        F,N=E.equations(signs)
        E.need(all(E.eval_poly(f,point)==0 for f in F),'positive free-vector witness')
        E.need(tuple(E.eval_poly(n,point) for n in N)==norms,'exact witness radii')
    # The first is U=V=W=1/2: equal exponents really would permit concurrence.
    certificate=json.loads((Path(__file__).parent/'certificate.json').read_text())
    reject(lambda:V.identity_audit(certificate[:-1]),'case count')
    bad=copy.deepcopy(certificate)
    for identity in bad[0]['identities']:
        nonempty=next((h for h in identity if h),None)
        if nonempty:
            nonempty[0][1]=str(Q(nonempty[0][1])+1);break
    reject(lambda:V.identity_audit(bad),'defining-ideal identity')
    bad=copy.deepcopy(certificate)
    next(c for c in bad if not c['delta_zero'])['delta_zero']=True
    reject(lambda:V.identity_audit(bad),'equal-radius consequence')
    bad=copy.deepcopy(certificate);bad[0]['basis']=[];bad[0]['identities']=[]
    reject(lambda:V.identity_audit(bad),'nonzero consequence')
    rows=[((1,0),(1,0),(0,0)),((1,0),(0,0),(1,0)),((0,0),(1,0),(1,0)),
          ((1,0),(0,1),(-1,1)),((1,0),(-1,1),(0,1))]
    E.need(V.normalized_signs(rows)==(1,1,1,1,1),'normalization fixture')
    reject(lambda:V.normalized_signs(rows[:-1]+[rows[-2]]),'two full sections')
    print(json.dumps({'status':'PASS','exact_free_vector_witnesses':2,'corruptions_rejected':5,
                      'equal_exponents_counterexample':True,'no_free_vector_nonconcurrence_claim':True},sort_keys=True))


if __name__=='__main__':main()
