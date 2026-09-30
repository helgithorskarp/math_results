# At most six leave edges among five replication-four points

Researcher: **six-code-1**, 2026-09-30.

**Computer-assisted theorem.** Let `Q` consist of twenty distinct four-subsets
of a seventeen-element set, with every pair in at most one member. Suppose
exactly five points have replication four and the other twelve have replication
five. Let `H` be the five replication-four points, and let `L` be the graph of
pairs in no member of `Q`. Then

\[
                         |E(L[H])|\leq 6.
\]

This strengthens the preceding [bound of seven](UNIT_HIGH_CORE.md).
No automorphism, second-star, completion, or ambient-code hypothesis is imposed.
Sharpness of six is not established here. The new part excludes **all three**
four-clique-free seven-edge high cores, including both block branches of one
core. The unrestricted interval for `A(18,6,5)` remains **69–72**.

For the coding application, remove a point `u` of replication twenty from each
codeword containing it. Its shortened quadruples satisfy the pair-packing
hypothesis, since two original words intersect in at most two points. Write
`d[u,x]` for pair multiplicity and `t[u,x]=5-d[u,x]`. If the positive deficit
row at `u` is `(1^5)`, its five deficient neighbors have shortened replication
four and the other twelve have replication five. Thus at most six uncovered
triples through `u` have both other points among its deficient neighbors.
This necessary condition applies to every such star, including in codes of
size below seventy-two.

The complementary [mixed-star result by six-code-3](../coding_theory/a18_6_5_no_221_at_72/PROOF.md)
excludes every `(2,2,1)` row at size seventy-two. With the prior
[minimum-pair-three result](NO_DEFICIT_THREE.md), this leaves only rows
`(2,1,1,1)` and `(1^5)`. That remaining-frontier description is cited as
context; neither result is a premise of the local theorem proved here.

## Ordinary reduction to three leaves and four branches

A point of replication `rho` has leave degree `16-3*rho`. The high points have
degree four and the low points degree one. There are sixteen leave edges.
Brouwer's established `A(17,6,4)=20` implies that the leave of any twenty-block
packing contains no four-clique: its four vertices could otherwise be adjoined
as a twenty-first quadruple. The preceding bound-of-seven theorem uses this
fact and its complete eight-edge obstruction. It remains a dependency of the
present strengthening; that obstruction is not asserted anew.

Suppose now that `L[H]` has seven edges. Its complementary graph `C` of covered
high pairs has three edges. A three-edge graph on five vertices is one of
`K3+2K1`, `P4+K1`, `P3+K2`, or `K1,3+K1`. In the last case the isolated point
and the three leaves induce a four-clique in `L[H]`, so it is impossible.
This classification can also be checked by considering whether three edges
contain a cycle, have a vertex of degree three, or have maximum degree two.

Label `H={0,1,2,3,4}` and the twelve low points `5,...,16`. Every high vertex
`h` has `deg_C(h)` attached low leave neighbors, since it has total leave
degree four and `4-deg_C(h)` high leave neighbors. All attached low points
are distinct because their leave degree is one. There are exactly six of
them, denoted `S`. The six remaining low points form three matching edges.
Thus each covered high graph determines the entire leave up to relabeling:

| Model | Covered high pairs | Attached low leave neighbors | Low matching edges |
|---|---|---|---|
| Triangle | `01,02,12` | `0:5,6; 1:7,8; 2:9,10` | `11–12,13–14,15–16` |
| Path | `01,12,23` | `0:5; 1:6,7; 2:8,9; 3:10` | `11–12,13–14,15–16` |
| Wedge and edge | `01,12,34` | `0:5; 1:6,7; 2:8; 3:9; 4:10` | `11–12,13–14,15–16` |

Here `01` means `{0,1}`. In every row the high leave edges are the seven pairs
not in the second column, and `S={5,...,10}`. These are three universal local
cases, not three symmetry classes of ambient codes.

Let `b_j` count quadruples with exactly `j` high points. There can be no
quadruple with four high points. Every covered high pair occurs once, so

\[
 b_2+3b_3=3,\qquad b_1+2b_2+3b_3=20,
 \qquad b_0+b_1+b_2+b_3=20.
\]

There are only two possibilities. The **double-high branch** has three
double-high, fourteen single-high and three zero-high quadruples. It applies
to all three models. The **triple-high branch** has one triple-high, seventeen
single-high and two zero-high quadruples. It applies only to the triangle
model, since a triple of high points must have all three high pairs covered.

