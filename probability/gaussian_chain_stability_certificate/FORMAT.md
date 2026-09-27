# Rational supplied-chain certificate format

All rational numbers are JSON integers or strings accepted by Python's
`Fraction`, such as `"3/2"`. Floating-point values and booleans are rejected.
Coordinates are length-three arrays. Indices are zero-based. Unknown optional
metadata does not establish any mathematical hypothesis.

Input schema: `chain-cloud-family-input-v1`.

- `stages`: at least two arrays of the same `n>=2` labelled points, including
  both endpoints. Adjacent stages are shared literally; separate link lists
  cannot silently disagree about their common intermediate law.
- `step_guards`: one dictionary for each adjacent pair of stages. `kind` is
  `norm`, `straight`, or `orthogonal_lift`. A `norm` guard has `anchors`, a pair
  of three-vectors whose norm equalities and radius bounds hold exactly.
  A `straight` guard checks every pair's terminal distance derivative.
  An `orthogonal_lift` guard checks affine-rank sum at most five. All three
  require every pair contraction. Unsupported motion labels are rejected.
- `comparison_radius`: integer `R>=1`, bounding the initial source about its
  endpoint center and every N link about its respective anchor.
- `endpoint_centers`: independent source/target translation centers.
- `endpoint_radius`: integer `Re>=1`, bounding the endpoint radii about those
  centers. It need not equal `R`; the initial source must satisfy both bounds.
- `mass_exponent`: integer `ell>=0`; all reference weights range over
  `v_i>=2^-ell`, `sum v_i=1`. The checker rejects an empty simplex.
- `variance_ratio`: rational `S>=1`; the spatial units have lower variance 1.
- `width_witness`: the existing `nested-hulls-rational-cap-v1` guard, with
  `target_in_source_hull` giving an `n` by `n` barycentric matrix **after the
  independent endpoint center translations**; a rational unit `cap_axis`;
  `cap_cosine` in `[0,1)`; a nonnegative `cap_sine_upper` whose square is at
  least `1-cap_cosine^2`; a `source_witness` index; and optional nonnegative
  `perpendicular_bits` (default 16). An insufficient cap is rejected rather
  than interpreted as a counterexample.
- Optional `endpoint_anchor_obstruction`: `n` rational coefficients satisfying
  the nonzero dual inconsistency witness in PROOF.md, equation (17). This
  affects the scope diagnostic, not the positive comparison proof.

Output schema: `chain-cloud-family-certificate-v1`. The record gives exact
per-step unordered loss sums and strict-pair counts, their endpoint telescope,
a uniform **ordered** loss floor for the entire prior simplex, rational cap
bounds, and the binary integer schedule. The conclusion is specifically
`[1,S]`, all thresholds, with the error guard

```
2*cloud_radius + l1(u-v) + l1(z-v) <= 2^-budget_exponent.
```

`N` is exactly the sufficient mixed-chain band exponent from R8's Theorem B
and `M=a+N`. Understating either exponent is deliberately rejected. The
`middle_band` ends at the actual source peak, which is the range needed
for the all-threshold cloud join. The imported margin itself is stronger.

`verify.py --input FILE --certificate FILE` checks inequalities, not a demand
for producer-minimal exponents. Conservative valid floors and budgets are
allowed. It does not import or call `certificate.py` in this mode. Both files
use exact integer/rational arithmetic, but their losses use different
representations and an extra endpoint variance telescope in the verifier.
Affine ranks are checked through scatter-matrix principal minors, separately
from the producer's rational row reduction.

Passing means that the displayed reference family satisfies the finite
hypotheses of the written theorem, with its explicit analytic dependencies.
There is no unsupplied chain search, completeness claim for all contractions,
cloud-membership oracle, floating-point sign inference, or independent peer
review hidden in the status string. Rejection means only that this sufficient
certificate format did not validate the supplied data.
