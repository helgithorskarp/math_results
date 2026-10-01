"""Check a positive monochromatic AP for every mandatory residual cut.

No generator, rectangle constructor, or coverage verifier is imported. This
checker directly evaluates the seven changed colors at each submitted AP.
The full family conclusion additionally needs exact cover-complement checks.
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


class InvalidCertificate(ValueError):
    pass


def require(ok, reason):
    if not ok:
        raise InvalidCertificate(reason)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class Budget:
    def __init__(self):
        self.cases = 0

    def add(self, count=1):
        self.cases += count
        if self.cases > 200000:
            raise RuntimeError('Unchanged200000-case operational limit')


def verify(data, cuts, word, cover_digest, cuts_digest, budget):
    n = len(word)
    budget.add(n + 10)
    require(type(cuts) is dict and set(cuts) == {'length', 'term_count', 'base_bits_sha256', 'cover_sha256', 'cuts'},
            'mandatory cut schema')
    require(type(cuts['length']) is int and cuts['length'] == n and type(cuts['term_count']) is int
            and cuts['term_count'] == 7 and cuts['base_bits_sha256'] == hashlib.sha256(word.encode()).hexdigest()
            and cuts['cover_sha256'] == cover_digest, 'mandatory cut scope')
    mandatory = cuts['cuts']
    require(type(mandatory) is list and len(mandatory) == 2899, 'mandatory cut count')
    previous = None
    for cut in mandatory:
        budget.add(7)
        require(type(cut) is list and len(cut) == 2 and all(type(x) is int for x in cut)
                and 0 <= cut[0] < cut[1] <= n, 'mandatory cut geometry')
        require(previous is None or previous < cut, 'mandatory cut order')
        previous = cut
    require(type(data) is dict and set(data) == {'length', 'term_count', 'base_bits_sha256', 'cover_sha256',
                                               'residual_cuts_sha256', 'points'}, 'point certificate schema')
    require(type(data['length']) is int and data['length'] == n, 'point interval length')
    require(type(data['term_count']) is int and data['term_count'] == 7, 'point term count')
    require(data['base_bits_sha256'] == hashlib.sha256(word.encode()).hexdigest(), 'point word digest')
    require(data['cover_sha256'] == cover_digest, 'point cover digest')
    require(data['residual_cuts_sha256'] == cuts_digest, 'point residual digest')
    points = data['points']
    require(type(points) is list and len(points) == len(mandatory), 'point count')
    colors = [0, 0]
    for cut, point in zip(mandatory, points):
        budget.add(22)
        require(type(point) is list and len(point) == 4 and all(type(x) is int for x in point), 'integer point coordinates')
        left, right, a, d = point
        require([left, right] == cut, 'mandatory cut order/coverage')
        require(a >= 1 and d >= 1 and a + 6 * d <= n, 'actual nonconstant seven-term AP')
        changed = []
        for k in range(7):
            position = a + k * d
            changed.append(int(word[position - 1]) ^ int(left < position <= right))
        require(all(c == changed[0] for c in changed), 'actual AP is bichromatic')
        colors[changed[0]] += 1
    return {'status': 'ALL2899_MANDATORY_RESIDUAL_CUTS_HAVE_DIRECTLY_CHECKED_MONO_APS',
            'mandatory_cuts': len(mandatory), 'APs_verified': len(points), 'actual_term_color_checks': 7 * len(points),
            'AP_color_counts': colors, 'complete_residual_coverage': True,
            'full_family_conclusion_needs_exact_cover_complement': True}


CONTROLS = {'empty_points': 'point count', 'missing_point': 'point count',
            'duplicate_cut': 'mandatory cut order/coverage', 'wrong_cut': 'mandatory cut order/coverage',
            'boolean_coordinate': 'integer point coordinates', 'zero_step': 'actual nonconstant seven-term AP',
            'outside_word': 'actual nonconstant seven-term AP', 'bichromatic_AP': 'actual AP is bichromatic',
            'wrong_length': 'point interval length', 'unsupported_terms': 'point term count',
            'wrong_word_digest': 'point word digest', 'wrong_cover_digest': 'point cover digest',
            'wrong_residual_digest': 'point residual digest', 'extra_hypothesis': 'point certificate schema'}


def corrupt(data, control):
    data = copy.deepcopy(data)
    if control == 'empty_points':
        data['points'] = []
    elif control == 'missing_point':
        data['points'].pop()
    elif control == 'duplicate_cut':
        data['points'][-1] = copy.deepcopy(data['points'][0])
    elif control == 'wrong_cut':
        data['points'][0][:2] = [0, 3704]
    elif control == 'boolean_coordinate':
        data['points'][0][2] = True
    elif control == 'zero_step':
        data['points'][0][3] = 0
    elif control == 'outside_word':
        data['points'][0][2] = 3704
    elif control == 'bichromatic_AP':
        data['points'][0][2:] = [2, 617]
    elif control == 'wrong_length':
        data['length'] = 3703
    elif control == 'unsupported_terms':
        data['term_count'] = 8
    elif control == 'wrong_word_digest':
        data['base_bits_sha256'] = '0' * 64
    elif control == 'wrong_cover_digest':
        data['cover_sha256'] = '0' * 64
    elif control == 'wrong_residual_digest':
        data['residual_cuts_sha256'] = '0' * 64
    else:
        data['assume_symmetric'] = True
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--word', type=Path, required=True)
    parser.add_argument('--cover', type=Path, required=True)
    parser.add_argument('--cuts', type=Path, required=True)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--control', choices=list(CONTROLS))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    began = time.monotonic()
    require(not args.output.exists(), 'Existing evidence cannot be overwritten')
    word = args.word.read_text().strip()
    require(len(word) == 3704 and set(word) <= {'0', '1'}, 'binary base word')
    cuts, data = json.loads(args.cuts.read_text()), json.loads(args.certificate.read_text())
    budget = Budget()
    if args.control:
        try:
            result = verify(corrupt(data, args.control), cuts, word, sha(args.cover), sha(args.cuts), budget)
        except InvalidCertificate as error:
            require(str(error) == CONTROLS[args.control], 'Control hit wrong defect: ' + str(error))
            result = {'status': 'MATHEMATICAL_CORRUPTION_REJECTED', 'control': args.control, 'reason': str(error)}
        else:
            raise RuntimeError('Corruption passed verification')
    else:
        result = verify(data, cuts, word, sha(args.cover), sha(args.cuts), budget)
    result.update(agent='six-vdw-1', role='researcher', checked_at=datetime.now(timezone.utc).isoformat(),
                  word_sha256=sha(args.word), cover_sha256=sha(args.cover), residual_cuts_sha256=sha(args.cuts),
                  certificate_sha256=sha(args.certificate), checker_sha256=sha(__file__),
                  conservative_combined_cases=budget.cases, seconds=time.monotonic() - began,
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, interpreter_optimization=sys.flags.optimize,
                  threads=1, full_family_exclusion_from_point_checker_alone=False, new_W_bound=None)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'cases': budget.cases}), flush=True)


if __name__ == '__main__':
    main()
