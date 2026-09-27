# Independent acceptance: support-cap localization

## Target and verdict

- Discovery Net artifact:
  `bafkreiaw7nlu2jooneqkbw4pbujsxgzrosyjclqjfkbfk2acv3vbm3tn3i`
- Exact reviewed source commit:
  `6eeb8a1d66bbbae6a998f814ba646bea9d2039d7`
- Reviewed source:
  [`../gaussian_support_cap_localization`](../gaussian_support_cap_localization/)

**Accept with high confidence.**  The proof correctly establishes eventual
full Gaussian majorisation for every fixed bounded contraction in `R^3` with
a strictly positive support half-mean-width gap.  Its quantitative cap-mass
version and its uniform labelled-cloud consumer have the stated cutoff

```text
s >= (2112 R^4/d) 2^(8N),
N = max(1,ceil(R(k+1)/b)).
```

The exact six-chart width certificate is valid and eventually succeeds for
every noncongruent rational finite contraction.  Together with genuine
support-cover and mass data, the proof correctly gives certificate existence
throughout the strictly positive support-width bounded-law sector.

This is an eventual-variance result.  It does not prove the unrestricted
all-variance conjecture, infer positive width for every non-isometric infinite
support, supply a measure-independent finite complexity bound, or prove an
additional Kneser--Poulsen volume theorem.

## Quantitative analytic join

Let `J(lambda)` be the spherical average of the source log-MGF minus the
target log-MGF.  A source cap of depth `a` and mass at least `2^-k` gives,
direction by direction,

```text
log M_mu(lambda theta) >= lambda(h_K(theta)-a)-k log 2,
log M_nu(lambda theta) <= lambda h_L(theta).
```

Thus a support-width lower bound `delta>=delta_0` gives
`J(lambda)>=lambda b-k` with `b=delta_0-a`, using `log 2<1`.  The definition
of `N` implies `J>=1` for `lambda>=N/R`.

On `1/(2R)<=lambda<=N/R`, the independently accepted spherical comparison
gives

```text
J(lambda) >= lambda^2 D exp(-4 lambda R)/12
          >= d exp(-4N)/(48R^2)
          >= d 2^(-8N)/(48R^2) = eta.
```

The last step has the correct orientation because `e<4`.  Since contraction
and the radius bound imply `d<=D<=4R^2`, one has `eta<=1/12`; hence the large
ray bound `J>=1` also dominates `eta`.  Substitution in the accepted endpoint
criterion gives

```text
44R^2/eta = (2112 R^4/d) 2^(8N),
```

and this automatically exceeds its separate `8R^2` requirement.  The two
lambda ranges meet exactly, so no moving threshold or middle interval is
left untreated.

## Fixed bounded laws

For compact `K=supp(mu)`, a finite `a/4`-net chosen inside `K` supplies a
uniform positive cap mass.  A net point within `a/4` of an exposed maximizer
has its entire `a/4` support ball inside the depth-`a` cap, and every such
ball has positive measure by the definition of support.  Taking the minimum
over finitely many balls produces a finite `k`.

If the mean pair loss `D` were zero, continuity and full support would make
every pair loss zero on `K x K`; the accepted equality case then makes the
endpoint map an isometry on the support, forcing zero support-width gap.
Thus positive width supplies `D>0`, and the quantitative theorem applies.
No atom mass, covariance floor, or strict Lipschitz constant is inserted.

The proof is careful not to reverse this implication for arbitrary infinite
supports.  Finite strict mean-width comparison does not by itself establish
strictness for an infinite compact support.

## Uniform finite-cover consumer

For a labelled cloud, the common-weight hypothesis gives
`q_i q_j >= (1-rho)^2 p_i p_j`.  If a reference pair difference `v` has
`|v|<=2R0` and its cloud perturbation has `|e|<=2r`, then

```text
abs(|v+e|^2-|v|^2) <= 8R0 r+4r^2.
```

Paying this error at both endpoints and using nonnegative reference losses
proves

```text
D_actual >= (1-rho)^2 D0-16R0 r-8r^2 = d.
```

For each direction, the cloud attached to a maximizing source reference site
has mass at least `(1-rho) min_i p_i`, source projection at least
`h_X-r`, and target support at most `h_Y+r`.  This directly yields
`J_actual(lambda)>=lambda(w-2r)-k`, without first approximating the actual
support width and paying a second displacement error.  The actual-cloud
contraction remains an explicit premise and is not inferred from the cover.

## Exact width certificate

The six cube faces, under radial projection, cover `S^2` up to null
boundaries.  If `v=(+/-1,u,v)` and `q=1+u^2+v^2`, the area Jacobian is
`q^(-3/2)` and homogeneity contributes `q^(-1/2)`.  Therefore the normalized
width integral is exactly

```text
(4 pi)^(-1) sum_faces integral g(v)/q^2 du dv.
```

