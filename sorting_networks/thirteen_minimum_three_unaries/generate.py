"""Bitmask BFS with exact event-prefix reuse; six-sorting-1, researcher."""
from collections import deque
import hashlib,itertools,json,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
CACHE=HERE/'scratch/generate/nodes'
PAIRS=tuple(itertools.combinations(range(10),2))
CAPS=(3,2,3)
INITIAL=tuple(sorted(map(tuple,json.loads((HERE/'fixture.json').read_text())['initial_two_minimum_profile'])))
def weight(profile):return sum(1<<d for mask,d in profile)

def enumerate_kernels():
    words=[]
    def visit(p,q,u,word):
        if len(set(p))==1:
            assert p==(0,0,0)
            if u==2 and q[1]==2:
                assert len(word)==4;words.append(word)
            return
        if len(word)==4:return
        for gate in PAIRS:
            occupied=set(p).intersection(gate)
            if not occupied:continue
            new_u=u+(len(occupied)==1)
            new_q=tuple(c+(position in gate) for position,c in zip(p,q))
            if new_u>2 or any(c>cap for c,cap in zip(new_q,CAPS)):continue
            new_p=tuple(gate[0] if position in gate else position for position in p)
            visit(new_p,new_q,new_u,word+(gate,))
    visit((0,1,5),(0,0,0),0,())
    assert len(words)==len(set(words))==1138
    return sorted(words)

def step(profile,gate):
    a,b=gate;A,B=1<<a,1<<b;result={}
    for mask,d in profile:
        new_d=d+bool(mask&(A|B))
        if mask&B and not mask&A:mask^=A|B
        result[mask]=max(result.get(mask,new_d),new_d)
    return tuple(sorted(result.items()))

def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()

def freeze_state(raw):
    return bool(raw[0]), tuple(map(tuple, raw[1]))

def roots(prefix):
    current = (0, 1, 5)
    for gate in prefix:
        current = tuple(gate[0] if p in gate else p for p in current)
    return set(current)

def nongate_closure(prefix, seeds, source_hash, state_limit, deadline):
    seed_hash = digest(sorted(seeds))
    path = CACHE / (digest(prefix) + '.json')
    if path.exists():
        from driver import read_node
        cached, states = read_node(path)
        assert cached['source_sha256'] == source_hash and cached['seed_sha256'] == seed_hash
        if len(states) > state_limit:
            return None, {'status': 'operational_limit_incomplete', 'reason': 'cached_prefix_exceeds_class_state_limit'}
        return states, cached
    start = time.monotonic()
    occupied = roots(prefix)
    allowed = tuple(g for g in PAIRS if occupied.isdisjoint(g))
    states, queue = set(seeds), deque(sorted(seeds))
    if len(states) > state_limit:
        return None, {'status': 'operational_limit_incomplete', 'reason': 'seed_count_exceeds_class_state_limit'}
    edges = maximum_cuts = weight_cuts = processed = 0
    while queue:
        if time.monotonic() >= deadline:
            return None, {'status': 'operational_limit_incomplete', 'reason': 'class_seconds_limit'}
        maximum_used, profile = queue.popleft()
        processed += 1
        for gate in allowed:
            edges += 1
            if 9 in gate and (gate != (8, 9) or maximum_used):
                maximum_cuts += 1
                continue
            following = step(profile, gate)
            if weight(following) > 512:
                weight_cuts += 1
                continue
            state = maximum_used or 9 in gate, following
            if state not in states:
                if len(states) >= state_limit:
                    return None, {'status': 'operational_limit_incomplete', 'reason': 'class_state_limit'}
                states.add(state)
                queue.append(state)
    record = {'prefix': prefix, 'source_sha256': source_hash, 'seed_sha256': seed_hash,
              'status': 'complete_nongate_closure', 'count': len(states), 'processed': processed,
              'nongate_edges': edges, 'maximum_cuts': maximum_cuts, 'weight_cuts': weight_cuts,
              'state_sha256': digest(sorted(states)), 'seconds': time.monotonic() - start}
    path.write_text(json.dumps(dict(record, states=sorted(states)), separators=(',', ':')) + '\n')
    return states, record

def explore(word, source_hash, deadline):
    start = time.monotonic()
    seeds = {(False, INITIAL)}
    counts, block_hashes, records = [], [], []
    edges = maximum_cuts = weight_cuts = 0
    for index, gate in enumerate(word):
        frontier, record = nongate_closure(word[:index], seeds, source_hash,
                                           50000 - sum(counts), min(start + 45, deadline))
        if frontier is None:
            return {'kernel': word, 'status': 'operational_limit_incomplete', 'detail': record,
                    'phase_counts': counts, 'seconds': time.monotonic() - start}
        records.append(record)
        counts.append(len(frontier))
        block_hashes.append(record['state_sha256'])
        edges += record['nongate_edges'] + len(frontier)
        maximum_cuts += record['maximum_cuts']
        weight_cuts += record['weight_cuts']
        seeds = set()
        for maximum_used, profile in frontier:
            following = step(profile, gate)
            if weight(following) > 512:
                weight_cuts += 1
            else:
                seeds.add((maximum_used, following))
        if not seeds:
            counts += [0] * (len(word) - index)
            break
        if index == len(word) - 1:
            counts.append(len(seeds))
    states = sum(counts)
    if states > 50000:
        return {'kernel': word, 'status': 'operational_limit_incomplete', 'reason': 'terminal_class_state_limit'}
    status = 'terminal_found' if seeds else 'complete_empty_selected_kernel_closure'
    result = {'kernel': word, 'status': status, 'phase_counts': counts,
              'states': states, 'edges': edges, 'maximum_cuts': maximum_cuts,
              'weight_cuts': weight_cuts, 'prefix_state_hashes': block_hashes,
              'seconds': time.monotonic() - start}
    return result

def main():
    from driver import run
    all_words=enumerate_kernels()
    forbidden=[w for w in all_words if any(9 in gate for gate in w)]
    assert len(forbidden)==288 and all(all(g!=(8,9) for g in w) for w in forbidden)
    words=[w for w in all_words if w not in forbidden]
    def front_weight(word):
        profile=INITIAL
        for gate in word:profile=step(profile,gate)
        return weight(profile)
    words.sort(key=lambda word:(front_weight(word),word))
    assert weight(INITIAL)==208
    run('generate',words,all_words,explore,{'initial_weight':208,'forbidden9_words':288},CACHE)
if __name__=='__main__':main()
