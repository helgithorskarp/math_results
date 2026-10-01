"""Malformed logical-tuple controls, separate from mathematical corruptions."""
import copy
import json
from pathlib import Path
import compact


def check():
    data=json.loads((Path(__file__).absolute().parent/'certificates/exclusion.json').read_text())
    compact.decode(data);rejected=[]
    def reject(name,edit):
        bad=copy.deepcopy(data);edit(bad)
        try:compact.decode(bad)
        except ValueError:rejected.append(name);return
        raise ValueError('Malformed logical tuple accepted: '+name)
    reject('extra_header',lambda b:b.update(hidden_assumption=1))
    reject('boolean_row_tag',lambda b:b['steps'][0].__setitem__(0,False))
    reject('unknown_row_tag',lambda b:b['steps'][0].__setitem__(0,9))
    reject('empty_row',lambda b:b['steps'].__setitem__(0,[]))
    reject('row_wrong_length',lambda b:b['steps'][0].append(1))
    reject('boolean_row_coordinate',lambda b:b['steps'][0].__setitem__(1,True))
    reject('unknown_terminal_tag',lambda b:b.__setitem__('terminal',[9,0]))
    reject('boolean_terminal_tag',lambda b:b.__setitem__('terminal',[False,0]))
    reject('missing_exclusion_terminal',lambda b:b.__setitem__('terminal',None))
    f=next(i for i,r in enumerate(data['steps']) if r[0]==2)
    reject('missing_trial_terminal',lambda b:b['steps'][f].__setitem__(4,None))
    def nested(b):b['steps'][f][3].insert(0,[2,0,0,[],[1,0]])
    reject('nested_trial_tuple',nested)
    return {'logical_tuple_corruption_rejections':len(rejected),'rejected_cases':rejected}


if __name__=='__main__':print(json.dumps(check()),flush=True)
