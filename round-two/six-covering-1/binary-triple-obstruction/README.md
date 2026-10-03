# Binary-triple allocation obstruction

Author: six-covering-1, researcher. Conditional ordinary lemma in the explicit
five-copy, one-supplemental-row covering-tail model; no new global L_min(8) bound.

For an unmarked Q with entire original inventory {d3,d9,24,720},
d3 in{3,6,12}, d9 in{9,18,36}, another copy containing {8,16,48} has
common support at most110 if unmarked, at most108 if marked. Extra originals
on that copy are allowed. With original144 also on it, the marked bound is107.
A111-point candidate needs productive core3 classes in at least two other copies.

Read [the proof](proof.md). Run from this directory with Python3.10 or later;
only the standard library is required:

```sh
python3 audit_binary3.py > /tmp/binary3-normal.json
python3 -O audit_binary3.py > /tmp/binary3-optimized.json
python3 -c 'import json; a=json.load(open("expected.json")); b=json.load(open("/tmp/binary3-normal.json")); c=json.load(open("/tmp/binary3-optimized.json")); assert a==b==c; print("exact agreement")'
```

Use one process at a time; no numerical-library or solver threads are used.
The deterministic compact output checks all400 target shapes,193200 original
phase capacities,38400 binary3 phase triples and324000 five-point-row phase
intersections, with12055 physical original-phase/owner maps.

The written loss/overlap and extra-resource budget argument proves the lemma;
these finite counts audit its arithmetic facts. All allocations are not enumerated.
No external table, compiled binary, private ledger, key or large generated corpus
is required or included. The proof is unformalized and no independent external
review verdict is claimed. expected.json contains counts and canonical hashes,
including the exact checker source hash.
