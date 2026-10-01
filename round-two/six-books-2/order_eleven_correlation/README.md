# Order-eleven obstruction for R(B4,B7)

Author: **six-books-2**, role **researcher**, 2026-10-01.

[PROOF.md](PROOF.md) gives an ordinary correlation and cyclic-gap proof:
a simple22-vertex red graph of maximum degree at most10, with red-edge
page cap3 and blue-edge page cap6, has no order-eleven automorphism.
Consequently11 does not divide its automorphism group order, and it is
not vertex-transitive. Both cycle types11^2 and11^1 1^11 are covered.

The proof derives the minimum-eight bound within the free cyclic family,
then excludes degrees8,9,10 using small gap shapes and cross-triangle
counts. Its only imported premise for the **global** group restrictions
is the upper-ten conclusion of [lemma8012](../../../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md),
source ce3177a731086284ee89f18a8a3948b672b3c64e. That part imports an
exact Gram exclusion and the preceding capacity proof. The predecessor's
separate historical-classification-dependent minimum-eight corollary,
regular110/Hall closure, and campaign edge-count bounds are not used.
The Ramsey interval22..23 remains unresolved.

From this directory, with CPython3.11+ and no third-party packages:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
```

Both programs compare their compact deterministic output with their part
of [expected.json](expected.json), keeping checks active under optimization.
`check.py` validates the written small cases, a primary positive baseline,
literal/correlation identities, and damaged-input controls. `verify.py`
imports no checker and uses a different bitset implementation. It validates
all physical spines of the baseline and deterministic arbitrary controls,
then scans every265912 two-orbit template with degrees8..10, obtaining
zero survivors. This scan corroborates the **ordinary proof**; the theorem
does not depend on completing it. Neither program invokes a solver.

[primary22.g6](primary22.g6) is a compact prior-art fixture, credited to
Lidicky--McKinley--Pfender--Van Overberghe and taken verbatim from
[their published Bn-1Bn graph file](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/polycirculant/Bn-1Bn.txt),
repository revision a4809717b5d3c0083292c72e83fdbfbb22092d15. The
R(B5,B6)>22 entry has red pages at most4 and blue pages at most5;
it does not satisfy the current red cap3. Reproduction is validation,
not a new construction. Block-circulant methods and formulas are credited
to the primary literature in the proof; no historical priority is asserted.

The files are compact source, proof and expected summaries. No key,
private ledger, solver log, exhaustive graph corpus or generated state
is included. The proof is not formally mechanized, and independent
review of this new theorem is pending.
