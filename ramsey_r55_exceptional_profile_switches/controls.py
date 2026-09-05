#!/usr/bin/env python3
"""Exhaustive small controls and entry-level independent seed/endpoint checks."""
import argparse
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def module(name):
    spec = importlib.util.spec_from_file_location(name,HERE/(name+'.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def literal_profiles(adj):
    universe = set(range(len(adj)))
    return tuple((sum(v in adj[u] for u,v in combinations(sorted(adj[e]),2)),
                  sum(v not in adj[u] for u,v in combinations(sorted(universe-adj[e]-{e}),2)))
                 for e in range(3))


def signatures_control(search):
    totals = Counter()
    for sig in product(range(8),repeat=4):
        preserved = search.preserves(sig)
        q1 = Counter(tuple(sorted((sig[u],sig[v]))) for u,v in ((0,2),(1,3)))
        q2 = Counter(tuple(sorted((sig[u],sig[v]))) for u,v in ((0,3),(1,2)))
        old = sig[0]==sig[1] or sig[2]==sig[3]
        require((q1==q2)==old,'quota equality characterization')
        totals['signature_assignments'] += 1
        totals['profile_preserving_signatures'] += int(preserved)
        totals['quota_preserving_signatures'] += int(old)
        totals['broader_only_signatures'] += int(preserved and not old)
        for free in range(32):
            adj = [set() for _ in range(7)]
            def edge(u,v):
                adj[u].add(v)
                adj[v].add(u)
            edge(3,5)
            edge(4,6)
            for v,s in enumerate(sig,start=3):
                for e in range(3):
                    if s >> e & 1:
                        edge(e,v)
            for bit,(u,v) in enumerate(((0,1),(0,2),(1,2),(3,4),(5,6))):
                if free >> bit & 1:
                    edge(u,v)
            before = literal_profiles(adj)
            degrees = list(map(len,adj))
            for u,v in ((3,5),(4,6),(3,6),(4,5)):
                if v in adj[u]:
                    adj[u].remove(v)
                    adj[v].remove(u)
                else:
                    edge(u,v)
            after = literal_profiles(adj)
            require(list(map(len,adj))==degrees,'small switch changed a degree')
            expected = [(((sig[0] >> e & 1)-(sig[1] >> e & 1))*
                         ((sig[3] >> e & 1)-(sig[2] >> e & 1))) for e in range(3)]
            observed = [(x[0]-y[0],x[1]-y[1]) for x,y in zip(after,before)]
            require(observed==[(d,-d) for d in expected],'literal two-color root delta discrepancy')
            require((before==after)==preserved,'signature criterion discrepancy')
            totals['seven_vertex_completions'] += 1
            totals['preserved_completions'] += int(before==after)
    require(totals['signature_assignments']==4096 and totals['profile_preserving_signatures']==1728
            and totals['quota_preserving_signatures']==960 and totals['broader_only_signatures']==768
            and totals['seven_vertex_completions']==131072,'small control coverage')
    return dict(sorted(totals.items()))


def compare_graph(search, verify, parent, checker, rows):
    entries = []
    reference = verify.census(parent,checker,rows,entries)
    listed = list(search.swaps(rows))
    moves = {search.support(move):move for move in listed}
    require(len(listed)==len(moves),'duplicate production switch support')
    require(set(moves)=={entry[0] for entry in entries},'matching vs bitset support set disagreement')
    gate,count = search.dependencies()
    table = gate.lifting_rows(rows)
    before = count.counts(rows)
    blue = count.complement(rows)
    totals = Counter()
    unsafe_example = None
    for support,kind,violation,full_counts,quota_change in entries:
        move = moves[support]
        changed = tuple(gate.flip(rows,move))
        pass4 = gate.lifted(changed,table,move)
        require(pass4==gate.lifted(changed,table,range(43)),'four-row shortcut discrepancy')
        require(pass4==(kind!='lifting_failure'),'bitset vs literal lifting disagreement')
        require(search.quota_preserving(rows,move)==(not quota_change),'quota classification disagreement')
        if gate.lifted(changed,table,move[:2]) and not pass4:
            totals['unsafe_first_pair_gate_false_accepts'] += 1
            if quota_change:
                totals['unsafe_first_pair_gate_false_accepts_quota_changing'] += 1
                if unsafe_example is None:
                    unsafe_example = {'move':move,'signatures':[rows[v]&7 for v in move],
                                      'literal_lifting_violation':violation}
        if pass4:
            require(gate.mixed_after_switch(changed,move)==(kind=='admissible'),'mixed-K5 checker disagreement')
        if kind=='admissible':
            predicted = tuple(x+d for x,d in zip(before,count.k5_change(rows,move,blue)))
            require(predicted==full_counts,'incremental vs full K5 enumeration disagreement')
            totals['full_color_count_comparisons'] += 1
        totals['support_feasibility_comparisons'] += 1
    return {'comparison_counts':dict(sorted(totals.items())),'unsafe_first_pair_example':unsafe_example,
            'independent_census':reference}


def negative_controls(search, verify, parent, checker, seed):
    # Select a genuinely nonpreserving alternating move rather than merely
    # mutating metadata. The literal profile test must observe the change.
    adj = parent.neighbors(seed)
    witness = None
    for a,b,c,d in combinations(range(3,43),4):
        for move in ((a,b,c,d),(a,c,b,d),(a,d,b,c),(a,b,d,c),(a,c,d,b),(a,d,c,b)):
            x,y,z,w = move
            if z in adj[x] and w in adj[y] and w not in adj[x] and z not in adj[y]:
                if not search.preserves([seed[v]&7 for v in move]):
                    witness = move
                    break
        if witness is not None:
            break
    require(witness is not None,'negative-control coverage')
    changed = parent.changed_graph(adj,search.support(witness))
    require(checker.local_profiles(seed)[1][:3]!=checker.local_profiles(verify.encode(changed))[1][:3],
            'nonpreserving switch went undetected')
    malformed = list(seed)
    malformed[3] ^= 1 << 3
    try:
        checker.decode(verify.document(malformed))
    except ValueError:
        pass
    else:
        raise ValueError('loop accepted')
    return {'nonpreserving_move':witness,'literal_profile_change_detected':True,'loop_rejected':True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph',type=Path,default=HERE/'GRAPH.json')
    parser.add_argument('--report',type=Path,required=True)
    args = parser.parse_args()
    start = time.monotonic()
    search,verify = module('search'),module('verify')
    require(hashlib.sha256(search.SEED.read_bytes()).hexdigest()==search.SEED_SHA,'seed pin')
    parent = verify.load_parent()
    checker = parent.load_audit()
    seed = checker.decode(json.loads(search.SEED.read_text()))
    endpoint = checker.decode(json.loads(args.graph.read_text()))
    report = {'small_exhaustive_control':signatures_control(search),
              'negative_controls':negative_controls(search,verify,parent,checker,seed),
              'seed_entry_comparison':compare_graph(search,verify,parent,checker,seed),
              'endpoint_entry_comparison':compare_graph(search,verify,parent,checker,endpoint)}
    args.report.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS','small_control':report['small_exhaustive_control'],
                      'elapsed_seconds':round(time.monotonic()-start,6),
                      'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__=='__main__':
    main()
