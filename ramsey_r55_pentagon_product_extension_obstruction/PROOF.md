# No proper Ramsey extension of the pentagon product

Call a graph **good** if it has neither a clique nor an independent set of
order five. Let H=C5[C5], the lexicographic product of two pentagons. Its
vertices are (i,a), with i,a in Z/5Z. Vertices in the same outer block i
are adjacent when their inner coordinates differ by 1 or 4. Vertices in
distinct outer blocks are adjacent exactly when the outer coordinates
differ by 1 or 4. Red means edge; blue means nonedge.

**Theorem.** No good graph contains H as a proper induced subgraph.
In particular, every 43-vertex graph with an induced H has a monochromatic
five-set. The conclusion allows every possible attachment and every edge
among the other 18 vertices; the 43-vertex graph need not have any symmetry.

**Integration with h3931.** Its independently accepted equality theorem
states that the only good25 graph containing neither an induced P5 nor its
complement is H, up to isomorphism. Therefore the complete good43 branch
with a 25-set containing neither pattern is empty. Every 25-set in a
hypothetical good43 must contain P5 or its complement.

The output gate is this complete physical-family exclusion, with a literal
obstruction extractor. It is not a new carrier comparison or an estimate
of how much faster a solver will run. No good43 is constructed or ruled
out outside the specified family, and no h3887 task is declared decided.

## One outside vertex gives the contradiction

Suppose x is outside an induced copy of H. In inner block i, mark R if
the red neighbors of x contain an adjacent pair. Mark B if the blue
neighbors of x contain a nonadjacent pair, where adjacency is in H.
A block may have both marks.

Every block has at least one mark. Otherwise the red neighbors in that
inner C5 form an independent set of size at most 2, while the blue
neighbors form a clique of size at most 2. These two sets partition all 5
vertices of the block, which is impossible.

If two adjacent outer blocks are marked R, take a red adjacent neighbor
pair from each. All four cross edges are red by the definition of H, and
all four vertices are red neighbors of x. They and x form a red K5.
Likewise, two nonadjacent outer blocks marked B supply a blue K5 with x.

Thus avoiding a monochromatic K5 would make the R-marked outer blocks an
independent set in C5, and the B-marked outer blocks a clique in C5.
Each set has at most 2 elements. Their union cannot cover all 5 blocks,
contradicting the preceding covering property. The marks need not be
disjoint; the inequality |R union B| <= |R|+|B| <=4 still applies.

This elementary argument deals with every possible neighborhood of x.
It uses neither h3931 nor an imported Ramsey-number bound. The h3931
equality theorem is used only to identify the entire 25-vertex
(P5,complement-P5)-free branch with this fixed core in a hypothetical target.

The fixed core itself is good: a clique meets at most two adjacent outer
blocks, with at most two vertices in each; the analogous assertion in the
complement bounds independent sets by 4. Both bounds are attained.
The independent finite check additionally inspects every one of its 53,130
five-sets for K5, independent 5, P5 and complement-P5. Its 150 red edges and
literal 300-bit word match the accepted h3931 order 25 witness exactly.

## Complete physical 43 family

Fix the standard ordered core on vertices 0,...,24. All 300 internal core
pairs are fixed. The other 25*18+binom(18,2)=603 physical pairs are
unrestricted. Hence this fixed-core family contains exactly 2^603 distinct
labeled 43-vertex graphs. The theorem rejects every one of them.

The full class includes arbitrary embeddings of H into the 43 vertices.
Different embeddings may describe the same graph, so we do not multiply
2^603 by any number of embeddings or labelings. This is not a fraction of
the h3887 carrier and is not combined with any earlier denominator.

For a fixed outside vertex, its 25 core contacts have 2^25 possibilities.
The other 578 free edges cannot change a five-set contained in H union{x}.
This observation transports the universal one-vertex certificate to the
whole 603-edge family. There is no assumption on the graph induced by the
outside vertices or on their contacts with one another.

## A compact complete certificate

The 32 five-bit attachment words for an inner pentagon have tags R-only,
B-only, or both, with counts 11,11,10 respectively. CERTIFICATE.json gives
each word's exact tag and a literal pair for each mark it has.

There are 3^5=243 possible five-block tag vectors. For each vector, the
certificate selects either two adjacent R-marked blocks or two nonadjacent
B-marked blocks. Its class weight is the product of the five tag counts.
These classes partition all 32^5=33,554,432 attachment words. The sum of
the recorded weights is exactly 2^25.

