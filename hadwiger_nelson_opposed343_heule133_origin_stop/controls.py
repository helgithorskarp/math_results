#!/usr/bin/env python3
"""Check valid evidence, then reject false extension-rule hypotheses/words."""
from pathlib import Path
import copy,json,verify
B=Path(__file__).resolve().parent;c=json.loads((B/'certificate.json').read_text())
verify.verify(c);p,e,*_=verify.construct()
checks=[]
x=copy.deepcopy(c);w=x['source_four_word'];x['source_four_word']=w[0]*2+w[2:]
checks.append(('improper source word',lambda:verify.verify(x)))
# Execute each closure before x is rebound.
rejected=[]
for name,run in checks:
    try:run()
    except ValueError:rejected.append(name)
    else:raise ValueError('false source accepted')
x=copy.deepcopy(c);w=x['whole_four_word'];x['whole_four_word']=w[0]*2+w[2:]
try:verify.verify(x)
except ValueError:rejected.append('improper whole word')
else:raise ValueError('false whole word accepted')
x=copy.deepcopy(c);w=x['complement_with_origin_four_word'];neighbor=next(b-342 for a,b in e if a==0 and b>=343)
x['complement_with_origin_four_word']=w[:neighbor]+'0'+w[neighbor+1:]
try:verify.check_extension_rule(x,e)
except ValueError:rejected.append('monochromatic complement-origin edge')
else:raise ValueError('false complement word accepted')
try:verify.check_extension_rule(c,e+[(1,343)])
except ValueError:rejected.append('unaccounted non-origin source contact')
else:raise ValueError('invalid universal-extension premise accepted')
# Every transposition is a permutation on all four symbols, with 0 mapped to c.
for color in range(4):
    w=verify.swap_zero('0123',color)
    verify.need(set(w)==set('0123') and w[0]==str(color),'colour permutation control')
print(json.dumps({'baseline_accepted':True,'corruptions_rejected':rejected,'all_colour_transpositions_checked':True},indent=2))
