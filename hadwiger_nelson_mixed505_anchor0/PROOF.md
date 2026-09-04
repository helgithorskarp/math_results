# Universal angular exclusion for one mixed 505-vertex assembly

Let `A` be the archived Parts `v159e646` point set, with its origin at
source label 0. Let `V` be the archived `v214e977` point set in source order.
Set

\[
t=\frac{5+i\sqrt{11}}6,\qquad B=A\cup tA,\qquad
q=V_0=1-\frac{\sqrt{33}}6,\qquad H=V-q.
\]

**Theorem (exact computer-assisted).** For every plane Euclidean isometry
`g` fixing the origin, the strict unit-distance graph on `B union g(H)` is
four-colorable. The family has at most 505 vertices.

The inner multiplier `t` and the anchor `q` are fixed. The theorem includes
all angular parameters in both orientation parities. It does not assert
an exclusion for another anchor, another inner placement, or an arbitrary
graph of this order.

## 1. Geometry and reflection symmetry

All component coordinates lie in the restricted complex field

\[
E=\mathbb Q(i\sqrt3,i\sqrt{11})=R(\alpha),\qquad
R=\mathbb Q(\sqrt{33}),\quad\alpha=i\sqrt3.
\]

The coefficient tuple `(a,b,c,d)` denotes
`a+b sqrt(33)+c i sqrt(3)+d i sqrt(11)`. This is a subfield of the complex
numbers, not the larger Cartesian plane `Q(sqrt(3),sqrt(11))^2`.

Since `|t|=1`, the two copies used in `B` are isometric. Exact coordinate
reconstruction gives 26 overlaps and 18 new inner edges, hence 292 distinct
vertices and 1,251 strict unit edges. Its labels retain `A` first, followed
by previously unseen points of `tA` in source order. The origin has label 0.
The centered component `H` has 214 distinct vertices and 977 strict unit
edges, and its label 0 is also the origin.

Both implementations check the permutation `j -> rho(j)` specified by
`conjugate(H[j])=H[rho(j)]`, including `rho(0)=0` and `rho^2=id`. Therefore
`conjugate(H)=H` as point sets. An origin-fixing isometry has the form
`z -> uz` or `z -> u conjugate(z)` with `|u|=1`, so it suffices to consider
`B union uH` for all unit complex numbers `u`. Reflection adds no point
sets for a given multiplier. We count unit multipliers, without counting
the reflection parity a second time or quotienting by other symmetries.

## 2. Reduction of all angles to finitely many complete edge sets

