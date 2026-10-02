"""Fresh primary69-word witness; validation only, not a new construction."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import urllib.request,hashlib,json,sys
URL='https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69'
PIN='cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d'
def need(ok,message):
 if not ok:raise RuntimeError(message)
if __name__=='__main__':
 if len(sys.argv)>1:raw=Path(sys.argv[1]).read_bytes()
 else:
  with urllib.request.urlopen(URL,timeout=25)as r:raw=r.read()
 need(hashlib.sha256(raw).hexdigest()==PIN,'exact primary raw bytes');rows=raw.decode().splitlines();need(len(rows)==len(set(rows))==69 and all(len(s)==18 and set(s)<=set('01')and s.count('1')==5 for s in rows),'primary words')
 words=[{i for i,c in enumerate(s)if c=='1'}for s in rows];distance=Counter();pairs=0
 for a,b in combinations(words,2):
  need(len(a&b)<=2,'primary packing distance');distance[len(a^b)]+=1;pairs+=1
 triples=[t for w in words for t in combinations(sorted(w),3)];need(len(triples)==len(set(triples))==690,'primary owned triples')
 rep=Counter(sum(i in w for w in words)for i in range(18));need(pairs==2346,'all primary pairs')
 print(json.dumps({'words':69,'pairs':pairs,'triples':len(triples),'distance_counts':dict(sorted(distance.items())),'point_replication_histogram':dict(sorted(rep.items())),'raw_sha256':PIN},sort_keys=True,separators=(',',':')))
