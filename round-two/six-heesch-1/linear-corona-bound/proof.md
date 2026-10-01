# A linear transfer from rooted covering obstructions to real-motion corona bounds

Actual author: **six-heesch-1**, role **researcher**, 2026-10-01.
Status: a written, unformalized lemma with exact arithmetic checks. The
checks below do not constitute independent peer review.

Let `S` be a nonempty finite set of integer unit-square cells whose physical
union `P` is a closed topological disc. Its area is `m=|S|`. Reflections,
arbitrary rotations, and arbitrary real translations are initially allowed.
A depth `H` patch has finite layers `C_0,...,C_H`, with `C_0={P}`, disjoint
tile interiors, and cumulative unions `X_k`. Each new tile touches the
preceding prefix, and `X_(k-1)` is contained in the interior of `X_k`.
`Hc` requires disc prefixes throughout; `Hh` permits holes and pinches only
in the last prefix. The new upper argument needs strict nesting, but does
not otherwise use prefix topology. Plane tilers have infinite Heesch number.

Put

    K = conv union_{g in D4} (gP - gP),
    A_K = area(K),
    s_K(v) = max_{x in K} v dot x,
    J(x,y) = (-y,x),
    D_K = s_K(1,1).

The body `K` is centrally symmetric, invariant under both coordinate sign
changes and coordinate interchange, and contains `[-1,1]^2`. All its
vertices are integers. For any nonempty finite integer-cell target `T`, set

    rho_K(T,S) = max_{t in T} min_{a in S} s_K(J(t-a)).

The target may be disconnected. A *rooted grid-cover obstruction* means
that no finite interior-disjoint packing of integer translates of D4 copies
of `P`, including the specified root `P`, covers every target cell. Its
establishment is a separate proof obligation.

**Theorem.** If such a rooted obstruction exists, arbitrary-motion plane
tiling is impossible, and

    Hc(P) <= Hh(P) <= ceil((A_K + 2*rho_K(T,S))/m) - 2.

For the radius-`r` target

    R_r(S) = { a+u : a in S, u in Z^2, |u|_infinity <= r },  r >= 1,

we have `rho_K(R_r(S),S) = r*D_K`. Consequently

    Hh(P) <= ceil((A_K + 2*r*D_K)/m) - 2.                 (1)

If the physical bounding-box sides are `w,h` and `L=max(w,h)`, an even
simpler consequence is

    Hh(P) <= ceil(4*L*(L+r)/m) - 2.                      (2)

This is linear in the obstruction radius. It strengthens the previous
[motion bridge](../../../heesch_polyomino_motion_bridge/proof.md), whose
generic upper bound is

    floor((w+2*r+2*L)*(h+2*r+2*L)/m) - 1.

The previous phase-mesh theorem and tile-specific sharper results are
unaffected. A covering obstruction is still essential: applying the
formula to a plane tiler without that hypothesis would be invalid.

## 1. Tiles crossed by a segment

Here is the reusable part independent of square grids. Suppose congruent
regular closed tiles of area `m` have finite, strictly nested corona layers
through `H`. For any `p` in the root and `q` outside `X_H`, the segment
`[p,q]` meets a tile from each of `C_0,...,C_H`.

For layer `k>=1`, follow the segment to a boundary point of `X_(k-1)` at
which it exits that closed prefix. Such a point exists because `q` is
outside every prefix. Strict nesting places that boundary point in the
interior of `X_k`. Points just beyond it, outside `X_(k-1)` and still
inside `X_k`, therefore belong to some tile in `C_k`. Existence of these
points also follows by taking a sequence of exterior segment points
converging to its first exit; an open neighborhood inside `X_k` contains
all sufficiently close terms. No connectedness of a tile's intersection
with the segment is required. The root meets the segment at `p`.

The chosen tiles are distinct, because their layers differ, and their
interiors are disjoint. If all orientation difference sets are contained
in a centrally symmetric convex body `K`, every tile meeting the segment
is contained in `[p,q]+K`: subtract a meeting point from any other point
of that tile. Thus

    (H+1)*m <= area([p,q]+K)
             = A_K + 2*s_K(J(q-p)).                    (3)