The previously proved [field-coloring theorem](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
four-colors the entire `E`. Thus every multiplier `u in E` is settled,
including all additional coincidences and edges in that branch.

Suppose `u not in E`. A nonzero coincidence `b=uh`, with `b in B` and
`h in H`, would give `u=b/h in E`. Consequently the only common point is
the origin. The union has exactly `292+214-1=505` vertices and
`1251+977=2228` internal edges. Edges incident to the shared origin already
belong to these internal graphs.

If there is no new cross edge, component colorings can be permuted to agree
at the origin and glued. Otherwise fix a new edge `|b-uh|=1` with `b,h`
nonzero. Set

\[
c=\overline b h\ne0,\qquad S=|b|^2+|h|^2-1,\qquad
\Delta=4|b|^2|h|^2-S^2.
\]

Here `c in E` and `S,Delta in R`. The edge equation and `|u|=1` imply

\[
cu^2-Su+\overline c=0.
\]

If `Delta<0`, there is no unit root. If `Delta>=0`, the two roots, counted
with multiplicity, are `(S +/- sqrt(-Delta))/(2c)` and have modulus one.
For positive `Delta`, a square root of `-Delta` lies in `E=R+alpha R`
exactly when `Delta/3` is a square in `R`. Indeed a purely imaginary element
of `E` is `alpha y` with `y in R`, whose square is `-3y^2`. The double-root
case `Delta=0` also lies in `E`.

Every remaining pair therefore yields an irreducible monic quadratic

\[
P_{b,h}(X)=X^2-TX+W,\qquad T=S/c,\qquad W=\overline c/c.
\]

Two such polynomials have a root outside `E` in common if and only if they
are equal: both would be that root's monic minimal polynomial over `E`.
It follows that equal-polynomial classes are precisely the **complete**
new cross-edge sets at either root. Each class has two distinct unit roots;
different classes have disjoint multiplier sets. Conversely each root
realizes every edge in its class. This exhausts all angles with new cross
edges, without a discretization or a denominator cutoff.

This reduction is the unequal-component argument from the
[fixed-Moser three-copy proof](../hadwiger_nelson_nonmono159_moser_triple/PROOF.md),
applied to `B,H`. Its validity does not require congruent components.

## 3. Exact census and coloring certificate

The exhaustive classification of the `291*213=61,983` nonzero labeled
pairs is:

| Pair class | Count |
|---|---:|
| Negative discriminant | 10,682 |
| Unit roots in `E` | 14,028 |
| Two unit roots outside `E` | 37,273 |

The last row yields 24,423 quadratic classes and 48,846 unit multipliers.
The complete cross-edge histogram is:

| New cross edges | Classes |
|---|---:|
| 1 | 16,893 |
| 2 | 4,926 |
| 3 | 1,333 |
| 4 | 678 |
| 5 | 265 |
| 6 | 135 |
| 7 | 56 |
| 8 | 53 |
| 9 | 34 |
| 10 | 22 |
| 11 | 12 |
| 12 | 6 |
| 13 | 4 |
| 14 | 6 |

Thus the outside-field cases with a new cross edge have between 2,229 and
2,242 strict edges on 505 vertices. The bound of 14 concerns new cross
edges outside `E`; it is not a bound for the separate in-field branch.

Use the three proper `B` colorings from the prior three-copy certificate
and the two proper `H` colorings in `colors_H.txt`. Every row has color 0
at its component origin. The verifier checks every internal edge, then for
each quadratic class finds rows `f,k` and one of the six color permutations
`pi` fixing 0 such that `f(b) != pi(k(h))` at every new cross edge.
This defines a proper union coloring: it agrees on the sole overlap,
preserves all internal edges, and satisfies the complete cross-edge set.
Every class is covered. The already-settled in-field and cross-edge-free
branches complete the universal theorem.

The five component rows total 1,309 bytes: 879 reused bytes for `B` and
430 bytes for `H`. The two `H` rows came from the field coloring. No new
SAT query was needed to discover this certificate. Verification uses only
positive colorings and exact arithmetic; it needs no solver.

## 4. Checks with different arithmetic and explicit coordinates

The main verifier uses the four-coefficient field implementation and the
exact real-sign and square criteria from the prior census. The second
implementation uses `E=R+alpha R`, independently reconstructs both
components and their strict graphs, and groups pairs by `c/S` when `S!=0`
and by the real projective direction of `c` when `S=0`. This avoids the main
monic leading-coefficient normalization. It independently checks coloring
coverage and agrees on the hashes of every pair classification, the entire
edge partition, and the reflection permutation.

A class attaining the maximum 14 new edges, seeded by labels `(70,143)`,
has

\[
T=\frac{-1+i\sqrt{11}}3,\qquad
W=\frac{-5-i\sqrt{11}}6.
\]

Writing `beta=i sqrt(11)`, its two roots are

\[
u_\varepsilon=\frac{(\beta-1)(1+\varepsilon i\sqrt2)}6
 =\frac{-1-\varepsilon\sqrt{22}
          +i(\sqrt{11}-\varepsilon\sqrt2)}6,
\qquad\varepsilon\in\{-1,1\}.
\]

Their norm is one and they satisfy `u^2-Tu+W=0`. Their nonzero real
`sqrt(22)` coefficients also show they lie outside `E`, by linear
independence in the real basis of `Q(sqrt(2),sqrt(3),sqrt(11))`.

The standalone `check_example.py` imports neither census nor field code.
It constructs `B` and both `u_epsilon H` directly in that eight-element
real radical basis at common integer coordinate scale 72. It checks the
unit norm and quadratic identities by integer arithmetic. For both roots
and both labeled orientation parities, it examines all 127,260 vertex pairs,
checks all 505 points are distinct, recovers 1,251 and 977 internal edges
and exactly the predicted 14 cross edges, and verifies the actual coloring.
Reflections use the checked permutation of `H` to transport color labels.
All four realizations have 2,242 strict unit edges. The two parities at a
given root are the same point set; the check does not claim four different
graphs.

All checks passed. They are implementation cross-checks by the author,
not an independent review of this result. The continuous-to-finite bridge
and imported field-coloring theorem are ordinary unformalized mathematics.
Other trust boundaries are the hash-pinned coordinate and coloring input,
the exact Python programs, and ordinary software/hardware execution. No
floating-point unit-distance decision or omitted large certificate occurs.

## 5. Source and research scope

The coordinate [provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md)
is Parts' archived data accompanying
[the graph-minimization paper](https://arxiv.org/abs/2010.12665).
The 509-vertex benchmark is also reported in the introduction of
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4), checked
on 2026-09-04. No record improvement is obtained here.

This result closes one mixed gadget assembly inside the target vertex
budget. Its small outside-field contact bound gives a concrete reason to
seek a denser anchoring or a different inner placement before further
coloring searches. Neither a universal mixed-gadget obstruction nor a
priority claim for the quadratic and color-permutation methods is made.
