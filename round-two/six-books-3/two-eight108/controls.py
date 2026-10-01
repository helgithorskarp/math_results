#!/usr/bin/env python3
"""Reject damaged coverage, equal-deficit tags and static support certificates."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import verify

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def compute():
    certificate = json.loads((HERE / 'certificate.json').read_text())
    keys, census = verify.incidence_census()
    good = verify.verify_certificate(certificate, keys, census)
    pair_index = next(i for i, entry in enumerate(certificate['entries'])
                      if entry['exclusion']['type'] == 'star_pair_cover')
    empty_index = next(i for i, entry in enumerate(certificate['entries'])
                       if entry['exclusion']['type'] == 'empty_star' and any(entry['domain_sizes']))
    pair = certificate['entries'][pair_index]
    frame = verify.LiteralFrame(verify.NEIGHBORS,
                               verify.rows_from_key(verify.validate_key(pair['key'])), verify.DEFICITS)
    stars = frame.domains()
    b = pair['exclusion']['point']
    c, supported = next((c, x) for c in range(11) if c != b for x in stars[b]
                        if any(frame.compatible(b, x, c, y) for y in stars[c]))
    first = pair['exclusion']['covers'][0]
    wrong_empty_point = next(i for i, size in enumerate(certificate['entries'][empty_index]['domain_sizes']) if size)
    distinct_index = next(i for i, entry in enumerate(certificate['entries']) if entry['key'][0] != entry['key'][1])
    cases = []

    def add(name, edit):
        damaged = deepcopy(certificate)
        edit(damaged)
        cases.append((name, damaged))

    add('missing_orbit', lambda v: v['entries'].pop(0))
    add('duplicate_orbit', lambda v: v['entries'].append(deepcopy(v['entries'][0])))
    add('unordered_orbits', lambda v: v['entries'].reverse())
    add('same_total_wrong_tags', lambda v: v.__setitem__('outside_deficits', [3, 1] + [0] * 9))
    add('boolean_deficit', lambda v: v['outside_deficits'].__setitem__(0, True))
    add('false_coverage_count', lambda v: v.__setitem__('incidence_records', 4909))
    add('wrong_red_cap', lambda v: v.__setitem__('red_page_cap', 4))
    add('boolean_schema', lambda v: v.__setitem__('schema', True))
    add('wrong_local_graph', lambda v: v.__setitem__('local_graph', 'P-minus-edge'))
    add('boolean_row_word', lambda v: v['entries'][0]['key'].__setitem__(0, True))
    add('changed_low_row', lambda v: v['entries'][0]['key'].__setitem__(0, v['entries'][0]['key'][0] ^ 1))
    add('reversed_equal_tag_rows', lambda v: v['entries'][distinct_index]['key'].__setitem__(slice(0, 2), v['entries'][distinct_index]['key'][:2][::-1]))
    add('changed_multiplicity', lambda v: v['entries'][0]['key'][3].__setitem__(0, (v['entries'][0]['key'][3][0] + 1) % 3))
    add('false_orbit_size', lambda v: v['entries'][0].__setitem__('orbit_size', v['entries'][0]['orbit_size'] + 1))
    add('false_domain_hash', lambda v: v['entries'][0].__setitem__('domains_sha256', '0' * 64))
    add('false_domain_size', lambda v: v['entries'][0]['domain_sizes'].__setitem__(0, 999))
    add('false_empty_star', lambda v: v['entries'][empty_index]['exclusion'].__setitem__('point', wrong_empty_point))
    add('supported_star_claimed_unsupported', lambda v: v['entries'][pair_index]['exclusion']['covers'][0].update({'against': c, 'stars': [supported]}))
    add('duplicate_unsupported_star', lambda v: v['entries'][pair_index]['exclusion']['covers'][0]['stars'].append(first['stars'][0]))
    add('incomplete_star_cover', lambda v: v['entries'][pair_index]['exclusion']['covers'].pop())
    add('overlapping_star_cover', lambda v: v['entries'][pair_index]['exclusion']['covers'].append(deepcopy(v['entries'][pair_index]['exclusion']['covers'][0])))
    add('wrong_target_point', lambda v: v['entries'][pair_index]['exclusion'].__setitem__('point', (b + 1) % 11))
    add('unknown_certificate_field', lambda v: v.__setitem__('unproved_bridge', True))
    add('null_exclusion', lambda v: v['entries'][0].__setitem__('exclusion', None))
    rejected = []
    for name, damaged in cases:
        require(verify.pack(damaged) != verify.pack(certificate), 'control did not alter input: ' + name)
        try:
            verify.verify_certificate(damaged, keys, census)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('damaged certificate accepted: ' + name)
    expected = json.loads((HERE / 'expected.json').read_text())
    forged = deepcopy(expected)
    forged['verifier']['low_word_sizes']['2']['6'] = 200  # Unjustified K2,3-filtered domain.
    with tempfile.TemporaryDirectory(prefix='book108-two8-integrity-') as directory:
        path = Path(directory) / 'expected.json'
        path.write_text(json.dumps(forged))
        command = [sys.executable] + (['-O'] if not __debug__ else [])
        command += [str(HERE / 'verify.py'), '--expected', str(path)]
        answer = subprocess.run(command, capture_output=True, text=True, timeout=45)
        require(answer.returncode != 0 and 'verifier expected-summary mismatch' in answer.stderr,
                'forged narrowed-domain summary accepted by checker')
    return {'good_incidence_records': good['incidence_records'], 'damaged_certificate_rejections': len(rejected),
            'damage_names': rejected, 'forged_narrowed_domain_summary_rejections': 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--derive', action='store_true')
    args = parser.parse_args()
    result = compute()
    if not args.derive:
        require(verify.pack(result) == verify.pack(json.loads((HERE / 'expected.json').read_text())['integrity_controls']),
                'integrity-control expected-summary mismatch')
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
