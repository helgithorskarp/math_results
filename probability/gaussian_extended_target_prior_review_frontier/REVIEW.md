# Independent acceptance: extended-target full-prior Gaussian cell

## Verdict

I independently accept the result in source commit
`4e006ae51713af09a45229d9df59341a6f4fd03c`: at variance one, every
sixteen-component source/target pair in the stated coordinate boxes and with
each common label weight at least `15/256` has nonpositive source-minus-target
Gaussian hinge gap at every threshold.  The stronger stated margins on the
low and middle ranges are also certified.

This accepts a 105-parameter cell with arbitrary diffuse component laws.  It
does not accept full dimension-three Gaussian majorisation, any other
variance, a larger defect cap, or a Kneser--Poulsen conclusion.  The inherited
coordinate geometry and equal-prior cell were already independently reviewed;
this review addresses the new full-prior and diffuse-component quantifiers.
Novelty and historical priority were not audited.

## Proof audit

The key measure-side reduction is correct.  If `p0` is the uniform prior,
`p^i` is a simplex vertex, and `q^i=2p0-p^i`, the target hinge functional has
the common supporting plane

```text
G(p) >= G(p0) + ell.(p-p0).
```

Evaluating it at `q^i` bounds `ell.(p^i-p0)` from below.  Combining that same
linear functional with convexity of the source hinge and a barycentric
expansion of `p` gives

```text
F(p)-G(p) <= max_i [F(p^i)+G(q^i)-2G(p0)].
```

No convexity of `F-G`, differentiability of a level set, or coupling of the
component laws is used.  Here `p^i` has weights `31/256,15/256,...`, while
`q^i` has weights `1/256,17/256,...`; all auxiliary target mixtures are genuine
positive laws.  The tetrahedral group is transitive separately on the four
core and twelve flap labels, so exactly two asymmetric vertex curves remain.

The middle certificate uses upper source and backward-target kernel bounds and
a lower uniform-target bound with coefficient pattern `1,1,-2`.  Its absolute
coefficient sum is four, giving twice the accepted pair-hinge quadrature error;
only the two positive coefficients contribute omitted-tail error.  The
component displacement is less than `1/1024`.  Because a hinge integral of
equal-mass densities is Lipschitz in total variation, direct comparison of the
actual source and target mixtures with their reference mixtures costs at most
`1/1024` in total.  This comparison is made before applying the reference
supporting-plane certificate, so it is not multiplied by the auxiliary
coefficients.

For high thresholds, the normalized Gaussian Hessian has operator norm at
most one, the grid maximum therefore gives the stated peak enclosure, and
arbitrary component displacement costs at most `(61/100)/1024`.  Convexity in
the prior extends the two vertex peak bounds over the simplex.

For low thresholds, the mass floor yields the uniform source lower envelope
and the target upper envelope with all residual mass assigned to the largest
component.  Both densities have one outer radial boundary beyond the common
inner ball.  On each threshold window, the source radius at the left endpoint
and target radius at the right endpoint are valid for the whole window.
Signed Jacobian bounds are used in the correct direction.  The four finite
bands cover `S in [7/2,64]` without gaps, and the inherited projection estimate
with `log(256/15)<3` handles every `S>=64`.  Since `exp(-49/8)>1/512`, the low,
middle, and high ranges overlap.

## Reproduction and independent evidence

Both production executions reproduced `EXTENDED_TARGET_PRIOR_CELL_PASS` and
record hash `f1882e7c29809ef2b2fe81ca68b3fe8d3a365bc4e49e509c1358cd90a8a94ac4`.
The normal run took 247.816 seconds with peak RSS 355,128 KiB.  The target
optimized run took 245.075 seconds with peak RSS 356,700 KiB.  The target
manifest and all ten pinned dependencies pass.

`independent_check.py` imports none of the target verifier.  It:

* constructs all 24 signed-coordinate tetrahedral symmetries and checks their
  exact action on every source and target label;
* verifies transitivity on the core and flap label orbits and compares all 16
  asymmetric curves on an invariant 729-site rational-kernel grid;
* checks the supporting-plane bound on the actual 15-dimensional simplex for
  exact synthetic sixteen-component densities at every denominator-two
  barycentric point in four families and thirteen thresholds; and
* independently checks the committed middle and peak margins, coverage
  accounting for all 560 radial windows and 396,168 endpoint obligations,
  far-tail inequalities, threshold overlap, and the exact lattice-prior count.

Run from this directory with standard-library Python 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected marker: `INDEPENDENT_EXTENDED_TARGET_PRIOR_REVIEW_PASS`.

## Trust boundary

The production verifier performs the complete 13,997,521-site middle
calculation and checks every radial endpoint with outward integer exponential
bounds.  The independent checker validates the new extremal reduction,
sixteen-label symmetry, coverage arithmetic, and exact reported margins, but
does not independently regenerate the full middle histogram or all radial
roots.  Angular-chart coverage, nonsmooth Gaussian quadrature, and far-tail
projection estimates remain pinned, previously reviewed dependencies.  The
universal supporting-plane, perturbation, peak, and layer-cake arguments were
reviewed as written mathematics rather than formalized.  Floating root
proposals are not proof inputs; all accepted radial signs are exact.
