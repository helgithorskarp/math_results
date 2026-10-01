"""Find positive AP obstructions for residual cuts, with fixed resumable quotas.

Only small-step APs crossing an interval boundary are queried. Failed prefix
searches never assert that the coloring is AP free or that the family is closed.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import time


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--word', type=Path, required=True)
    parser.add_argument('--cuts', type=Path, required=True)
    parser.add_argument('--point-index', type=int, required=True)
    parser.add_argument('--next-d', type=int, default=1)
    parser.add_argument('--next-a', type=int, default=1)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    began = time.monotonic()
    require(not args.output.exists(), 'Existing evidence')
    word = args.word.read_text().strip()
    n = len(word)
    require(n == 3704 and set(word) <= {'0', '1'}, 'Binary base interval')
    data = json.loads(args.cuts.read_text())
    require(type(data) is dict and set(data) == {'length', 'term_count', 'base_bits_sha256', 'cover_sha256', 'cuts'},
            'Residual cut schema')
    require(type(data['length']) is int and data['length'] == n and type(data['term_count']) is int
            and data['term_count'] == 7 and data['base_bits_sha256'] == hashlib.sha256(word.encode()).hexdigest(),
            'Residual cut scope')
    cuts = data['cuts']
    require(type(cuts) is list and len(cuts) == 2899, 'Residual count')
    previous = None
    for cut in cuts:
        require(type(cut) is list and len(cut) == 2 and all(type(x) is int for x in cut)
                and 0 <= cut[0] < cut[1] <= n, 'Integer residual cut')
        require(previous is None or previous < cut, 'Residual order/uniqueness')
        previous = cut
    require(0 <= args.point_index <= len(cuts) and 1 <= args.next_d <= 65 and 1 <= args.next_a <= n + 1,
            'Resume cursor')
    bits = [int(b) for b in word]
    index, step, first = args.point_index, args.next_d, args.next_a
    tests, finished, cases = 0, 0, n + 5 * len(cuts) + 20
    positives, unresolved = [], []

    def add(count):
        nonlocal cases
        cases += count
        if cases > 200000:
            raise RuntimeError('Unchanged200000-case operational limit')

    quota = False
    while index < len(cuts) and finished < 32:
        left, right = cuts[index]
        found = False
        while step <= 64:
            add(12)
            ranges = []
            for boundary in [left, right]:
                lo, hi = max(1, boundary - 6 * step + 1), min(boundary, n - 6 * step)
                if lo <= hi:
                    ranges.append((lo, hi))
            if len(ranges) == 2 and ranges[1][0] <= ranges[0][1] + 1:
                ranges = [(ranges[0][0], max(ranges[0][1], ranges[1][1]))]
            for lo, hi in ranges:
                a = max(lo, first)
                while a <= hi:
                    if tests == 8000:
                        first, quota = a, True
                        break
                    # This is discovery only; a separate checker evaluates every
                    # submitted positive AP directly from its seven positions.
                    colors = 0
                    for k in range(7):
                        pos = a + k * step
                        colors += bits[pos - 1] ^ int(left < pos <= right)
                    tests += 1
                    add(12)
                    if colors in (0, 7):
                        positives.append([left, right, a, step])
                        found = True
                        break
                    a += 1
                if found or quota:
                    break
            if found or quota:
                break
            step, first = step + 1, 1
        if quota:
            break
        if not found:
            unresolved.append([left, right])
        index, finished, step, first = index + 1, finished + 1, 1, 1
    status = 'PREFIX64_POSITIVE_APS_PROPOSED_NO_FAMILY_CONCLUSION'
    result = {'agent': 'six-vdw-1', 'role': 'researcher', 'created_at': datetime.now(timezone.utc).isoformat(),
              'status': status, 'initial_cursor': [args.point_index, args.next_d, args.next_a],
              'next_cursor': [index, step, first], 'finished_points': finished, 'AP_tests': tests,
              'positive_points': positives, 'prefix64_unresolved_cuts': unresolved,
              'test_quota': 8000, 'finished_point_quota': 32, 'difference_limit': 64,
              'word_sha256': hashlib.sha256(args.word.read_bytes()).hexdigest(),
              'cuts_sha256': hashlib.sha256(args.cuts.read_bytes()).hexdigest(),
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'conservative_combined_cases': cases, 'seconds': time.monotonic() - began,
              'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, 'threads': 1,
              'positive_witnesses_pending_independent_check': True, 'failed_prefix_not_nonexistence': True,
              'full_family_exclusion': False, 'new_W_bound': None}
    args.output.write_text(json.dumps(result, separators=(',', ':')) + '\n')
    print(json.dumps({'status': status, 'next_cursor': result['next_cursor'], 'tests': tests,
                      'positive': len(positives), 'unresolved': len(unresolved), 'cases': cases}), flush=True)


if __name__ == '__main__':
    main()
