"""Actual bad cut certificates and altered whole-cover semantics.

References are rebuilt from the physical row decoder before a candidate is
mutated. Operational exceptions cannot count as detected semantic damage.
"""
import argparse
import copy
import json
from pathlib import Path

import frame
import pair_stage
import row_domains


def expect(name,call,message,results):
    try:call()
    except ValueError as error:
        frame.require(str(error)==message,'Different/operational failure is not the intended semantic damage')
        results.append(dict(name=name,detected_by=message));return
    raise ValueError('Actual damaged cut was accepted: '+name)


def packet_scope(packet):
    frame.require(packet["case_index"]==frame.CASE_INDEX and packet["columns"]==list(frame.COLUMNS),
                  "Untrusted cut changes the complete selected case scope")


def run(cover,packet):
    packet_scope(packet)
    rows=row_domains.run(cover);domain={(r['point'],r['A_neighbors']):r['all_physical_B_words']
        for r in rows['whole_pattern_row_records']}
    expected=rows['remaining_graph_indices'];records=packet['completed_graph_records']
    frame.require([r['physical_graph_index'] for r in records]==expected,
                  'Control reference misses an actual surviving graph')
    guard=frame.Guard();valid=[]
    for r in records:
        k=r['physical_graph_index'];graph=rows['whole_representative_graphs'][k]
        initial=[domain[(i,graph[i])] for i in range(9)]
        frame.require(graph==r['whole_graph'] and initial==r['initial_domains'],
                      'Actual control reference graph/domain differs')
        checked=pair_stage.check(graph,initial,r['ordered_deletion_proposals'],guard)
        frame.require(checked==r['literal_check'],
                      'Actual complete control reference differs from literal replay')
        valid.append(k)
    results=[]
    bad=copy.deepcopy(cover);bad['selected_case_index']=-1
    expect('change_selected_cover_case',lambda:row_domains.run(bad),
           'Untrusted cover changes the complete shared type/matrix scope',results)
    bad=copy.deepcopy(cover);bad['ordered_A'][0],bad['ordered_A'][1]=bad['ordered_A'][1],bad['ordered_A'][0]
    expect('change_complete_physical_A_order',lambda:row_domains.run(bad),
           'Untrusted cover changes the complete shared type/matrix scope',results)
    bad=copy.deepcopy(cover);bad['whole_A_types'][0]^=1
    expect('change_whole_type_tag',lambda:row_domains.run(bad),
           'Untrusted cover changes the complete shared type/matrix scope',results)
    bad=copy.deepcopy(cover);bad['all_complete_case_columns'][sorted(frame.MATRICES).index(frame.CASE_INDEX)][1][0]^=1
    expect('change_whole_deficit_tag',lambda:row_domains.run(bad),
           'Untrusted cover changes the complete shared type/matrix scope',results)
    bad=copy.deepcopy(cover);bad['representative_neighbor_masks'][1]=bad['representative_neighbor_masks'][0]
    expect('replace_representative_neighbor_pair',lambda:row_domains.run(bad),
           'Untrusted cover changes the necessary neighbor-pair scope',results)
    bad=copy.deepcopy(cover);bad['representative_cover_graphs'].pop()
    expect('omit_one_complete_physical_graph',lambda:row_domains.run(bad),
           'Entire untrusted cover differs from fresh physical enumeration',results)
    bad=copy.deepcopy(cover);bad['representative_cover_graphs'][0][0]^=4
    expect('change_one_physical_adjacency',lambda:row_domains.run(bad),
           'Entire untrusted cover differs from fresh physical enumeration',results)
    bad=copy.deepcopy(cover);bad['all_complete_case_columns'].pop()
    expect('omit_one_whole_tagged_case',lambda:row_domains.run(bad),
           'Untrusted cover changes the complete shared type/matrix scope',results)
    bad=copy.deepcopy(packet);bad['case_index']=-1
    expect('change_selected_case_index',lambda:packet_scope(bad),
           'Untrusted cut changes the complete selected case scope',results)
    bad=copy.deepcopy(packet);bad['columns'][0]^=1
    expect('change_entire_selected_deficit_column',lambda:packet_scope(bad),
           'Untrusted cut changes the complete selected case scope',results)
    if not records:
        frame.require(not rows['remaining_graph_indices'] and rows['empty_row_graph_count']==1800*len(frame.ALLOWED_PAIRS),
                      'Row-only reference does not close the entire physical cover')
        return dict(agent='six-books-3',role='researcher',case_index=frame.CASE_INDEX,
            status='ACTUAL_ROW_ONLY_SEMANTIC_SCOPE_DAMAGES_CHECKED',
            all_complete_cut_records_checked=valid,actual_semantic_damages=results,
            actual_positive_nonempty_prefixes=0,row_only_exclusion=True,
            operational_failure_counted_as_semantic_damage=False,
            independent_person_review=False,work_units=guard.work)
    r=next(r for r in records if r['ordered_deletion_proposals'])
    graph=r['whole_graph'];initial=r['initial_domains'];i,word,j=r['ordered_deletion_proposals'][0]
    unsupported_message='Proposed cut target/witness is not in the current physical domains'
    expect('outside_target_point',lambda:pair_stage.check(graph,initial,[[9,word,j]],guard),
           unsupported_message,results)
    expect('outside_B_word',lambda:pair_stage.check(graph,initial,[[i,word|512,j]],guard),
           unsupported_message,results)
    expect('self_witness',lambda:pair_stage.check(graph,initial,[[i,word,i]],guard),
           unsupported_message,results)
    expect('repeat_already_deleted_word',lambda:pair_stage.check(graph,initial,[[i,word,j],[i,word,j]],guard),
           unsupported_message,results)
    positive=None
    for candidate in records:
        if not candidate['ordered_deletion_proposals']:continue
        a,w,_=candidate['ordered_deletion_proposals'][0]
        for b in range(9):
            if a==b:continue
            if any(pair_stage.literal_support(candidate['whole_graph'],a,b,w,z)
                   for z in candidate['initial_domains'][b]):
                positive=(candidate,a,w,b);break
        if positive:break
    frame.require(positive is not None,'No actual positive support for semantic witness control')
    cr,a,w,b=positive
    expect('delete_word_with_an_actual_literal_support',lambda:pair_stage.check(
        cr['whole_graph'],cr['initial_domains'],[[a,w,b]],guard),
        'Proposed deletion has a literal ordinary-spine support',results)
    nonempty=pair_stage.check(graph,initial,[],guard)
    frame.require(not nonempty['excluded'] and not nonempty['empty_rows'],
                  'An empty deletion prefix was turned into an exclusion')
    proper=None
    for candidate in records:
        cuts=candidate['ordered_deletion_proposals']
        if len(cuts)<2:continue
        prefix=pair_stage.check(candidate['whole_graph'],candidate['initial_domains'],cuts[:1],guard)
        if not prefix['excluded']:proper=prefix;break
    frame.require(proper is not None,'No proper positive nonempty prefix control')
    return dict(agent='six-books-3',role='researcher',
        status='ACTUAL_CUT_SEMANTIC_DAMAGES_AND_VALID_NONEMPTY_PREFIXES_CHECKED',case_index=frame.CASE_INDEX,row_only_exclusion=False,
        all_complete_cut_records_checked=valid,
        actual_semantic_damages=results,actual_positive_nonempty_prefixes=2,
        valid_prefix_domains=nonempty['final_domains'],valid_proper_prefix=proper,
        operational_failure_counted_as_semantic_damage=False,
        independent_person_review=False,work_units=guard.work)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--cover',required=True)
    parser.add_argument('--packet',required=True);parser.add_argument('--case',type=int,required=True);args=parser.parse_args();frame.select(args.case)
    print(json.dumps(run(json.loads(Path(args.cover).read_bytes()),
                         json.loads(Path(args.packet).read_bytes())),sort_keys=True,separators=(',',':')))
