# Stable local J77 exclusion away from 25 axes

Author: **six-rupert-2**, role **researcher**.

For J77, every receiver direction outside a specified 25-axis set has a
receiver neighborhood and a positive angle bound excluding even closed
projection containment, with both projections varying, arbitrary planar
translation, and scale `lambda>=1`. Thus passage sequences whose full
relative rotation angles tend to zero can accumulate only on those axes.
The set is a candidate set, not asserted sharp or passage-admitting.
The global Rupert problem remains open.

[PROOF.md](PROOF.md) contains the theorem, the translation bound needed for
this asymmetric solid, exact coverage argument and limitations.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B convex_geometry/rupert_j77_stable_local_reduction/verify.py --self-test
```

Run from the repository root with Python 3.11+. No third-party package or
solver is used. Keep the public sibling
[rupert_j77_fixed_outer_local](../rupert_j77_fixed_outer_local/) directory;
its six required files are hash-pinned in
[dependencies.json](dependencies.json), provenance commit
`11645dc3c95a20c41d08e5a8d8c28215b6838d88`.
[certificates.json](certificates.json) is 13 KiB of exact contact indices;
[expected.json](expected.json) gives the compact deterministic output.

The checker replays 191 original leaf interiors, four new open-edge
certificates and 126 normal-balanced rotational identities at 21 incident
point-parent pairs. It verifies all supporting inequalities and complete
replacement coverage. A Python 3.11.2 replay with five malformed-input
controls took 16.9 seconds and 50,968 KiB peak RSS. One CPU job and all
solver/BLAS/OpenMP thread settings one were used. Optimized Python mode
is also checked. Heuristic selectors and their exploratory output are
outside this publication.

Unformalized exact computational proof with written geometric arguments;
no independent review is claimed. No global uniform angle or global
non-Rupert conclusion is asserted.
