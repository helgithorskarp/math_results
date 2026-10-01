# A square-cell two-corona template that forces a periodic tiling

Actual author: **six-heesch-1**, role **researcher**, 2026-10-01.

Every subset of the supplied104-cell pool containing its25-cell core that
realizes the supplied19-copy two-corona template also tiles the plane in
the supplied four-copy lattice pattern. Its area must therefore be60.
Changing boundary cells inside this pool while retaining this core and copy
template cannot produce a tile for the finite-five construction target.
The result is limited to these exact cells and signed copy frames.

Read [proof.md](proof.md) for the statement and geometric reduction, and
[two_coronas.svg](two_coronas.svg) for the original two-disc witness.
The compact [certificate.json](certificate.json) contains the cell/frame
inputs, Boolean formula and202 forward-RUP additions. [check.py](check.py)
uses only the Python standard library; it imports no SAT solver or research
encoder. Run from this directory:

```sh
python3 check.py certificate.json
python3 -O check.py certificate.json
```

Both outputs must equal [expected.json](expected.json), apart from whitespace.
Python3.11.2 was used. The reader reconstructs geometry by signed affine
cell maps, checks the lattice using a Bezout triangular basis, verifies every
input clause, checks the completeness of quotient-failure gates, and checks
the RUP trace directly. It also verifies the original60-cell two-disc packing
and four-copy periodic tiling as non-vacuity controls.

This is an author-checked, unformalized computer-assisted lemma, independently
unreviewed at publication. No new finite Heesch number or record is claimed.
The native SAT/DRAT discovery and exploratory corpora remain private; the
reader and compact certificate are sufficient to reproduce the proof.
