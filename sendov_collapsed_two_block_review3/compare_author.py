#!/usr/bin/env python3
"""Optional original-source replay and all-parameter coefficient comparison.

Usage: python3 -I -B compare_author.py /path/to/original/verify.py
The independent checker does not call this optional author-code replay.
"""
from pathlib import Path
from hashlib import sha256
import argparse
import contextlib
import importlib.util
import io
import json
import sys

HERE = Path(__file__).resolve().parent
ORIGINAL_SHA256 = '8f85b2a9e0d1c7703a60e051d8ab75844efdca69e00e32880f688b6eb13b1d2c'

def demand(ok, message):
    if not ok:
        raise ValueError(message)

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original', type=Path)
    args = parser.parse_args()
    original_path = args.original.resolve()
    demand(sha256(original_path.read_bytes()).hexdigest() == ORIGINAL_SHA256,
           'Original input SHA256 mismatch; no original code executed')
    original = load('quartic_original_author_replay', original_path)
    native = load('quartic_independent_review', HERE/'independent_check.py')
    captured = {}

    def capture(frame, event, arg):
        if event == 'return' and frame.f_code is original.run.__code__:
            captured.update(frame.f_locals)

    stdout = io.StringIO()
    previous_profile = sys.getprofile()
    with contextlib.redirect_stdout(stdout):
        sys.setprofile(capture)
        try:
            original.run()
        finally:
            sys.setprofile(previous_profile)
    manifest = json.loads(stdout.getvalue())
    demand(manifest['status'] == 'PASS' and manifest['exact_checks'] == 60
           and manifest['rejected_coefficient_mutations'] == 5,
           'Original reproduction manifest mismatch')
    raw = {label: [{'real': c[0].data(), 'imaginary': c[1].data()}
                   for c in captured[label]] for label in ('gap', 'energy')}

    total, energy = native.calculate(native.S, -native.RR, 4, 'author comparison')
    total[0] = total[0] - 2*native.M*native.V
    entries = []
    for label, values in [('gap', total), ('energy', energy)]:
        for j, value in enumerate(values):
            for part, ours in [('real', value), ('imaginary', native.R())]:
                entry = raw[label][j][part]
                numerator = native.P({(int(m), int(r), 0): native.F(c)
                    for m, r, c in entry['numerator_terms_m_r']})
                den = entry['denominator_exponents_m_3mplus2_mplus2']
                # Author units m,D,m+2; ours m,D,m+1. Clear both separately.
                author_units = [native.UNITS[0], native.UNITS[1], native.UNITS[0]+2]
                author_den = author_units[0]**den[0]*author_units[1]**den[1]*author_units[2]**den[2]
                ours_den = native.UNITS[0]**ours.den[0]*native.UNITS[1]**ours.den[1]*native.UNITS[2]**ours.den[2]
                demand(not (ours.num*author_den-numerator*ours_den).t,
                       'Generic coefficient differs: '+repr((label, j, part)))
                entries.append([label, j, part])
    demand(len(entries) == 20, 'Incomplete coefficient comparison')
    print(json.dumps({
        'reviewer': 'six-reviewer-3', 'role': 'independent mathematical reviewer',
        'status': 'ORIGINAL REPRODUCED AND ALL 20 GENERIC COEFFICIENT ENTRIES AGREE',
        'original_source_commit': 'c8fc799c8c2455b7973e900d51d8a83be001bafe',
        'original_verify_sha256': ORIGINAL_SHA256,
        'author_exact_checks': manifest['exact_checks'],
        'author_rejected_coefficient_mutations': manifest['rejected_coefficient_mutations'],
        'generic_coefficient_entries_compared': len(entries),
        'captured_coefficient_sha256': sha256(json.dumps(raw, sort_keys=True,
            separators=(',', ':')).encode()).hexdigest(),
        'trust_boundary': 'Optional author-code replay after SHA256 verification; '
            'all coefficients compared as rational identities in m,r. '
            'The independent checker does not import this replay or author code.'
    }, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
