"""Falsify an exact strip/orthogonal-diamond characterization FIRST.

Bounded full literal output domains are fixed in this source. If those
pass, enumerate the complete small strip-chain domain and its exact
word-multiplicity partition. No full grid literal census, fitted entropy
constant or full-target solution is claimed. Same-author proof controls.
"""

import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import resource
import time

from adaptive_full_guard_probe_v1 import encode, require
from definition_checker import occurrences


def inverse(p):
    return tuple(p.index(label)+1 for label in range(1,len(p)+1))


def comparison_word(p):
    return tuple(int(p.index(j)<p.index(j+1)) for j in range(1,len(p)))


@lru_cache(None)
def strip(old,guard,old_first):
    otags=tuple(('old',j-1) for j in old)
    gtags=tuple(('guard',j-1) for j in guard)
    tags=otags+gtags if old_first else gtags+otags
    word=tuple(2*j+1 if kind=='old' else 2*j+2 for kind,j in tags)
    return word,tags,tuple(occurrences(word))


def predicted_strips(rows,guards,tags,axis):
    r=len(rows)
    positions={tag:pos for pos,tag in enumerate(tags)}
    result=set()
    for h in range(r-1):
        for i,old_first in ((h,True),(h+1,False)):
            word,local,boxes=strip(rows[i],guards[h],old_first)
            for q in boxes:
                selected=tuple((kind,i if kind=='old' else h,j) for kind,j in (local[pos] for pos in q))
                if axis=='column':selected=tuple((kind,j,i) for kind,i,j in selected)
                result.add(tuple(sorted(positions[tag] for tag in selected)))
    return result


def predicted_diamonds(rows,columns,guards,gcolumns,tags):
    r=len(rows)
    positions={tag:pos for pos,tag in enumerate(tags)}
    result={}
    for i in range(1,r-1):
        for j in range(r-1):
            if rows[i].index(j+1)<rows[i].index(j+2) and gcolumns[j][i-1]<gcolumns[j][i]:
                selected=(('guard',i-1,j),('old',i,j),('old',i,j+1),('guard',i,j))
                q=tuple(sorted(positions[tag] for tag in selected))
                result[q]=('old_row_guard_column',i,j)
    for j in range(1,r-1):
        for i in range(r-1):
            if columns[j][i]<columns[j][i+1] and guards[i].index(j)<guards[i].index(j+1):
                selected=(('old',i,j),('guard',i,j-1),('guard',i,j),('old',i+1,j))
                q=tuple(sorted(positions[tag] for tag in selected))
                result[q]=('old_column_guard_row',i,j)
    return result


class Mismatch(Exception):
    def __init__(self,record):self.record=record


def full_check(rows,columns,guards,gcolumns,metadata):
    r=len(rows)
    require(all(not tuple(occurrences(p)) for p in rows+columns+guards+gcolumns),'Component outside avoiding domain')
    word,tags=encode(rows,columns,guards,gcolumns)
    actual=tuple(occurrences(word))
    horizontal=predicted_strips(rows,guards,tags,'row')
    vertical=predicted_strips(tuple(map(inverse,columns)),tuple(map(inverse,gcolumns)),tags,'column')
    diamonds=predicted_diamonds(rows,columns,guards,gcolumns,tags)
    predicted=horizontal|vertical|set(diamonds)
    record={'r':r,'old_rows':rows,'old_columns':columns,'guard_rows':guards,'guard_columns':gcolumns,
            'metadata':metadata,'word':word,'complete_occurrences':actual,
            'horizontal_strip_occurrences':sorted(horizontal),'vertical_strip_occurrences':sorted(vertical),
            'orthogonal_diamond_occurrences':sorted((q,label) for q,label in diamonds.items())}
    if predicted!=set(actual):
        record.update({'tags':tags,'missing_predicted_occurrences':sorted(set(actual)-predicted),
                       'extra_predicted_occurrences':sorted(predicted-set(actual))})
        raise Mismatch(record)
    return record


def avoiding_inputs():
    return {r:tuple(p for p in itertools.permutations(range(1,r+1)) if not tuple(occurrences(p))) for r in range(1,6)}


