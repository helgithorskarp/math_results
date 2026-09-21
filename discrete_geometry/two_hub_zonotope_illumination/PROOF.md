# Exact illumination of two-hub graphical zonotopes

Let `n>=1`. The graph `K_(2,n)` has hubs `a,b`, leaves `1,...,n`,
and every edge from a hub to a leaf. In the sum-zero space
`V subset R^{n+2}`, give its edges arbitrary positive real weights and set

\[
 Z=\sum_{i=1}^n[-\alpha_i(e_a-e_i),\alpha_i(e_a-e_i)]
   +\sum_{i=1}^n[-\beta_i(e_b-e_i),\beta_i(e_b-e_i)],
 \qquad \alpha_i,\beta_i>0.
\]

All interiors and directions are relative to `V`, of dimension `n+1`.
Using one-sided segments or reversing generators only translates the
body or changes the positive weights, so the same result holds for those
conventions.

**Theorem.** The ordinary and fractional illumination numbers satisfy

\[
                         I(Z)=I_f(Z)=2^n+2.             \tag{1}
\]

There is an explicit optimal set of directions which works for every
positive weight assignment. There are `2^n+2` corresponding vertices
which are pairwise antipodal, certifying both lower bounds. The theorem
does not determine illumination for general graphical zonotopes or prove
the general illumination conjecture.

A nonzero direction `u` illuminates a boundary point `p` if
`p+t u` lies in the interior for some `t>0`. Fractional illumination
allows a finite nonnegative Borel measure on normalized directions, with
mass at least one on the directions illuminating each boundary point.

## 1. Standard normal-cone facts and positive weights

If a full-dimensional polytope is given by finitely many inequalities
`f_j(x)<=b_j`, a direction illuminates `p` precisely when
`f_j(u)<0` for every inequality active at `p`. Necessity is immediate;
for sufficiency choose a sufficiently small positive step, also preserving
each initially strict inequality. Redundant inequalities cause no problem.
Equivalently, `f(u)<0` for every nonzero covector in the outward normal
cone at `p`.

Illuminating every vertex suffices. If `p` is in the relative interior
of a face, choose one of its vertices `v`; every inequality active at
`p` is active at `v`. Thus a direction illuminating `v` illuminates `p`.

Positive rescaling of individual zonotope generators preserves their
normal fan and all these illumination sets at corresponding vertices.
For clarity, a covector `f` uniquely maximizes on a generator segment
at the endpoint prescribed by the sign of `f(g)`, provided `f(g)!=0`.
The regions of the hyperplane arrangement `f(g)=0` therefore index
vertices, and their closures are the normal cones, independently of
positive segment lengths. A boundary hyperplane gives a nondegenerate
segment in the maximizing face, so adjacent regions cannot merge into
one vertex after a positive rescaling. This proves the assertion and
also transfers fractional illumination measures.

This invariance is known: Rotem--Schejter--Slomka, Lemma B.1. We included
the normal-fan proof to specify exactly what transfers. We do **not**
assert that the different weighted bodies are affinely equivalent.

It remains to prove (1) when every weight equals one.

## 2. A common-axis sum of diamonds

Write an unweighted zonotope point using `s_i,t_i in [-1,1]` on the
generators at `a,b`. Define linear coordinates on `V` by

\[
 x_i=\tfrac12 y_i=-\tfrac12(s_i+t_i),\qquad
 z=\tfrac12(y_a-y_b)=\tfrac12\sum_i(s_i-t_i).
\]

This is an isomorphism, with inverse

\[
 y_i=2x_i,\qquad y_a=z-\sum_i x_i,\qquad
 y_b=-z-\sum_i x_i.                                    \tag{2}
\]

Put `z_i=(s_i-t_i)/2`. The conditions `|s_i|,|t_i|<=1` are
equivalent to `|x_i|+|z_i|<=1`. For a fixed `x`, the possible sums
`z=sum z_i` form the full interval of radius `sum_i(1-|x_i|)`.
The image of the zonotope is therefore exactly

\[
 P_n=\{(x,z): |x_i|\le1\ (1\le i\le n),\quad
                     |z|+\sum_i|x_i|\le n\}.           \tag{3}
\]

In particular, this is not a product decomposition of independent
circuits. For `n>=3`, the four-cycles in `K_(2,n)` overlap.

The complete vertex set is

\[
 (x,\delta(n-k)),\qquad
 x\in\{-1,0,1\}^n,\quad
 k=|\{i:x_i\ne0\}|,\quad \delta\in\{-1,1\},           \tag{4}
\]

