# Independent fourteen-edge Book Ramsey review

Actual author: **six-reviewer-2**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms committed claim8218: a valid ten-regular
red graph on22 vertices has fourteen or fifteen edges in every red
neighborhood. The new two-five-row exclusion independently checks all
933 selected row pairs and1,747,161 residual matrices. The Ramsey endpoint
remains unresolved. Earlier finite premises are credited independent reviews.

The proof uses CPython3.11 standard library, g++12/C++17, and OpenSSL3
libcrypto development headers. SHA256 is used for provenance agreement;
the mathematical verdict uses exhaustive coverage and strict integer forms.
No solver, floating proof input, downloaded graph catalogue, author Python
module, or unpublished raw author corpus is required.

Place this directory next to the existing public input directory
`book_ramsey_b4_b7_regular110_neighborhood_floor14`. Its authenticated
`expected.json` supplies comparison pins; its `negative_vectors.json`
supplies untrusted integer proof objects. `INPUT.json` records reviewed
source commit and byte hashes. The domain is regenerated from literal
local graphs and every five-subset. Author executables are never called.

Run sequentially, one numerical thread and one intensive job:

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B book_ramsey_floor14_review2/verify.py --work /tmp/book14-normal
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O book_ramsey_floor14_review2/verify.py --work /tmp/book14-optimized
```

`--target PATH` can supply a separately authenticated input directory.
Generated native inputs, executable, result records and metrics stay in
`--work`, outside published source. Native guards are200,000 pairing nodes
and ten seconds per selected-row fiber. Incomplete guards raise an error
and supply no exclusion. They must not be increased to hide a failed case.

`verify.py` regenerates the complete census and controls by default.
The optional pair `--record PATH --control-record PATH` only compares
previously completed records with compact expected evidence; it does not
rerun or certify their generation. `VALIDATION.md` distinguishes the cold
runs from that publication-path comparison. All substantive checks use
explicit exceptions and survive optimized Python.
