"""Reconstruct entire coverage and literal complete selected-owner stars."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import frame
import pair_stage
import row_domains

OWNER=3
def select_owner(owner):
    global OWNER
    frame.require(type(owner) is int and 0<=owner<9,'Invalid physical outside owner')
    OWNER=owner
def selected_scope(packet):
    x=frame.B[OWNER]
    frame.require(packet['case_index']==frame.CASE_INDEX and packet['columns']==list(frame.COLUMNS)
        and packet['ordered_A']==list(frame.A) and packet['ordered_B']==list(frame.B)
        and packet['owner_B_point']==OWNER and packet['owner_physical_high']==x
        and packet['owner_full_tag']==[frame.TYPES[x],frame.COLUMNS[x]],
        'Untrusted outside certificate changes the entire physical case/owner scope')

def physical_owner_star(word):
    x=frame.B[OWNER]
    frame.require(type(word) is int and 0<=word<(1<<18) and not word&(1<<x)
        and word.bit_count()==10-frame.TYPES[x].bit_count(),
        'Literal outside star changes degree10 or includes its physical owner')
    red=frozenset({i for i in range(4) if frame.TYPES[x]&(1<<i)}|
        {4+y for y in range(18) if word&(1<<y)})
    return red,frozenset(set(range(22))-red-{4+x})

def literal_initial(guard):
    x=frame.B[OWNER];initial=[];raw=0
    low=[{4+y for y,t in enumerate(frame.TYPES) if t&(1<<j)} for j in range(4)]
    for chosen in itertools.combinations([y for y in range(18) if y!=x],10-frame.TYPES[x].bit_count()):
        guard.tick();raw+=1;word=sum(1<<y for y in chosen);red,blue=physical_owner_star(word);actual=[]
        for j in range(4):
            if j in red:cap,pages=3,len(low[j]&red)
            else:cap,pages=6,len((set(range(22))-low[j]-{j})&blue)
            actual.append(cap-pages)
        if actual==[frame.sigma(x,j) for j in range(4)]:initial.append(word)
    frame.require(frame.TYPES[x] in (3,4,5,6) and raw==24310,
        'Complete literal selected-owner subset coverage differs')
    return sorted(initial)

def fresh_reference(cover,pairs,frame_packet,guard):
    frame.configuration()
    frame.require(pairs['case_index']==frame_packet['case_index']==frame.CASE_INDEX
        and pairs['columns']==frame_packet['columns']==list(frame.COLUMNS)
        and frame_packet['ordered_A']==list(frame.A) and frame_packet['ordered_B']==list(frame.B)
        and frame_packet['high_types']==list(frame.TYPES) and not pairs['not_yet_attempted'],
        'Untrusted outside input changes the entire frame/pair scope')
    initial=literal_initial(guard)
    frame.require(frame_packet['whole_original_indexed_domains'][frame.B[OWNER]]==initial,
        'Untrusted owner initial domain differs from every literal subset')
    rows=row_domains.run(cover);guard.work+=rows['work_units'];guard.tick()
    patterns={(r['point'],r['A_neighbors']):r['all_physical_B_words'] for r in rows['whole_pattern_row_records']}
    frame.require([r['physical_graph_index'] for r in pairs['completed_graph_records']]==rows['remaining_graph_indices'],
        'Untrusted outside pair prefix does not cover every fresh physical graph')
    reference=[]
    for source in pairs['completed_graph_records']:
        k=source['physical_graph_index'];graph=rows['whole_representative_graphs'][k]
        initial_A=[patterns[(i,graph[i])] for i in range(9)]
        frame.require(source['whole_graph']==graph and source['initial_domains']==initial_A,
            'Untrusted outside prefix changes the complete graph/initial A rows')
        checked=pair_stage.check(graph,initial_A,source['ordered_deletion_proposals'],guard)
        frame.require(checked==source['literal_check'],'Untrusted outside prefix differs from literal replay')
        if not checked['excluded']:reference.append(dict(physical_graph_index=k,graph=graph,pools=checked['final_domains']))
    frame.require(pairs['row_stage_empty_graphs']==rows['empty_row_graph_count']
        and pairs['row_stage_remaining']==rows['remaining_graph_indices']
        and pairs['row_stage_mathematics_sha256']==hashlib.sha256(frame.encode(rows)).hexdigest()
        and pairs['remaining_graph_indices']==[r['physical_graph_index'] for r in reference],
        'Untrusted outside prefix changes entire row/pair/survivor coverage')
    return rows,reference,initial

def literal_support(graph,pools,i,star,word):
    br,bb=physical_owner_star(star);ar,ab=pair_stage.physical_star(graph,i,word)
    red=4+frame.B[OWNER] in ar
    if red!=(4+frame.A[i] in br):return False
    return (len(ar&br) if red else len(ab&bb))<=(3 if red else 6)

def check_one(reference,initial,packet,guard):
    graph,pools=reference['graph'],reference['pools']
    frame.require(packet['physical_graph_index']==reference['physical_graph_index']
        and packet['whole_graph']==graph and packet['all_current_A_rows']==pools,
        'Untrusted outside certificate changes the complete current graph/A rows')
    frame.require(packet['all_initial_owner_high_words']==initial,
        'Untrusted outside certificate omits or changes a literal initial owner star')
    current=set(initial);checked=[]
    for star,i in packet['ordered_owner_star_deletion_proposals']:
        frame.require(type(i) is int and 0<=i<9 and star in current,
            'Outside deletion target/witness is not in the current physical domains')
        for word in pools[i]:
            guard.tick()
            frame.require(not literal_support(graph,pools,i,star,word),
                'Outside deletion has an actual reciprocal ordinary-spine support')
        current.remove(star);checked.append([star,i])
    frame.require(sorted(current)==packet['final_owner_high_words'],
        'Untrusted outside final domain differs from entire literal replay')
    return dict(physical_graph_index=reference['physical_graph_index'],whole_graph=graph,
        all_current_A_rows=pools,all_literal_initial_owner_words=initial,
        all_literal_checked_deletions=checked,final_owner_high_words=sorted(current),excluded=not current)

def run(cover,pairs,frame_packet,packet):
    guard=frame.Guard();selected_scope(packet)
    rows,reference,initial=fresh_reference(cover,pairs,frame_packet,guard)
    frame.require([r['physical_graph_index'] for r in packet['records']]==[r['physical_graph_index'] for r in reference],
        'Untrusted outside certificate misses an entire fresh survivor')
    records=[check_one(r,initial,p,guard) for r,p in zip(reference,packet['records'])]
    return dict(agent='six-books-3',role='researcher',case_index=frame.CASE_INDEX,
        status='COMPLETE_LITERAL_FULL_OUTSIDE_OWNER_STAR_AUDIT',columns=list(frame.COLUMNS),
        complete_physical_cover_size=len(rows['whole_representative_graphs']),row_empty=rows['empty_row_graph_count'],
        owner_B_point=OWNER,owner_physical_high=frame.B[OWNER],
        owner_full_tag=[frame.TYPES[frame.B[OWNER]],frame.COLUMNS[frame.B[OWNER]]],
        pair_empty=len(rows['remaining_graph_indices'])-len(reference),owner_raw_subsets=24310,
        entire_owner_initial_domain=initial,entire_checked_outside_records=records,
        literal_outside_deletions=sum(len(r['all_literal_checked_deletions']) for r in records),
        remaining_graph_indices=[r['physical_graph_index'] for r in records if not r['excluded']],
        case_excluded=all(r['excluded'] for r in records),whole_profile_excluded=False,
        fixed_A_column_assumed=False,B_B_star_supports_attempted=False,original_broad_pair_producer_used=False,
        ordinary_bridges_formalized=False,independent_person_review=False,work_units=guard.work,
        work_guard=2000000,internal_seconds_guard=40)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--cover',required=True)
    p.add_argument('--pairs',required=True);p.add_argument('--frame',required=True);p.add_argument('--packet',required=True)
    p.add_argument('--out',required=True);p.add_argument('--owner',type=int,required=True)
    a=p.parse_args();frame.select(a.case);select_owner(a.owner)
    result=run(json.loads(Path(a.cover).read_bytes()),json.loads(Path(a.pairs).read_bytes()),
        json.loads(Path(a.frame).read_bytes()),json.loads(Path(a.packet).read_bytes()))
    Path(a.out).write_bytes(frame.encode(result)+b'\n')
    print(frame.encode(dict(status=result['status'],graphs=len(result['entire_checked_outside_records']),
        literal_outside_deletions=result['literal_outside_deletions'],case_excluded=result['case_excluded'],
        work_units=result['work_units'])).decode())
