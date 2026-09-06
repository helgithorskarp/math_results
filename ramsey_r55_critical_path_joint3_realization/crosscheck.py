"""Entry-level checker agreement and deliberately invalid graph controls."""
import argparse
import copy
import itertools as it
import json
from pathlib import Path
import tempfile
import bitcheck
import verify


def need(ok,msg):
    if not ok:raise ValueError(msg)


def run(path):
    literal,left=verify.audit(path,True);bit,right=bitcheck.audit(path,True)
    need(left==right,'all clique masks and all root-union rows')
    for key in set(literal)&set(bit)-{'status'}:
        need(json.dumps(literal[key],sort_keys=True)==json.dumps(bit[key],sort_keys=True),'field '+key)
    doc=json.loads(path.read_text());mutations=[]
    def change(label,fn):
        d=copy.deepcopy(doc);fn(d);mutations.append((label,d))
    change('missing order',lambda d:d.pop('n'))
    change('wrong order',lambda d:d.__setitem__('n',42))
    change('boolean order',lambda d:d.__setitem__('n',True))
    change('duplicate edge',lambda d:d['red_edges'].append(d['red_edges'][0]))
    change('missing edge',lambda d:d['red_edges'].pop())
    change('reversed pair',lambda d:d['red_edges'][0].reverse())
    change('endpoint out of range',lambda d:d['red_edges'][0].__setitem__(1,43))
    change('float endpoint',lambda d:d['red_edges'][0].__setitem__(0,0.0))
    change('unsorted edges',lambda d:d['red_edges'].reverse())
    change('unexpected field',lambda d:d.__setitem__('claimed_ramsey',True))
    change('non-list edges',lambda d:d.__setitem__('red_edges',{}))
    # Deliberately corrupt the graph; this is a verifier test, not local search.
    # A two-switch preserves degrees, the entire fixed core, and all footprints.
    # Find one that introduces a forbidden <=3-outside K5, using the fast checker.
    R={tuple(e) for e in doc['red_edges']};switch=None;trials=0
    with tempfile.TemporaryDirectory(prefix='r55-joint3-controls-') as tmp:
        trial_path=Path(tmp)/'trial.json'
        for four in it.combinations(range(11,43),4):
            a,b,c,d=four;matchings=[{(a,b),(c,d)},{(a,c),(b,d)},{(a,d),(b,c)}]
            for remove,add in it.permutations(matchings,2):
                if not remove<=R or add&R:continue
                trials+=1;mutant={'n':43,'red_edges':sorted(R-remove|add)}
                trial_path.write_text(json.dumps(mutant))
                try:bitcheck.audit(trial_path)
                except ValueError as exc:
                    if str(exc)=='joint three-outside layer':
                        switch={'removed':sorted(remove),'added':sorted(add)}
                        mutations.append(('degree-preserving layer violation',mutant));break
                if trials>=1000:break
            if switch is not None or trials>=1000:break
        need(switch is not None,'bounded malformed-layer fixture')
        rejected=[]
        for label,mutant in mutations:
            trial_path.write_text(json.dumps(mutant))
            messages=[]
            for checker in (verify.audit,bitcheck.audit):
                try:checker(trial_path)
                except ValueError as exc:messages.append(str(exc))
                else:raise ValueError('invalid graph accepted: '+label)
            rejected.append({'label':label,'literal_message':messages[0],'bit_message':messages[1]})
    return {'status':'VERIFIED_ENTRY_LEVEL_AGREEMENT','graph_sha256':literal['graph_sha256'],
            'clique_masks_compared':sum(map(len,left['k5_masks'].values())),
            'root_union_rows_compared':len(left['root_rows']),
            'clique_set_sha256':literal['clique_set_sha256'],'root_rows_sha256':literal['root_rows_sha256'],
            'bad_graphs_rejected_by_both':len(rejected),'controls':rejected,
            'layer_violation_switch':switch,'switch_trials':trials}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--graph',type=Path,default=Path(__file__).with_name('GRAPH.json'))
    p.add_argument('--report',type=Path,required=True);a=p.parse_args();need(not a.report.exists(),'fresh report')
    r=run(a.graph);a.report.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r))
