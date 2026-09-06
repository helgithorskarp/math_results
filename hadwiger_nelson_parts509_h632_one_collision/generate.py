"""Produce a Hall-witness certificate excluding maps with at most one collision.

All generated state belongs in the supplied output directory outside the repo.
"""
from collections import Counter,deque
from hashlib import sha256
from pathlib import Path
import argparse,json,time,resource
import geometry as G

def graph(n,edges):
 a=[set() for _ in range(n)]
 for u,v in edges:a[u].add(v);a[v].add(u)
 return a

def hall_witness(lists):
 """Return a Hall subset with deficiency >=2, or None.

 Full augmenting-path matching is discovery only; the verifier checks the
 resulting neighbour-union inequality and does not run this algorithm.
 """
 order=sorted(lists,key=lambda u:(len(lists[u]),u));owner={}
 def visit(u,seen):
  for h in sorted(lists[u]):
   if h in seen:continue
   seen.add(h)
   if h not in owner or visit(owner[h],seen):owner[h]=u;return True
  return False
 for u in order:visit(u,set())
 if len(owner)>=len(lists)-1:return None
 used=set(owner.values());A=set(lists)-used;queue=deque(sorted(A));B=set()
 while queue:
  u=queue.popleft()
  for h in sorted(lists[u]):
   if h in B:continue
   B.add(h)
   if h in owner and owner[h] not in A:A.add(owner[h]);queue.append(owner[h])
 G.need(B==set().union(*(lists[u] for u in A)) and len(B)<=len(A)-2,'produced Hall witness')
 return sorted(A)

def domhash(D):return sha256(json.dumps([sorted(d) for d in D],separators=(',',':')).encode()).hexdigest()

def produce(sa,ha):
 n=len(sa);m=len(ha)
 initial=[{h for h in range(m) if len(ha[h])>=len(sa[v])-1} for v in range(n)]
 D=[set(d) for d in initial];records=[];reasons={};rounds=[];start=time.monotonic()
 while True:
  pending=[]
  for v in range(n):
   for h in sorted(D[v]):
    rows={u:D[u]&ha[h] for u in sorted(sa[v])}
    empty=next((u for u,z in rows.items() if not z),None)
    if empty is not None:kind='A';A=[empty]
    else:
     A=hall_witness(rows)
     if A is None:continue
     kind='H'
    # All excluded neighbour values that justify the witnessed union.
    dependencies=set()
    for u in A:
     for b in sorted((initial[u]&ha[h])-D[u]):dependencies.add(reasons[u,b])
    pending.append((v,h,kind,A,sorted(dependencies)))
  if not pending:break
  for v,h,kind,A,dep in pending:
   reasons[v,h]=len(records);records.append([v,h,kind,A,dep]);D[v].remove(h)
  round_info={'round':len(rounds),'removed':len(pending),'remaining':sum(map(len,D)),'empty':[v for v,d in enumerate(D) if not d],'domains_sha256':domhash(D)};rounds.append(round_info)
  print(json.dumps(round_info),flush=True)
  if any(not d for d in D):break
 empty=[v for v,d in enumerate(D) if not d]
 G.need(empty,'domain reduction did not decide this family')
 # Backward slice for each available empty-domain contradiction.
 slices=[]
 for v in empty:
  todo=[reasons[v,h] for h in initial[v]];use=set()
  while todo:
   i=todo.pop()
   if i in use:continue
   use.add(i);todo.extend(records[i][4])
  slices.append((len(use),v,sorted(use)))
 size,root,use=min(slices)
 certificate={'format':'one-collision-hall-v1','source_vertices':n,'host_vertices':m,'maximum_identifications':1,'empty_source_vertex':root,'removals':[[records[i][0],records[i][1],records[i][2],records[i][3]] for i in use]}
 summary={'source_vertices':n,'host_vertices':m,'initial_domain_values':sum(map(len,initial)),'full_removals':len(records),'rounds':rounds,'empty_source_vertices':empty,'slice_empty_source_vertex':root,'slice_removals':size,'slice_kinds':dict(sorted(Counter(r[2] for r in certificate['removals']).items())),'seconds':time.monotonic()-start,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 return certificate,summary

def main(out):
 out.mkdir(parents=True,exist_ok=False);se,he=G.inputs();sa=graph(509,se);ha=graph(632,he)
 certificate,summary=produce(sa,ha)
 raw=(json.dumps(certificate,separators=(',',':'))+'\n').encode();(out/'certificate.json').write_bytes(raw)
 summary['certificate_bytes']=len(raw);summary['certificate_sha256']=sha256(raw).hexdigest();(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();main(a.out)
