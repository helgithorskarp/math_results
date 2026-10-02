"""Post-seal data alignment; imports no producer executable.

Compare all 31 native rational budgets, six whole field identities, and all
14 lower-coefficient phase weights against the independently sealed evidence.
Other native polynomial coordinates are covered by replay and the separate
independent identities, not claimed to have been coefficient-wise aligned.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
from audit import K, OMEGA_POWERS, load_fixture, require

ROOT = Path(__file__).resolve().parent
NATIVE_SHA = '898cfca7871dbb4d16a15e94bb50ea9a04ff59c402a3a155236f4462e9f0eae8'
PAIRS = [
 ('full original displacement below V/4','quarter root displacement'),
 ('full linear displacement below V/4','quarter linear displacement'),
 ('all phase full normal quadratic budget9/8','all-phase half-normal budget'),
 ('all phase non-T full root quadratic budget1','all-phase displacement tail'),
 ('complete centered objective eta2 budget40','original reciprocal quadratic40'),
 ('whole cube leading-normal remainder40eta2','original cube remainder40'),
 ('whole fourth-phase leading-normal remainder46eta2','original fourth remainder46'),
 ('positive sqrt21 enclosure','original mu square'),
 ('full sharp-coercivity budget16','original coercivity16'),
 ('R3 below gapbudget/100','original cube Delta margin'),
 ('R4 below gapbudget/12','original fourth Delta margin'),
 ('real mean inversion below4gap/3','original mean4over3'),
 ('rotated Q inversion below21gap','original Q3over2'),
 ('H difference below26gap','original H26'),
 ('full origin real energy below7gap','original real energy7'),
 ('imag mean sqrt term below1',None),
 ('imag mean gap term below1','original D Delta1'),
 ('imag mean eta2 term below44','original D quadratic44'),
 ('root mean/T eta2 aggregate below125','all-root quadratic125'),
 ('all9 root-motion gap coefficient below8','original motion Delta8'),
 ('all9 root-motion sqrt coefficient below3','original motion sqrt3'),
 ('sharp uniform slope exceeds111/40','original rational111over40'),
 ('selected cosine lower cubic sign','cubic lower sign'),
 ('selected cosine upper cubic sign','cubic upper sign'),
 ('selected cosine monotone divisor','cubic branch monotonicity'),
 ('w4 below3/5','dual w4 upper3over5'),
 ('w4 above1/2','dual w4 lowerhalf'),
 ('w3 above4','dual w3 lower4'),
 ('w3 below23/5','dual w3 upper23over5'),
 ('whole centered radius below1/96','centered tail radius'),
 ('positive full reciprocal tail divisor','entire Legendre denominator'),
]


def compare(path):
    require(hashlib.sha256(path.read_bytes()).hexdigest() == NATIVE_SHA,
            'whole native fixture source pin')
    native = load_fixture(path)
    own = load_fixture(ROOT / 'EXPECTED.json')
    seal = load_fixture(ROOT / 'INDEPENDENCE.json')
    for name, sha in seal['source_sha256'].items():
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == sha,
                'independent seal changed')
    om = {r['name']: F(r['exact']) for r in own['strict_margins']}
    astar = 1 - F(own['original_eta_endpoint'])
    scales = {name: F(16) for name in [
        'R3 below gapbudget/100', 'R4 below gapbudget/12',
        'H difference below26gap', 'full origin real energy below7gap']}
    scales['all9 root-motion sqrt coefficient below3'] = 49 * astar**2
    margins = []
    require([r['name'] for r in native['whole_domain_margins']] ==
            [n for n, o in PAIRS], 'complete ordered margin census')
    for row, (name, source) in zip(native['whole_domain_margins'], PAIRS):
        scale = scales.get(name, F(1))
        # The native proof uses sqrt(3)<7/4 here. This post-seal scalar
        # alignment is distinguished from the sealed sharper squared bound.
        value = scale * om[source] if source else 1 - F(1, 2) / astar
        require(value > 0 and value == F(row['margin']), 'native budget: ' + name)
        margins.append({'native_name': name, 'own_name': source,
                        'scale': str(scale), 'entire_exact_value': str(value),
                        'post_seal_looser_sqrt_enclosure': source is None})
    oi = {r['name']: r for r in own['identities']}
    ni = {r['name']: r for r in native['identities']}
    fields = []
    for name, other, sign in [
        ('real leading mean dual', 'dual mean', 1),
        ('rotated trace dual', 'dual second moment', 1),
        ('known sharp coefficient', 'sharp coefficient', 1),
        ('known optimal cube moment', 'cube optimum', 1),
        ('known optimal fourth moment', 'fourth optimum', 1),
        ('whole nonzero Cramer determinant', 'Cramer determinant', -1),
    ]:
        require(len(oi[other]['full_map']) == 1 and
                oi[other]['full_map'][0][0] == [], 'constant field identity')
        full = (sign * K(oi[other]['full_map'][0][1])).pack()
        require(full == ni[name]['whole_six_field_coefficients'],
                'whole native field: ' + name)
        fields.append({'native_name': name, 'own_name': other,
                       'orientation_sign': sign, 'whole_coefficients': full})
    rows = []
    for k in [3, 4]:
        maps = {}
        for phase in [k, 9-k]:
            row = oi['entire integrated linear displacement ' + str(phase)]
            maps[phase] = {tuple((v, p) for v, p in powers): K(coef)
                           for powers, coef in row['full_map']}
        for j in range(1, 8):
            key = tuple(sorted([('d' + str(j), 1), ('u', j - 8)]))
            # Entire sealed displacement, multiplied by the conjugate base
            # phase, then averaged over the opposite labels.
            coef = (maps[k].get(key, K()) * OMEGA_POWERS[-k % 9] +
                    maps[9-k].get(key, K()) * OMEGA_POWERS[k]) / 2
            rows.append({'phase': k, 'degree': j,
                         'whole_pair_coefficient': coef.pack()})
    require(rows == ni['entire fourteen lower coefficient phase weights']['rows'],
            'every whole lower-coefficient phase weight')
    return {'schema': 'post-seal-native-data-alignment-v1',
            'all_native_margins': margins, 'six_whole_field_identities': fields,
            'all_fourteen_lower_phase_coefficients': rows,
            'scope': '31 rational margins, six full fields and 14 full phase coefficients; no claim of coefficient-wise alignment of the other native coordinate maps',
            'producer_executable_imported': False,
            'sealed_core_unchanged': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('native_fixture', type=Path)
    parser.add_argument('--record', type=Path)
    args = parser.parse_args()
    try:
        record = compare(args.native_fixture)
        if args.record:
            args.record.write_text(json.dumps(record, sort_keys=True, indent=2) + '\n')
        print(json.dumps({'status': 'PASS', 'native_rational_margins': 31,
                          'whole_field_maps': 6, 'whole_lower_phase_coefficients': 14,
                          'sealed_core_unchanged': True}))
    except (ValueError, TypeError, KeyError, OSError) as exc:
        print('FAIL:', exc, file=sys.stderr)
        raise SystemExit(1)
