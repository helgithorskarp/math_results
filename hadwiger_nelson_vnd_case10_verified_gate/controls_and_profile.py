"""Reproduce parser controls and the fixed exact cross-interface profile."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q
import json,sys
import os
P=Path(os.environ.get("VND_WORKDIR",str(Path(__file__).resolve().parent/"work"))).resolve();sys.path.insert(0,str(P))
from audit_source import parse_scalar,require

def main():
 bad=['__import__("os")','sqrt(-1)','sqrt(7)','1/(1+sqrt(2))','1.5','sqrt(2,3)','(lambda:0)()','2**3']
 for s in bad:
  try:parse_scalar(s)
  except ValueError:pass
  else:raise ValueError('unsafe/out-of-field syntax accepted '+s)
 for s,k,value in [('sqrt(15/2)',7,Q(1,2)),('1/(2*sqrt(2))',1,Q(1,4)),('sqrt(2/3)',3,Q(1,3))]:
  want=[Q(0)]*8;want[k]=value;require(parse_scalar(s)==tuple(want),'exact parser control')
 edges=json.loads((P/'exact_edges.json').read_text());cross=[(u,v) for u,v in edges if 0<u<=32256<v];count=Counter(x for e in cross for x in e);labels=sorted(count)
 require(len(cross)==120 and len(count)==240 and set(count.values())=={1},'cross edges are matching')
 profile=json.loads((P/'interface_profile.json').read_text())
 require(profile['boundary_vertex_labels']==labels,'exact boundary labels');require(sum(x<=32256 for x in labels)==sum(x>32256 for x in labels)==120,'half-boundary count')
 require(profile['target_508_remaining_vertices_if_all_boundary_retained']==508-len(labels),'order budget arithmetic')
 print(json.dumps({'verified':True,'rejected_parser_inputs':len(bad),'radical_controls':3,'cross_edges':len(cross),'boundary_vertices':len(labels),'cross_interface_is_matching':True,'non_four_colourability_claimed':False},indent=2))
if __name__=='__main__':main()
