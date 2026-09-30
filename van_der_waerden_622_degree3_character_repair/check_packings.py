"""Definition-level checker: no discovery code, SAT model, or solver input.

Python 3.10+, standard library. All positions in certificates are one-based.
The mathematical reduction from arbitrary coefficients is in PROOF.md.
"""
import argparse
import hashlib
import json
from pathlib import Path


class InvalidCertificate(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidCertificate(message)


def evaluate(coefficients, x):
    value = 0
    for coefficient in reversed(coefficients):
        value = (value*x + coefficient) % 311
    return value


def check(data):
    require(isinstance(data, dict), 'certificate must be an object')
    require(set(data) == {'field', 'period', 'packing_size', 'cases'}, 'certificate keys')
    require(type(data['field']) is int and data['field'] == 311, 'field must be 311')
    require(type(data['period']) is int and data['period'] == 622, 'period must be 622')
    require(type(data['packing_size']) is int and data['packing_size'] == 20, 'packing must have size 20')
    expected = [[(-a) % 311, 0, 1] for a in (0, 1, 11)]
    expected += [[0, (-a) % 311, 0, 1] for a in (0, 1, 11)]
    expected += [[1, a, 0, 1] for a in range(311)]
    require(isinstance(data['cases'], list) and len(data['cases']) == 317, '317 cases required')
    require(all(isinstance(c, dict) and set(c) == {'coefficients', 'aps'}
                for c in data['cases']), 'case keys')
    require([c['coefficients'] for c in data['cases']] == expected, 'canonical case coverage/order')
    terms = 0
    aps = 0
    largest_position = 0
    for case_index, case in enumerate(data['cases']):
        coefficients = case['coefficients']
        require(all(type(x) is int for x in coefficients), 'integer coefficients required')
        require(isinstance(case['aps'], list) and len(case['aps']) == 20, '20 APs per case required')
        used_residues = set()
        for pair in case['aps']:
            require(isinstance(pair, list) and len(pair) == 2, 'AP is [start,difference]')
            a, d = pair
            require(type(a) is int and type(d) is int, 'AP parameters must be integers')
            require(1 <= a <= 311 and 1 <= d <= 310, 'AP parameter range')
            positions = [a+j*d for j in range(7)]
            require(positions[-1] <= 2171, 'AP must be in [1,2171]')
            colors = []
            support = set()
            for position in positions:
                t = position-1
                residue = t % 311
                value = evaluate(coefficients, residue)
                require(value != 0, f'root used in case {case_index}')
                euler = pow(value, 155, 311)
                require(euler in (1, 310), 'nonzero quadratic character')
                bit = int(euler == 1)
                colors.append((t % 2) ^ bit)
                support.add(residue)
                terms += 1
            require(len(support) == 7, 'seven distinct field residues required')
            require(len(set(colors)) == 1, f'AP not monochromatic in case {case_index}')
            require(used_residues.isdisjoint(support), f'overlapping supports in case {case_index}')
            used_residues.update(support)
            largest_position = max(largest_position, positions[-1])
            aps += 1
        require(len(used_residues) == 140, '140 distinct non-root residues per case required')
    require(aps == 6340 and terms == 44380, 'complete certificate coverage')
    return {'status': 'ALL_ROOT_FREE_DISJOINT_AP_PACKINGS_VERIFIED',
            'canonical_cases': 317, 'APs_checked': aps, 'integer_term_colors_checked': terms,
            'non_root_residues_per_case': 140, 'packing_size': 20,
            'largest_certified_position': largest_position,
            'non_root_column_repair_lower_bound': 20,
            'length3704_non_root_coordinate_repair_lower_bound': 220,
            'coefficient_coverage': 'PROOF.md, with arithmetic audits; not a 24-billion-case enumeration',
            'new_W_bound': None}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', nargs='?', type=Path,
                        default=Path(__file__).with_name('packings.json'))
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    result = check(json.loads(raw))
    result['certificate_sha256'] = hashlib.sha256(raw).hexdigest()
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
