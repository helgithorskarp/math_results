#!/usr/bin/env python3
"""Literal graph and four-vertex-matching audit; imports no search code."""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent/'ramsey_r55_triple_graph_realization'
INPUT_SHA = 'a57fc26ea50196d82537220cf057c659860f9842dd35351d33445781f019eae5'
AUDIT_SHA = '154358fe08d7c07f2818aa4105ce127d3767a4af736362d55c7ba79ed683c207'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_audit():
    path = PARENT/'verify.py'
    require(hashlib.sha256(path.read_bytes()).hexdigest() == AUDIT_SHA,'parent graph checker changed')
    spec = importlib.util.spec_from_file_location('literal_graph_checker',path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def neighbors(rows):
    return [{v for v in range(len(rows)) if row >> v & 1} for row in rows]


def triangles(adj):
    tt = [0]*len(adj)
    for a,b,c in combinations(range(len(adj)),3):
        if b in adj[a] and c in adj[a] and c in adj[b]:
            for u in (a,b,c):
                tt[u] += 1
    return tt


def defect(tt, signatures):
    return sum(max(0,t-100,101-len(signatures[v])-t) for v,t in enumerate(tt) if v>=3)


def quotas(adj, signatures):
    return Counter(tuple(sorted((tuple(signatures[a]),tuple(signatures[b]))))
                   for a,b in combinations(range(3,43),2) if b in adj[a])


@lru_cache(None)
def upper(a,b):
    if min(a,b) == 1:
        return 1
    left,right = upper(a-1,b),upper(a,b-1)
    return left+right-int(left%2 == right%2 == 0)


def conditions(adj):
    """Unmerged literal root conditions, retaining named roots and colors."""
    result = []
    for word in product(range(3),repeat=3):
        A = frozenset(u for u,w in enumerate(word) if w == 1)
        B = frozenset(u for u,w in enumerate(word) if w == 2)
        if not A|B or any(b not in adj[a] for a,b in combinations(sorted(A),2)) or any(b in adj[a] for a,b in combinations(sorted(B),2)):
            continue
        S = frozenset(v for v in range(43) if v not in A|B and A<=adj[v] and not B&adj[v])
        for u in range(43):
            if u in A|B:
                continue
            if A<=adj[u]:
                result.append((u,True,S-{u},upper(4-len(A),5-len(B))-1,tuple(sorted(A)),tuple(sorted(B))))
            if not B&adj[u]:
                result.append((u,False,S-{u},upper(5-len(A),4-len(B))-1,tuple(sorted(A)),tuple(sorted(B))))
    return result


def lifting_failure(adj, rows):
    for u,red,S,cap,A,B in rows:
        actual = len(S&adj[u]) if red else len(S-adj[u])
        if actual > cap:
            return [u,int(red),list(A),list(B),actual,cap]
    return None


def mixed_failure(adj, support=None):
    if support is None:
        # Full pointed K4 enumeration, not an incremental check.
        for root in range(3):
            for red in (True,False):
                side = adj[root] if red else set(range(43))-adj[root]-{root}
                for four in combinations(sorted(side),4):
                    if all((v in adj[u]) == red for u,v in combinations(four,2)):
                        return [int(red),sorted((root,)+four)]
    else:
        # A new mixed K5 must contain a changed central edge. Literal triples
        # in its same-color common neighborhood give a five-set certificate.
        for u,v in support:
            red = v in adj[u]
            common = [w for w in range(43) if w not in (u,v)
                      and (w in adj[u]) == red and (w in adj[v]) == red]
            for triple in combinations(common,3):
                if min(triple) >= 3:
                    continue
                if all((b in adj[a]) == red for a,b in combinations(triple,2)):
                    five = tuple(sorted((u,v)+triple))
                    require(all((b in adj[a]) == red for a,b in combinations(five,2)), 'invalid five-set witness')
                    return [int(red),list(five)]
    return None


def matching_supports(adj, signatures):
    """All central four-edge degree/partition-quota-preserving edits."""
    for a,b,c,d in combinations(range(3,43),4):
        matchings = (((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c)))
        for first,second in combinations(matchings,2):
            colors1 = {v in adj[u] for u,v in first}
            colors2 = {v in adj[u] for u,v in second}
            if len(colors1) != 1 or len(colors2) != 1 or colors1 == colors2:
                continue
            q1 = Counter(tuple(sorted((tuple(signatures[u]),tuple(signatures[v])))) for u,v in first)
            q2 = Counter(tuple(sorted((tuple(signatures[u]),tuple(signatures[v])))) for u,v in second)
            if q1 == q2:
                yield tuple(sorted(first+second))


def changed_graph(adj, support):
    new = list(adj)
    for u in {x for e in support for x in e}:
        new[u] = set(adj[u])
    for u,v in support:
        if v in new[u]:
            new[u].remove(v)
            new[v].remove(u)
        else:
            new[u].add(v)
            new[v].add(u)
    return new


def triangle_change_literal(adj, new, support):
    affected = {tuple(sorted((u,v,w))) for u,v in support for w in range(len(adj)) if w not in (u,v)}
    delta = [0]*len(adj)
    for triple in affected:
        change = int(all(v in new[u] for u,v in combinations(triple,2)))-int(all(v in adj[u] for u,v in combinations(triple,2)))
        for u in triple:
            delta[u] += change
    return delta


def census(adj, signatures):
    tt = triangles(adj)
    base = defect(tt,signatures)
    lifted = conditions(adj)
    require(len(lifted) == 884,'root-inequality coverage')
    summary = Counter()
    histogram = Counter()
    support_digest = hashlib.sha256()
    entries_digest = hashlib.sha256()
    neutral = []
    for support in sorted(matching_supports(adj,signatures)):
        support_digest.update((json.dumps(support,separators=(',',':'))+'\n').encode())
        summary['all_switches'] += 1
        new = changed_graph(adj,support)
        delta = triangle_change_literal(adj,new,support)
        next_score = defect([t+d for t,d in zip(tt,delta)],signatures)
        change = next_score-base
        summary['decreasing' if change<0 else 'nondecreasing'] += 1
        violation = lifting_failure(new,lifted)
        if violation is not None:
            kind = 'lift_failure'
        else:
            violation = mixed_failure(new,support)
            kind = 'mixed_failure' if violation is not None else 'admissible'
        summary[kind] += 1
        if change < 0:
            summary['decreasing_'+kind] += 1
        if kind == 'admissible':
            require(change >= 0,'strictly improving admissible switch found')
            histogram[change] += 1
            if change == 0:
                neutral.append([list(e) for e in support])
        entries_digest.update((json.dumps([support,change,kind,violation],separators=(',',':'))+'\n').encode())
    return {'counts':dict(sorted(summary.items())),
            'admissible_score_change_histogram':{str(k):v for k,v in sorted(histogram.items())},
            'neutral_switch_supports':neutral,
            'canonical_supports_sha256':support_digest.hexdigest(),
            'canonical_classification_sha256':entries_digest.hexdigest()}


def check_path(input_rows, expected_rows, records):
    adj = neighbors(input_rows)
    signatures = [tuple(sorted(row&{0,1,2})) for row in adj]
    initial_quotas = quotas(adj,signatures)
    initial_degrees = list(map(len,adj))
    root_conditions = conditions(adj)
    initial_exceptional = triangles(adj)[:3]
    scores = [defect(triangles(adj),signatures)]
    moves = []
    for step in records['steps']:
        move = step['move']
        if move is None:
            require(step is records['steps'][-1],'nonterminal absent move')
            continue
        require(len(move)==4 and len(set(move))==4 and all(type(v) is int and 3<=v<43 for v in move),'move domain')
        a,b,c,d = move
        require(signatures[a] == signatures[b],'different signature cells')
        require(c in adj[a] and d in adj[b] and d not in adj[a] and c not in adj[b],'alternating switch pattern')
        support = tuple(sorted(tuple(sorted(e)) for e in ((a,c),(b,d),(a,d),(b,c))))
        adj = changed_graph(adj,support)
        tt = triangles(adj)
        require(list(map(len,adj)) == initial_degrees,'degree changed')
        require(quotas(adj,signatures) == initial_quotas,'cell edge quota changed')
        require(tt[:3] == initial_exceptional,'exceptional local total changed')
        require(lifting_failure(adj,root_conditions) is None,'path violates a pointwise lift')
        require(mixed_failure(adj) is None,'path creates a mixed K5')
        current = defect(tt,signatures)
        require(step['before_score']==scores[-1] and current==step['after_score'] and current<scores[-1],'invalid strict descent score')
        moves.append(move)
        scores.append(current)
    reconstructed = [sum(1 << v for v in row) for row in adj]
    require(reconstructed == list(expected_rows),'path endpoint mismatch')
    require(records['initial_score']==scores[0] and records['final_score']==scores[-1],'path score endpoints')
    return {'moves':moves,'scores':scores,'all_path_invariants_verified':True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph',type=Path,default=HERE/'GRAPH.json')
    parser.add_argument('--path',type=Path,default=HERE/'PATH.json')
    parser.add_argument('--report',type=Path,required=True)
    args = parser.parse_args()
    original = (PARENT/'GRAPH.json').read_bytes()
    require(hashlib.sha256(original).hexdigest() == INPUT_SHA,'input provenance')
    checker = load_audit()
    input_rows = checker.decode(json.loads(original))
    document = json.loads(args.graph.read_text())
    rows = checker.decode(document)
    path = check_path(input_rows,rows,json.loads(args.path.read_text()))
    # Entire endpoint audit includes all962598 literal five-sets and an
    # independently implemented recursive bitset clique enumeration.
    endpoint = checker.inspect(document)
    adj = neighbors(rows)
    signatures = [tuple(sorted(row&{0,1,2})) for row in adj]
    complete = census(adj,signatures)
    report = {'graph_sha256':hashlib.sha256(args.graph.read_bytes()).hexdigest(),
              'input_sha256':INPUT_SHA,'path':path,'endpoint':endpoint,'complete_one_switch_census':complete,
              'scope':'No strictly improving four-edge central degree/quota-preserving edit retains all mixed-K5 and pointwise conditions; not a Ramsey graph.'}
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'scores':path['scores'],'census':complete,'central_red_K5':endpoint['central_red_K5'],
                      'central_blue_K5':endpoint['central_blue_K5'],
                      'central_cap_failures':len(endpoint['central_vertices_failing_hard_local_caps'])},sort_keys=True))


if __name__ == '__main__':
    main()
