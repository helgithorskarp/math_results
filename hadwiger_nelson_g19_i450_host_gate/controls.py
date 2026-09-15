"""Check geometry independently, then reject altered interface witnesses."""
import copy,importlib.util,json
from pathlib import Path
from itertools import combinations
P=Path(__file__).resolve().parent

def load(name):
 s=importlib.util.spec_from_file_location(name,P/(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
v=load('verify');g=load('generate');cert=json.loads((P/'certificate.json').read_text())
a,D,edges,mp=g.generate();b,E,ve,_,hm,*_=v.geometry()
if edges!=ve or mp[19:]!=hm:raise RuntimeError('independent graph/mapping mismatch')
if len(a)!=len(b):raise RuntimeError('point count')
for p,q in zip(a,b):
 if any(x*E!=y*D for c,d in zip(p,q) for x,y in zip(c,d)):raise RuntimeError('independent coordinates')
count=0
for i,j in combinations(range(len(a)),2):
 n=g.twice_norm(a[i],a[j]);m=v.twice_norm(b[i],b[j])
 if any(x*E*E!=y*D*D for x,y in zip(n,m)):raise RuntimeError('independent distance mismatch')
 count+=1
changes={}
c=copy.deepcopy(cert);c['four_colouring']='11'+c['four_colouring'][2:];changes['improper_four_word']=c
c=copy.deepcopy(cert);c['boundary_word']='3'+c['boundary_word'][1:];changes['wrong_host_intersection_word']=c
c=copy.deepcopy(cert);c['extra_edges']=c['extra_edges'][:-1];changes['missing_private_contact']=c
for name,c in changes.items():
 try:v.verify(c)
 except ValueError:pass
 else:raise RuntimeError('accepted corruption '+name)
print(json.dumps({'status':'CONTROLS_PASS','independent_coordinate_rows':len(a),'independent_edge_entries':len(edges),'independent_distance_rows':count,'rejected_mutations':list(changes)},indent=2,sort_keys=True))
