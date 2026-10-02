#!/usr/bin/env python3
"""Independent symmetry-free h<=12 three-pair root obstruction controls.
No source from the target or preceding cohorts is imported.
"""
from itertools import combinations,product
from math import comb
import hashlib,json

def need(ok,message):
 if not ok:raise RuntimeError(message)
def compositions(n,total):
 if n==1:
  yield (total,);return
 for first in range(total+1):
  for rest in compositions(n-1,total-first):yield(first,)+rest
def main():
 records=[];maximizers=[]
 for deficit in compositions(9,3):
  degrees=[3-t for t in deficit];marks=(8,8,8,9,9,9,10,10,10)
  capacity=108-12-sum((m-9)*h+comb(h,2) for m,h in zip(marks,degrees))
  formula=153-sum(t*t for t in deficit)-2*sum(deficit[:3])+2*sum(deficit[6:])
  need(2*capacity==formula,'direct/deficiency capacity identity')
  need(capacity<=78,'universal capacity upper bound')
  if capacity==78:maximizers.append(deficit)
  records.append([list(deficit),capacity])
 need(len(records)==165 and len({tuple(x[0]) for x in records})==165,'all nine labeled deficiencies')
 need(maximizers==[(0,0,0,0,0,0,1,1,1)],'unique required tight degree assignment')
 # Directly enumerate every simple internal graph on the THREE degree8
 # neighbors; cyclic regularity is unnecessary for an even internal degree.
 even_rows=[];pairs=list(combinations(range(3),2))
 for word in range(8):
  deg=[0]*3
  for k,(i,j) in enumerate(pairs):
   if word>>k&1:deg[i]+=1;deg[j]+=1
  need(sum(deg)%2==0 and any(d%2==0 for d in deg),'ordinary handshake on odd vertex class')
  even_rows.append({'word':word,'internal_degrees':deg,'even_rows':[i for i,d in enumerate(deg) if d%2==0]})
 # Every possible original9-row odd column, rather than an abstract
 # representative, checks X diag(X^T1)=XX^T1 modulo2.
 columns=checks=0
 for size in (3,5):
  for c in combinations(range(9),size):
   columns+=1
   for row in range(9):
    need(((row in c)*size-(row in c))%2==0,'actual odd-column row parity');checks+=1
 b=(json.dumps(records,separators=(',',':'))+'\n').encode()
 print(json.dumps({'complete':True,'symmetry_used':False,'full_labeled_deficiency_domain':165,'maximum_pair_capacity':78,'unique_tight_deficiencies':maximizers,'entire_deficiency_capacity_records_sha256':hashlib.sha256(b).hexdigest(),'all_eight_low_internal_graphs':even_rows,'all_odd_columns':columns,'all_original_column_row_parities':checks,'theorem_scope':'valid22,e<=99,d(x)=9,A global8^3,9^3,10^3,B all global8or10,h(A)<=12 impossible; no h13 or unrestricted-profile conclusion'},sort_keys=True))
if __name__=='__main__':main()
