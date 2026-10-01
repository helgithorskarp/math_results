"""All forty-five eleven-distinct first-(4,10) B11 classes: exact reduction.

six-sorting-1, researcher. Python3.11+, exact standard-library arithmetic.
Profile/local-map cores adapt this author's graph8126/source9e233924.
No solver or private fixture is needed. Written bridges are unformalized.
"""
import argparse
from collections import Counter, deque
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import sys
import signal
import time
import resource

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


def move(weights,gate,maximum):
    a,b=gate;out=list(weights);w=2*max(weights[a],weights[b])
    out[a],out[b]=(0,w) if maximum else (w,0)
    return tuple(out)


def successor(s,g):
    lo,hi,flag=s
    if not flag and g[1]==10 and g[0] in (0,7,9):return None
    dl,dh=move(lo,g,False),move(hi,g,True)
    if sum(dl)>16 or sum(dh)>16:return None
    return dl,dh,flag or g[1]==10


def empty(s):
    return tuple(i for i,(a,b) in enumerate(zip(s[0],s[1])) if not a and not b)


def terminal(s):
    return s==((16,)+(0,)*10,(0,)*10+(16,),True)


def planes(rows,n):
    return tuple(sum((r>>w&1)<<i for i,r in enumerate(rows)) for w in range(n))


def apply(p,word):
    p=list(p)
    for a,b in word:p[a],p[b]=p[a]&p[b],p[a]|p[b]
    return tuple(p)


def local_monoids():
    records=[];lookups={}
    for n in range(1,5):
        gates=tuple(itertools.combinations(range(n),2));root=planes(range(1<<n),n)
        states=[root];ids={root:0};words=[()];queue=deque([0]);edges=[]
        while queue:
            i=queue.popleft()
            for k,g in enumerate(gates):
                d=apply(states[i],(g,))
                if d not in ids:
                    ids[d]=len(states);states.append(d);words.append(words[i]+(k,));queue.append(ids[d])
                edges.append([i,k,ids[d]])
        records.append({'wires':n,'maps':len(states),'edges':len(edges),
                        'loops':sum(i==j for i,k,j in edges),
                        'diameter':max(map(len,words)),
                        'length_histogram':dict(sorted(Counter(map(len,words)).items())),
                        'edge_sha256':digest(edges),'representative_words':words})
        lookups[n]={s:words[i] for i,s in enumerate(states)}
    return records,lookups


def trace(word):
    remaining=set(range(len(word)));answer=[]
    while remaining:
        allowed=[i for i in remaining if not any(j<i and not set(word[j]).isdisjoint(word[i]) for j in remaining)]
        i=min(allowed,key=lambda j:(word[j],j));answer.append(word[i]);remaining.remove(i)
    return tuple(answer)


def class_triples(f,root):
    code=int(f['class_code']);start=root,0;target=((16,)+(0,)*10,(0,)*10+(16,),True),code
    nodes={start};outgoing={};queue=deque([start])
    while queue:
        q=queue.popleft();s,used=q;choices=[]
        for k,g in enumerate(GATES):
            d=successor(s,g)
            if d is None or d==s or (used>>(2*k)&3)>=(code>>(2*k)&3):continue
            child=d,used+(1<<(2*k));choices.append((g,child))
            if child not in nodes:nodes.add(child);queue.append(child)
        outgoing[q]=choices
    @lru_cache(None)
    def live(q):return q==target or any(live(d) for g,d in outgoing[q])
    triples=Counter()
    def walk(q,before,first,after):
        if q==target:
            assert first is not None and len(before)+1+len(after)==11
            triples[trace(before),first,trace(after)]+=1;return
        for g,d in outgoing[q]:
            if not live(d):continue
            if first is None and d[0][2]:walk(d,before,g,())
            elif first is None:walk(d,before+(g,),None,after)
            else:walk(d,before,first,after+(g,))
    walk(start,(),None,())
    table=[[list(map(GATES.index,b)),GATES.index(g),list(map(GATES.index,a)),n]
           for (b,g,a),n in sorted(triples.items())]
    assert sum(triples.values())==f['parent_effective_words']
    return table


