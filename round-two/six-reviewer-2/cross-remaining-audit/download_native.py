#!/usr/bin/env python3
"""Optional late inputs from the exact public source commit, with whole pins."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    pins=json.loads((Path(__file__).resolve().parent/'NATIVE_INPUTS.json').read_text())
    for rec in pins['files']:
        url='https://raw.githubusercontent.com/helgithorskarp/math_results/'+pins['commit']+'/'+rec['path']
        with urllib.request.urlopen(url,timeout=20) as response:data=response.read()
        if len(data)!=rec['bytes'] or hashlib.sha256(data).hexdigest()!=rec['sha256']:
            raise ValueError('whole native source mismatch: '+rec['path'])
        dest=args.output/Path(rec['path']).name
        if dest.exists() and dest.read_bytes()!=data:raise ValueError('refuse conflicting local input')
        dest.write_bytes(data)
    print(json.dumps({'whole_pinned_files':len(pins['files']),'commit':pins['commit']}))

if __name__=='__main__':main()
