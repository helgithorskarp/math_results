# Universal fixed-vertex extension and a sharp rigidity theorem

Let H be a Ramsey (5,5) graph on four disjoint internally red triangles
C0,...,C3, with a simultaneous order-three rotation on the triangles.
Thus every cross block is a circulant three-bit word. A complete word
is impossible, since it gives a red K6. Every remaining red block is
empty, a matching, or a six-cycle; in particular it contains no K2,2.
The preceding catalog classifies these H into 197 marked-action classes.

An outside vertex is *uniform* if its edges to each Ci have a single
color. Its signature S is the subset of triangles to which it is red.
The statements below concern the graph induced by H and these uniform
vertices. They impose no degree window or conditions involving the
seven other moving triangles of a full 43-vertex candidate.

**Theorem.** Every such H admits ten uniform outside vertices, making
a Ramsey (5,5) graph on 22 vertices. If H contains a blue K4, then at
most ten uniform outside vertices are possible. At equality, their
signatures are exactly the four singleton and six two-element subsets
of {0,1,2,3}, each once. All intersecting signature pairs have blue
edges; disjoint pairs have red edges except that at most one of the
three complementary two-subset pairs may have a blue edge. All four
of these fixed-edge choices are valid, for every H.

This describes fixed vertices up to their labels. It is not a claim
that the four choices are pairwise nonisomorphic under a stabilizer.
Of the 197 catalog cores, 118 contain a blue K4, so the sharp equality
classification applies to those 118. The remaining 79 still admit
the same four constructions; no upper bound of ten is asserted for
those cores.

## Universal construction

Introduce v_S for every singleton or two-element subset S of a
four-element ground set. Join v_S red to Ci exactly when i is in S.
Join v_S and v_T red exactly when S and T are disjoint. Initially all
three complementary pair edges are red.

There is no red K4 contained in one or two core triangles. The possible
occupancies are 3+1, requiring a complete word, and 2+2, requiring a
red K2,2. Consequently a red K5 with exactly one outside vertex is
impossible: its four core vertices would lie in at most two triangles.
Two red-adjacent outside vertices have disjoint signatures, so no core
vertex can be red to both. A red clique consisting only of outside
vertices corresponds to pairwise disjoint nonempty subsets of a
four-element set and has size at most four. H itself has no red K5.

For blue cliques, an outside set with signatures A can see blue core
vertices only in triangles outside the union of A, with at most one
vertex per triangle. Distinct singleton/pair signatures in a blue
clique are pairwise intersecting. For q=1,2,3,4 such signatures, the
union has size at least q. Indeed, the only three nonempty singleton/
pair subsets on two points are not pairwise intersecting, and a
pairwise-intersecting family of singleton/pair subsets on three points
has size at most three. A pairwise-intersecting family on four points
has size at most four: with a singleton it is a star of size at most
four; without a singleton, its pairs form a star or triangle. Thus a
blue clique cannot reach size five, either mixed with core vertices
or entirely outside. H itself has no blue K5.

One may change a single complementary two-subset edge to blue. This
cannot create a red K5. A new blue K5 containing that edge cannot use
a core vertex, because the two signatures cover all four triangles.
It also cannot use a singleton outside vertex: a singleton is disjoint
from one of the two complementary pairs, and that edge stays red.
Finally, any five of the six pair vertices contain two complementary
pairs, so one of their complementary edges stays red. The change is
therefore safe. This proves all four advertised constructions valid.

## The sharp upper bound when the core contains a blue K4

Choose one blue K4 in H. It uses one vertex from each Ci. An empty
signature is impossible, since its vertex would extend that K4 to a
blue K5. Write n for the number of uniform outside vertices, X for
the number of singleton signatures, and I for their total red
incidence with the four triangles.

For each Ci, its uniform red neighbors form a blue clique: a red
edge among them, together with Ci, would be a red K5. There are
therefore at most four of them, and I <= 16.

Each singleton signature {i} occurs at most once. Two such vertices
would have a blue edge because both are red to Ci; the other three
vertices of the chosen core blue K4 would complete a blue K5.
Hence X <= 4. Every other nonempty signature has size at least two,
so

