#!/usr/bin/env python3
"""Small decoder controls plus one end-to-end damaged-word rejection."""
from copy import deepcopy
import base64
import json

import verify


def pack(values):
    raw=bytearray((len(values)+3)//4)
    for i,c in enumerate(values):raw[i//4]|=c<<(2*(i%4))
    return base64.b64encode(bytes(raw)).decode('ascii')


def main():
    rejected=0
    try: verify.decode_packed('!',511)
    except (ValueError,base64.binascii.Error):rejected+=1
    data=json.loads((verify.HERE/'certificate.json').read_text())
    bad=deepcopy(data);bad['schema']=2
    try:verify.validate(bad)
    except ValueError:rejected+=1
    old,fresh=verify.source_points();bad=deepcopy(data['supports'][0])
    words=[list(verify.decode_packed(row,511)) for row in bad['packed_singleton_words']]
    graph=verify.exact_edges(old+(verify.point(fresh[319]['coordinates']),))
    a,b=next((a,b) for a,b in graph if 0 not in (a,b));words[0][a]=words[0][b]
    bad['packed_singleton_words'][0]=pack(words[0]);bad['word_stream_sha256']=verify.word_hash(words)
    try:verify.check_support(bad,old,fresh)
    except ValueError:rejected+=1
    if rejected!=3:raise ValueError('control accepted')
    print(json.dumps({'status':'PASS','malformed_controls_rejected':rejected},sort_keys=True))


if __name__=='__main__':main()
