# Which finite Lp measurements identify a convex body?

For a smooth origin-symmetric convex body K with positive curvature, fix
p>1 and a finite-dimensional space W of even Holder-continuous functions
on the sphere. Measure volume and the integrals of functions in W against
the Lp surface area measure h_K^(1-p) dS_K.

**These data identify K among all symmetric convex bodies exactly when
h_K^p belongs to W.** Otherwise the nearby equal-data bodies form an
infinite-dimensional manifold. The proof includes p equal to the dimension.

For the Firey translation-volume function, this gives an exact criterion
for uniqueness from volume and one even Taylor term: the corresponding
power of the support function must be a homogeneous polynomial. It also
gives:

- A complete quadratic-jet classification among all symmetric bodies,
  including nonsmooth ones: precisely the ellipsoids are uniquely identified.
- Explicit smooth positive-curvature bodies with every even minimum full
  jet order p, in every dimension d>=2:
  `h(x)=(|x|^p + e Re(x_1+i x_2)^p)^(1/p)`,
  `0<|e|<=1/(4p)`.

Read [PROOF.md](PROOF.md) for exact hypotheses and the complete analytic
argument, [SOURCES.md](SOURCES.md) for attribution and novelty limits, and
[VALIDATION.md](VALIDATION.md) for the finite checks and trust boundary.

From this directory, with CPython 3.11 or later and no external packages:

```sh
python3 -B verify.py
sha256sum -c SHA256SUMS
```

The checker must match [expected.json](expected.json) and print `VERIFIED`.
It uses exact rational arithmetic to audit variations, spherical integrals,
normalizations, affine examples and the sharpness construction. It does not
replace the analytic proof. No solver, downloaded dataset or large
certificate is needed.

The finite-measurement converse assumes positive C^(2,alpha) support
curvature. The single-term criterion does not classify arbitrary full
jets with several different Lp indices. The main proof is independent of
the previous polytope theorem; the Firey application imports its
[Taylor coefficient formula](../firey_volume_sharp_jets/PROOF.md).

Status: proved here by an unformalized analytic argument; independent
review pending. No historical-priority claim.
