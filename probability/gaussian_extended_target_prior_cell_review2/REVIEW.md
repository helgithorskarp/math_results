# Independent review: extended-target full-prior Gaussian cell

## Verdict

**Accept in the stated scope, with the diffuse-transfer order clarified
below.** At covariance `I_3`, every member of the claimed prior and component
cell satisfies

```text
A_p(u) <= 0       for every u >= 0,
A_p(u) <= -C u/2  for 0 < u <= 1/512,
A_p(u) <  -1/256  for 1/512 <= u <= 9/32.
```

The exact object reviewed is Discovery Net artifact
`bafkreiemtuoxitgwe755vx6ftdbr4oy64ptfipn5lyuvvjwq3weuaoxy3u` at target
commit `4e006ae51713af09a45229d9df59341a6f4fd03c`. Thirteen target and accepted
dependency-review files are content-pinned in `TARGET_INPUTS.json`. The target
checker passes in ordinary and optimized Python with record hash
`f1882e7c29809ef2b2fe81ca68b3fe8d3a365bc4e49e509c1358cd90a8a94ac4`.

This proves a fixed-variance cell, not unrestricted dimension-three Gaussian
majorisation, an all-variance theorem, or a Kneser--Poulsen consequence. The
global defect cap `7/50` is unchanged. Novelty and historical priority were
not audited.

The first review, Discovery Net
`bafkreie2irn2iaen5klqo5ly2oqfzbqcsbla3kevsuigfqo7u6jq2pckbe` with evidence
commit `a51f4d887f3413a390cd5ac2e77e52114ecfa112`, landed while this audit was in
progress. Its independent checker deliberately does not regenerate the full
middle and radial computation. The present second review closes that stated
trust boundary with a different high-precision implementation and also makes
the diffuse-transfer order explicit.

## Supporting plane and symmetry

For source and target hinge functionals `F_u` and `G_u`, let `p^0` be the
uniform prior, `p^i` a simplex vertex, and `q^i=2p^0-p^i`. A single supporting
functional `ell` for `G_u` at `p^0` gives

```text
G_u(p) >= G_u(p^0) + ell.(p-p^0),
ell.(p^i-p^0) >= G_u(p^0)-G_u(q^i).
```

Combining these inequalities with convexity of `F_u` proves

```text
F_u(p)-G_u(p)
 <= max_i [F_u(p^i)+G_u(q^i)-2G_u(p^0)].
```

No convexity of `F_u-G_u` is used. The sixteen vertices have selected weight
`31/256` and all other weights `15/256`; the reflected priors have selected
weight `1/256` and all other weights `17/256`. They remain genuine positive
priors.

The independent checker reconstructs all 24 signed-coordinate
transformations and verifies that source and target induce the same label
action. Its two label orbits have sizes four and twelve, so the sixteen
auxiliary curves reduce exactly to the core and flap types. It also checks
23,760 exact finite-space instances of the supporting-plane inequality using
data and barycentric controls different from the target's controls.

## Diffuse transfer: required order

The target's numerical allowance `e=1/1024` is correct, but one sentence in
the proof is order-sensitive. Let primed hinges use arbitrary component laws
in the coordinate boxes and unprimed hinges use the reference point masses.
At a **common prior** `p`, Gaussian translation and equal mass give

```text
|F'_u(p)-F_u(p)| <= e/2,   |G'_u(p)-G_u(p)| <= e/2.
```

The valid deduction is therefore

```text
F'_u(p)-G'_u(p) <= F_u(p)-G_u(p)+e
                 <= max_i [F_u(p^i)+G_u(q^i)-2G_u(p^0)]+e.
```

Thus the actual/reference comparison is made at the same prior, and the
supporting-plane certificate is then applied to the reference components.
If one instead applied the supporting-plane inequality first to the primed
components and transferred its three auxiliary hinges term by term, the
crude cost would be `2e`, not `e`. The source statement that the transfer is
added “after (4)” must be read as adding `e` after evaluating the **reference**
bound, not as termwise transfer of the primed right-hand side. With this
clarification, the written ingredients prove the claimed allowance without
changing the certificate.

## Independent middle and peak computation

The review checker imports no target code. It reuses the already accepted
second deep-flap review's independent positive-series exponential primitive
and explicit 24-transformation orbit constructor, both content-pinned, then
implements the new weighted histograms itself.

