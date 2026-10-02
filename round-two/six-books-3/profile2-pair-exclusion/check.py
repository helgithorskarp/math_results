"""Independent literal 22-point pair-deletion verification.

Rebuilds all physical matrices and high stars. Imports no producer, its
inventory routine or bit-plane kernel. Producer status is never a verdict.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

import physical

LIMIT=2000000
RULE='HIGH_RED_PARITY_COLOR_SUBTOTAL_MAXIMA_V1'
require=physical.require


class Limit(Exception):
    pass


def verify(packet):
    started=time.monotonic()
    t=packet['template']
    require(type(t) is int and 0<=t<40 and packet['schema']=='PAIR_EMPTY_V1'
        and packet['rule']==RULE and packet['claim_template_excluded'] is False
        and packet['claim_whole_profile'] is False, 'Certificate scope/claims differ')
    counts,types,low_rows,budget,matrices,census,domains,raw=physical.build()
    require(packet['profile_counts']==counts and packet['types']==list(types)
        and packet['columns']==list(matrices[t]), 'Wrong physical scope/matrix')
    original=[set(domains.get((x,matrices[t][x]),[])) for x in range(18)]
    current=[set(r) for r in original]
    initial_sizes=[len(r) for r in original]
    require(packet['initial_sizes']==initial_sizes, 'Wrong original domains')
    work=0;checked=[];pending=None
    color_caps=[]
    initial_empty=[x for x,r in enumerate(current) if not r]

    def tick():
        nonlocal work
        if work>=LIMIT or time.monotonic()-started>=40:
            raise Limit
        work+=1

    if initial_empty:
        require(packet['removals']==[] and packet['pending'] is None
            and packet['current_sizes']==initial_sizes,
            'Initial-empty certificate has extraneous actions')
        status='PHYSICAL_INITIAL_DOMAIN_EMPTY_CHECKED'
    else:
        universe=frozenset(range(22));lows=frozenset(range(4))
        low_red=[frozenset(4+x for x in r) for r in low_rows]
        low_blue=[universe-low_red[i]-{i} for i in range(4)]
        red={};blue={};caps={}
        for x,row in enumerate(original):
            row_caps=set()
            for sx in row:
                r=frozenset(i for i in range(4) if types[x] & (1<<i)) | frozenset(
                    4+y for y in range(18) if sx & (1<<y))
                require(len(r)==10 and 4+x not in r, 'Bad physical high degree/self')
                b=universe-r-{4+x}
                sigma=[3-len(r&low_red[i]) if i in r else 6-len(b&low_blue[i])
                       for i in range(4)]
                require(all(s>=0 for s in sigma)
                    and sum(s*4**i for i,s in enumerate(sigma))==matrices[t][x],
                    'Literal mixed column differs')
                B=2+2*len(r&lows)-sum(sigma)
                parity=sum(sigma[i] for i in r&lows)%2
                require(B>=0,'Negative high deficit budget')
                # Scalar enumeration independently checks the color maxima.
                feasible=[v for v in range(B+1) if v%2==parity]
                rc=max(feasible,default=-1)
                bc=max((B-v for v in feasible),default=-1)
                red[x,sx]=r;blue[x,sx]=b;caps[x,sx]=(rc,bc)
                row_caps.add((B,parity,rc,bc))
            require(len(row_caps)==1,'Nonconstant endpoint color budget')
            B,p,rc,bc=next(iter(row_caps))
            color_caps.append(dict(vertex=x,budget=B,red_parity=p,
                                   red_max=rc,blue_max=bc))

        def pair(x,sx,y,sy):
            tick()
            rx,ry=red[x,sx],red[y,sy]
            edge=4+y in rx
            if edge!=(4+x in ry):
                return False
            if edge:
                common=rx&ry
                deficit=3-len(common)
                if deficit<0 or any(common&low_red[i] for i in common&lows):
                    return False
            else:
                deficit=6-len(blue[x,sx]&blue[y,sy])
                if deficit<0:
                    return False
            color=0 if edge else 1
            return deficit<=min(caps[x,sx][color],caps[y,sy][color])

        status='CHECKED_PAIR_PREFIX_NO_EXCLUSION'
        try:
            for index,cut in enumerate(packet['removals']):
                x,sx,y=cut['x'],cut['star'],cut['y']
                require(type(x) is int and type(y) is int and type(sx) is int
                    and 0<=x<18 and 0<=y<18 and x!=y and sx in current[x],
                    'Malformed/repeated physical removal')
                require(all(current), 'Action after first empty domain')
                pending=dict(index=index,x=x,star=sx,y=y)
                require(not any(pair(x,sx,y,sy) for sy in sorted(current[y])),
                        'Claimed unsupported star has a literal support')
                current[x].remove(sx)
                checked.append([x,sx,y])
                pending=None
                if not current[x]:
                    require(index+1==len(packet['removals']), 'Actions after final empty')
                    status='FULL_PAIR_DELETION_EXCLUSION_CHECKED'
                    break
        except Limit:
            status='OPERATIONAL_LIMIT_WITH_CHECKED_PREFIX_NO_EXCLUSION'
    empty=[x for x,row in enumerate(current) if not row]
    if pending is None:
        require(packet['current_sizes']==[len(r) for r in current], 'Final domains differ')
    record=dict(agent='six-books-3',role='researcher',template=t,counts=counts,
        types=list(types),columns=list(matrices[t]),mixed_row_budgets=budget,
        physical_census=census,raw_stars=raw,stored_stars=sum(len(r) for r in domains.values()),
        color_caps=color_caps,initial_sizes=initial_sizes,current_sizes=[len(r) for r in current],
        current_domains=[sorted(r) for r in current],checked_removals=checked,
        initial_empty=initial_empty,empty_targets=empty,checked_stars=len(checked),
        work_units=work,limit=LIMIT,pending=pending,status=status,
        claim_template_excluded=bool(empty) and pending is None,
        claim_whole_profile=False,seconds=time.monotonic()-started)
    return record


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    raw=a.packet.read_bytes();record=verify(json.loads(raw))
    record['packet_sha256']=hashlib.sha256(raw).hexdigest()
    a.out.write_text(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in record.items()
        if k not in ('checked_removals','current_domains','physical_census')},sort_keys=True))
