#!/usr/bin/env python3
"""Download only pinned public target files and check their complete bytes."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    manifest=json.loads(Path(__file__).with_name('AUTHOR_SOURCE.json').read_text())
    a.out.mkdir(parents=True,exist_ok=True)
    def fetch(item):
        url='https://raw.githubusercontent.com/helgithorskarp/math_results/'+manifest['source_commit']+'/'+item['path']
        with urlopen(Request(url,headers={'User-Agent':'six-reviewer-4-independent-audit'}),timeout=25) as response:
            data=response.read()
        if len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:
            raise ValueError('pinned whole source mismatch '+item['path'])
        (a.out/Path(item['path']).name).write_bytes(data)
        return Path(item['path']).name
    with ThreadPoolExecutor(max_workers=4) as pool:names=list(pool.map(fetch,manifest['files']))
    print(json.dumps({'exact_pinned_files':names,'source_commit':manifest['source_commit']}))

if __name__=='__main__':main()
