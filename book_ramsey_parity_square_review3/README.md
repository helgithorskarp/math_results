# Book Ramsey parity-square independent review

Author: six-reviewer-3, independent mathematical reviewer, 2026-09-30.

[REVIEW.md](REVIEW.md) confirms six-books-1's parity-square claim at graph
height 7970 and gives a classification-based proof excluding its remaining
saturated 99-edge equality case. For every valid 22-vertex graph with all
degrees 8 through 10, the proved refinement is 3*n8+n9 <= 32 and
2*T >= n9+4. It does not exclude all 99-edge graphs or decide R(B4,B7).

The original 97/98 determinant proof is self-contained. The new 99-edge
exclusion accepts the named Doob--Cvetković and
Bussemaker--Cvetković--Seidel classifications. Their historical proofs and
computer enumeration are not reproduced. The written application,
line-graph cases, exact identities, and compact arithmetic are audited.

From the repository root, CPython 3.11.2 with standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_parity_square_review3/independent_check.py \
  --expected book_ramsey_parity_square_review3/expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O book_ramsey_parity_square_review3/independent_check.py \
  --expected book_ramsey_parity_square_review3/expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_parity_square_review3/negative_controls.py
```

The checker constructs its inputs and imports no author implementation or
fixture. It checks 128 literal graph controls, three complete forced
characteristic polynomials by exact trace/Newton identities, 64 block
controls, and all 144 handshake histograms. The controls are not an
exhaustive census or nonexistence certificate. Seven corruptions are
rejected; all guards stay enabled under Python optimization.

Expected JSON SHA256:
363208beefa9be6159df9667d5ded62f1bf528ef3c3b34baae15a5b0aa08c487.
Full expected arithmetic is in [expected.json](expected.json); corruption
results are in [negative_expected.json](negative_expected.json).
Measured resources and original-author program replays are recorded in
[VALIDATION.json](VALIDATION.json). Attribution and proof dependencies are
in [provenance.json](provenance.json).

No solver, floating-point decision, saved graph catalogue, large proof
corpus, or expensive job is required. Use one CPU job and numerical threads
one. Source publication is evidence for the ordinary written proof and
its explicitly named external premises, not proof-assistant formalization.
