"""Literal primary69 calibration; no71-saturated identities are applied."""
import argparse,hashlib,json
from collections import Counter
from itertools import combinations
from pathlib import Path

def need(x,m):
 if not x:raise ValueError(m)
def check(path):
 raw=path.read_bytes();strings=raw.decode().splitlines()
 need(len(strings)==69 and len(set(strings))==69,'69 distinct primary rows')
 need(all(len(s)==18 and set(s)<=set('01')and s.count('1')==5 for s in strings),'literal weight/length')
 words=[frozenset(i for i,b in enumerate(s)if b=='1')for s in strings]
 distances=Counter();owned=set()
 for w in words:
  for t in combinations(sorted(w),3):need(t not in owned,'repeated triple');owned.add(t)
 for v,w in combinations(words,2):
  d=10-2*len(v&w);need(d>=6,'distance scope');distances[d]+=1
 return {'words':69,'pairs':sum(distances.values()),'unique_owned_triples':len(owned),'distance_histogram':dict(sorted(distances.items())),
  'primary_raw_sha256':hashlib.sha256(raw).hexdigest(),'scope':'prior lower69 only, not a71-code or new construction'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);a=p.parse_args();print(json.dumps(check(a.input),sort_keys=True))
