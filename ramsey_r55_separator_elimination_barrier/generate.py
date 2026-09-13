"""Inject all pairs of free physical edges into distinct containing five-sets."""
import argparse,json,time,hashlib,struct,resource
from pathlib import Path
from itertools import combinations
from collections import deque

def edges(n,cycle):
 fixed={tuple(sorted((v,(v+1)%n))) for v in range(n)} if cycle else set()
 return [(u,v) for u in range(n) for v in range(u+1,n) if (u,v) not in fixed]

def build(n,cycle,out):
 started=time.monotonic();E=edges(n,cycle);em=[(1<<u)|(1<<v) for u,v in E];pairs=list(combinations(range(len(E)),2));unions=[em[i]|em[j] for i,j in pairs];chosen=[0]*len(pairs);owner={};checks=0;augmentations=0;maximum_visited=0
 def choices(i):
  U=unions[i];outside=[v for v in range(n) if not U>>v&1];a=U.bit_count()
  for S in combinations(outside,5-a):
   m=U
   for v in S:m|=1<<v
   yield m
 # Each step augments a matching. No partial result can be certified as complete.
 for root in range(len(pairs)):
  found=None
  for m in choices(root):
   checks+=1
   if m not in owner:found=m;break
  if found is not None:owner[found]=root;chosen[root]=found
  else:
   augmentations+=1;queue=deque([root]);parents={root:None};last=None;terminal=None
   while queue and terminal is None:
    i=queue.popleft()
    for m in choices(i):
     checks+=1;j=owner.get(m)
     if j is None:last=i;terminal=m;break
     if j not in parents:parents[j]=(i,m);queue.append(j)
   if terminal is None:raise RuntimeError(('No augmenting path',root,len(parents)))
   maximum_visited=max(maximum_visited,len(parents))
   i=last;m=terminal
   while True:
    owner[m]=i;chosen[i]=m
    if i==root:break
    i,m=parents[i]
  if root%50000==0:print('matched',root+1,'/',len(pairs),'seconds',time.monotonic()-started,flush=True)
 assert len(owner)==len(pairs) and len(set(chosen))==len(pairs)
 data=b''.join(struct.pack('<Q',m) for m in chosen);out.write_bytes(data)
 info={'n':n,'fixed_cycle':cycle,'variables':len(E),'variable_pairs':len(pairs),'assigned_distinct_five_sets':len(owner),'certificate_format':'One little-endian uint64 five-set bitmask per lexicographic unordered pair of lexicographic free physical edges.','certificate_sha256':hashlib.sha256(data).hexdigest(),'certificate_bytes':len(data),'seconds':time.monotonic()-started,'candidate_checks':checks,'augmenting_searches':augmentations,'largest_visited_left_set':maximum_visited,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'status':'COMPLETE_INCIDENCE_MATCHING_NO_RAMSEY_VERDICT'};out.with_suffix('.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info),flush=True)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=43);ap.add_argument('--cycle',action='store_true');ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();build(a.n,a.cycle,a.output)
