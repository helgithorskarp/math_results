"""Directed test of adaptive full-grid guard orders, preserving all input weights.

The old inputs and guard inputs are separately decoded from fixed bands.
This tests a specified universal-completion mechanism; it does not test
aggregate P or decide target410. Stop at the first complete zero-guard fiber
or a fixed 1000-core prefix. Complete selected fiber sets are retained.
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import time

from definition_checker import occurrences, validate_permutation


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def encode(rows, columns, guard_rows, guard_columns):
    r = len(rows)
    require(r >= 2 and len(columns) == r and len(guard_rows) == len(guard_columns) == r - 1,
            'Grid band counts differ')
    groups = (rows, columns, guard_rows, guard_columns)
    for group, size in zip(groups, (r, r, r - 1, r - 1)):
        require(all(len(validate_permutation(p)) == size for p in group), 'Input sizes differ')
    position = {('old', i, j): (2 * i, rows[i].index(j + 1))
                for i in range(r) for j in range(r)}
    value = {('old', i, j): (2 * j, columns[j][i])
             for i in range(r) for j in range(r)}
    for i in range(r - 1):
        for j in range(r - 1):
            tag = ('guard', i, j)
            position[tag] = (2 * i + 1, guard_rows[i].index(j + 1))
            value[tag] = (2 * j + 1, guard_columns[j][i])
    by_value = sorted(value, key=value.__getitem__)
    rank = {tag: k + 1 for k, tag in enumerate(by_value)}
    tags = tuple(sorted(position, key=position.__getitem__))
    return tuple(rank[tag] for tag in tags), tags


def decode(word, r):
    vertical = {}
    offset = 0
    for j in range(r):
        for rank in range(1, r + 1):
            vertical[offset + rank] = ('old', j, rank)
        offset += r
        if j < r - 1:
            for rank in range(1, r):
                vertical[offset + rank] = ('guard', j, rank)
            offset += r - 1
    rows, guard_rows = [], []
    columns, guard_columns = [[None] * r for _ in range(r)], [[None] * (r - 1) for _ in range(r - 1)]
    start = 0
    for i in range(r):
        band = tuple(vertical[x] for x in word[start:start + r])
        require(all(kind == 'old' for kind, j, rank in band), 'Old horizontal band differs')
        rows.append(tuple(j + 1 for kind, j, rank in band))
        for kind, j, rank in band:
            columns[j][i] = rank
        start += r
        if i < r - 1:
            band = tuple(vertical[x] for x in word[start:start + r - 1])
            require(all(kind == 'guard' for kind, j, rank in band), 'Guard horizontal band differs')
            guard_rows.append(tuple(j + 1 for kind, j, rank in band))
            for kind, j, rank in band:
                guard_columns[j][i] = rank
            start += r - 1
    require(start == len(word) == offset, 'Fixed output length differs')
    return tuple(rows), tuple(map(tuple, columns)), tuple(guard_rows), tuple(map(tuple, guard_columns))


def rank_word(word):
    return tuple(sum(y <= x for y in word) for x in word)


def check_core(data, stream):
    r = len(data[0])
    rows, columns = data
    require(all(not tuple(occurrences(p)) for p in rows + columns), 'Old component outside Av domain')
    choices = tuple(p for p in itertools.permutations(range(1, r)) if not tuple(occurrences(p)))
    records, good = [], 0
    for auxiliary in itertools.product(choices, repeat=2 * (r - 1)):
        grows, gcols = auxiliary[:r - 1], auxiliary[r - 1:]
        word, tags = encode(rows, columns, grows, gcols)
        require(decode(word, r) == (rows, columns, grows, gcols), 'All-component decoder failed')
        actual = tuple(occurrences(word))
        record = {'old_rows': rows, 'old_columns': columns, 'guard_rows': grows, 'guard_columns': gcols,
                  'word': word, 'tags': tags, 'complete_occurrences': actual}
        stream.update((json.dumps(record, separators=(',', ':')) + '\n').encode())
        records.append(record)
        good += not actual
    return good, records


def run():
    began = time.monotonic()
    r = 3
    old = tuple(itertools.permutations((1, 2, 3)))
    stream = hashlib.sha256()
    rows = []
    failure = None
    for index, data in enumerate(itertools.product(old, repeat=6)):
        if index == 1000:
            break
        core = (data[:3], data[3:])
        good, records = check_core(core, stream)
        rows.append({'old_components': data, 'all_guard_profiles': len(records), 'compatible_profiles': good})
        if not good:
            failure = {'core': core, 'complete_guard_fiber': records}
            break
    return {'author': 'literature-researcher-2', 'decision_message_id': 410, 'full_target_solved': False,
            'scope': 'first zero adaptive-full-guard fiber or fixed1000-core prefix, complete16 guard profiles per tested core',
            'r': r, 'output_length': r * r + (r - 1) ** 2,
            'cores_tested': len(rows), 'guard_profiles_tested': sum(row['all_guard_profiles'] for row in rows),
            'full_old_component_population_tested': len(rows) == len(old) ** 6,
            'ordered_stream_sha256': stream.hexdigest(), 'core_rows': rows,
            'first_zero_fiber': failure, 'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'literal_checker_sha256': hashlib.sha256((Path(__file__).parent / 'definition_checker.py').read_bytes()).hexdigest(),
            'review_status': 'author controls; separate independent check pending',
            'python': platform.python_version(), 'elapsed_seconds': time.monotonic() - began,
            'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'Preserve previous evidence')
    report = run()
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ('core_rows', 'first_zero_fiber')}, indent=2))
    if report['first_zero_fiber']:
        print(json.dumps({'zero_core': report['first_zero_fiber']['core']}, indent=2))