For a low point `x`, let `n_j(x)` count its occurrences in blocks with `j`
high points. Replication and covered high-pair counts give

\[
 \sum_j n_j(x)=5,\qquad \sum_j jn_j(x)=5-\mathbf1_{x\in S},
 \qquad n_0(x)-\sum_{j\geq2}(j-1)n_j(x)=\mathbf1_{x\in S}.       \tag{1}
\]

In the double-high branch, choose the two low tail points of the block on
each of the three covered high pairs. Allow **all twelve** low points;
retain exactly the triples of quadruples avoiding the leave and with disjoint
pair sets. In particular, tails belonging to disjoint high edges may share
one low point. No unsupported disjointness simplification is made.
Equation (1) then specifies the complete low-point incidence multiset of the
three zero-high blocks: it is one copy of each point of `S`, plus every low
tail occurrence. Its total multiplicity is twelve. Enumerate every three
low quadruples with exactly this multiset, avoiding the leave and previously
used pairs, and with pairwise disjoint pair sets. These six fixed quadruples
exhaust every block that has zero or at least two high points.

In the triple-high branch the fixed triple is `012x`. If `x` were attached,
equation (1) would require three zero-high incidences at `x`, but there are
only two zero-high blocks. Hence `x` is matched. It belongs to both zero-high
blocks, and those blocks partition the six attached points into two triples.
There are six choices for `x` and ten unordered partitions, giving sixty
raw three-block prefixes. The remaining blocks all have one high point.

## Complete finite certificate

The full groups of actual leave permutations have orders 4608, 384 and 384.
The low matching contributes `3! * 2^3 = 48` maps. The triangle model has
`3! * 2 = 12` high maps and `2^3 = 8` attached-leaf maps. The path model has
two high maps and four attached-leaf maps. The wedge-and-edge model has four
high maps and two attached-leaf maps. These exhaust the groups: leave degrees
distinguish high and low points; having a high leave neighbor distinguishes
attached from matched low points; a high map must preserve `C`; each attached
fiber follows its high neighbor; and the low matching is preserved.
Every generated map is separately checked on the actual sixteen-edge leave.

First quotient all double-high tail triples by the full leave group. Then
quotient all legal zero-high block triples by the **stabilizer of that tail**.
The implementations explicitly form every orbit, check containment in its
raw carrier, check disjoint coverage and the orbit-stabilizer equation, and
sum its orbit sizes. A tail orbit of size `n` with `z` compatible zero-block
frames represents exactly `n*z` raw joint prefixes, by relabeling transport.
This proves the two-stage quotient covers every labeled prefix and makes no
automorphism assumption on a packing. The triple-high branch is quotiented
directly by the same actual leave group.

| Model and branch | Raw tail triples | Tail orbits | Raw fixed prefixes | Prefix orbits | Residual pairs | Columns, range | Rejection nodes |
|---|---:|---:|---:|---:|---:|---:|---:|
| Triangle, triple | — | — | 60 | 2 | 102 | 360–370 | 2382 |
| Triangle, double | 4645 | 17 | 289440 | 205 | 84 | 88–174 | 578 |
| Path, double | 11185 | 117 | 412320 | 1486 | 84 | 76–176 | 3938 |
| Wedge and edge, double | 28272 | 299 | 566880 | 1995 | 84 | 66–166 | 5245 |
| Total | | | 1268700 | 3688 | | | 12143 |

Remove all pairs in the fixed prefix and all leave pairs from the 136 pairs.
A residual column is any quadruple containing exactly one high point whose
six pairs are still present. A cover of these rows is exactly a completion
by the remaining fourteen or seventeen single-high blocks, by the proved
block counts. Conversely any packing with the selected leave must give such
a cover for one of the represented prefixes.

At each rejection-tree node the certificate selects an uncovered pair and
includes a child for **every** compatible column containing it. Each child
removes that column's six pairs. A terminal node has an uncovered pivot with
no compatible column. Reaching an empty set of pairs would instead exhibit
a positive cover and is explicitly rejected by the verifier. Every one of
the 3688 trees is complete. The maximum tree has 1761 nodes. Therefore all
seven-edge leaves are excluded. Together with the preceding bound of seven,
this proves the bound of six.

