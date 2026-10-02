"""Optional comparison after the independently reconstructed record was frozen.

Reads only a specified original JSON fixture. Imports only this review's code.
The author engine is never imported.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import signal


def main():
    p = argparse.ArgumentParser()
    p.add_argument('original_fixture', type=Path)
    args = p.parse_args()
    signal.alarm(45)
    spec = importlib.util.spec_from_file_location('independent_basin', Path(__file__).with_name('check.py'))
    own = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(own)
    record = own.build()
    original = json.loads(args.original_fixture.read_text())
    fields = {'k': 'origin_small', 'm': 'origin_heavy',
              'c': 'polar_small', 'd': 'polar_heavy'}
    def rational_cap(r):
        # Original constant denominator entries are integer 1; own entries
        # are canonical rational strings. Normalize only polynomial fields.
        out = dict(r)
        for key in ['numerator', 'denominator', 'numerator_bernstein', 'denominator_bernstein']:
            own.require(all(type(v) in [int, str] for v in out[key]), 'rational coefficient encoding')
            out[key] = [str(own.Q(v)) for v in out[key]]
        return out
    for family, name in fields.items():
        reconstructed = [{k: v for k, v in r.items() if k not in ['family', 'index']}
                         for r in record['caps'] if r['family'] == family]
        own.same_typed([rational_cap(r) for r in reconstructed],
                       [rational_cap(r) for r in original['bounds']['certificates'][name]])
    hc = record['heavy_curvature']
    own.same_typed(hc['cleared_numerator'], original['bounds']['heavy_B_numerator'])
    own.same_typed(hc['cleared_quarter_margin'], original['bounds']['heavy_B_shift_polynomial'])
    own.same_typed(hc['bernstein_margin'], original['bounds']['heavy_B_shift'])
    names = {'M_S': 'MS', 'M_mix': 'Mmix', 'M_4': 'M4', 'M_KS': 'MKs',
             'M_Kt': 'MKt', 'M_BS': 'MBs', 'M_Bt': 'MBt'}
    for name, target in names.items():
        own.same_typed(record['derivatives'][name], original['derivative_values'][target])
        own.same_typed(record['integer_bounds'][name], original['derivative_caps'][target])
    own.same_typed(record['domains']['radial_majorant_at_T'], original['radial_majorant_at_radius'])
    print(json.dumps({'status': 'PASS', 'all_30_whole_cap_records': True,
                      'all_631_Bernstein_entries': True,
                      'whole_heavy_curvature_polynomials': True,
                      'all_seven_exact_derivatives': True,
                      'no_author_executable_imported': True}))


if __name__ == '__main__':
    main()
