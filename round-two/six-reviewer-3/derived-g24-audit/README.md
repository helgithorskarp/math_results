# Independent derived-G24 capacity audit

Actual author **six-reviewer-3**, independent mathematical reviewer.

The entire closed-interval capacity theorem of LEMMA9966 is independently
confirmed. The literal thirteen-label motif is realizable exactly on
[1/sqrt(3),593/1000] within the original interval [14/25,593/1000], and a
fourteenth point exists at every feasible parameter. Thus the conditional
maximum is exactly14 throughout that feasible interval. The degree10=4
corollary retains the precise9922 G20 implication. Other branches and global
N15 optimality remain open.

Read PROOF.md for the complete ordinary reduction, the full dual/Sturm certificate
argument and uniform attainment. EXPECTED.json is the complete compact typed
record: all364 active triples,367 closed leaves, all13 polynomial coordinates,
all78 core pairs and the actual uniform14-point witness. SUMMARY.json reports
counts; the full record is the comparison boundary. There is no proof-corpus,
external dataset, solver or floating arithmetic.

Python3.11+ and the standard library suffice. Set all solver/BLAS/OpenMP thread
variables to1; run the following commands serially from this directory:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 audit.py --expected EXPECTED.json --output /tmp/g24-independent.json
python3 -O audit.py --expected EXPECTED.json --output /tmp/g24-independent-optimized.json
python3 validate.py --expected EXPECTED.json --output /tmp/g24-independent-validation.json
```

Both first commands compare the whole typed record, including every path and
polynomial fingerprint. VALIDATION.json records the actual13 serial children,
24 signed-remainder bridge controls and10 Sturm controls, four mathematical
source damages in both modes, and three external typed-record damages. The
third external damage adds an incorrect unbound sign-fingerprint field; it is
a whole-record/schema rejection, not a separately proved altered polynomial.
The baseline files also test two valid whitespace/key-order representations.
Maximum child time was under8.50seconds and peak child RSS27012KiB; the hard
per-child guard remains45seconds. Incompletion is failure.

SEAL.json binds eight primary files before any access to target executable
source or its certificate. The target written mathematical formulas were
exposed; this was not blind. Later comparison/replay files report their distinct
trust boundary. Same-author target replay is not another independent reviewer.
The ordinary proof is unformalized.
