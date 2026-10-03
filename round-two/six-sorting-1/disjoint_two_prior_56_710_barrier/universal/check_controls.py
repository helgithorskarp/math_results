"""Four actual semantic damages with repaired complete finite transport hashes."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from run import operations_allow

ROOT = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def main():
    original = (ROOT/'work/proposal.json').read_bytes()
    valid = json.loads(original)
    cases = []
    bad = deepcopy(valid)
    bad['finite']['actual_seed_original_D'] += 1
    bad['finite']['certified_total_lower_bound'] += 1
    cases.append(('false-seed-D', bad, 'Claimed original seed deletion/identity counts differ'))
    bad = deepcopy(valid)
    bad['finite']['full_original_conditional_assignments'].remove(38)
    cases.append(('omitted-actual-input', bad, 'Claimed conditional assignments omit or substitute'))
    bad = deepcopy(valid)
    bad['finite']['conditional_coordinatewise_greatest_pattern'] = 56
    bad['finite']['greatest_pattern_weight'] = 3
    cases.append(('false-greatest-input', bad, 'Claimed greatest conditional input differs'))
    bad = deepcopy(valid)
    chosen = next(row for row in bad['finite']['complete_weight2_output_zero_choices'] if row[0] == 24)
    chosen[1], chosen[2] = [5], 5  # actual weight-two output24 has a ONE at physical5.
    cases.append(('actual-nonzero-head', bad, 'Claimed selected head is not a zero coordinate'))
    records = []
    started = time.monotonic()
    for name, bad, reason in cases:
        bad['finite_sha256'] = digest(bad['finite'])
        file = ROOT/'work'/('damage-'+name+'.json')
        file.write_text(json.dumps(bad, indent=2)+'\n')
        for optimized in (False, True):
            operations_allow()
            command = [sys.executable]+(['-O'] if optimized else [])+[str(ROOT/'verify.py'), str(file)]
            result = subprocess.run(command, env=dict(os.environ), capture_output=True, text=True, timeout=55)
            if result.returncode == 0 or reason not in result.stderr:
                raise ValueError('Semantic damage was not rejected for its intended reason: '+name)
            records.append({'damage': name, 'optimized': optimized,
                            'returncode': result.returncode, 'intended_semantic_reason': reason,
                            'transport_finite_sha256_repaired': True})
    if (ROOT/'work/proposal.json').read_bytes() != original:
        raise ValueError('The genuine original proposal bytes changed')
    finite = {'genuine_proposal_finite_sha256': valid['finite_sha256'], 'controls': records,
              'genuine_proposal_bytes_unchanged': True, 'all8_intended_semantic_rejections': True}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'finite': finite, 'finite_sha256': digest(finite), 'seconds': time.monotonic()-started}
    (ROOT/'work/controls.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
