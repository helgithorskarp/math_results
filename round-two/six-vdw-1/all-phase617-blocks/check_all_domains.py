"""Gauss/Cartesian local row necessity and whole actual block transport.

Each row uses only root-free APs entirely in its OWN block, never a global cut.
"""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import struct


def need(ok,message):
    if not ok:
        raise ValueError(message)


def gauss_keys():
    signs={r:sum((j*r)%617>308 for j in range(1,309))%2 for r in range(1,617)}
    return [None if r in (0,1,4,16) else
            sum(w*signs[(r-t)%617] for w,t in zip((8,4,2,1),(0,1,4,16)))
            for r in range(617)]


def remove_monochromatic(excluded,support):
    missing=[k for k in range(16) if k not in support]
    assignments=[0]
    for k in missing:
        assignments += [x+2**k for x in assignments]
    mask=sum(2**k for k in support)
    for x in assignments:
        excluded[x]=1;excluded[x+mask]=1


def check(plan):
    scope={'schema':'NEW_ALL_SIX_PHASES_INDEPENDENT_PERIOD_BLOCK_F617_PLAN_V1',
           'q':617,'target_N':3704,'roots':[0,1,4,16],'physical_phase_period':6,
           'global_regular_phases':[],'block_varying_phases':[0,1,2,3,4,5],
           'regular_color_helpers':576,'original_color_helpers':602,'actual_original_color_tags':596,
           'all_selector_bits':216,'actual_root_bits':26,'proposed_full_CNF_variables':818,
           'all_original_roots_free':True,'periodic_roots':False,'palette_anchor':False,
           'antipodal_cut':False,'edit_budget':None,'extra_foreign_constraints':[],
           'old_global_coordinate_projection_cut_imported':False,
           'old_two_region_tail_projection_cut_imported':False,'old_closure_transferred':False,
           'whole_original_AP_model_generated':False,'whole_original_AP_model_audited':False,
           'native_attempts':0,'AP7_free_feasibility_proved':False,'family_excluded':False,
           'new3704_coloring':False,'AP_tag_stream_encoding':'<HH7H'}
    for name,value in scope.items():
        need(plan[name]==value,'whole independent block-row plan:'+name)
    keys=gauss_keys();supports=[set() for _ in range(6)]
    prefix_count=prefix_regular=0
    for step in range(6,103,6):
        for start in range(617-6*step):
            image=[keys[start+j*step] for j in range(7)];prefix_count+=1
            if None not in image:
                supports[start%6].add(tuple(sorted(set(image))));prefix_regular+=1
    domains=[];observed_masks=[]
    for relative in range(6):
        excluded=bytearray(65536)
        for support in supports[relative]:
            remove_monochromatic(excluded,set(support))
        observed={keys[n] for n in range(relative,617,6) if keys[n] is not None}
        missing=set(range(16))-observed
        need(missing==({10} if relative==2 else set()),'only actual unobserved local key')
        mask=sum(2**k for k in observed);observed_masks.append(mask)
        domains.append(sorted({table&mask for table in range(65536) if not excluded[table]}))
    need(list(map(len,domains))==[78,52,32,34,58,46],'all six exact local observable table domains')
    roots=[n for n in range(3704) if n%617 in (0,1,4,16)]
    root_tags={n:577+i for i,n in enumerate(roots)}
    tags=[root_tags[n] if n in root_tags else
          1+96*(n//617)+6*keys[n%617]+n%6 for n in range(3704)]
    absent=sorted(set(range(1,577))-set(tags))
    need(absent==plan['only_unobserved_color_helpers']==[63,158,253,354,449,544],
         'whole literal six-block geometry and only absent entries')
    cursor=603;rows=[];total=regular=0;stream=hashlib.sha256()
    for block in range(6):
        for phase in range(6):
            relative=(phase+block)%6;domain=domains[relative]
            width=(len(domain)-1).bit_length()
            color_tags=[96*block+6*k+phase+1 for k in range(16)]
            row={'block':block,'physical_phase':phase,'relative_first_period_phase':relative,
                 'truth_tables':domain,'binary_choice_bits':width,
                 'selector_variables_little_endian':list(range(cursor,cursor+width)),
                 'color_variables_by_key':color_tags,
                 'unobserved_color_variables_fixed_to_zero':[color_tags[10]] if relative==2 else [],
                 'zero_interval':[617*block,617*block+616]}
            rows.append(row);cursor+=width
            for step in range(6,103,6):
                for local in range(relative,617-6*step,6):
                    start=617*block+local
                    points=list(range(start,start+7*step,step));total+=1
                    need(all(n//617==block and n%6==phase for n in points),
                         'every transported row AP stays in its actual block and physical phase')
                    image=[keys[n%617] for n in points]
                    if None in image:
                        continue
                    need([tags[n] for n in points]==[color_tags[k] for k in image],
                         'entire literal root-free own-block color transport')
                    regular+=1;stream.update(struct.pack('<HH7H',start,step,*[tags[n] for n in points]))
    need(rows==plan['block_rows'] and cursor==819 and len(rows)==36,
         'whole exact36 independent rows/216 selector labels')
    count=math.prod(len(row['truth_tables']) for row in rows)*2**26
    need(count==plan['necessary_regular_and_root_choices'],'necessary choices before mixed APs')
    need(total==29886 and regular==29478,'entire own-block same-phase AP coverage')
    return rows,{'author':'six-vdw-1','role':'researcher',
                 'status':'EXACT_ALL_SIX_PHASES_LOCAL_BLOCK_ROW_NECESSITY_CHECKED',
                 'raw_truth_tables_examined':6*65536,'prefix_original_APs':prefix_count,
                 'prefix_root_free_APs':prefix_regular,'prefix_domain_sizes':list(map(len,domains)),
                 'actual_own_block_APs':total,'root_free_own_block_APs':regular,
                 'whole_root_free_literal_tag_stream_sha256':stream.hexdigest(),
                 'whole_actual_position_tag_stream_sha256':hashlib.sha256(struct.pack('<3704H',*tags)).hexdigest(),
                 'independent_rows':36,'selector_bits':216,'actual_root_bits':26,
                 'original_color_helpers':602,'actually_realized_tags':596,
                 'unused_regular_entries':absent,'necessary_choices_before_mixed_APs':count,
                 'global_or_old_projection_cuts_imported':False,'necessary_only':True,
                 'feasibility_claimed':False,'family_excluded':False,'native_solver_used':False}


if __name__=='__main__':
    h=Path(__file__).resolve().parent
    _,result=check(json.loads((h/'ALL_PHASE_BLOCKS_NEXT_PLAN.json').read_bytes()))
    print(json.dumps(result,sort_keys=True))
