"""Six damaged data/hypothesis controls, each rejected by both arithmetic checks."""
from pathlib import Path
import argparse,copy,json
import check,audit

def damaged(source):
 cases=[]
 x=copy.deepcopy(source);x['edges'].remove([7,12]);cases.append(('missing_retained_cross_contact',x))
 x=copy.deepcopy(source);x['root_bracket']=['0.59','0.591'];cases.append(('false_root_bracket',x))
 x=copy.deepcopy(source);x['functions']['rho']['n']=[-v for v in x['functions']['rho']['n']];cases.append(('negative_radical',x))
 x=copy.deepcopy(source);x['functions']['packing_threshold_factor']['n'][0]+=1;cases.append(('false_threshold_factor',x))
 x=copy.deepcopy(source);x['functions']['1_-1_6_8_a']['n']=[-v for v in x['functions']['1_-1_6_8_a']['n']];cases.append(('wrong_threshold_branch_sign',x))
 x=copy.deepcopy(source);x['noncontact_upper']='1/100';cases.append(('false_noncontact_gap',x))
 return cases

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--prerequisite-root',type=Path,default=check.ROOT)
 args=parser.parse_args()
 source=json.loads((check.HERE/'certificate.json').read_text())
 derived=check.derive(args.prerequisite_root)
 rejected=[]
 for name,c in damaged(source):
  for label,fn in (('primary',lambda:check.verify(c,args.prerequisite_root,derived)),
                   ('audit',lambda:audit.audit(c))):
   try:fn()
   except ValueError:pass
   else:raise ValueError(label+' accepted damaged control '+name)
  rejected.append(name)
 print(json.dumps({'status':'ALL_DAMAGED_CONTROLS_REJECTED','both_checkers':True,'controls':rejected},sort_keys=True))
