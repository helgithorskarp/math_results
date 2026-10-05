"""Author controls of the separate simple-marker refinement, not a team check."""

from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math
import platform
import time

from cartesian_fibers import pair_key, predecessor_masks, require
from check_lyra_boundary import occurrences
from verify_marker_construction import formula_pair, marker_map, minimum_at


def proper_intervals(p):
    result = []
    for first in range(len(p)):
        low = high = p[first]
        for end in range(first + 2, len(p) + 1):
            low = min(low, p[end - 1])
            high = max(high, p[end - 1])
            if end - first < len(p) and high - low + 1 == end - first:
                result.append((first, end))
    return tuple(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    began = time.perf_counter()
    criterion_rows = []
    for m in range(2, 7):
        simple = 0
        digest = hashlib.sha256()
        for p in itertools.permutations(range(1, m + 1)):
            image = marker_map(p)
            intervals = proper_intervals(image)
            expected = []
            if p[0] == m:
                expected.append((0, 2))
            if p[-1] == 1:
                expected.append((len(image) - 2, len(image)))
            require(intervals == tuple(expected), 'Simplicity criterion failed')
            simple += not intervals
            digest.update((json.dumps([p, intervals], separators=(',', ':'))+'\n').encode())
        criterion_rows.append({'m': m, 'all_inputs': math.factorial(m),
                               'simple_images': simple, 'interval_stream_sha256': digest.hexdigest()})
    extension_rows = []
    for m in range(1, 6):
        digest = hashlib.sha256()
        count = 0
        for p in itertools.permutations(range(1, m + 1)):
            tau = (1,) + tuple(x + 1 for x in p) + (m + 2,)
            image = marker_map(tau)
            require(not proper_intervals(image), 'Extension is not simple')
            expected = tuple(tuple(3 * (i + 1) for i in row) for row in occurrences(p))
            require(occurrences(image) == expected, 'Extension occurrence correspondence failed')
            free = image[::3]
            require(tuple(x - m - 2 for x in free[1:-1]) == p, 'Extension decoding failed')
            require(pair_key(image) == formula_pair(m + 2), 'Extension left common fiber')
            digest.update((json.dumps([p, image, expected], separators=(',', ':'))+'\n').encode())
            count += 1
        extension_rows.append({'m': m, 'all_inputs': count, 'image_length': 3 * m + 4,
                               'extension_stream_sha256': digest.hexdigest()})
    branches = []
    for m in range(2, 13):
        pair = formula_pair(m)
        pred = predecessor_masks(pair)
        chosen = sum(1 << (3 * i - 1) for i in range(1, m))
        available = [i for i in range(3 * m - 2) if not chosen & (1 << i) and not pred[i] & ~chosen]
        require(available == list(range(0, 3 * m - 2, 3)), 'Availability changed')
        for t in range(m - 1):
            image = marker_map(minimum_at(m, t))
            require(not proper_intervals(image), 'Simple viable witness fails')
            require(not occurrences(image), 'Simple viable witness contains a box')
            require(pair_key(image) == pair and image[3 * t] == m, 'Simple witness prefix/pair failed')
        # Explicitly expose the forced forbidden interval at the excluded last position.
        bad = marker_map(minimum_at(m, m - 1))
        require((len(bad)-2, len(bad)) in proper_intervals(bad), 'Last-rank interval obstruction absent')
        branches.append({'m': m, 'available_positions': m, 'simple_viable_witnesses': m-1})
    report = {'author': 'literature-researcher-1', 'claim_status': 'finite controls of separate uniform author proof; different-researcher check pending',
              'full_target_solved': False, 'criterion_controls': criterion_rows, 'extension_controls': extension_rows,
              'simple_branch_controls': branches, 'python': platform.python_version(), 'seconds': time.perf_counter()-began}
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
