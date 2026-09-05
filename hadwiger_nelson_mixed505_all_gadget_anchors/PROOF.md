# An exact exclusion for every 214-gadget anchor at one fixed inner origin

Let `A` and `V` denote the archived Parts `v159e646` and `v214e977` point
sets in their hash-pinned source order. Define

\[
t=(5+i\sqrt{11})/6,\qquad B=A\cup tA.
\]

**Theorem.** For every Euclidean isometry `g` with `0 in g(V)`, the strict
unit-distance graph on `B union g(V)` is four-colorable. It has at most
505 vertices.

Only the chosen origin of `B` is an attachment point in this statement.
The location of `B`, its inner multiplier `t`, and the two gadget inputs
are fixed. The vertex of `V` attached there is arbitrary.

## 1. Field, geometry, and orientation reduction

Both components lie in

\[
E=\mathbb Q(i\sqrt3,i\sqrt{11})=R(\alpha),\quad
R=\mathbb Q(\sqrt{33}),\quad\alpha=i\sqrt3.
\]

A tuple `(a,b,c,d)` denotes `a+b sqrt(33)+c i sqrt(3)+d i sqrt(11)`.
The input tables have denominator 12. The multiplier `t` is unit, and the
exact union has 292 distinct vertices and 1,251 strict unit edges. Labels
retain `A` first and then append new points of `tA` in source order.
Its origin has label 0. The other component has 214 distinct vertices and
977 strict unit edges. These facts are reconstructed by both verifiers.

For an orientation-preserving `g` with `g(q)=0`, `q in V`, write
`g(V)=u(V-q)` with `|u|=1`. For an orientation-reversing map the image is
`u(conjugate(V)-conjugate(q))`. Both verifiers check
`conjugate(V)=V`, so the second image is also `u(V-r)` for the anchor
`r=conjugate(q) in V`. Thus it suffices to handle all 214 anchors and all
unit multipliers in the rotation parameterization. No quotient by other
geometric symmetries is used in the computation.