For normalized sites, each coordinate derivative of the support-function
difference has magnitude at most two and `|g(v)|<=2 sqrt(q)`.  Differentiating
`g/q^2` gives the valid coordinate bound

```text
2/q^2 + 8|u|/q^(5/2) <= 10.
```

Each square of side `2/M` is therefore within `20/M` of its midpoint value.
The total parameter area of six faces is 24, yielding the stated global
error `480/M`.

The integer cell formula has the correct normalization:

```text
C = 4M (max_i X_i.z-max_i Y_i.z)
        / (H(M^2+a^2+b^2)^2).
```

Python integer `//` rounds downward even for negative cells, so summing
`floor(2^B C)` gives a genuine lower midpoint sum.  The extra rounding loss
is at most `6M^2 2^-B`.  When the resulting integral lower bound is positive,
`pi<4` gives the physical half-width lower bound `R0 I_low/16`; the positivity
guard is necessary and correctly enforced.

With `B=max(32,4 bit_length(M))`, both the global quadrature error and the
rounding error vanish as `M` grows.  Gorbovickis strictness supplies a positive
finite-reference width unless the labelled configurations are congruent, so
the rational mesh eventually certifies every noncongruent finite reference.

## Certificate-existence boundary

Successively finer finite nets from the original support, with Voronoi cell
masses, give genuine source and image covers.  Each distinct net site owns a
small support ball and hence has positive cell mass.  Hausdorff convergence
of the endpoint hulls makes the reference width converge to the positive
support width, while the pair perturbation estimate makes `D0` converge to
`D>0`.  A sufficiently fine cover therefore has positive width and loss
reserves.

For rationalization, a tiny uniform contraction of the finite target creates
strict slack on every distinct source pair.  Finite rational perturbations of
both labelled lists can then preserve all contractions, and positive weights
can be approximated with arbitrarily small relative error.  Continuity keeps
the already strict reserves positive.  This proves existence, but it is not
an algorithm for extracting exact cap masses from an unspecified measure.

## Independent exact evidence

[`independent_check.py`](independent_check.py) imports no target module and
uses a materially different width computation.  Instead of midpoint values
plus one global `480/M` error, each cell gets a pointwise interval lower
bound:

- one source affine branch, chosen at the midpoint, minorizes the source
  support function throughout the cell;
- all target branches at all four corners majorize the target support
  function throughout the cell; and
- the minimum or maximum `q` endpoint is selected according to whether the
  resulting gap is negative or nonnegative.

Every cell contribution is then rounded downward as one exact rational.  On
the published fixture, a mesh of only 64 and 40 rounding bits certifies all
24,576 cells, including 36 cells with negative gap.  It obtains

```text
width >= 790915992361/2199023255552,
N = 28,
cutoff exponent = 224.
```

This independently signs the same family and is stronger for this fixture
than the author certificate (`N=64`, exponent `512`); it is a finite
certificate improvement, not a strengthening of the universal theorem.  The
checker separately recovers the author loss reserve and mass exponent,
verifies the exact endpoint constant, tests a segment of known width, rejects
a rotated isometry, exercises 800 negative control cells, rejects an expanding
reference, and rejects zero loss reserve.  Eleven source/dependency files are
content-pinned.

Normal and optimized CPython runs match [`EXPECTED.json`](EXPECTED.json),
status `INDEPENDENT_SUPPORT_CAP_REVIEW_PASS`, record SHA-256
`903d67a9693578ca7014ee38191edd788e18c0fa21b7dbe90df79d1c194f46a6`.
The author producer, supplied-record verifier, normal audit, and optimized
audit were also replayed exactly; their runtimes here were approximately
5.3, 6.1, 20.6, and 23.4 seconds.

## Trust boundary and novelty

The exact programs guarantee their finite rational arithmetic, chart coverage,
rounding direction, reserves, schedules, fixtures, and provenance pins.  They
do not prove the continuum theorem.  The two accepted spherical/endpoint
dependencies, compact-support cap argument, support-limit passage, and
certificate-existence argument remain conventionally reviewed mathematics,
not proof-assistant output.

Aishwarya--Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*](https://arxiv.org/abs/2609.07041), states the unrestricted
majorisation conjecture and proves full preservation only through lower
dimensions or stronger pressure classes.  Gorbovickis,
[*Strict Kneser--Poulsen conjecture for large
radii*](https://arxiv.org/abs/1006.0531), Theorem 1.5, gives strict convex-hull
mean-width increase for noncongruent finite expansions, with exactly the
orientation used here.  The target does not extend that strictness silently
to infinite supports.  Historical priority for this support-cap join was not
established by this bounded source review.

## Reproduction

From this directory:

```sh
python3 -B independent_check.py > /tmp/support-cap-review.json
cmp /tmp/support-cap-review.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/support-cap-review-opt.json
cmp /tmp/support-cap-review-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_SUPPORT_CAP_REVIEW_PASS`.
