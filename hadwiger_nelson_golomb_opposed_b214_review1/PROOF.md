# Proof and review analysis

## 1. Exact geometry

All coordinates have common denominator 36 in the multiquadratic field
`Q(sqrt(3),sqrt(5),sqrt(11))`. Basis indices are three-bit subsets of
`{3,5,11}`. Multiplication sends indices `i,j` to `i xor j` and multiplies the
coefficient by every prime whose bit lies in `i and j`. Linear independence
of the eight basis terms makes collision and distance equality
coefficientwise.

The review reconstructs the pinned A159 and B214 source graphs as 159/646 and
214/977 points/edges. It independently verifies the B214 marked distance
three and the A159 marked equilateral squared-distance-seven triangle.

Apply `L(x,y)=(x-1/2,y)` and `R(x,y)=(-x+1/2,y)` to B214. Exact lookup, not a
declared label map, finds all ten Golomb points in each transformed copy.
Merging the 438 input labels gives 343 physical points. Scanning all 58,653
physical pairs finds 1,782 unit edges. The union of inherited Golomb and B214
edge images has 1,674 edges; the remaining 108 are real incidental contacts.

Adjoining native A159 and merging all 597 labels gives 359 physical points:
143 A159 points overlap the old support and 16 are new. All 64,261 pairs give
1,893 unit edges. Relative to S343 this adds 111 edges, including 32 new
contacts beyond the inherited component sets. Point and edge streams match
the target's four published hashes entry-for-entry.

## 2. Complete normalized input relation

The Golomb vertices `0,1,2` form a unit triangle. Any four-colouring can be
globally relabelled so their colours are `0,1,2`. Literal enumeration of the
remaining `4^7` assignments gives exactly 95 proper normalized Golomb words.
The certificate contains one proper 343-point word and one proper 359-point
word for each of 66 distinct prefixes. The review checks all 132 words on the
freshly reconstructed complete edge sets.

For the other 29 prefixes, introduce four one-hot variables per S343 vertex
and one selector per prefix. Vertex clauses enforce exactly one colour, edge
clauses forbid equal endpoint colours, three units fix the normalizing
triangle, and a selector disjunction chooses one excluded prefix. The 29
selector implications fix its ten Golomb colours. Consequently the CNF is
satisfiable exactly when some missing normalized prefix extends to S343.
It has

```text
1401 variables = 4*343 + 29 selectors,
9823 clauses   = 7*343 + 4*1782 + 3 + 1 + 29*10.
```

The regenerated DIMACS stream has SHA-256
`93690a58e3a2bc01e281e65a37e3955c7fedb720e5a983b19cb99882e47c9e04`.
An occurrence-count unit propagator independently verifies every one of the
1,382 deletion-free RUP additions and the final empty clause. Therefore none
of the 29 prefixes extends, and the S343 relation is exactly the 66 positive
prefixes.

## 3. Interaction and native-completion conclusions

The excluded prefix `0121212203` has a checked proper 214-symbol word on each
isolated B214 source, and exact coordinate containment maps both words to that
same Golomb prefix. The RUP theorem excludes it jointly. Hence at least one
loss arises from the complete physical interaction, rather than from the
intersection of the two isolated positive tests. No completeness statement is
made about the separate-copy relations of the other 28 excluded prefixes.

S343 is the induced old-vertex subgraph of S359. Its exclusion proof therefore
also excludes those 29 prefixes from S359, while the 66 checked S359 words show
all other prefixes survive. Thus the native A159 completion changes the
relation by exactly zero patterns.

## 4. Chromatic number and cut structure

Exhausting all `3^7` normalized Golomb tails finds no proper word. Because the
normalizing triangle must use three different colours, this excludes every
three-colouring of Golomb and hence of both larger supports. Their positive
four-colour words prove both chromatic numbers equal four.

A direct low-link traversal of each reconstructed graph finds one connected
component, minimum degree five, no articulation vertex, and no bridge. The
source relation gain is therefore not a bridge, articulation, or pendant
effect. This does not make the relation loss sufficient for five-chromaticity.

The same S343 support has 96 squared-distance-seven pairs and no such triangle,
so the native A159 placement is not obtained by identifying its marked
sqrt(7) triangle with three old points. Its 143 overlaps arise through the
larger native coordinate structure.

## 5. Trust boundary and limitation

The theorem trusts the two hash-pinned public coordinate files, the target's
hash-pinned positive words and RUP trace, multiquadratic basis independence,
Python arbitrary-precision integers, finite enumeration code, and ordinary
hardware. The review independently checks the semantics rather than trusting
the target checker or the solver that produced the trace.

The geometry and relations are complete only for the fixed two B214 frames and
one native A159 placement. They do not classify nearby or arbitrary
placements. Sixty-six full Golomb inputs remain, both graphs have explicit
four-colourings, and no cap-feasible operation eliminating the residual is
supplied. This is a forcing-bearing construction lemma and a neutral
completion stop, not global progress on the chromatic number of the plane.