The [whole-field theorem](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
four-colors `E`. Therefore every `u in E` is settled, including additional
coincidences and all strict unit edges. This is a coloring theorem for the
restricted complex field, not the larger Cartesian plane
`Q(sqrt(3),sqrt(11))^2`.

If `u not in E`, a coincidence `b=u(v-q)` with `v!=q` would imply
`u=b/(v-q) in E`. Hence the sole overlap is the origin. The union then has
exactly 505 vertices and 2,228 internal edges, with every edge incident to
the origin already internal. If no further cross edge exists, component
colorings can be permuted to agree at the common point and glued.

## 2. Displacement census and exact projection to anchors

Put `D=V-V`. For any new cross edge, write `d=v-q != 0` and `b in B-{0}`.
With

\[
c=\overline b d,\qquad S=|b|^2+|d|^2-1,\qquad
\Delta=4|b|^2|d|^2-S^2,
\]

the unit-distance condition and `|u|=1` give

\[
cu^2-Su+\overline c=0.
\]

Here `c!=0`, `c in E` and `S,Delta in R`. If `Delta<0` there is no unit
root. If `Delta>=0`, the roots `(S +/- sqrt(-Delta))/(2c)` are unit.
They lie in `E` exactly when `Delta/3` is a square in `R`, including the
double-root case. For positive `Delta`, this follows because every purely
imaginary element of `E` is `alpha y`, `y in R`, with square `-3y^2`.

Every remaining pair defines an irreducible monic quadratic over `E`,

\[
P_{b,d}(X)=X^2-(S/c)X+\overline c/c.
\]

Two such polynomials share a root outside `E` exactly when they are equal,
by uniqueness of the root's monic minimal polynomial. Therefore an ambient
class `C` of equal quadratics is the complete set of pairs `(b,d)` giving
new cross edges at either of its two distinct unit roots. Different ambient
classes have disjoint multiplier sets.

For each anchor `q`, project this class to

\[
C_q=\{(b,v):(b,d)\in C,\ v=q+d\in V\}.
\]

The incidence table for `D` records every ordered pair `(q,v)` with
`v-q=d`. Thus `C_q` is the complete new cross-edge set for `B union u(V-q)`
at both roots of `C`. A nonempty `C_q` cannot coincide with the nonempty
projection of another ambient class: any common pair would force the
same pair `(b,v-q)` into both classes. Empty projections simply return to
the gluing case.

This proves completeness for every anchor without enumerating its repeated
displacement vectors again. The argument uses the
[earlier quadratic reduction](../hadwiger_nelson_nonmono159_moser_triple/PROOF.md)
and the [single-anchor instance](../hadwiger_nelson_mixed505_anchor0/PROOF.md),
with the additional exact projection through `V-V`.

## 3. Integer implementation of the field decisions

Represent `B` by integer coefficient tuples at denominator 72, and `D` by
integer tuples at denominator 12. For an integer tuple `z=(a,b,c,d)`, its
unscaled norm in `R` is

\[
N(z)=(a^2+33b^2+3c^2+11d^2)+(2ab+2cd)\sqrt{33}.
\]

Let `n_B=N(b_num)` and `n_D=N(d_num)`. Then

\[
S=S_0/5184,\quad S_0=n_B+36n_D-5184,\qquad
\Delta=\Delta_0/5184^2,\quad\Delta_0=144n_Bn_D-S_0^2.
\]

The rational positive square denominator does not affect signs or whether
`Delta/3` is a square in `R`. The sign of `p+q sqrt(33)` is decided by the
signs of `p,q` and comparison of `p^2` with `33q^2`, using integers only.

To test whether `(p+q sqrt(33))/3` is a square in `R`, if `q=0` test whether
`p/3` or `p/99` is a rational square. Otherwise a square root `r+s sqrt(33)`
requires the integer `p^2-33q^2` to be a nonnegative perfect square `k^2`,
and one of `(p+k)/6`, `(p-k)/6` to be a positive rational square `r^2`.
These conditions are sufficient too: take `s=q/(6r)` and substitute.
Rational square tests reduce numerator and denominator by their gcd and
check both with integer square roots. No floating-point sign or square
root is used.

Instead of normalizing by `c`, the integer verifier groups by `c/S` when
`S!=0`. Write `c=c_r+alpha c_i`, with `c_r,c_i in R`. The four rational
coefficients of `c_r/S` and `3c_i/S` are encoded with one positive common
denominator, reduced together by a gcd. Fixed scale factors common to all
pairs do not change equality. If `S=0`, use the real projective direction
of `c`: `3c_i/c_r` when `c_r!=0`, and a separate vertical key otherwise.
This is equivalent to equal monic quadratics: for `S!=0`, their nonzero
linear coefficient determines `c/S`, while for `S=0` the constant
`conjugate(c)/c` determines precisely the direction modulo a nonzero real
factor. All denominators divided by the code are nonzero in `R`.

The rational audit uses the original monic normalization `S/c` and
`conjugate(c)/c` with four-dimensional exact field arithmetic. It does not
import this integer verifier or its square-test implementation.

## 4. Exhaustive counts and positive colorings

The 45,582 nonzero ordered differences of `V` give 4,418 distinct nonzero
vectors. All `291*4418=1,285,638` pairs with a nonzero vertex of `B` are
classified as follows:

| Class of pair | Count |
|---|---:|
| Negative discriminant | 566,826 |
| Unit roots in `E` | 133,378 |
| Two unit roots outside `E` | 585,434 |

The last row gives 140,110 ambient quadratic classes, hence 280,220
distinct unit multipliers. Projecting them to every anchor gives 4,163,154
nonempty anchor/class cases. Twice that number, 8,326,308, counts
anchor/root incidences; it does not count distinct multipliers, point sets,
or graph isomorphism types.

Every projected class has at most 26 new cross edges. This maximum is
attained at source anchors 10 and 11, namely `+/- i sqrt(3)/6`. The strict
outside-field graphs therefore have between 2,228 and 2,254 edges, where
the lower value includes placements with no new cross edge. The bound on
new cross edges does not concern the separate in-field branch.

Use the three proper `B` coloring rows from the fixed-Moser certificate
and the two proper `V` rows from the single-anchor certificate. The latter
also color the untranslated `V`, since its internal graph is unchanged.
Every internal unit edge is checked directly.

For anchor `q`, replace each right-component row `h(v)` by
`h(v) XOR h(q)`, a permutation of the four color labels sending the anchor
to 0. For each class try a `B` row, a `V` row, and one of the six color
permutations fixing 0. These 36 choices suffice for all 4,163,154 cases.
The integer verifier intersects their allowed-choice masks along every
cross edge, selects a surviving choice, and checks it on all edges in the
projection. The rational audit searches these choices explicitly.
Both find zero uncovered cases and exactly the same first witness stream.
The 1,309 bytes of component colorings are reused without additions;
no new SAT query is required.

Internal-edge validity, agreement at the origin, and validity on every
complete cross-edge projection prove proper four-colorability. Together
with the in-field and empty-projection cases, this proves the theorem.

## 5. Direct maximum-contact realizations and trust

For anchor `q=V[10]=i sqrt(3)/6`, a 26-contact class has polynomial

\[
U^2-\frac{-1+i\sqrt{11}}3U+\frac{-5-i\sqrt{11}}6=0.
\]

Both roots are

\[
u_\varepsilon=\frac{-1-\varepsilon\sqrt{22}
+i(\sqrt{11}-\varepsilon\sqrt2)}6,\qquad\varepsilon=\pm1.
\]

They have norm one and are outside `E`, as seen from the nonzero real
`sqrt(22)` coefficient in the linearly independent basis of
`Q(sqrt(2),sqrt(3),sqrt(11))`. The direct checker verifies their polynomial
and norm identities, then constructs all points of `B union u_epsilon(V-q)`
in this eight-element real radical basis at integer scale 72. It tests all
127,260 pairs per root and recovers exactly 505 distinct vertices,
1,251 plus 977 internal edges, and the 26 cross edges listed in
`maximum_example.json`. Both strict graphs have 2,254 edges, and an actual
four-coloring is directly checked. This uses the separate published
integer-radical helper, not either census or the complex-field module.

The integer census first matched the complete edge-partition hash of the
prior anchor-0 rational census. The full rational audit additionally checks
every pair classification, the entire ambient edge partition, every anchor
projection and coloring, and all per-anchor counts and histograms. These
are cross-checks by the author; no independent review of the present
strengthening is claimed. The imported field theorem and angular reduction
remain unformalized mathematics. Other trust boundaries are the pinned
inputs, exact Python programs, and ordinary software and hardware. No
approximate unit-distance decision or omitted large certificate is used.

The coordinate [provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md)
is Parts' archive accompanying
[the graph-minimization paper](https://arxiv.org/abs/2010.12665).
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4),
checked on 2026-09-05, still reports the 509-vertex benchmark. This result
is a family exclusion, not a record improvement or a priority claim for
the elementary quadratic and color-permutation methods.
