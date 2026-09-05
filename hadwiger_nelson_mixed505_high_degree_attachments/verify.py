#!/usr/bin/env python3
"""Exact repaired coloring cover at B vertices 28 and 185; B origin is imported."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import importlib.util,argparse,json
from cover import cover

HERE=Path(__file__).resolve().parent
PATH=HERE.parent/'hadwiger_nelson_mixed505_all_gadget_anchors/verify.py'
if sha256(PATH.read_bytes()).hexdigest()!='526b12cbd9d28217e59feb7191c93ace4e5a572ebeadd66cdf384393126aee38':raise ValueError('integer census dependency mismatch')
spec=importlib.util.spec_from_file_location('integer_census',PATH)
F=importlib.util.module_from_spec(spec);spec.loader.exec_module(F)


def libraries(B,V,EB,EV,baseline=False):
 libB,libV=F.libraries(B,V,EB,EV)
 if baseline:return libB,libV
 for side,lib,points,edges in [('B',libB,B,EB),('V',libV,V,EV)]:
  rows=[tuple(map(int,line)) for line in (HERE/f'new_{side}.txt').read_text().splitlines()]
  F.require(len(rows)==5,'wrong repair library size')
  for c in rows:
   F.require(len(c)==len(points) and c[0]==0 and all(x in range(4) for x in c),'bad repair coloring domain')
   F.require(all(c[i]!=c[j] for i,j in edges),'invalid repair coloring')
  lib.extend(rows)
 return libB,libV


def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--baseline',action='store_true',help='reproduce old-library residuals without claiming a closure')
 parser.add_argument('--details-dir',type=Path,help='write the full per-anchor summaries')
 args=parser.parse_args()
 if args.details_dir:args.details_dir.mkdir(parents=True,exist_ok=True)
 B,V,D,inc,EB,EV=F.construction();degree=Counter(i for e in EB for i in e)
 F.require([i for i in range(len(B)) if degree[i]>=22]==[0,28,185],'wrong high-degree vertex set')
 libB,libV=libraries(B,V,EB,EV,args.baseline)
 summaries=[]
 for p in [28,185]:
  order=[p]+[i for i in range(len(B)) if i!=p]
  BP=[F.subtract(B[i],B[p]) for i in order]
  colors=[tuple(c[i]^c[p] for i in order) for c in libB]
  counts,groups,ch=F.enumerate_groups(BP,D)
  result,_=cover(groups,inc,colors,libV)
  result={'B_anchor':p,'point_scale72':B[p],'degree':degree[p],'classification_sha256':ch,'pairs':counts,'ambient_classes':len(groups),**result}
  if not args.baseline:F.require(result['uncovered_total']==0,'uncovered class')
  if args.details_dir:(args.details_dir/f'anchor_{p}.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
  anchor_rows=result.pop('anchors')
  result['anchor_summary_sha256']=sha256(json.dumps(anchor_rows,separators=(',',':')).encode()).hexdigest()
  summaries.append(result)
 output={'baseline':args.baseline,'library_B':len(libB),'library_V':len(libV),'high_degree_B_vertices':[0,28,185],'new_B_vertices_checked':[28,185],'origin_covered_by_previous_theorem':True,'new_anchor_classes_total':sum(r['anchor_classes_total'] for r in summaries),'uncovered_total':sum(r['uncovered_total'] for r in summaries),'families':summaries}
 print(json.dumps(output,indent=2))


if __name__=='__main__':main()
