# Complete first-step triple-neighbour support of the dense506 hosts

**Status: exact computer-assisted exclusion theorem.** For each of the two
specified 506-point embeddings below, the previously published fixed
four-colouring extends simultaneously to every nonhost point having at least
three unit neighbours in the host. The resulting strict unit-distance graph
has **1,926 vertices and 12,074 edges** and is four-colourable. Consequently
all subgraphs of this finite support are four-colourable, without an order
restriction. This closes every deletion/addition repair confined to this
support, including all one-deletion/three-candidate repairs of order 508.

This does not exclude arbitrary three-point additions, another relative
placement, or a second round of completion. No graph improving 509 is
constructed.

## Exact hosts and imported finite census

Use the pinned Parts coordinate tables A of order 159 and V of order 214,
with the original source row order. Set

\[
 \alpha=i\sqrt3,\quad z=\sqrt{33},\quad\beta=\alpha z/3=i\sqrt{11},
 \quad r=\sqrt{-408+72z}>0,
\]
\[
 t=(5+z+5\alpha-\beta)/12,\qquad B=A\cup(\overline A+t),
\]
\[
 u_\pm=\frac{-18-6z-30\alpha+6\alpha z
                  \pm r(3+6\alpha+\alpha z)}{72},
 \qquad H_\pm=B\cup u_\pm(V-V[10]).
\]

Here V[10]=alpha/6. B has 293 vertices; H_plus and H_minus each have
506 distinct vertices and 2,389 strict unit edges. Their exact geometry,
labelling and fixed colouring are established in the
[two-point extension package](../hadwiger_nelson_dense506_two_point_extension/PROOF.md),
source commit `dc57db82a86037be322374b20b31a65fb73df452`, and checked by the
[independent review](../hadwiger_nelson_dense506_two_point_extension_review1/README.md),
review source commit `de9cd586d128b12df93d3fdb228d573fe373575c`.

For a finite plane set H define

\[
 C_3(H)=\{p\notin H:|\{h\in H:|p-h|=1\}|\geq3\},\qquad
 U_3(H)=H\cup C_3(H).
\]

Three distinct points on a unit circle are noncollinear and determine its
centre uniquely. Thus C_3(H) is precisely the set of external centres of
host triples with unit circumradius. This reduces an unrestricted Euclidean
condition to a finite enumeration, without a preselected coordinate grid.
The cited census exhausts all 21,464,520 triples of H_plus and proves:

| Quantity | Exact value |
|---|---:|
| Host-centred unit-circle triples | 93,131 |
| External-centred unit-circle triples | 10,517 |
| Distinct points of C_3(H_plus) | 1,420 |
| H_plus to C_3(H_plus) unit edges | 5,710 |
| Unit edges inside C_3(H_plus) | 3,975 |

The graph on U_3(H_plus) therefore has 506+1420=1926 vertices and
2389+5710+3975=12074 edges. The automorphism sigma:r->-r of
Q(z,r,alpha), fixing z and alpha, commutes with complex conjugation and
preserves squared-distance equalities. It maps H_plus to H_minus and maps
the complete candidate set label by label. The same labelled unit graph
and colour certificate apply to both embeddings. The present audit also
reconstructs both full graphs directly.

Host labels are 0 through 505 as in the cited source. Candidate labels are
0 through 1419 in lexicographic order of the canonical integer tuple

\[
(d,X_1,X_z,X_r,X_{zr},Y_1,Y_z,Y_r,Y_{zr}),
\]

representing

\[
 \frac{X_1+X_zz+X_rr+X_{zr}zr+
        \alpha(Y_1+Y_zz+Y_rr+Y_{zr}zr)}{d}.
\]

Here d is positive and the nine entries have gcd one. Candidate j has
full-graph label 506+j. For H_minus use sigma on each labelled coordinate;
do not sort the conjugated points again.

## Constructing the simultaneous extension

Keep the fixed host colouring c from the cited two-point theorem. For each
candidate p let L(p) be the colours in {0,1,2,3} absent from its host
neighbours. There are initially 941 singleton lists, 461 lists of size two,
and 18 of size three. Unlike pair-by-pair extension, we now colour the
entire candidate graph at once.

Whenever L(p)={a}, every extension must colour p with a. Remove a from every
candidate neighbour's list and repeat. No list becomes empty. This process
forces 426 additional vertices, leaving 1,367 singleton lists, 38 doubleton
lists and 15 tripleton lists. A deterministic queue implementation performs
429 individual colour removals. Independently applying the rule in
synchronous rounds gives singleton totals 1,293, 1,356 and 1,367, then
stabilizes.

The graph induced by the 53 nonsingleton vertices is a forest. Its seven
edges, in candidate labels, are

```
941 1190       949 967        1072 1144
1130 1171      1130 1183      1162 1183      1163 1192
```

