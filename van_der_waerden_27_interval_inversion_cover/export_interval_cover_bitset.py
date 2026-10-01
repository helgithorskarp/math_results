"""Independent bit-pattern/bitset reconstruction of the uncovered cuts.

No rectangle proposer or sorted-union verifier is imported. Actual seven-bit
patterns are XORed with every contiguous term mask, then covered R values
are ORed as integer bitsets. Exported cuts remain unverified candidates.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import sys
import time


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--word', type=Path, required=True)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--row-start', type=int, required=True)
    parser.add_argument('--row-count', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    began = time.monotonic()
    require(not args.output.exists(), 'Output exists')
    word = args.word.read_text().strip()
    n = len(word)
    require(n == 3704 and set(word) <= {'0', '1'}, 'Base binary interval')
    require(0 <= args.row_start < n and 1 <= args.row_count <= 32 and args.row_start + args.row_count <= n, 'Row scope')
    data = json.loads(args.certificate.read_text())
    require(type(data) is dict and set(data) == {'length', 'term_count', 'base_bits_sha256', 'APs'}, 'Certificate schema')
    require(type(data['length']) is int and data['length'] == n and type(data['term_count']) is int
            and data['term_count'] == 7, 'Scope mismatch')
    require(data['base_bits_sha256'] == hashlib.sha256(word.encode()).hexdigest(), 'Word digest')
    APs = data['APs']
    require(type(APs) is list and 1 <= len(APs) <= 289, 'AP scope')
    cases, rectangles, seen, originals = n + 3, [], set(), 0

    def add(count=1):
        nonlocal cases
        cases += count
        if cases > 200000:
            raise RuntimeError('Unchanged200000-case operational limit')

    for ap in APs:
        add(12)
        require(type(ap) is list and len(ap) == 2 and all(type(t) is int for t in ap), 'Integer AP coordinates')
        a, d = ap
        require(a >= 1 and d >= 1 and a + 6 * d <= n and (a, d) not in seen, 'AP geometry/uniqueness')
        seen.add((a, d))
        points = [a + k * d for k in range(7)]
        pattern = sum((word[x - 1] == '1') << k for k, x in enumerate(points))
        originals += pattern in (0, 127)
        bounds = [0] + points + [n + 1]
        for first in range(8):
            for stop in range(first, 8):
                mask = ((1 << (stop - first)) - 1) << first
                add(4)
                if (pattern ^ mask) in (0, 127):
                    rectangles.append((bounds[first], bounds[first + 1] - 1, bounds[stop], bounds[stop + 1] - 1))
                    add(4)
    require(originals <= 1 and len(rectangles) <= 2 * len(APs) + 7, 'Checked pattern count bound')
    cuts, rows, domain = [], [], 0
    complete_mask = (1 << (n + 1)) - 1
    for left in range(args.row_start, args.row_start + args.row_count):
        allowed = complete_mask ^ ((1 << (left + 1)) - 1)
        covered = 0
        for llo, lhi, rlo, rhi in rectangles:
            add()
            if llo <= left <= lhi:
                covered |= ((1 << (rhi - rlo + 1)) - 1) << rlo
                add(3)
        missing = allowed & ~covered
        count = missing.bit_count()
        while missing:
            low = missing & -missing
            right = low.bit_length() - 1
            require(left < right <= n, 'Actual exported cut')
            cuts.append([left, right])
            missing ^= low
            add(3)
        rows.append({'left': left, 'cut_intervals': n - left, 'uncovered': count})
        domain += n - left
    require(len(cuts) == sum(r['uncovered'] for r in rows), 'Bitset population accounting')
    result = {'agent': 'six-vdw-1', 'role': 'researcher', 'checked_at': datetime.now(timezone.utc).isoformat(),
              'status': 'INDEPENDENT_BITSET_CUT_COMPLEMENT_VERIFIED_AND_EXPORTED', 'row_start': args.row_start,
              'row_stop_exclusive': args.row_start + args.row_count, 'rows': rows, 'cut_intervals_checked': domain,
              'uncovered_count': len(cuts), 'cuts': cuts, 'selected_APs': len(APs), 'derived_rectangles': len(rectangles),
              'certificate_sha256': hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
              'word_file_sha256': hashlib.sha256(args.word.read_bytes()).hexdigest(),
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'interpreter_optimization': sys.flags.optimize,
              'conservative_combined_cases': cases, 'seconds': time.monotonic() - began,
              'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, 'threads': 1,
              'all_family_exclusion': False, 'uncovered_cuts_not_known_AP_free': True, 'new_W_bound': None}
    args.output.write_text(json.dumps(result, separators=(',', ':')) + '\n')
    print(json.dumps({'status': result['status'], 'rows': len(rows), 'uncovered': len(cuts), 'cases': cases}), flush=True)


if __name__ == '__main__':
    main()
