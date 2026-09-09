#!/usr/bin/env python3
"""Exact source-extension and finite-kernel checks for the written theorem."""
from pathlib import Path
from itertools import combinations,permutations,product
from copy import deepcopy
import argparse,hashlib,json
import kernel
import audit_kernel
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
RAD=[1,3,5,15,11,33,55,165]

def need(x,msg):
 if not x:raise ValueError(msg)
def mul(a,b):
 r=[0]*8
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:r[i^j]+=x*y*RAD[i&j]
 return r
def norm(a,b):
 dx=[x-y for x,y in zip(a[:8],b[:8])];dy=[x-y for x,y in zip(a[8:],b[8:])]
 return [x+y for x,y in zip(mul(dx,dx),mul(dy,dy))]
def proper(word,n,edges):
 need(type(word) is str and len(word)==n and set(word)<={'0','1','2','3'},'colour word')
 need(all(word[a]!=word[b] for a,b in edges),'monochromatic source edge')
def extension_check(rec,n,edges,ports):
 patterns=['001','010','011','012'] if n==159 else ['01']
 need(rec['terminals']==ports and [w['pattern'] for w in rec['extensions']]==patterns,'complete canonical patterns')
 seen=set();edge_checks=0
 for row in rec['extensions']:
  word=row['colours'];proper(word,n,edges)
  need(''.join(word[i] for i in ports)==row['pattern'],'terminal pattern')
  for palette in permutations('0123'):
   image=''.join(palette[int(c)] for c in word);proper(image,n,edges)
   seen.add(''.join(image[i] for i in ports));edge_checks+=len(edges)
 target={''.join(w) for w in product('0123',repeat=len(ports)) if len(set(w))>1}
 need(seen==target,'all nonmono boundary assignments covered')
 return len(seen),edge_checks

