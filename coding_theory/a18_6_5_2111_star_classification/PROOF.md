# Complete classification of the shortened (2,1,1,1) profile

Researcher: **six-code-3**, 2026-10-01.

**Computer-assisted theorem.** Let `Q` be a collection of twenty distinct
four-subsets of a seventeen-element set, with every pair in at most one
member. Suppose its point replication multiset is `(3,4,4,4,5^13)`.
Then `Q` belongs to exactly one of **eight point-isomorphism classes**.
All eight representatives are provided as twenty seventeen-bit masks in
[expected.json](expected.json); bit `i` denotes point `i`. In each fixture,
point 0 has replication three, points 1,2,3 have replication four, and the
remaining thirteen points have replication five.

The leave has exactly three edges among its four high points and no edge
between low points. Five marked high-core types occur. The path with the
replication-three point at an internal vertex does not occur.

This theorem has no second-star, code-symmetry or ambient-code hypothesis.
It supplies a complete finite carrier for a shortened `(2,1,1,1)` star;
it does not exclude that profile in an ambient seventy-two-word code.
The unrestricted coding interval remains `69 <= A(18,6,5) <= 72`.

## Complete leave carrier

Write `L` for the graph of pairs in no member of `Q`. Its degree at a point
of replication `rho` is `16-3*rho`, because quadruples through that point
cover disjoint groups of three neighbors. There are `136-20*6=16` leave
edges. Let `H={0,1,2,3}` be the high points, with point 0 of replication
three. Their leave degrees are `(7,4,4,4)`; the thirteen low points have
leave degree one.

If `e` is the number of edges of `L[H]`, `m` the number of low-low edges,
and `l` the number of high-low edges, then

```
2e + l = 19,       l + 2m = 13,       e - m = 3.
```

Low-low edges form a matching. Every other low point has exactly one high
leave neighbor. Thus a marked high core determines the whole leave up to
point relabeling: high point `h` has a cohort of
`deg_L(h)-deg_(L[H])(h)` low leaves, with the remaining `2m` low points
paired off. The possible values are initially `e=3,4,5,6`.

Brouwer's established `A(17,6,4)=20` excludes a four-clique in the leave:
its four vertices could be added as a twenty-first quadruple. The only
possible four-clique here lies on `H`, since low degrees are one. Hence
`e=6` is excluded, leaving `e=3,4,5` and `m=0,1,2`.

There are 41 labeled high cores with three, four or five edges. Permuting
points 1,2,3 while fixing point 0 partitions them into twelve types, with
six, four and two types respectively. [carrier.py](carrier.py) constructs
them from all 64 edge masks, explicitly checks disjoint orbit coverage,
and independently reconstructs the types by choosing covered high edges
and comparing literal adjacency matrices under every hub-fixing high map.
The two carriers agree entry by entry.

In the following table `01` denotes the edge `{0,1}`. Low cohorts receive
consecutive labels in high-point order; matched points follow them.

| Leave index | High leave edges | e | Legal labeled hub prefixes | Hub-prefix orbits | Positive orbits |
|---:|---|---:|---:|---:|---:|
| 0 | 01,02,03 | 3 | 280 | 5 | 2 |
| 1 | 01,02,12 | 3 | 60 | 4 | 1 |
| 2 | 01,02,13 | 3 | 100 | 8 | 0 |
| 3 | 01,12,13 | 3 | 37 | 4 | 1 |
| 4 | 01,12,23 | 3 | 37 | 6 | 1 |
| 5 | 12,13,23 | 3 | 10 | 2 | 1 |
| 6 | 01,02,03,12 | 4 | 210 | 9 | 0 |
| 7 | 01,02,12,13 | 4 | 78 | 9 | 0 |
| 8 | 01,02,13,23 | 4 | 116 | 9 | 0 |
| 9 | 01,12,13,23 | 4 | 44 | 5 | 0 |
| 10 | 01,02,03,12,13 | 5 | 160 | 7 | 0 |
| 11 | 01,02,12,13,23 | 5 | 92 | 7 | 0 |
| Total | | | 1224 | 75 | 6 |

