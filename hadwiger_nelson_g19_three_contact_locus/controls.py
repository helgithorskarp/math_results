"""Independent distance identities and corruption controls for locus proof."""
from pathlib import Path
from itertools import combinations
import importlib.util,json,copy
P=Path(__file__).resolve().parent

def load(name):
 s=importlib.util.spec_from_file_location(name,P/(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
p=load('produce');v=load('verify');cert=json.loads((P/'certificate.json').read_text())
a,_,_,_=p.geometry();b,_,_,_=v.check_g19_geometry(json.loads((P/'source_g19.json').read_text()))
if a!=b:raise RuntimeError('independent source coordinates')
new=[(v.number(v.Q(1,2)),v.minus(v.ONE,v.times(v.S,v.Q(1,2)))),(v.ONE,v.plus(v.ONE,v.S))];pts=a+new
pairs=triples=0
for i,j in combinations(range(21),2):
 if p.norm(p.psub(pts[i],pts[j]))!=v.norm(v.pminus(pts[i],pts[j])):raise RuntimeError('norm mismatch')
 pairs+=1
for i,j,k in combinations(range(19),3):
 u=p.psub(a[j],a[i]);w=p.psub(a[k],a[i]);det=p.sub(p.mul(u[0],w[1]),p.mul(u[1],w[0]));left=p.scale(p.mul(det,det),4)
 A=v.norm(v.pminus(a[j],a[i]));B=v.norm(v.pminus(a[k],a[i]));C=v.norm(v.pminus(a[j],a[k]));z=v.minus(v.plus(A,B),C);right=v.minus(v.times(v.m8(A,B),4),v.m8(z,z))
 if left!=right:raise RuntimeError('determinant/Gram mismatch')
 triples+=1
changes={}
c=copy.deepcopy(cert);c['new_points'][0][0][0]='2/3';changes['wrong_external_centre']=c
c=copy.deepcopy(cert);c['edges'].remove([7,19]);changes['missing_new_contact']=c
c=copy.deepcopy(cert);c['unit_radius_triples']+=1;changes['incorrect_radius_census']=c
c=copy.deepcopy(cert);c['four_colouring'][19]=c['four_colouring'][7];changes['improper_extension_word']=c
c=copy.deepcopy(cert);del c['centre_multiplicities']['20'];changes['missing_centre_multiplicity']=c
for name,c in changes.items():
 try:v.verify(c)
 except ValueError:pass
 else:raise RuntimeError('accepted mutation '+name)
print(json.dumps({'status':'CONTROLS_PASS','independent_point_rows':19,'independent_distance_rows':pairs,'independent_Gram_determinant_rows':triples,'rejected_mutations':list(changes)},indent=2,sort_keys=True))
