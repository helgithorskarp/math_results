"""Six repeated-effective-(1,3) B11 classes: exact reduction and exclusions.

six-sorting-1, researcher. Python3.11+, exact standard-library arithmetic.
Inverse13/rank-permutation/scalar cores adapt this author's graph8126/source9e233924.
Imports neither the generator nor a solver. No private input is needed. Written bridges are unformalized.
"""
import argparse
from collections import Counter, deque
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
GATES = tuple(itertools.combinations(range(11), 2))
PAIRS = tuple(itertools.combinations(range(13), 2))
PINS = {
    'common': ('sorting_networks/thirteen_single_preparation_normal_form/fixture.json',
               'bf67cd5f265cc91cfd4be7fb39fb4b67df303475437aea575a167320545400ff'),
    'classes': ('sorting_networks/thirteen_extreme_multiset_quotient/certificate.json',
                'd670b600ed1c2e31990d6e2458b748d160a257b5dacf4bf15d3e270414202047'),

}
COMMON_FIELDS = ('prefix20', 'minimum_word', 'prefix22', 'B11_states',
                 'B11_known23_control', 'initial_low', 'initial_high', 'families')

def digest(x):
    return hashlib.sha256(json.dumps(x,separators=(',',':')).encode('ascii')).hexdigest()


def scalar(values,word):
    v=list(values)
    for a,b in word:
        if v[a]>v[b]:v[a],v[b]=v[b],v[a]
    return tuple(v)


def marked(pair,maximum):
    other=iter(range(11) if maximum else range(2,13))
    return tuple((11 if maximum else 0)+pair.index(i) if i in pair else next(other) for i in range(13))


def transport(values,word,maximum):
    values=list(values);hits=0
    for a,b in word:
        hits+=bool(values[a]>=11 or values[b]>=11) if maximum else bool(values[a]<2 or values[b]<2)
        if values[a]>values[b]:values[a],values[b]=values[b],values[a]
    ports=tuple(i for i,v in enumerate(values) if (v>=11 if maximum else v<2))
    assert len(ports)==2
    return ports,hits


def original_profile(prefix,maximum):
    out={}
    for p in PAIRS:
        destination,d=transport(marked(p,maximum),prefix,maximum)
        out[destination]=max(out.get(destination,-1),d)
    return tuple(sorted(out.items()))


def fibers(maximum):
    result={}
    for g in GATES:
        out={}
        for p in PAIRS:
            dest,d=transport(marked(p,maximum),((g[0]+1,g[1]+1),),maximum)
            out.setdefault(dest,[]).append((p,d))
        assert all(len(pre)<=2 for pre in out.values())
        assert all(d==1 for pre in out.values() if len(pre)==2 for p,d in pre)
        result[g]=out
    return result


def inverse(profile,fb):
    old=dict(profile);out={}
    for dest,pre in fb.items():
        values=[old[p]+d for p,d in pre if p in old]
        if values:out[dest]=max(values)
    return tuple(sorted(out.items()))


def canonical(s):
    vectors=[]
    for profile,held in ((s[0],0),(s[1],12)):
        vector=[0]*11
        for pair,d in profile:
            assert held in pair and d>=5
            port=next(i for i in pair if i!=held)-1;assert 0<=port<11
            vector[port]=1<<(d-5)
        vectors.append(tuple(vector))
    return *vectors,s[2]


def empty(s):
    c=canonical(s)
    return tuple(i for i,(a,b) in enumerate(zip(c[0],c[1])) if not a and not b)


def terminal(s):
    return s==((((0,1),9),),(((11,12),9),),True)