There are 41 isolated vertices, four two-vertex components, and one
four-vertex path. A forest with lists of size at least two is list-colourable:
root each tree, choose any permitted root colour, and colour children in
root-to-leaf order while avoiding their parent's colour. At least one
choice remains at every step. All conflicts with forced vertices were
removed during propagation. The forced vertices themselves have no
monochromatic edge, since that would have emptied a list. This proves the
extension criterion used here.

The [deterministic constructor](construct.py) orders roots and neighbours by
label and always chooses the least permitted colour. It produces the
[complete colouring](colors.txt), a single row of 1,926 digits followed by a
newline, with colour class sizes 522, 460, 476 and 468. Every geometric unit
edge is checked directly against this row. Thus the theorem does not rely
on solver soundness, propagation completeness or an optimality claim.

Colour-file SHA-256:
`1851be3b084aba56c0ec2910bdd4769b706d36c4ce8756b38d0c6726ca973a0b`.
The lexicographically sorted full edge list, serialized as compact JSON
without a trailing newline, has SHA-256
`eed323973fe213bef63a30f24d71eea1da4bca390d751e0a52afe4b09a7dff53`.

## Consequences for geometric repair

**Deletion and completion closure.** Every subset of U_3(H_plus) or
U_3(H_minus), with any subset of its unit edges, is four-colourable by
restriction. In fact, for every S subset of H, U_3(S) is contained in
U_3(H): any external point with three neighbours in S either already lies
in H or has three neighbours in H. Hence completing any subset of either
host in one step using all its triple-neighbour points is also
four-colourable. This statement permits any number of deletions and added
points, within this single-step rule.

**Necessary escape condition.** If a non-four-colourable graph uses some
vertices of H and other plane points, at least one of those new points has
at most two unit neighbours in the original H. Otherwise the entire graph
would be contained in U_3(H).

For a proposed repair (H minus {h}) union {p,q,s}, where p,q,s are distinct
and outside H, this condition can be sharpened. If the repaired graph were
non-four-colourable, choose a vertex-minimal non-four-colourable subgraph J.
It has minimum degree at least four: a vertex of degree at most three can
be deleted, and a four-colouring of the smaller graph extended greedily.
Every one of p,q,s belongs to J, because the cited two-point theorem colours
H with any at most two arbitrary new points. An added point x having at
most two neighbours in H therefore must have exactly two, neither equal
to the deleted h, and must be adjacent to both other new points. Its degree
in J is exactly four. At least one such point must occur. This is a
necessary condition, not a construction or an exclusion of all such repairs.
Every added vertex of J has at least two neighbours in H, since it has
at most two added neighbours. Hence the remaining one-deletion/three-point
family has a finite complete candidate universe

\[
 C_2(H)=\{x\notin H:|N_H(x)|\geq2\},\qquad
 |C_2(H)|\leq2\binom{506}{2}=255530.
\]

Indeed, each such point is an intersection of two unit circles centred
at distinct host vertices, and each pair of circles has at most two
intersections. At least one of the three added points must lie in
C_2(H) minus C_3(H). These intersections may leave the degree-eight field
used by C_3(H); no field restriction is justified here. This finite bound
and necessary condition specify a possible next search. No C_2 enumeration
or search of this remaining geometry was started here.

## Verification and trust boundary

[verify.py](verify.py) checks pinned input identities, rebuilds host edges,
reconstructs the colour lists, regenerates the deterministic colouring,
and checks every listed edge. [audit.py](audit.py) imports the pinned
independent reviewer's quotient-ring arithmetic, not the primary geometry
module. For each root it checks all 1,853,775 unordered point pairs with the
modular image p=5051,z=2194,r=528, resolving every survivor by exact integer
norm arithmetic. There are respectively 12,221 and 12,190 survivors; both
exact graphs have 12,074 edges and identical labelled edge lists. All host,
cross and candidate adjacency lists match entry by entry. The audit derives
lists as sets, propagates synchronously, and verifies the residual forest
by repeated leaf deletion rather than the constructor's tree traversal.

This pass regenerates the complete candidate table with the prior public
producer. Its completeness theorem and independent exhaustive review are
imported dependencies; the present audit does not perform another full
host-triple scan. Arithmetic decisions are exact and use no floating point.
The residue map is a rejection filter only: a unit-distance equality must
vanish modulo the prime, and every survivor is checked in the number field.
All current denominators are invertible modulo that prime; the imported
checker rejects any noninvertible denominator instead of silently skipping it.

The new audit is an author-run check using independently derived published
arithmetic. It is not a new external review of this contribution. Residual
trust consists of the imported completeness proof and coordinate data,
CPython integer semantics, hashes for identity, and ordinary unformalized
mathematics/code. The source gadgets' advertised chromatic or forcing
properties are not needed for this colouring theorem.
