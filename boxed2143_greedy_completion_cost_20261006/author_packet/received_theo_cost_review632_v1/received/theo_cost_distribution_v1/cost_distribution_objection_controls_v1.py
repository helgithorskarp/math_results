#!/usr/bin/env python3
"""Fixed-family controls for the proposed weighted-cost objection."""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import resource
import sys
import time

sys.dont_write_bytecode = True
from check_quinn_gap_opening_v1 import complete


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists(), 'Preserve original output'
    began = time.perf_counter()
    rows, cases = [], 0
    digest = hashlib.sha256()
    for n in range(3, 17):
        parent = tuple(range(n-1, 0, -1)) + (n,)
        costs = []
        for g in range(n+1):
            source = parent[:g] + (n+1,) + parent[g:]
            result = complete(source)
            assert result['stage_costs'][:-1] == [0] * n
            expected = g-1 if 2 <= g < n else 0
            assert result['stage_costs'][-1] == expected
            assert result['output_length'] == n+1+expected
            costs.append(expected)
            digest.update((json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n').encode())
            cases += 1
        assert sum(costs) == (n-2)*(n-1)//2
        rows.append({'n': n, 'parent': parent, 'gap_costs': costs,
                     'sum_cost': sum(costs),
                     'conditional_mean_exact_numerator_denominator': [sum(costs), n+1]})
    assert cases == 147
    here = Path(__file__).resolve().parent
    report = {'author': 'literature-researcher-4', 'different_researcher_check': 'pending',
              'decision_message_id': 410, 'full_target_solved': False,
              'scope': 'same-author fixed descending-prefix family controlsn3..16; uniform law/induction separate',
              'case_count': cases, 'rows': rows,
              'ordered_complete_trace_stream_sha256': digest.hexdigest(),
              'sources': {name: hashlib.sha256((here/name).read_bytes()).hexdigest()
                          for name in ('cost_distribution_objection_controls_v1.py',
                                       'check_quinn_gap_opening_v1.py', 'COST_DISTRIBUTION_OBJECTION_V1.md')},
              'python': platform.python_version(), 'seconds': time.perf_counter()-began,
              'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'rows'}, indent=2))


if __name__ == '__main__':
    main()
