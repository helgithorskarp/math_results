#!/usr/bin/env python3
"""Exhaust all seven-vertex alternating-switch completions against literal K5s."""
import argparse
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import search
import verify


def literal_counts(rows):
    counts = [0,0]
    for five in combinations(range(len(rows)),5):
        first = rows[five[0]] >> five[1] & 1
        if all((rows[u] >> v & 1)==first for u,v in combinations(five,2)):
            counts[0 if first else 1] += 1
    return tuple(counts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report',type=Path,required=True)
    args = parser.parse_args()
    move = (0,1,2,3)
    fixed = {(0,2):1,(1,3):1,(0,3):0,(1,2):0}
    free = [e for e in combinations(range(7),2) if e not in fixed]
    cases = nonzero = 0
    delta_histogram = {}
    for mask in range(1 << len(free)):
        rows = [0]*7
        colors = dict(fixed)
        colors.update((e,mask >> bit & 1) for bit,e in enumerate(free))
        for (u,v),red in colors.items():
            if red:
                rows[u] |= 1 << v
                rows[v] |= 1 << u
        changed = list(rows)
        for u,v in fixed:
            changed[u] ^= 1 << v
            changed[v] ^= 1 << u
        before = literal_counts(rows)
        after = literal_counts(changed)
        literal = tuple(y-x for x,y in zip(before,after))
        predicted = search.k5_change(rows,move)
        if literal!=predicted:
            raise ValueError('eight-triangle identity disagrees with five-set definition')
        cases += 1
        nonzero += int(any(literal))
        key = ','.join(map(str,literal))
        delta_histogram[key] = delta_histogram.get(key,0)+1
    if not nonzero:
        raise ValueError('vacuous K5 update control')
    # On fewer than seven vertices a switched K5 cannot occur: three vertices
    # of the alternating C4 are never monochromatic, leaving fewer than three outside.
    small = []
    for n in (4,5,6):
        free_small = [e for e in combinations(range(n),2) if e not in fixed]
        for mask in range(1 << len(free_small)):
            rows = [0]*n
            for (u,v),red in list(fixed.items())+[(e,mask >> bit & 1) for bit,e in enumerate(free_small)]:
                if red:
                    rows[u] |= 1 << v
                    rows[v] |= 1 << u
            if search.k5_change(rows,move)!=(0,0):
                raise ValueError('small-order zero control')
        small.append({'order':n,'completions':1 << len(free_small),'all_updates_zero':True})
    rejected = []
    for name,rows,wrong in (
        ('nonalternating',[0]*7,move),
        ('repeated_vertex',[0]*7,(0,0,2,3)),
    ):
        try:
            search.k5_change(rows,wrong)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('invalid switch accepted')
    # Complete entry-level comparison on the actual 43-vertex endpoint.
    parent = verify.load_parent()
    checker = parent.load_audit()
    endpoint = checker.decode(json.loads((verify.HERE/'GRAPH.json').read_text()))
    expected = json.loads((verify.HERE/'report.json').read_text())['complete_one_switch_census']
    if hashlib.sha256(search.SOURCE.read_bytes()).hexdigest()!=search.SOURCE_SHA:
        raise ValueError('gate source changed')
    spec = importlib.util.spec_from_file_location('fast_endpoint_gates',search.SOURCE)
    fast = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fast)
    adj = parent.neighbors(endpoint)
    signatures = [tuple(sorted(row&{0,1,2})) for row in adj]
    literal_supports = set(parent.matching_supports(adj,signatures))
    table = fast.lifting_rows(endpoint)
    conditions = parent.conditions(adj)
    base = literal_counts(endpoint)
    entries = []
    for move in fast.swaps(endpoint):
        a,b,c,d = move
        support = tuple(sorted(tuple(sorted(e)) for e in ((a,c),(b,d),(a,d),(b,c))))
        changed = parent.changed_graph(adj,support)
        rr = tuple(fast.flip(endpoint,move))
        violation = parent.lifting_failure(changed,conditions)
        if bool(violation is None)!=fast.lifted(rr,table,move[:2]):
            raise ValueError('pointwise predicate disagreement')
        kind = 'lifting_failure'
        values = None
        if violation is None:
            violation = parent.mixed_failure(changed,support)
            if bool(violation is None)!=fast.mixed_after_switch(rr,move):
                raise ValueError('mixed K5 predicate disagreement')
            kind = 'mixed_failure' if violation is not None else 'admissible'
        if kind=='admissible':
            delta = search.k5_change(endpoint,move)
            values = tuple(x+d for x,d in zip(base,delta))
            literal_full = tuple(len(checker.monochromatic_bitsets(rr,color)) for color in (True,False))
            if values!=literal_full:
                raise ValueError('actual-graph K5 update disagreement')
        entries.append([support,kind,violation,values])
    if len(entries)!=len(literal_supports) or {x[0] for x in entries}!=literal_supports:
        raise ValueError('complete support-set disagreement')
    digest = hashlib.sha256()
    for entry in sorted(entries):
        digest.update((json.dumps(entry,separators=(',',':'))+'\n').encode())
    if digest.hexdigest()!=expected['canonical_classification_sha256']:
        raise ValueError('complete entry-level classification disagreement')
    with tempfile.TemporaryDirectory(prefix='r55-k5-limit-') as scratch:
        work = Path(scratch)/'one'
        subprocess.run([sys.executable,'-B',str(verify.HERE/'search.py'),'--work',str(work),
                        '--max-steps','1'],check=True,capture_output=True,text=True)
        bounded = json.loads((work/'result.json').read_text())
        if bounded['status']!='STEP_LIMIT' or bounded['steps']!=1 or bounded['final_color_counts']!=[230,206]:
            raise ValueError('step limit misreported as a barrier')
    report = {'all_seven_vertex_completions':cases,'nonzero_color_delta_vectors':nonzero,
              'color_delta_histogram':dict(sorted(delta_histogram.items())),
              'small_order_zero_controls':small,'negative_controls_rejected':rejected,
              'actual_endpoint_entries_compared':len(entries),
              'actual_endpoint_classification_sha256':digest.hexdigest(),
              'one_step_limit_control':{'status':'STEP_LIMIT','steps':1,'final_K5s':436}}
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':
    main()
