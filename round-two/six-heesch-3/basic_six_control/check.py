#!/usr/bin/env python3
"""Reproduce the known six control plus a fixed-patch one-cell grid cut."""
from copy import deepcopy
import json
from pathlib import Path
import geometry
import one_cell_cut

HERE=Path(__file__).resolve().parent

def must_reject(data,fragment):
    try:
        geometry.check(data)
    except ValueError as ex:
        geometry.require(fragment in str(ex),'negative control rejected for unexpected reason')
        return str(ex)
    raise ValueError('invalid certificate accepted')

def main():
    data=json.loads((HERE/'certificate.json').read_text())
    lower=geometry.check(data)
    cut=one_cell_cut.check(data)
    for result in (lower,cut):
        result.pop('elapsed_seconds',None)
        result.pop('peak_rss_kib',None)
    gap=deepcopy(data)
    gap['copies']=[r for r in gap['copies'] if r['level']<=1]
    gap.pop('level_counts')
    del gap['copies'][1]
    rejection_gap=must_reject(gap,'strictly inside')
    overlap=deepcopy(data)
    overlap['copies']=[r for r in overlap['copies'] if r['level']<=1]
    overlap.pop('level_counts')
    overlap['copies'][1]['pose'][2]+=4
    rejection_overlap=must_reject(overlap,'interiors overlap')
    result={'lower':lower,'fixed_grid_cut':cut,
            'negative_controls':{'deleted_first_corona_copy':rejection_gap,
                                 'translated_copy_overlaps':rejection_overlap},
            'independent_peer_review_claimed':False,
            'new_Heesch_record_claimed':False}
    # JSON is the evidence schema: tuple/list values and integer mapping
    # keys must be normalized before comparing an in-memory result with
    # the parsed file. This does not change any mathematical entry.
    result=json.loads(json.dumps(result))
    expected=HERE/'expected.json'
    if expected.exists():
        geometry.require(result==json.loads(expected.read_text()),'deterministic expected evidence mismatch')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
