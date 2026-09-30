"""Independent local-depth invariant and scalar clamped-input audit.

six-sorting-2, researcher. Imports no generator code. Full thirteen-wire pair profiles
are rebuilt with inverse fibers; no tagged path enumeration is used.
"""
from collections import defaultdict
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import argparse
import resource
import time

HERE = Path(__file__).resolve().parent
PAIRS13 = tuple(itertools.combinations(range(13), 2))
GATES = tuple(itertools.combinations(range(11), 2))


def scalar(values, word):
    values = list(values)
    for a,b in word:
        if values[a]>values[b]:values[a],values[b]=values[b],values[a]
    return values


def marked(pair, word, maximum):
    values=list(range(2,15))
    values[pair[0]],values[pair[1]]=((20,21) if maximum else (-2,-1))
    D=0
    for a,b in word:
        D+=int(any((values[p]>15 if maximum else values[p]<0) for p in (a,b)))
        if values[a]>values[b]:values[a],values[b]=values[b],values[a]
    positions=tuple(p for p,v in enumerate(values) if (v>15 if maximum else v<0))
    assert len(positions)==2
    return positions,D


def canonical(state):
    vectors=[]
    for profile,held in [(state[0],0),(state[1],12)]:
        weights=[0]*11
        for pair,d in profile:
            assert held in pair and d>=5
            p=next(v for v in pair if v!=held)-1
            weights[p]=2**(d-5)
        vectors.append(tuple(weights))
    return *vectors,state[2]


