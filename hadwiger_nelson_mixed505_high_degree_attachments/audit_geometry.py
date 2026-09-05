#!/usr/bin/env python3
"""Full independent rational geometry census for one high-degree attachment."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import importlib.util,argparse,json

HERE=Path(__file__).resolve().parent
PATH=HERE.parent/'hadwiger_nelson_mixed505_all_gadget_anchors/audit.py'
if sha256(PATH.read_bytes()).hexdigest()!='e0a1f96817c05545b3e1b03d16936700e5ce71143072df1660d4a4945dceb599':raise ValueError('rational dependency mismatch')
spec=importlib.util.spec_from_file_location('rational_geometry',PATH)
A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)
K=A.K

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--anchor',type=int,choices=[28,185],required=True)
 parser.add_argument('--expected',type=Path,required=True)
 args=parser.parse_args();p=args.anchor
 B,V,D,inc,EB,EV=A.construction()
 degrees=Counter(i for edge in EB for i in edge)
 if [i for i in range(len(B)) if degrees[i]>=22]!=[0,28,185]:raise ValueError('wrong high-degree vertex set')
 order=[p]+[i for i in range(len(B)) if i!=p]
 BP=[K.add(B[i],K.negate(B[p])) for i in order]
 ch=A.Classification();counts,groups=A.T.enumerate_classes(BP,D,False,ch)
 partition=sha256();hist=[Counter() for _ in V]
 for ee in sorted(groups.values()):
  partition.update((';'.join(f'{b},{d}' for b,d in ee)+'\n').encode())
  per_anchor=Counter(q for b,d in ee for q,v in inc[d])
  for q,n in per_anchor.items():hist[q][n]+=1
 result={'B_anchor':p,'degree':degrees[p],'nonzero_pairs':counts.pop('nonzero_pairs'),
         'pairs':counts,'ambient_classes':len(groups),'classification_sha256':ch.h.hexdigest(),
         'ambient_edge_partition_sha256':partition.hexdigest(),
         'anchor_classes_total':sum(sum(h.values()) for h in hist),
         'maximum_cross_edges':max(max(h) for h in hist)}
 expected=json.loads(args.expected.read_text())
 for key in result:
  if key!='nonzero_pairs' and result[key]!=expected[key]:raise ValueError('geometry mismatch: '+key)
 for q,h in enumerate(hist):
  row=expected['anchors'][q]
  if row['anchor']!=q or row['classes']!=sum(h.values()) or row['unit_multipliers']!=2*sum(h.values()) or {str(k):v for k,v in sorted(h.items())}!=row['histogram']:
   raise ValueError('projected geometry mismatch')
 result['all_pair_classifications_and_edge_groups_match']=True
 result['all_anchor_histograms_match']=True
 print(json.dumps(result,indent=2))

if __name__=='__main__':main()