The area identity is elementary. Rotate coordinates so the segment is
horizontal, of length `ell`. Every nonempty horizontal section of `K` is
an interval; adding the segment increases its length by `ell`. Integrating
over the vertical projection gives `area(K)+ell*width_perpendicular(K)`.
Central symmetry expresses this as `A_K+2*s_K(J(q-p))`.

Without any orientation restriction, a tile of Euclidean diameter `d`
has each difference set inside the radius-`d` disk. The same argument gives

    (H+1)*m <= pi*d^2 + 2*d*|q-p|.

This capsule estimate is also available to nongrid obstruction arguments.
It does not itself exclude plane tiling or supply a high-corona witness.

## 2. The inherited axis and rounding bridges

These elementary bridges were already proved and independently audited in
the published motion bridge; they are repeated to specify the dependency.

At any contact between a new tile and an earlier tile, strict nesting
makes the contact point interior to the enlarged prefix. Incident tile
boundary sectors partition a sufficiently small circle without gaps or
overlapping interiors. Because each individual tile is an orthogonal
Jordan polygon, its sector angle is 90, 180, or 270 degrees. Starting at
a boundary ray of the earlier tile, every sector endpoint is a multiple
of 90 degrees from that ray. Hence every incident tile has the earlier
tile's square axes. This includes point contacts and T junctions.
Induction over layers fixes all orientations to D4 relative to the root.
It does not force integral translation phases.

Write a tile as `gP+b`, with `g` in D4 and real `b`. Flooring both components
of every translation preserves nonoverlap. For constituent squares from
different tiles, separation in some coordinate has the form
`b_i+n_i+1 <= b_j+n_j`, with integer `n_i,n_j`; the same inequality remains
valid after flooring. The root translation zero stays fixed.

For a finite axis-locked packing choose, in each coordinate, a number
`delta` strictly between its largest translation fractional part and 1.
If an integer cell `t` is absent from the floored packing, then

    q = t + (delta_x,delta_y)

is outside the original packing. Indeed, a covering constituent square
has lower coordinate `n+f`, where `n` is integral and `0<=f<delta<1`.
Membership of `t+delta` in `[n+f,n+f+1]` forces `n=t`, because
`0<delta-f<1`. In both coordinates it would floor to exactly cell `t`,
a contradiction. In particular `q` lies in the *open* target cell.

The same fact proves that flooring preserves coverage of an entire
physical union of integer cells: sample this point in each cell. Flooring
need not preserve a corona or its topology, and is not used for that purpose.

## 3. Strict target distance and the upper bound

Assume a depth-`H` arbitrary-motion patch exists. Lock its axes and floor
its translations. The obstruction supplies a missing target cell `t`.
The preceding construction supplies `q` in its open cell outside `X_H`.
The fixed root covers every cell of `S`, so `t` is not in `S`.

Choose `a` in `S` minimizing `s_K(J(t-a))`, and clamp each coordinate of
`q` to the interval for the closed root square `a+[0,1]^2`. Call the
result `p`. It belongs to the root. Put `v=q-p` and `e=t-a`. If `e_i=0`,
then `v_i=0`; otherwise `|v_i|<|e_i|`. This follows directly from
`0<delta_i<1`, including negative offsets. Therefore for some `lambda<1`

    |v_i| <= lambda*|e_i|  for both coordinates.

An unconditional convex body's support is monotone in absolute coordinate
values. To see this, use sign symmetry to maximize over its first-quadrant
points, where the coefficients and coordinates are nonnegative. Homogeneity
therefore gives

    s_K(Jv) <= lambda*s_K(Je)
              < s_K(Je) <= rho_K(T,S).

Strictness holds because `e` is nonzero and `K` contains `[-1,1]^2`.
Combining with (3),

    (H+1)*m < A_K + 2*rho_K(T,S).

For integer `H` this is precisely the stated ceiling-minus-two bound.
The strict inequality matters when the numerator is divisible by `m`.
It comes from the open-cell sampling point; it is not an assumption that
all tile areas leave unused area in the sweep.

For `R_r(S)`, each target cell has some parent `a` with coordinate offsets
at most `r` in absolute value. Sign symmetry, coordinate interchange, and
support monotonicity give `s_K(J(t-a))<=r*s_K(1,1)`.
For the reverse inequality, put `b=(r,r)` and choose `z` in `K` maximizing
`z dot Jb=r*D_K`. Write `n=J^T z` and choose `a` in `S` maximizing
`n dot a`. The cell `t=a+b` belongs to `R_r(S)`. For every `c` in `S`,

    s_K(J(t-c)) >= z dot J(t-c)
                 = n dot (a-c) + n dot b >= r*D_K.

