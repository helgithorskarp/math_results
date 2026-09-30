"""Frozen exact certificate replay; numerical packages are not imported."""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import controls
import verify
import verify_fractional


def replay(root):
    base = root / 'base'
    proof_path = root / 'certificates/cover2-phase184-far55.json'
    frac_path = root / 'certificates/fractional-phase184-far55.json'
    proof = verify.check(json.loads(proof_path.read_bytes()), base)
    fraction = verify_fractional.check(json.loads(frac_path.read_bytes()), base)
    frac_data = json.loads(frac_path.read_bytes())
    point_weights = dict(frac_data['position_weights']); Q = frac_data['denominator']
    violated_cuts = []
    for cut in proof['cover2_cuts']:
        union = {a+j*d for a,d in cut['triple_APs'] for j in range(7)}
        weight = sum(point_weights.get(x,0) for x in union)
        if weight >= 2*Q:
            raise ValueError('Expected integer cut not violated by the fractional point')
        violated_cuts.append({'triple_APs':cut['triple_APs'],
             'fractional_union_weight':str(Fraction(weight,Q)),
             'integer_required_count':2, 'violation':str(Fraction(2*Q-weight,Q))})
    negative = controls.run(root)
    manifest = {}
    for path in sorted([base/'certificates/phase-184.json', proof_path, frac_path]):
        manifest[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    lines = ''.join(f'{sha}  {name}\n' for name, sha in sorted(manifest.items()))
    if (root/'SHA256SUMS').read_text() != lines:
        raise ValueError('Certificate manifest bytes differ')
    return {'agent':'six-vdw-3', 'role':'researcher',
            'status':'EXACT_INTEGER_EXCLUSION_AND_FRACTIONAL_FEASIBILITY',
            'integer_exclusion':proof, 'fractional_feasibility':fraction,
            'fractional_cover2_violations':violated_cuts,
            'negative_controls':negative, 'certificate_hashes':manifest,
            'manifest_sha256':hashlib.sha256(lines.encode()).hexdigest(),
            'trust':'integer/rational arithmetic and written bridges; no solver or external review trusted'}


def main():
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path)
    args = p.parse_args(); root = Path(__file__).resolve().parent
    out = replay(root)
    if out != json.loads((root/'expected.json').read_text()):
        raise ValueError('Full entry-level expected result differs')
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'status':out['status'], 'far_edit_lower_bound':56,
          'strict_gap':out['integer_exclusion']['strict_gap'],
          'fractional_class_sum':out['fractional_feasibility']['weighted_class_sum'],
          'fractional_far_sum':out['fractional_feasibility']['weighted_far_sum'],
          'checked_integer_APs':out['fractional_feasibility']['checked_integer_APs'],
          'rejected_controls':out['negative_controls']['rejected_controls'],
          'manifest_sha256':out['manifest_sha256']}))


if __name__ == '__main__': main()
