#!/usr/bin/env python3
"""Validate the baseline, then reject incomplete and false certificates."""
from pathlib import Path
import copy,json,verify
B=Path(__file__).resolve().parent
c=json.loads((B/'certificate.json').read_text());verify.verify(c)
cases=[]
x=copy.deepcopy(c);x['extensions'].pop();cases.append(('missing complete source word',x))
x=copy.deepcopy(c);w=x['extensions'][0];x['extensions'][0]=w[0]*2+w[2:];cases.append(('unit-edge colour collision',x))
x=copy.deepcopy(c);x['points144'][10][0]+=1;cases.append(('displaced physical point',x))
x=copy.deepcopy(c);x['edges'].remove([4,17]);cases.append(('omitted private unit edge',x))
rejected=[]
for name,x in cases:
    try:verify.verify(x)
    except ValueError:rejected.append(name)
    else:raise ValueError('corruption was accepted: '+name)
# Connectivity implementation has a transparent small-graph oracle:
# paths have bridges, a triangle does not, a bowtie has an articulation.
require=verify.require
require(verify.components(3,[(0,1),(1,2)])==1,'path connected')
require(verify.components(3,[(0,1),(1,2)],removed_vertex=1)==2,'path articulation')
require(verify.components(3,[(0,1),(1,2)],removed_edge=(0,1))==2,'path bridge')
tri=[(0,1),(0,2),(1,2)]
require(all(verify.components(3,tri,removed_vertex=v)==1 for v in range(3)),'triangle vertex connectivity')
require(all(verify.components(3,tri,removed_edge=e)==1 for e in tri),'triangle edge connectivity')
require(verify.components(5,tri+[(0,3),(0,4),(3,4)],removed_vertex=0)==2,'bowtie articulation')
print(json.dumps({'baseline_accepted':True,'corruptions_rejected':rejected,'connectivity_controls_passed':True},indent=2))
