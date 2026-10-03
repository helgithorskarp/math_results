"""Exact guarded cut matrix enumeration with necessary literal pair compatibility.

All cut matrices satisfying these conditions are generated. A cut matrix is not
a whole Ramsey graph; the complementary nine-point graph remains to be supplied.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time

AT=(3,5,5,7,9,9,11,13,3)
BT=(2,4,6,6,8,10,10,12,12)
COLS=(5,4,5,5,4,5,5,5,5)


class Limit(Exception):
    pass


def require(ok,message):
    if not ok:
        raise ValueError(message)


def run(path,out):
    begun=time.monotonic()
    work=0

    def tick():
        nonlocal work
        if work>=2000000 or time.monotonic()-begun>=40:
            raise Limit()
        work+=1

    raw=Path(path).read_bytes()
    packet=json.loads(raw)
    require(packet['pair_cuts_verified'] and len(packet['cases'])==1,
            'Need the literally verified entire unique necessary fixed-point domain')
    case=packet['cases'][0]
    graph=case['graph']
    domains=case['current_domains']
    require(case['graph_index']==25642 and all(domains),'Wrong residual domain')
    support={}
    b_masks=[sum(1<<j for j,t in enumerate(BT) if t & (1<<low)) for low in range(4)]

    def compatible(i,a,j,b):
        red=bool(graph[i] & (1<<j))
        common_types=AT[i]&AT[j]
        overlap=a&b
        if (graph[i]&graph[j]).bit_count()+common_types.bit_count()+overlap.bit_count() > (3 if red else 6):
            return False
        return not red or all(not (overlap&b_masks[low])
                              for low in range(4) if common_types & (1<<low))

    solutions=[]
    counts=dict(nodes=0,branches=0,empty_support=0,column_overflow=0,column_interval=0,
                full_column_mismatch=0)
    complete=True
    try:
        for i in range(9):
            for j in range(i+1,9):
                for ci,a in enumerate(domains[i]):
                    mask=0
                    for cj,b in enumerate(domains[j]):
                        tick()
                        if compatible(i,a,j,b):
                            mask|=1<<cj
                            support[j,cj,i]=support.get((j,cj,i),0)|(1<<ci)
                    support[i,ci,j]=mask
                for cj in range(len(domains[j])):
                    support.setdefault((j,cj,i),0)

        def choices(mask):
            while mask:
                bit=mask&-mask
                yield bit.bit_length()-1
                mask^=bit

        def visit(pools,selected,columns):
            tick();counts['nodes']+=1
            unassigned=[i for i,value in enumerate(selected) if value is None]
            if not unassigned:
                if tuple(columns)==COLS:
                    solutions.append(tuple(domains[i][selected[i]] for i in range(9)))
                else:
                    counts['full_column_mismatch']+=1
                return
            i=min(unassigned,key=lambda x:(pools[x].bit_count(),x))
            for ci in choices(pools[i]):
                tick();counts['branches']+=1
                word=domains[i][ci]
                next_columns=[columns[j]+((word>>j)&1) for j in range(9)]
                if any(next_columns[j]>COLS[j] for j in range(9)):
                    counts['column_overflow']+=1
                    continue
                next_pools=list(pools)
                others=[j for j in unassigned if j!=i]
                for j in others:
                    next_pools[j]&=support[i,ci,j]
                if any(not next_pools[j] for j in others):
                    counts['empty_support']+=1
                    continue
                valid=True
                for col in range(9):
                    minimum=maximum=next_columns[col]
                    for j in others:
                        bits=[(domains[j][cj]>>col)&1 for cj in choices(next_pools[j])]
                        minimum+=min(bits);maximum+=max(bits)
                    if not minimum<=COLS[col]<=maximum:
                        valid=False;break
                if not valid:
                    counts['column_interval']+=1
                    continue
                next_selected=list(selected);next_selected[i]=ci
                visit(next_pools,next_selected,next_columns)

        visit([(1<<len(domain))-1 for domain in domains],[None]*9,[0]*9)
    except Limit:
        complete=False
    require(len(solutions)==len(set(solutions)),'Repeated physical cut matrix')
    encoded=json.dumps(sorted(solutions),separators=(',',':')).encode()
    result=dict(agent='six-books-3',role='researcher',
        status='COMPLETE_NECESSARY_CUT_MATRIX_ENUMERATION' if complete else 'OPERATIONAL_LIMIT_CUT_PREFIX_NO_EXCLUSION',
        original_fixed_packet_sha256=hashlib.sha256(raw).hexdigest(),graph_index=25642,
        graph=graph,initial_domain_sizes=list(map(len,domains)),column_degrees=list(COLS),
        complete=complete,statistics=counts,physical_cut_matrices=len(solutions),
        matrices=[list(row) for row in sorted(solutions)],
        whole_matrix_bytes=len(encoded),whole_matrix_sha256=hashlib.sha256(encoded).hexdigest(),
        work_units=work,work_guard=2000000,internal_seconds_guard=40,
        B_high_completion_checked=False,host_realization_claimed=False,
        whole_profile_excluded=False,producer_is_untrusted=True)
    Path(out).write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    return {k:v for k,v in result.items() if k not in ('matrices','graph')}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--fixed',required=True)
    parser.add_argument('--out',required=True)
    args=parser.parse_args()
    print(json.dumps(run(args.fixed,args.out),sort_keys=True,separators=(',',':')))
