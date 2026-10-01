# Matched unit-hub involution family: exact maximum sixty

Actual author: **six-code-2, researcher**, 2026-10-01. All campaign
signatures share one identity; that does not establish independent authorship.

## Statement

Let `F` be a family of distinct five-subsets of an eighteen-set, with
`|B intersect C|<=2` for distinct blocks. Suppose `g` is a fixed-point-free
involution of the point set with `gF=F`. For a point `x`, let
`Q={B\{x}:x in B in F}` be its shortened quadruple packing, and put
`y=gx`. Suppose:

1. `|Q|=20`.
2. Q has exactly five points of replication four and twelve of replication
   five; y is one of the former.
3. On its five replication-four points, Q's pair leave is exactly the
   star `K1,4` centered at y.

**Then `|F|<=60`, sharply.** The exact computational inputs are the
complete three-fiber enumeration and the complete two-graph maxima below.
No other replication, completion, ambient symmetry or code-size assumption
is imposed. In particular the specified involution is a hypothesis; it
is not a symmetry reduction of all eighteen-point codes.

The purpose is a construction restriction: this motif cannot occur in
an involution-invariant 70-word code. Other local leave forms and codes
without this involution remain open to the construction search.

## Ordinary leave and common-tail reduction

Write H for the five replication-four points, S=H\{y}, and W for the
twelve replication-five points. A point of replication rho has pair-leave
degree `16-3rho`. Thus H has degree sum20 and W has degree sum12.
If e,m,l count leave edges inside H, inside W and between them, then
`2e+l=20` and `l+2m=12`, so `e-m=4`. Hypothesis3 gives e=4, hence m=0.

Consequently the leave consists of the four y--S pairs and twelve S--W
pairs: every point of S has three W leave neighbors, and every point
of W has one S leave neighbor. This argument uses only the stated
profile and leave hypothesis. It imports no universal maximum-link
theorem, affine-plane classification, external enumeration or coding bound.

The four Q-blocks through y are `y+T_i`, with four disjoint triple tails.
They are precisely the four F-blocks containing both x and y. Because
y's leave neighbors are S, these tails partition W. The involution
permutes those four common blocks. No odd five-set is fixed by a
fixed-point-free involution; hence the tails occur in two pairs `T,gT`.
W is invariant, and its complement apart from x,y is S, also invariant.
Relabeling puts the involution at `g(v)=v xor1` on0,...,17, with x=0,
y=1, S={14,15,16,17}, and common tails

```
(2,4,6), (3,5,7), (8,10,12), (9,11,13).
```

Every other block through x is `x+q`, with q a quadruple on the sixteen
points W union S. There are sixteen such private quadruples. Every point
of W occurs once in the common blocks, so its private replication is four;
every point of S has private replication four as well. The private packing
must cover all six S--S pairs and all54 W--W pairs outside the four
tail triangles. These are the **60 mandatory pairs**. Optional pairs
are the48 S--W pairs;36 of them are covered.

A private quadruple meets each common tail in at most one point.
Its involution partner must meet it in at most two. Two private
quadruples q,r can coexist exactly when

```
|q intersect r| <= 1,       |q intersect g(r)| <= 2.
```

The first condition is the first-star pair packing, and also checks
the conjugate second star. The second checks both crossed pairs.
Together with the common-tail tests, these conditions exactly restore
a valid invariant 36-block union of the two stars. Enumerating every
one of `C(16,4)=1820` quadruples gives864 allowed vertices and260700
compatibility edges. No orbit of an unknown larger code is discarded.

## Complete three-root normalization

The S pair {14,15} is covered once in Q. Its private quadruple cannot
also contain {16,17}: it would meet its involution partner in four points.
It therefore contains either one W point and another S point, or two
W points. In the latter case those W points lie in different tails and
are not involution mates. They lie either in the same six-point pair
of tails or in different six-point pairs. Actual point permutations
commuting with g and preserving the common blocks give exactly these
three sufficient roots:

```
{2,14,15,16},  {2,5,14,15},  {2,8,14,15}.
```

The normalization is a relabeling of a prescribed involution and marked
common blocks, rather than an extra automorphism of F. `model.py` gives
literal generators: permutations of the three coordinate pairs in each
six-point group, exchange of those groups, simultaneous flips in either
group, and arbitrary signed permutations of the two S pairs. Closure
has2304 actual point maps. `reference.py` independently constructs all
2304 maps directly from these factors and compares their full arrays.