def full_graph(prefix):
    low,high=fibers(False),fibers(True)
    root=original_profile(prefix,False),original_profile(prefix,True),False
    assert sum(1<<d for p,d in root[0])==sum(1<<d for p,d in root[1])==480
    stack=[root];seen=set();outgoing={};edges=[]
    while stack:
        s=stack.pop()
        if s in seen:continue
        seen.add(s);outgoing[s]={}
        for g in GATES:
            if not s[2] and g[1]==10 and g[0] in (0,7,9):continue
            dl,dh=inverse(s[0],low[g]),inverse(s[1],high[g])
            if sum(1<<d for p,d in dl)>512 or sum(1<<d for p,d in dh)>512:continue
            child=dl,dh,s[2] or g[1]==10
            outgoing[s][g]=child;edges.append((canonical(s),g,canonical(child)))
            if child not in seen:stack.append(child)
    states=sorted(map(canonical,seen));before=Counter();unary=Counter();entries=set();loops=0
    for s in states:
        J={i for i,(a,b) in enumerate(zip(s[0],s[1])) if not a and not b}
        if not s[2]:
            assert sum(s[0])==sum(s[1])==15 and s[0][10]==s[1][10]==1
            assert [i for i,(a,b) in enumerate(zip(s[0],s[1])) if a and b]==[10]
            assert all(w==0 or w>=2 and w&(w-1)==0 for w in s[0][:10]+s[1][:10])
            assert len(J)<=4;before[len(J)]+=1
        else:assert sum(s[0])==sum(s[1])==16 and not any(a and b for a,b in zip(s[0],s[1]))
    for s,g,d in edges:
        J={i for i,(a,b) in enumerate(zip(s[0],s[1])) if not a and not b}
        K={i for i,(a,b) in enumerate(zip(d[0],d[1])) if not a and not b}
        if s==d:assert set(g)<=J;loops+=1;continue
        if not s[2] and d[2] and s[0][g[0]]==0:
            assert g[0] in J and K==J-{g[0]};entries.add((s,g,d));unary[len(J)]+=1
        else:
            assert J<=K and set(g).isdisjoint(J)
            if s[2] or not d[2]:assert len(K)==len(J)+1
    for s in seen:
        for g in itertools.combinations(empty(s),2):assert outgoing[s][g]==s
    audit={'states':len(seen),'edges':len(edges),'loops':loops,
           'state_sha256':digest(states),'edge_sha256':digest(sorted(edges)),
           'pre_empty_histogram':dict(sorted(before.items())),
           'unary_entry_histogram':dict(sorted(unary.items())),'unary_entries':len(entries)}
    assert len(seen)==2214 and len(edges)==22536
    return root,outgoing,entries,audit


def rank_monoids():
    records=[];lookups={}
    for n in range(1,5):
        gates=tuple(itertools.combinations(range(n),2));inputs=tuple(itertools.permutations(range(n)))
        states=[inputs];indices={inputs:0};words=[()];edges=[];queue=deque([0])
        while queue:
            i=queue.popleft()
            for k,g in enumerate(gates):
                child=tuple(scalar(row,(g,)) for row in states[i])
                if child not in indices:
                    indices[child]=len(states);states.append(child);words.append(words[i]+(k,));queue.append(indices[child])
                edges.append([i,k,indices[child]])
        records.append({'wires':n,'maps':len(states),'edges':len(edges),
                        'loops':sum(i==j for i,k,j in edges),'diameter':max(map(len,words)),
                        'length_histogram':dict(sorted(Counter(map(len,words)).items())),
                        'edge_sha256':digest(edges),'representative_words':words})
        lookups[n]={s:words[i] for i,s in enumerate(states)}
    return records,lookups


def canonical_trace(word):
    word=list(word);result=[]
    while word:
        available=[i for i,g in enumerate(word) if all(set(g).isdisjoint(h) for h in word[:i])]
        i=min(available,key=lambda j:(word[j],j));result.append(word.pop(i))
    return tuple(result)


def independent_triples(f,root,outgoing):
    code=int(f['class_code']);start=root,0;target=((((0,1),9),),(((11,12),9),),True),code
    graph={};stack=[start];seen=set()
    while stack:
        q=stack.pop()
        if q in seen:continue
        seen.add(q);s,used=q;graph[q]=[]
        for g,d in outgoing[s].items():
            k=GATES.index(g)
            if d==s or (used>>(2*k)&3)>=(code>>(2*k)&3):continue
            child=d,used+(1<<(2*k));graph[q].append((g,child))
            if child not in seen:stack.append(child)
    visiting=set()
    @lru_cache(None)
    def ways(q):
        assert q not in visiting,'Non-loop cycle'
        visiting.add(q)
        n=1 if q==target else sum(ways(d) for g,d in graph[q])
        visiting.remove(q);return n
    assert ways(start)==f['parent_effective_words']
    triples=Counter()
    def enumerate_words(q,word):
        if q==target:
            split=next(i for i,g in enumerate(word) if g[1]==10)
            b,g,a=canonical_trace(word[:split]),word[split],canonical_trace(word[split+1:])
            triples[b,g,a]+=1;return
        for g,d in graph[q]:
            if ways(d):enumerate_words(d,word+(g,))
    enumerate_words(start,())
    return [[list(map(GATES.index,b)),GATES.index(g),list(map(GATES.index,a)),n]
            for (b,g,a),n in sorted(triples.items())]


