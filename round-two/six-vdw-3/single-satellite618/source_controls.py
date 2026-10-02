#!/usr/bin/env python3
"""Repaired coverage and local-consequence damage checks."""
import argparse
import copy
import json
from pathlib import Path
from cover_check import audit
from profile_check import scope


def controls(cover,expected):
    rejected = 0
    bad = copy.deepcopy(cover)
    bad['cases'].pop()
    try:audit(bad)
    except ValueError:rejected += 1
    else:raise ValueError('Incomplete exact input cover accepted')
    trials = []
    bad = copy.deepcopy(expected)
    bad['proved_case_numbers'].pop()
    trials.append((cover,bad))
    bad = copy.deepcopy(cover)
    bad['cases'][0]['unique_opposite_satellite'] = 52
    trials.append((bad,expected))
    bad = copy.deepcopy(expected)
    bad['restricted_profile_scope']['geometry_records'][0]['necessary_local_binary_patterns_remaining'] += 1
    trials.append((cover,bad))
    for c,e in trials:
        try:scope(c,e)
        except ValueError:rejected += 1
        else:raise ValueError('Damaged local consequence accepted')
    return {'incomplete_input_cover_rejected':1,'profile_damages_rejected':3,'total_damages_rejected':rejected}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cover',type=Path,required=True)
    p.add_argument('--expected',type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(controls(json.loads(a.cover.read_text()),json.loads(a.expected.read_text()))))
