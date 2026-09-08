"""Decode a complete43 covering code; duplicates are explicitly allowed."""
from pathlib import Path
from itertools import combinations
from functools import lru_cache
import argparse,json
import base,tails,strengthen
HERE=Path(__file__).resolve().parent

class Carrier:
 def __init__(self,parent):
  self.parent=parent;self.counts=json.loads((HERE/'GLOBAL_COUNTS.json').read_text());self.rows=self.counts['branches'];self.total=self.counts['whole_graph_representation_count'];self.catalogs={c['n']:c for c in json.loads((HERE/'TAIL_COVERS.json').read_text())['catalogs']}
  self.cover=lru_cache(None)(self._cover)
 def _cover(self,n,index):return tails.PartitionCover(tails.graph6(self.catalogs[n]['entries'][index]['graph6']))
 def tail(self,row,index):
  if type(index) is not int or not 0<=index<row['tail_carrier_count']:raise ValueError('Tail index')
  if row['carrier_mode']!='catalog_embedding':return None
  t=row['branch'][2];n=row['residual_vertices']
  for entry in self.catalogs[n]['entries']:
   count=entry['embedding_covers_by_last_red_edges'][t]
   if index<count:
    cover=self.cover(n,entry['index']);order=cover.unrank_embedding(t,index)
    return {'catalog_order':n,'catalog_index':entry['index'],'embedding_index':index,'new_to_catalog':order,'rows':cover.rows}
   index-=count
  raise ValueError('Tail cover exhausted')
 def locate(self,index):
  if type(index) is not int or not 0<=index<self.total:raise ValueError('Global covering code')
  for row in self.rows:
   if index<row['whole_graph_cover_count']:return row,index
   index-=row['whole_graph_cover_count']
  raise ValueError('Branch cover exhausted')
 def unrank(self,index):
  row,local=self.locate(index);p=self.parent['model'].Packing(row['branch']);local,tailcode=divmod(local,row['tail_carrier_count']);tail=self.tail(row,tailcode);inside={tuple(x) for x in row['residual_pairs']};matrices=[];digits=[]
  oldtail=tailcode
  for i,j in p.matrix_pairs:
   if (i,j) in inside and tail is not None:
    offset=43-row['residual_vertices'];order=tail['new_to_catalog'];rows=tail['rows']
    value=sum(((rows[order[u-offset]]>>order[v-offset])&1)<<(a*len(p.blocks[j])+b) for a,u in enumerate(p.blocks[i]) for b,v in enumerate(p.blocks[j]))
   else:
    domain=p.matrix_domain(i,j)
    if (i,j) in inside:oldtail,digit=divmod(oldtail,len(domain))
    else:local,digit=divmod(local,len(domain));digits.append(digit)
    value=domain[digit]
   matrices.append(value)
  if local or (tail is None and oldtail):raise ValueError('Unused mixed-radix digit')
  p.check_matrices(matrices);graph=p.graph(matrices)
  if tail is not None:tail={k:v for k,v in tail.items() if k!='rows'}
  return {'status':'COMPLETE43_COVERING_STATE_NOT_TARGET','global_code':index,'task_id':row['task_id'],'parameters':{'branch':row['branch'],'matrices':matrices},'tail_code':tailcode,'tail_embedding':tail,'outside_digits':digits,'graph':graph}
 def rank_code(self,task_id,tail_code,outside_digits):
  rows=[r for r in self.rows if r['task_id']==task_id]
  if len(rows)!=1:raise ValueError('Task ID')
  row=rows[0];p=self.parent['model'].Packing(row['branch']);inside={tuple(x) for x in row['residual_pairs']};radices=[len(p.matrix_domain(i,j)) for i,j in p.matrix_pairs if (i,j) not in inside]
  if type(tail_code) is not int or not 0<=tail_code<row['tail_carrier_count'] or not isinstance(outside_digits,list) or len(outside_digits)!=len(radices):raise ValueError('Code schema')
  local=0
  for digit,radix in reversed(list(zip(outside_digits,radices))):
   if type(digit) is not int or not 0<=digit<radix:raise ValueError('Outside digit')
   local=local*radix+digit
  local=local*row['tail_carrier_count']+tail_code
  return sum(r['whole_graph_cover_count'] for r in self.rows[:self.rows.index(row)])+local

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path);p.add_argument('--index',type=int,required=True);p.add_argument('--output',type=Path);a=p.parse_args();parent=base.load(a.base);family=Carrier(parent);d=family.unrank(a.index)
 matrix=parent['verify_target'].adjacency(d['graph']);packing=parent['model'].Packing(d['parameters']['branch']);d['closure_obstruction']=strengthen.check_closure(matrix,packing)
 d['target_check']=parent['verify_target'].count(d['graph'])
 if a.output:
  if a.output.exists():raise ValueError('Output already exists')
  a.output.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
 print(json.dumps(d,sort_keys=True))