def main():
    assert __debug__
    started=time.monotonic()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalogue',type=Path,help='Compare all states and edges entry by entry')
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args=parser.parse_args()
    fixture=json.loads((HERE/'fixture.json').read_text())
    certificate=json.loads(args.certificate.read_text())
    expected=certificate
    assert certificate['schema']=='sorting13-B11-pruning-activity-v1'
    assert certificate['agent']=='six-sorting-2' and certificate['role']=='researcher'
    P=fixture['prefix22']
    profiles=[];original=[];fibers=[];forward=[]
    for maximum in (False,True):
        profile={};families=[]
        for pair in PAIRS13:
            positions,D=marked(pair,P,maximum)
            profile[positions]=max(profile.get(positions,-1),D)
            families.append((pair,positions,D))
        profiles.append(tuple(sorted(profile.items())))
        original.append(families)
        inv={};fwd={}
        held=12 if maximum else 0
        for gate in GATES:
            table=defaultdict(list);destinations={}
            for pair in PAIRS13:
                dest,charge=marked(pair,[(gate[0]+1,gate[1]+1)],maximum)
                table[dest].append((pair,charge));destinations[pair]=(dest,charge)
            assert all(len(v)<=2 for v in table.values())
            assert all(charge==1 for v in table.values() if len(v)==2 for _,charge in v)
            inv[gate]=[(d,v) for d,v in sorted(table.items()) if held in d]
            fwd[gate]=destinations
        fibers.append(inv);forward.append(fwd)
    @lru_cache(None)
    def transform(profile,gate,mode):
        old=dict(profile);result=[]
        for destination,preimages in fibers[mode][gate]:
            candidates=[old[p]+charge for p,charge in preimages if p in old]
            if candidates:result.append((destination,max(candidates)))
        return tuple(result)
    initial=profiles[0],profiles[1],False
    assert sum(2**d for _,d in initial[0])==sum(2**d for _,d in initial[1])==480
    stack=[initial];seen={initial};edges=set()
    depth_checks=0;deficiency_edges=0
    while stack:
        state=stack.pop()
        for gate in GATES:
            if not state[2] and gate[1]==10 and gate[0] in (0,7,9):continue
            dest=(transform(state[0],gate,0),transform(state[1],gate,1),state[2] or gate[1]==10)
            if any(sum(2**d for _,d in p)>512 for p in dest[:2]):continue
            edges.add((canonical(state),gate,canonical(dest)))
            loss=0
            for mode in (0,1):
                new=dict(dest[mode])
                for pair,d in state[mode]:
                    after,charge=forward[mode][gate][pair]
                    gap=new[after]-(d+charge)
                    allowed_loss=(mode==0 and not state[2] and dest[2] and pair==(0,11)
                                  and dict(state[0]).get((0,gate[0]+1))==6)
                    assert gap==int(allowed_loss),(state,gate,pair,gap)
                    if allowed_loss:loss+=1
                    depth_checks+=1
            assert loss<=1
            deficiency_edges+=loss
            if dest not in seen:seen.add(dest);stack.append(dest)
    terminal=(((0,1),9),),(((11,12),9),),True
    assert terminal in seen and len(seen)==2214 and len(edges)==22536
    assert certificate['profile_states']==len(seen) and certificate['profile_edges']==len(edges)
    digest=lambda value:hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()
    assert digest(sorted(map(canonical,seen)))==certificate['state_sha256']
    assert digest(sorted(edges))==certificate['edge_sha256']
    assert deficiency_edges==380
    if args.catalogue:
        actual=json.loads(args.catalogue.read_text())
        normalize=lambda x:json.loads(json.dumps(x))
        assert normalize(sorted(map(canonical,seen)))==actual['states'],'Complete state entries mismatch'
        assert normalize(sorted(edges))==actual['edges'],'Complete edge entries mismatch'
    # Reverse reachability independently confirms both first-touch cases
    # really extend to terminal profile words, and no enumerated state is dead.
    incoming=defaultdict(set)
    for s,g,d in edges:incoming[d].add(s)
    reverse_seen={canonical(terminal)};todo=list(reverse_seen)
    while todo:
        d=todo.pop()
        for s in incoming[d]:
            if s not in reverse_seen:reverse_seen.add(s);todo.append(s)
    assert reverse_seen==set(map(canonical,seen))
    first=[(s,g,d) for s,g,d in edges if not s[2] and d[2]]
    assert sum(bool(s[0][g[0]]) for s,g,d in first)==380
    assert sum(not s[0][g[0]] for s,g,d in first)==593
    # Distinct scalar ranks establish original pruning data; all free Boolean
    # assignments check the threshold bridge and exact slice images.
    families=[];strongest=0;free_assignments=0
    B11=set()
    for bits in itertools.product((0,1),repeat=13):
        after=scalar(bits,P)
        assert after[0]==min(bits) and after[12]==max(bits)
        B11.add(sum(v<<p for p,v in enumerate(after[1:12])))
    assert sorted(B11)==fixture['B11_states'] and len(B11)==158
    for maximum in (False,True):
        mode=int(maximum);held=12 if maximum else 0
        for positions,d in profiles[mode]:
            p=next(v for v in positions if v!=held)-1
            originals=[pair for pair,z,D in original[mode] if z==positions and D==d]
            domains=[]
            for pair in originals:
                free=[q for q in range(13) if q not in pair]
                domain=set()
                for values in itertools.product((0,1),repeat=11):
                    row=[0]*13
                    row[pair[0]],row[pair[1]]=((2,3) if maximum else (-2,-1))
                    for q,v in zip(free,values):row[q]=v
                    D=0
                    for a,b in P:
                        D+=int(any((row[q]>1 if maximum else row[q]<0) for q in (a,b)))
                        if row[a]>row[b]:row[a],row[b]=row[b],row[a]
                    assert D==d
                    actual=tuple(q for q,v in enumerate(row) if (v>1 if maximum else v<0))
                    assert actual==positions
                    encoded=sum(int(v>=1)<<i for i,v in enumerate(row[1:12]))
                    assert encoded in B11
                    domain.add(encoded);free_assignments+=1
                domains.append((pair,frozenset(domain)))
            all_domains=set(D for pair,D in domains)
            minimal=sorted([D for D in all_domains if not any(E<D for E in all_domains)],
                           key=lambda D:(len(D),sorted(D)))
            reps=[next(pair for pair,D in domains if D==domain) for domain in minimal]
            families.append(dict(mode='max' if maximum else 'min',partner=p,prefix_D=d,
                                 strongest_witnesses=len(domains),distinct_domains=len(all_domains),
                                 inclusion_minimal_domains=len(minimal),domain_sizes=list(map(len,minimal)),
                                 original_representatives=reps,
                                 final_D=9 if maximum or p!=10 else '8 if first10 min-binary; 9 if min-unary',
                                 domains=[sorted(D) for D in minimal]))
            strongest+=len(domains)
    normalize=lambda x:json.loads(json.dumps(x))
    families.sort(key=lambda r:(r['mode']=='max',r['partner']))
    assert normalize(families)==expected['families']
    assert strongest==126 and sum(x['inclusion_minimal_domains'] for x in families)==13
    tag_results=[]
    for mode in (0,1):
        for pair,d in profiles[mode]:
            held=12 if mode else 0
            p=next(v for v in pair if v!=held)-1
            outcomes=([[0,8,1],[0,9,2]] if mode==0 and p==10 else
                      [[10 if mode else 0,9,1],[10 if mode else 0,9,2]])
            tag_results.append(dict(mode='max' if mode else 'min',partner=p,prefix_D=d,terminal=outcomes))
    assert tag_results==certificate['terminal_tag_results']
    assert normalize(canonical(initial))==certificate['initial_state']
    assert certificate['class_labelled_distinct_domains']==sum(f['distinct_domains'] for f in families)==14
    assert certificate['strongest_families']==126
    assert certificate['guaranteed_saturated_families']==125
    assert certificate['conditionally_saturated_families']==1
    assert certificate['minimal_domains']==13 and certificate['mandatory_domains']==12 and certificate['conditional_domains']==1
    min0=next(f for f in families if f['mode']=='min' and f['partner']==0)
    small=min0['domains'][0]
    assert len(small)==101 and min0['original_representatives'][0]==(1,5)
    assert all(not (r&1) and ((r>>4)&1)<=((r>>10)&1) for r in small)
    required=((1,4),(2,4),(3,4))
    invariant_transitions=0
    for bits in itertools.product((0,1),repeat=11):
        if bits[0] or bits[4]>bits[10]:continue
        for gate in itertools.combinations(range(10),2):
            if gate in required:continue
            after=scalar(bits,[gate])
            assert after[0]==0 and after[4]<=after[10]
            invariant_transitions+=1
    assert invariant_transitions==32256
    initial_gates=sorted(g for s,g,d in edges if s==canonical(initial))
    failures=[]
    for gate in initial_gates:
        failed=[]
        for f in families:
            if f['final_D']!=9 or f['partner'] in gate:continue
            for domain in f['domains']:
                if not any((r>>gate[0]&1) and not (r>>gate[1]&1) for r in domain):
                    failed.append([f['mode'],f['partner'],len(domain)])
        if failed:failures.append([gate,failed])
    pre_edges=[(s,g,d) for s,g,d in edges if not s[2] and not d[2]]
    empty4=[e for e in pre_edges if e[0][0][4]==0]
    preparatory=[e for e in pre_edges if e[1] in required]
    assert all(e[2][0][4]==0 for e in empty4+preparatory)
    first4=[(s,g,d) for s,g,d in edges if not s[2] and d[2] and g==(4,10)]
    assert len(empty4)==603 and len(preparatory)==184
    assert sum(bool(s[0][4]) for s,g,d in first4)==76
    assert sum(not s[0][4] for s,g,d in first4)==100
    preparation=dict(slice_original_pair=[1,5],slice_size=101,required_prior_gates=required,
        invariant_transitions=invariant_transitions,profile_allowed_initial_gates=initial_gates,
        activity_forbidden_initial_gates=failures,
        prephase_empty4_edges=len(empty4),prephase_preparation_edges=len(preparatory),
        first4_binary_edges_excluded=76,first4_unary_edges_remaining_relaxation=100,
        minimum_unary_if_first_gate_on_10_is_4_10=True)
    assert normalize(preparation)==certificate['first4_preparation']
    assert len(initial_gates)==18 and failures==[[(4,10),[['min',0,101]]]]
    word=fixture['B11_known23_control']
    assert len(word)==23
    for r in B11:
        bits=[r>>i&1 for i in range(11)]
        assert scalar(bits,word)==sorted(bits)
    lift=P+[[a+1,b+1] for a,b in word]
    duplicate=[word[0]]+word
    lift46=P+[[a+1,b+1] for a,b in duplicate]
    assert len(lift)==45 and len(lift46)==46
    for bits in itertools.product((0,1),repeat=13):
        assert scalar(bits,lift)==sorted(bits)
        assert scalar(bits,lift46)==sorted(bits)
    assert 0 not in word[0]
    for r in small:
        bits=[r>>i&1 for i in range(11)]
        once=scalar(bits,[word[0]])
        assert scalar(once,[word[0]])==once
    controls=dict(B11_known23_rows=158,lifted45_original_rows=8192,
        duplicated46_original_rows=8192,duplicated_first_gate=word[0],
        duplicated_gate_is_retained_and_inactive_in_min0_slice=True)
    assert controls==certificate['controls']
    out=dict(agent='six-sorting-2',role='researcher',status='ALL_INDEPENDENT_CHECKS_PASSED',
             profile_states=len(seen),profile_edges=len(edges),local_depth_transitions=depth_checks,
             unique_loss_edges=deficiency_edges,strongest_witnesses=126,
             minimum_strongest_witnesses=sum(x['strongest_witnesses'] for x in families if x['mode']=='min'),
             maximum_strongest_witnesses=sum(x['strongest_witnesses'] for x in families if x['mode']=='max'),
             free_assignments=free_assignments,minimal_domains=13,
             unconditional_domains=12,conditional_domains=1,
             seconds=time.monotonic()-started,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(json.dumps(out,indent=2),flush=True)


if __name__=='__main__':main()