def reconstruct(f):
    prefix=f['prefix22'];assert len(prefix)==22
    assert prefix==f['prefix20'][:-1]+[[10,12]]+f['minimum_word'] and f['minimum_word']==[[0,5],[0,1]]
    rows=set()
    control=prefix+[[a+1,b+1] for a,b in f['B11_known23_control']];assert len(control)==45
    for x in range(8192):
        bits=tuple(x>>i&1 for i in range(13));out=scalar(bits,prefix)
        assert out[0]==min(bits) and out[12]==max(bits)
        rows.add(sum(v<<i for i,v in enumerate(out[1:12])))
        assert scalar(bits,control)==tuple(sorted(bits))
    assert sorted(rows)==f['B11_states'] and len(rows)==158
    for fam in f['families']:
        maximum=fam['mode']=='max'
        assert len(fam['domains'])==len(fam['original_representatives'])
        for pair,domain in zip(fam['original_representatives'],fam['domains']):
            pair=tuple(pair);dest,d=transport(marked(pair,maximum),prefix,maximum)
            assert d==fam['prefix_D'] and dest==tuple(sorted((12 if maximum else 0,fam['partner']+1)))
            free=[i for i in range(13) if i not in pair];actual=set()
            for x in range(2048):
                values=[0]*13
                values[pair[0]],values[pair[1]]=(1,3) if maximum else (-2,-1)
                for j,i in enumerate(free):values[i]=x>>j&1
                out=scalar(values,prefix)
                actual.add(sum(int(v>0)<<i for i,v in enumerate(out[1:12])))
            assert sorted(actual)==domain
    return 13*2048


def completion_table(f,root,outgoing,monoids,triples):
    rows=f['B11_states'];images=[];ids={};cases=[];representatives={};families=f['families']
    words=[]
    for ti,(bl,fl,al,count) in enumerate(triples):
        before=tuple(GATES[k] for k in bl);first=GATES[fl];after=tuple(GATES[k] for k in al);s=root
        for g in before:s=outgoing[s][g]
        J=empty(s);assert len(J)==len(before) and first[0] in J
        local=tuple(itertools.combinations(range(len(J)),2))
        for mi,labels in enumerate(monoids[len(J)-1]['representative_words']):
            prep=tuple((J[local[k][0]],J[local[k][1]]) for k in labels);word=before+prep+(first,)+after
            middle=set()
            for r in rows:
                out=scalar(tuple(r>>w&1 for w in range(11)),word)
                assert out[0]==int(r==2047) and out[10]==int(r!=0)
                middle.add(sum(v<<w for w,v in enumerate(out[1:10])))
            image=tuple(sorted(middle))
            if image not in ids:ids[image]=len(images);images.append(image)
            imageid=ids[image];budget=11-len(prep);ci=len(cases)
            cases.append([ti,mi,imageid,budget]);words.append(word)
            representatives.setdefault((imageid,budget),(ci,word))
            # Independently check all thirteen actual marked-pair saturations
            # on every prefix, including equivalent-image representatives.
            full=f['prefix22']+[(a+1,b+1) for a,b in word]
            for fam in families:
                for p in fam['original_representatives']:
                    maximum=fam['mode']=='max';dest,d=transport(marked(tuple(p),maximum),full,maximum)
                    assert d==9 and dest==((11,12) if maximum else (0,1))
    pairs=[];survivors=[];blocked=0;actual_obstruction_checks=0
    for (ii,budget),(ci,word) in sorted(representatives.items()):
        domains=[[[list(r>>w&1 for w in range(11)) for r in d] for d in fam['domains']] for fam in families]
        routes=[fam['partner'] for fam in families];hits=[fam['prefix_D'] for fam in families];obstacle=None
        for event,(a,b) in enumerate(word):
            for j,(route,ds) in enumerate(zip(routes,domains)):
                if route in (a,b):continue
                for k,domain in enumerate(ds):
                    if not any(row[a]>row[b] for row in domain) and obstacle is None:obstacle=[event,j,k]
            for ds in domains:
                for domain in ds:
                    for row in domain:
                        if row[a]>row[b]:row[a],row[b]=row[b],row[a]
            for j,fam in enumerate(families):
                if routes[j] in (a,b):hits[j]+=1;routes[j]=b if fam['mode']=='max' else a
        assert hits==[9]*len(families) and all(r==(10 if fam['mode']=='max' else 0) for r,fam in zip(routes,families))
        pairs.append([ii,budget,ci,obstacle])
        if obstacle is None:survivors.append([ii,budget,ci]);continue
        blocked+=1;event,j,k=obstacle;fam=families[j];pair=tuple(fam['original_representatives'][k]);maximum=fam['mode']=='max'
        free=[i for i in range(13) if i not in pair]
        pre=f['prefix22']+[(a+1,b+1) for a,b in word[:event]];a,b=word[event];a+=1;b+=1
        for x in range(2048):
            v=[0]*13;v[pair[0]],v[pair[1]]=(1,3) if maximum else (-2,-1)
            for k,i in enumerate(free):v[i]=x>>k&1
            out=scalar(v,pre)
            assert out[a] in (0,1) and out[b] in (0,1) and out[a]<=out[b]
            actual_obstruction_checks+=1
    table={'effective_words':sum(t[3] for t in triples),'triples':triples,'local_map_cases':cases,
           'images9':images,'image_budget_pairs':pairs,'remaining_completion_pairs':survivors,
           'prefix_activity_excluded_pairs':blocked,
           'remaining_row_budget_pairs':sorted([[len(images[i]),b] for i,b,c in survivors]),
           'scope':'Complete literal-image/budget reduction with prefix activity obstructions.'}
    return table,actual_obstruction_checks


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', type=Path, default=HERE.parents[1])
    parser.add_argument('--ten-parent', type=Path)
    parser.add_argument('--peer-certificate', type=Path)
    parser.add_argument('--certificate', type=Path, default=HERE / 'reduction.json')
    return parser.parse_args()


