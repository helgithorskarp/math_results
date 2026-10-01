# A radial capacity criterion for short spherical cycles

Author: **six-tammes-1**, role: **researcher**, 2026-10-01.
Status: complete author-checked ordinary proof. Independent review is pending.
The exact arithmetic companion checks the constants, not the geometric proof.

## Statement

A spherical `c`-code is a set of distinct unit vectors whose pairwise inner
products are at most `c`. Consider distinct vertices `v_0,...,v_(m-1)`, `m>=3`,
joined cyclically by minor geodesic arcs. Suppose this is a simple closed curve,
and write `P` for its smaller closed spherical region. Let `H` denote the
spherical convex hull of the boundary vertices in the containing hemisphere
supplied below; in particular `P` is contained in `H`. Assume

\[
 \frac12\le c\le\frac35,\qquad
 v_i\cdot v_{i+1}\ge c-\frac1{40}.
\]

Suppose a unit vector `q` is in the interior of `P` and

\[
 \frac16\le q\cdot v_i\le c\quad\hbox{for every }i.                 \tag{1}
\]

Then the following strict covering margin holds:

\[
 x\in H,\quad q\cdot x\le\frac35
 \quad\Longrightarrow\quad
 \max_i x\cdot v_i>\frac35+\frac1{12500}=\frac{7501}{12500}.        \tag{2}
\]

In particular, if the boundary vertices and `q` belong to a spherical `c`-code,
then **no second code point belongs to `H`**, and hence none belongs to `P`.
For prescribed cycles in such a
code, simplicity is automatic at the stated edge tolerance; Section 3 proves
this rather than adding a contact-graph assumption.

This is independent of the number of sides, coordinate templates, convexity,
equal edge lengths, facial status, vertex degrees and irreducibility. Condition
(1) concerns an actual interior point and is essential to this result. The
covering proof itself needs only the cycle, edge and radial hypotheses, rather
than packing inequalities on nonadjacent boundary pairs.

For a cycle containing at least two additional interior code points, its useful
contrapositive is

\[
 \text{for each such point }q,\quad \min_i q\cdot v_i<\frac16.      \tag{3}
\]

Thus a putative two-insertion short hexagon in the fifteen-point problem must
have a boundary vertex farther than `arccos(1/6)` from each insertion. This
does not show that every short hexagon satisfies (1), and does not improve the
global Tammes bound.

## 1. The region and its tangent directions

Put `a=1/6` and `s_i=q dot v_i`. All vertices lie in the open hemisphere
`H_q={v:q dot v>0}`. A minor arc between two of them is the normalization of
a positive combination of its endpoints, so the entire boundary is in `H_q`.
Gnomonic projection centered at `q`,

\[
 G(v)=\frac{v}{q\cdot v}-q\ \in q^\perp,
\]

sends the boundary to a simple planar polygon. Its bounded closed region lies
in the convex hull of its projected vertices, including when the polygon is
concave. The inverse of that bounded region is compactly contained in `H_q`,
so its area is strictly below `2*pi`; it is precisely `P`. In particular the
chosen interior point `q` projects to the origin inside the planar region.

Every `x in H`, and hence every `x in P`, is the normalization of a nonzero nonnegative combination of
the boundary vectors. Rescale the coefficients to sum to one and write
`x=y/||y||`, `y=sum_i lambda_i v_i`, `lambda_i>=0`, `sum_i lambda_i=1`.
Then `q dot y>=a` and `||y||<=1`, hence

\[
 t:=q\cdot x\ge a.                                               \tag{4}
\]

For each vertex define the unit tangent direction

\[
 u_i=\frac{v_i-s_iq}{\sqrt{1-s_i^2}}.
\]

It is defined because `a<=s_i<=c<=3/5<1`. Adjacent tangent directions obey

\[
 u_i\cdot u_{i+1}
 =\frac{v_i\cdot v_{i+1}-s_i s_{i+1}}
        {\sqrt{(1-s_i^2)(1-s_{i+1}^2)}}
 \ge \frac{c-c^2-1/40}{1-a^2}
 \ge \frac{387}{1750}=:B>0.                                    \tag{5}
\]

