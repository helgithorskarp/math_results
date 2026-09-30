"""Independent scalar/inverse-fiber DFS; six-sorting-1, researcher.
No generator import or generator state-set seeds. Compare exact independently
regenerated state sets against the generator only after closure completion.
"""
import hashlib,itertools,json,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
GEN_CACHE=HERE/'scratch/generate/nodes'
OWN_CACHE=HERE/'scratch/verify/nodes'
PAIRS=tuple(itertools.combinations(range(10),2))
LOWER=(0,0,1,3,5,9,12,16,19,25,29,35,39,44)

def scalar(row,word):
    row=list(row)
    high=low=0
    for a,b in word:
        high+=row[a]==1 or row[b]==1
        low+=row[a]==0 or row[b]==0
        row[a],row[b]=min(row[a],row[b]),max(row[a],row[b])
    return row,high,low

def prerequisites(fixture):
    initial={};caps={0:100,1:100,5:100};maximum9_cap=100
    count=0
    for rec in fixture['R137']['prefixes']:
        prefix=rec['prefix26'];image=set()
        for mask in range(8192):
            values=[(mask>>i)&1 for i in range(13)]
            out,high,low=scalar(values,prefix)
            assert out[10:]==sorted(values)[-3:]
            r=sum(v<<i for i,v in enumerate(out[:10]));image.add(r)
            assert scalar(out,fixture['R137']['known19_control'])[0]==sorted(values)
            if r==512:
                maximum9_cap=min(maximum9_cap,44-LOWER[13-mask.bit_count()]-high)
            if mask.bit_count()==12:
                port=out.index(0);assert port in caps
                caps[port]=min(caps[port],5-low)
            if mask.bit_count()==11:
                zeros=sum((v==0)<<i for i,v in enumerate(out[:10]))
                initial[zeros]=max(initial.get(zeros,0),low)
            count+=1
        assert image==set(fixture['R137']['states'])
        assert 256 in image and 512 in image
    assert caps=={0:3,1:2,5:3} and maximum9_cap==1
    initial=tuple(sorted(initial.items()))
    assert initial==tuple(sorted(map(tuple,fixture['initial_two_minimum_profile'])))
    assert sum(2**d for m,d in initial)==208
    return initial,{'original_inputs':count,'two_minimum_profile':initial,'minimum_caps':caps,
                    'maximum9_cap':maximum9_cap,'R_onehot8_and9':True}

def marker_transitions():
    table={}
    for positions in itertools.combinations(range(10),2):
        mask=sum(1<<i for i in positions)
        row=[int(i not in positions) for i in range(10)]
        for gate in PAIRS:
            out,high,deleted=scalar(row,[gate])
            destination=sum((v==0)<<i for i,v in enumerate(out))
            assert destination.bit_count()==2
            table[mask,gate]=destination,deleted
    assert len(table)==2025
    return table

def enumerate_words():
    pairs = tuple(itertools.combinations(range(10), 2))
    rows = tuple(tuple(int(i != p) for i in range(10)) for p in (0, 1, 5))
    words = []

    def visit(values, costs, unary, word):
        occupied = {row.index(0) for row in values}
        if len(occupied) == 1:
            assert occupied == {0}
            if unary == 2 and costs[1] == 2:
                assert len(word) == 4
                words.append(word)
            return
        if len(word) >= 4:
            return
        for a, b in pairs:
            touched = occupied.intersection((a, b))
            if not touched:
                continue
            next_unary = unary + (len(touched) == 1)
            next_costs = tuple(c + (row[a] == 0 or row[b] == 0)
                               for row, c in zip(values, costs))
            if next_unary > 2 or any(c > cap for c, cap in zip(next_costs, (3, 2, 3))):
                continue
            next_rows = []
            for row in values:
                following = list(row)
                following[a], following[b] = min(row[a], row[b]), max(row[a], row[b])
                next_rows.append(tuple(following))
            visit(tuple(next_rows), next_costs, next_unary, word + ((a, b),))

    visit(rows, (0, 0, 0), 0, ())
    assert len(words) == len(set(words))
    return sorted(words)

def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()

def transition(profile, gate, table):
    fibers = {}
    for mask, deletion in profile:
        destination, addition = table[mask, gate]
        fibers.setdefault(destination, []).append(deletion + addition)
    return tuple(sorted((mask, max(values)) for mask, values in fibers.items()))

def occupied(prefix):
    rows = [tuple(int(i != p) for i in range(10)) for p in (0, 1, 5)]
    for gate in prefix:
        rows = [tuple(scalar(row, [gate])[0]) for row in rows]
    return {row.index(0) for row in rows}

