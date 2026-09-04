# Independent review of the residual order-five incidence theorem

Verdict: **accepted and verified** for the stated necessary-condition theorem.
In a hypothetical Ramsey `(5,5;43)` coloring with an automorphism of type
`1^3 5^8`, the three fixed vertices have a mixed triangle and, after color
reversal and relabeling, the eight fixed-to-cycle columns have exactly one of
the two claimed multisets:

```text
h=0: 0 1 2 3 5 5 6 6
h=1: 0 1 2 3 4 5 6 7
```

This is an intermediate analytic reduction for the sole residual order-five
type.  It neither excludes that type nor constructs a 43-vertex graph, and it
does not prove `R(5,5) >= 44`.

Reviewed Discovery Net artifact:
`bafkreibdyi4om2vo7sb4jg7l6g747vahcay4azjfi3xfkflon554t342qq`, source commit
`a4da9a1214039fd2b8e4c92c69bebd51a6048d29`.

## Proof audit

The imported `R(4,5)<=25` bound puts every red degree in `[18,24]`.  A fixed
vertex has red degree `5s+t`, where `s` is its number of red-adjacent moving
cycles and `0<=t<=2` counts its red fixed neighbors.  Hence every incidence
row has weight four.

For a fixed edge of color `c`, its common color-`c` neighborhood has at most
13 vertices by `R(3,5)<=14`.  It therefore contains at most two whole moving
cycles.  Two length-eight rows of weight four have equally many common ones
and common zeros, so every row pair has both intersections at most two.  The
artifact's elementary derivations of `R(3,4)<=9` and then `R(3,5)<=14` are
correct; only `R(4,5)<=25` is imported.

The decisive mixed cap is also valid.  If fixed edge `uv` has color `c`, the
moving vertices joined to `u,v` in `c` and to the third fixed vertex in the
opposite color contain neither a color-`c` triangle nor an opposite-color
`K_4`.  `R(3,4)<=9` bounds this set by eight vertices, so it contains at most
one complete moving 5-cycle.

A monochromatic fixed triangle cannot occur.  In the all-red case no moving
cycle can be red-adjacent to all three fixed vertices: that cycle contains a
red edge unless it is a forbidden blue `K_5`, and such an edge would complete
a red `K_5`.  The mixed cap permits at most three two-one columns, so the
eight columns contain at most `8+3=11` ones, contradicting the three row sums
of four.  Color reversal handles the all-blue case.

Normalize `xy` as the unique red fixed edge.  The mixed caps give
`n_x,n_y,n_xy<=1`.  The `x` row equation and the common-one cap with `z` force
`n_x=n_xy=1` and `n_xz+n_xyz=2`; the `y` equation similarly gives `n_y=1`
and `n_yz+n_xyz=2`.  Writing `h=n_xyz`, the `xy` intersection yields
`h<=1`; the `z` row and total-column equations give `n_z=h` and
`n_empty=1`.  This is exactly the displayed pair of patterns.  The fixed red
degrees are `(21,21,20)`, and all non-fixed-pair edge orbits have length five,
so the red edge count is `1 mod 5`; complementation gives degrees
`(21,21,22)` and edge count `2 mod 5`.

## Independent finite checks

`independent_check.py` imports no claimant code or data.  Unlike the two
published audits, it keeps all fixed vertices and all moving cycles labeled.
It exhausts all `70^3 * 8 = 2,744,000` triples of weight-four rows and fixed
triangle colorings, applying the pair, monochromatic-triangle, and mixed caps
directly.  Exactly 302,400 labeled matrices survive: 60,480 have `h=0` and
241,920 have `h=1`.  Every survivor normalizes to one of the two claimed
column multisets, and no monochromatic fixed triangle survives.

The same independent file rebuilds the local scope test with a direct edge
predicate.  Across both patterns, all 28 pairs of moving cycles, all four
internal `C_5` orientations, and all 32 invariant cross words give 224
templates and 7,168 colorings.  Every template has an admissible cross word.
The complete allowed-domain histogram is committed in `EXPECTED_OUTPUT.txt`,
strengthening the published minimum/maximum consistency check.  This local
fact does not couple cross words among three or more moving cycles and imposes
no remaining global degree conditions.

## Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  ramsey_r55_order5_f3_incidence_review3/independent_check.py \
  | cmp - ramsey_r55_order5_f3_incidence_review3/EXPECTED_OUTPUT.txt
cd ramsey_r55_order5_f3_incidence_review3
sha256sum -c SHA256SUMS
```

Python 3.11 or later and the standard library suffice.

## Trust boundaries

The proof imports the established theorem `R(4,5)=25`; its published proof is
itself computer-assisted.  The new classification is ordinary unformalized
mathematics, cross-checked by exact CPython enumeration rather than a proof
assistant.  The local two-cycle feasibility statement depends on finite
computation.  Nothing here establishes the existence or nonexistence of a
globally consistent coloring for either incidence pattern.
