"""B11 pruning-saturation generator; six-sorting-2, researcher.

The forward profile kernel below adapts six-sorting-1's source
65a48340a24e9a4d8b294f590e12d4328a72808f, credited in README.md.

Python3.11+ standard library, integer arithmetic, no operational truncation.
Import this file to obtain initial_state(), successor(), and closure().
The relaxation is necessary for the specified full44 branch, not sufficient.
"""
from collections import defaultdict, deque
import argparse
import resource
import time
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATES = tuple(itertools.combinations(range(11), 2))


def marker_profile(prefix, maximum):
    profile = {}
    for original in itertools.combinations(range(13), 2):
        marks = (1 << original[0]) | (1 << original[1])
        depth = 0
        for a, b in prefix:
            A, B = 1 << a, 1 << b
            depth += bool(marks & (A | B))
            if maximum:
                if marks & A and not marks & B: marks ^= A | B
            elif marks & B and not marks & A: marks ^= A | B
        profile[marks] = max(depth, profile.get(marks, -1))
    return tuple(sorted(profile.items()))


def reduce_profile(profile, maximum):
    weights = [0] * 11
    held = 12 if maximum else 0
    for marks, depth in profile:
        assert marks & (1 << held) and marks.bit_count() == 2
        partner = (marks ^ (1 << held)).bit_length() - 2
        assert 0 <= partner < 11 and depth >= 5
        weights[partner] = 2 ** (depth - 5)
    return tuple(weights)


def initial_state(fixture):
    profiles = [marker_profile(fixture['prefix22'], maximum) for maximum in (False, True)]
    return (*[reduce_profile(f, bool(i)) for i, f in enumerate(profiles)], False)


def move(weights, gate, maximum):
    a, b = gate
    result = list(weights)
    merged = 2 * max(weights[a], weights[b])
    result[a], result[b] = (0, merged) if maximum else (merged, 0)
    return tuple(result)


def successor(state, gate):
    low, high, touched = state
    if not touched and gate[1] == 10 and gate[0] in (0, 7, 9): return None
    low_out, high_out = move(low, gate, False), move(high, gate, True)
    if sum(low_out) > 16 or sum(high_out) > 16: return None
    return low_out, high_out, touched or gate[1] == 10


def terminal(state):
    low, high, touched = state
    return touched and low == (16,) + (0,) * 10 and high == (0,) * 10 + (16,)


def potential(state):
    low, high, _ = state
    return 2 * sum(bool(w) for w in low + high) + 32 - sum(low + high)


def closure(initial):
    seen = {initial: ()}
    queue = deque([initial])
    edges = set()
    while queue:
        state = queue.popleft()
        for gate in GATES:
            dest = successor(state, gate)
            if dest is None: continue
            edges.add((state, gate, dest))
            if dest != state: assert potential(dest) < potential(state)
            if dest not in seen:
                seen[dest] = seen[state] + (gate,)
                queue.append(dest)
    return seen, edges


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode('ascii')).hexdigest()


def boolean(row, word):
    for a, b in word:
        if row >> a & 1 and not row >> b & 1:
            row ^= (1 << a) | (1 << b)
    return row


def marker(original, word, maximum):
    row = sum(1 << p for p in original)
    D = 0
    for a, b in word:
        D += bool(row & ((1 << a) | (1 << b)))
        if (row >> a & 1 and not row >> b & 1) if maximum else (row >> b & 1 and not row >> a & 1):
            row ^= (1 << a) | (1 << b)
    return row, D


