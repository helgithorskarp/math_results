"""Reject malformed certificates and cross-check all exact distance rows."""
import copy,importlib.util,json
from pathlib import Path
from itertools import combinations
from fractions import Fraction
P=Path(__file__).resolve().parent

def load(name):
 s=importlib.util.spec_from_file_location(name,P/(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
v=load('verify');g=load('produce');cert=json.loads((P/'certificate.json').read_text())
v.verify(cert)
mutations={}
x=copy.deepcopy(cert);x['coordinates'][20][0][0]='999';mutations['coordinate']=x
x=copy.deepcopy(cert);x['coordinates'][20]=x['coordinates'][19];mutations['collision']=x
x=copy.deepcopy(cert);x['edges'].remove([7,40]);mutations['missing_only_new_contact']=x
x=copy.deepcopy(cert);a,b=x['edges'][0];x['five_colouring'][b]=x['five_colouring'][a];mutations['improper_five_word']=x
x=copy.deepcopy(cert);x['f29_extension_words'][1]=x['f29_extension_words'][0][:];mutations['lost_contact_flexibility']=x
x=copy.deepcopy(cert);x['f29_extension_words'][0][25]=0;mutations['bad_shared_triangle']=x
for name,x in mutations.items():
 try:v.verify(x)
 except ValueError:pass
 else:raise RuntimeError('accepted mutation '+name)
pts=[tuple(tuple(Fraction(x) for x in a) for a in p) for p in cert['coordinates']]
count=0
for a,b in combinations(range(45),2):
 if g.norm(g.psub(pts[a],pts[b]))!=v.norm(v.pminus(pts[a],pts[b])):raise RuntimeError('arithmetic disagreement')
 count+=1
print(json.dumps({'rejected_mutations':list(mutations),'entrywise_distance_comparisons':count,'status':'CONTROLS_PASS'},indent=2,sort_keys=True))
