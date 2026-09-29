# Exact quartic realization of complementary marked polyforms

Author: **six-heesch-3**, role: researcher.

This is a geometric bridge for the charge certificates in [README.md](README.md).
It does not assert that a seven-corona marked polyform has been found. The
general use of bumps and nicks to realize complementary matching conditions
is prior art; the purpose here is an explicit algebraic profile and a proof
that arbitrary partial contacts do not evade its charge obstruction.

## Statement

Let `S` be a simple polyomino, polyhex, or polyiamond, viewed as a topological
disk with boundary subdivided into unit grid edges. Some edges are marked
`+(j)` or `-(j)` for finitely many colors `j`; the rest are flat. In the
marked grid model a nonflat edge may meet only the opposite sign of its own
color, and flat edges meet flat edges. Both rotations and reflections are
allowed.

Choose distinct positive rational numbers `lambda_j < 1/10`, and set

`f(t) = t^2*(1-t)^2`, for `0 <= t <= 1`.

For a boundary edge from `v` to `v+e` directed counterclockwise, where `e` is
a unit vector, let `n=(e_y,-e_x)` be its outward normal. Replace an edge of
sign `sigma` and color `j` by the parametrized arc

`v + t*e + sigma*lambda_j*f(t)*n`.

Leave flat edges straight. The resulting boundary is simple and defines an
unmarked topological disk `T`. The following properties hold.

1. Every nonflat boundary arc of a tile strictly inside an admissible finite
   patch is paired in full with exactly one opposite-sign arc of the same
   color on another tile. This holds for arbitrary Euclidean placements,
   including reflections; lattice alignment is not assumed.
2. Every admissible complete corona patch in the marked grid model transfers
   to a patch of `T` with the same tiles and layers. Its strict containment and
   hole-free properties are preserved.
3. If any color has unequal positive and negative edge counts, `T` has a
   finite Heesch number with the explicit upper certificates of the README.
   If the original marked model has an `H`-corona patch, then this construction
   gives a rigorously finite unmarked shape with Heesch number at least `H`.

No assertion about equality of the two Heesch numbers is made. Off-grid
patches of `T` might exist. Property 1 still excludes arbitrarily deep complete
coronas when a color is imbalanced.

## The polynomial contact lemma

Consider the reference arcs `y = sigma*lambda*f(x)`, `0 <= x <= 1`.
Suppose a Euclidean isometry takes a nontrivial subarc of one such arc onto a
subarc of another, of parameters `tau,mu`. Then `mu=lambda`; the isometry
maps the entire arcs onto each other and maps their endpoint pairs onto each
other.

Here is an elementary algebraic proof. Write the isometry as `Qz+(u,v)`, and
let

`F(x,y)=y-sigma*lambda*f(x)`.

Substitute `y=sigma*lambda*f(x)` into the equation of the transformed second
curve. The resulting polynomial vanishes at infinitely many values of `x`,
so it vanishes identically. Polynomial division by the polynomial `F`, which
is monic in `y`, shows that `F` divides the transformed curve equation. Both
equations have total degree four, so the transformed equation equals `c*F`
for a nonzero constant `c`.

Its homogeneous term of degree four is a nonzero multiple of
`(Q_11*x+Q_12*y)^4`. The homogeneous term of `F` is a multiple of `x^4`.
Thus `Q_12=0`. Orthogonality now gives `Q=diag(a,b)` with `a,b` in `{+1,-1}`.
Comparing the coefficient of `y` gives `c=b`. Comparing the fourth-degree
coefficient gives `tau*mu=b*sigma*lambda`, hence `mu=lambda` and
`tau=b*sigma`. Comparing the cubic coefficients of `f(a*x+u)` and `f(x)`
gives `u=(1-a)/2`. Since `f(1-x)=f(x)`, comparison of the constant terms
then gives `v=0`. These transformations all map the full parameter interval
onto itself.

A straight segment cannot share a nontrivial arc with this quartic: its line
equation substituted into the quartic graph would otherwise vanish
identically. The same reasoning shows that two noncoincident transformed
quartics have only finitely many intersections. One can see this directly by
substituting the graph parametrization into the other curve equation; it is
a nonzero univariate polynomial.

## Why partial contacts and reflections are covered

The boundary of a tile contained in the interior of a patch is covered by
the boundaries of the other tiles. Indeed, an open part of its boundary
cannot lie in the interior of a different tile without overlapping the first
tile's interior. There are finitely many tiles and finitely many boundary
arcs. The preceding contact lemma implies that a given quartic port cannot
be covered by only finite intersections: some other port must coincide with
it in full. The matching amplitudes therefore have the same color, and the
base chord endpoints coincide as well.

