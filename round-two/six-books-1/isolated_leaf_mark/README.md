# Fixed-leaf mark obstruction

Actual author **six-books-1**, researcher. Read [PROOF.md](PROOF.md) for
the exact hypotheses and unformalized ordinary-to-code reduction.

For the displayed one-nine leaf and e(G)<=108, the degree-nine mark
has a non-ten red neighbor, without a global maximum assumption. An
explicit maximum ten makes that neighbor deficient. A mark with no
deficient red neighbor instead requires one degree-eleven neighbor;
that last alternative is still open. No Ramsey endpoint is determined.

Use CPython **3.12.14**, standard library only. There is no solver,
floating point, graph catalogue or external corpus. Run commands
serially from this directory:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 derive.py > /tmp/six-books-1-leaf-derived.json
python3 verify.py --emit > /tmp/six-books-1-leaf-verified.json
cmp EXPECTED.json /tmp/six-books-1-leaf-derived.json
cmp EXPECTED.json /tmp/six-books-1-leaf-verified.json
python3 verify.py
python3 -O derive.py > /tmp/six-books-1-leaf-derived-O.json
python3 -O verify.py --emit > /tmp/six-books-1-leaf-verified-O.json
cmp EXPECTED.json /tmp/six-books-1-leaf-derived-O.json
cmp EXPECTED.json /tmp/six-books-1-leaf-verified-O.json
python3 verify.py --damage-controls
python3 -O verify.py --damage-controls
```

[EXPECTED.json](EXPECTED.json) is the entire compact typed finite
record: 816 X states represented by 17 orbits, 40 fixed-spine frames,
and every one of the 780 blocked red rows at their selected ordinary
X point. All 17 orbit expansions are compared entrywise with a fresh
complete domain. Both programs regenerate the entire record; the
checker never imports the producer. Its independent enumeration
uses columns and Boolean third-vertex counts, with literal subset-pair
controls of orders six and eight and a separate row enumeration of
the Y type sets.

The whole 16071-byte expected file, including its terminating newline,
has SHA256
`84fa548e5250dfaab789ad22ff77029a3528cefca41e61458a349007270d82e5`.
Its sorted X-state subrecord has SHA256
`8dbfb419d3321668baa129bcb7c544d34f8f92c22a59437ed22793c94ff0c60a`.
The checker rejects thirteen deliberate damages per mode, including
an omitted obstruction/blocked choice, wrong orbit size/color/page/row,
wrong symmetry and a Boolean substituted for an integer.

Six final serial normal/optimized producer, checker and damage runs
completed in at most **11.400982 seconds** and **23716 KiB** reported
child peak RSS, unchanged 1CPU/2GiB. Each run had the unchanged
90-second external guard; programs additionally have fixed 45-second
guards. Measurements are in [provenance.json](provenance.json). RSS
from RUSAGE_CHILDREN is cumulative across prior serial children and
therefore bounds each run's individual peak. No timeout or missing
case is proof. An early slower private prototype reached its guard
and supplies no evidence.

The finite obstruction is a premise of the computer-assisted result.
The normal form and code correspondence remain unformalized;
same-author different algorithms are not independent peer review.
Partial frames are not full valid-host constructions. The remaining
ordinary Y graph, full cross-matrix and O_Y global tags are unnecessary
for this contradiction and are never asserted classified.
