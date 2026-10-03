"""One-process source-only entrypoint; actual mathematical children remain serial.

Published compact expected outputs are never input to a mathematical checker.
After all fresh mathematical replays, compare the complete mathematical record
against the optional published expected certificate. Operational timings and
byte hashes of timed generated records are intentionally not compared.
"""
import json
import sys
from pathlib import Path

from controls import operations_allow
from inputs import checked_finite, need, static_sources
import run
import freeze

ROOT = Path(__file__).resolve().parent


def main():
    operations_allow()
    static_sources()
    expected_path = ROOT / 'certificate.json'
    expected = checked_finite(json.loads(expected_path.read_text())) if expected_path.exists() else None
    need(len(sys.argv) == 1, 'reproduce.py needs no arguments')
    sys.argv = [str(ROOT / 'run.py'), 'all']
    run.main()
    freeze.main('work/reproduction-audit')
    actual = checked_finite(json.loads((ROOT / 'work/reproduction-audit/certificate.json').read_text()))
    if expected is not None:
        need(actual['finite'] == expected['finite'], 'Entire cold mathematical record differs from published expectation')
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher',
                      'status': 'COMPLETE_FRESH_SOURCE_ONLY_SCOPED_ROUTE_REPRODUCTION',
                      'finite_sha256': actual['finite_sha256'],
                      'entire_expected_mathematical_record_equal': expected is not None,
                      'external_person_review_claimed': False}), flush=True)


if __name__ == '__main__':
    main()
