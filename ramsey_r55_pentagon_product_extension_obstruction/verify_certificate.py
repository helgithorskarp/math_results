"""Independent ten-physical-pair verifier; imports no producer or core code."""
from pathlib import Path
import argparse
import hashlib
import json


def verify(graph, certificate):
    if type(graph.get('n')) is not int or graph['n']!=43:
        raise ValueError('graph order')
    text=graph.get('red_hex')
    if not isinstance(text,str) or len(text)!=226 or any(c not in '0123456789abcdef' for c in text):
        raise ValueError('graph word')
    value=int(text,16)
    if value >= 2**903:
        raise ValueError('graph high bit')
    if certificate.get('format')!='physical-monochromatic-five-v1' or type(certificate.get('n')) is not int or certificate['n']!=43:
        raise ValueError('certificate format/order')
    if certificate.get('red_hex_sha256')!=hashlib.sha256(text.encode('ascii')).hexdigest():
        raise ValueError('graph binding')
    color=certificate.get('color')
    if color not in ('red','blue'):
        raise ValueError('color')
    vertices=certificate.get('vertices')
    if not isinstance(vertices,list) or len(vertices)!=5 or any(type(v) is not int or not 0<=v<43 for v in vertices) or vertices!=sorted(set(vertices)):
        raise ValueError('five vertices')
    checked=0
    for i,u in enumerate(vertices):
        for v in vertices[i+1:]:
            bit=u*(85-u)//2+v-u-1
            if bool(value & (1 << bit)) != (color=='red'):
                raise ValueError('not monochromatic')
            checked+=1
    if checked!=10:
        raise ValueError('pair count')
    return dict(status='VERIFIED_PHYSICAL_MONOCHROMATIC_K5',color=color,vertices=vertices,pairs_checked=checked)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    request=json.loads(a.input.read_text());out=json.loads(a.output.read_text())
    print(json.dumps(verify(request['graph'],out['certificate']),indent=2,sort_keys=True))
