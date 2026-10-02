#!/usr/bin/env python3
"""Separate physical-coordinate full catalogue, no cyclic polynomial import."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import argparse,json,hashlib

def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args();z=json.loads((a.work/'INVERSE.json').read_bytes());columns=[int(s,16)for s in z['inverse_columns_hex']]
 need(z['points']==list(range(1,103))and len(columns)==102 and all(0<=c<1<<102 for c in columns),'whole original point coordinate domain')
 rows=[{(k*s)%103 for s in range(80,87)}for k in range(1,103)]
 sets=[{r for r in range(1,103)if c>>(r-1)&1}for c in columns]
 for k,row in enumerate(rows):
  for j,col in enumerate(sets):need(len(row&col)%2==int(k==j),'every set-based physical inverse entry')
 hist=Counter();digest=hashlib.sha256();count=0;allword=(1<<102)-1
 for cardinality in [1,3]:
  for ids in combinations(range(102),cardinality):
   word=allword
   for j in ids:word^=columns[j]
   w=word.bit_count();hist[w]+=1;count+=1;need(count<=2_000_000,'INCOMPLETE fixed2M full catalogue guard');digest.update(enc([tuple(j+1 for j in ids),format(word,'x'),w]))
 expected=json.loads((a.work/'HISTOGRAM.json').read_bytes())['weight_histogram'];need({str(k):v for k,v in sorted(hist.items())}==expected,'entire physical/full and gap-quotient histograms differ')
 print(json.dumps({'complete':True,'author_helpers_imported':False,'cyclic_polynomial_code_imported':False,'full_literal_syndromes':count,'full_minimum_weight':min(hist),'weight15_candidates':hist[15],'set_based_inverse_entry_checks':10404,'entire_histogram':dict(sorted(hist.items())),'full_literal_word_stream_sha256':digest.hexdigest()},sort_keys=True))
if __name__=='__main__':main()
