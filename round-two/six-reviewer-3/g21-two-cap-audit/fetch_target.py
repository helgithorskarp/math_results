#!/usr/bin/env python3
"""Read-only pinned public source fetch; no credentials or graph interaction."""
import argparse,hashlib,json,pathlib,urllib.request
P=pathlib.Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--dest',required=True);a=ap.parse_args();dest=pathlib.Path(a.dest);pins=json.loads((P/'NATIVE-PINS.json').read_text());dest.mkdir(parents=True,exist_ok=True)
for name,v in pins['files'].items():
 if pathlib.PurePosixPath(name).name!=name:raise ValueError('flat source filename boundary')
 url='https://raw.githubusercontent.com/helgithorskarp/math_results/'+pins['source_commit']+'/round-two/six-tammes-2/g21-two-cap-capacity/'+name
 with urllib.request.urlopen(url,timeout=25) as r:b=r.read();status=r.status
 if status!=200 or len(b)!=v['bytes'] or hashlib.sha256(b).hexdigest()!=v['sha256']:raise ValueError('whole public source differs: '+name)
 path=dest/name
 if path.exists() and path.read_bytes()!=b:raise ValueError('different existing destination; preserve it')
 path.write_bytes(b)
print(json.dumps({'source_commit':pins['source_commit'],'files':len(pins['files']),'bytes':sum(v['bytes'] for v in pins['files'].values()),'all_whole_hashes_verified':True}))
