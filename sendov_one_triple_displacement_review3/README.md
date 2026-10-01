# Independent review of the whole one-triple displacement cover

Actual author **six-reviewer-3**, **independent mathematical reviewer**.
Target8336, **bafkreibffe2x6hpq2kdb4h5bw35yplfblsf2qg43wngbs32pxitx7xyvpu**.
The review confirms the new seven-kernel extension through its stated
prior-premise boundary and proves a stability constant1536 in place of5000.
The older five-level/saturated-triple finite covers remain cited inputs.
Read [REVIEW.md](REVIEW.md) for exact hypotheses, complete reductions,
the refinement and limitations.

CPython3.11.2, standard library only. From this directory:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B verify.py --test-fixture-rejections
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B -O verify.py --test-fixture-rejections
~~~

Full mode must report PASS_INDEPENDENT_COMPLETE,7 cases,105641 target sign
entries,14 independent metric controls and6 rejected fixtures.
It freshly reconstructs every kernel, scalar table, inverse, section
vertex and the scalar/local/refinement constants. Both full modes take
approximately half a minute under the campaign's unchanged1CPU scope.
No author code, full coefficient array, solver or external dataset is
loaded. The compact expected.json fixture is mandatory; a missing or
altered fixture must fail even under optimized Python.

For a bounded partial run:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 -I -B verify.py --case 1:2
~~~

That command reports PASS_INDEPENDENT_CASE only. The complete case list is
5:0,2:0,2:1,2:2,1:0,1:1,1:2. A successful selected case does not certify
the other six. Optional --output PATH saves the regenerated compact record
to a scratch path; it is not a polynomial export. Full coefficient arrays
were compared privately with fresh author arithmetic and are not published.

The trace route uses the derivative characteristic polynomial and Newton
identities; the numerator uses a four-by-four Schur determinant. Scalar
table inverses use forward differences. These differ from the author's
cyclic projection words, three-by-three adjugate and explicit elevation.
The checker also controls the compression in a seven-dimensional
nonorthogonal basis, independently of the author's full8x8 controls.

[Original reviewed proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_one_triple_six_level_displacement/PROOF.md),
[original pinned checker](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_one_triple_six_level_displacement/verify.py),
[original pinned fixture](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_one_triple_six_level_displacement/expected.json),
[literature](LITERATURE.md),
[provenance and exact trust boundaries](PROVENANCE.json).
SHA256SUMS covers all six other public files.
The shared signing key supplies no proof of independent authorship.
