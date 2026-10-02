"""Meaningful budget counterchecks plus whole external-fixture corruption controls."""
import copy,hashlib,json
from audit import build,canonical,broken_budgets,need

def check_external(candidate):
 need(type(candidate) is dict and candidate==build(),'whole external fixture mismatch')

def main():
 r=build();check_external(r)
 changes=[('polar_mean_coefficient',lambda x:x['polar']['mean']['certificate']['coefficients'].__setitem__(2,'0')),
 ('radial_face_2',lambda x:x['radial'][1]['interval_certificate']['coefficients'].__setitem__(0,'0')),
 ('radial_face_8_omitted',lambda x:x['radial'].pop()),
 ('normalization_zero_variance',lambda x:x['normalization'].__setitem__('zero_variance_division',True)),
 ('origin_phase_constant',lambda x:x['scalars'].__setitem__('K1','300')),
 ('energy_budget',lambda x:x['scalars'].__setitem__('energy_clean_budget','80000000')),
 ('abstract_control_relabelled',lambda x:x['controls'][0].__setitem__('abstract_only',False)),
 ('actual_lowF_relabelled',lambda x:x['controls'][2].__setitem__('low_F',True))]
 out={}
 for label,change in changes:
  c=copy.deepcopy(r);change(c)
  try:check_external(c)
  except ValueError:out[label]='rejected'
  else:raise ValueError('corruption accepted '+label)
 for label,c in [('wrong_type',[]),('missing_all_fields',{})]:
  try:check_external(c)
  except ValueError:out[label]='rejected'
  else:raise ValueError('malformed record accepted')
 print(json.dumps({'whole_record_sha256':hashlib.sha256(canonical(r)).hexdigest(),
  'mathematical_budget_controls':broken_budgets(),'external_record_controls':out},sort_keys=True))
if __name__=='__main__':main()