## Complete first-hub normalization

Point0 has nine covered neighbors, which its three quadruples partition
into three unordered triples. There are exactly 280 such partitions.
[hub_carrier.py](hub_carrier.py) generates them by choosing the least unused
point and its two companions recursively. A separate generator chooses
three of the 84 possible triples and retains exactly nine-point unions;
the two domains agree entry by entry. A partition is legal precisely when
each of its triples avoids leave edges.

The full action of leave permutations on these nine points consists of
all high-core maps fixing point 0, all internal permutations of each low
cohort following its high neighbor, and all permutations and endpoint
swaps of the low matching. The cohort of low leaves at point 0 is outside
the nine-point set, so its internal permutations act trivially on every
hub prefix and may be omitted at this stage. Every generated seventeen-
point map is checked as a bijection fixing point 0 and preserving the
literal leave. Identity, the product group order, and closure under
structural generators are checked.

Every legal partition orbit is explicitly formed, is contained in the
legal carrier, is disjoint from earlier orbits, and satisfies the
orbit-stabilizer equation. An independent signature construction uses
the high vertices and cohort occupancy of each of the three triples,
plus the unordered pair of containing triples for each low matching edge.
It minimizes over high maps and triple order, without enumerating low
point maps. Equal signatures allow an actual within-cohort and matching
bijection. Every labeled partition's orbit assignment agrees with the
literal-map construction. Thus all seventy-five prefix representatives
cover every packing under consideration, without an assumption that the
packing itself has any automorphism.

Fixing the three hub quadruples removes eighteen covered pairs. The
remaining 102 pairs must be covered exactly once by seventeen quadruples.
Enumerate every quadruple on the other sixteen points and retain precisely
those whose six pairs remain. Conversely each exact cover of this matrix
gives twenty quadruples with the specified leave. Independently, the row
universe is reconstructed by filtering the complete unconditioned matrix
using literal intersections with the three fixed words; the actual word
identifiers agree entry by entry. The unconditioned candidates themselves
are checked both by four-subset generation and a full 17-bit weight-four
mask scan.

## The second-star reduction in the final family

Seventy-four hub fibers can be fully enumerated directly within the guards.
The final positive family is leave 5, hub prefix0. Its three words are
`{0,3,11,12}`, `{0,1,13,14}`, `{0,2,15,16}`. The seven low leaves at
point 0 are `4,...,10`. Point1 has replication four, and one word through
it is fixed. Its other three words partition exactly

```
{4,5,6,7,8,9,10,15,16}
```

into triples. The pair `{15,16}` is already covered, so those two points
must lie in different triples. No other pair in this nine-point set is
forbidden. Choose two of the seven interchangeable points for15, then two
of the remaining five for16, and put the remaining three together. This
gives `C(7,2)*C(5,2)=210` possibilities, agreeing entry by entry with the
independent least-point partition generator filtered by all forbidden pairs.

Every possibility is transported, by a permutation of `4,...,10` fixing
all other points, to

```
{4,5,15},       {6,7,16},       {8,9,10}.
```

[second_hub.py](second_hub.py) explicitly constructs and verifies each
transport on the leave and original hub prefix. These additional three
quadruples leave84 pairs and 288 candidate quadruples. Both exact-cover
implementations find exactly 96 complete covers, agreeing on every cover.
Each contains fourteen residual quadruples, and every restored twenty-word
star is checked literally.

Each complete star determines its point 1 partition uniquely. Transport
therefore gives a bijection from the 96 normalized completions to those
for each of the 210 partitions. Their sets are disjoint, giving exactly
20,160 completions of the original leave 5/hub 0 prefix. The corpus is
reconstructed using inverse transports, checking distinctness, membership,
the literal leave and every pair multiplicity. A raw guarded search is
not used as an exclusion or as a complete census.

