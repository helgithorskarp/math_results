#!/usr/bin/env python3
"""Reject incomplete, misoriented, or misaligned polygon evidence."""
from copy import deepcopy
import json
from check import (HERE, audit_polygon, audit_contacts, group, vertices,
                   lf, Z, ONE, require)


def rejected(label, fn):
    try:
        fn()
    except ValueError:
        return
    raise ValueError('invalid evidence was accepted: '+label)


def main():
    data = json.loads((HERE / 'polygon.json').read_text())
    mats = group()
    vs = vertices(mats)
    cases = []
    for label, change in (
        ('missing vertex', lambda d: d['counterclockwise_vertex_indices'].pop()),
        ('duplicate vertex', lambda d: d['counterclockwise_vertex_indices'].__setitem__(0, d['counterclockwise_vertex_indices'][1])),
        ('boolean index', lambda d: d['counterclockwise_vertex_indices'].__setitem__(0, True)),
        ('out-of-range index', lambda d: d['counterclockwise_vertex_indices'].__setitem__(0, 92)),
        ('reversed boundary', lambda d: d['counterclockwise_vertex_indices'].reverse()),
        ('wrong axis', lambda d: d.__setitem__('axis', ['0', '1', 'phi'])),
        ('wrong short edge', lambda d: d.__setitem__('base_short_edge', [27, 33])),
        ('unexpected field', lambda d: d.__setitem__('unchecked_radius', '0.1')),
    ):
        bad = deepcopy(data)
        change(bad)
        cases.append((label, bad))
    for label, bad in cases:
        rejected(label, lambda bad=bad: audit_polygon(vs, bad))
    changed = list(vs)
    changed[33] = tuple(lf(0, Z) for _ in range(3))
    rejected('changed original point', lambda: audit_polygon(changed, data))
    rejected('missing proper endpoint swap', lambda: audit_contacts(vs, []))
    print(json.dumps({'evidence_controls': 'PASS', 'malformed_cases_rejected': 10},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
