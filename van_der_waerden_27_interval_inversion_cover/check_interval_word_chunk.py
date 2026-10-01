"""Definition-level integer AP checker; imports neither search nor model encoder."""
import argparse
from bisect import bisect_right
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank_domain(n):
    maximum = (n-1)//6
    return [n*k-3*k*(k+1) for k in range(maximum+1)]


def positions_at_rank(n, rank, boundaries):
    d = bisect_right(boundaries, rank)
    a = rank-boundaries[d-1]
    positions = tuple(a+j*d for j in range(7))
    assert d > 0 and 0 <= a < positions[-1] < n
    return a, d, positions


def controls():
    words = cases = 0
    for n in range(7, 13):
        boundaries = rank_domain(n)
        by_rank = [positions_at_rank(n, rank, boundaries)[2] for rank in range(boundaries[-1])]
        # Separate a-major definition enumeration, with a different loop order.
        direct = [(a, a+d, a+2*d, a+3*d, a+4*d, a+5*d, a+6*d)
                  for a in range(n) for d in range(1, n) if a+6*d < n]
        assert len(by_rank) == len(set(by_rank)) == len(direct)
        assert set(by_rank) == set(direct)
        for bits in itertools.product((0, 1), repeat=n):
            got = {row for row in by_rank if all(bits[j] == bits[row[0]] for j in row)}
            expected = {row for row in direct if len({bits[j] for j in row}) == 1}
            assert got == expected
            words += 1
            cases += len(by_rank)+len(direct)
    assert cases < 200000
    return {'status': 'INTERVAL_RANK_DOMAIN_AND_MONOCHROME_CONTROLS_PASSED',
            'words': words, 'actual_AP_assignment_cases': cases,
            'length_range': [7, 12], 'solver_or_encoder_imported': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--word', type=Path)
    parser.add_argument('--start', type=int)
    parser.add_argument('--stop', type=int)
    parser.add_argument('--monochromes', type=Path)
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists(), 'refusing to overwrite evidence'
    start_time = time.perf_counter()
    if args.controls:
        assert args.word is None
        result = controls()
    else:
        assert args.word is not None and args.monochromes is not None
        assert not args.monochromes.exists()
        raw = args.word.read_text().strip()
        if not 7 <= len(raw) <= 4000 or not set(raw) <= {'0', '1'}:
            raise ValueError('invalid binary interval coloring')
        n = len(raw)
        domain = rank_domain(n)
        assert 0 <= args.start < args.stop <= domain[-1]
        assert args.stop-args.start <= 190000
        found = 0
        ones_counts = [0]*8
        with args.monochromes.open('x') as stream:
            for rank in range(args.start, args.stop):
                a, d, points = positions_at_rank(n, rank, domain)
                colors = tuple(raw[j] for j in points)
                ones_counts[colors.count('1')] += 1
                if len(set(colors)) == 1:
                    stream.write(json.dumps({'rank': rank, 'a_zero_based': a, 'd': d,
                                             'positions_one_based': [j+1 for j in points],
                                             'color': int(colors[0])})+'\n')
                    found += 1
        result = {'status': 'COMPLETE_INTEGER_AP_SLICE_CHECKED',
                  'word': str(args.word), 'word_file_sha256': sha(args.word),
                  'word_bits_sha256': hashlib.sha256(raw.encode()).hexdigest(),
                  'length': n, 'complete_domain_APs': domain[-1],
                  'AP_start_inclusive': args.start, 'AP_stop_exclusive': args.stop,
                  'APs_checked': args.stop-args.start, 'monochromatic_APs': found,
                  'ones_histogram': ones_counts, 'monochromes': str(args.monochromes),
                  'monochromes_sha256': sha(args.monochromes),
                  'solver_or_encoder_imported': False,
                  'partial_slice_not_a_full_word_certificate': True,
                  'mathematical_nonexistence_claim': False}
    result.update(agent='six-vdw-1', role='researcher',
                  checked_at=datetime.now(timezone.utc).isoformat(),
                  seconds=time.perf_counter()-start_time,
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  checker_sha256=sha(Path(__file__)))
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: result[key] for key in ('status', 'seconds')}), flush=True)


if __name__ == '__main__':
    main()
