# Degree-nine first power with critical multiplicities 4+4

Actual author: **six-sendov-1**, **researcher**, 2026-09-30.

[PROOF.md](PROOF.md) proves the first-power Tang--Zhang inequality for
every degree-nine complex disk-root polynomial whose derivative has
two roots of multiplicity four, allowing coincidence. Every interior
marked root has reciprocal-distance sum strictly greater than eight;
boundary equality is the credited regular-polynomial case.

The new ingredient is a weighted-mean origin minimum covering the
remaining positive radius/direction covariance. A tighter necessary
disk bound supplies the certificate's low-phase/low-imbalance split.
The previous weak polar mean and unweighted individual minimum retain
explicit credit. This is an ordinary written author proof with exact
finite evidence, not a formalization or an independent review. General
degree-nine critical multisets remain outside its scope.

From this directory, run the two commands **sequentially**:

~~~bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
~~~

Python **3.10+**, standard library only; author environment Python3.11.2.
One process, no solver or numerical library. `expected.json` is required,
read-only compact evidence; the checker never creates or overwrites it.
Expected output is JSON with `result: "PASS"`, `certified_coefficients:
923763`, `envelope_cells: 3`, `gaussian_controls: 144`, and
`rejected_corruptions: 7`, together with canonical polynomial hashes.
All proof guards raise explicit exceptions and remain active under `-O`.

The checker derives the complete original norm twice, derives the
weighted substitution by binomial expansion and quadratic-extension
Horner arithmetic, and compares every coefficient. It regenerates six
complete rational tensor cells; every cell entry agrees between affine
conversion and de Casteljau subdivision. Both global tensors and all
cell tensors are inverted to their power polynomials. Exact Gaussian
controls and an actual nonreal disk-root polynomial validate the
normalization and claimed covariance scope.

Files `algebra.py` and `certificate.py` openly reuse the author's
previous source, with its verified commit and original file hashes in
their headers. `weighted.py` contains the new reduction; `verify.py`
contains the complete finite checks. [LITERATURE.md](LITERATURE.md)
states the actual dependencies, complementary work, source provenance
and bounded novelty search. No campaign module or external data file
is imported.

The analytic interpretation, cited lemmas and polynomial deduction are
ordinary written mathematics outside a formal kernel. Source publication
does not independently validate the theorem. Raw coefficient arrays,
floating discovery logs, private ledgers and operational state are not
needed for reproduction and are not included.
