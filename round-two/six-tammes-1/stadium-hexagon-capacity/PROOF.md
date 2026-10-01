# Short hexagons have insertion capacity at most one

Actual author: **six-tammes-1**, role **researcher**, 2026-10-01.
Status: complete author-checked geometric proof with rigorous endpoint
enclosures in two arithmetic representations. Independent review and
formalization are pending. No global optimality or numerical Tammes bound
is claimed.

## 1. Statement

Let `X` be any finite spherical `c`-code: distinct unit vectors with all pair
inner products at most `c`. Assume

\[
 14/25\le c\le3/5.
\]

Take six distinct members `v_0,...,v_5` in cyclic order with

\[
 v_i\cdot v_{i+1}\ge c-1/100\quad(i\bmod6).                     \tag{1}
\]

Their minor-geodesic cycle is automatically simple and hemispherical.
Its smaller closed region `P` contains **at most one member of `X` other
than its six boundary vertices**.

The theorem has no coordinate-template, radial, convexity, contact-equality,
facial, degree, irreducibility or initial insertion-proximity hypothesis.
It applies to a concave cycle and to code points with contacts inside that
cycle. It concerns `P`; the entire convex hull of a concave cycle need not
have the same capacity.

For fifteen points this is a necessary global geometric exclusion: in the
actual embedded graph joining pairs with dot at least `c-1/100`, no six-cycle
can have two or more other code vertices on **each** spherical side. One
side of such a cycle contains at most one of the nine remaining vertices.
This is not an occurrence theorem for a prescribed incumbent contact pattern,
and supplies no improved global numerical bound.

The code parameter range includes every strict improvement of the known
fifteen-point incumbent. The solved `N=14` problem bounds such a code parameter
below by a value greater than `14/25`, and comparison with the incumbent
bounds it above by a value less than `3/5`. This application domain is prior
context; the theorem is proved directly on its stated interval.

## 2. Simplicity and the smaller region

Put `e=1/100`, `k=c-e`, `L=arccos(k)` and `d=arccos(c)`. Then
`k>=11/20>1/2`, so `3L<pi`. Edges in a `c`-code with dot at least
`k>2c-1` cannot cross. At an intersection of edges with four distinct
endpoints, a common vector has nonnegative representations
`W=alpha A+beta B=gamma C+delta D` with coefficient sums `a,b>0`.
Same-edge norm bounds and cross-pair code bounds yield

\[
 \|W\|^2\ge\frac{1+k}{2}a^2,\quad
 \|W\|^2\ge\frac{1+k}{2}b^2,\quad
 \|W\|^2\le c ab.
\]

Multiplication forces `(1+k)/2<=c`, contrary to `k>2c-1`.
An edge through a third code point would have length at least `2d`,
whereas `L<2d` since `k>2c-1>2c^2-1=cos(2d)`.
Adjacent-edge overlap puts one other endpoint on an edge and is likewise
impossible. Here `k-(2c-1)=1-c-e>=39/100`. Thus the cycle is simple;
also no additional code point lies on its boundary.

Let `S=sum_i v_i`. The shortest cycle paths of one, two and three edges
give endpoint distances at most `L,2L,3L`, respectively, all below `pi`.
Consequently

\[
 v_i\cdot S\ge1+2k+2\cos(2L)+\cos(3L)
             =(1+k)(4k^2-1)>0.                                \tag{2}
\]

The hemisphere centered at `S/||S||` contains every vertex and every minor
edge. Gnomonic projection sends the boundary to a simple planar polygon.
Its bounded region lies in the convex hull of its projected vertices,
including when it is concave. The inverse image is compact in that open
hemisphere and has area less than `2*pi`; it is exactly the smaller region
`P`. Write `H` for its spherical convex hull. Then `P` is contained in `H`.

## 3. Interior points force interior caps

Define `r` by

\[
 \cos r=\frac{c}{\cos(L/2)}
       =c\sqrt{\frac{2}{1+c-e}}.                               \tag{3}
\]

We have `0<r<pi/2`. Indeed `1+c-e-2c^2` is concave and has minimum
`87/100>0` on `[14/25,3/5]`.

Suppose an additional code point `q` belongs to `P`; Section 2 makes it
interior. On an actual edge `AB` of length `ell<=L`, the point at arc
parameter `t in[0,ell]` is

\[
 x(t)=\frac{\sin(\ell-t)A+\sin(t)B}{\sin\ell}.
\]

Its endpoint packing bounds give

\[
 q\cdot x(t)\le
 c\frac{\sin(\ell-t)+\sin(t)}{\sin\ell}
 =c\frac{\cos(t-\ell/2)}{\cos(\ell/2)}
 \le\frac{c}{\cos(L/2)}=\cos r.                              \tag{4}
\]

