# Second independent review verdict

**Verdict: accept in the stated scope.**  At covariance `I_3`, every member
of the target's 96-coordinate deep-flap cell satisfies its claimed Gaussian
hinge comparison at every threshold.  The conclusion is an explicit
fixed-variance cell, not unrestricted dimension-three majorisation, an
all-variance theorem, or a new Kneser--Poulsen consequence.

## Exact object reviewed

- Discovery Net target:
  `bafkreidewnncabhfdz4rugy7wqmrcl6hnuyqyj6d2vbehj7vdji3mkdt7m`.
- Verified target commit: `8ee386da005a59786fbbab26eb673856e7200346`.
- First independent review: Discovery Net
  `bafkreih4knvvl5grkggcsm26sa33esepgwus6zqcwwi2hzm5ie7w32ipcm`,
  published source boundary `660c395774692d339baba960d89c612ba2702e62`.
- Twelve target, inherited-dependency, and first-review files are content-pinned by
  `TARGET_INPUTS.json`.
- The author checker passes under ordinary and optimized Python, and its
  checksum manifest passes.

## Independent computation

The first independent review already certifies the entire radial cover with
a binomial exponential enclosure, but explicitly does not reimplement the
13.9-million-site middle histogram.  This second review closes that remaining
computational boundary at higher precision.  Its additional positive-series
radial replay is a third enclosure method and confirms, rather than merely
repeating, the already independently accepted low tail.

The new proof obligation is the low-threshold signed radial-volume cover.
The target encloses exponentials by an alternating fixed-point series.  The
review checker instead encloses positive `exp(r)` series, adds a geometric
tail, reciprocates outward, and squares after range reduction.  Twelve
higher-precision rational controls test this independent primitive, and two
deliberately damaged radial endpoints are rejected.

The angular charts are regenerated at 44-bit precision using the exact
parameter-square radius `1/(sqrt(2)n)` rather than the target's coarser
`3/(4n)` bound.  At 22-bit radial resolution and 58-bit exponential
precision, all 194,280 endpoints are checked:

- 49,200 endpoints on `[7/2,6]`, with minimum signed-volume lower bound
  `2830909891356874710162247650145836881927 /
   127605887595351923798765477786913079296`;
- 145,080 endpoints on `[6,64]`, with minimum lower bound
  `224618509917193810995970841674548649671 /
   21267647932558653966460912964485513216`.

Both bounds are greater than `1/2`; their worst windows begin at `7/2` and
`6`, respectively.  Positive patch contributions use the lower Jacobian and
negative contributions use the upper Jacobian.

The middle computation is also independent.  It constructs each orbit by
applying the 24 tetrahedral transformations to a representative rather than
using the target multiplicity formula.  A direct unquotiented control agrees
on 125 sites.  At 56-bit precision, 597,861 explicit orbits reconstruct all
13,997,521 lattice sites and all 124,992 candidate thresholds.  The resulting
cell adverse upper bound is

`-194265938362851489846245777476205532474452798247 /
 23384026197294446691258957323460528314494920687616`,

which is strictly below `-1/128`.  The independent source-peak upper bound
`124091402636767683/450359962737049600` is strictly below `9/32`.

## Analytic audit

The pair-loss calculation gives reference minimum `127/2048` and uniform
cell floor `1/32`.  The displayed paired determinant is independently
recomputed as `-250047/4096`.

The layer-cake identity has the target's sign: equal mass converts the
adverse hinge into minus the integral of the source-minus-target superlevel
volume.  Jensen's inequality places the ball of radius `9/4` inside both
low superlevel sets.  Beyond that ball every summand decreases along each
ray, establishing the unique radial boundary used by the finite cover.

The two triangular charts cover the sphere, up to null walls, under the
24-element symmetry group.  Actual cell members need not be symmetric:
the coordinate perturbation is included independently in every dot and
norm enclosure before the reference labels are permuted.

For the infinite tail, all 16 target midpoint witnesses and all six source
cross-polytope witnesses are independently reconstructed.  They imply the
strict support gap `41/3584`.  The angular mean-support lower bound is

`127879066476765543630230550243401 /
 446213011280336749326839528292352 > 1/4`.

The far-tail error at `S=64` is independently recovered as
`1743464522020333/8589934592000000 < 21/100`, and it decreases thereafter.
Thus the finite radial bands and the analytic tail meet without a gap.

Finally, moving each source or target center by Euclidean distance at most
`1/1024` costs at most `1/2048` in total variation, giving the stated total
hinge transfer loss `1/1024`.  The middle and peak ranges therefore join the
low radial range at `1/512` and `9/32` with no uncovered threshold.

## Guarantees, assumptions, and limits

`independent_check.py` guarantees the pinned bytes, exact geometry, complete
angular and threshold-window counts, every outward-rounded radial endpoint,
signed volume sums, group-orbit coverage, middle-knot maximum, quadrature
arithmetic, peak cutoff, and far-tail rational inequalities using Python
integers and `fractions.Fraction`.

The layer-cake, Jensen/star-shaped, symmetry, perturbation, radial-envelope,
and quadrature reductions remain reviewed written mathematics rather than a
proof-assistant formalization.  The accepted direct-hinge quadrature estimate
is an explicit dependency.  Floating point proposes endpoints only; every
endpoint used in a conclusion is subsequently checked by independent exact
integer enclosures.  No novelty or priority claim is assessed.
