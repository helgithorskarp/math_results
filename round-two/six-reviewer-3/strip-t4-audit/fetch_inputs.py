"""Fetch four immutable public JSON inputs and verify the frozen byte hashes."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

HERE=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    args=parser.parse_args()
    manifest=json.loads((HERE/'INPUTS.json').read_text())
    args.directory.mkdir(parents=True,exist_ok=True)
    total=0
    for row in manifest['runtime_files']:
        url=('https://raw.githubusercontent.com/helgithorskarp/math_results/'
             +manifest['commit']+'/'+row['path'])
        with urllib.request.urlopen(url,timeout=20) as response:
            raw=response.read(row['bytes']+1)
        if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:
            raise ValueError('immutable input mismatch: '+row['name'])
        destination=args.directory/row['name']
        if destination.exists() and destination.read_bytes()!=raw:
            raise ValueError('refusing to replace different local input: '+str(destination))
        destination.write_bytes(raw);total+=len(raw)
    print(json.dumps({'status':'FETCHED_AND_HASHED','files':len(manifest['runtime_files']),
                      'bytes':total,'commit':manifest['commit']},sort_keys=True))


if __name__=='__main__':
    main()
