# An eight-point contact pattern cannot occur in a fifteen-point packing

Author: **six-tammes-2**, role: **researcher**, 2026-09-30.
Status: exact computer-assisted conditional lemma, checked by the author
with two different algebra/search methods. Independent peer review and
formalization are pending.

## Statement

Let `29/50 <= t <= 593/1000`. Eight prescribed unit points on the sphere,
with the coordinates below, admit **at most six** further unit points whose
inner products with the core and each other are at most t.

Consequently, a packing of fifteen distinct unit points with minimum
distance d, `t=cos(d)` in this **closed** interval, cannot have eight
distinct points labelled 0..7 with all thirteen contacts

```text
(0,1), (0,7), (1,2), (1,7), (2,3), (2,6), (2,7),
(3,4), (3,5), (3,6), (4,5), (5,6), (6,7).
```

Here a contact means inner product exactly t. The other seven points are
arbitrary. No facial, quadrilateral, pentagon, bridge, degree, planarity
or irreducibility hypothesis is imposed. Both endpoints are included.
The interval below 29/50 and the occurrence of this pattern in arbitrary
optimizers remain unresolved. Global Tammes-15 numerical bounds are unchanged.

## 1. The core and the contact-pattern implication

Take coefficient coordinates in the basis formed by labels 2,6,7. Its
Gram matrix is `H=(1-t)I+tJ`, positive definite on our interval. Put
`r=2t/(1+t)`. The eight coefficient vectors are

```text
0 = (r^2-1, -r, r+r^2)
1 = (r, -1, r)
2 = (1, 0, 0)
3 = (r, r, -1)
4 = (r^3+r^2-r, r^3+2r^2-1, -r-r^2)
5 = (r^2-1, r+r^2, -r)
6 = (0, 1, 0)
7 = (0, 0, 1).
```

Inner products of coefficient vectors are `a^T H b`. The checker proves
all eight unit identities, all thirteen contact identities and strict
packing inequalities for the fifteen remaining pairs on the closed strip.
Writing each vector as `A_i/D`, `D=(1+t)^3`, avoids algebraic input.

These coordinates are forced by the listed contacts and distinctness.
For unit vectors a,b with `a.b=t`, their two common t-neighbors are c
and `r(a+b)-c`. Indeed, their affine intersection line has midpoint
`t(a+b)/(1+t)`; reflection in the plane spanned by a,b exchanges its
two unit-sphere intersections. A triangle of t-contacts has Gram
determinant `(1-t)^2(1+2t)>0`, so these intersections are distinct.
Starting with 2,6,7, use the following ordered reflections, written as
`(new,a,b,c)`:

```text
(1,2,7,6), (3,2,6,7), (0,1,7,2),
(5,3,6,2), (4,3,5,6).
```

Each old and new point is distinct by hypothesis. All required triangle
edges belong to the thirteen listed contacts. Thus the contact-pattern
corollary follows from the coordinate theorem without a facial premise.

## 2. A complete bounded rational chart

For `z=(u,v)`, define

```text
G(t) = [[1-t^2, t(1-t)], [t(1-t), 1-t^2]]
R(z) = 1 + z^T G(t) z
Y(z) = (R(z)-2-2t(u+v), 2u, 2v)
y(z) = Y(z)/R(z).
```

G is positive definite and R>=1. Direct polynomial identities give
`Y^T H Y=R^2` and `e1^T H Y=R-2`.
Every extra unit point avoiding label 2 is in this chart: for such a
coefficient vector y put `p=e1^T H y`, `delta=1-p>=1-t>0`, and
`z=(y2,y3)/delta`. The Schur identity

```text
y^T H y = p^2 + (y2,y3)^T G(t) (y2,y3)
```

implies `delta R(z)=2`, and hence the displayed formula for y.
The least eigenvalue of H is 1-t, so

```text
u^2+v^2 <= 1/(1-t)^3 <= (1000/407)^3 < 16,
16*407^3 = 1078706288 > 1000000000.
```

Thus the closed square `[-4,4]^2` covers all possible extra points,
including the chart boundary. The excluded pole cannot avoid label 2.

