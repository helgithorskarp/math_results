"""Six external mutations of the whole record; same comparator as audit.py."""
from pathlib import Path
import json,copy
from audit import compare_expected

def main():
 good=Path(__file__).with_name('EXPECTED.json').read_bytes();record=json.loads(good);mutants=[]
 a=copy.deepcopy(record);a['orbits'].pop();mutants.append(('omit full star class',a))
 a=copy.deepcopy(record);a['orbits'][0]['directions'][0]['sigma']='0';mutants.append(('wrong actual defect',a))
 a=copy.deepcopy(record);a['literal'][0]['whole_sha256']='0'*64;mutants.append(('wrong original matrix',a))
 a=copy.deepcopy(record);a['universal']['improved_floor']='1/2';mutants.append(('unproved stronger floor',a))
 a=copy.deepcopy(record);a['thresholds'][0]['k']+=1;mutants.append(('first failing successor',a))
 a=copy.deepcopy(record);a['permutation']['permutation']=list(range(7));mutants.append(('wrong physical relabelling',a))
 compare_expected(good,good)
 for label,a in mutants:
  try:compare_expected((json.dumps(a,sort_keys=True,indent=2)+'\n').encode(),good)
  except ValueError:continue
  raise ValueError('accepted external fixture:'+label)
 print(json.dumps({'rejected':[label for label,a in mutants],'whole_byte_comparator':True}))
if __name__=='__main__':main()
