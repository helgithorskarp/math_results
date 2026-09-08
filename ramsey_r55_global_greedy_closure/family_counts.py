"""Whole-43 covering bound with one coupled residual carrier per branch."""
from pathlib import Path
from itertools import combinations
from math import prod
from fractions import Fraction
import json,argparse
HERE=Path(__file__).resolve().parent

def compute(base):
 old=json.loads((base/'COUNTS.json').read_text());tails=json.loads((HERE/'TAIL_COVERS.json').read_text());by_n={x['n']:x for x in tails['catalogs']}
 pair={(x['left'],x['right']):x['count'] for x in json.loads((base/'DOMAINS.json').read_text())}
 rows=[];removed=[]
 for oldrow in old['branches']:
  r,s,t=oldrow['branch']
  if s==0 or (s<4 and t==3):removed.append(oldrow['branch']);continue
  n=15-3*s;blocks=list(range(7+s,12));types=oldrow['atoms'];old_tail=prod(pair[types[i],types[j]] for i,j in combinations(blocks,2))
  if s<4:
   embedding=by_n[n]['embedding_cover_totals'][t];carrier=min(embedding,old_tail);mode='catalog_embedding' if embedding<old_tail else 'original_pair_matrices'
  else:embedding=1;carrier=1;mode='fixed_triple'
  if oldrow['count']%old_tail:raise ValueError('nonintegral matrix factor')
  bound=oldrow['count']//old_tail*carrier
  rows.append({'branch':[r,s,t],'task_id':f'r{r}-s{s}-t{t}','residual_vertices':n,'residual_blocks':blocks,'residual_pairs':[list(p) for p in combinations(blocks,2)],'parent_count':oldrow['count'],'parent_tail_pair_count':old_tail,'catalog_embedding_cover':embedding,'carrier_mode':mode,'tail_carrier_count':carrier,'other_matrix_count':oldrow['count']//old_tail,'whole_graph_cover_count':bound,'red_four_free_union_size':43-4*r if r<7 else None,'red_triangle_free_union_size':n if s<4 else None})
 total=sum(x['whole_graph_cover_count'] for x in rows);parent=old['retained_rooted_family'];ratio=Fraction(parent,total)
 if len(rows)!=39 or not 4*total<parent:raise ValueError('Declared global factor4 gate failed')
 return {'status':'VERIFIED_EXACT_GLOBAL_CARRIER_BOUND','branches':rows,'removed_normal_form_branches':removed,'branch_count':39,'parent_physical_count':parent,'whole_graph_representation_count':total,'strict_reduction_factor4':4*total<parent,'reduction_factor':{'numerator':ratio.numerator,'denominator':ratio.denominator},'strict_power_two_upper_bound':total.bit_length(),'counts_are':'Exact carrier codes; catalog codes can duplicate physical graphs. Upper bound for the new constrained physical family. Large residual no-red-K4 constraints and remaining global five-sets are not assumed in the product.'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path,default=HERE.parent/'ramsey_r55_global_clique_packing');a=p.parse_args();d=compute(a.base)
 (HERE/'GLOBAL_COUNTS.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:v for k,v in d.items() if k not in ('branches','removed_normal_form_branches')}))
