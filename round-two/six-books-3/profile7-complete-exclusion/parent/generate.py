"""Untrusted bounded producer for an initial-empty or pair-deletion certificate."""
import argparse
import json
import time
from pathlib import Path

import model
from witness_kernel import LIMIT, Limit, bits, kernel, require

RULE = 'HIGH_RED_PARITY_COLOR_SUBTOTAL_MAXIMA_V1'


class Empty(Exception):
    pass


def produce(template):
    started=time.monotonic()
    require(type(template) is int and template>=0, 'Bad matrix number')
    inventory=model.build()
    require(template<len(inventory['matrices']), 'Matrix number outside complete inventory')
    types=inventory['types'];columns=inventory['matrices'][template]
    initial=[inventory['domains'].get((x,columns[x]),()) for x in range(18)]
    removals=[];pending=None;work=0;current=initial
    status='CANDIDATE_INITIAL_EMPTY_UNCHECKED'
    if all(initial):
        k=kernel(types,columns,initial,deadline=started+40)
        status='PAIR_FIXED_POINT_NO_HOST_VERDICT'
        try:
            while True:
                changed=False
                for x in sorted(range(18),key=lambda p:(k['active'][p].bit_count(),p)):
                    for j in list(bits(k['active'][x])):
                        sx=k['pool'][x][j]
                        for y in sorted((p for p in range(18) if p!=x),
                                        key=lambda p:(k['active'][p].bit_count(),p)):
                            pending=dict(x=x,star=sx,y=y)
                            if not k['supports'](x,sx,y):
                                removals.append(pending)
                                k['active'][x] &= ~(1<<j)
                                changed=True
                                if not k['active'][x]:
                                    raise Empty
                                break
                if not changed:
                    pending=None
                    break
        except Empty:
            status='CANDIDATE_PAIR_DOMAIN_EMPTY_UNCHECKED'
            pending=None
        except Limit:
            status='OPERATIONAL_LIMIT_WITH_COMPLETED_PROPOSAL_PREFIX'
        work=k['work']()
        current=[[sx for j,sx in enumerate(k['pool'][x]) if k['active'][x] & (1<<j)]
                 for x in range(18)]
    return dict(agent='six-books-3',role='researcher',schema='PAIR_EMPTY_V1',
        profile_counts=inventory['counts'],types=list(types),template=template,
        columns=list(columns),initial_sizes=[len(r) for r in initial],
        current_sizes=[len(r) for r in current],rule=RULE,removals=removals,
        pending=pending,status=status,work_units=work,limit=LIMIT,
        seconds=time.monotonic()-started,producer_only=True,
        claim_template_excluded=False,claim_whole_profile=False)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--template',type=int,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    record=produce(a.template)
    a.out.write_text(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ('removals','types','columns')},sort_keys=True))
