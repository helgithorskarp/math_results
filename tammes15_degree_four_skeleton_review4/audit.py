"""Regenerate the independent census, medial bridge, and exact angle audit."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import platform

import angles
import maps
import sympy

HERE = Path(__file__).resolve().parent


def rejected(fn, message):
    try:
        fn()
    except (ValueError, KeyError, IndexError, TypeError):
        return message
    raise ValueError('invalid control accepted: ' + message)


def controls(reference, cert, census):
    results = []
    bad = deepcopy(reference)
    bad['cover']['graph_representatives'][0]['orbit'] += 1
    # No repeated full census is necessary: the independently obtained
    # representative list must reject this altered orbit partition.
    original = [(r['graph_mask'], r['orbit_size']) for r in census['maps']]
    results.append(rejected(lambda: maps.need(
        original == [(r['mask'], r['orbit']) for r in bad['cover']['graph_representatives']],
        'orbit comparison'), 'wrong orbit size'))
    for name, mutate in [
        ('missing quadrilateral', lambda c: c['Qs'].pop()),
        ('reused quadrilateral vertex', lambda c: c['Qs'][0].__setitem__(1, c['Qs'][0][0])),
        ('fake closure walk', lambda c: c.__setitem__('closure_cycle', [0, 1, 0])),
        ('wrong original star', lambda c: c.__setitem__('one_T_vertex', 4)),
        ('wrong critical corner', lambda c: c.__setitem__('upper_bound_slot', 11)),
        ('changed complete face complex', lambda c: c['Qs'][0].__setitem__(1, 0)),
    ]:
        bad = deepcopy(cert)
        mutate(bad)
        results.append(rejected(lambda: angles.run(census, bad), name))
    # A global face reflection preserves the whole unoriented map and
    # even/odd corner slots (reflection fixes the first corner).
    reflected = deepcopy(cert)
    for key in ('Ts', 'Qs'):
        reflected[key] = [[f[0]] + list(reversed(f[1:])) for f in reflected[key]]
    maps.need(angles.run(census, reflected) == angles.run(census, cert),
              'global face reflection control')
    return {'rejected_mutations': results, 'global_face_reflection': 'passed'}


def run(repository):
    provenance = json.loads((HERE/'provenance.json').read_text())
    for name, expected in provenance['input_sha256'].items():
        actual = hashlib.sha256((repository/name).read_bytes()).hexdigest()
        maps.need(actual == expected, 'pinned author source input: ' + name)
    base = repository/'tammes15_nine_quad_degree_four_exclusion'
    reference = json.loads((base/'EXPECTED.json').read_text())
    cert = json.loads((base/'CERTIFICATE.json').read_text())
    census = maps.run(reference)
    interpretation = angles.run(census, cert)
    return {'agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'enumeration': census, 'geometry_interpretation': interpretation,
            'controls': controls(reference, cert, census)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', type=Path, default=HERE.parent)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = json.dumps(run(args.repository), indent=2, sort_keys=True) + '\n'
    if args.check:
        maps.need(output == (HERE/'EXPECTED.json').read_text(), 'entire expected independent output')
        print(json.dumps({'status': 'passed', 'python': platform.python_version(),
                          'sympy': sympy.__version__,
                          'expected_sha256': hashlib.sha256(output.encode()).hexdigest()}, sort_keys=True))
    else:
        print(output, end='')
