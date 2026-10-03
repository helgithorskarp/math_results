"""Semantic damages checked against fresh equations, without expected record pins."""
import copy,json,sys
from pathlib import Path
from fractions import Fraction
from second import check

def change(v,path):
 x=v
 for k in path[:-1]:x=x[k]
 k=path[-1];x[k]=str(Fraction(x[k])+1)
def run(v):
 check(v)
 cases=[('original cubic mean',['critical_mean',3,0,0]),('large real repair',['critical_large',2,0,0]),('small beta column',['critical_small',3,2,0]),('marked anchor',['anchor',2,0,0]),('primitive leading factor',['whole_polynomial',9,0,0,0]),('primitive anchored constant',['whole_polynomial',0,4,0,0]),('original root nonlinear jet',['all_nine_roots',3,4,0,0]),('normal fourth curvature',['all_nine_half_normals',3,4,0,0]),('individual fourth constraint',['all_nine_half_normals',5,4,1,0]),('full inverse distance objective',['whole_first_objective',4,0,0]),('physical eta objective',['second_objective_affine',0,0]),('closing real parameter',['closing_parameters',0,0]),('dual weight',['repair_domain','positive_dual_weights',0,0]),('repair cone zero column',['repair_domain','infimum_second_objective',1,0])]
 rejected=[]
 for name,path in cases:
  x=copy.deepcopy(v);change(x,path)
  try:check(x)
  except ValueError as e:rejected.append({'damage':name,'reason':str(e)})
  else:raise ValueError('semantic damage unexpectedly accepted: '+name)
 malformed=[]
 mutations=[('missing entire root',lambda x:x['all_nine_roots'].pop()),('missing affine zero column',lambda x:x['all_nine_half_normals'][0][0].pop()),('missing field zero coordinate',lambda x:x['whole_polynomial'][0][0][0].pop()),('missing jet order',lambda x:x['critical_small'].pop()),('extra field coordinate',lambda x:x['closing_parameters'][0].append('0')),('noncanonical rational',lambda x:x['closing_parameters'][0].__setitem__(0,'2/2')),('float coefficient',lambda x:x['closing_parameters'][0].__setitem__(0,1.0)),('wrong physical multiplicity',lambda x:x['counts'].__setitem__('critical_multiplicities',[2,6])),('wrong root label order',lambda x:x.__setitem__('basis_degrees',list(reversed(range(12))))),('unknown metadata field',lambda x:x.__setitem__('unexpected',True))]
 for name,mutate in mutations:
  x=copy.deepcopy(v);mutate(x)
  try:check(x)
  except (ValueError,TypeError,ZeroDivisionError)as e:malformed.append({'damage':name,'reason':str(e)})
  else:raise ValueError('malformed unexpectedly accepted: '+name)
 return{'status':'ALL_SEMANTIC_AND_SHAPE_DAMAGES_REJECTED_WITHOUT_EXPECTED_PINS','semantic_rejections':rejected,'malformed_rejections':malformed,'valid_positive_repairs':['1/2','1','2'],'expected_record_used':False}
if __name__=='__main__':print(json.dumps(run(json.loads(Path(sys.argv[1]).read_text())),sort_keys=True,separators=(',',':')))