def close(prefix, seeds, table, source_hash, bound, deadline):
    name = digest(prefix) + '.json'
    expected_path, own_path = GEN_CACHE / name, OWN_CACHE / name
    if not expected_path.exists():
        return None, {'status': 'awaiting_generator_prefix'}
    from driver import read_node
    expected, generated_states = read_node(expected_path)
    assert expected['seed_sha256'] == digest(sorted(seeds))
    if own_path.exists():
        record, states = read_node(own_path)
        assert record['source_sha256'] == source_hash and record['seed_sha256'] == digest(sorted(seeds))
    else:
        positions = occupied(prefix)
        allowed = tuple(g for g in PAIRS if positions.isdisjoint(g))
        states, stack = set(seeds), list(sorted(seeds))
        processed = edges = maximum_cuts = weight_cuts = 0
        while stack:
            if time.monotonic() >= deadline:
                return None, {'status': 'operational_limit_incomplete', 'reason': 'seconds_limit'}
            used, profile = stack.pop()
            processed += 1
            for gate in allowed:
                edges += 1
                if 9 in gate and (gate != (8, 9) or used):
                    maximum_cuts += 1
                    continue
                following = transition(profile, gate, table)
                if sum(2 ** d for m, d in following) > 512:
                    weight_cuts += 1
                    continue
                candidate = used or 9 in gate, following
                if candidate not in states:
                    if len(states) >= bound:
                        return None, {'status': 'operational_limit_incomplete', 'reason': 'state_limit'}
                    states.add(candidate)
                    stack.append(candidate)
        record = {'prefix': prefix, 'source_sha256': source_hash,
                  'seed_sha256': digest(sorted(seeds)), 'status': 'complete_nongate_closure',
                  'count': len(states), 'processed': processed, 'nongate_edges': edges,
                  'maximum_cuts': maximum_cuts, 'weight_cuts': weight_cuts,
                  'state_sha256': digest(sorted(states))}
        own_path.write_text(json.dumps(dict(record, states=sorted(states)), separators=(',', ':')) + '\n')
    assert len(states) <= bound
    assert states == generated_states, (prefix, 'entry_level_state_set_mismatch')
    for key in ('prefix', 'seed_sha256', 'count', 'processed', 'nongate_edges',
                'maximum_cuts', 'weight_cuts', 'state_sha256'):
        assert json.dumps(record[key]) == json.dumps(expected[key]), (prefix, key)
    return states, record

def check_word(word, initial, table, source_hash, deadline):
    start = time.monotonic()
    seeds, counts, hashes = {(False, initial)}, [], []
    edges = maximum_cuts = weight_cuts = 0
    for index, gate in enumerate(word):
        frontier, record = close(word[:index], seeds, table, source_hash,
                                  50000 - sum(counts), min(start + 45, deadline))
        if frontier is None:
            return {'kernel': word, 'status': record['status'], 'detail': record}
        counts.append(len(frontier))
        hashes.append(record['state_sha256'])
        edges += record['nongate_edges'] + len(frontier)
        maximum_cuts += record['maximum_cuts']
        weight_cuts += record['weight_cuts']
        seeds = set()
        for used, profile in frontier:
            following = transition(profile, gate, table)
            if sum(2 ** d for m, d in following) > 512:
                weight_cuts += 1
            else:
                seeds.add((used, following))
        if not seeds:
            counts += [0] * (len(word) - index)
            break
        if index == len(word) - 1:
            counts.append(len(seeds))
    assert sum(counts) <= 50000
    return {'kernel': word, 'status': 'terminal_found' if seeds else 'complete_empty_selected_kernel_closure',
            'phase_counts': counts, 'states': sum(counts), 'edges': edges,
            'maximum_cuts': maximum_cuts, 'weight_cuts': weight_cuts,
            'prefix_state_hashes': hashes}

def main():
    from driver import run
    fixture=json.loads((HERE/'fixture.json').read_text())
    initial,controls=prerequisites(fixture)
    table=marker_transitions()
    all_words=enumerate_words()
    forbidden=[w for w in all_words if any(9 in g for g in w)]
    assert len(forbidden)==288 and all(all(g!=(8,9) for g in w) for w in forbidden)
    words=[w for w in all_words if w not in forbidden]
    def front_weight(word):
        profile=initial
        for gate in word:profile=transition(profile,gate,table)
        return sum(2**d for mask,d in profile)
    words.sort(key=lambda word:(front_weight(word),word))
    controls['scalar_two_zero_transitions']=len(table)
    run('verify',words,all_words,
        lambda word,source,deadline:check_word(word,initial,table,source,deadline),controls,OWN_CACHE)
if __name__=='__main__':main()
