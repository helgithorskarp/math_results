#!/usr/bin/env python3
"""Negative controls for the difference-body certificate verifier."""

import copy
import json
import tempfile
from pathlib import Path

import verify


HERE=Path(__file__).resolve().parent


def rejected(cert):
    with tempfile.NamedTemporaryFile('w',suffix='.json')as handle:
        json.dump(cert,handle);handle.flush()
        try:verify.verify(handle.name,False)
        except ValueError:return True
    return False


def main():
    source=json.loads((HERE/'certificate.json').read_text())
    tests=[]
    bad=copy.deepcopy(source);bad['source_geometry_sha256']='0'*64;tests.append(bad)
    bad=copy.deepcopy(source);bad['possible_equality_cluster_count']-=1;tests.append(bad)
    bad=copy.deepcopy(source);bad['possible_unit_cluster_edge_count']-=1;tests.append(bad)
    bad=copy.deepcopy(source);bad['conservative_graph_sha256']='0'*64;tests.append(bad)
    bad=copy.deepcopy(source);bad['four_colour_word']=bad['four_colour_word'][:-1];tests.append(bad)
    if not all(rejected(test)for test in tests):raise ValueError('control accepted')
    print(json.dumps({'status':'ALL_CONTROLS_REJECTED','corruptions':len(tests)},indent=2))


if __name__=='__main__':main()
