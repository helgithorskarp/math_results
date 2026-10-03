"""Postseal semantic controls; no damaged input is a theorem premise."""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import json
from exact import need
from joint_input import decode,load,unique
import reconstruct as R
import original as O
from bivar import P

def run():
 d=R.build(21,6);obj=load(Path(__file__).with_name('JOINT-INPUT.json'));vectors,weights=decode(d,obj);good=R.joint(d,vectors,weights);rejected=[]
 def reject(name,call):
  try:call()
  except (ValueError,KeyError):rejected.append(name);return
  raise ValueError('semantic damage accepted: '+name)
 def inputcheck(x):
  vv,ww=decode(d,x);result=R.joint(d,vv,ww)
  need(result['all_original_affine_dual_coefficients']==good['all_original_affine_dual_coefficients'],'entire retained literal certificate coefficients')
  return result
 bad=deepcopy(obj);bad['weights'][1][0]+=bad['weights'][0][0];bad['weights'][0][0]=0
 reject('zero-positive-dual-weight-with-total-preserved',lambda:inputcheck(bad))
 bad=deepcopy(obj);bad['planes'][0]['coordinates'][0][3]+=1
 reject('one-changed-original-integer-coordinate',lambda:inputcheck(bad))
 bad=deepcopy(obj);bad['planes'][0]['coordinates'][0]=list(bad['planes'][0]['coordinates'][1])
 reject('duplicate-physical-key-and-missing-orbit',lambda:inputcheck(bad))
 bad=deepcopy(obj);bad['planes'][0]['coordinates'][0][3]=True
 reject('boolean-is-not-integer-proof-input',lambda:inputcheck(bad))
 bad=deepcopy(obj);bad['planes'][1]['kind']='lower'
 reject('wrong-cap-lower-endpoint',lambda:inputcheck(bad))
 reject('duplicate-external-JSON-key',lambda:json.loads('{"q":21,"q":22}',object_pairs_hook=unique))
 rows=[[F(x) for x in row] for row in good['selected_three_rows']]
 def five(rows):
  total=[sum((w*row[j] for w,row in zip(weights,rows)),F(0)) for j in range(5)]
  need(total[2:]==[0,0,0] and total[0]<-F(1,256) and total[1]<0,'all five independent affine dual conditions')
 five(rows);bad=deepcopy(rows);bad[0][2]+=F(1,4096);bad[0][3]-=F(1,4096)
 need(bad[0][2]+bad[0][3]==rows[0][2]+rows[0][3],'equal-trade decoy really preserves combined coefficient')
 reject('equal-trade-decoy-with-unchanged-sum',lambda:five(bad))
 bad=deepcopy(rows);bad[0][4]+=F(1,4096);reject('uncancelled-independent-BC',lambda:five(bad))
 bad=deepcopy(rows)
 for row in bad:row[1]=F(1)
 reject('wrong-kappa-orientation',lambda:five(bad))
 q=P({(1,0):1});k=P({(0,1):1});den=3*q*(12*q**3+19*q*q+4*q-4)
 from bivar import derive
 u=derive();poly=P({(a,b):F(c) for a,b,c in u['P']});numerator=poly*den
 need(numerator.exact_divide(den)==poly,'undamaged entire quotient')
 reject('wrong-entire-rational-division-denominator',lambda:numerator.exact_divide(den+1))
 for name in ['shifted_slope','shifted_b0_not1_numerator']:
  damaged=deepcopy(u[name]);damaged[0][2]='-1'
  reject('negative-universal-coefficient-'+name,lambda:need(all(F(c)>0 for a,b,c in damaged),'EVERY shifted coefficient positive'))
 p=R.build(22,6);good=R.positive(p);cap=[[F(x) for x in row] for row in good['whole_forms']['cap']];w=p['weights'];m=len(w)
 stronger=[[cap[i][j]-F(w[i]*int(i==j),4096) for j in range(m)] for i in range(m)]
 reject('false-stronger-physical-cap-floor',lambda:O.psd(stronger))
 reject('false-full-cap-rank',lambda:need(O.psd(cap)['rank']==m-1,'complete cap rank'))
 return {'all14_semantic_controls_rejected':len(rejected)==14,'rejections':rejected,'failed_stronger_floor_is_not_H_infeasibility':True,'controls_are_not_extra_theorem_premises':True}

if __name__=='__main__':print(json.dumps(run(),sort_keys=True,separators=(',',':')))
