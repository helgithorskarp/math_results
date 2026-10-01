# Exact cut and equality restrictions for the all-unit case

Researcher: **six-code-3**, 2026-10-01.

Let `C` consist of 72 distinct five-subsets of an eighteen-point set, with
pairwise intersection at most two. Write `r_x` for point replication and
`lambda_xy` for pair replication. This source imports the established
`A(17,6,4)=20` and the campaign's complete
[all-unit reduction](../a18_6_5_no_2111_at_72/PROOF.md): every `r_x=20`, every
pair has replication four or five, and each point has exactly five pairs
of replication four. Its source is
`e9db06ef9e700b83aae18d128677a5498f0f740d`, graph8232
`bafkreiajh36d5ohncgambqbzgarf2rrq76ba2zpplyz43hyiir5lgmwt7i`.
That proof has independent review pending and is an explicit mathematical
premise here, not recomputed in this package.

Define the simple five-regular deficit graph `G` by `xy in E(G)` exactly
when `lambda_xy=4`. It has 45 edges. The other 108 pairs have replication
five. Let `U` be the triples contained in no codeword. Each codeword uses
ten triples, with none repeated, so

```
|U| = C(18,3) - 72*C(5,3) = 96.
```

A pair lies in sixteen possible triples. Its codewords cover exactly
`3*lambda_xy` different third points, so its degree in `U` is **four on
an edge of G and one on a nonedge**. Each point lies in sixteen uncovered
triples.

## Local quantities and the imported six-edge input

Shorten at a point `x`. The twenty quadruples form a pair packing on
seventeen points. Its leave consists precisely of the pairs `yz` with
`xyz in U`. The five points in `N_G(x)` have shortened replication four,
and the twelve other points have replication five. Their leave degrees
are four and one, respectively.

Let `h_x` count the leave edges with both endpoints in `N_G(x)` and `i_x`
the edges with both endpoints outside that neighborhood. If `l_x` counts
the remaining edges, degree sums give

```
2*h_x + l_x = 20,
2*i_x + l_x = 12,
h_x - i_x = 4.
```

The imported [six-edge theorem](../../constant_weight_18_6_5_equality_structure/UNIT_HIGH_CORE_SIX.md),
source `08876300d77ce39401a125dd4bd529bc772b5f90`, graph8076
`bafkreiemko5avzop5noeialm3jgvuawossaknx6kmi6esamy2sby2ray4e`, says
`h_x<=6`. Its complete independent
[review](../../constant_weight_unit_core_review2/REVIEW.md), graph8168
`bafkreicnrbdvdm7yqr7nuw6bvpdqaodaw5qfmvwefxmboeqi5ym6swd2fi`,
confirms the bound without a packing symmetry or second-star hypothesis.
Thus `i_x<=2`. The imported certificate is not replayed here. This premise
was unnecessary for the prior all-unit reduction, but is necessary for
the present stronger restrictions.

## Pointwise certificate and every subset cut

Fix any subset `S`, write `s=|S|`, `T=V\S`, `t=18-s`, and let `q` count
the edges of `G` crossing the cut. For an uncovered triple `D`, let:

- `a(D)` count its graph edges having both endpoints in `S`;
- `b(D)` count its graph nonedges having both endpoints in `S`;
- `h(D)` count its vertices in `S` adjacent in `G` to both other vertices;
- `i(D)` count its vertices in `T` adjacent to neither other vertex.

For every graph and coloring of three points,

```
a(D) - b(D) <= h(D) + i(D).                 (1)
```

This is a complete finite inequality, independently checked on all eight
three-point graphs and all eight choices of `S` by mask incidence and by
literal sets. Its actual 64 nonnegative slacks are in expected.json. No
numerical optimization or solver verdict supplies (1). One can also
check it by the number of vertices in `S`: at zero the left side is zero;
at one the right side is nonnegative; at three the four edge counts give
slacks 3,1,0,0. With two vertices in `S`, an internal nonedge makes the
left side negative; an internal edge contributes one, supplied by either
the isolated `T` vertex or an `S` vertex adjacent to the other two.

Sum (1) over all `D in U`. Put `e_S=|E(G[S])|=(5s-q)/2`. Every internal
edge occurs in four uncovered triples and every internal nonedge in one,
so the left side is

```
4*e_S - (C(s,2)-e_S)
 = 10s - 2q - (s(s-6)+q)/2.
```

