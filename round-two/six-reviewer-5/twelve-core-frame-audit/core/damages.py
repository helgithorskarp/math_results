"""Independent damaged-certificate and interval-failure controls."""
from copy import deepcopy
import json,tempfile
from pathlib import Path
from partition import decode
from replay import predicate
from fractions import Fraction as F

P=Path(__file__).resolve().parent.parent
plan=json.loads((P/'author/PLAN.json').read_text());table=json.loads((P/'author/LITERALS.json').read_text())
rejected=[];accepted=[]
def trial(name,change,valid=False):
    a,b=deepcopy(plan),deepcopy(table);change(a,b)
    with tempfile.TemporaryDirectory(prefix='independent-g20-',dir=P) as directory:
        root=Path(directory);(root/'PLAN.json').write_text(json.dumps(a));(root/'LITERALS.json').write_text(json.dumps(b))
        try:leaves,coverage=decode(root)
        except (ValueError,ArithmeticError):
            if valid:raise ValueError('valid representation rejected: '+name)
            rejected.append(name)
        else:
            if not valid:raise ValueError('semantic damage accepted: '+name)
            accepted.append(name)
trial('drop branch',lambda a,b:a['trees'].pop())
trial('change branch sign',lambda a,b:a['trees'][1].__setitem__('epsilon',-1))
trial('g-half witness used for a whole branch',lambda a,b:a['trees'][0].__setitem__('tree','3'))
trial('truncate closed partition',lambda a,b:a['trees'][0].__setitem__('tree',a['trees'][0]['tree'][:-1]))
trial('unused partition suffix',lambda a,b:a['trees'][0].__setitem__('tree',a['trees'][0]['tree']+'0'))
trial('unrecognized witness',lambda a,b:a['trees'][0].__setitem__('tree','?'))
trial('wrong full interval',lambda a,b:a.__setitem__('box',['14/25','592/1000','-5/2','5/2']))
trial('restore removed point',lambda a,b:a['labels'].append(13))
trial('drop a required contact',lambda a,b:a['contacts'].pop())
trial('substitute removed-point comparison',lambda a,b:b['literals'].__setitem__(9,['pair',6,13]))
trial('wrong precision metadata',lambda a,b:a.__setitem__('lattice_bits',79))
trial('permute literal codes',lambda a,b:b.__setitem__('codes',b['codes'][::-1]))
trial('unknown W contact',lambda a,b:b['literals'].__setitem__(4,['W-pair',7,13]))
trial('replace all leaves by false chart tests',lambda a,b:a['trees'][0].__setitem__('tree','0'))
trial('depth guard',lambda a,b:a['trees'][0].__setitem__('tree','T'*23+'0'*24))
trial('harmless metadata',lambda a,b:a.__setitem__('annotation','same mathematics'),True)
trial('dictionary field order',lambda a,b:(a.__setitem__('format',a.pop('format')),b.__setitem__('format',b.pop('format'))),True)
branch=('bad',-1,-1)
box=(F(14,25),F(14,25),F(0),F(0))
if predicate(branch,box,['chart'])[0]:raise ValueError('false chart contradiction accepted')
if predicate(branch,box,['empty-necessary-intersection'])[0]:raise ValueError('false empty constraint accepted')
try:predicate(branch,box,['outside-target-g-half'])
except ValueError:rejected.append('arithmetic g-half target leak')
else:raise ValueError('target-specific arithmetic accepted')
print(json.dumps(dict(structural_damages=rejected,valid_representations=accepted,
 false_chart_rejected=True,false_empty_rejected=True),sort_keys=True,indent=2))
