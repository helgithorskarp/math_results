# Every overlap at the fixed rotation (7+i sqrt(15))/8 is four-colourable

Let `A159,V214` be the exact archived vertex sets in
[the source package](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md), and set

\[
\nu=(5+i\sqrt{11})/6,\quad B=A159\cup\nu A159,
\quad u=(7+i\sqrt{15})/8.
\]

**Theorem (exact computer-assisted finite-family closure).** For every
`h in C` such that `B` and `u V214+h` intersect, their entire strict
Euclidean unit-distance graph is four-colourable. There are exactly
62,488 such translations; each union has exactly 505 vertices.
The statement also covers `u bar(V214)+h`, since `bar(V214)=V214`.

The rotation is fixed. Disjoint translations at this rotation, other
rotations, other inner constructions, and the sealed Parts pool are
outside this theorem. No five-chromatic graph or record improvement is
obtained. This is a different fixed angle from the preceding
[all-translation closure](../hadwiger_nelson_mixed506_fixed_rotation/PROOF.md).
The [all-angle origin theorem](../hadwiger_nelson_mixed505_all_gadget_anchors/PROOF.md)
and [high-degree attachment theorem](../hadwiger_nelson_mixed505_high_degree_attachments/PROOF.md)
cover only three particular inner anchors. Here every inner anchor is used.

## 1. Coordinates and the complete translation list

Write

\[
E=\mathbb Q(\alpha,\beta),\quad \alpha=i\sqrt3,\quad\beta=i\sqrt{11},
\qquad R=\mathbb Q(\sqrt{33}).
\]

The integer tuple `(a,b,c,d)` represents
`(a+b sqrt(33)+c alpha+d beta)/72`. The exact source construction gives
292 distinct vertices and 1,251 strict edges in `B`, and 214 distinct
vertices and 977 strict edges in `V214`. The latter's original denominator
12 is converted to 72. Both graphs and all stored colourings are checked.
The independent audit reconstructs the sources with generic radical
multiplication; its second source is translated by its first vertex,
which changes no differences, labels, or family membership.

The quadratic subfields of the biquadratic field `E` are
`Q(sqrt(-3)), Q(sqrt(-11)), Q(sqrt(33))`. Thus `sqrt(5)` is not in `E`.
Since `u=(7+alpha sqrt(5))/8`, we have `u notin E` and `E(u)=E(sqrt(5))`.
Also `u bar(u)=1`.

If source vertices `B[m]` and `V[n]` coincide after placement, then

\[
h=B[m]-uV[n].\tag{1}
\]

If two distinct anchor pairs gave the same translation, subtraction would
give `B[m]-B[m']=u(V[n]-V[n'])`. A nonzero right difference forces `u in E`;
a zero difference forces both labels equal. Hence the 292 times 214
translations (1) are distinct, and each has exactly one overlapping
physical vertex. This proves the finite reduction and the order 505.
No bound on a translation's size or denominator is imposed.

## 2. Exact classification of every new cross edge

At the placement (1), consider endpoints `p=B[i]` and `uV[j]+h`, and put
`x=B[i]-B[m]`, `y=V[j]-V[n]`. Their difference is `x-u y`. A cross pair
with `x=0` or `y=0` is a unit edge already inherited from one source at the
shared vertex. It is properly coloured once the two anchor colours agree.
Only `x,y` both nonzero can introduce a new edge.

For `c=bar(x)y`, expansion in the quadratic extension `E(sqrt(5))` gives

\[
N(x-u y)=N(x)+N(y)-\frac78(c+\bar c)
             -\frac{\alpha\sqrt5}{8}(c-\bar c).
\]

The coefficient of `sqrt(5)` vanishes exactly when `c=bar(c)`. This is
Euclidean parallelism of `x,y` and is equivalent to `x/y in R`. Consequently

\[
N(x-u y)=1
\quad\Longleftrightarrow\quad
\bar x y\in R\ \text{ and }\ 4N(x)+4N(y)-7\bar x y=4.\tag{2}
\]

This equivalence is exact, including antiparallel displacements.

To enumerate parallel pairs, use unscaled numerator coordinates
`X=(a,b,c,d)`, so that

\[
X=(a+b\sqrt{33})+\frac\alpha3(3c+d\sqrt{33}).
\]

If `a=b=0`, assign the imaginary-axis key `(0,)`. Otherwise the ratio of
the alpha coefficient to the real part is represented by

\[
\frac{3ac-33bd+(ad-3bc)\sqrt{33}}{3(a^2-33b^2)}.\tag{3}
\]

Store the denominator and two numerators after dividing by their common
gcd and making the denominator positive. The denominator is nonzero
because `sqrt(33)` is irrational. Two nonzero vectors have the same key
if and only if they are parallel over `R`. In particular both signs of a
real or imaginary axis are included.

There are 17,336 distinct nonzero `B` differences and 4,418 distinct
nonzero `V` differences. Of their 76,590,448 ordered pairs, exactly
64,352 have equal keys. For each, `c=bar(x)y` is real; its two numerator
coefficients for `X=(a,b,c,d)`, `Y=(A,H,C,D)` are

\[
(aA+33bH+3cC+11dD,\ aH+bA+cD+dC).
\]

The norm numerator of `X` is
`(a^2+33b^2+3c^2+11d^2, 2(ab+cd))`. The second test in (2), multiplied by
`72^2`, is an equality of these two integer coefficients. It leaves
exactly **66** difference pairs, listed in [contacts.tsv](contacts.tsv).
Thirty have `x=y`, `N(x)=4`. The remaining 36 split equally between the
ordered norm pairs `((17+sqrt(33))/6,(17-sqrt(33))/6)` and the reverse.
These norm counts describe this finite source census, not a general
classification of solutions to (2).