Along an interior point of the common arc, the two tile interiors must be on
opposite local sides. Use the transported reference frames of the two unit
edges, with the second coordinate pointing outward in each frame. The contact
lemma's normal sign must then be `b=-1`, forcing `tau=-sigma`. This argument
is independent of the determinant of either tile's placement isometry, and
so includes reflected copies. A third tile sharing the same whole port
would occupy the same local side as one of the first two and would overlap
it. Pairing is consequently one-to-one.

Only nonflat arcs are ports in this argument. Straight boundary edges are
uncharged and need not be atomic: they may slide or split among contacts.
This distinction is what permits the charge proof to avoid a separate
grid-locking theorem. Simply decorating every straight edge symbolically
would not justify the same conclusion for an unmarked shape.

## Simple boundaries and transfer of the corona construction

The profile satisfies

`0 <= f(t) <= 1/16`,

`f(t)/t <= 4/27`, `f(t)/(1-t) <= 4/27` for interior `t`.

The latter maxima follow by differentiating `t*(1-t)^2` and its reversal.
The displacement of an arc is at most `lambda_j/16 < 1/160`. Viewed from
either endpoint, the arc lies in a cone about the original grid edge with
half-angle less than `arctan(2/135) < pi/6`.

In the square grid distinct edge rays at a vertex have separation at least
`pi/2`, and nonincident unit grid edges have distance at least one. In the
triangular grid the respective bounds are `pi/3` and `sqrt(3)/2`; the regular
hexagon edge grid is a subset of a unit triangular grid. For the distance
claim, a nearest pair on nonparallel disjoint segments includes an endpoint.
A triangular-grid vertex is at distance at least `sqrt(3)/2` from a
nonincident unit edge (or at least one from its nearest endpoint). Distinct
parallel grid lines have separation at least `sqrt(3)/2`; collinear
nonincident edges are at distance at least one. The square-grid argument is
the same with integer coordinates.

The endpoint cones therefore separate arcs on distinct incident grid rays.
The displacement bound separates arcs on nonincident grid edges. Scaling
all amplitudes continuously from zero to their selected values never
introduces a crossing. Thus the modified boundary is a Jordan curve.

For a finite valid marked patch, opposite-sign matched edges define the same
geometric arc: reverse the parameter by `t -> 1-t`, reverse the outward
normal, and use `f(1-t)=f(t)`. This remains true for reflected tiles. Other
grid edges in the patch can remain straight. The resulting finite embedded
edge network has exactly the same incidence and cyclic order as before.
It is an isotopy of the original finite network; it extends over its faces
and the exterior to an ambient homeomorphism. Equivalently, each disk face
can be mapped to its new Jordan face with the prescribed boundary map, and
these maps agree on shared edges. Consequently distinct tile interiors
remain disjoint, all patch holes are preserved, and each old nested patch
is contained in the interior of the next one. Contacts between successive
coronas are preserved, so the complete corona construction transfers.

## Exact area and conservative diameter bounds

The area is exactly

`area(T) = area(S) + (1/30)*sum(sigma*lambda_j)`

because `integral_0^1 f(t) dt = 1/30`. If `D0` is an upper bound on the
diameter of the convex hull of the original boundary vertices and
`lambda_max` is the largest amplitude, then

`diameter(T) <= D0 + lambda_max/8`.

To justify this for the whole filled tile, the modified boundary lies within
distance `lambda_max/16` of that original convex hull. The convex hull of
the modified boundary, which contains the tile, lies in the same parallel
body. Distances can thus increase by at most twice this displacement. These
bounds can be substituted in the rational depth certificates; a rational
upper bound on `D0` is enough.

## A compact realized fixture

[quartic_boundary.py](quartic_boundary.py) specifies an exact unmarked curved
tetromino obtained from the `4 by 1` rectangle. Its ten unit boundary edges
carry three `a+`, two `a-`, two `b+`, and three `b-` profiles, with amplitudes
`lambda_a=1/100`, `lambda_b=1/200`.

There are five bumps and five nicks in total, but color `a` alone has a `3:2`
imbalance, as does color `b` after reversing its signs. Its area is exactly
`24001/6000`. Its squared diameter is bounded above by `(4001/800)^2`, using
`sqrt(17)<5` for the base rectangle. At depth 22 the recurrence requires
12,137 tiles, while the packing bound allows at most 10,395. Thus its Heesch
number is at most 21. The compact closed certificate independently excludes
depth 32. No positive lower bound on its Heesch number is claimed.

```sh
python3 heesch_weighted_matching_obstruction/quartic_boundary.py
```

This returns the explicit parametrized boundary, its exact geometry bounds,
and the matching/depth certificate. It checks the area both by the profile
integral and by direct polynomial integration of Green's formula. The
geometric contact and topology proofs above remain the trust boundary;
the program does not independently formalize them.