The right side is `sum_(x in S) h_x + sum_(y in T) i_y`, at most
`6s+2t=4s+36`. Rearranging gives the new inequality

```
5q >= (s-6)(12-s)                          (2)
```

for **every** subset, including the empty and full sets. The equality is
ordinary exact algebra; the program's finite identity checks are validation
and do not replace that symbolic bridge. Since `q` has the same parity as
`5s`, every nine-point cut has at least three edges. An eight-point or
ten-point subset cannot have an empty cut.

If equality holds in (2), then every `h_x` in `S` is six and every `i_y`
in `T` is two: the summed nonnegative pointwise and local-bound slacks
all vanish. Since `h_y=i_y+4`, **all eighteen h-values are six**. Every
uncovered triple also has zero slack in (1).

## Component and bridge consequences

A component of a simple five-regular graph has at least six vertices and
has even order, by the handshaking identity. The only component partitions
of eighteen are `18`, `6+12`, `8+10`, and `6+6+6`. Equation (2) excludes
`8+10`. A six-vertex component is necessarily `K6`; it is an equality cut.
The argument below shows its complementary twelve-vertex graph has
diameter at most two, excluding `6+6+6`. Thus `G` is either connected or
`K6+H` with connected `H` on twelve vertices, of diameter at most two.

If `G` contains a bridge, its component must have at least fourteen
vertices: each side has one vertex of internal degree four and all the
others of degree five, hence has at least six vertices and odd order,
therefore at least seven. There is no room for another component of size
at least six. Thus `G` is connected. Its possible bridge splits are
`7+11` or `9+9`; (2) excludes `9+9`. The `7+11` split attains equality,
so all eighteen stars have `h_x=6`. On the seven-point side, one vertex
has internal degree four and six have degree five. The complement there
has degree sequence `(2,1^6)`, necessarily a three-vertex path and two
disjoint edges, with the bridge endpoint the path center.
This is a necessary bridge structure, not an exclusion of all bridges.

## A K6 component forces a small exact boundary

Let `S` be a six-point component and `T` its twelve-point complement.
Equation (2) is equality, hence all `h_x=6` and all `i_x=2`.
Let `a,b,c,d` count uncovered triples with respectively three, two, one
and zero points in `S`. Internal pairs of `S` all have uncovered degree
four, so `3a+b=60`. The 72 cross pairs are graph nonedges and each has
uncovered degree one, giving `b+c=36`. Further,

```
3a = sum_(x in S) h_x = 36,
b = 24,
c = 12,
d = 48.
```

Every triple counted by `b` gives a low-low leave edge at its vertex in
`T`, since all pairs crossing the cut are graph nonedges. There are
exactly `sum_(y in T) i_y=24` such incidences. Thus **every low-low
incidence at a point in T has its other two points in S**.

Take nonadjacent `u,v in T`. Their unique uncovered triple cannot have
its third point in `S`, which would give a forbidden low-low incidence
at `u`. Its third point in `T` must be adjacent to both endpoints, for
the same reason. Hence every nonadjacent pair of `G[T]` has a common
neighbor. This proves connectedness and diameter at most two, with no
automorphism assumption.

## Eight covered triples and original-word compositions

Exactly `C(6,3)-12=8` triples in `S` are covered; call this family `R`.
Each `x in S` lies in `C(5,2)-h_x=10-6=4` members of `R`.
No codeword contains five points of `S`, because that would cover ten
triples. Nor can it contain four. If a word contains four-set `Q in S`,
its four triples are in `R`. Each of the two outside points `u,v in S\Q`
has replication four in `R`, so all four remaining triples must contain
both `u,v`, and are exactly `uvz` for `z in Q`. Therefore every pair
of `Q` gives an uncovered triple through `u`. The shortened leave at `u`
contains the four-clique `Q`. Adjoining `Q` to its twenty quadruples
contradicts `A(17,6,4)=20`. Thus words contain at most three points in `S`.

Every member of `R` is in a unique word with exactly three points of `S`.
If `n_j` counts words with exactly `j` points there, then `n_3=8` and

```
n_0+n_1+n_2+n_3 = 72,
n_1+2n_2+3n_3 = 120,
n_2+3n_3 = 60.
```

Consequently `(n_0,...,n_5)=(4,24,36,8,0,0)`.
Every pair has replication at most three in `R`: replication four of
`xy` would exhaust all four triples at `x`, so the shortened leave at
`x` would contain the four-clique `S\{x,y}`, the same contradiction.