```text
2n <= I + X <= 16 + 4 = 20.
```

Thus n <= 10. Equality forces X=4, I=16, and no signature of size
three or four. Each singleton occurs exactly once. Let y_ij count
the signature {i,j}. The vertices with signatures {i} and {i,j}
are all red to Ci and hence form a blue clique. There is a blue
cross edge between the two remaining core triangles (otherwise
those triangles form a red K6). Three of these outside vertices
and that blue edge would be a blue K5, so 1+y_ij <= 2. Thus
y_ij <= 1. There are six remaining outside vertices and six pair
signatures, so all occur exactly once.

The controls additionally enumerate the nonnegative signature-count
vectors satisfying these incidence, singleton and oriented
singleton/pair inequalities, independently recovering this unique
ten-vertex equality profile. This is an arithmetic check of the
displayed argument, not an enumeration of arbitrary graph realizations.

## All fixed-edge choices at equality

Two intersecting signatures must have a blue edge, as already proved.
Consider disjoint signatures.

* If {i} and {j} had a blue edge, those two vertices and v_{ij}
  would form a blue triangle. A blue cross edge between the other
  two core triangles would complete a blue K5. Thus the edge is red.
* If {i} and {j,k} had a blue edge, with i,j,k distinct, the four
  vertices v_i,v_{jk},v_{ij},v_{ik} would form a blue K4. Any vertex
  of the fourth core triangle is blue to all of them. Thus this
  edge too must be red.
* The only remaining disjoint signatures are the three complementary
  pair pairs. If two of these edges were blue, the four endpoints
  together with either vertex of the third pair would form a blue
  K5. Therefore at most one can be blue.

These necessary conditions give precisely the four constructions
already verified sufficient. No additional fixed-edge patterns exist
when n=10 and H has a blue K4.

## One-vertex census and exact checking

For any core H, a uniform signature S is allowed for one outside
vertex exactly when the red-induced core on triangles in S has no
red K4, and the blue-induced core on the complementary triangles has
no blue K4. A core blue K4 uses all four triangles, so the latter
condition simply forbids S=empty when such a clique exists.

The producer enumerates the core red K4 supports and a blue K4
witness, then calculates the allowed signatures. The independent
checker instead constructs and checks all 197*16 literal thirteen-
vertex graphs for monochromatic K5s. The numbers of allowed
signatures are 11,13,14,15,16 in respectively 1,19,42,125,10 cores.

For each core, the producer writes the four valid 22-vertex edge
lists. The independent checker reconstructs the core using literal
rotation orbits, reads and validates every serialized graph, checks
the order-three action on all 231 pairs, and counts all monochromatic
K5s by recursive adjacency intersections. It also checks all eight
choices of complementary-pair edges. In bit-mask order 0,...,7,
the red K5 counts are always zero and the blue K5 counts are exactly
0,0,0,2,0,2,2,6. Thus the four invalid template variants are also
directly witnessed. The compact result records every valid graph's
edge hash and edge count, in addition to all signature data.

## Application and limitations

No one of the 197 cores can be excluded using only the Ramsey
constraints on its twelve vertices and ten uniform fixed vertices:
each has four explicit satisfying extensions. For 118 cores, the
fixed-signature and edge classification can be imposed in a future
full extension search. For the other 79, these templates prove
feasibility but do not classify all fixed extensions.

The local fixture labels put singleton signatures first. They must
not be inserted as fixed-vertex units in the accepted full formula
without reconciling its full eleven-bit lexicographic row ordering.
This pass supplies no new full-formula bridge, CNF, SAT/UNSAT verdict,
43-vertex graph, global exclusion, or Ramsey lower-bound improvement.
All 197 full extensions remain open, with the preceding meaning of
untested full extensions. The three-versus-eight branch is unchanged.

The structural theorem is solver-free and its proof needs no external
Ramsey value or catalog completeness. Applying its census to the
entire four-versus-seven boundary imports the preceding 197-class
cover and full-action normalization, which still await independent
review. This new theorem and its internal computational checks also
await independent review. Ordinary unformalized reasoning, exact
Python/runtime/hardware, inherited source bytes and SHA256 remain
trust boundaries. No historical-priority claim is made.
