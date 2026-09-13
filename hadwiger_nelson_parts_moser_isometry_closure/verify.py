"""Solver-free family verifier, using exhaustive word-bitsets for list colouring.

The discovery implementation used recursive list search. Here all proper words
are generated directly from the graph definition, then filtered by each list.
"""
import argparse,base64,gzip,hashlib,json,math,time
from collections import Counter
from functools import lru_cache
from itertools import combinations,product
from pathlib import Path
import geometry as G
HERE=Path(__file__).resolve().parent

def require(ok,msg):
 if not ok:raise ValueError(msg)
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def unpack(raw,n):return [(raw[i//4]>>(2*(i%4)))&3 for i in range(n)]
def libraries(edges):
 deps=json.loads((HERE/'DEPENDENCIES.json').read_text())
 for p,h in deps['files'].items():require(hashlib.sha256((HERE.parent/p).read_bytes()).hexdigest()==h,'input hash '+p)
 base=json.loads((HERE.parent/'hadwiger_nelson_parts509_criticality/certificate.json').read_text())
 raw=base64.b64decode(base['deletion_colorings_base64'],validate=True)
 require(len(raw)==509*127,'base row count');libs=[]
 for u in range(509):
  c=unpack(raw[127*u:127*(u+1)],508);c.insert(u,4);libs.append([c])
 q=json.loads(gzip.decompress((HERE.parent/'hadwiger_nelson_parts509_quad_closure/certificate.json.gz').read_bytes()))
 raw=base64.b64decode(q['family_rows_base64'],validate=True);off=0
 require(len(q['family_sizes'])==509,'family count')
 for u,n in enumerate(q['family_sizes']):
  require(type(n)is int and n>=0,'row multiplicity')
  for _ in range(n):
   require(off+127<=len(raw),'truncated rows');c=unpack(raw[off:off+127],508);off+=127;c.insert(u,4);libs[u].append(c)
 require(off==len(raw),'row framing')
 for u,rows in enumerate(libs):
  for c in rows:
   require(len(c)==509 and c[u]==4,'colour row shape')
   require(all(c[a]!=c[b]for a,b in edges if u not in (a,b)),'improper base colouring')
 return libs

@lru_cache(None)
def tables(n,edges):
 require(1<=n<=5,'new point budget')
 require(all(0<=a<b<n for a,b in edges),'edge labels')
 words=[w for w in product(range(4),repeat=n)if all(w[a]!=w[b]for a,b in edges)]
 table=[]
 for i in range(n):
  singles=[sum(1<<j for j,w in enumerate(words)if w[i]==c)for c in range(4)]
  table.append(tuple(sum(singles[c]for c in range(4)if m>>c&1)for m in range(16)))
 return tuple(table)
def possible(table,masks):
 z=table[0][masks[0]]
 for i in range(1,len(masks)):
  z &= table[i][masks[i]]
  if not z:return False
 return bool(z)
def masks_for(c,qs,neighbours):
 masks=[]
 for q in qs:
  m=15
  for v in neighbours[q]:m &= ~(1<<c[v])
  masks.append(m)
 return masks

def cover(g,libs,progress=False):
 A=g['assemblies'];N=g['neighbours'];U=[[]for _ in A]
 tab=[tables(len(a['fresh']),tuple(map(tuple,a['edges'])))for a in A]
 used=set()
 for u,rows in enumerate(libs):
  pending=list(range(len(A)))
  for ri,c in enumerate(rows):
   cache={};nextp=[]
   for k in pending:
    masks=[]
    for q in A[k]['fresh']:
     if q not in cache:cache[q]=masks_for(c,[q],N)[0]
     masks.append(cache[q])
    if possible(tab[k],masks):used.add((u,ri))
    else:nextp.append(k)
   pending=nextp
   if not pending:break
  for k in pending:U[k].append(u)
  if progress and u%50==0:print('colour deletion family',u,flush=True)
 return U,used

def partial_frontier(g,libs,U):
 # For B subset A, U(B) subset U(A). Intersect bounds across all parent A.
 sub={};routes=0
 for k,unknown in enumerate(U):
  a=g['assemblies'][k];n=len(a['fresh'])
  for b in range(1,min(n,len(unknown)-1)+1):
   for ids in combinations(range(n),b):
    key=tuple(a['fresh'][i]for i in ids);routes+=1
    if key not in sub:
     ix={i:j for j,i in enumerate(ids)};edges=tuple((ix[i],ix[j])for i,j in a['edges']if i in ix and j in ix)
     sub[key]={'edges':edges,'unknown':set(unknown)}
    else:sub[key]['unknown'].intersection_update(unknown)
 frontier=[];tested=0
 for key,r in sorted(sub.items()):
  if len(r['unknown'])<=len(key):continue
  tested+=1;table=tables(len(key),r['edges']);bad=[]
  for u in sorted(r['unknown']):
   if not any(possible(table,masks_for(c,key,g['neighbours']))for c in libs[u]):bad.append(u)
  if len(bad)>len(key):frontier.append({'fresh':list(key),'edges':[list(e)for e in r['edges']],'unknown':bad})
 return frontier,{'subset_routes':routes,'distinct_subsets':len(sub),'requiring_new_tests':tested,'residual_subsets':len(frontier),'target_instances':sum(math.comb(len(r['unknown']),len(r['fresh'])+1)for r in frontier),'subset_size_histogram':dict(Counter(len(r['fresh'])for r in frontier))}

def target_keys(frontier):
 for r in frontier:
  for D in combinations(r['unknown'],len(r['fresh'])+1):yield tuple(r['fresh']),D

def check_targets(g,frontier,certificate):
 cert=json.loads(certificate.read_text());require(cert['format']=='parts-moser-isometry-colours-v1','certificate format');rows={}
 for r in cert['rows']:
  key=(tuple(r['fresh']),tuple(r['deleted']));require(key not in rows,'duplicate target');rows[key]=r
 required=set(target_keys(frontier));require(set(rows)==required,'complete target coverage')
 edge_checks=0
 for key,r in rows.items():
  qs,D=key;require(list(qs)==sorted(set(qs)) and list(D)==sorted(set(D)),'canonical labels')
  require(all(type(i)is int and 0<=i<len(g['points'])for i in qs),'point labels')
  require(all(type(i)is int and 0<=i<509 for i in D),'deleted labels')
  retained=[v for v in range(509)if v not in D];n=len(retained)+len(qs);require(n==508,'target order')
  raw=base64.b64decode(r['colours'],validate=True);require(len(raw)==127,'target row size');c=unpack(raw,n)
  labels=retained+[509+i for i in range(len(qs))];ci=dict(zip(labels,c))
  E=[(a,b)for a,b in g['base_edges']if a not in D and b not in D]
  E += [(v,509+i)for i,q in enumerate(qs)for v in g['neighbours'][q]if v not in D]
  unit=G.scale(G.O,g['scale']**2)
  E += [(509+i,509+j)for i,j in combinations(range(len(qs)),2)if G.norm(G.sub(g['points'][qs[i]],g['points'][qs[j]]))==unit]
  require(all(ci[a]!=ci[b]for a,b in E),'improper target colouring');edge_checks+=len(E)
 return {'target_rows':len(rows),'target_edge_checks':edge_checks,'certificate_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest()}

def run(args):
 st=time.monotonic();g=G.build(args.progress);libs=libraries(g['base_edges']);U,used=cover(g,libs,args.progress);front,sub=partial_frontier(g,libs,U)
 result={'geometry':g['summary'],'base_colour_rows_checked':sum(map(len,libs)),'used_base_rows':len(used),'uncovered_histogram':dict(Counter(map(len,U))),'maximum_uncovered':max(map(len,U)),'coverage_sha256':digest(U),'partial':sub,'frontier_sha256':digest(front)}
 if args.emit_frontier:
  args.emit_frontier.write_text(json.dumps({'geometry':g,'frontier':front},separators=(',',':'))+'\n');result['all_sub509_subgraphs_four_colourable']=False
 else:
  result.update(check_targets(g,front,args.certificate));result['all_sub509_subgraphs_four_colourable']=True
 if args.check_expected:
  expected=json.loads((HERE/'EXPECTED.json').read_text());require(json.loads(json.dumps(result))==expected,'expected-result mismatch')
 if args.output:args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps(result,indent=2,sort_keys=True));print('wall_seconds',round(time.monotonic()-st,3))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'certificate.json');p.add_argument('--output',type=Path);p.add_argument('--emit-frontier',type=Path);p.add_argument('--check-expected',action='store_true');p.add_argument('--progress',action='store_true');run(p.parse_args())
