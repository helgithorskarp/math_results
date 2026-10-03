"""Different fixed-order literal22-point cut search from ALL original row words.

No producer, forward-support table, or final four row deletions are imported.
All512 physical words per point are reconstructed from four actual low spines.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time

TYPES=(2,3,3,4,5,5,6,6,7,8,9,9,10,10,11,12,12,13)
SIGMA=(0,1,4,1,0,16,0,0,0,1,0,64,0,0,0,0,0,0)
A=(2,4,5,8,10,11,14,17,1)
B=(0,3,6,7,9,12,13,15,16)
ORDER=(8,0,1,2,3,4,5,6,7)


class Limit(Exception):
    pass


def require(ok,message):
    if not ok:
        raise ValueError(message)


def run(fixed, proposed):
    begun=time.monotonic();work=0

    def tick():
        nonlocal work
        if work>=2000000 or time.monotonic()-begun>=40:
            raise Limit()
        work+=1

    fixed_raw=Path(fixed).read_bytes()
    packet=json.loads(fixed_raw)
    require(packet['pair_cuts_verified'] and len(packet['cases'])==1,'Wrong residual graph input')
    case=packet['cases'][0]
    graph=case['graph']
    require(case['graph_index']==25642
            and graph==[146,97,336,176,13,266,134,73,36], 'Different unique physical graph')
    require([row.bit_count() for row in graph]==[3]*8+[2]
            and all(not graph[i]&(1<<i) for i in range(9))
            and all(bool(graph[i]&(1<<j))==bool(graph[j]&(1<<i))
                    for i in range(9) for j in range(9)), 'Malformed actual simple neighborhood')
    full=(1<<22)-1
    low_rows=[sum(1<<(h+4) for h,t in enumerate(TYPES) if t&(1<<low))
              for low in range(4)]
    low_blue=[full^(low_rows[low]|(1<<low)) for low in range(4)]
    b_points=sum(1<<(h+4) for h in B)
    columns=tuple(5-((SIGMA[h]>>0)&3) for h in B)
    require(columns==(5,4,5,5,4,5,5,5,5),'Wrong literal root0 column ranks')
    domains=[]
    row_cache={}
    complete=True
    solutions=[]
    stats=dict(nodes=0,branches=0,literal_pair_rejections=0,column_rejections=0,
               completed_assignments=0)
    try:
        for i,h in enumerate(A):
            actual_a=sum(1<<(A[j]+4) for j in range(9) if graph[i]&(1<<j))
            domain=[]
            for word in range(512):
                tick()
                red=TYPES[h]|actual_a|sum(1<<(B[j]+4) for j in range(9) if word&(1<<j))
                require(not red&(1<<(h+4)),'Red diagonal in actual high row')
                if red.bit_count()!=10:
                    continue
                blue=full^(red|(1<<(h+4)))
                valid=True
                for low in range(4):
                    sigma=(SIGMA[h]>>(2*low))&3
                    if red&(1<<low):
                        pages=(red&low_rows[low]).bit_count();target=3-sigma
                    else:
                        pages=(blue&low_blue[low]).bit_count();target=6-sigma
                    if pages!=target:
                        valid=False;break
                if valid:
                    domain.append(word);row_cache[i,word]=red,blue
            domains.append(domain)
        require(domains==case['original_domains'],'Entire independent original domains differ')

        def allowed(i,a,j,b):
            tick()
            ir,ib=row_cache[i,a];jr,jb=row_cache[j,b]
            red=bool(ir&(1<<(A[j]+4)))
            require(red==bool(jr&(1<<(A[i]+4))),'Reciprocal literal edge differs')
            if red:
                common=ir&jr
                if common.bit_count()>3:
                    return False
                for low in range(4):
                    if common&(1<<low) and common&b_points&low_rows[low]:
                        return False
            elif (ib&jb).bit_count()>6:
                return False
            return True

        # The checker uses a fixed, different order and does not propagate
        # pair support to future row pools. Future ranges use original rows.
        remaining_min=[];remaining_max=[]
        for level in range(10):
            remaining_min.append([sum(min((word>>col)&1 for word in domains[i])
                for i in ORDER[level:]) for col in range(9)])
            remaining_max.append([sum(max((word>>col)&1 for word in domains[i])
                for i in ORDER[level:]) for col in range(9)])

        def visit(level,selected,margins):
            tick();stats['nodes']+=1
            if level==9:
                require(tuple(margins)==columns,'Unpruned wrong complete column ranks')
                solutions.append(tuple(selected[i] for i in range(9)))
                stats['completed_assignments']+=1
                return
            i=ORDER[level]
            for word in domains[i]:
                tick();stats['branches']+=1
                if any(not allowed(i,word,j,selected[j]) for j in ORDER[:level]):
                    stats['literal_pair_rejections']+=1;continue
                next_margins=[margins[col]+((word>>col)&1) for col in range(9)]
                if any(not next_margins[col]+remaining_min[level+1][col]
                    <=columns[col]<=next_margins[col]+remaining_max[level+1][col]
                    for col in range(9)):
                    stats['column_rejections']+=1;continue
                selected[i]=word
                visit(level+1,selected,next_margins)
                del selected[i]

        visit(0,{},[0]*9)
    except Limit:
        complete=False
    encoded=json.dumps(sorted(solutions),separators=(',',':')).encode()
    require(len(solutions)==len(set(solutions)),'Repeated actual complete cut')
    if complete:
        producer=json.loads(Path(proposed).read_bytes())
        require(producer['complete'] and producer['original_fixed_packet_sha256']==hashlib.sha256(fixed_raw).hexdigest()
                and producer['matrices']==[list(matrix) for matrix in sorted(solutions)]
                and producer['whole_matrix_sha256']==hashlib.sha256(encoded).hexdigest(),
                'Whole independent cut domain differs from producer')
    return dict(agent='six-books-3',role='researcher',
        status='COMPLETE_LITERAL_ORIGINAL_CUT_DOMAIN_CHECK' if complete else 'OPERATIONAL_LIMIT_NO_EXCLUSION',
        complete=complete,graph_index=25642,all_original_word_domains_reconstructed=complete,
        original_domain_sizes=list(map(len,domains)),four_low_spines_checked=True,
        variable_order=list(ORDER),imports_producer_or_forward_support=False,
        final_four_pair_deletions_required=False,statistics=stats,
        physical_cut_matrices=len(solutions),whole_matrix_bytes=len(encoded),
        whole_matrix_sha256=hashlib.sha256(encoded).hexdigest(),
        proposed_whole_domain_compared=complete,work_units=work,
        work_guard=2000000,internal_seconds_guard=40,
        full_host_realization_claimed=False,global_Ramsey_bound_claimed=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--fixed',required=True)
    parser.add_argument('--proposed',required=True)
    args=parser.parse_args()
    print(json.dumps(run(args.fixed,args.proposed),sort_keys=True,separators=(',',':')))