The separate checker reconstructs the cycle and core as literal edge sets.
It checks every inner tag/pair, every outer class, and every one of 27,015
selected two-block attachment combinations against all ten physical pairs
of the returned five-set. The other three blocks never meet that five-set,
so all their attachments are covered by the class weight. This is an
exhaustive factored proof, not a claim that 33,554,432 full attachments were
individually enumerated. Class disjointness follows from their unique tags.

The producer's choice to prefer a red certificate breaks a computational
tie only; its red/blue output counts are not invariants of the graph family.
No candidate search or target solver is needed for the proof or replay.

## Physical interface and independent certificate boundary

Give interface.py a full 903-bit 43-vertex graph and an unordered list of 25
vertices. It recognizes the specified induced core and, if present, returns
an actual monochromatic five-set in the full graph.

The recognizer uses a property specific to H. For a pair u,v inside a
single inner block, exactly 2 other core vertices distinguish u and v by
adjacency; for vertices in different blocks, exactly 14 distinguish them.
The within-block values follow directly from the five-cycle. For distinct
adjacent outer blocks the common red-neighbor count is 4, and for distinct
nonadjacent blocks it is 5; since all core degrees are 12, removing the two
endpoints gives 14 distinguishers in both cases. These counts identify the
five inner blocks under any relabeling.

The code then checks the five inner cycles and outer cycle and explicitly
verifies all 300 core pairs against the standard product. It is a specialized
recognizer, not a general graph-automorphism or canonical-labeling tool.
Its completeness on H follows from the 2/14 calculation and cycle traversal;
its soundness rests on the final literal pair check. No invalidated earlier
automorphism verifier is used.

The extractor chooses one outside vertex, computes its five attachment
words, selects the certified block pair, and translates the resulting
five-set back to the full physical labels. verify_certificate.py imports
no core, producer, or recognizer code. It checks the graph binding and the
ten physical edges directly using the closed-form 903-bit pair index.

If the supplied 25-set is not H, the interface returns
OUTSIDE_SPECIFIED_CORE_FAMILY. This gives no Ramsey verdict about that
graph and does not claim there is no H on another 25-set. The universal
theorem supplies the existence of a valid embedding for members of the
declared family; the interface accepts that subset as input. It does not
enumerate all binom(43,25) possible subsets.

The controls cover 12 complete 43-vertex fixtures, arbitrary transport of
the entire core and tail, both colors, a changed core, malformed inputs,
and corrupted family/physical certificates. They support implementation
correctness; the elementary argument and complete class certificate supply
the universal exclusion. The stored full 43 fixture is deliberately rejected
and is not a Ramsey candidate.

## Downstream effect, dependencies and boundary

The accepted h3931 theorem left a unique 25-vertex equality case. It did
not itself decide the arbitrary 43-vertex extensions of that case. Here all
those extensions are rejected by a physical witness, eliminating that
complete global branch. The corollary moves the guaranteed induced-pattern
statement from 26-sets to 25-sets inside a hypothetical good43, but the
milestone is the complete extension decision and its universal extractor.

BRIDGE_CONTROL.json demonstrates the change on a complete physical graph.
Take the standard core, let vertex 25 be adjacent just to core vertex 0,
and set the other free edges blue. The order (25,0,1,2,3) is an induced P5,
so the 26-set 0,...,25 falls outside the earlier pattern-free 26-core premise.
The new interface nevertheless returns a literal blue K5 in this graph.
The controls check all ten pairs of each pattern. This example illustrates
the interface change; it is not a substitute for the universal family proof.

The elementary core-extension theorem is self-contained. The bridge from
an arbitrary 25-vertex pattern-free set imports h3931's equality result,
accepted at h3935, and therefore its classical theorem dependencies as
stated in that package. The finite checker does not re-prove the imported
modular-decomposition classification. Source and review commits, graph refs,
manifest hashes and the equality-witness file are pinned in DEPENDENCIES.json.

Residual trust includes the written covering/product argument, the two
Python implementations, exact integer/bit and SHA-256 semantics, OS and
hardware. No solver, external graph catalog, floating-point calculation,
or full-graph automorphism claim is a proof dependency. This elementary
argument may be classical; no historical novelty or external review of the
new package is claimed.

The declared gate ends after validation, publication and immutable handoff.
Do not continue here with another core size, product-template enumeration,
attachment search, carrier quotient, or threshold refinement. The h3937
carrier and regular 18 density gates remain parked. Physical completion
belongs to team-r55-1. All 2,189,178 h3887 tasks remain undecided at this
checkpoint; this result supplies no new bound for R(5,5).
