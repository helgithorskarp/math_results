# Independent RID wedge audit

Actual reviewer: **six-reviewer-4**, independent mathematical reviewer.
Confirms committed LEMMA8995 at its exact all-source, signed, closed receiving
wedge scope. Global RID Rupertness remains open. REVIEW.md contains the complete
written reduction, exact trust boundaries and sharper area domination constants.

Python3.11+, standard library only. This directory is self-contained. Run
separately, with one library thread and at most one CPU-intensive job at a time:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 timeout 40s python3 -B check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 timeout 40s python3 -B -O check.py
```

Both print PASS after comparing every expected.json byte. --emit prints the
freshly reconstructed record. The checker imports only this reviewer's field.py;
no author code or expected record executes or supplies proof data. It enumerates
all original facets, proper rotations, area-polar axes and direct physical shadows.
Its affine/radical gates support the written continuum proof, which remains
unformalized. Expected record57,076 bytes; SHA256
01ceac565960ac6a2a0346fa9dcfc8226045541a013c559973e0e6251faf89cf.

The optional compare.py reads the author's public expected.json or captured normal
output, comparing26 common exact entries and six damaged-input controls:

```sh
python3 -B compare.py /path/to/author/expected.json --controls
python3 -B -O compare.py /path/to/author/expected.json --controls
```

The normal native replay was complete. The optimized native replay hit its40s
guard and was stopped; no budget increase or retry. The independent optimized
checker completed. Metrics and provenance are in VALIDATION.json/PROVENANCE.json.
No timeout or incomplete enumeration proves mathematical nonexistence.
