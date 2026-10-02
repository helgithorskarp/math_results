#!/usr/bin/env python3
"""Restore only hash-bound own reviewed premises; never overwrite wrong inputs."""
import hashlib,json,sys,urllib.request
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def restore(root,row):
 path=Path(row['path'])
 if path.is_absolute() or '..' in path.parts:raise ValueError('unsafe input path')
 target=root/path
 def valid(b):return len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
 if target.exists():
  if not valid(target.read_bytes()):raise ValueError('existing input differs '+str(path))
  return
 url='https://raw.githubusercontent.com/helgithorskarp/math_results/'+row['commit']+'/'+row['path']
 with urllib.request.urlopen(url,timeout=20) as r:b=r.read()
 if not valid(b):raise ValueError('download binding differs '+str(path))
 target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
def main():
 rows=json.loads((HERE/'OWN_INPUTS.json').read_text())['files']
 if len(rows)!=30 or any(not r['path'].startswith('round-two/six-reviewer-3/') for r in rows):raise ValueError('own30 premises only')
 for row in rows:restore(ROOT,row)
 print('PASS thirty hash-bound own inputs')
if __name__=='__main__':main()
