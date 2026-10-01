"""Definition-level controls for the untrusted cut and incidence certificates."""
from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import verify


def rejected(callback):
    try:
        callback()
    except RuntimeError:
        return 1
    raise RuntimeError('Damaged proof object was accepted')


def main():
    cuts = json.loads((verify.HERE / 'cuts.json').read_text())
    original = cuts['cuts'][0]
    graph, degree = verify.graph(original['F_mask'])
    target, caps = verify.spine_bounds(graph, degree)
    rows = verify.partition_rows(graph, degree, caps)
    verify.certify(original, rows, target, caps)
    damaged = []
    x = deepcopy(original); x['gamma'] -= 1; damaged.append(x)
    x = deepcopy(original); x['rhs'] = 0; damaged.append(x)
    x = deepcopy(original); x['beta'][0][2] = -1; damaged.append(x)
    x = deepcopy(original); x['beta'].append(x['beta'][0]); damaged.append(x)
    rejections = sum(rejected(lambda cut=cut: verify.certify(cut, rows, target, caps))
                     for cut in damaged)
    fixture = json.loads((verify.HERE / 'incidences.json').read_text())
    with TemporaryDirectory() as directory:
        path = Path(directory) / 'missing.json'
        forged = deepcopy(fixture)
        forged['records'].pop()
        path.write_text(json.dumps(forged))
        rejections += rejected(lambda: verify.audit(fixture_path=path, check_baseline=False))
    graph, _ = verify.graph(fixture['F_mask'])
    first = fixture['records'][0]
    # This matrix has a feasible star at row zero; an alleged empty star there
    # must be rejected. The actual selected obstruction is checked by audit.
    rejections += rejected(lambda: verify.empty_blue_stars(graph, first['rows'], 0))
    verify.baseline()
    verify.require(rejections == 6, 'Control coverage differs')
    print(json.dumps({'damaged_objects_rejected': rejections,
                      'primary_baseline': [93, 117, 3, 6]}, sort_keys=True))


if __name__ == '__main__':
    main()