def sources():
 deps=json.loads((HERE/'DEPENDENCIES.json').read_text())
 for name,h in deps['input_sha256'].items():need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,'source hash: '+name)
 cert=json.loads((HERE/'extensions.json').read_text());out=[];graph_data={}
 for n,ports,d in [(159,[141,142,144],7),(214,[186,187],9)]:
  text=(ROOT/f'hadwiger_nelson_nonmono159_214_lowden2/points{n}.tsv').read_text().splitlines()
  need(text[0]=='# scale 12','source scale')
  points=[tuple(map(int,l.split())) for l in text if l.strip() and not l.startswith('#')]
  need(len(points)==len(set(points))==n and all(len(x)==16 for x in points),'exact source points')
  edges=[(i,j) for i,j in combinations(range(n),2) if norm(points[i],points[j])==[144]+[0]*7]
  need(len(edges)==(646 if n==159 else 977),'strict source edges')
  need(all(norm(points[i],points[j])==[144*d]+[0]*7 for i,j in combinations(ports,2)) and d>4,'strict terminal separation')
  assignments,checks=extension_check(cert[str(n)],n,edges,ports)
  out.append({'vertices':n,'strict_unit_edges':len(edges),'all_pairs_checked':n*(n-1)//2,'nonmono_assignments':assignments,'renamed_witness_edge_checks':checks,'private_vertices':n-len(ports),'squared_terminal_distance':d})
  graph_data[n]=(edges,ports)
 corruptions=[]
 x=deepcopy(cert['159']);x['extensions'].pop();corruptions.append(('missing boundary pattern',x))
 x=deepcopy(cert['159']);a,b=graph_data[159][0][0];w=list(x['extensions'][0]['colours']);w[a]=w[b];x['extensions'][0]['colours']=''.join(w);corruptions.append(('false colouring',x))
 x=deepcopy(cert['159']);x['terminals'][0]=0;corruptions.append(('wrong terminal index',x))
 for name,x in corruptions:
  try:extension_check(x,159,*graph_data[159])
  except ValueError:pass
  else:raise RuntimeError('accepted corruption: '+name)
 return out,[name for name,_ in corruptions]

def colour_auxiliary(n,unit,chosen):
 adj=[set() for _ in range(n)]
 for a,b in unit|chosen:adj[a].add(b);adj[b].add(a)
 need(max(map(len,adj),default=0)<=4,'auxiliary degree')
 active=set(range(n));removed=[]
 while True:
  v=next((v for v in sorted(active) if len(adj[v]&active)<=3),None)
  if v is None:break
  active.remove(v);removed.append(v)
 need(len(active)<=2*len(chosen)<=8,'small residual kernel')
 colours={}
 def solve():
  if len(colours)==len(active):return True
  v=min(active-set(colours))
  for c in range(4):
   if all(colours.get(u)!=c for u in adj[v]):
    colours[v]=c
    if solve():return True
    del colours[v]
  return False
 need(solve(),'fixture kernel is four-colourable')
 for v in reversed(removed):colours[v]=next(c for c in range(4) if all(colours.get(u)!=c for u in adj[v]))
 need(all(colours[a]!=colours[b] for a,b in unit|chosen),'fixture colouring')
 return max(map(len,adj),default=0),len(active)

def geometric_controls():
 # (x,y) denotes the point (x/2, y*sqrt(3)/2).
 def dist4(a,b):return (a[0]-b[0])**2+3*(a[1]-b[1])**2
 diamond=[(0,0),(2,0),(1,1),(3,1)]
 fixtures=[('four_distant_pairs',[[p,(p[0]+20,p[1])] for p in diamond]),('four_identical_triples',[[(0,0),(6,0),(0,6)]]*4),('four_pairs_shared_centre',[[(0,0),p] for p in [(6,0),(-6,0),(0,6),(0,-6)]])]
 report=[]
 for name,blocks in fixtures:
  points=sorted(set(p for b in blocks for p in b));ix={p:i for i,p in enumerate(points)}
  need(all(dist4(a,b)>16 for block in blocks for a,b in combinations(block,2)),'fixture strict separation')
  sets=[set(ix[p] for p in b) for b in blocks]
  unit={(i,j) for i,j in combinations(range(len(points)),2) if dist4(points[i],points[j])==4}
  choices=[tuple(combinations(sorted(s),2)) for s in sets];degrees=[]
  for pairs in product(*choices):
   chosen=set(pairs);need(not(unit&chosen),'long edge is nonunit')
   for v in range(len(points)):
    neigh={b if a==v else a for a,b in unit if v in (a,b)}
    need(all(len(neigh&s)<=int(v not in s) for s in sets),'geometric incidence bound')
   degree,core=colour_auxiliary(len(points),unit,chosen);degrees.append(degree)
  report.append({'fixture':name,'vertices':len(points),'unit_edges':len(unit),'pair_choices_checked':len(degrees),'maximum_auxiliary_degree':max(degrees)})
 # Two unit-circle intersection points have squared separation 3, not 1.
 points=[(0,0),(2,0),(1,1),(1,-1)]
 need(all(dist4(points[i],points[j])==4 for i in (0,1) for j in (2,3)) and dist4(points[2],points[3])==12,'no planar unit K4')
 # Sharpness of the six-long-edge K5 lemma; this is an auxiliary graph.
 points=[(0,0),(2,0),(1,1),(20,0),(22,0)]
 ds=[dist4(a,b) for a,b in combinations(points,2)]
 need(ds.count(4)==4 and sum(d>16 for d in ds)==6,'sharp six-long-edge fixture')
 # Strict >2 is essential to the one-neighbour-per-terminal-set bound.
 need(dist4((-2,0),(2,0))==16 and dist4((-2,0),(0,0))==dist4((2,0),(0,0))==4,'distance-two boundary')
 return report

def run():
 primary=kernel.run();audit=audit_kernel.run()
 for p,a in zip(primary['finite_kernels'],audit['finite_kernels']):
  need(p['vertices']==a['vertices'] and p['labelled_four_regular_graphs']==a['degree_polynomial_count'] and p['positive_four_colourings']==a['positive_covered_graphs'] and p['graph_set_sha256']==a['graph_set_sha256'],'independent complete kernel audit')
 need(primary['K5_geometry']['surviving_masks_sha256']==audit['K5_geometry']['surviving_masks_sha256'],'independent K5 geometry masks')
 src,rejections=sources();fixtures=geometric_controls()
 budgets=[]
 for b in range(6):
  a=5-b;terminals=3 if b==0 else 2 if a==0 else 4
  budgets.append({'A159_copies':a,'B214_copies':b,'private_vertices':156*a+212*b,'terminal_union_lower_bound':terminals,'total_order_lower_bound':156*a+212*b+terminals})
 need(min(r['total_order_lower_bound'] for r in budgets)==783,'full-gadget architecture floor')
 need(5*102>508,'private-size necessary bound')
 return {'status':'AT_MOST_FOUR_SEPARATED_TERMINAL_MODULES_ARE_FOUR_COLOURABLE','record_improvement':False,'finite_proof':primary,'independent_audit':audit,'source_extensions':src,'geometric_controls':fixtures,'rejected_source_corruptions':rejections,'five_full_module_order_lower_bounds':budgets,'full_A159_B214_nonfour_order_lower_bound':783,'at_most508_nonfour_assembly_requires_some_private_size_at_most':101,'solver_calls':0,'brooks_theorem_required_for_finite_proof':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check-expected',action='store_true');a=p.parse_args();out=run()
 if a.check_expected:need(out==json.loads((HERE/'EXPECTED.json').read_text()),'expected result')
 print(json.dumps(out,indent=2,sort_keys=True))
