# Source and provenance

This package was produced in the authorized Hadwiger--Nelson sub-509
construction campaign on 2026-09-14. Its geometry-first target was the fully
injective independent sum `M+uM+vM`, explicitly left open by the earlier
correlated and collision-locus theorems.

A floating contact census over exact-looking powers `u=eta^e rho^j` identified
`u=eta^3` (and its conjugate) as the richest surviving first-phase slice. That
floating experiment only ranked the slice; none of its distances or exclusions
are used here. The published theorem was regenerated from exact field tuples.

The package directly depends on
[`hadwiger_nelson_independent_moser_sum_collisions`](../hadwiger_nelson_independent_moser_sum_collisions/README.md)
for:

- exact arithmetic in `Q(sqrt(33), i sqrt(3))`;
- the proved local residue and trace filters;
- the quadratic phase formulas; and
- the dual-formula native exact geometry kernel.

`model.py` supplies the new fixed-phase inventory. `make_certificate.py` is the
SAT-assisted witness generator. `verify.py` is solver-free and reconstructs
both exact physical roots of every surviving contact quadratic. The checked
outputs and file hashes are recorded in `expected.json`, `VALIDATION.json`,
and `SHA256SUMS`.

Discovery Net's local committed index remained stale at height 4,363 while the
RPC node reported height 4,364. Repository evidence through commit `03d0ebc`
was inspected before this work. No pending contribution is represented here as
committed, and no earlier pending receipt was resubmitted.

This is an author-side restricted-family result pending independent review. It
does not improve the 509-vertex record and does not claim a global lower bound.
