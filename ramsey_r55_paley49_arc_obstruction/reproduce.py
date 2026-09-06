"""Replay the finite certificate and controls; the published theorem is imported."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import build
import check
import controls
import extract
import verify_witness


def main():
    root = Path(__file__).resolve().parent
    os.chdir(root)
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        check.need(hashlib.sha256((root/name).read_bytes()).hexdigest() == digest, 'manifest: '+name)
    generated = build.build()
    check.need((json.dumps(generated, separators=(',', ':'))+'\n').encode() == (root/'certificate.json').read_bytes(), 'regenerated certificate identity')
    result = check.check(json.loads((root/'certificate.json').read_text()))
    check.need(result == json.loads((root/'expected.json').read_text()), 'expected certificate output')
    check.need(controls.main() == json.loads((root/'expected_controls.json').read_text()), 'expected controls')
    output = extract.extract(json.loads((root/'fixture.json').read_text()))
    check.need(output == json.loads((root/'fixture_witness.json').read_text()), 'physical fixture identity')
    verify_witness.verify(output)
    flags = ['-B']+(['-O'] if sys.flags.optimize else [])
    separation = json.loads(subprocess.check_output([sys.executable, *flags, 'separation.py',
        '../ramsey_r55_catalog_switch_extensions/r55_42some.g6'], text=True))
    check.need(separation == json.loads((root/'separation.json').read_text()), 'family separation')
    print(json.dumps({'status':'VERIFIED_PALEY49_SWITCH_OBSTRUCTION_WITH_HILL_LOVE_PREMISE',
                      'affine_cases':714, 'physical_witness_pairs':7140,
                      'maximum_unswitched_K5_free_subset_upper_bound':21,
                      'excluded_switched_subset_orders':'>=43',
                      'published_classification_imported':True,
                      'classification_recomputed':False,
                      'ramsey_bound_improved':False}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
