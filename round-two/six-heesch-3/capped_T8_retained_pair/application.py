#!/usr/bin/env python3
"""Bind the pair to the previously published credited six-corona witness.

Actual author six-heesch-3, researcher. The standalone pair lemma needs no
external input. This application uses only previously published OWNED decoder
source and the credited witness as data. Foreign executable code is never run.
"""
from hashlib import sha256
import json
from pathlib import Path
import resource
import sys
import time
import check


def run():
    started = time.monotonic()
    here = Path(__file__).resolve().parent
    previous = here.parent / 'external_six_corona_replay'
    sys.path.insert(0, str(previous))
    import decoder
    expected = json.loads((previous / 'expected.json').read_text())['h8l']
    foreign = previous / 'witness_h8l.txt'
    check.g.require(sha256(foreign.read_bytes()).hexdigest() == expected['foreign_sha256'],
                    'credited positive input changed')
    data, source = decoder.decode(foreign, 8, True, previous / 'drafter_tables.py')
    serialized = (json.dumps(data, indent=2) + '\n').encode()
    check.g.require(sha256(serialized).hexdigest() == check.WITNESS_SHA,
                    'entire normalized six-copy placement list differs')
    document = json.loads((here / 'certificate.json').read_text())
    rows = document['certificate']['template']
    for row in rows:
        actual = data['copies'][row['original_index']]
        check.g.require(actual['pose'] == row['pose'] and actual['level'] == row['original_level'] == 6,
                        'two retained copies are absent from actual six')
    checked = check.read(document)
    out = {'actual_author':'six-heesch-3','role':'researcher',
        'status':'two-copy obstruction applies to the credited literal six layout',
        'certificate_sha256':document['certificate_sha256'],
        'literal_six_witness_sha256':check.WITNESS_SHA,
        'original_indices':[row['original_index'] for row in rows],
        'original_levels':[row['original_level'] for row in rows],
        'complete_strict_point_reader_replayed':True,
        'prior_construction_commit':'35e06b5f68cc76930d5421edeb64af1bb220d756',
        'six_construction_uses_prior_complete_polygon_replay':True,
        'foreign_checker_or_solver_executed':False,
        'no_other_six_layout_or_shape_global_upper_claimed':True}
    out['stable_mathematical_sha256']=check.canonical(out)
    out['elapsed_seconds']=time.monotonic()-started
    out['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return out

if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
