#!/usr/bin/env python3
"""Post-filter for one-anchor configurations: drop type II configurations whose mirror point y is exactly a
vertex w ∈ V.  Exactness: y is one of the two common unit neighbours of b, d ∈ Q; if w ∈ V is at exact unit
distance from b and from d (K arithmetic, or the K-point/non-K test) then w ∈ {x, y}; x is not w (x has a
single vertex neighbour within 1e-5 while w's neighbours are all at distance exactly 1), and |x − y| = 1, so
w = y when w is within 1e-6 of y.  Such a configuration re-adds a vertex: for D ∌ w the point y is a twin of w
(irrelevant), for D ∋ w the graph G − D + A contains G − (D \ {w}) + (A \ {y}), a delete-4-add-3 instance,
which is 4-colourable by the committed closure.  Hence these configurations cannot give a 5-chromatic graph
on 508 vertices and may be discarded.  Also drops any configuration whose point x coincides exactly with a
vertex (should not occur: the enumerator discards them).
usage: filter_configs.py IN.json OUT.json
"""
import json, sys, importlib.util
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('oa2', HERE / 'enumerate_one_anchor.py')
oa2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(oa2)
oa2.load()
D = oa2.D
confs = json.loads(Path(sys.argv[1]).read_text())
keep, dropped, unresolved = [], 0, 0
for cf in confs:
    if cf['type'] != 'II':
        keep.append(cf); continue
    y = np.array(cf['points'][1]['x']); b = cf['points'][2]['q']; d = cf['points'][3]['q']
    dist, w = D['treeV'].query(y)
    if dist < 1e-6:
        wE = D['VE'][w]
        if oa2.kpoint_unit_to_gen(wE, b) and oa2.kpoint_unit_to_gen(wE, d):
            dropped += 1; continue
        unresolved += 1
    keep.append(cf)
print(f'{len(confs)} configurations: dropped {dropped} type II with y ∈ V (exact), {unresolved} near-vertex kept, {len(keep)} kept')
Path(sys.argv[2]).write_text(json.dumps(keep))
