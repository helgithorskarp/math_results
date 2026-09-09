#!/usr/bin/env python3
"""Six rejection controls, including under optimized Python."""
import copy
import json
import tempfile
from pathlib import Path
import verify
from common import HERE, X


def run():
    original = json.loads((HERE/'certificate.json').read_text())
    cases = []
    d = copy.deepcopy(original);d['modular_prime'] = 1000005
    cases.append(('composite proof modulus',d,'prime proof modulus'))
    d = copy.deepcopy(original);d['charts'][0]['q'][0] += 2
    cases.append(('false eliminant factor',d,'complete exact eliminant factor product'))
    d = copy.deepcopy(original);d['charts'][0]['x'][0] = '1'
    cases.append(('false physical x coordinate',d,'complete linear fibre'))
    d = copy.deepcopy(original);d['charts'][0]['isolating_intervals'].pop()
    cases.append(('omitted real embedding',d,'every real root covered'))
    d = copy.deepcopy(original);d['charts'][0]['closed_unit_circle'] = True
    cases.append(('false retired-circle disposition',d,'entire chart belongs'))
    d = copy.deepcopy(original);d['charts'][0]['colour_word'] = [0,0,0,0,0]
    cases.append(('improper physical colouring',d,'proper colour on every actual unit edge'))
    rejected = []
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)/'modified.json'
        for label,data,reason in cases:
            path.write_text(json.dumps(data))
            try:verify.run(path)
            except ValueError as error:
                X.need(reason in str(error), 'control reached intended mathematical check: '+label)
                rejected.append(label)
            else:raise ValueError('accepted corrupt certificate: '+label)
    return {'verified':True, 'rejected':rejected, 'assertions_used_for_correctness':False}


if __name__ == '__main__':print(json.dumps(run(),indent=2,sort_keys=True))