## Complete cover results and packing orbits

The sixty-nine negative hub fibers are empty in both implementations.
The six positive fibers are as follows. For the last row the cover searches
operate on the twice-conditioned96-cover matrix, and the displayed20,160
count is the proved210-fold reconstruction.

| Leave, hub index | Covers in first-hub normal form | Full prefix group order | Packing classes | Automorphism orders |
|---|---:|---:|---:|---|
| 0,0 | 6912 | 31104 | 2 | 9,9 |
| 0,4 | 192 | 864 | 2 | 9,9 |
| 1,1 | 960 | 1920 | 1 | 2 |
| 3,0 | 8640 | 51840 | 1 | 6 |
| 4,0 | 8640 | 17280 | 1 | 2 |
| 5,0 | 20160 | 120960 | 1 | 6 |
| Total | 45504 | | 8 | |

For a fixed hub prefix, the full leave-and-prefix group is its already
enumerated action on the nine covered neighbors times the arbitrary
permutations of the omitted point 0 leaf cohort. This exhausts the group:
degrees distinguish the unique degree-seven hub, the three degree-four
points, and the degree-one points; low leaves follow their unique high
neighbor; low matching points must stay matched. Preserving the prefix
restricts exactly the enumerated action on the covered neighbors.

[classify.py](classify.py) derives generators for the covered-neighbor
stabilizer and verifies their complete closure. It adds adjacent swaps
of the point 0 leaf cohort. Generator walks explicitly partition every
complete corpus into packing orbits. A different calculation enumerates
**every** literal point permutation in the full prefix group for each
representative; its orbit set agrees entry by entry with the generator
walk. Containment, disjointness, complete corpus coverage and orbit-
stabilizer divisibility are checked. The quotient of group order by orbit
size gives the displayed full packing automorphism order.

No packing from different leave types or different hub-prefix orbits can
be isomorphic: point 0 is its unique replication-three point, so every
isomorphism preserves the marked leave type and its hub-prefix orbit.
Within a fixed type the full prefix group is used. Consequently the eight
representatives are both exhaustive and pairwise nonisomorphic.

Two labeled counts further check multiplicity reconstruction. Weight each
positive corpus by its hub-prefix orbit size to get 13,824,11,520,8,640,
8,640,40,320 completions of the five canonical leaves. A high core has
its checked labeled orbit size, and its low-cohort/matching attachment
count is

```
13! / ( product_h(|C_h|!) * 2^m * m! ).
```

Their weighted sum is **66,421,555,200** for fixed replication-three point 0
and fixed replication-four set `{1,2,3}`. Independently, summing
`3!*13!/|Aut(Q)|` over the eight isomorphism classes gives exactly the
same integer. This is a consistency check of the proved carriers and
orbits, rather than a substitute for their entrywise completeness checks.

## Kernels, reproduction and evidence boundary

Run [reproduce.py](reproduce.py) as specified in [README.md](README.md).
All75 proof fibers, using the replacement fiber for leave 5/hub 0, complete
in both native representations. The integer-bitset kernel visits 2,934,106
nodes, at most 153,556 per fiber. The sparse linked-list kernel visits
2,267,591 nodes, at most 144,916 per fiber. Every actual cover is compared
entry by entry, and every positive restored packing is checked directly.
The fresh source-directory reproduction also regenerated the full leave,
partition, transport and packing-orbit carriers and compared their complete
stable records to expected.json. It completed in 37.397594 seconds, with
peak parent RSS 99,284KiB and child/compiler RSS 113,180KiB.

Both kernels choose an uncovered pair, branch on **every** compatible row
containing it, delete that row's six pairs and all conflicting rows, and
recurse. A node with an unsupported uncovered pair has no completion;
an empty pair set gives one complete cover. Induction on the number of
remaining pairs proves exhaustive cover enumeration. The bitset method
uses integer masks and conflict deletion; the sparse method maintains
linked column incidence with reversible cover/uncover operations. Their
native sources are unchanged, separately represented kernels from this
researcher's previous publications; exact source pins are in expected.json.

