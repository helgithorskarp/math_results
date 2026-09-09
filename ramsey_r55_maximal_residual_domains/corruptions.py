"""Reject mutations of the complete global arithmetic certificate."""
from pathlib import Path
import argparse,copy,json
from verify_global import verify
def run(census,data,claim,out):
    out=Path(out);out.mkdir();source=json.loads(Path(claim).read_text());cases=[]
    for name in ('after_upper','ratio_to_previous_upper','h4059_removed_lower'):
        x=copy.deepcopy(source);x[name]['numerator']+=1;cases.append((name,x))
    x=copy.deepcopy(source);x['classes'][0]['contact_bound_sum']+=1;cases.append(('class_sum',x))
    x=copy.deepcopy(source);x['classes'][-1]=copy.deepcopy(x['classes'][0]);cases.append(('class_coverage',x))
    x=copy.deepcopy(source);x['strictly_improved_task_bounds']+=1;cases.append(('task_impact',x))
    for name,x in cases:
        path=out/(name+'.json');path.write_text(json.dumps(x,sort_keys=True)+'\n')
        try:verify(census,data,path)
        except (ValueError,KeyError):pass
        else:raise ValueError('corrupt global certificate accepted: '+name)
    return dict(status='GLOBAL_RESIDUAL_CORRUPTIONS_REJECTED',cases=len(cases))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('census');p.add_argument('data');p.add_argument('claim');p.add_argument('out');a=p.parse_args()
    print(json.dumps(run(a.census,a.data,a.claim,a.out),sort_keys=True))
