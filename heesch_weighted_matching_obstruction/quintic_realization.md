# Self-compatible colors and directions with exact quintic edges

Author: **six-heesch-3**, role: researcher.

This is an explicit geometric realization of a **rotations-only** marked
polyform model. Arbitrary Euclidean motions are allowed for the resulting
unmarked shape; the curves themselves force a common handedness. The use of
colors, directions and bumps/nicks is established prior art, including
Mann and Thomas, *Heesch Numbers of Edge-Marked Polyforms*, Experimental
Mathematics 25 (2016), 281–294,
[DOI](https://doi.org/10.1080/10586458.2015.1096867).
That paper's full matching/motion tables were not accessible in this pass;
no larger marked record is assumed and no historical priority is claimed.

## Explicit marked model and shape

Let `S` be a simple unit-side polyomino, polyiamond or regular polyhex.
Every boundary unit edge has a color `c` in `{1,...,m}` and a state `s` in
`{-1,0,+1}`. A neighboring pair is legal exactly when its colors are equal
and its states are opposite. Thus `s=0` is self-compatible. The nonzero
states may be viewed as arrows along the boundary's counterclockwise
tangent: opposite states on opposite tangents give the same physical arrow
direction. State zero is not a wildcard for a directed edge. The marked
grid model allows translations and rotations preserving the cell grid,
without reflections.

Set

```
eta = 1/(100*m),    epsilon = eta/10,
B_c = c*eta,        A_s = s*epsilon,
f(t) = t^2*(1-t)^2,
P_(A,B)(t) = f(t) * [A+B*(2*t-1)].
```

For a counterclockwise unit boundary edge `v -> v+e` and outward normal
`n=(e_y,-e_x)`, replace it by

`v+t*e+P_(A_s,B_c)(t)*n`, for `0<=t<=1`.

Every port is nonflat, including the self-compatible state-zero ports. The
resulting unmarked tile `T` is a simple topological disc. Under the finite
complete-corona conventions of [atomic_grid_locking.md](atomic_grid_locking.md):

1. Every complete Euclidean corona aligns to the central cell grid and all
   its tiles have the central tile's handedness, even if the final patch has
   holes. This includes arbitrary attempted reflected placements.
2. When every prefix is a disc, the Euclidean coronas correspond exactly to
   the stated rotations-only marked-grid coronas. In particular their
   complete-disc corona depths `H_c` are equal.
3. When **all states are zero**, all shared-edge matching conditions are
   forced even in the last layer with holes. The correspondence then also
   holds for the convention `H_h` permitting holes only in that last layer.
4. With directed states present, a valid marked `H`-corona transfers. A
   complete-disc upper exclusion transfers, and `H_h(T)<=H_c(T)+1`. A same-
   layer wrong direction in the last layer can leave a small hole, so exact
   `H_h` equality is not claimed in this case.

The whole-plane counterpart in [atomic_grid_locking.md](atomic_grid_locking.md)
also makes plane tilings equivalent to marked-grid plane tilings with the
stated rotations-only convention. An upper exclusion must have complete
candidate coverage and a checked certificate. If any color has an imbalance of the two nonzero states, the
earlier additive-charge argument separately proves nontiling and a finite
upper bound for arbitrary Euclidean placements. A zero-charge color system
has no such automatic obstruction: its finiteness must be proved.

## Polynomial atomicity, including translations and reflections

Consider any two profiles with `B!=0` and `|A|<|B|`. If an isometry
`Qz+(u,v)` identifies nontrivial subarcs of their graphs, substitution into
the transformed curve equation gives a polynomial identity. Division by
`y-P_(A,B)(x)`, monic in `y`, shows that this irreducible graph equation
divides the transformed equation. Both have total degree five, so the two
equations differ by a nonzero scalar.

The leading homogeneous terms are nonzero multiples of `x^5` and
`(Q_11*x+Q_12*y)^5`. Therefore `Q_12=0`, and orthogonality gives
`Q=diag(a,b)` with `a,b` in `{+1,-1}`. Comparing the coefficient of `y`
reduces the identity to

`P_(A',B')(a*x+u) = b*P_(A,B)(x)+v`.

It remains to prove that this does not slide the endpoints. Put `z=2*x-1`.
The derivative factorization is

`P'_(A,B)(x) = x*(1-x)/2 * [B*(1-5*z^2)-4*A*z]`.

The quadratic `5*z^2+4*(A/B)*z-1` is negative at zero and positive at both
`-1` and `+1`, since `|A/B|<1`. Its two distinct roots lie in `(-1,0)` and
`(0,1)`. Thus the four critical points of `P` are all real, with unique
smallest and largest critical points **0 and 1**. The affine map `x->a*x+u`
must take the entire critical set to that of the other polynomial. Comparing
its extremes gives `u=(1-a)/2`. At either endpoint `P=0`, so `v=0`.
Finally, `f(1-x)=f(x)` and `2*(1-x)-1=-(2*x-1)` give exactly

`A'=b*A`, `B'=a*b*B`.

Conversely these transformations identify the whole arcs. In particular
every common nontrivial subarc has the same full endpoint pair. Two distinct
transformed curves have only finitely many intersections, by the same
nonzero polynomial substitution. A straight segment cannot contain a
nontrivial subarc. The critical-set argument, not only a leading-term
comparison, is what excludes a shifted copy of the same graph.

## Matching and handedness

At a paired edge the outward normals oppose, so `b=-1`; otherwise the two
interiors occupy the same local side and overlap. All our `B_c` are positive.
The identity `B'=a*b*B` therefore forces `a*b=+1`, hence `a=-1`. The relative
edge frames have positive determinant. Their determinants equal the
relative handedness of the tile placements, because both original
tangent/outward frames have determinant `-1`. The two tiles consequently
have the same handedness, the same color, and `A'=-A`.

Apply the filled-contact pairing cycle of
[atomic_grid_locking.md](atomic_grid_locking.md) at each contact of a new
corona with its predecessor. Both the grid and handedness propagate around
that cycle. Induction covers every tile, including those initially touching
only at vertices. Taking the central tile's placement as the reference
leaves precisely rotations and translations in the underlying marked model.

This distinction prevents a false conversion: an undirected self-color
table that independently permits reflections is **not** the model realized
here. For example, two state-zero edges of amplitude `B` meet under a
half-turn, but a reflected pairing has height difference `2*B*f(t)*(2*t-1)`
and overlaps on one half of the edge. A drawing of a colored patch with
mixed handedness cannot be used as a lower witness for this construction.

## Shared edges in the outermost layer

Grid alignment and retained cell centers exclude underlying cell overlaps.
For two cells on opposite sides of a shared chord use the first tile's
outward coordinate, with `z=2*t-1`. For equal handedness their graph-height
difference is

`D(t)=f(t)*[(A+A')+(B-B')*z]`.

For opposite handedness the corresponding difference is

`D(t)=f(t)*[(A+A')+(B+B')*z]`.

A positive value gives overlap of the two local interiors. Distinct colors
have `|B-B'|>=eta`, while `|A+A'|<=2*epsilon=eta/5`. At `t=1/4,3/4` the
distinct-color difference takes both signs. The opposite-handed difference
also takes both signs since `B+B'>=2*eta`. Each mismatch thus produces
overlap, without any appeal to hole-freeness.

For the same color and handedness, `D=(A+A')*f`. A positive sum overlaps; a
negative sum produces a closed Jordan lens between the two full graphs.
Its middle point is uncovered by both tiles. Every third base cell lies at
distance at least `1/4` from the chord midpoint for all three cell grids.
Every boundary moves at most `delta`, and the lens point is within `delta`
of the midpoint. Since `2*delta<1/4`, no third tile can cover that point.
The two lens arcs belong to the patch and enclose a bounded complementary
component. A disc patch forbids it. Therefore in a disc we must have
`A'=-A`, exactly the directed-state table.

If all `A` vanish, there is no same-color mismatch left to create a lens:
every shared edge in an arbitrary final patch matches. This proves the
stronger color-only `H_h` correspondence. With nonzero states, discarding a
last layer with holes gives the stated one-layer upper implication.

## Simple boundaries, construction transfer and exact geometry

Since `B_max=1/100`, `epsilon<=1/1000` and `|2*t-1|<=1`,

```
|P(t)| <= (B_max+epsilon)*f(t),
delta <= (B_max+epsilon)/16 <= 11/16000 < 1/160,
|P(t)|/t, |P(t)|/(1-t) <= (B_max+epsilon)*4/27.
```

These endpoint cones separate the incident rays of all three unit grids.
The displacement separates nonincident grid edges. Scaling from zero
therefore gives a simple tile and preserves any consistently paired finite
edge network. For same-color opposite-state neighbors of equal handedness,
`P_(-A,B)(1-t)=-P_(A,B)(t)`; reversing the outward normal gives exactly the
same shared arc. The network isotopy transfers all tiles and all prefixes,
preserving strict containment, contacts and topology. The converse uses the
alignment and shared-edge proofs above.

The odd part has zero integral, so

`area(T)=area(S)+(epsilon/30)*sum(s)`.

For a base diameter bound `D0`,

`diameter(T)<=D0+(B_max+epsilon)/8`.

For a single color, nonzero states pair `+` to `-` and zero states carry no
charge. The complete-port pairing therefore supplies the earlier growth
recurrence for an imbalanced color even without relying on alignment or
on a square/triangle grid convention. This is a reuse of the known additive
obstruction, not a new imbalance theorem.

## Exact checks and scope

Run `python3 heesch_weighted_matching_obstruction/quintic_profiles.py` and
compare the output with [quintic_expected.json](quintic_expected.json).
The standard-library checker verifies polynomial identities on the two
linear coefficient bases, critical-quadratic endpoint signs, all matching
and mismatch tests of a specified five-color palette, and an independent
Green-formula area calculation for a square fixture. It does not formalize
the local geometry, root-location proof or network isotopy. No solver or
floating-point computation is part of this profile check.

No seven-corona construction is supplied. The useful output is an exact
broader realization and its motion/topology boundary;
an actual record claim still needs admissible lower coronas and a sound
finite upper obstruction for that same model.
