"""Match the literal input to the precisely stated QR617 formula."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from math import isqrt
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
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    began = time.monotonic()
    require(not args.output.exists(), 'Existing evidence')
    word = args.word.read_text().strip()
    require(len(word) == 3704 and set(word) <= {'0', '1'}, 'Binary interval')
    require(all(617 % d for d in range(2, isqrt(617) + 1)), '617 is prime')
    for position in range(1, 3705):
        residue = (position - 1) % 617
        expected = (int(position == 3703) if residue == 0 else int(pow(residue, 308, 617) != 1))
        require(int(word[position - 1]) == expected, 'Stated QR formula does not match input')
    result = {'agent': 'six-vdw-1', 'role': 'researcher', 'checked_at': datetime.now(timezone.utc).isoformat(),
              'status': 'EXPLICIT_QR617_FORMULA_MATCHES_ALL3704_BITS', 'positions_checked': 3704,
              'word_sha256': hashlib.sha256(args.word.read_bytes()).hexdigest(),
              'word_bits_sha256': hashlib.sha256(word.encode()).hexdigest(),
              'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'interpreter_optimization': sys.flags.optimize, 'conservative_combined_cases': 3704 * 3 + 25,
              'seconds': time.monotonic() - began, 'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'threads': 1, 'new_W_bound': None}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'cases': result['conservative_combined_cases']}), flush=True)


if __name__ == '__main__':
    main()
