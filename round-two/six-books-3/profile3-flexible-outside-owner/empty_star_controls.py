"""Literal validation of complete empty high-star witnesses and damaged packets."""
import argparse
import copy
import json
from pathlib import Path
import frame

def run(packet):
    guard=frame.Guard();frame.configuration()
    literal,raw=frame.literal_original_domains(guard)
    empty=[x for x,row in enumerate(literal) if not row]
    frame.require(bool(empty),'An empty-star exclusion needs an actual empty original domain')
    def check(candidate):
        frame.require(candidate['case_index']==frame.CASE_INDEX
            and candidate['columns']==list(frame.COLUMNS)
            and candidate['high_types']==list(frame.TYPES)
            and candidate['ordered_A']==list(frame.A)
            and candidate['ordered_B']==list(frame.B),
            'Untrusted empty-star frame changes the complete physical case scope')
        frame.require(candidate['whole_original_indexed_domains']==literal,
            'Untrusted empty-star frame differs from every literal original domain')
        frame.require(candidate['empty_original_high_domains']==empty
            and candidate['original_raw_stars']==raw and candidate['case_excluded'] is True,
            'Untrusted empty-star frame changes the entire checked witness coverage')
    check(packet);results=[]
    def damage(name,candidate,message):
        try: check(candidate)
        except ValueError as error:
            frame.require(str(error)==message,'An unrelated failure is not intended empty-star damage')
            results.append(dict(name=name,detected_by=message));return
        raise ValueError('Actual damaged empty-star frame was accepted')
    scope='Untrusted empty-star frame changes the complete physical case scope'
    for name,key in [('selected_case','case_index'),('entire_column','columns'),
                     ('whole_type','high_types'),('physical_A','ordered_A'),('physical_B','ordered_B')]:
        bad=copy.deepcopy(packet)
        if key=='case_index':bad[key]=-1
        elif key in ('ordered_A','ordered_B'):bad[key][0],bad[key][1]=bad[key][1],bad[key][0]
        else:bad[key][0]^=1
        damage(name,bad,scope)
    bad=copy.deepcopy(packet);bad['whole_original_indexed_domains'].pop()
    damage('omit_entire_original_point',bad,
           'Untrusted empty-star frame differs from every literal original domain')
    x=empty[0]
    rank=10-frame.TYPES[x].bit_count()
    fake=sum(1<<y for y in [y for y in range(18) if y!=x][:rank])
    bad=copy.deepcopy(packet);bad['whole_original_indexed_domains'][x]=[fake]
    damage('insert_actual_invalid_nonempty_star',bad,
           'Untrusted empty-star frame differs from every literal original domain')
    bad=copy.deepcopy(packet);bad['empty_original_high_domains']=[]
    damage('omit_all_literal_empty_witnesses',bad,
           'Untrusted empty-star frame changes the entire checked witness coverage')
    # The inserted rank-correct star violates an actual prescribed mixed spine.
    red=frame.TYPES[x]|(fake<<4);allpoints=(1<<22)-1
    blue=allpoints^(1<<(4+x))^red
    actual=[]
    for i in range(4):
        low=sum(1<<(4+y) for y,t in enumerate(frame.TYPES) if t&(1<<i))
        isred=bool(frame.TYPES[x]&(1<<i))
        pages=((low&red) if isred else ((allpoints^(1<<i)^low)&blue)).bit_count()
        actual.append((3 if isred else 6)-pages)
    frame.require(actual!=[frame.sigma(x,i) for i in range(4)],
                  'The supposed invalid inserted star has all actual prescribed deficits')
    return dict(agent='six-books-3',role='researcher',case_index=frame.CASE_INDEX,
        status='COMPLETE_LITERAL_EMPTY_STAR_EXCLUSION_AND_ACTUAL_DAMAGES',
        every_original_domain_literal_reconstructed=True,raw_subsets=raw,
        entire_empty_original_high_domains=empty,actual_semantic_damages=results,
        inserted_rank_correct_star_actual_deficits=actual,case_excluded=True,
        whole_profile_excluded=False,ordinary_bridges_formalized=False,
        independent_person_review=False,work_units=guard.work,
        operational_failure_counted_as_semantic_damage=False)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True)
    p.add_argument('--packet',required=True);a=p.parse_args();frame.select(a.case)
    print(frame.encode(run(json.loads(Path(a.packet).read_bytes()))).decode())
