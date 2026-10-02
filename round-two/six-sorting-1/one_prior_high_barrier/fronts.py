"""Private complete post-preparation first-HIGH-singleton/tail fronts.
ExactlyONE preceding HIGH equal merge;261 functions survive checked minimum
locks. Full original-domain activity/minimum tests remain distinct from profiles.
"""
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT=Path(__file__).resolve().parent


def need(test,message):
    if not test:raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()


def advance(columns,gate):
    a,b=gate;a-=2;b-=2
    row=list(columns);row[a],row[b]=columns[a]&columns[b],columns[a]|columns[b]
    return tuple(row)


def tails(classes):
    # Two remaining cost6 leaves must pair. Four cost7 subtrees then pair
    # in the three unordered partitions; disjoint children commute.
    unit=[p for p,d in classes if d==6];other=[p for p,d in classes if d==7]
    need(len(unit)==2 and len(other)==3,'Post-singleton HIGH weights differ')
    first=sorted(unit);roots=sorted(other+[max(unit)])
    words=[]
    for mate in roots[1:]:
        left=sorted([roots[0],mate]);right=[p for p in roots if p not in left]
        words.append([first,left,right,sorted([max(left),max(right)])])
    need(len(words)==3,'HIGH saturated genealogy cover differs')
    return words