Here the numerator is positive, the denominator is at most `1-a^2=35/36`,
and the concave polynomial `c-c^2` has minimum `6/25` on `[1/2,3/5]`.
Thus every principal angular arc between adjacent `u_i` has length at most
`arccos(B)<pi/2`.

Let `e` be any unit direction in `q^perp`. The planar ray from the origin in
direction `e` meets the polygon boundary, since the origin is interior and
the polygon is bounded. If it meets a vertex, that vertex has direction `e`.
Otherwise it meets a segment between `G(v_i)` and `G(v_(i+1))`. The direction
of this segment point is a positive combination of `u_i,u_(i+1)` and lies on
their principal angular arc. At least one endpoint is at angular distance
at most half that arc length from `e`. Consequently

\[
 \max_i e\cdot u_i\ge\sqrt{\frac{1+B}{2}}
   =\sqrt{\frac{2137}{3500}}=:\rho.                              \tag{6}
\]

This ray argument does not assume that all vertex directions occur in
increasing angular order, that the polygon is star shaped about `q`, or that
its fan triangles partition the region. Boundary segments may have zero
angular increment; (6) still applies.

## 2. The scalar lower envelope

For a point in (2), (4) gives `a<=t<=3/5`. Write
`x=t q+sqrt(1-t^2)e` and use a vertex chosen by (6). Its inner product with
`x` is at least

\[
 t s_i+\rho\sqrt{1-t^2}\sqrt{1-s_i^2}
 \ge a t+\beta\sqrt{1-t^2},\qquad
 \beta=\frac45\rho,\quad\beta^2=\frac{8548}{21875}.              \tag{7}
\]

The rational number `beta_0=6251/10000` is a strict lower bound for `beta`,
because

\[
 \beta^2-\beta_0^2=\frac{10993}{700000000}>0.                    \tag{8}
\]

The function `f(t)=t/6+beta_0 sqrt(1-t^2)` is concave on `[1/6,3/5]`,
so its minimum is at an endpoint. At the upper endpoint,

\[
 f(3/5)=\frac1{10}+\frac45\frac{6251}{10000}
       =\frac35+\frac1{12500}.                                 \tag{9}
\]

At the lower endpoint, use `sqrt(35)>11/2` to get

\[
 f(1/6)>\frac1{36}+\frac{11}{12}\frac{6251}{10000}
       =\frac35+\frac1{12500}+\frac{1271}{1800000}.              \tag{10}
\]

Equations (7)--(10) prove (2), with strictness supplied by (8) and
`sqrt(1-t^2)>0`. A second distinct code point `x in H` would satisfy
`q dot x<=c<=3/5` and every `x dot v_i<=c<=3/5`, contradicting (2).
This also proves (3).

## 3. Why prescribed short code cycles are simple

The following standard positive-cone argument is included for completeness;
it also appears in our earlier short-polygon source. For a spherical `c`-code
with `0<c<1`, draw all minor arcs whose endpoint dot is at least `k`, where
`k>2c-1`. If two edges with four distinct endpoints intersect, their common
direction has representations

\[
 W=\alpha A+\beta B=\gamma C+\delta D,
 \quad \alpha,\beta,\gamma,\delta\ge0,
 \quad \alpha+\beta>0,\quad\gamma+\delta>0.
\]

Writing `r=alpha+beta`, `s=gamma+delta`, the same-edge norm estimates and
the cross-pair packing estimates give

\[
 \|W\|^2\ge\frac{1+k}{2}r^2,\qquad
 \|W\|^2\ge\frac{1+k}{2}s^2,\qquad
 \|W\|^2\le c r s.
\]

Multiplying the first two inequalities and comparing with the square of the
third gives `(1+k)/2<=c`, contradicting `k>2c-1`. This excludes crossings
and shared segments, including a meeting at one endpoint of the other edge.
An edge through a third code vertex has length at least `2 arccos(c)`, but
the edge length is at most `arccos(k)<2 arccos(c)` since
`k>2c-1>2c^2-1=cos(2 arccos(c))`. Adjacent arcs cannot overlap away from
their common endpoint: such an overlap would put one other endpoint on the
other arc. Therefore every cycle on distinct selected vertices is simple.

For the present constants, `k=c-1/40` has

\[
 k-(2c-1)=1-c-1/40\ge3/8>0.
\]

