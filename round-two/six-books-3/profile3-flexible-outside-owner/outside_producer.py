"""Full selected outside-star proposals against fixed current physical A rows.

No fixed A-column premise is assumed. No B-B supports, broad original
high-star pair producer, or old certificate is used.
"""
import argparse
import json
from pathlib import Path
import frame

OWNER=3
def select_owner(owner):
    global OWNER
    frame.require(type(owner) is int and 0<=owner<9,'Invalid physical outside owner')
    OWNER=owner
def compatible(graph,i,word,star):
    red=bool(word&(1<<OWNER))
    if red!=bool(star&(1<<frame.A[i])): return False
    high=sum(1<<frame.A[k] for k in range(9) if graph[i]&(1<<k))
    high|=sum(1<<frame.B[k] for k in range(9) if word&(1<<k))
    pages=(frame.TYPES[frame.A[i]]&frame.TYPES[frame.B[OWNER]]).bit_count()+(high&star).bit_count()
    return pages<=(3 if red else 6)

def run(frame_packet,pairs,owner=3,guard=None):
    select_owner(owner)
    guard=frame.Guard() if guard is None else guard
    frame.configuration();x=frame.B[OWNER]
    frame.require(frame.TYPES[x] in (3,4,5,6) and frame_packet['case_index']==pairs['case_index']==frame.CASE_INDEX
        and frame_packet['columns']==pairs['columns']==list(frame.COLUMNS)
        and not pairs['not_yet_attempted'],'Outside proposal changes complete case scope')
    initial=frame_packet['whole_original_indexed_domains'][x]
    sources=[r for r in pairs['completed_graph_records'] if not r['literal_check']['excluded']]
    frame.require([r['physical_graph_index'] for r in sources]==pairs['remaining_graph_indices'],
        'Outside proposal omits a stated current pair survivor')
    records=[]
    for source in sources:
        graph=source['whole_graph'];pools=source['literal_check']['final_domains'];cuts=[];kept=[]
        for star in initial:
            witness=None
            for i,row in enumerate(pools):
                supported=False
                for word in row:
                    guard.tick()
                    if compatible(graph,i,word,star): supported=True;break
                if not supported:witness=i;break
            if witness is None:kept.append(star)
            else:cuts.append([star,witness])
        records.append(dict(physical_graph_index=source['physical_graph_index'],whole_graph=graph,
            all_current_A_rows=pools,all_initial_owner_high_words=initial,
            ordered_owner_star_deletion_proposals=cuts,final_owner_high_words=kept))
    return dict(agent='six-books-3',role='researcher',case_index=frame.CASE_INDEX,
        status='COMPLETE_UNTRUSTED_OUTSIDE_OWNER_PROPOSALS_NO_VERDICT',
        columns=list(frame.COLUMNS),ordered_A=list(frame.A),ordered_B=list(frame.B),
        owner_B_point=OWNER,owner_physical_high=x,owner_full_tag=[frame.TYPES[x],frame.COLUMNS[x]],
        records=records,all_proposed_owner_domains_empty=all(not r['final_owner_high_words'] for r in records),
        fixed_A_column_assumed=False,B_B_star_supports_attempted=False,
        original_broad_pair_producer_used=False,case_excluded=False,whole_profile_excluded=False,
        ordinary_bridges_formalized=False,independent_person_review=False,work_units=guard.work)

def automatic(frame_packet,pairs):
    guard=frame.Guard();attempts=[]
    for owner in (3,0,1,2,4,5,6,7,8):
        packet=run(frame_packet,pairs,owner,guard)
        attempts.append(dict(owner_B_point=owner,owner_physical_high=frame.B[owner],
            owner_full_tag=[frame.TYPES[frame.B[owner]],frame.COLUMNS[frame.B[owner]]],
            all_domains_empty=packet['all_proposed_owner_domains_empty'],
            complete_remaining_counts=[[r['physical_graph_index'],len(r['final_owner_high_words'])]
                for r in packet['records']]))
        if packet['all_proposed_owner_domains_empty']:break
    packet['untrusted_owner_attempts']=attempts
    return packet

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True)
    p.add_argument('--frame',required=True);p.add_argument('--pairs',required=True);p.add_argument('--out',required=True)
    p.add_argument('--owner',type=int)
    a=p.parse_args();frame.select(a.case)
    f,pairs=json.loads(Path(a.frame).read_bytes()),json.loads(Path(a.pairs).read_bytes())
    result=automatic(f,pairs) if a.owner is None else run(f,pairs,a.owner)
    Path(a.out).write_bytes(frame.encode(result)+b'\n')
    print(frame.encode(dict(status=result['status'],graphs=len(result['records']),
        proposed_empty=result['all_proposed_owner_domains_empty'],work_units=result['work_units'])).decode())
