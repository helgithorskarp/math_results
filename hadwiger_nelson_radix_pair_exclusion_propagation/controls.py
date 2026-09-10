#!/usr/bin/env python3
"""Reject incomplete coverage, a false transversal obstruction, and false counts."""
import argparse
import copy
import json
import tempfile
from pathlib import Path
import common as C
import verify


def run(frontier,incidence):
    original = json.loads((C.HERE/'certificate.json').read_text())
    cases = []
    d = copy.deepcopy(original);d['three_section_cores'].pop()
    cases.append(('omitted affected pencil','exactly one obstruction for every affected pencil',d))
    d = copy.deepcopy(original)
    C.need(d['three_section_cores'][0] == [0,[0,1,2]],'pinned first obstruction fixture')
    d['three_section_cores'][0][1] = [0,2,3]
    # Curves 2727,1798,1827 form an unblocked transversal of these three
    # alternative sections. This mutation has valid distinct section indices.
    cases.append(('noncovering valid three-section choice','every transversal of the three witness sections',d))
    d = copy.deepcopy(original);d['closed_pencils_index_raw_before'][0][2] += 1
    cases.append(('false admissible-lift count','every changed pencil count agrees entrywise',d))
    d = copy.deepcopy(original);d['moved_pairs'] += 1
    cases.append(('false global pair-mode count','all compact certificate fields verified',d))
    rejected = []
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory)/'mutated.json'
        export = Path(directory)/'must-not-be-exported.json'
        for name,reason,data in cases:
            path.write_text(json.dumps(data))
            try:verify.run(frontier,incidence,path,export)
            except ValueError as error:
                C.need(reason in str(error),'mutation reached its intended mathematical check: '+name)
                C.need(not export.exists(),'invalid certificate must not publish an output interface')
                rejected.append(name)
            else:raise ValueError('accepted corrupt certificate: '+name)
    return {'verified':True,'rejected':rejected,'assertions_used_for_correctness':False}


if __name__ == '__main__':
    p = argparse.ArgumentParser();p.add_argument('--frontier',type=Path,required=True)
    p.add_argument('--incidence',type=Path,required=True);a = p.parse_args()
    print(json.dumps(run(a.frontier,a.incidence),indent=2,sort_keys=True))
