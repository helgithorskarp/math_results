"""Reproduce the entire independent record without author imports."""
import argparse
import hashlib
import json
from pathlib import Path

import adversarial
import independent
import refinements


def run():
    first = independent.run()
    first_bytes = (json.dumps(first, indent=2) + '\n').encode()
    seal = json.loads(Path(__file__).with_name('FIRST_SEAL.json').read_text())
    independent.require(
        hashlib.sha256(first_bytes).hexdigest() == seal['files']['first-record.json'],
        'Entire first record differs from the pre-author-code seal',
    )
    independent.require(
        hashlib.sha256(Path(independent.__file__).read_bytes()).hexdigest()
        == seal['files']['independent.py'],
        'First independent engine differs from the pre-author-code seal',
    )
    return {
        'agent': 'six-reviewer-5',
        'role': 'independent mathematical reviewer',
        'first_sealed_record': first,
        'literal_and_quantitative_record': refinements.run(),
        'damage_record': adversarial.run(),
        'all_n_scope': 'The written PSD/kernel/weight/moment/induction proof supplies unbounded coverage; finite controls do not.',
        'no_author_module_imports': True,
        'no_solver_or_floating_input': True,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    record = run()
    raw = (json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n').encode()
    if args.check:
        independent.require(args.check.read_bytes() == raw, 'Whole frozen independent record mismatch')
    if args.output:
        args.output.write_bytes(raw)
    print(json.dumps({
        'ok': True,
        'record_sha256': hashlib.sha256(raw).hexdigest(),
        'coefficient_controls': sum(v['edges'] for v in record['first_sealed_record']['identities']),
        'constant_controls': len(record['first_sealed_record']['identities']),
        'literal_original_entries': sum(v['full_original_entries'] for v in record['literal_and_quantitative_record']['literal_original_controls']),
        'point_star_equations': sum(v['point_star_equations'] for v in record['literal_and_quantitative_record']['literal_original_controls']),
        'damage_controls': len(record['damage_record']['damage_controls']) + 2,
        'eleven': record['literal_and_quantitative_record']['quantitative_consequences'][0],
    }))
