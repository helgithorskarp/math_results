"""All source-core deletion interfaces and complete affected registry counts."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import struct
import time
from lookup import Lookup, catalog
from compile_family import selected_matching, physical_suffix
from support import HERE, need

def run(cache, out):
    out = Path(out); lookup = Lookup(cache, out / 'tables'); summary = []
    for n, q, selected in ((11, 8, 4), (7, 9, 2)):
        words = catalog(cache, n); edges = list(combinations(range(n), 2))
        hist = Counter(); matching_hist = Counter(); core_hist = Counter()
        digest = hashlib.sha256(); total = 0; start = time.monotonic()
        record = struct.Struct('<IBH' + 'B' * (n-4))
        with (out / f'deletions{n}.bin').open('xb') as stream:
            for c, word in enumerate(words):
                a = [[0] * n for _ in range(n)]; rows = [0] * n
                for k, (i,j) in enumerate(edges):
                    if word >> k & 1:
                        a[i][j] = a[j][i] = 1; rows[i] |= 1 << j; rows[j] |= 1 << i
                matching = selected_matching(rows, selected)
                matching_hist[tuple(sum((list(e) for e in matching), []))] += 1
                destinations = set()
                for choice, (e, f) in enumerate(combinations(matching, 2)):
                    core = [v for v in range(n) if v not in e + f]
                    target, permutation = lookup.find(a, core)
                    raw = record.pack(c, choice, target, *permutation)
                    stream.write(raw); digest.update(raw)
                    hist[target] += 1; destinations.add(target); total += 1
                core_hist[len(destinations)] += 1
        # Every core-index row is covered above. Clause generation depends only
        # on its selected matching, not any other internal core edge.
        matching_json = json.dumps(sorted((list(k),v) for k,v in matching_hist.items()), separators=(',', ':')).encode()
        summary.append({'source_order': n, 'destination_order': n-4,
                        'source_cores': len(words), 'deletions': total,
                        'record_bytes': record.size, 'sha256': digest.hexdigest(),
                        'destination_histogram': [hist[i] for i in range(len(lookup.words[n-4]))],
                        'distinct_destination_records': len(hist),
                        'destinations_per_source_histogram': sorted(core_hist.items()),
                        'distinct_selected_matchings': len(matching_hist),
                        'matching_histogram_sha256': hashlib.sha256(matching_json).hexdigest(),
                        'seconds': time.monotonic()-start})
        print(json.dumps({k:v for k,v in summary[-1].items() if 'histogram' not in k}), flush=True)
    registry = json.loads((HERE.parent / 'ramsey_r55_maximal_block_order' / 'TASKS.json').read_text())
    rows = [{'q': r['q'], 'r': r['r'], 'tasks': r['core_stop'],
             'added_clauses_per_task': (36*r['r'] if r['q']==8 else 6*r['r'] if r['q']==9 else 0)}
            for r in registry['classes']]
    result = {'status': 'COMPLETE_CORE_DESTINATION_CENSUS', 'core_interfaces': summary,
              'registry': rows, 'affected_tasks': sum(x['tasks'] for x in rows if x['added_clauses_per_task']),
              'total_added_clauses_over_registry': sum(x['tasks']*x['added_clauses_per_task'] for x in rows),
              'total_tasks': registry['tasks'], 'new_task_decisions': 0, 'target_found': False}
    (out / 'CENSUS.json').write_text(json.dumps(result, indent=2) + '\n')
    return result

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('cache'); p.add_argument('out'); args = p.parse_args()
    result = run(args.cache, args.out)
    print(json.dumps({k:v for k,v in result.items() if k not in ('core_interfaces','registry')}))