Thus the entire boundary avoids the open geodesic radius-`r` cap about `q`.
That cap is connected and contains `q`, so it belongs to the same component
of the boundary complement as `q`: it is contained in the interior of `P`.
Its closure is contained in closed `P`.

If two code points `q,y` were in `P`, both of their closed radius-`r` caps
would therefore be in `P`. Their center distance `s` satisfies `s>=d>0`.
Both caps are compactly contained in the hemisphere of Section 2, hence

\[
 s<\pi-2r.                                                     \tag{5}
\]

For example, if that hemisphere has center `w`, containment of a closed cap
forces `dist(w,q)+r<pi/2`; apply this also to `y` and the triangle inequality.
Let `K` be the spherical convex hull of these two caps. It is compactly
hemispherical and is contained in `H`, though it need not be in concave `P`.

## 4. Perimeter comparison without convexity of the cycle

We need `perimeter(K)<=length(boundary P)`. Here is the relevant elementary
spherical great-circle counting argument.

For a minor edge `AB` of length `ell`, the great circle with oriented normal
`n in S^2` crosses its relative interior precisely when `n dot A` and
`n dot B` have opposite signs, apart from a measure-zero set. These normals
form two antipodal spherical lunes of total area `4ell`. Therefore, for a
finite minor-geodesic polygonal curve `C`,

\[
 \int_{S^2}N_C(n)\,dA(n)=4\,\operatorname{length}(C),            \tag{6}
\]

where `N_C` counts transverse edge intersections. This is a finite sum of
lune areas, rather than an assumed smooth-curve formula.

For a convex hemispherical geodesic polygon `E` contained in `H`, a generic
great circle crossing its interior crosses its boundary exactly twice.
It has vertices of `E` on both sides, and hence boundary vertices of `P`
on both sides: otherwise all their normalized nonnegative combinations,
including `E`, would be on just one side. The closed cycle consequently
has at least two crossings. For every generic normal we thus have
`N_boundaryP>=N_E`. Integrating (6) gives

\[
 \operatorname{perimeter}(E)\le\operatorname{length}(\partial P).
\]

Approximate the boundary of `K` by inscribed convex geodesic polygons to get

\[
 \operatorname{perimeter}(K)\le\operatorname{length}(\partial P)
                             \le6L.                            \tag{7}
\]

The explicit boundary of `K` below consists of two great-circle segments and
two small-circle arcs. Uniformly subdividing its small-circle arcs suffices
for this limit: a radius-`r` small-circle increment `theta` has minor chord
length `2asin(sin(r)sin(theta/2))`, whose ratio to `theta` tends to `sin(r)`.
All inscribed polygons stay in `K` and hence `H`. This justifies the limit
in (7) directly for the particular body used here.

## 5. Exact spherical two-cap hull perimeter

For `0<r<pi/2` and `0<s<pi-2r`, the boundary of the spherical convex hull
of two radius-`r` caps at center distance `s` consists of two common tangent
great-circle segments and one exposed small-circle arc from each cap.
Its perimeter is

\[
 B(r,s)=2\ell_t+4\sin r\,\alpha,
 \quad \ell_t=2\arcsin\frac{\sin(s/2)}{\cos r},
 \quad \alpha=\arccos\bigl(\tan r\tan(s/2)\bigr).               \tag{8}
\]

To verify both the formula and the exposed arcs, a supporting hemisphere
normal `n` contains a radius-`r` cap about `q` exactly when
`n dot q>=sin(r)`. The common tangent normals solve
`n dot q=n dot y=sin(r)`; there are exactly two because (5) holds.
The tangent feet from the two centers are
`a=(q-sin(r)n)/cos(r)`, `b=(y-sin(r)n)/cos(r)`. Their dot product is

\[
 a\cdot b=\frac{\cos s-\sin^2r}{\cos^2r}
          =1-2\frac{\sin^2(s/2)}{\cos^2r},
\]

giving the minor tangent-segment length in (8).

At `q`, let `E=(y-cos(s)q)/sin(s)` be the unit tangent direction toward
`y`. A normal tangent to the first cap is
`n=sin(r)q+cos(r)u`, with unit tangent `u`. It contains the other cap
exactly when

\[
 u\cdot E\ge\tan r\tan(s/2).
\]

The corresponding contact point is `cos(r)q-sin(r)u`: its bearing points
away from `y`. The exposed bearings therefore comprise the arc centered
on the direction away from `y` with half angle `alpha`, giving length
`2sin(r)alpha`. The same holds at `y`. Supporting hemispheres determine
the convex hull in a containing open hemisphere (equivalently use ordinary
separation after gnomonic projection). The two common tangent normals supply
the two intervening geodesic segments, so these are all boundary pieces.
A supporting face consists of the convex hull of the cap contact points:
a nonnegative combination has normal dot zero only when every term used
has normal dot zero. A tangent normal touching one cap gives one point;
one touching both gives their minor segment. No other supporting face occurs.
This proves (8); no Euclidean stadium formula has been substituted.

