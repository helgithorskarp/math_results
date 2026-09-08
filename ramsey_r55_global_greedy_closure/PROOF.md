# Greedy closure across whole residual unions

Let **good43** mean a red/blue coloring of K43 with no monochromatic K5.
The red graph and its complement both have clique number at most four.
We use the independently reviewed [h3835 packing cover](../ramsey_r55_global_clique_packing/PROOF.md),
at source `3f06352ae0735101a04afa1ba7b055736e7300f7`, whose review is
[here](../ramsey_r55_global_clique_packing_review1/README.md).

**Theorem.** Every good43 admits a labeling in one of the following 39
refined complete physical branches:

- r in {5,6,7};
- s in {1,2,3,4};
- t in {0,1,2} when s<4, and t in {0,1,2,3} when s=4.

The fixed blocks are r red K4s, 7-r blue K4s, s red triangles, 4-s blue
triangles, and a last triple with t red edges in the h3835 canonical shape.
The usual root-signature comparisons remain imposed. In addition:

1. When r<7, the union of all vertices outside the r red K4 blocks has
   **no red K4**. This union has 23 or 19 vertices.
2. When s<4, the union of the blue triangle blocks and the last triple has
   **no red triangle**. This union has 12, 9 or 6 vertices.

The complete target formulas in `strengthen.py` impose these constraints on
all physical vertices of the indicated unions, together with every h3835
root and target clause. Existence of a good43 is equivalent to satisfiability
of at least one of the 39 formulas. No such satisfiability question is decided
here.

## Why maximal greedy choices force the extra constraints

Choose red K4s greedily until either seven have been selected or none remains.
At least five can be selected: before the first five choices the residual
orders are 43,39,35,31,27, all at least R(4,5)=25, and a blue K5 is forbidden.
If the red count r is five or six, the entire residual of order 23 or 19 has
no red K4. Removing vertices cannot create one. R(4,4)<=18 supplies enough
blue K4s to bring the total number of four-clique blocks to seven: at most
one is chosen at each of residual orders 23 and 19. Fifteen vertices remain.
The larger red-K4-free residual includes those subsequently selected blue
K4 blocks; it is not merely the final tail.

Choose red triangles greedily from the tail15 until four have been selected
or none remains. At least one exists, because R(3,5)<=14. Here is an elementary
proof of that upper bound using the R(3,4)<=9 proof in h3835. In a coloring of
K14 without a red triangle or blue K5, every vertex has at most four red
neighbors, since five such neighbors would form a blue K5. Thus it has at
least nine blue neighbors. Within those neighbors, R(3,4)<=9 gives either a
forbidden red triangle or a blue K4 extending with the vertex to a blue K5.
This is a contradiction.

If s<4, the entire residual of order 15-3s has no red triangle. At residual
orders 12,9,6 as needed, R(3,3)<=6 then supplies blue triangles to complete
four triangle blocks. The last three vertices cannot form a red triangle,
so t cannot be three. When s=4 there is no condition on that last triple.
This proves the 39-branch list and both residual closure assertions.

This is precisely the consequence of the red-first greedy choices already
implemented by the h3835 normalizer when no external partition is supplied.
The wrapper in `strengthen.py` checks the new branch list and both closure
properties. Ordering blocks by color and sorting each child's signatures
against the root transport the entire graph by a vertex permutation. Each
constrained union consists of whole blocks and is preserved by these
operations. Mixed final triples retain only their shape-preserving swap.
No full-graph automorphism or fixed neighborhood is assumed.

## A coupled finite carrier for the small residual

For s<4 let n=15-3s and k=4-s. The residual consists of k ordered independent
triples in the red graph, followed by the last triple of prescribed red
shape t. It has neither a red triangle nor a blue K5, so it is a
Ramsey(3,5,n) graph.