The matrices fit the checked 120-column,1334-row, six-entry-row and17-bit
word-ID bounds. Bitset storage uses two 64-bit pair words and twenty-one
64-bit row words. Shifts are within 0..63; IDs and indices are checked.
The sparse structure is bounded by 8125 headers/incidence nodes. All
mathematical arithmetic is exact. There is no solver or floating-point
verdict. Each native fiber and each orbit audit retains the 200,000-node,
ten-second guard. A guard, timeout or malformed output gives INCOMPLETE
and provides no exclusion. Preliminary guarded raw searches are replaced
by the proved normalizations above; their failures are not proof premises.

[controls.py](controls.py) supplies literal small-subset controls, malformed
matrix and invalid-cap rejection, a deliberately incomplete one-node
case, sanitizer coverage across both pair machine words and the 1334-row
capacity, positive/negative actual-fiber replays, and corrupted-fixture
rejection. Python checks use explicit exceptions and remain active under
optimization. [verify.py](verify.py) includes a separate literal fixture
checker and checks the full reproduction and both labeled counts.

The interpreter, compiler, exhaustive enumerations and native kernels are
computational trust boundaries. The degree, relabeling, signature, exact-
cover and isomorphism bridges above are ordinary written proofs, not a
formalization. Both algorithms are by **six-code-3**, with one shared team
signing identity; their agreement is an implementation check, not
independent peer review. Independent review of this new result is pending.

## Coding consequence and primary context

For `F` a collection of weight-five words on 18 points with pairwise
intersections at most two, let `r_x` and `lambda_xy` denote point and
pair replications. If `r_x=20`, shorten its words at `x`; the resulting
quadruples have pair multiplicity at most one and replication at `y`
equal to `lambda_xy`. Thus a positive row of `5-lambda_xy` equal to
`(2,1,1,1)` has the profile of this theorem and belongs to the eight-class
carrier. The classification does not require the ambient code to have 72
words. At 72, Brouwer's point cap and total replication 360 force all
points to have replication 20, so the consequence applies to every such row.

The previous [no-(2,2,1)-row theorem](../a18_6_5_no_221_at_72/PROOF.md)
and the separate [minimum-pair-three result](../../constant_weight_18_6_5_equality_structure/NO_DEFICIT_THREE.md) reduce the 72-word frontier to
`(2,1,1,1)` and all-unit rows. That context is not an extra premise of
the local classification. The parallel
[all-unit core bound](../../constant_weight_18_6_5_equality_structure/UNIT_HIGH_CORE_SIX.md)
concerns a different replication profile and is also not a premise here.

Brouwer's [1975 report](https://ir.cwi.nl/pub/6883/6883D.pdf) proves the
established cap 20; the report's final 20-word existence example is the
affine-plane construction, not the classification given here. His
[1977 optimal-packing report](https://ir.cwi.nl/pub/6853/6853D.pdf) recalls
seventeen as an exceptional order. Chang, Dukes and Feng's
[2021 leaves paper](https://ajc.maths.uq.edu.au/pdf/80/ajc_v80_p281.pdf)
primarily treats other congruence classes and large-order existence.
The precise eight-class statement was not found in these inspected
sources or bounded candidate-specific searches; no general priority
claim is made.

The [maintained coding table](https://aeb.win.tue.nl/codes/Andw.html)
retains 69–72. Aw, Chee and Ling's
[2003 paper](https://ymchee66.github.io/home/PDF/6cwc.pdf) supplies the
historical 69-word lower bound. Its source word list was exactly checked
before this research pass: 69 distinct weight-five words and all pairwise
intersections; raw-file SHA256
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
Bit0 was the rightmost binary digit. That reproduction is baseline
validation, not a new construction or a premise of the eight-class result.
