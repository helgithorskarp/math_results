"""Optional proof regeneration. The solver-free reader checks published traces."""
import argparse
import hashlib
import json
from pathlib import Path

from cover import compile_cover, sweep
from rup import RupChecker


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    import pysat
    from pysat.solvers import Glucose4
    sweep.require(pysat.__version__ == '1.8.dev24', 'use the pinned python-sat version')
    args.out.mkdir(parents=True, exist_ok=True)
    records = json.loads(Path(__file__).with_name('cases.json').read_text())
    for record in records:
        cells = sweep.read_cells(record['cells'])
        target = tuple(map(tuple, record['obstruction']))
        unused, cnf, nv = compile_cover(cells, target)
        with Glucose4(bootstrap_with=cnf, with_proof=True) as solver:
            solver.conf_budget(30000)
            answer = solver.solve_limited()
            sweep.require(answer is False, 'UNKNOWN/SAT supplies no negative certificate')
            trace = '\n'.join(solver.get_proof()) + '\n'
        checked = RupChecker(cnf, nv).verify(trace, capture=True)
        trimmed = checked.pop('trimmed')
        checked_trim = RupChecker(cnf, nv).verify(trimmed)
        raw = trimmed.encode('ascii')
        path = args.out / f"case-{record['index']}.rup"
        path.write_bytes(raw)
        print(json.dumps(dict(index=record['index'], raw_check=checked,
                             trimmed_check=checked_trim,
                             sha256=hashlib.sha256(raw).hexdigest()), sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
