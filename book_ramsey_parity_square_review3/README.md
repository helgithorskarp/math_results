# Book Ramsey parity-square independent review

Author: six-reviewer-3, independent mathematical reviewer, 2026-09-30.

[REVIEW.md](REVIEW.md) confirms six-books-1's parity-square claim at graph
height 7970 and the concurrent saturation theorem at height 8006. With the
already reviewed global degree theorem, every valid 22-vertex graph has
3*n8+n9+n11 <= 32 and 2*T >= n9+n11+4, so n8 <= 10 and T >= 2. It does not exclude all 99-edge graphs or decide R(B4,B7).

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
controls, all 144 three-degree handshake histograms, and all four-degree
handshake histograms including the complete 21 parity-equality cases. The controls are not an
exhaustive census or nonexistence certificate. Seven corruptions are
rejected; all guards stay enabled under Python optimization.

Expected JSON SHA256:
0e30341af3357935b481ff69412093ec7879df8bc7045311cd8d575a2db32307.
Full expected arithmetic is in [expected.json](expected.json); corruption
results are in [negative_expected.json](negative_expected.json).
Measured resources and original-author program replays are recorded in
[VALIDATION.json](VALIDATION.json). Attribution and proof dependencies are
in [provenance.json](provenance.json).

No solver, floating-point decision, saved graph catalogue, large proof
corpus, or expensive job is required. Use one CPU job and numerical threads
one. Source publication is evidence for the ordinary written proof and
its explicitly named external premises, not proof-assistant formalization.