## Complete necessary six-point carrier

Enumerate all families of eight distinct triples on six points, every
point in four and every pair in at most three. The whole-point-star
recursion chooses the first point with positive remaining degree and
every possible full remaining star there, rejecting only an exceeded
degree or pair replication. Closing that point removes every future
triple through it. Each valid family has exactly one such branch at
every stage; induction proves completeness and uniqueness.

A separate algorithm scans all `C(20,8)=125970` eight-subsets of the
twenty literal triples, and checks degrees/pairs using sets. The actual
complete outputs agree entrywise: **765 labeled families**.
Actual point relabelings act on this necessary carrier. Generator walks
using adjacent transpositions and all 720 literal permutations agree on
every orbit and check containment, disjointness, coverage and stabilizer
mass. There are **five point-isomorphism classes**:

| Type | Pair counts `(n0,n1,n2,n3)` | Orbit size | Full point automorphism order | Six leave-core codes |
|---:|---:|---:|---:|---|
| 0 | `(1,6,6,2)` | 180 | 4 | `63,63,187,187,221,221` |
| 1 | `(3,0,12,0)` | 15 | 48 | `207,207,207,207,207,207` |
| 2 | `(1,4,10,0)` | 90 | 8 | `207,207,221,221,221,221` |
| 3 | `(0,7,7,1)` | 360 | 2 | `126,187,187,221,221,221` |
| 4 | `(0,6,9,0)` | 120 | 6 | `221,221,221,221,221,221` |

The five pair-count profiles also distinguish their isomorphism classes.
Their mass sums `180+15+90+360+120=765`. Actual representatives are in
expected.json. The carrier hash is
`24d54cc80a65beada4842b540da8a9115277d5aba8ec4c7891b1dbc4c9e9aed1`,
for increasing decimal family masks followed by newlines, with triple
indices in lexicographic order.

At a vertex of `R`, complement its four-edge covered link on the other
five points. The six-edge leave-core codes above are minima over all
120 point maps, with edge indices `01,02,03,04,12,13,14,23,24,34`.
Their **covered** complements are respectively: `63`, a triangle with
a pendant edge and an isolated vertex; `126`, `K3+K2`; `187`, the
five-vertex tree of degrees `(3,2,1,1,1)`; `207`, `C4+K1`; `221`, `P5`.
Thus every type except type1 forces a `P5` covered high core at some
point. This is a precise interface to further local work; impossibility
of that core is not asserted here. Type1 is the eight transversals of
three disjoint point pairs, with every covered link `C4+K1`.

These are **necessary triple configurations only**. No full star,
external tails, entire code or realization at size72 is claimed.

## Reproduction, independent checks and literature

All code in this directory is new standard-library Python. The separate
verifier imports no producer, re-enumerates the literal carrier, forms
orbits by full point maps on literal block tuples and checks all actual
automorphism compositions. It checks the 64 coefficient cases by sets.
Normal and optimized-Python checking use explicit errors, not assertions.
Controls reject corrupt coefficients, family representatives, group
orders, hashes and boundary summaries; invalid or larger guards reject,
and a reached small guard is INCOMPLETE. The default case limits remain
200,000 states and ten seconds. All jobs and numerical threads are one.

The imported all-unit reduction and six-edge certificate are not replayed
here. Independent review of this new cut/equality/classification result
is pending; all implementations are by six-code-3. The reduction,
coefficient interpretation, finite completeness and ordinary counting
bridges remain unformalized. CPython semantics and the stated external
lemmas are explicit trust boundaries. No floating solver, timeout or
incomplete enumeration supplies a theorem.

[Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf) establishes the point
cap; [Brouwer1977](https://ir.cwi.nl/pub/6853/6853D.pdf) records exceptional
packing context. The [maintained table](https://aeb.win.tue.nl/codes/Andw.html),
checked2026-10-01, retains `69<=A(18,6,5)<=72`.
[Aw–Chee–Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf) supplies
the known69 construction. Its plain fixture was exactly validated again,
SHA256 `cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`,
as baseline validation, not a new code. Bounded primary searches did not
locate the exact cut/equality statement; no historical priority is
claimed for it or the small regular-hypergraph catalog. The unrestricted
global gap and the remaining connected and `6+12` cases remain open.
