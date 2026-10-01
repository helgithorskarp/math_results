"""Independent Horner/Euler checks of actual reflected integer AP pairs.

Imports no proposer or reflection formula. Both APs are supplied explicitly;
their actual colors and negative field supports are checked directly.
"""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

PILOT = [0, 1, 2, 3, 4, 10, 157, 313, 314, 315, 469, 624]


class InvalidCertificate(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise InvalidCertificate(reason)


class Budget:
    def __init__(self):
        self.cases = 0

    def add(self, count=1):
        self.cases += count
        if self.cases > 200000:
            raise RuntimeError('unchanged200000-case operational limit')


def expected_coefficients(index):
    if index == 0:
        return [0, 0, 0, 0, 1]
    if index == 1:
        return [1, 0, 0, 0, 1]
    if index == 2:
        return [11, 0, 0, 0, 1]
    if 3 <= index < 314:
        return [index - 3, 0, 1, 0, 1]
    return [index - 314, 0, 11, 0, 1]


def verify(data, scope, budget):
    indexes = PILOT if scope == 'pilot' else list(range(625))
    require(type(data) is dict and set(data) == {'modulus', 'pairs_per_case', 'cases'}, 'certificate schema')
    budget.add(2)
    require(type(data['modulus']) is int and data['modulus'] == 311, 'modulus311')
    require(type(data['pairs_per_case']) is int and data['pairs_per_case'] == 12, 'supported pair bound12')
    require(type(data['cases']) is list and len(data['cases']) == len(indexes), 'mandatory case coverage')
    APs, terms, largest = 0, 0, 0
    for index, case in zip(indexes, data['cases']):
        budget.add()
        require(type(case) is dict and set(case) == {'index', 'coefficients', 'pairs'}, 'case schema')
        require(type(case['index']) is int and case['index'] == index, 'ordered canonical case index')
        coefficients = case['coefficients']
        require(type(coefficients) is list and len(coefficients) == 5, 'coefficient schema')
        budget.add(5)
        require(all(type(x) is int and 0 <= x < 311 for x in coefficients), 'integer field coefficients')
        require(coefficients == expected_coefficients(index), 'exact canonical coefficients')
        require(type(case['pairs']) is list and len(case['pairs']) == 12, 'twelve packing pairs')
        used = set()
        for pair in case['pairs']:
            budget.add()
            require(type(pair) is list and len(pair) == 2, 'two explicit APs per pair')
            supports, steps = [], []
            for ap in pair:
                budget.add(3)
                require(type(ap) is list and len(ap) == 2, 'AP coordinate schema')
                a, d = ap
                require(type(a) is int and type(d) is int, 'integer AP coordinates')
                require(1 <= a <= 311 and 1 <= d <= 310, 'canonical actual AP geometry')
                positions = [a + j * d for j in range(7)]
                require(positions[-1] <= 2171, 'actual interval2171')
                residues, colors = set(), []
                for position in positions:
                    budget.add()
                    x = (position - 1) % 311
                    value = 0
                    for coefficient in reversed(coefficients):
                        value = (value * x + coefficient) % 311
                    require(value != 0, 'root term')
                    character = pow(value, 155, 311)
                    require(character in (1, 310), 'Euler character')
                    colors.append(((position - 1) % 2) ^ int(character == 1))
                    residues.add(x)
                    terms += 1
                require(len(residues) == 7, 'seven distinct field residues')
                require(len(set(colors)) == 1, 'bichromatic AP')
                require(not used.intersection(residues), 'overlapping field supports')
                used.update(residues)
                supports.append(residues)
                steps.append(d)
                APs += 1
                largest = max(largest, positions[-1])
            budget.add(2)
            require(steps[0] == steps[1], 'reflection step mismatch')
            require(supports[1] == {(-x) % 311 for x in supports[0]}, 'incorrect negative field support')
        require(len(used) == 168, '168 disjoint nonroot residues')
    require(APs == 24 * len(indexes) and terms == 168 * len(indexes), 'complete AP/term coverage')
    return {'status': 'VERIFIED_REFLECTION_PAIRED_ROOT_FREE_AP_PACKINGS',
            'scope': scope, 'indexes': indexes, 'cases': len(indexes), 'pairs_per_case': 12,
            'APs_per_case': 24, 'APs_checked': APs, 'actual_term_colors_checked': terms,
            'field_residues_per_case': 168, 'largest_canonical_position': largest,
            'transported_interval_bound': 2171, 'nonroot_field_repair_floor_for_checked_cases': 24,
            'template_coordinate_repair_floor_at3704_for_checked_cases': 264,
            'unrestricted_coordinate_repair_floor_at2171_for_checked_cases': 24,
            'all625_cases_checked': scope == 'all', 'all_root_bits_independent_and_unrestricted': True,
            'packing_optimality_claim': False, 'unrestricted_nonexistence_claim': False, 'new_W_bound': None}


CONTROLS = {
    'missing_case': 'mandatory case coverage',
    'duplicate_case': 'ordered canonical case index',
    'zero_polynomial': 'exact canonical coefficients',
    'wrong_quadratic_class': 'exact canonical coefficients',
    'root_term': 'root term',
    'bichromatic_AP': 'bichromatic AP',
    'within_pair_overlap': 'overlapping field supports',
    'between_pair_overlap': 'overlapping field supports',
    'wrong_reflection': 'incorrect negative field support',
    'missing_pair': 'twelve packing pairs',
    'missing_reflection_member': 'two explicit APs per pair',
    'boolean_index': 'ordered canonical case index',
    'boolean_start': 'integer AP coordinates',
    'zero_start': 'canonical actual AP geometry',
    'zero_step': 'canonical actual AP geometry',
    'step311': 'canonical actual AP geometry',
    'outside_interval': 'canonical actual AP geometry',
    'extra_root_hypothesis': 'certificate schema',
    'unsupported_bound': 'supported pair bound12',
    'wrong_modulus': 'modulus311',
    'wrong_constant': 'exact canonical coefficients',
    'reversed_coefficients': 'exact canonical coefficients',
}


def corrupt(data, name):
    changed = copy.deepcopy(data)
    first = changed['cases'][0]
    if name == 'missing_case':
        changed['cases'].pop()
    elif name == 'duplicate_case':
        changed['cases'][-1] = copy.deepcopy(first)
    elif name == 'zero_polynomial':
        first['coefficients'] = [0] * 5
    elif name == 'wrong_quadratic_class':
        next(c for c in changed['cases'] if c['index'] == 314)['coefficients'][2] = 1
    elif name == 'root_term':
        first['pairs'][0][0] = [1, 2]
    elif name == 'bichromatic_AP':
        first['pairs'][0][0] = [2, 1]
    elif name == 'within_pair_overlap':
        first['pairs'][0][1] = copy.deepcopy(first['pairs'][0][0])
    elif name == 'between_pair_overlap':
        first['pairs'][1] = copy.deepcopy(first['pairs'][0])
    elif name == 'wrong_reflection':
        d = first['pairs'][0][0][1]
        replacement = next(ap for pair in first['pairs'][1:] for ap in pair if ap[1] == d)
        first['pairs'][0][1] = copy.deepcopy(replacement)
    elif name == 'missing_pair':
        first['pairs'].pop()
    elif name == 'missing_reflection_member':
        first['pairs'][0].pop()
    elif name == 'boolean_index':
        first['index'] = False
    elif name == 'boolean_start':
        first['pairs'][0][0][0] = True
    elif name == 'zero_start':
        first['pairs'][0][0][0] = 0
    elif name == 'zero_step':
        first['pairs'][0][0][1] = 0
    elif name == 'step311':
        first['pairs'][0][0][1] = 311
    elif name == 'outside_interval':
        first['pairs'][0][0][0] = 2172
    elif name == 'extra_root_hypothesis':
        changed['uniform_root_bit'] = 0
    elif name == 'unsupported_bound':
        changed['pairs_per_case'] = 13
    elif name == 'wrong_modulus':
        changed['modulus'] = 313
    elif name == 'wrong_constant':
        first['coefficients'][0] = 1
    elif name == 'reversed_coefficients':
        first['coefficients'].reverse()
    else:
        raise RuntimeError('unknown corruption')
    return changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--scope', choices=['pilot', 'all'], required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--control', choices=list(CONTROLS))
    args = parser.parse_args()
    require(not args.output.exists(), 'output already exists')
    began, budget = time.monotonic(), Budget()
    raw = args.certificate.read_bytes()
    data = json.loads(raw)
    if args.control:
        try:
            verify(corrupt(data, args.control), args.scope, budget)
        except InvalidCertificate as error:
            require(str(error) == CONTROLS[args.control], 'unexpected corruption-rejection reason')
            result = {'status': 'MATHEMATICAL_CORRUPTION_REJECTED', 'control': args.control,
                      'reason': str(error), 'scope': args.scope}
        else:
            raise InvalidCertificate('corruption incorrectly accepted')
    else:
        result = verify(data, args.scope, budget)
    result.update(agent='six-vdw-1', role='researcher', checked_at=datetime.now(timezone.utc).isoformat(),
                  certificate_sha256=hashlib.sha256(raw).hexdigest(),
                  checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  conservative_combined_cases=budget.cases, seconds=time.monotonic() - began,
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  interpreter_optimization=sys.flags.optimize, generator_or_solver_imported=False,
                  external_independent_review=False, hard_child_seconds=30, case_cap=200000, threads=1)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'conservative_combined_cases', 'seconds']}), flush=True)


if __name__ == '__main__':
    main()
