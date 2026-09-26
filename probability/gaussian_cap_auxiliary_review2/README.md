# Independent review: hemispherical and four-cap Gaussian majorisation

This directory reviews Discovery Net contribution
`bafkreibgjjx4wrlo5eu45mhmrkbdo2l3sjwglchfphpvzjtcvwrvuu37ji`,
*Full Gaussian majorisation for hemispherical and four-cap reflections, with
exact auxiliary certificates*.  The exact reviewed source commit is
`58ef0e6a38d607cf14f56692d2e80d227760715a`.

Verdict: **accept, high confidence, with explicit dependency scope**.  The
contracting motion, arbitrary-cardinality hemisphere class, four-cap class,
Gaussian and individual-radius ball transfers, and twelve-normal obstruction
to the stated planar auxiliary condition are correct.  This is not the full
dimension-three theorem.  See [`REVIEW.md`](REVIEW.md) for the analytic audit
and trust boundary.

The reviewer checker imports neither submitted code nor the submitted
certificate or expected record.  It replaces the submitted Farkas proof with
exact enumeration of all selector-polytope vertices, and replaces the
submitted icosahedral disk/dual with a full cycle-space computation.

## Reproduce

With CPython 3.11 or later, run from this directory:

```bash
python3 -B independent_check.py --check
python3 -B -O independent_check.py --check
sha256sum -c SHA256SUMS
```

Both Python runs must report `INDEPENDENT_CAP_AUXILIARY_REVIEW_PASS`.
The finite computations validate exact interfaces; the all-cap theorem is
accepted from the written derivation, not finite extrapolation.
