# Rootless108 occurrence and marked-neighborhood classification

six-books-1, researcher. See PROOF.md for the exact hypotheses, the ordinary
occurrence split, and the computer-assisted list of fourteen necessary
marked local types. Outside graph completion and R(B4,B7) remain open.

Python 3.11.2; standard library only; exact integers and sets. Run serially:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B enumerate.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B verify.py
python3 -B -O verify.py
```

Both programs require complete results matching expected.json. They fail
on malformed data, a mismatch, or an internal 45-second completion guard.
The author commands complete in seconds on one CPU with memory below
25 MiB. A timeout establishes no exclusion. The producer uses vertex
augmentation and canonical refinement; the independent checker uses edge
augmentation and direct isomorphism backtracking. Every marked class is
compared entry by entry. This is independent code written by one author,
not an independent peer review or a proof-assistant formalization.

model.json is a compact 179-record local certificate table, not a corpus
of full-host searches. A null packing_rejection marks one of fourteen
necessary survivors (2 at13 edges, 11 at14, 1 at15). Each other record
contains an exact subset packing contradiction. PROOF.md describes the
bit ordering. expected.json specifies the complete counts and controls.
The 21-point fixture is the off-diagonal red complement of the primary
construction, checked freshly against all441 entries and credited in
provenance.json. The primary flag upper-bound certificate is not replayed.

No third-party solver package or saved native proof log is required.
MANIFEST.json records SHA256 hashes of the compact source files. The
unformalized completeness arguments and program correctness remain the
trust boundary. No sufficient condition for a valid22-point host is claimed.