def completion_table(f,root,monoids,triples):
    rows=f['B11_states'];truth=planes(rows,11);rowindex={r:i for i,r in enumerate(rows)}
    families=f['families'];domains=tuple(tuple(sum(1<<rowindex[r] for r in d) for d in fam['domains']) for fam in families)
    images=[];ids={};cases=[];representatives={};extreme_lo=sum((r==2047)<<i for i,r in enumerate(rows));extreme_hi=sum((r!=0)<<i for i,r in enumerate(rows))
    for ti,(bl,fl,al,count) in enumerate(triples):
        before=tuple(GATES[k] for k in bl);first=GATES[fl];after=tuple(GATES[k] for k in al);s=root
        for g in before:s=successor(s,g)
        J=empty(s);assert len(J)==len(before) and first[0] in J
        local=tuple(itertools.combinations(range(len(J)),2))
        for mi,labels in enumerate(monoids[len(J)-1]['representative_words']):
            prep=tuple((J[local[k][0]],J[local[k][1]]) for k in labels);word=before+prep+(first,)+after
            out=apply(truth,word);assert out[0]==extreme_lo and out[10]==extreme_hi
            image=tuple(sorted(set(sum((out[w]>>i&1)<<(w-1) for w in range(1,10)) for i in range(len(rows)))))
            if image not in ids:ids[image]=len(images);images.append(image)
            imageid=ids[image];budget=11-len(prep);ci=len(cases)
            cases.append([ti,mi,imageid,budget])
            representatives.setdefault((imageid,budget),(ci,word))
    pairs=[];survivors=[];blocked=0
    for (ii,budget),(ci,word) in sorted(representatives.items()):
        wires=list(truth);routes=[fam['partner'] for fam in families];hits=[fam['prefix_D'] for fam in families];obstacle=None
        for event,(a,b) in enumerate(word):
            swaps=wires[a]&~wires[b]
            for j,(r,ds) in enumerate(zip(routes,domains)):
                if r in (a,b):continue
                for k,d in enumerate(ds):
                    if not swaps&d and obstacle is None:obstacle=[event,j,k]
            wires[a],wires[b]=wires[a]&wires[b],wires[a]|wires[b]
            for j,fam in enumerate(families):
                if routes[j] in (a,b):hits[j]+=1;routes[j]=b if fam['mode']=='max' else a
        assert hits==[9]*len(families) and all(r==(10 if fam['mode']=='max' else 0) for r,fam in zip(routes,families))
        pairs.append([ii,budget,ci,obstacle])
        if obstacle is None:survivors.append([ii,budget,ci])
        else:blocked+=1
    return {'effective_words':sum(t[3] for t in triples),'triples':triples,'local_map_cases':cases,
            'images9':images,'image_budget_pairs':pairs,'remaining_completion_pairs':survivors,
            'prefix_activity_excluded_pairs':blocked,
            'remaining_row_budget_pairs':sorted([[len(images[i]),b] for i,b,c in survivors]),
            'scope':'Complete literal-image/budget reduction with prefix activity obstructions.'}


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
        raw = (args.repository / relative).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == sha, ('import bytes changed', key)
        loaded[key] = json.loads(raw)
    for field in COMMON_FIELDS:
        assert f[field] == loaded['common'][field], ('common literal input changed', field)
    table = loaded['classes']['class_table']
    assert len(table) == 480 and digest(table) == f['parent_class_table_sha256']
    assert f['first_touch_effective_gate'] == [4, 10]
    gate = GATES.index((4, 10))
    selected = [[i, code, events, words] for i, (code, events, words) in enumerate(table)
                if events == 11 and ((int(code) >> (2*gate)) & 3) == 1
                and all(((int(code) >> (2*k)) & 3) <= 1 for k in range(55))]
    assert selected == f['classes'] and len(selected) == 45
    assert sum(r[3] for r in selected) == 440190
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

def replay(row, word, maximum=False):
    passages = 0
    for a, b in word:
        left, right = row >> a & 1, row >> b & 1
        passages += (left or right) if maximum else not (left and right)
        if left > right:
            row ^= (1 << a) | (1 << b)
    return row, passages


def prefix_word(f, table, monoids, case):
    ti, mi, image, budget = table['local_map_cases'][case]
    bl, fl, al, _ = table['triples'][ti]
    before = [GATES[z] for z in bl]
    s = (tuple(f['initial_low']), tuple(f['initial_high']), False)
    for g in before:
        s = successor(s, g)
    ports = empty(s)
    local = tuple(itertools.combinations(ports, 2))
    preparation = [local[z] for z in monoids[len(ports) - 1]['representative_words'][mi]]
    word = before + preparation + [GATES[fl]] + [GATES[z] for z in al]
    assert len(word) + budget == 22
    return word


