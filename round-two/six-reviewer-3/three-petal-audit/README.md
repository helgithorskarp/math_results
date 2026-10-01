# Independent three-petal capped-H audit

**six-reviewer-3, independent mathematical reviewer.** [REVIEW.md](REVIEW.md)
confirms the scoped three-petal/packet theorem8642 and proves a larger closed
rational rank-repair interval, an exact seed-nullity formula and separation
from both spectral endpoints. General spectral Chvátal H/I remain unresolved.

[audit.py](audit.py) independently reconstructs the matrices using pair
projectors, checks their exact slacks with integer Bareiss elimination, and
reconstructs the sign certificate using tensor Newton interpolation. It imports
no author code. [expected.json](expected.json) is the compact independent
receipt; [VALIDATION.json](VALIDATION.json) records normal/optimized runs.

Python3.11+, standard library only. From a full repository checkout:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-reviewer-3/three-petal-audit/audit.py --author-results round-two/six-downset-1/MULTI_RESULTS.json --coefficients round-two/six-downset-1/MARGIN_COEFFICIENTS.json --check round-two/six-reviewer-3/three-petal-audit/expected.json
```

Repeat with `python3 -O -B` to check that all validation survives optimization.
Expected output includes `ok: true`,24 triples,263 coefficient terms,37,035
reconstructed original matrix entries compared by hash and10 rejected controls.
Expected receipt SHA256:
`1f308179875428689bb126f7b5d6c9aecc1a7035a844c4383f7b5e685eca15ad`.
The largest literal matrix is74; a fixed80-vertex implementation guard does
not restrict the mathematical theorem. Each run took about64seconds and less
than28MiB peak child RSS in the recorded environment. No solver is required.

The two author comparison inputs are SHA256-pinned inside the checker. If the
author directory has advanced, retrieve the original public inputs and pass
their local paths instead:

* [original result JSON](https://raw.githubusercontent.com/helgithorskarp/math_results/b0af2f14d21dd013a6d52e3bba7fa7d367950321/round-two/six-downset-1/MULTI_RESULTS.json)
* [original coefficient JSON](https://raw.githubusercontent.com/helgithorskarp/math_results/b0af2f14d21dd013a6d52e3bba7fa7d367950321/round-two/six-downset-1/MARGIN_COEFFICIENTS.json)

The proof and exact degree bounds explain why interpolation is an identity
certificate over an infinite parameter orthant. Finite matrix/census checks
are corroboration. Ordinary real linear algebra, the explicitly credited
forced-span/tensor inputs, inspected Python arithmetic and hash comparisons
remain the trust boundary. No private input or large omitted corpus is needed.
