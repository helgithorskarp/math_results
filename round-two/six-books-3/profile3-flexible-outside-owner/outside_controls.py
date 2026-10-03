"""Actual full-owner-star certificate damages and valid nonempty prefixes."""
import argparse
import copy
import json
from pathlib import Path
import frame
import outside_check as checker

def run(cover,pairs,frame_packet,packet):
    guard=frame.Guard();checker.selected_scope(packet)
    rows,reference,initial=checker.fresh_reference(cover,pairs,frame_packet,guard)
    frame.require(bool(reference) and [r['physical_graph_index'] for r in reference]==
        [r['physical_graph_index'] for r in packet['records']],
        'Outside control reference does not cover every nonempty fresh survivor')
    checked=[checker.check_one(r,initial,p,guard) for r,p in zip(reference,packet['records'])]
    frame.require(all(r['excluded'] for r in checked),'Actual outside reference does not exclude every survivor')
    results=[]
    def expect(name,call,message):
        try:call()
        except ValueError as error:
            frame.require(str(error)==message,'Different/operational failure is not intended outside damage')
            results.append(dict(name=name,detected_by=message));return
        raise ValueError('Actual damaged outside certificate was accepted')
    scope='Untrusted outside certificate changes the entire physical case/owner scope'
    for name,key,value in [('case','case_index',-1),('column','columns',[packet['columns'][0]^1]+packet['columns'][1:]),
                           ('owner','owner_physical_high',(frame.B[checker.OWNER]+1)%18),
                           ('owner_tag','owner_full_tag',[frame.TYPES[frame.B[checker.OWNER]],-1])]:
        bad=copy.deepcopy(packet);bad[key]=value
        expect(name,lambda bad=bad:checker.selected_scope(bad),scope)
    bad=copy.deepcopy(packet);bad['records'].pop()
    expect('omit_complete_survivor',lambda:checker.run(cover,pairs,frame_packet,bad),
        'Untrusted outside certificate misses an entire fresh survivor')
    ref,p=reference[0],packet['records'][0]
    bad=copy.deepcopy(p);bad['whole_graph'][0]^=4
    expect('alter_whole_J',lambda:checker.check_one(ref,initial,bad,guard),
        'Untrusted outside certificate changes the complete current graph/A rows')
    bad=copy.deepcopy(p);bad['all_current_A_rows'][0].pop()
    expect('omit_current_A_word',lambda:checker.check_one(ref,initial,bad,guard),
        'Untrusted outside certificate changes the complete current graph/A rows')
    bad=copy.deepcopy(p);bad['all_initial_owner_high_words'].pop()
    expect('omit_initial_owner_star',lambda:checker.check_one(ref,initial,bad,guard),
        'Untrusted outside certificate omits or changes a literal initial owner star')
    expect('include_physical_owner',lambda:checker.physical_owner_star(initial[0]|(1<<frame.B[checker.OWNER])),
        'Literal outside star changes degree10 or includes its physical owner')
    target='Outside deletion target/witness is not in the current physical domains'
    bad=copy.deepcopy(p);bad['ordered_owner_star_deletion_proposals'][0][1]=9
    expect('outside_actual_A_witness',lambda:checker.check_one(ref,initial,bad,guard),target)
    bad=copy.deepcopy(p);bad['ordered_owner_star_deletion_proposals'][0][0]|=1<<18
    expect('outside_actual_high_star_word',lambda:checker.check_one(ref,initial,bad,guard),target)
    bad=copy.deepcopy(p);first=copy.deepcopy(bad['ordered_owner_star_deletion_proposals'][0])
    bad['ordered_owner_star_deletion_proposals']=[first,copy.deepcopy(first)]
    expect('repeat_deleted_owner_word',lambda:checker.check_one(ref,initial,bad,guard),target)
    positive=None
    for r,record in zip(reference,packet['records']):
        for star in initial:
            for i,row in enumerate(r['pools']):
                if any(checker.literal_support(r['graph'],r['pools'],i,star,w) for w in row):
                    positive=(r,record,star,i);break
            if positive:break
        if positive:break
    frame.require(positive is not None,'No actual reciprocal supported outside damage control')
    pr,pp,star,i=positive;bad=copy.deepcopy(pp)
    bad['ordered_owner_star_deletion_proposals']=[[star,i]]
    expect('delete_actual_supported_owner_word',lambda:checker.check_one(pr,initial,bad,guard),
        'Outside deletion has an actual reciprocal ordinary-spine support')
    bad=copy.deepcopy(p);bad['final_owner_high_words']=initial[:1]
    expect('wrong_complete_final_owner_domain',lambda:checker.check_one(ref,initial,bad,guard),
        'Untrusted outside final domain differs from entire literal replay')
    empty=copy.deepcopy(p);empty['ordered_owner_star_deletion_proposals']=[];empty['final_owner_high_words']=list(initial)
    nonempty=checker.check_one(ref,initial,empty,guard)
    frame.require(not nonempty['excluded'],'An actual empty prefix became an outside exclusion')
    proper=copy.deepcopy(p);proper['ordered_owner_star_deletion_proposals']=proper['ordered_owner_star_deletion_proposals'][:1]
    removed=proper['ordered_owner_star_deletion_proposals'][0][0]
    proper['final_owner_high_words']=[w for w in initial if w!=removed]
    prefix=checker.check_one(ref,initial,proper,guard)
    frame.require(not prefix['excluded'],'An actual proper prefix became an outside exclusion')
    return dict(agent='six-books-3',role='researcher',case_index=frame.CASE_INDEX,
        status='ACTUAL_FULL_OUTSIDE_DAMAGES_AND_VALID_NONEMPTY_PREFIXES_CHECKED',
        all_complete_survivors_checked=[r['physical_graph_index'] for r in checked],
        actual_semantic_damages=results,actual_valid_nonempty_prefixes=2,
        valid_empty_prefix=nonempty,valid_proper_prefix=prefix,work_units=guard.work,
        operational_failure_counted_as_semantic_damage=False,independent_person_review=False)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--cover',required=True)
    p.add_argument('--pairs',required=True);p.add_argument('--frame',required=True);p.add_argument('--packet',required=True)
    p.add_argument('--owner',type=int,required=True)
    a=p.parse_args();frame.select(a.case);checker.select_owner(a.owner)
    print(frame.encode(run(json.loads(Path(a.cover).read_bytes()),json.loads(Path(a.pairs).read_bytes()),
        json.loads(Path(a.frame).read_bytes()),json.loads(Path(a.packet).read_bytes()))).decode())
