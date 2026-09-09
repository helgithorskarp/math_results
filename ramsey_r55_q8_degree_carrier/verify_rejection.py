#!/usr/bin/env python3
"""Check a rejected graph using only the witness's ten physical pairs."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path


def verify(graph, certificate):
    text=graph['red_hex']
    if graph['n']!=43 or type(text) is not str or len(text)!=226 or any(c not in '0123456789abcdef' for c in text):
        raise ValueError('graph encoding')
    word=int(text,16)
    if word>=2**903 or certificate['graph_sha256']!=hashlib.sha256(text.encode('ascii')).hexdigest():
        raise ValueError('graph binding')
    vertices=certificate['vertices'];color=certificate['color']
    if (certificate['status']!='REJECT_WITH_MONOCHROMATIC_FIVE' or len(vertices)!=5 or
        len(set(vertices))!=5 or any(type(v) is not int or not 0<=v<43 for v in vertices) or
        type(color) is not int or color not in (0,1)):
        raise ValueError('witness format')
    for u,v in it.combinations(sorted(vertices),2):
        # Number of pairs in all rows preceding u, then the column offset.
        index=u*(85-u)//2+v-u-1
        if ((word>>index)&1)!=color:
            raise ValueError('witness pair has wrong color')
    return {'status':'VERIFIED_LITERAL_MONOCHROMATIC_FIVE','physical_pairs_checked':10}


def main():
    p=argparse.ArgumentParser();p.add_argument('graph',type=Path);p.add_argument('certificate',type=Path)
    a=p.parse_args();print(json.dumps(verify(json.loads(a.graph.read_text()),json.loads(a.certificate.read_text())),sort_keys=True))


if __name__=='__main__':
    main()
