"""Reconstruct20 finite necessary domains and check their ordinary bridge."""
from collections import Counter
import copy
import hashlib
import itertools
import json
from pathlib import Path
import sys
import time
import inventory
from row_types import need,unit_graphs
from selector import check,capacity,orientation

ROOT=Path(__file__).resolve().parent


def encode(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()


def compute():
    ts=inventory.types();cases=[];bridges=[]
    for E in (0,1,2):
        for a,b,c in ((1,1,5),(1,2,4),(1,3,3),(2,2,3)):
            for t in ((0,1) if E<2 else (1,)):
                case=inventory.run_case(ts,a,b,c,t,E);cases.append(case)
                for i,s in enumerate(case['survivors']):
                    bridges.append(dict(pair=(a,b,c),E=E,t=t,inventory_index=i,
                                        result=check(case,s)))
    need(len(cases)==20 and len(bridges)==50,'finite scope/count mismatch')
    totals=Counter(s['E'] for s in bridges)
    need(totals=={0:6,1:43,2:1},'surviving inventory totals')
    full=dict(row_types=ts,cases=cases,bridges=bridges)
    compact=dict(status='COMPLETE NECESSARY DOMAINS AND AUTHOR ORDINARY BRIDGE CHECKS',
                 row_types=len(ts),cases=len(cases),bridges=len(bridges),
                 surviving_by_E=dict(totals),
                 row_types_sha256=hashlib.sha256(encode(ts)).hexdigest(),
                 full_mathematical_record_sha256=hashlib.sha256(encode(full)).hexdigest(),
                 domains=[dict(pair_multiplicities=c['pair_multiplicities'],E=c['E'],t=c['t'],
                               states=c['states'],counts=c['counts'],
                               survivors_sha256=hashlib.sha256(encode(c['survivors'])).hexdigest()) for c in cases])
    return compact,full


def rejected(f):
    try:f()
    except RuntimeError:return True
    raise RuntimeError('Semantic damage was accepted')


def controls(full):
    labels=[]
    data=json.loads((ROOT/'unit_fixtures.json').read_text())
    for name,change in (
        ('omitted unit fixture',lambda x:x['fixtures'].pop()),
        ('duplicate quadruple',lambda x:x['fixtures'][0]['quadruples'].__setitem__(1,x['fixtures'][0]['quadruples'][0])),
        ('out-of-domain point',lambda x:x['fixtures'][0]['quadruples'][0].__setitem__(0,17)),
        ('duplicate point',lambda x:x['fixtures'][0]['quadruples'][0].__setitem__(1,x['fixtures'][0]['quadruples'][0][0])),
        ('wrong original fixture index',lambda x:x['fixtures'][0].__setitem__('original_fixture_index',10)),
    ):
        damaged=copy.deepcopy(data);change(damaged);rejected(lambda:unit_graphs(damaged));labels.append(name)
    rejected(lambda:capacity(6,3,1));labels.append('weakened uv tail coverage')
    rejected(lambda:capacity(6,4,2));labels.append('two outside edges at tight coverage')
    rejected(lambda:orientation([0,1,0],[2,0,0],1,2,0));labels.append('mixed second row without reversal')
    need(orientation([2,0,0],[0,1,0],0,2,1),'positive reverse-center control')
    case=next(c for c in full['cases'] if c['E']==1 and c['survivors'])
    for name,key,value in (('unsupported SS excess','X',1),('uncovered SS deficit triangle','tau',1)):
        damaged=copy.deepcopy(case['survivors'][0]);damaged[key]=value
        rejected(lambda:check(case,damaged));labels.append(name)
    tcase=next(c for c in full['cases'] if c['E']==2 and c['survivors'])
    damaged=copy.deepcopy(tcase['survivors'][0])
    damaged['exceptional_rows'][0]=list(damaged['exceptional_rows'][0])
    damaged['exceptional_rows'][0][4]=0
    rejected(lambda:check(tcase,damaged));labels.append('removed final q1 witness')
    return dict(rejected=labels,total=len(labels),positive_reversed_orientation=True,
                all_eight_positive_unit_fixtures=True)


def main():
    started=time.monotonic();compact,full=compute();checkdata=controls(full)
    expected=json.loads((ROOT/'EXPECTED.json').read_text())
    need(encode(compact)==encode(expected),'frozen compact exact readout differs')
    print(json.dumps(dict(actual_agent='six-code-1',role='researcher',
                         record=compact,controls=checkdata,
                         seconds=time.monotonic()-started),indent=2))


if __name__=='__main__':main()