def load_premises(f, args):
    loaded = {}
    for key, (relative, sha) in PINS.items():
        override = args.ten_parent if key == 'ten' else args.peer_certificate if key == 'peer' else None
        path = override or args.repository / relative
        raw = path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == sha, ('import bytes changed', key)
        loaded[key] = json.loads(raw)
    for field in COMMON_FIELDS:
        assert f[field] == loaded['common'][field], ('common literal input changed', field)
    table = loaded['classes']['class_table']
    assert len(table) == 480 and digest(table) == f['parent_class_table_sha256']
    assert f['repeated_effective_gate'] == [1,3]
    doubled = GATES.index((1, 3))
    selected = [[i, code, events, words] for i, (code, events, words) in enumerate(table)
                if (int(code) >> (2 * doubled)) & 3 == 2]
    assert selected == f['classes'] and len(selected) == 6
    assert all(events == 11 and words == 5385 for i, code, events, words in selected)
    return loaded


def summary(index, code, table):
    return {'parent_index': index, 'class_code': code,
            'effective_orders': table['effective_words'], 'phase_triples': len(table['triples']),
            'normalized_prefixes': len(table['local_map_cases']), 'literal_images': len(table['images9']),
            'image_budget_pairs': len(table['image_budget_pairs']),
            'prefix_activity_blocked': table['prefix_activity_excluded_pairs'],
            'table_sha256': digest(table), 'phase_triple_records': table['triples'],
            'activity_pair_records': table['image_budget_pairs'],
            'after_activity_pairs': table['remaining_completion_pairs']}


def prefix_word(f, table, monoids, case, root, outgoing):
    ti, mi, image, budget = table['local_map_cases'][case]
    before, first, after, _ = table['triples'][ti]
    state = root
    for label in before:
        state = outgoing[state][GATES[label]]
    ports = empty(state)
    local = tuple(itertools.combinations(ports, 2))
    prep = [local[label] for label in monoids[len(ports) - 1]['representative_words'][mi]]
    word = [GATES[label] for label in before] + prep + [GATES[first]] + [GATES[label] for label in after]
    assert len(word) + budget == 22
    return word


def original_image(f, word, expected_rows):
    full = f['prefix22'] + [(a + 1, b + 1) for a, b in word]
    image = set()
    for x in range(8192):
        values = [x >> i & 1 for i in range(13)]
        out = scalar(values, full)
        ordered = sorted(values)
        assert out[:2] == tuple(ordered[:2]) and out[11:] == tuple(ordered[11:])
        image.add(sum(v << i for i, v in enumerate(out[2:11])))
    assert sorted(image) == list(expected_rows)
    return full