def main():
    assert __debug__, 'Assertions are part of this exact check'
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export',type=Path,help='Private complete states/edges catalogue')
    parser.add_argument('--write-certificate',action='store_true',help='Explicit initial generation only')
    args=parser.parse_args()
    started=time.monotonic()
    fixture=json.loads((HERE/'fixture.json').read_text())
    P=fixture['prefix22']
    initial = initial_state(fixture)
    seen, edges = closure(initial)
    outgoing = defaultdict(list)
    for s, g, d in edges:
        if s != d:
            outgoing[s].append((g,d))
    order = sorted(seen,key=potential,reverse=True)
    tags = []
    for maximum in (False,True):
        weights = initial[int(maximum)]
        for p,w in enumerate(weights):
            if not w:continue
            D = w.bit_length()-1+5
            reached = {s:set() for s in seen}
            reached[initial].add((p,D,0))
            for s in order:
                for g,d in outgoing[s]:
                    a,b=g
                    for pos,depth,split in reached[s]:
                        new_pos = b if maximum and pos==a else a if not maximum and pos==b else pos
                        hit = int(pos in g)
                        new_split = split
                        if not s[2] and d[2]:new_split=1 if s[0][a] else 2
                        reached[d].add((new_pos,depth+hit,new_split))
            tag_terminal = sorted({x for s in seen if terminal(s) for x in reached[s]})
            if maximum or p!=10:
                assert tag_terminal == [(10 if maximum else 0,9,1),(10 if maximum else 0,9,2)]
            else:assert tag_terminal==[(0,8,1),(0,9,2)]
            tags.append(dict(mode='max' if maximum else 'min',partner=p,prefix_D=D,terminal=tag_terminal))
    projected = {x:(boolean(x,P)>>1)&2047 for x in range(8192)}
    assert sorted(set(projected.values()))==fixture['B11_states']
    assert all((boolean(x,P)&1)==int(x==8191) and ((boolean(x,P)>>12)&1)==int(x!=0) for x in range(8192))
    families=[]
    for maximum in (False,True):
        profile = {}
        originals = defaultdict(list)
        for pair in itertools.combinations(range(13),2):
            row,D=marker(pair,P,maximum)
            held=12 if maximum else 0
            assert row>>held&1
            p=(row^(1<<held)).bit_length()-2
            if D>profile.get(p,-1):profile[p]=D;originals[p]=[pair]
            elif D==profile[p]:originals[p].append(pair)
        for p,D in sorted(profile.items()):
            domains=[]
            for pair in originals[p]:
                mask=sum(1<<q for q in pair)
                domain=frozenset(v for x,v in projected.items() if (x&mask)==(mask if maximum else 0))
                domains.append((pair,domain))
            distinct = sorted(set(domain for pair,domain in domains),key=lambda d:(len(d),sorted(d)))
            minimal=[]
            for domain in distinct:
                if not any(smaller<=domain for smaller in minimal):minimal.append(domain)
            representatives=[next(pair for pair,Dm in domains if Dm==domain) for domain in minimal]
            families.append(dict(mode='max' if maximum else 'min',partner=p,prefix_D=D,
                                 strongest_witnesses=len(domains),distinct_domains=len(distinct),
                                 inclusion_minimal_domains=len(minimal),domain_sizes=list(map(len,minimal)),
                                 original_representatives=representatives,
                                 final_D=9 if maximum or p!=10 else '8 if first10 min-binary; 9 if min-unary',
                                 domains=[sorted(d) for d in minimal]))

    assert len(seen)==2214 and len(edges)==22536
    assert sum(f['strongest_witnesses'] for f in families)==126
    assert sum(f['inclusion_minimal_domains'] for f in families)==13
    min0=next(f for f in families if f['mode']=='min' and f['partner']==0)
    small=min0['domains'][0]
    assert min0['original_representatives'][0]==(1,5) and len(small)==101
    assert all(not (r&1) and ((r>>4)&1)<=((r>>10)&1) for r in small)
    required=((1,4),(2,4),(3,4))
    invariant_transitions=0
    for row in range(2048):
        if row&1 or ((row>>4)&1)>((row>>10)&1):continue
        for gate in itertools.combinations(range(10),2):
            if gate in required:continue
            out=boolean(row,[gate])
            assert not out&1 and ((out>>4)&1)<=((out>>10)&1)
            invariant_transitions+=1
    assert invariant_transitions==32256
    initial_gates=[g for g in GATES if successor(initial,g) is not None]
    failures=[]
    for gate in initial_gates:
        failed=[]
        for f in families:
            if f['final_D']!=9 or f['partner'] in gate:continue
            for domain in f['domains']:
                if not any(boolean(r,[gate])!=r for r in domain):
                    failed.append([f['mode'],f['partner'],len(domain)])
        if failed:failures.append([gate,failed])
    assert failures==[[(4,10),[['min',0,101]]]] and len(initial_gates)==18
    pre_edges=[(s,g,d) for s,g,d in edges if not s[2] and not d[2]]
    empty4=[e for e in pre_edges if e[0][0][4]==0]
    preparatory=[e for e in pre_edges if e[1] in required]
    assert all(e[2][0][4]==0 for e in empty4+preparatory)
    first4=[(s,g,d) for s,g,d in edges if not s[2] and d[2] and g==(4,10)]
    assert len(empty4)==603 and len(preparatory)==184
    assert sum(bool(s[0][4]) for s,g,d in first4)==76
    assert sum(not s[0][4] for s,g,d in first4)==100
    word=fixture['B11_known23_control']
    assert len(word)==23
    assert all(boolean(r,word)==((1<<r.bit_count())-1)<<(11-r.bit_count())
               for r in fixture['B11_states'])
    lifted=fixture['prefix22']+[[a+1,b+1] for a,b in word]
    assert len(lifted)==45
    assert all(boolean(r,lifted)==((1<<r.bit_count())-1)<<(13-r.bit_count()) for r in range(8192))
    # A duplicated first comparator gives a valid larger sorter with an
    # inactive retained comparator; saturation must not be assumed there.
    duplicate=[word[0]]+word
    duplicate_lift=fixture['prefix22']+[[a+1,b+1] for a,b in duplicate]
    assert all(boolean(r,duplicate_lift)==((1<<r.bit_count())-1)<<(13-r.bit_count()) for r in range(8192))
    assert 0 not in word[0] and not any(boolean(boolean(r,[word[0]]),[word[0]])!=boolean(r,[word[0]]) for r in small)
    report=dict(schema='sorting13-B11-pruning-activity-v1',agent='six-sorting-2',role='researcher',
                profile_states=len(seen),profile_edges=len(edges),initial_state=initial,
                state_sha256=digest(sorted(seen)),edge_sha256=digest(sorted(edges)),
                terminal_tag_results=tags,families=families,strongest_families=126,
                guaranteed_saturated_families=125,conditionally_saturated_families=1,
                class_labelled_distinct_domains=sum(f['distinct_domains'] for f in families),
                minimal_domains=13,mandatory_domains=12,conditional_domains=1,
                first4_preparation=dict(slice_original_pair=[1,5],slice_size=101,
                    required_prior_gates=required,invariant_transitions=invariant_transitions,
                    profile_allowed_initial_gates=initial_gates,
                    activity_forbidden_initial_gates=failures,
                    prephase_empty4_edges=len(empty4),prephase_preparation_edges=len(preparatory),
                    first4_binary_edges_excluded=76,first4_unary_edges_remaining_relaxation=100,
                    minimum_unary_if_first_gate_on_10_is_4_10=True),
                controls=dict(B11_known23_rows=158,lifted45_original_rows=8192,
                    duplicated46_original_rows=8192,duplicated_first_gate=word[0],
                    duplicated_gate_is_retained_and_inactive_in_min0_slice=True),
                scope='Necessary arbitrary-depth B11 C22 conditions, not a nonexistence certificate')
    report=json.loads(json.dumps(report))
    path=HERE/'certificate.json'
    if args.write_certificate:
        assert not path.exists(),'Refuse to replace an existing certificate'
        path.write_text(json.dumps(report,indent=2)+'\n')
    else:
        assert report==json.loads(path.read_text()),'Certificate mismatch'
    if args.export:
        args.export.parent.mkdir(parents=True,exist_ok=True)
        args.export.write_text(json.dumps(dict(states=sorted(seen),edges=sorted(edges)),separators=(',',':'))+'\n')
    print(json.dumps(dict(status='GENERATOR_CHECKS_PASSED',profile_states=len(seen),profile_edges=len(edges),
        guaranteed_saturated_families=125,mandatory_domains=12,conditional_domains=1,
        seconds=time.monotonic()-started,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))


if __name__=='__main__':main()