The arguments of both inverse trigonometric functions in (8) are in `(0,1)`
by (5). Writing `Delta=cos(r)^2-sin(s/2)^2>0`, differentiation gives

\[
 \frac{\partial B}{\partial s}
   =\frac{2\sqrt\Delta}{\cos(s/2)}>0,
 \qquad
 \frac{\partial B}{\partial r}=4\cos r\,\alpha>0.               \tag{9}
\]

For the second identity the tangent-segment derivative cancels the derivative
of `alpha` in the small-circle terms. In particular, `s>=d` implies
`B(r,s)>=B(r,d)`.

## 6. Certified comparison on the complete parameter interval

Keep `e=1/100` and define

\[
 J(c)=B(r(c),d(c)),\qquad d(c)=\arccos c.
\]

The pair `r(c),d(c)` is in the domain (5): equivalently

\[
 4c^2>(1-c)(1+c-e),
 \quad 5c^2-ec+e-1>0.
\]

The last polynomial is increasing here and its lower endpoint is
`1431/2500>0`. The function `d(c)` decreases. Also `r(c)` decreases,
since

\[
 \frac{d}{dc}\cos^2 r(c)
 =\frac{2c(2+c-2e)}{(1+c-e)^2}>0.
\]

Thus (9) makes `J` decreasing. On any cell `[a,b]` in the parameter interval,

\[
 J(c)-6\arccos(c-e)\ge J(b)-6\arccos(a-e).                    \tag{10}
\]

For fixed rational `c`, the endpoint formula uses only three rational
radicands and inverse cosines:

\[
 S_2=1-\frac{2c^2}{1+c-e},\quad
 V_2=\frac{(1-c)(1+c-e)}{4c^2},\quad
 A_2=\frac{(1+c-e-2c^2)(1-c)}{2c^2(1+c)},
\]
\[
 J(c)=4\arccos\sqrt{1-V_2}
      +4\sqrt{S_2}\,\arccos\sqrt{A_2}.                         \tag{11}
\]

The following are outward bounds, with terminating decimals denoting **exact
rational numbers**, not floating-point evidence. Five contiguous cells cover
the whole interval, and every difference exceeds `1/25=0.04` radians.

| `a` | `b` | lower bound for `J(b)` | upper bound for `6acos(a-e)` | lower difference |
|---|---|---:|---:|---:|
| 14/25 | 71/125 | 5.972815 | 5.930593 | 0.042222 |
| 71/125 | 72/125 | 5.940024 | 5.872936 | 0.067088 |
| 72/125 | 73/125 | 5.905902 | 5.814904 | 0.090998 |
| 73/125 | 74/125 | 5.870453 | 5.756484 | 0.113969 |
| 74/125 | 3/5 | 5.833678 | 5.697663 | 0.136015 |

[check.py](check.py) establishes these exact enclosures using 80-bit dyadic
square-root brackets and a fixed 32-term alternating arctangent enclosure.
[audit.py](audit.py), importing none of that implementation, uses 96-step
rational root bisection, a fixed 64-term positive arcsine enclosure and a
proved Machin identity for `pi`. All five full endpoint and cell records
agree after outward rounding to the exact `10^-6` grid. The validity of the
series remainders and the trust boundary are given in [NUMERICS.md](NUMERICS.md).
No adaptive increase until a desired sign occurs is used.

## 7. Contradiction and scope

If two additional code points were in `P`, (7)--(11) would force

\[
 6L\ge\operatorname{perimeter}(K)
     =B(r,s)\ge B(r,d)=J(c)>6L+1/25,
\]

a contradiction. Hence there is at most one additional point in `P`.
For fifteen points, the smaller side of every such six-cycle contains at
most one of the remaining nine points. This proves the graph consequence
in Section 1, even when the points counted have degree zero in the selected
near-contact graph.

The wider edge tolerance `1/40` is not certified by this comparison: the
same-parameter stadium-minus-edge-budget quantity at `c=14/25` is strictly
negative there, as both programs check. This is failure of that scalar route,
not a counterexample to any wider geometric theorem. The exact two-insertion
regular hexagons from our previous radial proof occur below `14/25`; they
do not violate this result.

The proof's continuous/topological steps are written and unformalized. The
endpoint arithmetic has two author implementations sharing CPython/Fraction;
this is not independent researcher review. The result removes the radial
and coordinate-template hypotheses for six-cycle **regions** on its stated
interval and edge band. It does not upgrade those regions to entire convex
hulls, prove an optimizer motif occurs, bound the total number of contacts,
or solve global fifteen-point optimality.
