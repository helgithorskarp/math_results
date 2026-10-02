"""Semantic adverse controls of scope, coverage and exact deletion checks."""
import argparse
import copy
import json
from pathlib import Path

import verify

ROOT=Path(__file__).resolve().parent

def require(ok,message):
    if not ok:
        raise ValueError(message)

def controls():
    originals={i:json.loads((ROOT/f'certificate-{i}.json').read_text()) for i in (0,1)}
    cases=[]
    def damage(name,index,change):
        x=copy.deepcopy(originals[index]);change(x);cases.append((name,index,x))
    damage('missing-actual-template',0,lambda x:x['completed'].pop())
    damage('duplicate-actual-template',0,lambda x:x['completed'].__setitem__(1,copy.deepcopy(x['completed'][0])))
    damage('wrong-slack-column',0,lambda x:x['completed'][0]['columns'].__setitem__(0,x['completed'][0]['columns'][0]+1))
    def bool_column(x):
        row=x['completed'][0]['columns'];row[row.index(0)]=False
    damage('boolean-slack-coordinate',0,bool_column)
    first_arc=next(n for n,c in enumerate(originals[0]['completed']) if c['status']=='ARC_EMPTY')
    def wrong_empty(x):
        c=x['completed'][first_arc];c['status']='INITIAL_EMPTY';c['steps']=[];c['empty_target']=0
    damage('false-initial-empty',0,wrong_empty)
    damage('wrong-unsupported-count',0,lambda x:x['completed'][first_arc]['steps'][0].__setitem__('count',x['completed'][first_arc]['steps'][0]['count']-1))
    damage('forged-unsupported-hash',0,lambda x:x['completed'][first_arc]['steps'][0].__setitem__('sha256','0'*64))
    damage('support-against-itself',0,lambda x:x['completed'][first_arc]['steps'][0].__setitem__('other',x['completed'][first_arc]['steps'][0]['target']))
    damage('false-global-Ramsey-scope',0,lambda x:x.__setitem__('scope','All22-point hosts are excluded; Ramsey endpoint resolved'))
    damage('even-red-row-budget',1,lambda x:x['budget'].__setitem__(0,2))
    def drop_alpha3(x):
        n=next(n for n,c in enumerate(x['completed']) if sum((s&3) for s,t in zip(c['columns'],x['types']) if t&1)==3)
        x['completed'].pop(n)
    damage('omitted-three-red-units-branch',1,drop_alpha3)
    def drop_coincidence(x):
        n=next(n for n,c in enumerate(x['completed']) if any(sum(bool((s>>(2*i))&3) for i in range(4))>1 for s in c['columns']))
        x['completed'].pop(n)
    damage('omitted-point-coincidence',0,drop_coincidence)
    damage('boolean-schema',0,lambda x:x.__setitem__('schema',True))
    damage('wrong-global-type',0,lambda x:x['types'].__setitem__(0,1))
    damage('unfinished-limit-called-proof',0,lambda x:x.__setitem__('status','OPERATIONAL_LIMIT_NO_VERDICT'))
    damage('false-all-empty-verdict',0,lambda x:x.__setitem__('claim_all_empty',False))
    return cases

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args();a.work.mkdir(parents=True,exist_ok=True)
    rejected=[]
    for name,index,record in controls():
        path=a.work/(name+'.json');path.write_text(json.dumps(record)+'\n')
        try:verify.verify(index,certificate=path)
        except (ValueError,KeyError,IndexError):rejected.append(name)
        else:raise RuntimeError('Semantic damaged certificate accepted: '+name)
    require(len(rejected)==16,'unfinished adverse-control coverage')
    print(json.dumps({'semantic_damages_rejected':len(rejected),'names':rejected,'ordinary_and_code_bridges_unformalized':True},sort_keys=True,separators=(',',':')))
