#!/usr/bin/env python3
"""Reject broken algebra, omitted physical edges, bad colours and wrong roots."""
from copy import deepcopy
import json
from pathlib import Path
import exact as X
import physical
import verify

HERE=Path(__file__).resolve().parent


def reject(name, action, fragment):
    try:
        action()
    except ValueError as error:
        X.need(fragment in str(error), name+': intended validation boundary')
        return name
    raise ValueError(name+': corrupt certificate accepted')


def main():
    cert=json.loads((HERE/'certificate.json').read_text())
    unique=[]
    for terms in cert['factorizations']:
        value=[1]
        for i,e in terms:
            for _ in range(e):
                value=X.mul(value,cert['blocks'][i])
        unique.append(tuple(value))
    broken=deepcopy(cert)
    broken['factorizations'][0][0][1]+=1
    passed=[reject('wrong_factor_multiplicity',lambda:verify.check_products(broken,unique),'factorization product')]
    passed.append(reject('shared_root_blocks',lambda:verify.modular_audit([[-1,1],[-1,0,1]]),'coprimality'))
    fixture=json.loads((HERE/'physical.json').read_text())
    omitted=deepcopy(fixture)
    omitted['graphs'][0]['edges'].pop()
    passed.append(reject('omitted_strict_unit_edge',lambda:physical.verify(omitted),'all and only strict unit edges'))
    colour=deepcopy(fixture)
    a,b=colour['graphs'][0]['edges'][0]
    colour['graphs'][0]['colouring'][a]=colour['graphs'][0]['colouring'][b]
    passed.append(reject('monochromatic_unit_edge',lambda:physical.verify(colour),'proper colouring'))
    interval=deepcopy(fixture)
    interval['real_generator_isolating_interval']=[[3,5],[7,10]]
    passed.append(reject('wrong_real_root_interval',lambda:physical.verify(interval),'unique isolated real root'))
    print(json.dumps({'passed':True,'rejected_corruptions':passed},indent=2,sort_keys=True))


if __name__=='__main__':
    main()