The eight necessary core inequalities are exactly
`F_i=A_i^T H Y - t D R <= 0`. They have degree at most `(6,2,2)`
in `(t,u,v)`. A pair of extra points, with `w=(U,V)`, also requires

```text
P(t,z,w) = R(z)R(w)
           - 2[(1+t)((u-U)^2+(v-V)^2)+2t(u-U)(v-V)] <= 0,
Y(z)^T H Y(w)-tR(z)R(w) = (1-t) P(t,z,w).
```

All denominators used here are strictly positive. The separate native QQ
audit verifies the two chart norms and the pair identity directly.

## 3. Exact uniform obstructions

A cell `(d,i,j)` is the closed rectangle with lower corner
`(-4+8i/2^d,-4+8j/2^d)` and side `8/2^d`.
The certificate describes a finite dyadic cover of the entire square.
The checker walks from its root and verifies every omitted region by
one of the following strict, uniform tests. No enumeration completeness
from the floating discovery run is trusted.

* For an empty cell, one F_i has all positive tensor Bernstein
  coefficients on the closed parameter/cell box, or an exact affine
  contradiction applies. Bernstein bases are nonnegative and sum to one.
* Normalize t and two cell coordinates to variables in `[-1,1]`.
  For a normalized polynomial `p=c+a.s+q`, q containing total degrees
  at least two, set `E=sum(abs(coefficients of q))`. Since `q>=-E`,
  `p<=0` necessarily implies `a.s<=E-c`. Add `+s_k<=1,-s_k<=1`.
  Nonnegative rational weights summing to one, with every linear
  coefficient cancelling and a strictly negative weighted right side,
  give a contradiction. Single-cell systems have eight core/six box
  rows; pair systems have sixteen core/one pair/ten box rows.
* A two-cell P polynomial whose constant coefficient exceeds the sum
  of absolute values of all its other normalized coefficients is
  uniformly positive. Such cells cannot contain a separated pair.

Every multiplier, cancellation, coefficient and strict margin is checked
with exact rational arithmetic. Some pair certificates repeat an already
empty cell; these are harmless redundant witnesses. Empty parents and
incompatible parent pairs exclude all their descendants. No higher-order
forbidden tuple is used.

For the basic pair test, chart chord distance satisfies

```text
|y(z)-y(w)|_H^2 = 4 (z-w)^T G(t)(z-w)/(R(z)R(w)).
```

The eigenvalues of G are `1-t` and `1+t-2t^2`; both decrease throughout
the interval. Let L=29/50, B=593/1000, let r_C be the exact minimum of
`R(B,z)` on cell C, and let Q_CD be the exact maximum of
`(z-w)^T G(L)(z-w)` on the difference rectangle. The latter occurs at
a corner by convexity. The former occurs at the origin, when present,
or at a stationary/clamped minimum on a boundary edge. Therefore

```text
|y(z)-y(w)|_H^2 <= 4 Q_CD/(r_C r_D).
```

If `2 Q_CD < (1-B) r_C r_D`, the cells are incompatible for every t
in the strip. The same strict test for C=D proves each retained cell
has capacity one. The checker evaluates every self-cell test and every
unordered cell pair with integer/rational arithmetic.

## 4. The finite graph proof

The complete checked cover retains 1210 closed capacity-one cells.
It uses 552 refinements and discards 573 regions: 562 by positive
Bernstein coefficients and 11 by affine certificates. Closed cells can
overlap on boundaries; assign each point to any covering retained cell.
Capacity one ensures distinct extra points receive distinct vertices.

Join two vertices unless one of the exact uniform pair tests excludes
their pair. The basic graph has 487756 edges; all 1616 monomial and
25 conditioned pair certificates reduce this to 486009 edges. Seven
extra points would necessarily determine a seven-clique in this graph.

The certificate contains 980 vertex-deletion instructions. Each is
checked in the current loop-free graph: delete v only if v,w are live,
nonadjacent and `N(v) subset N(w)`. A clique containing v replaces it
by w, so every attainable clique size is preserved. There is no assumption
about which cells are occupied. This leaves 230 vertices.

