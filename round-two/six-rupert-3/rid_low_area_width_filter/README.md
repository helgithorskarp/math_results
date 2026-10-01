# A RID area/width filter leaves only twofold source annuli

**six-rupert-3, researcher; 2026-10-01.** Author-checked, unformalized
geometric intermediate result with exact finite hypotheses. Independent
review and historical priority are not asserted. **The full RID Rupert
question remains open.**

The [proof](PROOF.md) supplies two useful reductions for the original
edge-two rhombicosidodecahedron. Write \(\phi=(1+\sqrt5)/2\),
\(A_1=\sqrt{940+1520\phi}\), and let \(\mu\) be physical minimum
projection width. Let \(\mathcal W\) be the six fivefold axes and
\(\mathcal T\) the fifteen twofold axes, including both unit-normal signs.

1. For receiving or source chord \(d\le1/30\) from \(\mathcal W\),
   \[
   \mu(n)^2\ge(20+32\phi)(1-(10/9)d^2).
   \]
   The tilt loss is **quadratic**. Actual adjacent contact vertices have
   opposite heights, so their spatial midpoint is equatorial. Its
   projected edge-line distance has no negative first-order term.
2. If \(0<\eta\le1/4\), a receiver with
   \[
   A(n_2)\le A_1+\eta,\qquad
   \mu(n_2)^2\le(20+32\phi)(1-10\eta^2/729)
   \]
   forces **every** closed-fit source of scale at least one within chord
   \(<1/8\) of \(\mathcal T\). The complete area polar has only two
   possible source orbits in this budget; quadratic width excludes the
   fivefold one. Source roll and physical translation are arbitrary.

For the exact receiver \(n_2=(1,0,12)/\sqrt{145}\), the filter passes
and circumradius gives the stronger annulus
\[
1/17<\operatorname{dist}(n_1,\mathcal T)<1/8.
\]
Its sixteen-corner shadow has area squared
\((28048+44032\phi)/29\), and minimum original axial height squared
\((2+3\phi)/145\). One actual perpendicular width direction is
\((12\phi,12,-\phi)\), with squared width
\((2371108+3159652\phi)/104401\), strictly below the filter threshold.
This ray is outside the specified prior twofold/fivefold caps and height
band; membership in every older geometric cover is not classified.
The source annulus includes the identical closed fit. **No all-source
passage exclusion or passage construction for this receiver is claimed.**

The concrete next problem is the remaining twofold source annuli with
arbitrary proper roll. The width estimate eliminates an entire alternative
source orbit without prescribing a nearby source or a numerical search.
Uniform scaling is handled in the proof; the normal chord is invariant.

## Reproduce

Python **3.11+**, standard library only. Keep both sibling prerequisite
directories. [DEPENDENCIES.json](DEPENDENCIES.json) pins the fivefold
geometry/cap source at commit `30c68fadf94ec1c0e891788177a5a5e1a8cc57b5`;
that source pins the original-hull/brightness source at
`58824907716016ff519f2aa5430fef92aa78c62c`. Both complete expected records
(3,536 and 4,452 bytes) replay unchanged before the new checks.
Run these separately from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
 timeout 55s python3 -B round-two/six-rupert-3/rid_low_area_width_filter/check.py
```

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
 timeout 55s python3 -B -O round-two/six-rupert-3/rid_low_area_width_filter/check.py
```

Both regenerate [expected.json](expected.json): **3,109 bytes**, SHA256
`62c99b8c370ccaba258951e6f14081aef91e0f4932c068c227f64672af9e1a16`.
Author runs: normal **12.947s**, **20,324 KiB** peak; optimized
**12.768s**, **24,836 KiB** peak, each under a separate 55-second deadline
and one process. `--emit` optionally regenerates the record. Exact
ordered \(\mathbb Q(\phi)\) decisions use `Fraction`; no numerical package
or solver is required.

The new finite checks cover all ten original contact edges, eighty strict
boundary comparisons, forty physical Gram/edge-distance identity checks,
all area/positive-root/width gates, the original example shadow and supports,
and the known identity-fit annulus. Six malformed/out-of-budget controls
reject with guards active under `-O`. This does not prove larger parameter
budgets impossible. The new continuum theorem is supplied by the written
proof; output theorem strings are descriptive metadata, not quantified
formal verification. Exact Python and the unformalized geometric bridges
remain trust boundaries. Reused area/polar methods and geometry are
credited; no floating passage search, private input or omitted large proof
corpus enters the claim.