[McKay's author catalog](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
is explicitly presented as complete for Ramsey(3,5) graphs. It has 32 graphs
at order6, 290 at order9 and 12 at order12. We import that completeness. All
334 entries are checked directly for the two forbidden configurations.
The public copies total 2,636 bytes; source URLs, exact hashes and attribution
are in `catalog-inputs.json`. No assumption about automorphism groups or
absence of duplicate catalog entries is needed for the upper bound.

For a catalog graph G, count ordered partitions

    (B1,...,Bk,T)

of its vertices into triples, where each Bj is independent and T has exactly
t red edges. If this count is P(G,t), the number of bijections from the
specified physical residual to G that respect its fixed internal edges is

    E(G,t) = P(G,t) * 6^k * a(t),
    a(0)=6, a(1)=2, a(2)=2.

There are six bijections for each independent triple. For the final triple,
there are exactly six or two bijections to its specified labeled three-vertex
mask; these small local possibilities are checked by explicit enumeration.
No division by an automorphism group occurs. Different catalog bijections
can represent the same physical graph, and that multiplicity is retained.

The producer uses a recurrence over the remaining vertex subset: choose the
next independent triple, and recurse. The independent checker instead assigns
source vertices to named bins of capacity three, requiring the first k bins
to be independent. It compares each P(G,t), each E(G,t), and all totals,
covering 167,046 ordered partitions. The total embedding covers are:

| Residual order n | t=0 | t=1 | t=2 |
|---|---:|---:|---:|
| 6 | 2,376 | 732 | 492 |
| 9 | 3,220,560 | 1,323,504 | 788,976 |
| 12 | 56,422,656 | 22,584,096 | 11,583,648 |

These are covering counts, not counts of distinct physical graphs.
In particular, the 12-vertex carrier describes edges across **four** tail
blocks simultaneously, and the 9-vertex carrier across **three** blocks.

## The bound for complete 43-vertex branches

Let M_b be the exact rooted h3835 pair-domain count for a surviving branch b.
Let D_b be the product of the old pair-domain cardinalities for all pairs
of blocks entirely inside the small residual. These coordinates use no root
matrix because the root is a four-clique outside the residual.

Let E_b be the applicable catalog covering total, and choose

    C_b = min(D_b,E_b),      for s<4;
    C_b = 1,                for s=4.

The first option retains the old residual matrix carrier; the second uses
all compatible catalog bijections. Each option covers every admissible
residual. Define

    H_b = (M_b / D_b) * C_b,
    H = sum over the 39 refined branches of H_b.

All remaining matrix coordinates use disjoint physical edge sets and retain
the original pair domains and root orderings. Thus H_b is exactly the number
of codes in the chosen whole-graph carrier. The catalog carrier can duplicate
physical graphs; consequently H bounds the number of represented physical
graphs from above. The large-union red-K4 constraints and the remaining
full-graph five-set constraints are additional hard conditions. They are
not silently factored into this count.

Exact integer computations in `GLOBAL_COUNTS.json`, independently recomputed
by multiplying the remaining coordinate factors directly, give

    4 H < M,        6 H < M,        H < 2^785,
    M/H = 6.282136433381775...,

where M is the original exact rooted h3835 family count. The decimal is only
an illustration; the inequalities use arbitrary-precision integers. The
predeclared factor-four gate is therefore met. The branch (5,1,2) has the
least covering count, below 2^752. Its coupled 12-vertex residual changes the
carrier factor from 13,982,193,214,230,528 to 11,583,648, a reduction exceeding
1,207,063,026. Its full43 branch still has all 846 cross edges as physical
decisions and the extra no-red-K4 constraint on 23 vertices.

This is a global existential search reduction under relabeling. It is not a
fraction of actual good43s discarded, an isomorphism census, individually
fixed edge bits, or a measured solver speedup. It is not multiplied into any
cut-rank or distance-sieve denominator.

## Complete target interface and limits

Every refined CNF has the same 846 physical edge variables and one true
constant as h3835. The parent formula still handles all 962,598 physical
five-subsets. For each forbidden smaller clique in a constrained residual,
a new clause says at least one of its physical edges is blue. A clause is
omitted only if an internal fixed blue edge already satisfies it. The
producer and independent physical-edge auditor compare all 106,263 added
clauses in the 39-branch registry; 103,941 involve at least three blocks.

The stronger formula preserves every good43 globally through normalization,
not necessarily within the same old branch label. The 21 removed labels
are therefore **not UNSAT claims** about their old formulas. Similarly,
UNSAT for a refined branch would decide that refined branch, not automatically
its entire older parent branch. Thirty-five retained branches receive new
clauses. Four branches (r=7,s=4,t arbitrary) are unchanged. In particular the
previous UNKNOWN result for (7,4,3) remains UNKNOWN.

`carrier.py` decodes the finite whole43 covering codes, with physical graph
reconstruction and a final target check. Catalog embedding codes have checked
ranking and unranking; a graph itself need not have a unique code. A code
can fail the large residual closure or a global five-set condition. Such
states are explicitly labeled as unverified carrier states, never good43s.
`strengthen.py` supplies the complete physical branch formulas and the greedy
normalizer; no fixed saved residual is imposed as the entire search.

The global forcing proof and the complete CNF cover use h3835's classical
Ramsey premise plus the elementary R(3,5) bound above. The numerical catalog
carrier and its coverage additionally import catalog completeness. The
execution is checked finite Python computation, not proof-assistant
formalization. Greedy maximality is standard; no historical priority is
claimed. No target solver is called, no candidate or branch exclusion is
produced, and the Ramsey lower bound is unchanged.

## Newly shared identical-block normalization

The prepublication refresh found [h3859](../ramsey_r55_global_packing_block_symmetry/PROOF.md),
at source `8978bce98fc64a7b3dc8e2b378a1fe95ca1467b2`, sorting whole nonroot
blocks of identical type by their root-signature keys. Its separately gated
physical application remained UNKNOWN. This is context, not a premise of
the present bound.

The residual closure constraints are invariant under that block action:
the red-K4-free union contains every blue K4 block and every triple block;
the red-triangle-free union, when present, contains every blue triangle
block and the mixed final triple if any. A pure blue final triple belongs
to the same whole union as the other blue triangles. When the final triple
is red, s=4 and the triangle closure condition is absent. Thus a permutation
of identical-type blocks preserves each constrained union. Sorting such
blocks can coexist mathematically with greedy closure. The present formulas
and hashes do not include those additional comparators; a combined generator
would need a separate literal audit. No symmetry factor is multiplied into H.
