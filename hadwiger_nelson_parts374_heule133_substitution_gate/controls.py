#!/usr/bin/env python3
"""Small metric fixtures and malformed-certificate controls."""
import json
from verify import require, is_unit, validate_payload, check_word, HERE

def run():
    z=(0,)*16
    x=(288,)+(0,)*15
    y=(0,)*8+(288,)+(0,)*7
    half=(144,)+(0,)*8+(144,)+(0,)*6  # (1/2,sqrt(3)/2)
    near=(289,)+(0,)*15
    require(is_unit(z,x) and is_unit(z,y) and is_unit(z,half),'unit fixtures')
    require(not is_unit(z,z) and not is_unit(z,near) and not is_unit(x,y),'nonunit fixtures')
    points=[tuple(p) for p in json.loads((HERE/'points.json').read_text())]
    word=(HERE/'four_colour.txt').read_text().strip()
    trials=[lambda:validate_payload(points,word[:-1]),lambda:validate_payload(points,'4'+word[1:]),
            lambda:validate_payload([points[1]]+points[1:],word),lambda:check_word([(0,1)],'00')]
    rejected=0
    for trial in trials:
        try: trial()
        except ValueError: rejected+=1
    require(rejected==len(trials),'certificate controls')
    print(json.dumps({'all_checks':True,'exact_metric_fixtures':6,'rejected_bad_certificates':rejected},sort_keys=True))

if __name__=='__main__':run()