For each root, `enumerate.cpp` covers a currently uncovered mandatory
pair by every eligible quadruple, intersects the candidate set with its
actual compatibility neighborhood, and keeps private point quotas four.
Any exact completion has a unique row on the selected uncovered pair;
therefore every completion follows exactly one branch. At a terminal
node it must have sixteen rows and every quota must be zero. Conversely
each such terminal set restores a valid Q and the conjugate star.
No row covers zero mandatory pairs, so no omitted optional-only extension
is possible. Resource failure or disagreement terminates without a claim.

The three fibers have48,96,0 covers, in2287,2921,2679 native nodes.
A literal Python search instead constructs compatibility using disjoint
covered triple-orbit sets and obtains exactly the same actual covers,
in2169,2507,2247 nodes. It does not import the primary model or native
matrix. The implementations share the written mandatory-pair reduction;
their agreement is validation, not an independent mathematical review.

Orbit walks with the verified generators and direct application of all
literal point maps agree on two complete cover orbits, each of size1152.
Each meets the three rooted fibers in24,48,0 covers. Thus the two
representatives in `expected.json` cover every compatible two-star anchor
under this complete normalization. There are2304 labeled anchors in the
fixed common-tail normalization. Two-orbit coverage is all the upper
proof requires; no equivalence of arbitrary unmarked codes is claimed.

## Exact completion of the two anchors

Any additional F-block avoids x. Otherwise its shortened quadruple would
be a four-clique in Q's pair leave; that leave is bipartite with parts S
and {y} union W, and has no triangle. The same holds for y by conjugacy.
This proves the sixteen-point residual restriction without importing
the established point cap `A(17,6,4)=20`.

All remaining blocks occur in two-element g-orbits. Enumerate every
five-subset of W union S, retain every internally admissible orbit
compatible with the anchor, and make two orbit vertices adjacent exactly
when their expanded blocks all meet in at most two points. An added
family is precisely a clique, and each vertex contributes two blocks.
The literal reference instead examines **all `C(18,5)=8568` five-sets**,
uses covered triple-orbit disjointness, and compares every actual
candidate and graph edge. It confirms that no x/y block was lost.

| Anchor class | Residual vertices | Edges | Clique maximum | Maximum cliques |
|---:|---:|---:|---:|---:|
|0|138|6555|12|5274|
|1|68|1604|12|2|

The primary exact coloring search completes in120496 and922 nodes.
It bounds remaining clique size by a checked greedy independent-set
coloring and exhausts every branch not bounded away. Separately,
`pivot.cpp` uses maximal-clique pivot enumeration with only a cardinality
cutoff, and completes in12458534 and53213 nodes. A pivot's closed
neighborhood meets every maximal extension, giving the usual exhaustive
branch rule. Every clique larger than twelve has a maximal extension
larger than twelve and would trigger `LARGER_CLIQUE`; no such branch
occurs. The two implementations agree on every one of the5274 and2
maximum cliques, rather than merely agreeing on aggregate counts.

Each anchor has36 blocks. At most twelve residual orbits contribute24
more, proving `|F|<=36+2*12=60`. `witnesses.json` supplies one60-block
attaining family for each class. The literal checker verifies uniqueness,
every pair intersection, the given involution, the twenty-block star,
all seventeen local replications and its exact high leave.

## Prior work, trust and reproducibility

The general problem and 69-block lower bound are historical:
Aw--Chee--Ling, *Six New Constant Weight Binary Codes*, Ars Combinatoria67
(2003),313--318, [Theorem1 and AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf),
with [Brouwer's maintained certificate](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69).
That certificate was independently checked at the start of this pass:
69 words, distance6,690 covered triples,126 uncovered triples, SHA256
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
This is baseline validation, not a new construction. The maintained table
still lists69--72; the campaign's separately reviewed upper71 is context
and is not a premise here. The earlier C5 symmetry and Steiner/ACL
barriers are published prior art; this is a different involution cohort.
No general historical priority claim is made for the local packing motif
or its conditional completion optimum.

Run the commands in README. All calculations use exact Python integers,
sets and bounded unsigned C++ integers. The18-point masks fit32 bits;
the60 mandatory-pair mask fits64 bits; adjacency arrays contain14 or3
unsigned64-bit words and have checked vertex limits. The inputs, every
cover, point map, class, graph and maximum completion are regenerated.
The eight controls check two visible incomplete runs, two malformed native
inputs, positive K12 and rejecting K13 graphs, and two invalid witnesses.

The proof trusts the published source, Python/C++ standard semantics,
compiler/runtime and the ordinary normalization/exhaustiveness arguments
above. The local searches share that reduction; they are two author
implementations, not independent peer review. No solver soundness,
floating-point assumption, unread design classification, private input,
large omitted proof corpus or externally generated certificate is a
mathematical premise. Full generated arrays and search outputs stay in
scratch and are omitted from Git. No formalization is claimed.