with the two choices of `delta` identified when `k=n`.
To prove completeness, intersect (3) with a fixed coordinate orthant
and `z>=0` or `z<=0`. After sign changes this is
`0<=x_i<=1`, `0<=z<=n-sum x_i`. It is the convex hull of the two
affine graphs over the cube's vertices. Thus all its candidate vertices
have zero-one `x` and either height zero or height `n-sum x_i`.
The height-zero candidates with `k<n` are not vertices of `P_n`, since
they are midpoints of two points with opposite nonzero heights. Every
point in (4) is exposed: the covector having coefficients `2x_i` on
the nonzero coordinates, zero on the others, and `delta` on `z` has
that point as its unique maximum, by (3). This also covers `k=0,n`.
There are exactly `2*3^n-2^n` vertices.

## 3. Matching lower certificate

Consider the following `2^n+2` vertices:

\[
 \mathcal A=\{(\varepsilon,0):\varepsilon\in\{-1,1\}^n\}
                   \cup\{(0,n),(0,-n)\}.              \tag{5}
\]

They are pairwise antipodal, meaning that each pair lies on opposite
parallel supporting hyperplanes (the hyperplanes need not touch uniquely).
Two different cube corners have some coordinate `x_i` equal to `1`
and `-1`, so the corresponding box inequalities certify antipodality.
The two poles are opposite extremes of `z`. A corner `(epsilon,0)`
and pole `(0,delta n)` are opposite extremes, `-n` and `n`, of

\[
                  -\sum_i\varepsilon_i x_i+\delta z,
\]

whose absolute value is at most `n` throughout (3).

No direction illuminates two points on opposite supporting hyperplanes:
the direction would have to strictly decrease both a nonzero normal and
its negative. Hence the illumination-direction sets of all the points
in (5) are pairwise disjoint. Every ordinary illuminating set has at
least `2^n+2` directions. Integrating against any feasible Borel
illuminating measure gives total mass at least `2^n+2` as well.

The normal-fan correspondence in Section 1 transfers the same opposing
normal pairs to the corresponding vertices of every positively weighted
zonotope. Thus the lower certificate is not a unit-weight accident.

## 4. An explicit parity cover

For each sign vector `eta in {-1,1}^n`, use the direction

\[
 d_\eta=\big(\eta,(n-1)\prod_i\eta_i\big).
\]

Add the two directions `(0,1)` and `(0,-1)`. The resulting set has
exactly `2^n+2` distinct nonzero directions. Apply (2) to obtain the
claimed directions in the original sum-zero graph coordinates. They
may be normalized, without changing illumination.

At a cube corner `(epsilon,0)`, take `eta=-epsilon`. Every active
box inequality decreases. The one-sided derivative of the other
constraint along this direction is

\[
                |(n-1)\prod_i\eta_i|+\sum_i\varepsilon_i\eta_i
                       =(n-1)-n=-1.
\]

At a vertex in (4) with `1<=k<n`, fix `eta_i=-x_i` on the `k`
nonzero coordinates. At least one sign is free, so choose the signs
on zero coordinates to force `prod eta_i=-delta`. Active box
constraints again decrease, and the one-sided derivative of the
last constraint in (3) is

\[
 \delta(n-1)\prod_i\eta_i
       +\sum_{x_i\ne0}x_i\eta_i+\sum_{x_i=0}|\eta_i|
      =-(n-1)-k+(n-k)=1-2k<0.                         \tag{6}
\]

These derivatives are exact linear expressions for all sufficiently
small positive steps, so there is no differentiability assumption at
zero coordinates. Inactive box constraints remain strict for a small
step. Finally, the poles (`k=0`) are illuminated by the pure vertical
direction pointing toward the origin. For `n=1` there are no intermediate
vertices; the formula supplies the four directions for a parallelogram.

Every vertex, and hence the whole boundary, is illuminated. Combined
with Section 3, this proves (1). Positive weights inherit the same
direction set in graph coordinates by Section 1. The necessary small
step size can depend on the weights and on the point.

## Scope and verification

Strict positivity of every edge weight matters. For example, removing
one edge from `K_(2,2)` leaves a tree; its three-dimensional graphical
zonotope is a parallelotope with illumination number eight rather than
six. No zero-weight extension is asserted. The case `n=0` is not covered.

The normal-fan correspondence, positive-generator rescaling invariance,
and use of antipodal vertices as lower bounds are established methods.
The result here is the explicit two-hub formula, parity cover and matching
certificate; priority is only relative to the primary sources inspected
in [SOURCES.md](SOURCES.md). No general fractional-illumination equality
for arbitrary zonotopes is claimed.

The universal result is the proof above. [verify.py](verify.py) checks
the concrete inequality model and separately reconstructs the original
weighted graph zonotopes using acyclic orientations and all supporting
cuts. Those exact finite computations corroborate the proof; they do
not establish its universal quantifiers or constitute independent peer
review or a proof-assistant formalization.
