"""Small independent soundness controls and complete binary-run checks."""
from collections import Counter
import argparse
from itertools import product
import json
from math import comb
from pathlib import Path
import tempfile

from audit import Invalid, need, verify, reconstruct


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path)
    parser.add_argument('--CNF', type=Path)
    args = parser.parse_args()
    accepted = rejected = 0
    with tempfile.TemporaryDirectory(prefix='qr617-review-') as temporary:
        root = Path(temporary)
        cnf, proof = root / 'tiny.cnf', root / 'tiny.lrat'
        square = 'p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n'
        correct = '5 1 0 1 2 0\n6 -1 0 3 4 0\n7 0 5 6 0\n'
        cnf.write_text(square)
        for trace in [correct, correct.replace('7 0', '6 d 1 2 0\n7 0')]:
            proof.write_text(trace)
            r = verify(cnf, proof)
            need(r['RUP_additions'] == 3 and r['hint_reads'] == 6, 'Positive fixture count')
            accepted += 1
        failures = [
            ('nonunit hint', correct.replace('5 1 0', '5 0'), 'Nonunit hint'),
            ('satisfied hint', correct.replace('1 2 0\n6', '1 1 0\n6'), 'Satisfied hint'),
            ('missing conflict', correct.replace('1 2 0\n6', '1 0\n6'), 'No RUP conflict'),
            ('false hint id', correct.replace('1 2 0\n6', '1 99 0\n6'), 'Unavailable proof hint'),
            ('negative hint', correct.replace('1 2 0\n6', '1 -2 0\n6'), 'Positive RUP hints required'),
            ('duplicate literal', correct.replace('5 1 0', '5 1 1 0'), 'Duplicate proof literal'),
            ('tautology', correct.replace('5 1 0', '5 1 -1 0'), 'Tautological proof clause'),
            ('bad variable', correct.replace('5 1 0', '5 3 0'), 'Proof variable domain'),
            ('stale id', correct.replace('5 1 0', '4 1 0'), 'Fresh proof identifier'),
            ('deleted hint', correct.replace('7 0', '6 d 5 0\n7 0'), 'Unavailable proof hint'),
            ('bad deletion', correct.replace('7 0', '6 d 99 0\n7 0'), 'Unavailable deletion'),
            ('no terminal', correct.rsplit('7 0', 1)[0], 'No terminal empty clause'),
            ('post terminal', correct + '8 0 5 6 0\n', 'Content after empty clause'),
            ('extra hints', correct.replace('1 2 0\n6', '1 2 3 0\n6'), 'Hints after conflict'),
            ('malformed ending', correct.replace('1 2 0\n6', '1 2\n6'), 'Proof terminators'),
        ]
        for name, trace, message in failures:
            proof.write_text(trace)
            try:
                verify(cnf, proof)
            except Invalid as error:
                need(str(error) == message, name + ': unexpected rejection ' + str(error))
                rejected += 1
            else:
                raise Invalid('Accepted false proof: ' + name)
        encoding_rejections = 0
        if args.source is not None:
            need(args.CNF is not None, 'CNF required for encoding controls')
            rows = args.CNF.read_text().splitlines()
            nv, nc = map(int, rows[0].split()[2:])
            variants = []
            wrong_unit = list(rows)
            index = next(i for i, row in enumerate(rows) if row == '-1 0')
            wrong_unit[index] = '1 0'
            variants.append(wrong_unit)
            missing = list(rows[:-1])
            missing[0] = f'p cnf {nv} {nc - 1}'
            variants.append(missing)
            extra = list(rows) + ['-2 0']
            extra[0] = f'p cnf {nv} {nc + 1}'
            variants.append(extra)
            wrong_ap = list(rows)
            index = next(i for i, row in enumerate(rows[1:], 1) if len(row.split()) == 8)
            values = list(map(int, wrong_ap[index].split()))
            values[0] *= -1
            wrong_ap[index] = ' '.join(map(str, values))
            variants.append(wrong_ap)
            changed = root / 'changed.cnf'
            for variant in variants:
                changed.write_text('\n'.join(variant) + '\n')
                try:
                    reconstruct(args.source, changed, 3)
                except Invalid as error:
                    need(str(error) == 'Complete clause multiset mismatch', 'Wrong encoding rejection')
                    encoding_rejections += 1
                else:
                    raise Invalid('Accepted changed encoding')
            altered = root / 'altered-inputs'
            altered.mkdir()
            word = (args.source / 'base3704.bits').read_bytes()
            pool = (args.source / 'AP-pool.json').read_text()
            (altered / 'base3704.bits').write_bytes(word)
            data = json.loads(pool)
            data['APs'][0][0] = True
            (altered / 'AP-pool.json').write_text(json.dumps(data))
            try:
                reconstruct(altered, args.CNF, 3)
            except Invalid as error:
                need(str(error) == 'Actual nonconstant AP domain', 'Boolean AP rejection')
                encoding_rejections += 1
            else:
                raise Invalid('Accepted Boolean AP coordinate')
            (altered / 'AP-pool.json').write_text(pool)
            changed_word = bytes([ord('1') if word[0] == ord('0') else ord('0')]) + word[1:]
            (altered / 'base3704.bits').write_bytes(changed_word)
            try:
                reconstruct(altered, args.CNF, 3)
            except Invalid as error:
                need(str(error) == 'Literal QR617 word', 'Changed word rejection')
                encoding_rejections += 1
            else:
                raise Invalid('Accepted changed literal word')
    total = normalized = endpoint_checks = 0
    for n in range(1, 11):
        counts = Counter()
        canonical = Counter()
        for bits in product([0, 1], repeat=n):
            one = sum(x == 1 and (i == 0 or bits[i - 1] == 0)
                      for i, x in enumerate(bits))
            zero = sum(x == 0 and (i == 0 or bits[i - 1] == 1)
                       for i, x in enumerate(bits))
            transition = sum(x != y for x, y in zip(bits, bits[1:]))
            counts[one] += 1
            if bits[0] == 0:
                canonical[one] += 1
            need(one + zero == transition + 1, 'Run-transition identity')
            if one <= 3 and one >= 3 and zero >= 3:
                need(bits[0] == 0 or (bits[-1] == 0 and zero == 3),
                     'Three-run complement normalization')
                normalized += 1
            if one >= 4 and zero >= 4:
                need(transition >= (8 if bits[0] == bits[-1] else 7),
                     'Endpoint-conditioned transition bound')
                endpoint_checks += 1
            total += 1
        for k in range((n + 1) // 2 + 1):
            need(counts[k] == comb(n + 1, 2 * k), 'Full cut count')
            need(canonical[k] == comb(n, 2 * k), 'Canonical cut count')
    result = {
        'agent': 'six-reviewer-5', 'role': 'independent reviewer',
        'valid_proof_fixtures': accepted, 'targeted_false_proofs_rejected': rejected,
        'targeted_encoding_and_input_corruptions_rejected': encoding_rejections,
        'binary_masks_checked_through_length_10': total,
        'three_run_normalization_controls': normalized,
        'endpoint_transition_controls': endpoint_checks,
        'atmost_three_masks_N3704': sum(comb(3705, 2 * k) for k in range(4)),
        'canonical_atmost_three_masks_N3704': sum(comb(3704, 2 * k) for k in range(4)),
        'exactly_three_masks_N3704': comb(3705, 6),
        'status': 'ALL_CONTROLS_PASS',
        'scope': 'Small controls validate code; written reductions cover the general domain.'}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
