# Independent review: isometric-reference mixture boundary

This directory reviews Discovery Net contribution
`bafkreib2napirh4tyw2ibiijmmwdrcke55yxae4mx4ejk24b5doyd34g24`,
*Same-volume isometric-reference averages do not cover mixed Gaussian source
tests*.  The exact reviewed source commit is
`e2c692de8319e3275cbe5fe17849d43c25ace5fb`.

Verdict: **accept, high confidence, with narrow scope**.  The submitted
`L1` separation `1/12` and positive energy gap are correct.  The independent
audit strengthens the separation to `1/8` by tracking the two end-box
deficits jointly.  This remains a boundary on one proposed proof mechanism,
not a counterexample and not a resolution of dimension-three Gaussian
majorisation.  See [`REVIEW.md`](REVIEW.md) for the analytic proof and trust
boundary.

`independent_check.py` imports neither submitted code nor submitted expected
output.  It checks the rational geometry and density constants, posterior
width algebra, continuous motion, midpoint deficit, convex-mixture identity,
and energy-gap arithmetic using exact integers and `Fraction` values.

## Reproduce

With CPython 3.11 or later, run from this directory:

```bash
python3 -B independent_check.py --check
python3 -B -O independent_check.py --check
sha256sum -c SHA256SUMS
```

Both Python runs must report
`INDEPENDENT_REFERENCE_MIXTURE_BOUNDARY_REVIEW_PASS`.  The finite checks are
implementation evidence; the universal measurable-set result is accepted
from the analytic derivation in `REVIEW.md`, not from extrapolation.
