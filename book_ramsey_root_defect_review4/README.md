# Book 98-edge root-defect audit

Actual author six-reviewer-4, independent mathematical reviewer. Original
theorem credit: six-books-1, researcher. See [REVIEW.md](REVIEW.md) for the
complete analytic proof, imported global premises, and proved improvements.

Requires CPython 3.11 or later, standard library only. Run sequentially from
this directory with native numerical thread limits set to one:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 audit.py --expected expected.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -O audit.py --expected expected.json
sha256sum -c SHA256SUMS
~~~

The two JSON outputs are identical. They reconstruct twelve forced defect
forms, prove rank 16 using literal contrasts and exact odd 16-dimensional
principal minors, and validate the algebra on 48 signed graph instances.
They also check625literal determinant controls, 24 relabelings, positive
contrast square roots, an invalid missing-cubic boundary, and the credited
21-point book construction. The expected records are compared only after
all checks have been rebuilt. Failure raises an explicit error under both
normal and optimized Python.

The principal minors of `(H-21I)/4` are 675/75/-25 for m=4, -255 for m=5,
and 59 for m=6. The proof is analytic; these checks are validation, not an
exhaustive census of 22-point host graphs. No author catalogue, external
package, solver, floating arithmetic or large artifact is required.

The author source and its two checks are pinned in [INPUT.json](INPUT.json).
Optional author graph/matrix exports, runtime logs and private checkpoints
are omitted. Replaying those author checks is additional provenance
validation and is not required to run this independent package.

[VALIDATION.json](VALIDATION.json) records exact final execution hashes,
resource measurements and literal source comparison counts. The complete
trust boundaries and unresolved positive-defect frontier are in the review.
