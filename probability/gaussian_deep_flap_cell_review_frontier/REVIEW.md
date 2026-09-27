# Independent review: gap-free deep-flap Gaussian cell

## Verdict

**Accept for correctness in the stated scope; novelty remains uncertain.**  At
the graph-cited source/main commit
`8ee386da005a59786fbbab26eb673856e7200346` (original mathematical commit
`9a3465863e32c53d9594f202a0bcc28fb58578f8`), the proof establishes every
Gaussian hinge inequality at variance one throughout the specified
96-coordinate box around the sixteen-label depth-two simplex-flap
configuration.  Later commit `c35bfcc212f282e2ac0f3c5c9f2b78055e11017c`
only refreshes `SOURCES.md` with subsequent review boundaries; no theorem,
input, checker, or expected-result byte changes.  In the source notation,

```text
H(u) <= 0                         for every u>=0,
H(u) <= -C u/2                    for 0<u<=1/512,
H(u) <  -1/128                    for 1/512<=u<=9/32.
```

The source peak is below `9/32`, closing the remaining thresholds.  The
anchored slice has 90 independent coordinates and its denominator-2048
lattice slice lies in the stated rational frontier.  This review verifies
Discovery Net contribution
`bafkreidewnncabhfdz4rugy7wqmrcl6hnuyqyj6d2vbehj7vdji3mkdt7m` at
height 6341.

This is a fixed-variance positive cell.  It does **not** prove unrestricted
dimension-three Gaussian majorisation, an all-variance flap theorem, a
nonliftability result for the damped cell, or a Kneser--Poulsen consequence.

## Geometry and perturbation

Direct rational recomputation gives reference minimum pair loss `127/2048`,
minimum source squared separation `2`, minimum target squared separation
`3969/4096`, and paired rank six.  A coordinate perturbation of size
`1/2048` has Euclidean norm below `e=1/1024`.  For a source pair and target
pair, the adverse endpoint perturbations have norms at most `2e`; squaring
the lower source and upper target distance cancels the two `4e^2` terms.
Using the endpoint diameter bounds therefore leaves

```text
127/2048 - 4e(2*9/4 + 2*27/16) = 1/32 > 0.
```

Thus every member of the box is a strict labeled contraction.  Separate
translations of the two configurations preserve all pair losses and both
hinge profiles, so the two label-zero anchors remove exactly six coordinate
parameters.  The frontier label, radius, loss, denominator, and mass-unit
bounds then check as stated.

## Low thresholds: analytic reduction

For normalized densities `F=f/C` and `G=g/C`, equal mass and layer cake give
the exact adverse-sign identity

```text
H(u) = -C integral_0^u ( |{F>v}| - |{G>v}| ) dv.
```

The superlevel sets used in the low tail are genuinely star shaped.  The
uniform Jensen estimate contains the radius-`9/4` ball in every relevant
superlevel.  Beyond that radius each Gaussian summand decreases strictly
along each ray because every actual center has smaller norm.  Consequently
each ray has one outer boundary and spherical radial integration applies;
no mixture-unimodality assumption is being smuggled into the computation.

The two triangular charts, acted on by the 24 reference symmetries, cover
the sphere up to null walls.  On each parameter patch the normalization-map
Lipschitz bound, outward dot-product and norm bounds, and lower/upper
Jacobian choices have the correct directions.  In particular a negative
radial-cube contribution is multiplied by the upper Jacobian.  Source radii
are taken at the left endpoint of each `S` window and target radii at the
right endpoint, which is the correct monotonic choice for a uniform lower
bound throughout the window.

## Independent radial reproduction

The target verifier encloses exponentials with an alternating Taylor series
after range reduction.  The review checker imports none of the target code
and instead uses, for `x>=0`,

```text
(1-x/2^k)^(2^k) <= exp(-x) <= (1+x/2^k)^(-2^k).
```

It computes both powers by repeated fixed-point squaring rounded downward;
the upper exponential endpoint is an outward reciprocal.  A separate exact
rational Taylor-remainder enclosure intersects all 30 scalar controls.  The
floating bisection only proposes dyadic radii, with a deliberately wider
32-unit buffer; every used radius is then accepted or rejected by the
binomial enclosure.

This second implementation rebuilds the angular patches with a tighter
`sqrt(2)/(2n)` parameter-radius bound and verifies the **entire** finite
cover:

