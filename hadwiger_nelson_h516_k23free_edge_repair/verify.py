#!/usr/bin/env python3
"""Independent exact graph/CNF audit for the 301-vertex abstract repair."""
import argparse,copy,hashlib,itertools,json,pathlib
D=pathlib.Path(__file__).resolve().parent;UP=D.parent/'hadwiger_nelson_h516_degree4_surgeries'
def need(ok,why):
 if not ok:raise ValueError(why)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def quotient(source,surgeries):
 labels=source['labels'];edges={tuple(e) for e in source['edges']};adj={v:set() for v in labels}
 for u,v in edges:adj[u].add(v);adj[v].add(u)
 stars=[];mp={v:v for v in labels}
 for c,u,v in surgeries:
  need(len(adj[c])==4,'surgery centre degree');need(u in adj[c] and v in adj[c],'centre neighbours');need(v not in adj[u],'nonedge merged pair');need(u<v,'canonical representative')
  stars.append(adj[c]|{c});mp[c]=None;mp[v]=u
 need(all(not(a&b) for a,b in itertools.combinations(stars,2)),'disjoint closed stars')
 active=sorted(v for v in labels if mp[v]==v);out=set()
 for x,y in edges:
  u,v=mp[x],mp[y]
  if u is None or v is None:continue
  need(u!=v,'loop-free quotient');out.add(tuple(sorted((u,v))))
 return active,sorted(out)

def forbidden(labels,edges):
 adj={v:set() for v in labels}
 for u,v in edges:adj[u].add(v);adj[v].add(u)
 k23=[]
 for i,u in enumerate(labels):
  for v in labels[i+1:]:
   common=sorted(adj[u]&adj[v])
   if len(common)>=3:k23.append([u,v,common])
 k4=[]
 for a in labels:
  for b in sorted(v for v in adj[a] if v>a):
   common=sorted(v for v in adj[a]&adj[b] if v>b)
   for i,c in enumerate(common):
    for d in common[i+1:]:
     if d in adj[c]:k4.append([a,b,c,d])
 return k23,k4

def hitting_counts(k23,chosen):
 constraints=set()
 for u,v,common in k23:
  for triple in itertools.combinations(common,3):constraints.add(frozenset(tuple(sorted((a,b))) for a in (u,v) for b in triple))
 universe=sorted(set().union(*constraints));want=frozenset(chosen);need(all(c&want for c in constraints),'chosen deletions miss K2,3')
 counts={}
 for k in range(len(want)+1):
  counts[k]=sum(all(c.intersection(h) for c in constraints) for h in itertools.combinations(universe,k))
  if counts[k]:break
 return len(constraints),len(universe),counts

def cnf_bytes(labels,edges,triangle):
 pos={v:i for i,v in enumerate(labels)};lines=[f'p cnf {4*len(labels)} {len(labels)+4*len(edges)+3}\n']
 for v in labels:lines.append(' '.join(str(4*pos[v]+c+1) for c in range(4))+' 0\n')
 for u,v in edges:
  for c in range(4):lines.append(f'{-4*pos[u]-c-1} {-4*pos[v]-c-1} 0\n')
 for c,v in enumerate(triangle):lines.append(f'{4*pos[v]+c+1} 0\n')
 return ''.join(lines).encode()

