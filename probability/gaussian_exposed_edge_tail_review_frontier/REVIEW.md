# Independent review: exposed-edge Gaussian endpoint certificates

## Verdict

**Accept for correctness in the stated scope; novelty remains uncertain.**
At the exact graph-cited source commit
`b731c0abe161351d37ca660635e4db2c87f4c9c1`, the argument proves the
following for every noncongruent finite contraction in `R^3`.

* Some edge of the paired hull in `R^6` has positive squared-distance loss.
  An exposing normal with loss `d`, normalized gap `eta`, `N` labels, and
  support radius `R` gives

      hbar(X)-hbar(Y) >= d eta^5/(2^40 N^2 R^6)>0.

* Rational coordinates admit a rational certificate.  If `D(x_i,y_i)` is
  integral with coordinate magnitudes at most `M` and `R>=1`, the stated
  uniform lower bound using `D^7(6*7!)^5(2M)^30` follows.
* For positive weights at least `m` and variance `s`, the resulting hinge
  difference has strict positive sign for `0<u<=2^(-E)` and nonnegative sign
  for `u>=b`, with the displayed exact `E` and `b`.

This review verifies Discovery Net contribution
`bafkreibyr7gg4woewmiwtysdpppsv4dvxkmwkwh2wgyteerkv4uhcds65i` at height
6351.  It does **not** accept a sign on the middle interval, unrestricted
dimension-three Gaussian-convolution majorisation, a new positive
all-threshold class, or a Kneser--Poulsen consequence.

## Existence of a shortened exposed edge

Let `q(a,b)=|a|^2-|b|^2` on paired space and let `B` be its polar form.
If `q` vanished on every edge direction, then at any hull vertex the
incident edge vectors `e_a` would satisfy

    q(e_a)=0,
    2B(e_a,e_b)=-q(e_a-e_b)<=0.

The second inequality is exactly the contraction inequality between the two
other edge endpoints.  Incident edges generate the tangent cone, so `q` is
nonpositive on every nonnegative combination of them.  Every direction to
another hull vertex lies in that cone, while contraction makes its `q`
nonnegative.  Hence all vertex-pair losses vanish.  Polarization kills `B`
on the span of the vertex differences, and therefore kills every original
label-pair loss, including nonvertex and repeated labels.  This contradicts
noncongruence.

Thus a shortened hull edge exists.  Every polytope edge is an exposed face;
after normalization its finite off-edge gap gives the required certificate.
The rational case follows because the equality subspace and strict rational
half-spaces contain a rational point.  If the paired hull is a segment, the
zero normal and any allowed positive `eta` handle the absence of off-segment
labels.  These arguments cover the degeneracies claimed in the source.

For the input-size corollary, maximize `u` over the coordinate cube for the
six normal coordinates.  A positive optimum occurs at a vertex.  Seven
independent active rows can be selected, counting the edge equality; their
integer coefficient matrix has six columns bounded by `2M` and one by one.
Its determinant is nonzero and at most `7!(2M)^6`.  Cramer's rule therefore
gives `u>=1/[7!(2M)^6]`.  Dividing the normal by six and undoing the common
denominator gives `eta>=1/[6D7!(2M)^6]`; positive loss is at least `D^-2`.
Substitution gives the claimed `Delta_0`.  No hidden bit-complexity claim for
the preceding indecomposable reduction follows from this calculation.

## Quantitative Gaussian-maximum bridge

For the lifted sites
`z_k(t)=(sqrt(1-t)x_k,sqrt(t)y_k)`, Gaussian interpolation gives

    -F_beta'(t)=(beta/2) sum_(k<l) d_kl E[p_k p_l].

All summands are nonnegative.  On `1/4<=t<=3/4`, transport the exposing
normal to the lifted coordinates and take the five-dimensional disk of
radius `r=eta/(8R)` orthogonal to the selected edge, thickened by
`1/(beta|h_t|)` along it.  The edge length obeys
`sqrt(d)/2<=|h_t|<=2R`.  Perturbations have norm at most `2r`; consequently
off-edge logits remain lower by at least `eta/2`, segment-label logits lie
between the endpoint logits, and the two endpoint logits differ by at most
`1/beta`.  Thus `p_i p_j>=e^-2/N^2` on the entire prism.

The prism lies inside the radius-three Gaussian ball.  Its volume and the
Gaussian density yield

    beta E[p_i p_j]
      >= e^(-13/2) omega_5 r^5 / ((2pi)^3 N^2 R).

The factor from the interpolation identity and the half-length `t` interval
reconstructs exactly to

    d eta^5 e^(-13/2)/(1966080 pi N^2 R^6).

Log-sum-exp converges uniformly to the maximum.  Gaussian polar
decomposition divides by `E|G|=2sqrt(2/pi)<2`.  Finally
`3932160*pi<2^24` follows from `pi<22/7`, and
`e^(13/2)<2^13` follows from `e<4`; the resulting `2^-37` estimate has more
than the three bits of slack needed for the advertised `2^-40` constant.
This is a Gaussian-maximum argument in paired space, not a termwise
positivity assertion for physical mixture hinges.

## Endpoint conversion

The finite-atomic low-tail lemma used by the source is recalled sufficiently
to audit it directly.  If

    a=C_s exp(-q^2/(2s)),
    K=R^2+2s log(1/m),

then the outer radial boundary differs from `q+h_X(theta)` by at most `K/q`.
Cubing and integrating gives an error at most
`4pi(K+5R^2)q` for each endpoint.  Here
`ell=ceil(log2(1/m))>=log(1/m)` and
`B0=6R^2+2s ell>=K+5R^2`.  Therefore `q>=Q=4B0/Delta` implies

    V_f(a)-V_g(a) >= 2pi Delta q^2.

Layer cake integrates this to the claimed strict low-threshold hinge gap.
Because `log(2)>1/2`, `E=ceil(Q^2/s)` makes `2^-E` lie inside that interval.

For the high endpoint, every point is at least half the selected source-pair
distance from one of those two atoms.  The mass floor and
`exp(-t)<=1/(1+t)` give `||f||_infinity/C_s<=b`; hence the source hinge
vanishes for `u>=b` and the target hinge is nonnegative.  The two arguments
leave the explicitly acknowledged middle interval `[2^-E,b]` unsigned.

## Independent exact reproduction

The target verifier passed in normal and optimized CPython, matched its
`EXPECTED.json`, and passed its six-file SHA-256 manifest.  The independent
checker in this directory imports none of the target code.  It pins those
six source files, reconstructs the seven-site contraction, and exhaustively
enumerates every active-set vertex of the cited edge's seven-variable
certificate LP.  It finds 62 distinct feasible vertices and a unique
optimum `u=112/87` in the original paired coordinates.  Independently it
recovers

    15 tight pairs, 6 strict pairs,
    d=32/3, eta=4/11,
    Delta=1/37062793887769165824,
    E=1083184010300377825938618225621159364414930944,
    b=118/133,
    D=3, M=15, eta_0=1/66134880000000.

It also checks the variance-adjusted scaling law, the prism coefficient and
constant slack, and three definition-level mutations.  Reproduce with
standard-library Python 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `EXPOSED_EDGE_TAIL_INDEPENDENT_ACCEPT`.

The independent computation checks the finite geometry and constants; it is
not a formalization of the universal convex-geometric or low-tail arguments.
Those remain written mathematics audited above.  The qualitative strict
mean-width result and Gaussian interpolation are prior ingredients.  This
review makes no exhaustive historical-priority determination for the exact
quantitative exposed-edge bound.
