#!/usr/bin/env python3
"""Optimization-independent census and deliberately malformed cover controls."""
from pathlib import Path
import argparse
import copy
import json
import subprocess
import sys
import audit
import verify


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    a = p.parse_args()
    root = Path(__file__).resolve().parent
    work = a.work.resolve()
    audit.require(not work.is_relative_to(root.parent), 'control output outside Git')
    work.mkdir(parents=True, exist_ok=True)
    for tag, options in (('normal', []), ('optimized', ['-O'])):
        subprocess.run([sys.executable]+options+[str(root / 'cores.py'), '--output', str(work / (tag+'_cover.json'))], check=True)
        subprocess.run([sys.executable]+options+[str(root / 'audit.py'), '--cover', str(work / (tag+'_cover.json')),
                                                '--report', str(work / (tag+'_audit.json'))], check=True)
    for part in ('cover', 'audit'):
        audit.require((work / ('normal_'+part+'.json')).read_bytes() == (work / ('optimized_'+part+'.json')).read_bytes(),
                      'optimized '+part+' mismatch')
    cover = json.loads((work / 'normal_cover.json').read_text())
    checked = verify.invariants(cover)
    rejected = []
    for name in ('missing_class', 'duplicate_class', 'missing_member', 'wrong_representative'):
        bad = copy.deepcopy(cover)
        if name == 'missing_class':
            bad['cases'].pop()
        elif name == 'duplicate_class':
            bad['cases'][1] = bad['cases'][0]
        elif name == 'missing_member':
            bad['cases'][0]['members'] = []
        else:
            bad['cases'][0]['bits'] = '111111111'
        try:
            audit.audit_cover(bad)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('accepted malformed cover: '+name)
    report = dict(optimized_cover_identical=True, optimized_audit_identical=True,
                  rejected_cover_mutations=rejected, literal_invariant_checks=checked)
    (work / 'controls.json').write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print('PASS controls '+json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