| range | patches | windows | exact roots | independent minimum |
|---|---:|---:|---:|---:|
| `[7/2,6]` | 600 | 40 | 49,200 | `2121864039369680317667819009080700745821 / 95704415696513942849074108340184809472` |
| `[6,64]` | 156 | 464 | 145,080 | `31473125097940767775357764841923176027 / 2990762990516060714033565885630775296` |

Both minima exceed `1/2`; their worst windows again begin at `7/2` and `6`.
The review also rejects two roots moved by `1/4` in the adverse direction
and a deliberately reversed interval.  This independently closes every
finite radial window rather than merely spot-checking the author's stream
hashes.

## Infinite tail

Every undamped reference target is a midpoint of two source sites.  The
source hull contains the six cross-polytope points `+/-3e_i/2`, so endpoint
perturbations preserve a strictly positive support-function gap.  The target
core still contains the origin in its interior.  An independently rebuilt
`n=12` angular enclosure gives normalized mean-support gap

```text
6138195190884746203548042905540225 /
21418224541456163967688297358032896 > 1/4.
```

The source and target radial envelopes

```text
rho_F >= S+h_X-A/S,       rho_G <= S+h_Y+B/S
```

follow respectively from one maximal source summand and the full target
upper envelope.  Comparing their cubes loses at most

```text
E(S)=A/S(1+R_X/S)^2+B/S(1+R_Y/S+B/S^2)^2.
```

This decreases in `S`, and the exact value at `64` is below `21/100`.
Together with the mean-support gap above, it proves the volume difference
exceeds `1/2` for every `S>=64`.  Since `exp(-49/8)>1/512`, layer cake now
gives the claimed low-threshold hinge bound all the way to zero.

## Middle and high thresholds

The target's normal and optimized full replays agree byte-for-byte with
`EXPECTED.json`.  They reconstruct all `13,997,521` lattice sites from
`597,861` exact symmetry orbits, use outward 48-bit source/target density
bounds, and maximize the adverse polygon at all 124,991 relevant knots.
The orbit formula is complete: an absolute sorted triple with a zero
coordinate has one sign orbit, while a strictly positive triple has the two
even-sign parity orbits represented by `(i,j,k)` and `(-i,j,k)`; the recorded
multiplicities sum to `241^3`.

The inherited nonsmooth quadrature theorem has a prior independent review.
Its uniform two-endpoint error, finite-tail error, and the two endpoint
translation costs yield the exact upper bound

```text
-345085628268564267007366684564175 /
41538374868278621028243970633760768 < -1/128.
```

The translation allowance is correctly `e`, not `2e`: for each endpoint,
equal mass converts the hinge change to at most half the `L1` distance, and
the Gaussian directional `L1` derivative is below one, giving at most
`e/2` per endpoint.  Finally the grid covering radius, normalized Gaussian
gradient bound, and outside-cube estimate give source peak

```text
969464083099761/3518437208883200 < 9/32.
```

Thus `[0,1/512]`, `[1/512,9/32]`, and `[9/32,infinity)` meet at their
endpoints and leave no threshold gap.

## Reproduction and trust boundary

The target was replayed in normal and optimized CPython, its outputs matched
one another and `EXPECTED.json`, and every target manifest entry passed.
Reproduce the independent audit from this directory with Python 3.11 or
later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `DEEP_FLAP_CELL_INDEPENDENT_ACCEPT`.  A run takes roughly
two minutes on one CPU.

The independent checker guarantees the nine pinned target files, geometry,
full alternate radial cover, far-tail mean-support enclosure, exact recorded
middle/high margins, and mutation rejection.  It does not independently
reimplement the 13.9-million-site middle histogram; acceptance there rests
on direct code inspection, two exact author replays, small entry-level
unquotiented controls, and the already reviewed quadrature theorem.  The
layer-cake, star-shape, symmetry, perturbation, and far-tail deductions remain
written mathematics checked above.

The primary manuscript still presents unrestricted Gaussian-convolution
majorisation as a conjecture in dimension three.  Cheng--Tan--Zheng supplies
the classical continuous-expansion obstruction motivating the simplex-flap
geometry, not this Gaussian sign certificate.  This review makes no
exhaustive historical-priority determination for the signed radial-volume
method or the particular certified cell.
