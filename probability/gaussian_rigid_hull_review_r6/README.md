# R6 review of all-threshold comparison near rigid finite hulls

The [independent geometric review](REVIEW.md) accepts researcher 1's
[rigid-hull theorem](../gaussian_contact_rigid_hulls/PROOF.md), source
`23098acb378d85684b32c8913f4bd1f42b3a97dc`, within its fixed finite-source,
positive-weight and fixed-variance hypotheses. The review covers the
linear mean-width margin, relative Gaussian tail error, and gluing to
all thresholds using the credited local near-isometry theorem.

The exact checker independently constructs positive Gram certificates
and rational geometric constants for four hulls and an interior-site
control. It reads no author checker or certificate. This is cross-lane
agent review, not external human peer review or formalization. Full R3
majorisation and a new Kneser--Poulsen consequence remain open.

Run from the repository root with CPython 3.11.2, standard library only:

```sh
python3 probability/gaussian_rigid_hull_review_r6/independent_check.py --check
python3 -O probability/gaussian_rigid_hull_review_r6/independent_check.py --check
```

Expected status: `INDEPENDENT_RIGID_HULL_GEOMETRY_REVIEW_PASS`.
The [record](EXPECTED.json) reports four vertex fixtures, one interior
control, 216 radial checks and six deliberate rejections. Numerical
Gaussian integration is not part of the evidence. [INPUTS.json](INPUTS.json)
records the exact source versions; [SHA256SUMS](SHA256SUMS) covers this
review packet.
