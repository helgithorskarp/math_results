# Review of the seven signed Gaussian beta diagonals

[REVIEW.md](REVIEW.md) accepts researcher 2's universal signs for N-j<=6,
the quantitative compact-frontier lower bound, polarized coefficient
positivity, equality cases and the first remaining rank-six classification.
The result is credited to the [reviewed source](../gaussian_beta_pair_conditioning/PROOF.md).
The full majorisation question and b_(7,0) remain open.

The review reconstructs the affine correction as a positive series of
Gaussian product integrals in dimensions 5,7,9,... and checks the author's
Poisson representation separately. It discloses the reviewer's prior
authorship of the weight-cell and uniform-frontier inputs. This is an
independent cross-lane agent audit, not external human review or formalization.

From the repository root, with standard-library Python 3.11 or later:

```sh
python3 probability/gaussian_beta_conditioning_review_r8/audit.py --check
python3 -O probability/gaussian_beta_conditioning_review_r8/audit.py --check
```

Expected status: `AFFINE_GAUSSIAN_PROJECTION_AUDIT_PASS`.
The canonical record hash is

    56cbdbde6f5bb00b3360a4b3e6d10974fffd946ecb020e2274b1d9eb1b640b3d

[EXPECTED.json](EXPECTED.json) holds the complete compact result.
[INPUTS.json](INPUTS.json) pins the inspected sources. The checker imports
none of them and reads no author certificate. Its exact geometry controls,
position-partition enumeration and compressed constants supplement the
written proof. No Gaussian integration is performed numerically.
Normal and optimized CPython 3.11.2 matched exactly; each audit took
about eight seconds in the review environment.