def marked_simulate(values, word, maximum):
    values = list(values)
    passages = 0
    for a, b in word:
        passages += (values[a] > 1 or values[b] > 1) if maximum else (values[a] < 0 or values[b] < 0)
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values, passages


def check_boundary(record, full, rows):
    assert record['mode'] in ('min', 'max')
    maximum = record['mode'] == 'max'
    k = record['boundary_size']
    assert k in (1, 2)
    control = record['original_control']
    assert 0 <= control < 8192
    control_bits = [control >> i & 1 for i in range(13)]
    marked_ports = [i for i, v in enumerate(control_bits) if v == int(maximum)]
    free_ports = [i for i in range(13) if i not in marked_ports]
    assert len(marked_ports) == k + 2 and len(free_ports) == record['free_inputs'] == 11 - k
    end_ports = set(range(11 - k, 13)) if maximum else set(range(k + 2))
    boolean_out = scalar(control_bits, full)
    assert boolean_out == tuple(sorted(control_bits))
    lower = {9: 25, 10: 29}[len(free_ports)]
    assert record['imported_size_bound'] == lower
    assignments = 0
    for free_values in itertools.product((0, 1), repeat=len(free_ports)):
        values = [None] * 13
        for order, port in enumerate(marked_ports):
            values[port] = order + 2 if maximum else -order - 1
        for port, value in zip(free_ports, free_values):
            values[port] = value
        output, passages = marked_simulate(values, full, maximum)
        marks = {i for i, v in enumerate(output) if (v > 1 if maximum else v < 0)}
        assert marks == end_ports and passages == record['prefix_passages']
        assignments += 1
    cap = 44 - lower - record['prefix_passages']
    assert cap == record['touch_cap']
    cut = record['cut_row9']
    assert cut in rows
    original = record['cut_original']
    assert 0 <= original < 8192
    out = scalar([original >> i & 1 for i in range(13)], full)
    assert sum(v << i for i, v in enumerate(out[2:11])) == cut
    K = range(9 - k, 9) if maximum else range(k)
    marked_total = cut.bit_count() if maximum else 9 - cut.bit_count()
    marked_inside = sum((cut >> i & 1) == int(maximum) for i in K)
    required = min(k, marked_total) - marked_inside
    assert required == record['required_crossings'] and required > 0
    internal = 0
    if record['forced_internal_gate9'] is not None:
        assert k == 2
        forced = 128 if maximum else 509
        assert record['forced_internal_gate9'] == ([7, 8] if maximum else [0, 1])
        assert record['forced_internal_row9'] == forced and forced in rows
        source = record['forced_internal_original']
        assert 0 <= source < 8192
        output = scalar([source >> i & 1 for i in range(13)], full)
        assert sum(v << i for i, v in enumerate(output[2:11])) == forced
        internal = 1
    else:
        assert record['forced_internal_row9'] is None and record['forced_internal_original'] is None
    assert record['required_touches'] == required + internal > cap
    return assignments


def local_cut_controls():
    checks = 0
    forced_checks = 0
    for maximum in (False, True):
        for k in (1, 2):
            K = set(range(9 - k, 9)) if maximum else set(range(k))
            control = [int(i in K) if maximum else int(i not in K) for i in range(9)]
            for x in range(512):
                values = [x >> i & 1 for i in range(9)]
                before = sum(values[i] == int(maximum) for i in K)
                for gate in itertools.combinations(range(9), 2):
                    assert scalar(control, (gate,)) == tuple(control)
                    output = scalar(values, (gate,))
                    change = sum(output[i] == int(maximum) for i in K) - before
                    crossing = (gate[0] in K) != (gate[1] in K)
                    assert 0 <= change <= int(crossing)
                    checks += 1
        forced = [0] * 7 + [1, 0] if maximum else [1, 0] + [1] * 7
        mandatory = (7, 8) if maximum else (0, 1)
        for gate in itertools.combinations(range(9), 2):
            output = scalar(forced, (gate,))
            assert output == tuple(sorted(forced)) if gate == mandatory else output == tuple(forced)
            forced_checks += 1
    return checks, forced_checks


def key(record):
    return record['parent_index'], record['image'], record['budget'], record['case']


