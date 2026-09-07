#!/usr/bin/env python3
"""Fetch the pinned native graph source to a path outside the repository."""
import argparse,hashlib,json
from pathlib import Path
from urllib.request import urlopen
HERE=Path(__file__).resolve().parent
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);a=ap.parse_args();out=a.output.resolve()
    if out.is_relative_to(HERE.parent):raise ValueError('put the downloaded input outside the repository')
    spec=json.loads((HERE/'input.json').read_text())
    data=out.read_bytes()if out.exists()else urlopen(spec['url'],timeout=60).read()
    if len(data)!=spec['bytes']or hashlib.sha256(data).hexdigest()!=spec['sha256']:raise ValueError('input identity mismatch')
    out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
    print(json.dumps({'verified':True,'bytes':len(data),'sha256':spec['sha256'],'path':str(out)}))
