#!/usr/bin/env python3
"""Reject faults in the compact positive-word certificate."""
import base64
import copy
from hashlib import sha256
import json
import verify

def reject(call):
    try:
        call()
    except ValueError:
        return
    raise ValueError('corrupt input accepted')

def main():
    g = verify.build()
    cert = json.loads((verify.HERE/'certificate.json').read_text())
    altered = copy.deepcopy(cert)
    altered['new_deleted_vertices'][0] = altered['new_deleted_vertices'][1]
    reject(lambda:verify.compute(altered,g))
    altered = copy.deepcopy(cert)
    raw = bytearray(base64.b64decode(altered['packed_colours_base64']))
    raw[127] |= 4
    altered['packed_colours_base64'] = base64.b64encode(raw).decode()
    altered['packed_sha256'] = sha256(raw).hexdigest()
    reject(lambda:verify.compute(altered,g))
    altered = copy.deepcopy(cert)
    raw = bytearray(base64.b64decode(altered['packed_colours_base64']))
    raw[:128] = bytes(128)
    altered['packed_colours_base64'] = base64.b64encode(raw).decode()
    altered['packed_sha256'] = sha256(raw).hexdigest()
    reject(lambda:verify.compute(altered,g))
    altered = copy.deepcopy(cert)
    altered['rows'] = 2
    reject(lambda:verify.compute(altered,g))
    reject(lambda:verify.check_word(g['edges'], [None]*510, palette=range(5)))
    print(json.dumps({'all_checks':True,'rejected_certificate_faults':4,
                      'rejected_placeholder_five_word':True}))

if __name__ == '__main__':
    main()