Once an interior `q` with (1) is specified, Section 1 also supplies the
hemisphere and the unambiguous smaller region. No facial or irreducibility
restriction has been hidden in the use of a simple polygon.

## 4. A geometric center criterion with no inserted center point

There is a second, independent interface for the same geometry. Keep the cycle
and edge hypotheses, but do not assume the existence of an inserted code point
`q`. Instead, suppose a unit geometric witness `h` is interior to `P` and

\[
 \frac25\le h\cdot v_i\le\frac35\quad\hbox{for every }i.          \tag{11}
\]

Then every admissible unit insertion in the **entire spherical convex hull**
`H` satisfies `h dot x>9/10`. Any two such insertions have dot product
strictly above `31/50>3/5`, so their packing capacity is at most one.
The witness need not be a member of the code and no packing inequality with
it is assumed. The conclusion covers concave cycles without a coordinate
template or an initial proximity assumption on the inserted points.

To prove this, repeat the hemisphere, positive-cone and ray arguments of
Section 1 with `a=2/5`, upper radial bound `b=3/5` and center `h`.
The tangent edge cosine lower bound is now

\[
 B_h=\frac{1/2-1/40-(3/5)^2}{1-(2/5)^2}
     =\frac{23}{168}>0,
 \quad \rho_h^2=\frac{191}{336},
 \quad \beta_h^2=(1-b^2)\rho_h^2=\frac{191}{525}.
\]

The rational lower bound `beta_h>601/1000` is certified by

\[
 \frac{191}{525}-\left(\frac{601}{1000}\right)^2
 =\frac{54779}{21000000}>0.
\]

For `x in H` put `t=h dot x>=2/5`. If `t<=9/10`, tangent coverage gives

\[
 F(x)\ge\frac25 t+\beta_h\sqrt{1-t^2}
 >\frac25 t+\frac{601}{1000}\sqrt{1-t^2}.
\]

The final function is concave on `[2/5,9/10]`. Its lower endpoint is strictly
above `4/25+(601/1000)(4/5)=801/1250`, using `sqrt(21)>4`. Its upper
endpoint is strictly above `9/25+(601/1000)(2/5)=1501/2500`, using
`sqrt(19)>4`. Therefore

\[
 x\in H,\quad h\cdot x\le9/10
 \quad\Longrightarrow\quad F(x)>1501/2500=3/5+1/2500.             \tag{12}
\]

An admissible insertion has `F(x)<=c<=3/5`, so `h dot x>9/10`.
For two such points, decomposition along `h` yields

\[
 x\cdot y\ge (h\cdot x)(h\cdot y)
 -\sqrt{1-(h\cdot x)^2}\sqrt{1-(h\cdot y)^2}
 >2(9/10)^2-1=31/50.
\]

This proves the capacity claim. The lower radial witness requirement (11)
is a sufficient shape condition, not proved to hold for arbitrary short
hexagons. For example the regular contact hexagon satisfies (11) with its
north axis throughout `29/50<=c<=3/5`, since its height is `sqrt(2c-1)`.
This gives an infinite family of examples of the interface; the exact regular
classification in [HEXAGON.md](HEXAGON.md) reaches a wider parameter range.

## Scope and trust boundary

All statements are invariant under a common orthogonal transformation, cyclic
relabeling and reversal. Closed endpoint and edge inequalities are allowed;
the exclusion margins remain strict. Interiority concerns `q` in the first
criterion or the geometric witness `h` in the second. Both covering statements
hold on the whole spherical convex hull for their stated projection ranges.

The proof uses the planar polygonal Jordan theorem, gnomonic projection,
positive cones, the spherical dot-product formula and elementary concavity.
These steps are written mathematics and are not formalized. `check.py` checks
the exact rational margins, general polynomial identities in the companion
hexagon calculation, and its explicit eight-point packing. No floating-point
search, external coordinates, enumeration claim or solver is a proof input.

The regular-hexagon calculation in [HEXAGON.md](HEXAGON.md) explains why capacity
one cannot be assumed throughout the wider strip merely from contact edges.
Its two-insertion examples lie below `14/25` and do not settle the unrestricted
hexagon question in the fifteen-point improvement interval. The next missing
step is to prove a radial condition such as (1) in the relevant configurations,
or to exclude the two-insertion cases satisfying (3).
