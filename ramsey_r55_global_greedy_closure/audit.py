"""Entry-level global closure, covering-code, and physical transport controls."""
from pathlib import Path
from itertools import combinations
import argparse,hashlib,json,random,time
import base,tails,check_tails,family_counts,check_global,strengthen,carrier
HERE=Path(__file__).resolve().parent

def require(condition,message):
 if not condition:raise ValueError(message)

def extra_check(branch,clauses):
 require(clauses==list(check_global.extras(branch)),'Independent residual clause mismatch')

def audit(parent_path):
 parent=base.load(parent_path);family=carrier.Carrier(parent);tailcount=json.loads((HERE/'TAIL_COVERS.json').read_text());rows=family.rows
 require(tails.census()==tailcount,'Tail census changed')
 tail_audit=check_tails.check();require(tail_audit==json.loads((HERE/'TAIL_AUDIT.json').read_text()),'Tail audit changed')
 require(family_counts.compute(parent_path)==family.counts,'Family census changed');bound=check_global.counts(parent_path)
 tail_boundaries=0;physical_tail_edges=0
 for c in tailcount['catalogs']:
  for entry in c['entries']:
   cv=family.cover(c['n'],entry['index']);n,edges=check_tails.parse(entry['graph6'])
   for t,size in enumerate(entry['embedding_covers_by_last_red_edges']):
    if not size:continue
    for index in sorted({0,size//2,size-1}):
     order=cv.unrank_embedding(t,index);require(cv.rank_embedding(t,order)==index,'Tail code inverse')
     require(sorted(order)==list(range(n)),'Physical vertex bijection')
     for u,v in combinations(range(n),2):
      expected=(min(order[u],order[v]),max(order[u],order[v])) in edges
      require(bool(cv.rows[order[u]]>>order[v]&1)==expected,'Independent physical tail edge');physical_tail_edges+=1
     for start in range(0,n-3,3):require(all((min(order[u],order[v]),max(order[u],order[v])) not in edges for u,v in combinations(range(start,start+3),2)),'Independent triple image')
     last=order[-3:];mask=sum(int((min(last[u],last[v]),max(last[u],last[v])) in edges)<<k for k,(u,v) in enumerate(combinations(range(3),2)));require(mask==(0,1,3,7)[t],'Final physical shape');tail_boundaries+=1
 formula_stats=[];extra_total=multi_total=0;codes=0;transport_edges=0;normalization_fixtures=0;negative=0;offset=0
 for row in rows:
  b=row['branch'];p=parent['model'].Packing(b);new=list(strengthen.extra_clauses(p));extra_check(b,new);stats={str(k):v for k,v in strengthen.stats(p).items()}
  oldrow=next(x for x in json.loads((parent_path/'COUNTS.json').read_text())['branches'] if x['branch']==b)
  formula_stats.append({'task_id':row['task_id'],'branch':b,'variables':847,'parent_clauses':oldrow['cnf_clauses'],'extra_clauses':len(new),'clauses':oldrow['cnf_clauses']+len(new),'extra_statistics':stats})
  extra_total+=len(new);multi_total+=sum(x['across_three_or_more_blocks'] for x in stats.values())
  if new:
   for changed in (new[:-1],[tuple(-x for x in new[0])]+new[1:]):
    try:extra_check(b,changed)
    except ValueError:negative+=1
    else:raise ValueError('Malformed extra formula accepted')
  for index in sorted({offset,offset+row['whole_graph_cover_count']//2,offset+row['whole_graph_cover_count']-1}):
   d=family.unrank(index);require(family.rank_code(d['task_id'],d['tail_code'],d['outside_digits'])==index,'Whole code inverse')
   matrix=parent['verify_target'].adjacency(d['graph']);bits=int(d['graph']['red_hex'],16)
   for k,(u,v) in enumerate(combinations(range(43),2)):require(matrix[u][v]==((bits>>k)&1),'Physical graph transport');transport_edges+=1
   p.check_matrices(d['parameters']['matrices'])
   if d['tail_embedding']:
    residual=list(range(43-row['residual_vertices'],43))
    require(all(not all(matrix[u][v] for u,v in combinations(q,2)) for q in combinations(residual,3)),'Catalog residual triangle')
    require(all(any(matrix[u][v] for u,v in combinations(q,2)) for q in combinations(residual,5)),'Catalog residual blue five')
   codes+=1
  offset+=row['whole_graph_cover_count']
  # Every prescribed branch has a physical structural fixture: fixed internal
  # edges and blue cross edges. These are intentionally not good43 graphs.
  bits=sum(color<<p.physical_positions[pair] for pair,color in p.fixed.items());fixture={'n':43,'red_hex':format(bits,'0226x')};normal=strengthen.normalize(fixture,parent)
  require(normal['parameters']['branch']==b,'Greedy normalizer branch fixture')
  oldmatrix=parent['verify_target'].adjacency(fixture);newmatrix=parent['verify_target'].adjacency(normal['graph']);order=normal['new_to_old']
  require(sorted(order)==list(range(43)),'Full graph permutation')
  for u,v in combinations(range(43),2):require(newmatrix[u][v]==oldmatrix[order[u]][order[v]],'Normalizer vertex transport')
  normalization_fixtures+=1
 require(offset==family.total,'Whole covering intervals')
 for bad in (-1,family.total,True):
  try:family.unrank(bad)
  except ValueError:negative+=1
  else:raise ValueError('Bad global index accepted')
 for b in ([5,0,0],[7,3,3],[4,1,0],[7,True,0]):
  require(not strengthen.allowed(b),'Invalid branch accepted');negative+=1
 return {'status':'VERIFIED_GLOBAL_GREEDY_CLOSURE_INTERFACE','independent_tail_audit':tail_audit,'global_bound':bound,'tail_code_boundary_checks':tail_boundaries,'independent_tail_edge_checks':physical_tail_edges,'whole43_code_boundary_checks':codes,'whole43_edge_checks':transport_edges,'normalization_fixtures':normalization_fixtures,'normalization_fixture_edges':normalization_fixtures*903,'all_extra_clauses_compared':extra_total,'extra_clauses_meeting_at_least_three_blocks':multi_total,'negative_controls':negative,'formula_stats':formula_stats,'target_found':False,'solver_calls':0}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path,default=base.DEFAULT);a=p.parse_args();start=time.monotonic();d=audit(a.base.resolve());(HERE/'INTERFACE_AUDIT.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(json.dumps({'seconds':time.monotonic()-start,**{k:v for k,v in d.items() if k!='formula_stats'}},sort_keys=True))
