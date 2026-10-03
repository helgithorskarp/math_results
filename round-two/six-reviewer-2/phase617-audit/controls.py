"""Damage controls against freshly rebuilt independent complete references."""
from pathlib import Path
from copy import deepcopy
import sys,json
from verify import row_check,sync_check,root_check,need

def damage(check,x,change,label):
    y=deepcopy(x);change(y)
    try:check(y)
    except(ValueError,IndexError,KeyError,TypeError):return label
    raise ValueError('semantic damage accepted: '+label)

def run(kind,path):
    x=json.loads(Path(path).read_text());check={'rows':row_check,'sync':sync_check,'roots':root_check}[kind];positive=check(x);bad=[]
    if kind=='rows':
        t=next(t for t,w in enumerate(x['whole_witnesses'][0])if w is not None)
        bad.append(damage(check,x,lambda y:y['whole_witnesses'][0].__setitem__(t,None),'omitted_nonprojection_table'))
        bad.append(damage(check,x,lambda y:y['phase_cutoffs'].__setitem__(1,631),'wrong_phase_endpoint'))
        bad.append(damage(check,x,lambda y:y['projection_bytes'].__setitem__(0,14),'wrong_projection_bit_order'))
    elif kind=='sync':
        bad.append(damage(check,x,lambda y:y['eliminating_progressions'].pop(),'missing_last_phase_cut'))
        bad.append(damage(check,x,lambda y:y['eliminating_progressions'][0].__setitem__('d',0),'zero_step'))
        bad.append(damage(check,x,lambda y:y['eliminating_progressions'][0].__setitem__('after',y['eliminating_progressions'][0]['after']+1),'wrong_full_history_count'))
    else:
        bad.append(damage(check,x,lambda y:y['root_positions'].__setitem__(3,y['root_positions'][0]),'linked_distinct_root_occurrences'))
        bad.append(damage(check,x,lambda y:y['records'][0]['implications'][0].__setitem__('value',1-y['records'][0]['implications'][0]['value']),'wrong_unit_color'))
        bad.append(damage(check,x,lambda y:y['records'][0]['leaves'].pop(),'omitted_actual_root_clause'))
        bad.append(damage(check,x,lambda y:y['records'][0].__setitem__('conflict',None),'dropped_physical_contradiction'))
        bad.append(damage(check,x,lambda y:y['records'][0]['conflict'].__setitem__('forbidden_color',1-y['records'][0]['conflict']['forbidden_color']),'wrong_conflict_polarity'))
    return dict(status='SEMANTIC_CONTROLS_COMPLETE',kind=kind,positive=positive,rejected=bad)
if __name__=='__main__':print(json.dumps(run(sys.argv[1],sys.argv[2]),sort_keys=True,separators=(',',':')))