For every retained difference pair, enumerate every incidence
`B[i]-B[m]=x` and `V[j]-V[n]=y`, and add the cross edge `(i,j)` to placement
`(m,n)`. Conversely every new cross edge at every overlap placement has
one of these incidences, by (2). There is no symmetry quotient or omitted
anchor. No projected edge is duplicated. The complete histogram is:

| New cross edges | Overlap translations |
|---:|---:|
| 0 | 55,972 |
| 1 | 4,339 |
| 2 | 1,417 |
| 3 | 431 |
| 4 | 136 |
| 5 | 120 |
| 6 | 73 |
| Total | 62,488 |

These are distinct translations with labelled source anchors, not distinct
graph isomorphism classes.

## 3. Positive four-colouring certificates

Use ten proper colourings of `B` and nine of `V`, each with values in
`{0,1,2,3}`. The first eight and seven rows respectively are inherited
from the earlier construction and high-degree attachment packages. This
package supplies two additional rows per source in `new_B.txt` and
`new_V.txt`. Every row is checked against every strict source edge.

For each placement `(m,n)`, enumerate source rows `b,v` and permutations
`pi` of four colours. Select a triple satisfying

\[
b[m]=\pi(v[n]),\qquad b[i]\ne\pi(v[j])
\quad\text{for every new cross edge }(i,j).\tag{4}
\]

The first equality gives a well-defined colour at the shared vertex.
All inherited edges are proper by the component checks, and all new edges
are proper by (4). Thus the selected triple certifies the entire strict
505-vertex graph. The verifier finds and checks such a triple for all
62,488 placements. It hashes the complete ordered placement/edge/witness
stream, not merely its histogram.

The original three/two-row library leaves 858 placements uncovered, and
the inherited eight/seven-row library leaves 82. These mean failure of a
specified library, not non-four-colourability. Two satisfiable colouring
queries, at anchors `(119,169)` and `(79,167)`, produced the additional
rows. Their strict graphs have respectively 2,234 and 2,233 edges. The
final ten/nine-row library leaves zero residuals. No minimality of the
colouring library is asserted.

## 4. Independent all-pairs geometric audit

The audit uses neither (3) nor the producer's arithmetic or incidence
construction. It obtains the source sets from independently pinned generic
radical arithmetic, builds difference sets directly, and scans **every one
of the 76,590,448 difference pairs** using actual rotated Cartesian
coordinates in finite fields.

All relevant coordinates lie in
`Z[1/2,1/3,sqrt(3),sqrt(5),sqrt(11)]`. The audit evaluates this ring using

| Prime | sqrt(3) | sqrt(5) | sqrt(11) |
|---:|---:|---:|---:|
| 1321 | 321 | 416 | 501 |
| 5281 | 1302 | 325 | 1874 |

It checks primality and each root identity. Denominators 72 and 8 are
invertible. Hence an exact unit squared distance must be one in both
finite fields. These are maps from the coordinate ring, not from a whole
characteristic-zero field.

The first field retains 58,696 pairs; the second leaves 80. The audit
then forms `8X-(7+i sqrt(15))Y` using generic multiplication in the
eight-dimensional real radical ring with basis
`sqrt(3)^e sqrt(5)^f sqrt(11)^g`, exponents zero or one. It tests whether
the exact squared norm is `576^2`. Exactly 66 pass. Fourteen two-prime
survivors are therefore rejected exactly; passing modular tests alone is
never treated as proof of a unit distance.

The full 66-pair stream equals the producer's stream. Independent endpoint
lookups reconstruct every projected edge list. Their complete stream
matches, as do all selected colourings, all 62,488 placements, and the
histogram. This supplies a different completeness computation from the
real-subfield slope partition.

The controls separately construct the two former residual graphs as
505 distinct generic-radical points. All 127,260 physical point pairs in
each are tested exactly. The resulting strict edge lists agree with the
finite reduction, the old library fails, and the newly generated positive
colouring is proper on every edge. Altering one endpoint colour to violate
an edge is rejected. Additional controls check the exact contact `x=y=2`,
the non-contact `x=y=1`, and projective axis and sign normalization.

## 5. Reproducibility, trust and scope

The [README](README.md) gives replay commands, versions and measured costs.
`expected.json`, `expected_audit.json`, `expected_controls.json` and
`SHA256SUMS` preserve compact evidence and dependency pins. No large search
trace, binary, private state or dataset is needed.

The optional generator uses CaDiCaL195 through `python-sat==1.8.dev24`,
with at most twenty queries and 200,000 conflicts per query. It stops and
preserves a local candidate on any non-SAT answer. Variables `X[v,c]`
encode exactly one of four colours at each of 505 physical vertices, with
one negative binary clause per edge and colour. The shared vertex's
colour is fixed to zero, a sound global colour symmetry. Only explicit
positive assignments are used. Source-normalized rows are extracted and
rechecked. The two observed queries have 2,020 variables and 12,472/12,468
clauses. Their compact provenance is in `solver_provenance.json`; the
ordinary proof replay needs no solver and trusts no UNSAT answer.

These audits are independent author implementations, not external peer
review or proof-assistant formalization. The trust boundary consists of
the exact archived coordinate data, the unformalized field and finite
reduction above, completeness of the finite programs, checked positive
colourings, and ordinary Python integer execution. No floating-point
equality, probabilistic coverage estimate, 2-adic rule, or sealed-family
solver result enters this theorem.

Primary record context remains Parts,
[Graph minimization](https://arxiv.org/abs/2010.12665), and the 509-vertex
benchmark stated in [Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4),
checked on 2026-09-05. No novelty priority is claimed. The remaining
geometric frontier at this angle is **disjoint** placement; it has not
been enumerated in this pass.