def strip_tables(avoiders):
    rows=[]
    for r in range(2,6):
        stream=hashlib.sha256()
        safe=Counter();types=Counter();representatives={}
        for old,guard in itertools.product(avoiders[r],avoiders[r-1]):
            for old_first in (False,True):
                word,tags,actual=strip(old,guard,old_first)
                safe[old_first]+=not actual
                for q in actual:
                    count=sum(tags[pos][0]=='guard' for pos in q)
                    require(1<=count<=3,'Avoiding components yield a monochrome strip box')
                    types[str(old_first)+':'+str(count)]+=1
                    if (old_first,count) not in representatives:
                        representatives[old_first,count]={'old':old,'guard':guard,'old_first':old_first,
                                                         'word':word,'complete_occurrences':actual,'first_selected_guard_count':count}
                stream.update((json.dumps([old,guard,old_first,word,actual],separators=(',',':'))+'\n').encode())
        rows.append({'r':r,'complete_component_pair_domain':len(avoiders[r])*len(avoiders[r-1]),
                     'old_then_guard_safe_pairs':safe[True],'guard_then_old_safe_pairs':safe[False],
                     'all_mixed_occurrence_type_counts':dict(sorted(types.items())),
                     'all_first_type_representatives':[representatives[key] for key in sorted(representatives)],
                     'entire_pair_stream_sha256':stream.hexdigest()})
    return rows


def directed_r3(avoiders):
    r=3;identity=(1,2,3);reverse=(3,2,1)
    cores=set()
    for base in (identity,reverse):
        for index in range(6):
            for p in avoiders[3]:
                core=[base]*6;core[index]=p;cores.add(tuple(core))
    for p,q in itertools.product(avoiders[3],repeat=2):cores.add((p,)*3+(q,)*3)
    records=[]
    for core in sorted(cores):
        for auxiliary in itertools.product(avoiders[2],repeat=4):
            records.append(full_check(core[:3],core[3:],auxiliary[:2],auxiliary[2:],{'control':'all16guards/fixed_old_core'}))
    return {'complete_specified_old_core_domain':len(cores),'all16_guard_profiles_per_core':True,'full_grid_cases':len(records),'records':records}


def transposition(r,index):
    p=list(range(1,r+1));p[index],p[index+1]=p[index+1],p[index];return tuple(p)


def diamond_truth_controls():
    r=4;identity=tuple(range(1,r+1));gid=tuple(range(1,r))
    records=[]
    for axis in ('old_row_guard_column','old_column_guard_row'):
        for internal in range(1,r-1):
            for gap in range(r-1):
                for first,second in itertools.product((0,1),repeat=2):
                    rows=[identity]*r;columns=[identity]*r;guards=[gid]*(r-1);gcolumns=[gid]*(r-1)
                    if axis=='old_row_guard_column':
                        rows[internal]=identity if first else transposition(r,gap)
                        gcolumns[gap]=gid if second else transposition(r-1,internal-1)
                    else:
                        columns[internal]=identity if first else transposition(r,gap)
                        guards[gap]=gid if second else transposition(r-1,internal-1)
                    record=full_check(tuple(rows),tuple(columns),tuple(guards),tuple(gcolumns),
                                      {'control':'complete_diamond_2bit_states','axis':axis,'internal':internal,'gap':gap,
                                       'two_bits':(first,second)})
                    if axis=='old_row_guard_column':
                        target=('old_row_guard_column',internal,gap)
                    else:target=('old_column_guard_row',gap,internal)
                    present=any(label==target for q,label in record['orthogonal_diamond_occurrences'])
                    require(present==bool(first and second),'Diamond target truth table failed')
                    records.append(record)
    return {'all4_states_both_axes_every_interior_and_gap':True,'full_grid_cases':len(records),'records':records}


def directed_r5():
    r=5;oldpool=((1,2,3,4,5),(5,4,3,2,1),(2,1,3,4,5),(1,3,2,4,5))
    gpool=((1,2,3,4),(4,3,2,1),(2,1,3,4),(1,3,2,4))
    profiles=set()
    for baseindex in (0,1):
        base=(oldpool[baseindex],)*10+(gpool[baseindex],)*8
        profiles.add(base)
        for index in range(18):
            for p in oldpool if index<10 else gpool:
                profile=list(base);profile[index]=p;profiles.add(tuple(profile))
    records=[]
    for profile in sorted(profiles):
        records.append(full_check(profile[:5],profile[5:10],profile[10:14],profile[14:],
                                  {'control':'one_component_variation_identity_or_reverse_base/fixed4choices'}))
    return {'specified_profiles':len(profiles),'full_grid_cases':len(records),'records':records}