The new obstruction also reduces the campaign's necessary all-unit carrier
from twenty to seventeen high-core types. This is **not** a classification
of realized packings: existence of any of the seventeen remaining types,
and their compatibility with other stars, are further obligations.
In the degree-only [catalog](local_types.json), the seventeen retained types
have six four-edge, six five-edge and five six-edge cores, all without a
four-clique. The unfiltered all-unit catalog has twenty-six types.

## Reproduction and trust boundary

Python 3.11.2, standard library only, exact integers; one process and all
numeric-library thread limits one. From the repository root:

```sh
python3 -B constant_weight_18_6_5_equality_structure/check_unit_eight.py
python3 -B constant_weight_18_6_5_equality_structure/verify_unit_eight.py --compare-primary
python3 -B constant_weight_18_6_5_equality_structure/check_unit_seven.py
python3 -B constant_weight_18_6_5_equality_structure/verify_unit_seven.py --compare-primary
```

The first two commands check the preceding eight-edge exclusion used here.
[`check_unit_seven.py`](check_unit_seven.py) enumerates zero-block frames by
a multiset cover recursion: select a point still needing an occurrence,
try every legal quadruple containing it, and derive the last quadruple from
the remaining four unit incidences. An induction on the number of remaining
blocks shows that this includes every frame. Its rejection-tree producer
reuses the exact integer-bitset kernel in
[`check_unit_eight.py`](check_unit_eight.py).

[`verify_unit_seven.py`](verify_unit_seven.py) imports no primary code in its
default mode. It starts from independently written literal leaves, filters
all five-point permutations and all `6!` attached and `6!` matched bijections,
and reconstructs double tails by scanning all `C(17,4)=2380` quadruples.
For zero-block frames it chooses the first two blocks in increasing order
and derives the third directly from the remaining point multiplicities.
Every valid ordered zero-block triple has those first two choices, so this
different enumeration is complete. It also reconstructs the triple-high
branch without assuming the matched-tail simplification. All residual
columns are rebuilt by another full scan of the 2380 quadruples.
With `--compare-primary`, every actual group map, raw tail triple,
raw zero-block fiber, triple-high prefix, canonical case, row and column
agrees **entry by entry** with the primary implementation.

The verifier replays [`unit_seven_certificate.json`](unit_seven_certificate.json)
using ordinary sets and literal branch checks. The certificate is 130798 bytes,
with SHA-256
`7fcaaa04f8cd79047881764066cbbeae1db31462ef5857df01805919e8642db6`.
The ordered instance stream has SHA-256
`44db7f336581c2a1b1934e60cd64ca0ee1971d6fc15e9cdec297e788e907c195`.
[`unit_seven_expected.json`](unit_seven_expected.json) records branch counts,
carrier hashes and expected results. Six corrupted certificates and two false
no-cover proofs for a positive instance are rejected. A known affine-plane
residual with sixteen quadruples is accepted as a cover, and the primary
kernel detects it. Zero node caps in both the cover producer and zero-frame
producer raise `INCOMPLETE`. The production guards remain 200000 nodes and
ten seconds per case; none was reached. Normal and optimized Python outputs
agree. Private exploration files and verbose run records are not published.

The two implementations are by the **same researcher**, not independent
peer review. The incidence, leaf classification, relabeling and exact-cover
bridges are ordinary written proofs and are not formalized. The interpreter,
the finite enumerations, the proof kernels and the previously published
eight-edge exclusion are computational dependencies. There is no solver or
floating-point verdict. No assertion excludes all seventy-two-word codes.

## Primary context

Brouwer's [1975 report](https://ir.cwi.nl/pub/6883/6883D.pdf) establishes
`A(17,6,4)=20`; his [1977 report](https://ir.cwi.nl/pub/6853/6853D.pdf) treats
seventeen as an exceptional packing order. These historical facts are
dependencies, not new results. Chang, Dukes and Feng's
[2021 paper](https://ajc.maths.uq.edu.au/pdf/80/ajc_v80_p281.pdf) on leaves
mainly treats other congruence classes and large-order existence and does
not settle these selected seventeen-point leaves. The
[maintained constant-weight table](https://aeb.win.tue.nl/codes/Andw.html),
checked live on 2026-09-30, retains 69–72 for `A(18,6,5)`.
[`reproduce.py`](reproduce.py) checks the published 69-word construction
exactly as baseline validation. This local strengthening is new to the
campaign and bounded searched sources; no general priority claim is made.
