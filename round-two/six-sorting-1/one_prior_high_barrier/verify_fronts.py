"""Independent complete singleton cover and scalar image/activity replay.
All original39 cubes/full8192 images are numeric. Tails use all legal HIGH
event orders then full32-row function deduplication, unlike producer partitions.
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


def gate(x,a,b):
    if x>>a&1 and not x>>b&1:x ^= (1<<a)|(1<<b)
    return x


def simulate(row,word):
    row=list(row)
    for a,b in word:
        if row[a]>row[b]:row[a],row[b]=row[b],row[a]
    return row


def table(word,dead):
    index={p:j for j,p in enumerate(dead)}
    result=[]
    for x in range(1<<len(dead)):
        for a,b in word:x=gate(x,index[a],index[b])
        result.append(x)
    return tuple(result)


def zero_tails(classes):
    leaves=[p for p,d in classes];histories=[];controls=0
    def visit(state,word):
        nonlocal controls
        if len(state)==1:
            need(state==((11,9),) and len(word)==4,'Final HIGH route differs')
            histories.append(word);return
        for i,j in combinations(range(len(state)),2):
            controls+=1;a,da=state[i];b,db=state[j]
            if da!=db:continue
            g=sorted([a,b]);fresh=tuple(sorted([r for k,r in enumerate(state) if k not in (i,j)]+[(g[1],da+1)]))
            visit(fresh,word+[g])
    visit(tuple(classes),[])
    functions={table(w,leaves) for w in histories}
    need(len(functions)==3,'Saturated HIGH tail full functions differ')
    return leaves,functions,len(histories),controls


def main():
    start=time.monotonic();deadline=start+45;metrics=Counter()
    fixture=json.loads((ROOT/'fixture.json').read_text())
    prefix=fixture['B23']+fixture['LOW_suffixes']['4']
    proposal=json.loads((ROOT/'work/low26-fiveport-preparation-partner4.json').read_text())
    minimum=json.loads((ROOT/'work/partner4-fiveport-minimum-lock-screen.json').read_text())
    claimed=json.loads((ROOT/'work/partner4-one-prior-singleton-fronts.json').read_text())
    full=set()
    for x in range(8192):
        row=simulate([x>>i&1 for i in range(13)],prefix)
        need(row[0]==int(x==8191) and row[1]==int(x.bit_count()>=12) and row[12]==int(x!=0), 'Initial global held ranks differ')
        full.add(sum(row[p]<<(p-2) for p in range(2,12)))
    states=sorted(full);index={x:i for i,x in enumerate(states)};domains={}
    for lo,hi in combinations(range(13),2):
        ref=[0]*13;ref[lo],ref[hi]=-2,-1;D=0
        for a,b in prefix:
            D+=ref[a]<0 or ref[b]<0
            if ref[a]>ref[b]:ref[a],ref[b]=ref[b],ref[a]
        if D!=9:continue
        free=[p for p in range(13) if p not in (lo,hi)];image=set()
        for x in range(2048):
            row=[0]*13;row[lo],row[hi]=-2,-1
            for j,p in enumerate(free):row[p]=x>>j&1
            out=simulate(row,prefix);need(out[:2]==[-2,-1],'Whole original LOW route differs')
            image.add(sum(out[p]<<(p-2) for p in range(2,12)))
        need(image<=full,'Conditional image lies outside full threshold image')
        domains[(1<<lo)|(1<<hi)]={index[x] for x in image}
    need(len(states)==157 and len(domains)==39,'Complete global/original cube images differ')
    metrics.update(original13_inputs=8192,original_LOW_free_assignments=79872)

    def active(values,g):
        a,b=g;inversions={i for i,x in enumerate(values) if (x>>(a-2)&1)>(x>>(b-2)&1)}
        return next((lo for lo,domain in domains.items() if not inversions&domain),None)

    def locked(values):
        wrong={i for i,x in enumerate(values) if (x&1)!=int(states[i]==1023)}
        if not wrong:return None
        return next((lo for lo,domain in domains.items() if not wrong&domain),None)

    groups={}
    for row in claimed['survivors']:
        key=(row['branch_id'],row['function_id'],tuple(row['singleton']))
        groups.setdefault(key,[]).append(row)
    reject_map={}
    for row in claimed['rejected_heads_or_tail_prefixes']:
        key=(row['branch_id'],row['function_id'],tuple(row['singleton']))
        need(key not in reject_map,'Head rejection duplicated');reject_map[key]=row
    need(not any(r['stage'].startswith('TAIL') for r in reject_map.values()),'Unexpected tail rejection requires extended audit')
    counts=Counter();covered=set();rejected=set();sizes=[]
    for bid,b in enumerate(proposal['branches']):
        dead=b['dead_preparation_ports'];g=b['HIGH_zero_gate']
        current=[gate(x,g[0]-2,g[1]-2) for x in states]
        live={p:6 for p in (5,6,7,9,10,11)};live[11]=7;del live[g[0]];live[g[1]]=7
        select=[r for r in minimum['records'] if r['branch_id']==bid and r['status']!='MINIMUM_LOCK_EXCLUDES_STANDARD_SIZE44']
        counts['surviving_preparation_functions']+=len(select)
        for f in select:
            need(time.monotonic()<deadline,'Operational45s full cover guard; incomplete is not exclusion')
            fid=f['function_id'];word=b['functions'][fid]['shortest_word'];values=current
            for a,q in word:values=[gate(x,a-2,q-2) for x in values]
            need(locked(values) is None,'An already minimum-locked function survived')
            for high,d in sorted(live.items()):
                if d!=6:continue
                for free in dead:
                    single=sorted([high,free]);key=(bid,fid,tuple(single));counts['candidate_singleton_heads']+=1
                    lo=active(values,single)
                    if lo is not None:
                        need(key in reject_map and reject_map[key]['stage']=='HEAD_LOW_D9_IDENTITY',
                             'Original whole-cube identity rejection differs')
                        # The producer picks masks in numerical order, while the
                        # scalar domain construction follows original wire pairs.
                        # Check its ACTUAL witness, not equality with our first one.
                        chosen=reject_map[key]['original_LOW_mask']
                        need(chosen in domains and all((values[i]>>(single[0]-2)&1)<=
                             (values[i]>>(single[1]-2)&1) for i in domains[chosen]),
                             'Proposed original cube is not a whole-cube identity')
                        rejected.add(key);counts['head_original_D9_identity_excluded']+=1;continue
                    head=[gate(x,single[0]-2,single[1]-2) for x in values]
                    need(locked(head) is None,'Unreported head minimum-lock')
                    need(key in groups and len(groups[key])==3,'Allowed singleton is missing or has incomplete genealogy list')
                    counts['active_unlocked_singleton_heads']+=1
                    after=dict(live);del after[high];after[max(single)]=7
                    leaves,functions,orders,controls=zero_tails(sorted(after.items()))
                    need({table(r['HIGH_tail'],leaves) for r in groups[key]}==functions,'Three canonical tail functions miss a legal order')
                    metrics['tail_event_orders']+=orders;metrics['tail_event_controls']+=controls
                    for row in groups[key]:
                        counts['candidate_complete_tails']+=1;out=head
                        for event in row['HIGH_tail']:
                            need(active(out,event) is None,'Unreported tail LOW identity')
                            out=[gate(x,event[0]-2,event[1]-2) for x in out]
                            need(locked(out) is None,'Unreported tail minimum-lock')
                        need(all((x>>9&1)==int(states[i]!=0) for i,x in enumerate(out)), 'Global second-largest control failed')
                        image=sorted({x&511 for x in out});need(image==row['nine_core_states'] and digest(image)==row['nine_core_sha256'],'Entire nine-core image differs')
                        literal=prefix+[g]+word+[single]+row['HIGH_tail']
                        need(literal==row['prefix'] and digest(literal)==row['prefix_sha256'] and len(literal)==32+len(word) and
                             row['remaining_gate_budget']==44-len(literal),'Literal prefix/budget differs')
                        need(row['global_port2_correct']==all((x&1)==int(states[i]==1023) for i,x in enumerate(out)), 'Global third order statistic differs')
                        counts['surviving_complete_fronts']+=1;sizes.append(len(image));covered.add(row['prefix_sha256'])
                        metrics['complete_scalar_core_inputs']+=len(states);metrics['complete_tail_comparisons']+=4*len(states)
    need(counts==Counter(claimed['census']) and len(rejected)==len(reject_map),'Complete independent front census differs')
    need(len(covered)==5613,'Literal fronts duplicated/missing')
    result={'agent':'six-sorting-1','role':'researcher','status':'PRIVATE_COMPLETE_5613_FRONT_COVER_INDEPENDENTLY_VERIFIED',
            'census':dict(counts),'metrics':dict(metrics),'front_image_size_range':[min(sizes),max(sizes)],
            'producer_records_sha256':claimed['finite_records_sha256'],'same_author_algorithmic_independence':True,
            'external_person_review_claimed':False,'seconds':time.monotonic()-start,
            'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
