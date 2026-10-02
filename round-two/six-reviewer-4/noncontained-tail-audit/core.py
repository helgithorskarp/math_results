#!/usr/bin/env python3
"""Independent original-point cap/tail reconstruction, no author helpers.
Defining literalD and proof/counts visible; author executable/fixtures unread.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
import argparse,json,hashlib
ROOT=Path(__file__).resolve().parent
def need(ok,m):
 if not ok:raise RuntimeError(m)
def canon(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def pts(m):return tuple(i for i in range(18)if m>>i&1)
def mask(s):return sum(1<<i for i in s)
def parent():
 D=json.loads((ROOT/'PARENT.json').read_text())['words']
 need(len(D)==68 and len(set(D))==68 and all(0<=b<1<<17 and b.bit_count()==5 for b in D),'literal parent words')
 trip=[mask(t)for b in D for t in combinations(pts(b),3)]
 need(len(trip)==680 and len(set(trip))==680 and set(trip)=={mask(t)for t in combinations(range(17),3)},'whole original triple partition')
 return D
def packing(words):
 need(len(words)==len(set(words)) and all(0<=w<1<<18 and w.bit_count()==5 for w in words),'distinct actual weight5 words')
 for u,v in combinations(words,2):need((u&v).bit_count()<=2,'actual word collision')
 triples=[mask(t)for w in words for t in combinations(pts(w),3)]
 need(len(set(triples))==10*len(words),'actual triple packing')
def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args();args.work.mkdir(parents=True,exist_ok=True)
 D=parent();Q=15;holes=[b for b in D if (b&Q).bit_count()==3]
 need(len(holes)==4 and all((b&Q).bit_count()!=4 for b in D),'noncontained Q and four distinct holes')
 candidates=[];cores=[];zero=[];nodes=0;partial_checks=0
 for cp in combinations(range(17),5):
  C=mask(cp)
  if C in D or (C&Q).bit_count()>2:continue
  required=[b for b in D if b not in holes and (b&C).bit_count()>=3]
  if any((b&C).bit_count()==4 for b in required):continue
  candidates.append(C);options={}
  for b in required:
   choices=[b^(1<<v)for v in pts(b)if v in cp]
   options[b]=tuple(t for t in choices if (t&Q).bit_count()<=1 and (t&C).bit_count()<=2)
  capcores=[]
  def walk(left,selected):
   nonlocal nodes,partial_checks
   nodes+=1;need(nodes<=2_000_000,'INCOMPLETE fixed2M core state guard')
   if not left:
    key=[C,sorted(selected.items())];capcores.append(key)
    words=[b for b in D if b not in holes and b not in selected]+[C,Q|(1<<17)]+[t|(1<<17)for t in selected.values()]
    need(len(words)==66,'literal single-core restoration size');packing(words);partial_checks+=1
    return
   remaining={b:tuple(t for t in options[b]if all((t&s).bit_count()<=1 for s in selected.values()))for b in left}
   b=min(left,key=lambda x:(len(remaining[x]),x))
   for t in remaining[b]:walk(left-{b},selected|{b:t})
  walk(set(required),{})
  if not capcores:zero.append(C)
  cores.extend(capcores)
 cores.sort(key=lambda c:(c[0],c[1]));need(len({canon(c)for c in cores})==len(cores),'distinct complete physical keys')
 need(len(candidates)>0 and len(cores)>0,'nonvacuous original carrier')
 raw=canon({'Q':Q,'holes':holes,'caps':candidates,'zero_core_caps':zero,'cores':cores});(args.work/'cores.json').write_bytes(raw)
 histogram=Counter(c[0]for c in cores)
 rec={'complete':True,'parent_triples':680,'old_five_set_domain':6188,'Q':Q,'hole_masks':holes,'prospective_caps':len(candidates),'zero_core_caps':len(zero),'positive_caps':len(histogram),'complete_cores':len(cores),'partial66_packings_checked':partial_checks,'partial_word_pairs_checked':partial_checks*2145,'dfs_nodes':nodes,'entire_physical_carrier_bytes':len(raw),'entire_physical_carrier_sha256':hashlib.sha256(raw).hexdigest(),'cap_multiplicity_histogram':dict(sorted(Counter(histogram.values()).items())),'author_helpers_imported':False}
 print(json.dumps(rec,sort_keys=True))
if __name__=='__main__':main()