def boundary_obstruction(f, table, word, index, image, budget, case):
    full = f['prefix22'] + [[a + 1, b + 1] for a, b in word]
    preimages = {}
    controls = {}
    for x in range(8192):
        out, _ = replay(x, full)
        preimages.setdefault((out >> 2) & 511, x)
        for maximum in (False, True):
            marks = x.bit_count() if maximum else 13 - x.bit_count()
            if marks not in (3, 4):
                continue
            k = marks - 2
            target = ((1 << marks) - 1) << (13 - marks) if maximum else 8191 ^ ((1 << marks) - 1)
            if out != target:
                continue
            _, spent = replay(x, full, maximum)
            key = maximum, k
            if key not in controls or spent > controls[key][1]:
                controls[key] = x, spent
    rows = table['images9'][image]
    assert sorted(preimages) == list(rows)
    for maximum in (False, True):
        for k in (1, 2):
            if (maximum, k) not in controls:
                continue
            control, spent = controls[maximum, k]
            mask = ((1 << k) - 1) << (9 - k) if maximum else (1 << k) - 1
            deficits = []
            for row in rows:
                marked = row.bit_count() if maximum else 9 - row.bit_count()
                inside = (row & mask).bit_count() if maximum else k - (row & mask).bit_count()
                deficits.append((min(k, marked) - inside, row))
            required, cut = max(deficits)
            forced_row = 128 if maximum else 509
            internal = int(k == 2 and forced_row in rows)
            lower = {1: 29, 2: 25}[k]
            cap = 44 - lower - spent
            if required + internal <= cap:
                continue
            return {'parent_index': index, 'image': image, 'budget': budget, 'case': case,
                    'mode': 'max' if maximum else 'min', 'boundary_size': k,
                    'original_control': control, 'prefix_passages': spent, 'free_inputs': 11 - k,
                    'imported_size_bound': lower, 'touch_cap': cap,
                    'cut_row9': cut, 'cut_original': preimages[cut], 'required_crossings': required,
                    'forced_internal_row9': forced_row if internal else None,
                    'forced_internal_original': preimages[forced_row] if internal else None,
                    'forced_internal_gate9': ([7, 8] if maximum else [0, 1]) if internal else None,
                    'required_touches': required + internal}
    return None


def bounded(call, *args):
    def stop(signum, frame):
        raise TimeoutError('45-second per-class stage limit; incomplete work is not an exclusion')
    previous = signal.signal(signal.SIGALRM, stop)
    signal.alarm(45)
    try:
        return call(*args)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


def main():
    assert not sys.flags.optimize, 'Run with assertions enabled'
    args = arguments()
    fixture = json.loads((HERE / 'fixture.json').read_text())
    load_premises(fixture, args)
    expected = json.loads(args.certificate.read_text())
    assert expected['schema'] == 'sorting13-first4-reduction-v1'
    assert expected['fixture_sha256'] == digest(fixture)
    monoids, _ = local_monoids()
    assert expected['local_monoid_sha256'] == digest(monoids)
    root = (tuple(fixture['initial_low']), tuple(fixture['initial_high']), False)
    out = HERE / 'out'
    out.mkdir(exist_ok=True)
    records = []
    start = time.monotonic()
    for index, code, events, orders in fixture['classes']:
        def one():
            local = dict(fixture, class_code=code, parent_effective_words=orders)
            triples = class_triples(local, root)
            assert {GATES[t[1]] for t in triples} == {(4,10)}
            table = completion_table(local, root, monoids, triples)
            boundaries, tails = [], []
            for image, budget, case in table['remaining_completion_pairs']:
                word = prefix_word(local, table, monoids, case)
                boundary = boundary_obstruction(local, table, word, index, image, budget, case)
                if boundary is not None:
                    boundaries.append(boundary)
                else:
                    tails.append(dict(parent_index=index, class_code=code, image=image,
                                      budget=budget, case=case, prefix_B11=word,
                                      rows9=table['images9'][image], rows9_sha256=digest(table['images9'][image])))
            record = {k:v for k,v in summary(index, code, table).items()
                      if k not in ('activity_pair_records', 'after_activity_pairs')}
            record.update(boundary_count=len(boundaries), boundary_sha256=digest(boundaries), remaining_tails=tails)
            return record, boundaries
        record, boundaries = bounded(one)
        record = json.loads(json.dumps(record))
        assert record == expected['classes'][len(records)], ('class certificate mismatch', index)
        (out / f'class{index}.boundary.json').write_text(json.dumps(boundaries, separators=(',',':'))+'\n')
        records.append(record)
        print(json.dumps(dict(parent_index=index, completed_classes=len(records),
                              status='CLASS_REDUCTION_REPRODUCED')), flush=True)
    assert len(records) == 45 and sum(r['effective_orders'] for r in records) == 440190
    report = dict(status='ALL_FIRST4_CLASS_REDUCTIONS_REPRODUCED', classes=45, effective_orders=440190,
                  normalized_prefixes=sum(r['normalized_prefixes'] for r in records),
                  pairs=sum(r['image_budget_pairs'] for r in records),
                  activity=sum(r['prefix_activity_blocked'] for r in records),
                  boundaries=sum(r['boundary_count'] for r in records),
                  tails=sum(len(r['remaining_tails']) for r in records),
                  seconds=time.monotonic()-start, peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (out / 'reduction-producer-checks.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
