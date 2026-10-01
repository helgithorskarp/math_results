"""Replay all native queries at the actual 67-word witness's tail choice.

Use an ASan/UBSan executable. This checks one positive fiber, not a
sanitized replay of the complete census.
"""
import argparse
import json
from pathlib import Path
import time

from native import Native
from verify_residual import check, encode


def run(work, executable):
    begun = time.monotonic()
    case, cover = 10, 30483
    header = json.loads((work / f'header-{case}.json').read_text())
    cores = json.loads((work / f'joints-{case}.json').read_text())
    check(any(c['cover'] == cover and c['core_sha256'] ==
              'efc2fcc2aa54a7d21e9d0d9bd8a51cfc89c0b4ac239dfda8465bd1634198e2bb'
              for c in cores), 'actual positive fiber binding')
    with (work / f'carrier-{case}.jsonl').open() as stream:
        for _ in range(cover + 1):
            line = stream.readline()
            check(bool(line), 'truncated sanitized fiber input')
        record = json.loads(line)
    check(record['cover'] == cover, 'sanitized fiber ordering')
    graphs = [[{i for i in range(len(a)) if row & (1 << i)} for row in a]
              for a in (header['y_adjacent'], header['z_adjacent'])]
    nodes = 0
    with Native(executable, graphs) as engine:
        got, count = engine.query(0, record['y_candidates'], target=11)
        check(got == record['y_eleven'], 'sanitized y query mismatch')
        nodes += count
        for z in record['z_cases']:
            got, count = engine.query(1, z['z_candidates'], target=11)
            check(got == z['z_eleven'], 'sanitized z query mismatch')
            nodes += count
    result = {'status': 'PASSED_ACTUAL_WITNESS_FIBER', 'case': case,
              'cover': cover, 'queries': 1 + len(record['z_cases']),
              'nodes': nodes, 'seconds': time.monotonic() - begun}
    print(json.dumps(result), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--executable', type=Path, required=True)
    args = parser.parse_args()
    run(args.work.resolve(), args.executable.resolve())