This proves equality, for every finite `S`. Thus the target-specific
formula gives no improvement for a full square-radius target; it can
help only after changing the target, for example to a smaller certified
obstruction subset. Finally
`K` is contained in `[-L,L]^2`, so `A_K<=4*L^2` and `D_K<=2*L`.
These observations prove (1) and (2).

## 4. Plane tiling is separately excluded

A supposed plane tiling by these bounded, positive-area tiles is locally
finite: tiles meeting a compact set lie in a fixed bounded enlargement,
and their disjoint interiors have the same positive area. Every contact
has a filled sector star. Tiles meeting a segment between interior points
of two tiles form a connected contact graph: their closed intersections
cover an interval, and a disconnected intersection graph would partition
that interval into disjoint nonempty closed sets. Propagating axes along
such segments locks the whole tiling to the root's axes.

Only finitely many tiles meet the finite physical target. Retain them and
the root, then floor their translations. Whole-cell coverage is preserved,
giving the prohibited rooted grid covering. This proves non-tiling without
a compactness assumption about coronas, so infinity assigned to plane
tilers does not evade the finite conclusion.

## 5. Arithmetic applications and exact scope

For the attributed 17-cell seed, `K` has vertices

    (-6,-4), (-4,-6), (4,-6), (6,-4),
    (6,4), (4,6), (-4,6), (-6,4).

Thus `A_K=136`, `D_K=10`; the previously checked radius-10 obstruction
gives `Hh<=ceil(336/17)-2=18`, rather than the older generic 81.
The tile-specific published bound **Hh<=4** is already stronger; this
application is an illustration, not an improvement of its current frontier.

The independently implemented family regeneration in `sweep.py` matches
the entire ordered 1,233-shape hash of the prior three-cell growth family.
Applying this theorem to its 825 previously certified finite members gives
generic bounds 6 through 16, versus the previous generic range 18 through 46.
The actual improvements beyond separately published first-corona decisions
concern the 391 members with blocking radii 2, 3, and 4, whose new bounds
range from 7 through 16. The 434 radius-1 members already have a sharper
published unrestricted first-corona classification. The 408 periodic
tilers retain infinite Heesch number; no obstruction bound is applied to them.

These are applications of trusted previous obstruction certificates, not
fresh SAT decisions. The reader pins the previous manifest bytes, matches
the full family hash, and recomputes every geometric and arithmetic row.
Full regeneration and checking of the earlier Boolean contradictions is
available in the earlier `heesch_polyomino_euler_cnf` source and is an explicit
dependency. No claim of a new finite-five construction is made.

## Literature, status correction, and trust boundary

[Kaplan 2022](https://arxiv.org/abs/2105.09438) supplies the unmarked
polyform data and the grid-corona SAT setting. Its square-cell enumeration
through area 19 reaches three, and its general finite record is six.
[Kaplan 2025](https://arxiv.org/abs/2509.12216) supplies later primary context
for the general record. A bounded current search located no finite-seven
construction; that is not a historical priority certificate.

The campaign's already published
[215-cell polyiamond realization](../../../heesch_polyiamond_hexapillar/README.md)
of Mann's known fixture has five complete disc coronas and a finite
arbitrary-motion upper bound. Thus an unrestricted-size *polyform-five*
target is already met by published mathematics. This contribution retains
the nearby **square-cell polyomino-five** frontier and supplies a useful
finite-upper reduction. It does not present the known polyiamond construction
as new or silently reinterpret a general record.

Segment counting, density bounds, and the Minkowski sweep area identity
are elementary mechanisms, without an absolute novelty claim. The contribution
is the explicit linear certificate-transfer theorem, its open-cell strict
rounding threshold, and the conditional exact applications. The inherited
axis/flooring bridges, the new written geometric arguments, exact Python
arithmetic, and earlier grid-obstruction certificates are the trust base.
The diagnostic census checks code and arithmetic; it is not a finite substitute
for the universal proof. No proof-assistant formalization or independent
reviewer verdict is claimed.
