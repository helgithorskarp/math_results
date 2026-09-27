# A rational geometric tail certificate for tight Gaussian contractions

[PROOF.md](PROOF.md) gives a quantitative mean-width margin from one
exposed edge of the paired configuration `(x_i,y_i)` in R6. If its
squared-distance loss is d, its normalized exposing gap is eta, there
are N labels, and both endpoint supports lie in B(0,R), then

    mean_support(X)-mean_support(Y)
        >= d eta^5/(2^40 N^2 R^6)>0.

Every noncongruent finite contraction has an eligible edge. Rational input
data admit a rational certificate. The bound supplies an explicit signed
low-threshold interval for the original map, allowing preserved distances
and image collisions. A simple source-peak bound supplies the upper interval.
The middle sign remains open.

There is also a uniform bound from rational input size. If all `D(x_i,y_i)`
are integer vectors with coordinates at most M in absolute value, and R>=1,

    mean_support(X)-mean_support(Y)
        >= 1/[2^40 N^2 R^6 D^7 (6*7!)^5 (2M)^30].

Every noncongruent rational contraction therefore has explicit signed
endpoints computable without an exposing vector. This controls the size of
the tail exponent for a given rational map. It does not bound the coordinate
size produced by the earlier indecomposable reduction or sign the middle.

This is a **complete author proof pending independent review**. Qualitative
strict mean-width comparison and the geometric Gaussian tail estimate are
credited prior results. The new content is their quantitative geometric
certificate interface for the tight indecomposable frontier. It gives no
new all-threshold class or Kneser--Poulsen conclusion.

From the repository root, using standard-library CPython 3.11 or later:

```sh
python3 -B probability/gaussian_exposed_edge_tail/verify.py --check
python3 -B -O probability/gaussian_exposed_edge_tail/verify.py --check
```

Expected status: `EXPOSED_EDGE_TAIL_CERTIFICATES_PASS`.
[EXPECTED.json](EXPECTED.json) records supplied rational certificates,
exact losses and margins, dyadic cutoff exponents, and rejection controls.
Use `--record` to regenerate it. The code is a verifier for compact supplied
geometry, not a general exposed-edge finder or a Gaussian integrator.
No enormous power of two is expanded to represent a tail cutoff.

The main fixture reuses the published seven-site positive indecomposable
example, which has 15 tight pairs and six strict pairs. Its known positivity
does not validate the new universal argument; it checks the certificate
plumbing on the intended tight-input class. [SOURCES.md](SOURCES.md) records
dependencies and the limits of the claim.

For this control the supplied-edge margin is exactly
`1/37062793887769165824`. At variance one and uniform weights its signed
tail extends to `2^(-1083184010300377825938618225621159364414930944)`;
the source-peak bound is `118/133`. These conservative endpoints illustrate
why no practical middle-certificate computation is claimed.
