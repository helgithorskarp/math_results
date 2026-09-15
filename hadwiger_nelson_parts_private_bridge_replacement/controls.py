#!/usr/bin/env python3
"""Metric and corrupt-colouring controls for the declared exact support."""
import json,tempfile
from pathlib import Path
import verify as v

def run():
 z=[0]*32;one=z.copy();one[0]=96;y=z.copy();y[8]=96;sy=z.copy();sy[9]=96
 mixed=one.copy();mixed[8]=96
 both=mixed.copy();both[16]=96;both[24]=-96
 near=z.copy();near[0]=95
 fixtures=[(z,z,{}),(one,z,{(1,0):18432}),(y,z,{(1,0):36864,(3,0):-9216}),(sy,z,{(1,0):110592,(3,0):-27648}),(mixed,z,{(1,0):55296,(3,0):-9216,(1,1):36864}),(both,z,{(1,0):110592,(3,0):-18432}),(near,z,{(1,0):18050})]
 for a,b,expected in fixtures:
  v.require(v.norm_twice(a,b)==expected and v.norm_twice(b,a)==expected,'exact metric fixture')
 pts=v.load_points();report,edges=v.verify();word=(v.HERE/'colour4.txt').read_text().strip();u,w=edges[0]
 conflict=list(word);conflict[w]=conflict[u]
 bad=[word[:-1],'4'+word[1:],''.join(conflict)]
 rejected=0
 with tempfile.TemporaryDirectory() as temp:
  p=Path(temp)/'word.txt'
  for text in bad:
   p.write_text(text+'\n')
   try:v.check_word(p,pts,edges,4)
   except ValueError:rejected+=1
 v.require(rejected==len(bad),'corrupt witness accepted')
 return {'all_checks':True,'metric_fixtures':len(fixtures),'ordered_norm_checks':2*len(fixtures),'corrupt_witnesses_rejected':rejected}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