def main():
    start=time.monotonic();deadline=start+45
    original=json.loads((ROOT/'work/low26-partner4-construction-pilot.json').read_text())
    domains=json.loads((ROOT/'work/low26-partner4-activity-pilot.json').read_text())['all39_original_domains']
    proposal=json.loads((ROOT/'work/low26-fiveport-preparation-partner4.json').read_text())
    minimum=json.loads((ROOT/'work/partner4-fiveport-minimum-lock-screen.json').read_text())
    fixture=json.loads((ROOT/'fixture.json').read_text())
    prefix=fixture['B23']+fixture['LOW_suffixes']['4']
    states=original['core_states']
    base=tuple(sum((x>>j&1)<<i for i,x in enumerate(states)) for j in range(10))
    target_min=sum(1<<i for i,x in enumerate(states) if x==1023)
    masks=[(r['original_LOW_mask'],r['core_image_index_mask']) for r in domains]
    need(len(masks)==39 and len(states)==157,'Base and original cube cover differ')

    def identity(columns,g):
        a,b=g;active=columns[a-2]&~columns[b-2]
        return next((lo for lo,mask in masks if not active&mask),None)

    def minimum_lock(columns):
        wrong=columns[0]^target_min
        if not wrong:return None
        domain=next((lo for lo,mask in masks if not wrong&mask),None)
        return domain

    allcounts=Counter();branch_counts=[];survivors=[];rejections=[]
    for branch_id,b in enumerate(proposal['branches']):
        counts=Counter();g=b['HIGH_zero_gate'];dead=b['dead_preparation_ports']
        after_gate=advance(base,g)
        patterns=[sum((after_gate[p-2]>>i&1)<<j for j,p in enumerate(dead)) for i in range(len(states))]
        bins=[sum(1<<i for i,x in enumerate(patterns) if x==k) for k in range(32)]
        selected=[r for r in minimum['records'] if r['branch_id']==branch_id and
                  r['status']!='MINIMUM_LOCK_EXCLUDES_STANDARD_SIZE44']
        counts['surviving_preparation_functions']=len(selected)
        live={p:6 for p in (5,6,7,9,10,11)}
        live[11]=7;del live[g[0]];live[g[1]]=7
        units=[p for p,d in sorted(live.items()) if d==6]
        need(len(units)==3 and sum(1<<d for d in live.values())==448,'Prior HIGH equal-merge costs differ')
        for frow in selected:
            need(time.monotonic()<deadline,'Operational45s intake guard; no partial exclusion')
            fid=frow['function_id'];f=b['functions'][fid]
            columns=list(after_gate)
            for p,c in zip(dead,f['full_five_variable_columns']):
                columns[p-2]=sum(bins[k] for k in range(32) if c>>k&1)
            columns=tuple(columns)
            old_min=next((lo for lo,mask in masks if not (columns[0]^target_min)&mask),None)
            need((old_min is not None)==bool(frow['original_D9_minimum_masks']), 'Compressed whole-cube minimum test differs')
            need(minimum_lock(columns) is None,'An already excluded preparation survived')
            for high in units:
                for free in dead:
                    single=sorted([high,free]);counts['candidate_singleton_heads']+=1
                    inactive=identity(columns,single)
                    if inactive is not None:
                        counts['head_original_D9_identity_excluded']+=1
                        rejections.append({'branch_id':branch_id,'function_id':fid,'singleton':single,
                                           'stage':'HEAD_LOW_D9_IDENTITY','original_LOW_mask':inactive})
                        continue
                    head=advance(columns,single)
                    locked=minimum_lock(head)
                    if locked is not None:
                        counts['head_minimum_lock_excluded']+=1
                        rejections.append({'branch_id':branch_id,'function_id':fid,'singleton':single,
                                           'stage':'HEAD_MINIMUM_LOCK','original_LOW_mask':locked})
                        continue
                    after=dict(live);del after[high];after[max(single)]=7
                    need(sum(1<<d for d in after.values())==512 and len(after)==5,'HIGH singleton did not saturate512')
                    words=tails(sorted(after.items()))
                    counts['active_unlocked_singleton_heads']+=1
                    for tail_id,word in enumerate(words):
                        counts['candidate_complete_tails']+=1
                        current=head;invalid=None
                        for t,event in enumerate(word):
                            lo=identity(current,event)
                            current=advance(current,event)
                            if lo is not None:
                                invalid=('TAIL_LOW_D9_IDENTITY',lo,t);break
                            lo=minimum_lock(current)
                            if lo is not None:
                                invalid=('TAIL_MINIMUM_LOCK',lo,t);break
                        if invalid:
                            counts[invalid[0]]+=1
                            rejections.append({'branch_id':branch_id,'function_id':fid,'singleton':single,
                                               'tail_id':tail_id,'stage':invalid[0],'original_LOW_mask':invalid[1],
                                               'tail_event_index':invalid[2]})
                            continue
                        # The full HIGH genealogy must hold the second largest.
                        high_target=sum(1<<i for i,x in enumerate(states) if x!=0)
                        need(current[9]==high_target,'HIGH tail failed the whole157-state second-largest control')
                        image=sorted({sum((current[j]>>i&1)<<j for j in range(9)) for i in range(len(states))})
                        literal=prefix+[g]+f['shortest_word']+[single]+word
                        counts['surviving_complete_fronts']+=1
                        survivors.append({'branch_id':branch_id,'function_id':fid,'prior_HIGH_equal_gate':g,
                                          'preparation_word':f['shortest_word'],'singleton':single,'candidate':high,
                                          'free_operand':free,'tail_id':tail_id,'HIGH_tail':word,
                                          'prefix':literal,'prefix_sha256':digest(literal),
                                          'front_prefix_length':len(literal),'remaining_gate_budget':44-len(literal),
                                          'nine_core_states':image,'nine_core_sha256':digest(image),
                                          'global_port2_correct':current[0]==target_min})
        allcounts.update(counts);branch_counts.append({'branch_id':branch_id,'prior_HIGH_equal_gate':g,'census':dict(counts)})
    need(allcounts['surviving_preparation_functions']==261,'Surviving preparation cover differs')
    out={'agent':'six-sorting-1','role':'researcher','status':'COMPLETE_PRIVATE_ONE_PRIOR_EQUAL_MERGE_SINGLETON_FRONT_INTAKE',
         'minimum_screen_records_sha256':minimum['records_sha256'],'census':dict(allcounts),
         'branches':branch_counts,'survivors':survivors,'rejected_heads_or_tail_prefixes':rejections,
         'finite_records_sha256':digest({'branches':branch_counts,'survivors':survivors,'rejections':rejections}),
         'complete_front_image_count':len({r['nine_core_sha256'] for r in survivors}),
         'front_image_size_range':[min((len(r['nine_core_states']) for r in survivors),default=0),max((len(r['nine_core_states']) for r in survivors),default=0)],
         'remaining_gate_budgets':dict(Counter(r['remaining_gate_budget'] for r in survivors)),
         'fronts_with_correct_global_port2':sum(r['global_port2_correct'] for r in survivors),
         'scope':'ExactlyONE prior HIGH equal merge and its full five-port preparation function before the first HIGH strict singleton afterP26partner4. Written commutation/full-function normalization still to package; six/seven-port and global13 gap open.',
         'same_author_producer_only':True,'external_person_review_claimed':False,
         'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (ROOT/'work/partner4-one-prior-singleton-fronts.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('survivors','rejected_heads_or_tail_prefixes')},sort_keys=True))


if __name__=='__main__':main()
