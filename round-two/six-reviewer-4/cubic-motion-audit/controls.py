"""Consequential external-record damages, without expected-byte pins."""
import copy,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from check import validate
from tower import need
r=json.loads(Path(sys.argv[1]).read_text())
def change(r,route,value):
 q=r
 for k in route[:-1]:q=q[k]
 q[route[-1]]=value
cases=[
 ('anchored_constant',['primitive',0,1,0],'0'),
 ('Newton_cubic_sign',['elementary',3,4,9],'1'),
 ('original_raw_sign',['roots',4,'raw',1,0],'1'),
 ('original_map_coefficient',['roots',2,'W',0],'1'),
 ('marked_root_motion',['roots',0,'L',0],'0'),
 ('winning_label_norm',['norms',2],r['norms'][3]),
 ('equality_profile_cost',['scalars','KE',0],'0'),
 ('rigidity_coefficient',['scalars','gamma_squared',0],'1'),
 ('repair_determinant',['scalars','repair_determinant',0],'0'),
 ('skewness_multiplicity',['multiplicity_ratios',2],'1/6'),
 ('deficit_identity',['polynomial_certificates',0,'deficit_residual',0,1],'1'),
 ('distance_identity',['polynomial_certificates',7,'distance_residual',0,1],'1'),
 ('duplicate_root_label',['roots',8,'label'],7),
 ('bool_root_label',['roots',0,'label'],False),
 ('omitted_original',['roots'],r['roots'][:-1]),
 ('dropped_zero_coordinate',['roots',0,'W'],r['roots'][0]['W'][:-1]),
 ('bad_slot_order',['slots'],r['slots'][::-1]),
 ('unrelated_field',['unrelated'],True)]
rejected=[]
for name,route,value in cases:
 q=copy.deepcopy(r);change(q,route,value)
 try:validate(q)
 except(ValueError,TypeError,KeyError,IndexError,ZeroDivisionError):rejected.append(name)
 else:raise ValueError('damaged mathematics accepted: '+name)
need(len(rejected)==18,'whole damage census')
print(json.dumps({'status':'all damages rejected','without_expected_fixture':True,'rejected':rejected},sort_keys=True))