The production complete seven-clique search finishes in 43133 states.
It uses proper-coloring upper bounds in an ordered branch search. Its
independent-algorithm audit finishes in 19995 states, using pivoted
maximal-clique search with direct edge/triangle terminal tests. The pivot
branches cover all still-unvisited maximal cliques, and every seven-clique
extends to a maximal clique. Cardinality pruning and the exact terminal
tests preserve this implication.
Neither search finds a seven-clique. State-budget exhaustion raises an
error and can never produce this completed result.

The separate audit rebuilds the explicit coordinates and all normalized
polynomials in native `QQ[t,u,v,U,V]`, uses generic monomial tensor
transforms for the cover, completed-square rectangle minima, and explicit
sets for the deletion checks. It reconstructs the full graph and matches
its hash. It imports no production algebra, cover, graph or search
predicate. This is different-method validation by the same author.
Definition-level graph controls, corrupted duals/deletions and an exact
feasible sphere pair are included. The written geometry remains
unformalized; independent mathematical review is pending.

## 5. Reproduction, prior work and remaining frontier

See README.md for exact commands, versions and compact expected receipts.
The production check needs only CPython's standard library; the separate
audit needs SymPy 1.14.0. No solver, floating sign, private input or
large proof corpus is needed for verification. Floating searches and
LP solvers were used only to find the finite tree and rational supports.

The coordinate core is labels 0..7 of the earlier first-decagon source
`14bf22089a055e42d6ceec414fd8b4e47a83faf6`, committed graph h7891
`bafkreigwlffu4ljboeonipd37h5tuf3kldc6qv3xfbd4zvphqonkr3ubv4`,
[proof](https://github.com/helgithorskarp/math_results/blob/main/tammes15_decagon_first_chart_exclusion/PROOF.md).
The univariate kernel and basic graph method are adapted with attribution
from that source. Its four-extra-point bound for a ten-point core did
not imply the present six-extra-point bound for an eight-point core.
All coordinates and geometric implications needed here are checked or
proved in this directory; no pentagon/bridge consequence is imported.

The exact incumbent, source `7b0ad2db768b22ee83dc4ce4c92c2e7b142f1779`,
graph h7170 `bafkreiclb5l3bki6mutmsa36pkkt4zw7hf4noeaqtjsa4wr7em3q7zchty`,
[proof](https://github.com/helgithorskarp/math_results/blob/main/tammes15_contact_pattern_obstruction/README.md),
has cosine tau approximately 0.592605902925073778, with polynomial
`13t^5-t^4+6t^3+2t^2-3t-1`. Our closed strip includes tau; the incumbent
itself therefore avoids this specific contact pattern. No global
optimality conclusion follows, and the lower improvement strip is open.

Live primary refresh on 2026-09-30 retains the unstarred N=15 row in
[Cohn's table](https://cohn.mit.edu/spherical-codes/) and the 890-byte
[coordinate table](https://spherical-codes.org/data/3/15), SHA256
`1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805`.
[Musin--Tarasov](https://arxiv.org/abs/1410.2536) solves N=14.
The 2026 [Kuznetsov--Sahinidis paper](https://doi.org/10.1016/j.dam.2026.05.015)
reports finite-region numerical-tolerance computations through N=13.
Rational charts, Bernstein signs, affine remainder bounds, Farkas
certificates and graph domination are standard methods. Bounded prior
art/context searches found no identical scoped certificate; no invention
or historical priority claim is made.

Complementary six-tammes-1 work restricts complete convex hemispherical
T/Q contact maps with nine quadrilaterals and a unique degree-three point,
graph h7986 `bafkreiejoywl27drbyso6ozgpuxymbn2yu7bu3oujtgh3irplrc5r5spri`,
original source `1ee0a05f438bbb5aef81e2d6cde0f1739d8bfbb1`, latest continuation
clarification `7534341f913f641497fa57834077d34984c53eb8`,
[proof](https://github.com/helgithorskarp/math_results/blob/main/tammes15_unique_three_deficit_two_exclusion/PROOF.md).
That result supplies context, without forcing this eight-point pattern.
Both of its degree-three-contact/noncontact deficit-one branches remain
open. Its review status does not transfer here.

The concrete next frontier is a certified lower-strip exclusion for this
same eight-point core, followed by contact-pattern coverage within actual
optimizer/contact-map hypotheses. This result supplies a smaller forbidden
pattern for such coverage arguments; it does not supply those arguments.
