#!/usr/bin/env python3
"""Replay all original 8941 certificate entries with the independent page oracle.

The public original certificate is an untrusted input; no researcher module is
executed. The independent complete census and generated orbits are reconstructed.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import check

RAW_CERTIFICATE_SHA256 = 'd9c61c545cc623184c6ff9d1fc782552fd9b54bb88dd1a8b345c6fd8b0bad401'


def integer(value, low, high, message):
    check.need(type(value) is int and low <= value <= high, message)


def exact_fields(value, names, message):
    check.need(type(value) is dict and set(value) == set(names), message)


def normalized_key(raw):
    check.need(type(raw) is list and len(raw) == 4, 'key structure')
    z, w, high, mu = raw
    integer(z, 0, 1023, 'three-tag word'); integer(w, 0, 1023, 'one-tag word')
    check.need(type(high) is list and len(high) <= 2 and high == sorted(high), 'large-word list')
    for x in high: integer(x, 0, 1023, 'large word')
    check.need(type(mu) is list and len(mu) == 5, 'multiplicity vector')
    for x in mu: integer(x, 0, 2, 'multiplicity')
    check.need(sum(mu) + len(high) == 9, 'number of full rows')
    return z, w, tuple(high), tuple(mu)


def replay(frame, domains, exclusion):
    check.need(type(exclusion) is dict, 'exclusion object')
    if exclusion.get('type') == 'empty_star':
        exact_fields(exclusion, ('type', 'point'), 'empty-star fields')
        b = exclusion['point']; integer(b, 0, 10, 'empty-star point')
        check.need(not domains[b], 'claimed initial domain is nonempty')
        return 0, 0
    exact_fields(exclusion, ('type', 'steps', 'empty_point'), 'trace fields')
    check.need(exclusion['type'] == 'arc_deletion' and type(exclusion['steps']) is list
               and bool(exclusion['steps']) and all(domains), 'trace initial conditions')
    current = [set(d) for d in domains]; removals = 0
    for step in exclusion['steps']:
        check.need(all(current), 'step after empty domain')
        exact_fields(step, ('point', 'against', 'removed'), 'step fields')
        b, c, removed = step['point'], step['against'], step['removed']
        integer(b, 0, 10, 'deletion point'); integer(c, 0, 10, 'support point')
        check.need(b != c, 'self support')
        check.need(type(removed) is list and bool(removed), 'removal list')
        for star in removed: integer(star, 0, 2047, 'removed star')
        check.need(removed == sorted(set(removed)) and set(removed) <= current[b], 'removal membership')
        for star in removed:
            check.need(all(not frame.compatible(b, star, c, y) for y in current[c]),
                       'removed star has actual support')
        current[b].difference_update(removed); removals += len(removed)
    b = exclusion['empty_point']; integer(b, 0, 10, 'final point')
    check.need(not current[b], 'incomplete trace')
    return len(exclusion['steps']), removals


def verify(certificate, keys, classes):
    exact_fields(certificate, ('blue_page_cap', 'entries', 'incidence_records', 'local_graph',
                              'order', 'outside_deficits', 'red_page_cap', 'schema'), 'certificate fields')
    for field, value in (('blue_page_cap', 6), ('red_page_cap', 3), ('order', 22), ('schema', 1)):
        integer(certificate[field], value, value, 'wrong ' + field)
    check.need(certificate['local_graph'] == 'KG(5,2)', 'local graph')
    check.need(certificate['outside_deficits'] == list(check.DEFICITS)
               and all(type(x) is int for x in certificate['outside_deficits']), 'deficiency tags')
    integer(certificate['incidence_records'], len(keys), len(keys), 'coverage count')
    entries = certificate['entries']; check.need(type(entries) is list, 'entry list')
    expected = {key: orbit for key, orbit in classes}
    covered = set(); ordered = []; steps = removals = 0; star_hashes = []
    for entry in entries:
        exact_fields(entry, ('domain_sizes', 'domains_sha256', 'exclusion', 'key', 'orbit_size'), 'entry fields')
        key = normalized_key(entry['key']); ordered.append(key)
        check.need(key in expected, 'unknown or nonminimal representative')
        orbit = expected[key]
        check.need(not (orbit & covered), 'overlapping orbit'); covered.update(orbit)
        integer(entry['orbit_size'], len(orbit), len(orbit), 'orbit size')
        frame = check.Frame(check.P, check.rows_of(key)); domains = frame.domains(check.DEFICITS)
        check.need(type(entry['domain_sizes']) is list and all(type(v) is int for v in entry['domain_sizes'])
                   and entry['domain_sizes'] == list(map(len, domains)), 'whole-domain sizes')
        check.need(entry['domains_sha256'] == check.digest(domains), 'whole-domain hash')
        star_hashes.append(entry['domains_sha256'])
        count, removed = replay(frame, domains, entry['exclusion']); steps += count; removals += removed
    check.need(ordered == sorted(set(ordered)) and set(ordered) == set(expected), 'complete representative set')
    check.need(covered == keys, 'complete incidence coverage')
    return {'original_entries': len(entries), 'original_steps': steps, 'original_removals': removals,
            'complete_incidence_sha256': check.digest(sorted(covered)),
            'complete_domain_hashes_sha256': check.digest(star_hashes),
            'canonical_certificate_sha256': check.digest(certificate)}


def damaged_controls(certificate, keys, classes):
    cases = []
    def damage(name, edit):
        value = deepcopy(certificate); edit(value); cases.append((name, value))
    damage('missing_orbit', lambda v: v['entries'].pop())
    damage('duplicate_orbit', lambda v: v['entries'].append(deepcopy(v['entries'][0])))
    damage('swapped_deficiency_tags', lambda v: v['outside_deficits'].__setitem__(slice(0, 2), [1, 3]))
    damage('wrong_domain_size', lambda v: v['entries'][0]['domain_sizes'].__setitem__(0, 2))
    arc = next(i for i, e in enumerate(certificate['entries']) if e['exclusion']['type'] == 'arc_deletion')
    frame = check.Frame(check.P, check.rows_of(normalized_key(certificate['entries'][arc]['key'])))
    domains = frame.domains(check.DEFICITS)
    b, c, star = next((b, c, x) for b in range(11) for c in range(11) if b != c
                      for x in domains[b] if any(frame.compatible(b, x, c, y) for y in domains[c]))
    damage('supported_star_removed', lambda v: v['entries'][arc]['exclusion']['steps'][0].update(
        {'point': b, 'against': c, 'removed': [star]}))
    damage('incomplete_deletion_trace', lambda v: v['entries'][arc]['exclusion']['steps'].pop())
    damage('step_after_empty', lambda v: v['entries'][arc]['exclusion']['steps'].append(
        deepcopy(v['entries'][arc]['exclusion']['steps'][-1])))
    damage('boolean_deficiency', lambda v: v['outside_deficits'].__setitem__(1, True))
    rejected = []
    for name, value in cases:
        try: verify(value, keys, classes)
        except ValueError as exc:
            if name == 'supported_star_removed': check.need(str(exc) == 'removed star has actual support', 'weak support damage')
            rejected.append(name)
        else: raise ValueError('damaged certificate accepted: ' + name)
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args(); raw = args.certificate.read_bytes()
    check.need(hashlib.sha256(raw).hexdigest() == RAW_CERTIFICATE_SHA256, 'original public input hash')
    certificate = json.loads(raw)
    keys, _ = check.complete_census(); classes = check.orbits(keys)
    result = verify(certificate, keys, classes)
    if args.controls: result['damaged_controls_rejected'] = damaged_controls(certificate, keys, classes)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