def audit(parent,graph,five,deletions,expected):
 need(sha(UP/'SOURCE.json')==expected['upstream_source_sha256'],'upstream source identity');need(sha(UP/'certificate.json')==expected['upstream_certificate_sha256'],'upstream certificate identity')
 source=json.loads((UP/'SOURCE.json').read_text());qlabels,qedges=quotient(source,parent['surgeries']);qset=set(qedges);pdel={tuple(e) for e in parent['deleted_edges']};pedges=sorted(qset-pdel)
 need(parent['source_case_index']==24 and parent['labels']==qlabels and parent['edges']==[list(e) for e in pedges],'parent 508 graph reconstruction');need(parent['vertices']==508 and parent['edge_count']==2514,'parent size')
 pk23,pk4=forbidden(qlabels,qedges);pc,pu,ph=hitting_counts(pk23,pdel);need((len(pk23),len(pk4),pc,pu,ph)==(6,0,12,32,{0:0,1:0,2:0,3:0,4:0,5:0,6:14400}),'parent minimum repair census');need(forbidden(qlabels,pedges)==([],[]),'parent repaired obstructions')
 labels=graph['labels'];active=set(labels);need(labels==sorted(active) and len(labels)==301,'core labels');edges=sorted(e for e in pedges if e[0] in active and e[1] in active);need(graph['edges']==[list(e) for e in edges] and graph['vertices']==301 and graph['edge_count']==1452,'core induced graph')
 core_qedges=sorted(e for e in qedges if e[0] in active and e[1] in active);cdel=sorted(set(core_qedges)-set(edges));need(graph['relevant_deleted_edges']==[list(e) for e in cdel] and len(cdel)==5,'core relevant deletions')
 ck23,ck4=forbidden(labels,core_qedges);cc,cu,ch=hitting_counts(ck23,cdel);need((len(ck23),len(ck4),cc,cu,ch)==(5,0,11,26,{0:0,1:0,2:0,3:0,4:0,5:2400}),'core minimum repair census');fk23,fk4=forbidden(labels,edges);need(not fk23 and not fk4,'core forbidden subgraphs')
 deg={v:0 for v in labels}
 for u,v in edges:deg[u]+=1;deg[v]+=1
 need((min(deg.values()),max(deg.values()))==(4,24),'degree range');need(graph['merged_degrees']=={str(v):deg[v] for v in (75,76,272,273)},'merged degrees')
 cols=five['colours'];need(set(cols)=={str(v) for v in labels} and set(cols.values())==set(range(5)),'five-colouring domain');need(all(cols[str(u)]!=cols[str(v)] for u,v in edges),'five-colouring edge')
 words=deletions['colourings'];need(set(words)=={str(v) for v in labels},'deletion-colouring domain')
 for removed in labels:
  order=[v for v in labels if v!=removed];word=words[str(removed)];need(len(word)==300 and all(type(c) is int and 0<=c<4 for c in word),'deletion word format');colour=dict(zip(order,word));need(all(removed in (u,v) or colour[u]!=colour[v] for u,v in edges),'deletion colouring edge')
 tri=graph['triangle'];es=set(edges);need(len(tri)==3 and all(tuple(sorted(e)) in es for e in itertools.combinations(tri,2)),'pin triangle');raw=cnf_bytes(labels,edges,tri);need(raw==(D/'four_colour.cnf').read_bytes(),'exact CNF');need(sha(D/'four_colour.lrat')==expected['LRAT_sha256'],'LRAT identity')
 return {'verified':True,'vertices':301,'edges':1452,'minimum_degree':4,'maximum_degree':24,'parent_vertices':508,'parent_K23_pairs':6,'parent_minimum_deletions':6,'parent_minimum_hitting_sets':14400,'core_pre_repair_K23_pairs':5,'core_minimum_deletions':5,'core_minimum_hitting_sets':2400,'final_K23_pairs':0,'final_K4s':0,'five_colouring_checked':True,'single_vertex_deletion_colouring_count':301,'vertex_critical_if_LRAT_accepts':True,'CNF_variables':1204,'CNF_clauses':6112,'CNF_sha256':hashlib.sha256(raw).hexdigest(),'LRAT_sha256':sha(D/'four_colour.lrat'),'method':'independent source quotient reconstruction, exact obstruction and hitting-set censuses, explicit colouring audits, and byte-exact CNF rebuild'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--work',type=pathlib.Path,required=True);a=ap.parse_args();a.work.mkdir(parents=True,exist_ok=True)
 parent=json.loads((D/'parent508.json').read_text());graph=json.loads((D/'graph.json').read_text());five=json.loads((D/'five_colouring.json').read_text());deletions=json.loads((D/'vertex_deletion_colours.json').read_text());expected=json.loads((D/'expected.json').read_text());r=audit(parent,graph,five,deletions,expected);need(r==expected['verification'],'expected receipt')
 controls={}
 for name,objs,mutate in [
  ('altered_graph',[copy.deepcopy(parent),copy.deepcopy(graph),copy.deepcopy(five),copy.deepcopy(deletions)],lambda x:x[1]['edges'].pop()),
  ('bad_five_colouring',[copy.deepcopy(parent),copy.deepcopy(graph),copy.deepcopy(five),copy.deepcopy(deletions)],lambda x:x[2]['colours'].__setitem__(str(x[1]['edges'][0][1]),x[2]['colours'][str(x[1]['edges'][0][0])])),
  ('missing_deletion_witness',[copy.deepcopy(parent),copy.deepcopy(graph),copy.deepcopy(five),copy.deepcopy(deletions)],lambda x:x[3]['colourings'].pop(next(iter(x[3]['colourings']))))]:
  mutate(objs)
  try:audit(*objs,expected)
  except ValueError:controls[name]=True
  else:raise ValueError('bad artifact accepted: '+name)
 need(controls==expected['negative_controls'],'negative controls');r['negative_controls']=controls;(a.work/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,sort_keys=True))
if __name__=='__main__':main()
