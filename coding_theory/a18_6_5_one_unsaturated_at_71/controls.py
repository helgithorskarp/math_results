"""Positive, negative, malformed and visibly incomplete controls."""
from copy import deepcopy
from itertools import combinations
import json
import resource
import time

from common import Guard, HERE, Incomplete, WORK, require
import producer
import verify


def rejected(call):
    try:call()
    except ValueError:return
    raise ValueError('invalid control was accepted')


def run():
    expected=json.loads((HERE/'expected.json').read_text())
    fixture=tuple(tuple(q) for q in expected['isolated_canonical'])
    verify.inspect_fixture(fixture,14)
    corruptions=[]
    duplicate=list(fixture);duplicate[1]=duplicate[0];corruptions.append(tuple(duplicate))
    short=list(fixture);short[0]=short[0][:-1];corruptions.append(tuple(short))
    outside=list(fixture);outside[0]=tuple(sorted(outside[0][:-1]+(17,)));corruptions.append(tuple(outside))
    changed=list(fixture);changed[0]=(0,1,3,15);corruptions.append(tuple(changed))
    for bad in corruptions:rejected(lambda bad=bad:verify.inspect_fixture(bad,14))
    rejected(lambda:verify.inspect_fixture(fixture,0))
    for nodes,seconds in ((True,10),(-1,10),(200001,10),(1,-1),(1,11),(1,float('nan'))):
        rejected(lambda nodes=nodes,seconds=seconds:Guard(nodes,seconds))
    eligible=tuple(combinations(range(4),2));columns=((0,1,2,3),);quota=(1,)*4+(0,)*11
    positive=[]
    incomplete=0
    for solver in (producer.all_covers,verify.literal_covers):
        covers,nodes=solver(eligible,columns,quota,eligible)
        require(covers==[(0,)],'positive singleton cover rejected');positive.append(nodes)
        try:solver(eligible,columns,quota,eligible,nodes=0)
        except Incomplete:incomplete+=1
        else:raise ValueError('zero-node cap did not report incomplete')
        rejected(lambda solver=solver:solver(eligible,columns+columns,quota,eligible))
        rejected(lambda solver=solver:solver(eligible,columns,(-1,)+quota[1:],eligible))
        rejected(lambda solver=solver:solver(eligible,columns,quota,((0,4),)))
    model=verify.literal_model('isolated')
    case=next(r for r in verify.inputs(model) if not r['direct'])
    negative=[]
    for solver in (producer.all_covers,verify.literal_covers):
        covers,nodes=solver(model['eligible'],case['columns'],case['quota'],case['mandatory'])
        require(not covers,'known finite negative case accepted');negative.append(nodes)
    return {'status':'COMPLETE','fixture_corruptions_rejected':5,'invalid_guards_rejected':6,
            'malformed_solver_inputs_rejected':6,'positive_covers_checked':2,'negative_cases_checked':2,
            'visible_incomplete_cases':incomplete,'positive_nodes':positive,'negative_nodes':negative}


def main():
    started=time.monotonic();result=run()
    result.update(seconds=time.monotonic()-started,maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    WORK.mkdir(parents=True,exist_ok=True);(WORK/'controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
