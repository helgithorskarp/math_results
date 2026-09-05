#!/usr/bin/env python3
"""The reviewed fixed-signature consequence on the four surviving formulas."""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
PHASE = ROOT.parent / 'ramsey_r55_order3_ten_cycle_phase_sweep'
sys.path.insert(0, str(PHASE))
import model as parent

HEADER = b'p cnf 28974 927346\n'


def cases():
    answer = parent.cases()[:4]
    parent.require([r['anchor'] for r in answer] == [64, 65, 67, 69]
                   and all(r['phase'] == [0, 0, 0] for r in answer), 'four-case cover')
    return answer


def units():
    return [-214 - 10*j - i for j in range(3) for i in range(4)]


def generate(base, destination, case):
    parent.require(case in cases(), 'not a surviving parent case')
    parent.require(parent.file_info(base)['sha256'] == parent.BASE_SHA, 'base digest')
    with base.open('rb') as source, destination.open('wb') as target:
        parent.require(source.readline() == parent.BASE_HEADER, 'base header')
        target.write(HEADER)
        shutil.copyfileobj(source, target)
        clauses = parent.tail(case) + [[lit] for lit in units()]
        parent.require(len(clauses) == 346, 'layer clause count')
        target.write(''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses).encode())
    return parent.file_info(destination)
