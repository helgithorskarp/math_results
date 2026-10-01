# Partial-cell corner obstruction for changed square-cell polyominoes

Author: **six-heesch-1**, role **researcher**.

Within the116-cell pool around the scale-two subdivision of Kaplan's other
seventeen-omino, a compulsory root and two specified whole-copy frames cannot
become interior whenever six extra cells are selected and seventeen cells
are absent. The proof allows arbitrary real motions for added copies. It
supplies a25-literal construction cut, replacing an exact118-literal shape
block. A second variant uses two old copies alone and35 absent cells.

[proof.md](proof.md) states both conditional results and the sector argument.
[data.json](data.json) supplies every finite parameter and a50-cell changed
prototype with a checked first disc corona. [check.py](check.py) rebuilds the
928-owner envelope from whole-square geometry, checks every rejection and the
nonvacuous construction, and runs nine damaged-input controls.

Python3.11.2, standard library only; no SAT solver or downloaded input needed:

```sh
python3 heesch_polyomino_partial_corner_filter/check.py
python3 -O heesch_polyomino_partial_corner_filter/check.py
```

Both outputs match [expected.json](expected.json). The root-context result
has34 mandatory selected cells,17 explicit empty cells,27 packing-implied
empty cells, and928 excluded owners (136 explicit absence,216 implied
absence,576 compulsory collisions). The first-disc witness has one root and
six copies, areas50/350 and perimeters44/178.

Status: author checked, unformalized and independently unreviewed. These
results concern specified patterns, not global height, finiteness, a census
of valid prototypes, or a finite-five construction. Kaplan's reference and
its three coronas remain prior art. A native bounded search with the new cut
returned UNKNOWN; it supplies no nonexistence claim and is not needed for
the proof. Raw search formulas, traces and exploratory outputs remain
outside this source directory.
