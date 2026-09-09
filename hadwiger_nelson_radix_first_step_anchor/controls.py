#!/usr/bin/env python3
"""Reject corrupt exact factors, roots, colours, collisions, and modular shortcuts."""
from copy import deepcopy
import json
from pathlib import Path
import common as C
import verify as V
X=C.X;HERE=Path(__file__).resolve().parent


def rejects(name,operation):
    try:operation()
    except (ValueError,StopIteration):return name
    raise ValueError('corruption was accepted: '+name)


def run():
    cert=json.loads((HERE/'certificate.json').read_text())
    factors,qs,base,groups=V.inventory();unique=sorted(set(qs[0])-{()})
    bypoly=V.check_products(cert,unique);results=[]
    bad=deepcopy(cert);bad['factorizations'][0][0]+=1
    results.append(rejects('wrong factor product',lambda:V.check_products(bad,unique)))
    roots=cert['real_root_counts'][:];roots[0]+=1
    results.append(rejects('wrong Sturm real-root count',lambda:C.root_audit(cert['blocks'],roots)))
    bad=deepcopy(cert);i=cert['blocks'].index([-1,0,21]);bad['colour_assignments'][0][i]=0
    results.append(rejects('first-digit word on the eight-curve physical block',lambda:V.check_colours(bad,qs,bypoly,base,groups)))
    bad=deepcopy(cert);bad['collision_witnesses'][0]['rows'][0]=[[1,0]]+[[0,0]]*4
    results.append(rejects('false physical collision witness',lambda:V.check_colours(bad,qs,bypoly,base,groups)))
    p=X.PRIMES[0]
    X.need(X.gcd_is_one([1,p],[1,p],p),'control exhibits misleading degree-dropping modular gcd')
    results.append(rejects('degree-dropping modular coprimality shortcut',lambda:V.modular_audit([[1,p],[1,p]],[1,1])))
    results.append(rejects('inseparable repeated factor',lambda:V.modular_audit([[1,2,1]],[1])))
    return {'verified':True,'rejected':results,'uses_assert_for_correctness':False}


if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