def chain_partition(avoiders):
    r=3;raw=0;chains=[];weights=Counter();stream=hashlib.sha256()
    for olds in itertools.product(avoiders[3],repeat=3):
        for guards in itertools.product(avoiders[2],repeat=2):
            raw+=1
            if any(strip(olds[i],guards[i],True)[2] or strip(olds[i+1],guards[i],False)[2] for i in range(2)):continue
            words=(tuple(map(comparison_word,olds)),tuple(map(comparison_word,guards)))
            weights[words]+=1
            row={'old_rows':olds,'guard_rows':guards,'old_comparison_words':words[0],'guard_comparison_words':words[1]}
            chains.append(row);stream.update((json.dumps(row,sort_keys=True,separators=(',',':'))+'\n').encode())
    states=tuple(sorted(weights));compatible=0;pairs=0;partstream=hashlib.sha256()
    for u,v in itertools.product(states,repeat=2):
        hu,gu=u;hv,gv=v
        allowed=not(any(hu[i][j] and gv[j][i-1] for i in range(1,r-1) for j in range(r-1))
                    or any(gu[i][j-1] and hv[j][i] for i in range(r-1) for j in range(1,r-1)))
        weight=weights[u]*weights[v]
        compatible+=weight*allowed;pairs+=1
        partstream.update((json.dumps([u,v,weight,allowed],separators=(',',':'))+'\n').encode())
    require(raw==864,'Complete small row-chain raw domain changed')
    return {'r':r,'complete_raw_row_chain_domain':raw,'compatible_row_chain_count':len(chains),
            'all_compatible_row_chains':chains,'complete_comparison_word_states':len(states),
            'complete_word_pair_domain':pairs,'all_full_chain_word_multiplicities':[{'old_words':u[0],'guard_words':u[1],'chain_count':weights[u]} for u in states],
            'claimed_K3_from_exact_kernel':compatible,'all_full_tuple_domain':6**6*2**4,
            'chain_filtered_tuple_domain':len(chains)**2,'a3_power6':6**6,
            'chain_stream_sha256':stream.hexdigest(),'partition_stream_sha256':partstream.hexdigest(),
            'no_fitted_all_size_delta_or_complete_grid_literal_census':True}


def run():
    began=time.monotonic();avoiders=avoiding_inputs()
    tables=strip_tables(avoiders)
    try:
        first=directed_r3(avoiders);diamonds=diamond_truth_controls();later=directed_r5()
    except Mismatch as error:
        return {'status':'first_complete_literal_characterization_failure','full_target_solved':False,
                'strip_tables':tables,'first_failure':error.record,'elapsed_seconds':time.monotonic()-began}
    allrecords=first['records']+diamonds['records']+later['records']
    counts=Counter();stream=hashlib.sha256()
    for row in allrecords:
        for q in row['complete_occurrences']:
            # Guard count is recovered by the exact selected point tags.
            word,tags=encode(row['old_rows'],row['old_columns'],row['guard_rows'],row['guard_columns'])
            counts[sum(tags[pos][0]=='guard' for pos in q)]+=1
        stream.update((json.dumps(row,sort_keys=True,separators=(',',':'))+'\n').encode())
    require(set(counts)=={1,2,3},'All mixed color counts must be nonvacuous')
    small=chain_partition(avoiders)
    deps=('definition_checker.py','adaptive_full_guard_probe_v1.py','FULL_GRID_STRIP_DIAMOND_PLAN_V1.md')
    return {'author':'literature-researcher-2','decision_message_id':410,'full_target_solved':False,
            'status':'all_pinned_literal_characterization_controls_pass','independent_review_status':'new author uniform reduction/controls; separate entire check pending',
            'scope':'adjacent strip + orthogonal diamond exact reduction; full bounded boxset equality and multiplicity-retaining small partition; no K density/growth theorem',
            'strip_tables':tables,'directed_r3':first,'diamond_controls_r4':diamonds,'directed_r5':later,
            'total_full_literal_grid_cases':len(allrecords),'mixed_guard_count_totals':dict(sorted(counts.items())),
            'entire_full_boxset_stream_sha256':stream.hexdigest(),'small_chain_partition':small,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'dependency_sha256':{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in deps},
            'python':platform.python_version(),'elapsed_seconds':time.monotonic()-began,
            'peak_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    require(not args.output.exists(),'Preserve every executed result')
    result=run();args.output.write_text(json.dumps(result,indent=2)+'\n')
    compact={key:value for key,value in result.items() if key not in('directed_r3','diamond_controls_r4','directed_r5','small_chain_partition')}
    if 'small_chain_partition' in result:compact['small_chain_partition']={key:value for key,value in result['small_chain_partition'].items() if key not in('all_compatible_row_chains','all_full_chain_word_multiplicities')}
    print(json.dumps(compact,indent=2))