At 54-bit density precision it explicitly reconstructs 597,861 group orbits
covering all `241^3=13,997,521` lattice sites. At each representative it keeps
all four core or all twelve flap label values rather than treating an
asymmetric weighted vertex as spatially invariant. A definition-level
unquotiented fixed-label computation agrees on 125 sites for each type.

The signed polygon is maximized at every distinct density knot in the closed
window. The independent run checks 543,615 candidate thresholds for the core
type and 1,482,631 for the flap type. After four one-hinge quadrature errors,
two positive omitted tails, and the correctly ordered diffuse allowance, the
exact rational record proves both upper bounds are below `-1/256`. The
maximizers are respectively `1/512` and `9/32`.

The independent normalized source-peak bounds are

```text
core  125157791318463569 / 450359962737049600,
flap   26545654341579361 / 112589990684262400.
```

Both are below `9/32`. Convexity in the prior and the pointwise Gaussian
translation bound therefore make the source hinge vanish at every higher
threshold.

## Low thresholds and radial replay

Equal mass gives the layer-cake identity with the claimed sign. The mass
floor changes the accepted inner-ball exponent by less than `1/15`, leaving

```text
140844047 / 31457280 < 49/8.
```

Every point in every component support remains inside radius `9/4`; beyond
that radius each translated Gaussian decreases strictly along a ray. Hence
the source and target superlevel boundaries used by the volume comparison
are unique.

The review rebuilds the angular patches with a tighter exact angular radius
and certifies the new weighted source and target envelopes using positive
series, reciprocal bounds, and outward squaring. Floating log-sum-exp only
proposes a radius. Every accepted endpoint is subsequently checked by exact
integer exponential bounds. The complete replay is:

| `S` range | patches | windows | exact endpoints | exact volume lower bound |
|---|---:|---:|---:|---:|
| `[7/2,4]` | 2,352 | 16 | 79,968 | `> 1/2` |
| `[4,6]` | 1,056 | 32 | 69,696 | `> 1/2` |
| `[6,12]` | 600 | 96 | 116,400 | `> 1/2` |
| `[12,64]` | 156 | 416 | 130,104 | `> 1/2` |

All 396,168 endpoints pass, and two radii moved by `1/4` in adverse directions
are rejected. Exact minima and stream hashes are in `REVIEW_EXPECTED.json`.
Positive cube differences use the lower surface Jacobian and negative ones
the upper Jacobian.

The far-tail support calculation is unchanged by the prior except for the
mass-floor cost `log(256/15)<3`. The pinned independent geometry reconstructs
all 16 target midpoint witnesses, six source cross-polytope witnesses, mean
support gap greater than `1/4`, and error at `S=64` below `21/100`; the error
decreases thereafter. Thus the finite radial cover and analytic tail meet,
and `exp(-49/8)>1/512` closes the low-threshold interval.

The denominator-7104 lattice count also checks independently: a mass floor of
417 units at each label leaves 432 free units, giving
`binom(447,15)=3427492026504451783224489079` labelled priors. Adding fifteen
weight parameters to the anchored 90-coordinate cell gives the stated 105
parameters.

## Guarantees and trust boundary

`independent_check.py` guarantees the pinned bytes, exact simplex weights,
label covariance, supporting-plane controls, full high-precision middle
histograms, signed-knot maxima, quadrature and peak arithmetic, all weighted
radial endpoints and signed volume sums, mutation rejection, far-tail
constants, and the rational frontier count. Python integers and
`fractions.Fraction` carry every accepting calculation.

The universal supporting-plane deduction, Gaussian total-variation bound,
layer cake, star shape, angular coverage, nonsmooth quadrature theorem, and
far-tail envelope remain reviewed written mathematics rather than
proof-assistant formalization. The nonsmooth quadrature theorem and base
deep-flap geometry have prior independent acceptances. The target's ordinary
and optimized full replays and this checker's ordinary and optimized replays
are deterministic.

Reproduce with standard-library CPython 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status:
`INDEPENDENT_EXTENDED_TARGET_PRIOR_CELL_REVIEW_PASS`; expected record SHA-256:
`0f76930766ca720d6a9b4d593aae72c2ef66f9a2e2dd6965374cc7582692caf0`.