def main():
    assert not sys.flags.optimize, 'Run with assertions enabled'
    args = arguments()
    fixture = json.loads((HERE / 'fixture.json').read_text())
    certificate = json.loads(args.certificate.read_text())
    assert certificate['schema'] == 'sorting13-repeated13-reduction-v1'
    assert certificate['agent'] == 'six-sorting-1' and certificate['role'] == 'researcher'
    assert certificate['fixture_sha256'] == digest(fixture)
    assert [(r['parent_index'], r['class_code']) for r in certificate['classes']] == [(r[0], r[1]) for r in fixture['classes']]
    premises = load_premises(fixture, args)
    domain_assignments = reconstruct(fixture)
    root, outgoing, entries, audit = full_graph(fixture['prefix22'])
    assert canonical(root) == (tuple(fixture['initial_low']), tuple(fixture['initial_high']), False)
    monoids, _ = rank_monoids()
    assert digest(monoids) == certificate['local_monoid_sha256']
    expected, tables = [], {}
    after_activity = set()
    activity_checks = 0
    for index, code, events, orders in fixture['classes']:
        f = dict(fixture, class_code=code, parent_effective_words=orders)
        triples = independent_triples(f, root, outgoing)
        table, actual = completion_table(f, root, outgoing, monoids, triples)
        activity_checks += actual
        tables[index] = table
        expected.append(summary(index, code, table))
        after_activity.update((index, image, budget, case) for image, budget, case in table['remaining_completion_pairs'])
    assert json.loads(json.dumps(expected)) == certificate['classes']
    boundaries = certificate['boundary_obstructions']
    imports = certificate['imported_obstructions']
    tails = certificate['remaining_tails']
    all_records = boundaries + imports + tails
    assert len(all_records) == len({key(r) for r in all_records})
    assert {key(r) for r in all_records} == after_activity
    actual_marker_checks = 0
    literal_prefix_inputs = 0
    for record in all_records:
        index, image, budget, case = key(record)
        table = tables[index]
        word = prefix_word(fixture, table, monoids, case, root, outgoing)
        full = original_image(fixture, word, table['images9'][image])
        assert len(full) + budget == 44
        literal_prefix_inputs += 8192
        if record in boundaries:
            actual_marker_checks += check_boundary(record, full, table['images9'][image])
        else:
            assert record['class_code'] == next(code for i, code, e, n in fixture['classes'] if i == index)
            assert record['prefix_B11'] == [list(g) for g in word]
            assert record['rows9'] == list(table['images9'][image])
            assert record['rows9_sha256'] == digest(record['rows9'])
    open_indices = {r['parent_index'] for r in tails}
    excluded = [i for i, code, e, n in fixture['classes'] if i not in open_indices]
    assert excluded == certificate['excluded_parent_indices'] == [36, 151, 157, 239]
    assert certificate['covered_effective_orders'] == sum(n for i, code, e, n in fixture['classes']) == 32310
    assert certificate['excluded_effective_orders'] == sum(n for i, code, e, n in fixture['classes'] if i in excluded) == 21540
    assert len(boundaries) == 16 and len(imports) == 0 and len(tails) == 3
    local, mandatory = local_cut_controls()
    print(json.dumps({'status': 'INDEPENDENT_REPEATED13_REDUCTION_VERIFIED',
        'covered_classes': 6, 'covered_effective_orders': 32310, 'excluded_classes': 4,
        'excluded_effective_orders': 21540, 'profile_states': audit['states'], 'profile_edges': audit['edges'],
        'rank_monoid_counts': [m['maps'] for m in monoids], 'original_B11_inputs': 8192,
        'known_full45_inputs': 8192, 'actual_clamped_domain_assignments': domain_assignments,
        'normalized_prefixes': sum(r['normalized_prefixes'] for r in expected),
        'B11_prefix_rows': 158 * sum(r['normalized_prefixes'] for r in expected),
        'literal_image_budget_pairs': sum(r['image_budget_pairs'] for r in expected),
        'prefix_activity_obstructions': sum(r['prefix_activity_blocked'] for r in expected),
        'actual_marked_prefix_obstruction_checks': activity_checks,
        'original_literal_prefix_inputs': literal_prefix_inputs,
        'actual_boundary_marked_free_assignments': actual_marker_checks,
        'local_cut_truth_checks': local, 'mandatory_internal_gate_checks': mandatory,
        'boundary_obstructions': len(boundaries), 'imported_obstructions': len(imports),
        'remaining_tails': [[r['parent_index'], r['image'], len(r['rows9']), r['budget']] for r in tails],
        'certificate_sha256': digest(certificate)}))


if __name__ == '__main__':
    main()
