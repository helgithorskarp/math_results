"""Exact whole-branch cardinalities of the globally forced packing family."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb,prod,log2
import json
from pathlib import Path
import domains

LAST=('B3','E3','P3','R3')
def kinds(branch):
 if not isinstance(branch,list) or len(branch)!=3 or any(type(x) is not int for x in branch):raise ValueError('branch schema')
 r,s,t=branch
 if r not in (5,6,7) or s not in range(5) or t not in range(4):raise ValueError('branch values')
 return ['R4']*r+['B4']*(7-r)+['R3']*s+['B3']*(4-s)+[LAST[t]]

def branches():return [[r,s,t] for r in (5,6,7) for s in range(5) for t in range(4)]

def polynomial_clauses(types,color):
 poly=[1,0,0,0,0,0]
 for kind in types:
  n,_=domains.TYPES[kind];fixed=domains.inside(kind);atom=[]
  for k in range(n+1):
   atom.append(sum(all(fixed[p]==color for p in combinations(q,2)) for q in combinations(range(n),k)))
  new=[0]*6
  for i,a in enumerate(poly):
   for j,b in enumerate(atom):
    if i+j<=5:new[i+j]+=a*b
  poly=new
 return poly[5]

def count(certificate):
 sizes={(x['left'],x['right']):x['count'] for x in certificate}
 result=[]
 for branch in branches():
  types=kinds(branch);pairs=Counter((types[i],types[j]) for i,j in combinations(range(12),2))
  unrooted=prod(sizes[k]**v for k,v in pairs.items())
  total=prod(len(domains.root_states(types[j])) if i==0 else sizes[types[i],types[j]] for i,j in combinations(range(12),2))
  red=polynomial_clauses(types,1);blue=polynomial_clauses(types,0)
  ordering=120*sum(len(domains.comparable_columns(kind)) for kind in types[1:])
  result.append({'branch':branch,'atoms':types,'count':total,'unrooted_count':unrooted,'red_clauses':red,'blue_clauses':blue,'root_order_clauses':ordering,'cnf_variables':847,'cnf_clauses':red+blue+ordering+1})
 total=sum(x['count'] for x in result);base=60*2**846;f=Fraction(total,base)
 return {'status':'EXACT_GLOBAL_PACKING_FAMILY_COUNT','branches':result,'branch_count':60,'vertices':43,'fixed_edges':57,'variable_edges':846,'matrix_coordinates':66,
         'raw_packing_family':base,'retained_pair_domain_family':sum(x['unrooted_count'] for x in result),'retained_rooted_family':total,'retained_fraction_of_packing':{'numerator':f.numerator,'denominator':f.denominator},
         'full_labelled_graph_space':2**903,'strict_power_of_two_upper_bound':total.bit_length(),'approx_log2_retained':log2(total),
         'five_sets_in_two_atoms':1971,'five_sets_across_three_or_more_atoms':comb(43,5)-1971}

if __name__=='__main__':
 d=count(json.loads(Path(__file__).with_name('DOMAINS.json').read_text()))
 Path(__file__).with_name('COUNTS.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:v for k,v in d.items() if k not in ['branches','retained_fraction_of_packing','full_labelled_graph_space','raw_packing_family']},indent=2))
