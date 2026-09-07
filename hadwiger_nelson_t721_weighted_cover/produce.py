#!/usr/bin/env python3
"""Regenerate the compact colouring DAG from twelve explicit seed words."""
import argparse,json
from pathlib import Path
import native,transport
HERE=Path(__file__).resolve().parent

def reproduce(path):
    source=json.loads((HERE/'seeds.json').read_text());g=native.build(path);cert=None;pos=0
    for size in source['seed_batches']:
        batch={'baseline':source['baseline'],'steps':source['steps'][pos:pos+size]};pos+=size
        cert=transport.generate(batch,g,g['rotations'],existing=cert)
    if pos!=len(source['steps']):raise ValueError('seed batches')
    return (json.dumps(cert,separators=(',',':'))+'\n').encode()
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True,type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args()
    data=reproduce(a.input)
    if data!=(HERE/'certificate.json').read_bytes():raise ValueError('certificate reproduction mismatch')
    if a.output:
        out=a.output.resolve()
        if out.is_relative_to(HERE.parent):raise ValueError('put regenerated output outside the repository')
        out.write_bytes(data)
    print(json.dumps({'verified':True,'certificate_bytes':len(data),'byte_identical':True}))
