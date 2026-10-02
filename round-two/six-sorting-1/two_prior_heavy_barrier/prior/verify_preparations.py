"""Independent numeric original cubes and 32-row preparation-function closure.
No packed producer imports or current-marker-profile substitution. Same author.
"""
from collections import Counter, deque
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT=Path(__file__).resolve().parent


def need(test,message):
    if not test:
        raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()


def swap(x,a,b):
    if (x >> a & 1) > (x >> b & 1):
        x ^= (1 << a) | (1 << b)
    return x


def table(word,ports):
    index={p:j for j,p in enumerate(ports)}
    rows=[]
    for x in range(32):
        for a,b in word:
            x=swap(x,index[a],index[b])
        rows.append(x)
    return tuple(rows)


def main():
    start=time.monotonic()
    fixture=json.loads((ROOT/'fixture.json').read_text())
    partners=[];metrics=Counter()
    for partner in (4,):
        proposal=json.loads((ROOT/f'work/low26-fiveport-preparation-partner{partner}.json').read_text())
        prefix=fixture['B23']+fixture['LOW_suffixes'][str(partner)]
        domains=[];masks=[]
        for lo,hi in combinations(range(13),2):
            reference=[0]*13;reference[lo],reference[hi]=-2,-1
            touched=0
            for t,(a,b) in enumerate(prefix):
                touched |= int(reference[a]<0 or reference[b]<0) << t
                if reference[a]>reference[b]:reference[a],reference[b]=reference[b],reference[a]
            need(touched.bit_count()<=9,'Initial LOW ceiling exceeded')
            if touched.bit_count()!=9:continue
            need([i for i,v in enumerate(reference) if v<0]==[0,1],'Original D9 route differs')
            free=[p for p in range(13) if p not in (lo,hi)]
            states=set();active=0
            for x in range(2048):
                row=[0]*13;row[lo],row[hi]=-2,-1
                for j,p in enumerate(free):row[p]=x >> j & 1
                actual_touched=0
                for t,(a,b) in enumerate(prefix):
                    marked=row[a]<0 or row[b]<0
                    actual_touched |= int(marked) << t
                    if row[a]>row[b]:
                        if not marked:active |= 1 << t
                        row[a],row[b]=row[b],row[a]
                need(actual_touched==touched and row[0:2]==[-2,-1],'Free-dependent original LOW route')
                states.add(sum(row[p] << (p-2) for p in range(2,12)))
            need(touched|active==(1<<26)-1,'Initial D9 redundant gate')
            masks.append((1<<lo)|(1<<hi));domains.append(states)
            metrics['original_LOW_free_assignments']+=2048
            metrics['original_LOW_gate_evaluations']+=2048*26
        need(len(domains)==39,'Original D9 domains incomplete')
        branches=[]
        expected_gates=list(combinations((5,6,7,9,10),2))
        need([tuple(b['HIGH_zero_gate']) for b in proposal['branches']]==expected_gates,
             'Prior HIGH equal-merge cover is incomplete or reordered')
        for gate,branch in zip(expected_gates,proposal['branches']):
            allowed=all(any((x >> (gate[0]-2) & 1) > (x >> (gate[1]-2) & 1) for x in domain)
                        for domain in domains)
            if not allowed:
                need(branch['status']=='INITIAL_GATE_INACTIVE_ON_A_LOW_D9_DOMAIN','Inactive initial gate accepted')
                continue
            need(branch['complete'] and branch['states_at_derived_budget12']==0,
                 'Producer had a guard or an unexpanded budget state')
            live=tuple(sorted([p for p in (5,6,7,9,10,11) if p not in gate]+[gate[1]]))
            dead=tuple(p for p in range(2,12) if p not in live)
            need(list(live)==branch['HIGH_live_ports'] and list(dead)==branch['dead_preparation_ports'],
                 'Actual live/dead port map differs')
            projected=[{sum((swap(x,gate[0]-2,gate[1]-2) >> (p-2) & 1) << j
                            for j,p in enumerate(dead)) for x in domain} for domain in domains]
            initial=tuple(range(32));queue=deque([initial]);words={initial:()};edges=0
            while queue:
                f=queue.popleft()
                for a,b in combinations(range(5),2):
                    accept=all(any((f[x] >> a & 1) > (f[x] >> b & 1) for x in domain)
                               for domain in projected)
                    if not accept:continue
                    fresh=tuple(swap(x,a,b) for x in f)
                    need(fresh!=f,'Admissible five-port comparator is an identity')
                    edges+=1
                    if fresh not in words:
                        words[fresh]=words[f]+((dead[a],dead[b]),)
                        queue.append(fresh)
            supplied={}
            for row in branch['functions']:
                word=row['shortest_word'];f=table(word,dead)
                need(f in words and len(word)==len(words[f]) and f not in supplied,
                     'Preparation witness is missing, duplicated or nonminimal')
                state=initial
                for a,b in word:
                    need(a in dead and b in dead and a<b,'Nonstandard preparation witness')
                    i,j=dead.index(a),dead.index(b)
                    need(all(any((state[x]>>i&1)>(state[x]>>j&1) for x in domain)
                             for domain in projected),'Witness gate is inactive on an original tight LOW cube')
                    state=tuple(swap(x,i,j) for x in state)
                need(state==f,'Full witness function differs after activity replay')
                cols=row['full_five_variable_columns']
                need(f==tuple(sum((col >> x & 1) << j for j,col in enumerate(cols)) for x in range(32)),
                     'Whole five-variable numeric function differs from producer columns')
                supplied[f]=row
                metrics['scalar_full_function_rows']+=32
            need(set(supplied)==set(words) and len(words)==branch['full_functions_seen'],
                 'Complete preparation-function lists differ')
            need(edges==branch['admissible_transition_count'],'All next-comparator edges differ')
            branches.append({'HIGH_zero_gate':gate,'dead_preparation_ports':dead,
                'full_preparation_functions':len(words),'admissible_edges':edges,
                'shortest_lengths':dict(sorted(Counter(map(len,words.values())).items())),
                'projected_original_domain_images':len({tuple(sorted(x)) for x in projected}),
                'full_numeric_functions_sha256':digest(sorted(words))})
        partners.append({'partner':partner,'original_D9_masks':sorted(masks),'branches':branches,
            'complete_functions':sum(b['full_preparation_functions'] for b in branches)})
    result={'agent':'six-sorting-1','role':'researcher',
        'status':'PRIVATE_UNRESTRICTED_LENGTH_FIVEPORT_ACTIVITY_CLOSURE_INDEPENDENTLY_VERIFIED',
        'partners':partners,'metrics':dict(metrics),
        'finite_records_sha256':digest({'partners':partners,'metrics':dict(metrics)}),
        'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'scope':'Exactly one prior equal HIGH merge after LOW26, complete five-variable preparation functions only. Singleton/tail/nested exclusions not checked; two/three prior merges and S13 remain open.',
        'same_author_algorithmic_independence':True,'external_person_review_claimed':False}
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
