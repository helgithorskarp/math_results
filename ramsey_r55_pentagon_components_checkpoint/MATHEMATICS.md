# Scope and missing component join

A graph is good if it has no clique and no independent set of order five.
For a graph G, let H(G) be the 5-uniform hypergraph whose edges are exactly
all vertex sets inducing C5. Its incidence components are the connected
components of the graph joining two vertices when they belong to a common
hyperedge. Vertices in no hyperedge are included as isolated components.
These definitions are invariant under every relabeling and color reversal.

## The declared complete split

Class D consists of graphs for which H(G) is disconnected or does not span
all vertices through nontrivial incidence. Class C consists of graphs for
which its support is connected and spans all vertices. Computing all
five-set induced subgraphs assigns every graph to exactly one class.
No selected pentagon, automorphism, or restriction on an edge is imposed.

No member of either complete order-43 class is decided by this package.
In particular, local consistency below is never promoted to feasibility,
and failure to prove consistency is never promoted to an exclusion.

## Coverage bookkeeping, with an external premise

Dyson--McKay, Theorem 1.2 of *Ramsey numbers for regular induced subgraphs*,
[arXiv:2604.08215v3](https://arxiv.org/html/2604.08215v3), states N5=21.
A regular graph on five vertices is I5, C5, or K5. Consequently any induced
C5-free set in a good graph has order at most 20. This is the sole external
premise of the size-profile bookkeeping, and it is a coverage asset only.
The order-20 enumeration is not reproduced; the paper reports the separate
cross-program comparison only through order 15.

Suppose H(G) has k nontrivial components of sizes c1<=...<=ck, and s isolated
vertices. Each ci is at least 5. Taking four vertices from each nontrivial
component and all isolated vertices produces a C5-free induced set: a
pentagon cannot cross different actual incidence components, and cannot
fit inside four selected vertices. Therefore

    s + sum ci = 43,    ci >= 5,    s + 4k <= 20.

The last inequality implies k<=5. The k=0 case is excluded already by the
external premise (and by the independent elementary pentagon-forcing result).
The unordered numerical profiles satisfying these conditions number

    k=1: 17; k=2: 185; k=3: 551; k=4: 608; k=5: 141; total: 1502.

Exactly (s=0,c1=43) represents C; the other 1501 profiles represent possible
D labels. These necessary labels give a complete conditional cover of
hypothetical good43 graphs, not a sufficiency theorem for the labels. No
profile in this cover was retired in this pass. The numerical restriction
is elementary inherited coverage bookkeeping, not claimed as a new
milestone or a new forcing threshold.

## Complete two-pentagon compatibility calculation

Fix two disjoint five-sets A and B and put a labeled induced pentagon in
each. All 25 pairs between them are independent. A cross matrix m uses bit
5*i+j for the edge between B_i and A_j. No quotient or symmetry reduction
is taken: exactly 2^25 matrices are in scope.

Every such ten-vertex graph is good. A clique or independent set uses at
most two vertices from each pentagon, hence has size at most four. To be
eligible as restrictions of two different incidence components, there must
also be no pentagon meeting both A and B.

The generator adds B vertices in their cyclic order. Whenever a new vertex
is added, it checks all five-sets containing that vertex and at least one
A vertex. A five-vertex graph is C5 exactly when all five induced degrees
are two. Rejecting such a prefix is valid under every extension. Conversely,
every mixed pentagon has a last B vertex and is tested at that step. Thus
all surviving full matrices, and only those matrices, have no mixed C5.

The exact prefix counts, including the empty prefix, are

    1, 22, 454, 8138, 103790, 344282.

The independent checker takes a different route. It explicitly generates
the twelve labeled five-cycles and places them on every mixed five-set.
Matching their internal A and B edges against the fixed cycles leaves 250
distinct forbidden partial cross assignments. It evaluates their union as
an exact Boolean truth vector on all 2^25 assignments. It compares every
bit of the complementary vector with the generator's matrix list, rejecting
out-of-range values and duplicate matrices. This comparison verifies all
local assignments, not just counts or selected witnesses.

There is at least one survivor for each number of cross edges from 0 to
25. All matrices have fewer than 2^25, all adjacency masks fewer than 2^10,
and all prefix/leaf counts fewer than 2^26. Unsigned bit arithmetic in the
producer is therefore within its declared integer domains.

This is an exact local catalogue. It does not classify incidence components
of size larger than five and does not settle the declared class D.

## Why even four-component joins are insufficient

Use the familiar lexicographic product Q=C5[C5] strictly as a control. Its
vertices are (i,j) in {0,...,4}^2. Within one bag i, use the inner pentagon;
between different bags, use the color of the outer pentagon pair.

Q is good: a monochromatic clique uses vertices from at most two outer
bags, and at most two vertices of each inner pentagon. Thus its order is
at most four in either color.

C5 has no proper module of size 2,3,4. If an induced pentagon in a substitution
graph uses several vertices from one bag and a vertex outside it, those
same-bag vertices would be a proper module of the pentagon. It follows that
every pentagon in Q either lies in one bag or uses five distinct bags.
In the latter case every choice of one vertex from each bag is a pentagon.
Hence Q has exactly 5 internal and 5^5=3125 transverse pentagons.

All thirty nonempty proper subsets of the five bags have only the internal
pentagons of their constituent bags. In particular all restrictions to two,
three, and four proposed bags treat them as separate incidence components.
Nevertheless the full incidence 2-section of Q is K25: same-bag pairs lie
in the internal pentagon, and cross-bag pairs lie in transverse pentagons.
The proposed bags are not components of the full object.

The checker examines all 53,130 physical five-sets of Q, verifies the absence
of monochromatic fives, classifies every pentagon, and verifies every proper
bag restriction. It also checks the 25 proper candidate modules in C5
against the literal definition. This control does not need the external
N5 theorem and does not assert that Q extends to order 43.

Therefore a join that only demands the declared decomposition on all unions
of at most four proposed pieces is invalid, even for a physical good graph.
A valid complete-component inference must also account for pentagons meeting
five pieces, their actual compatible pair colors, and all monochromatic
five-set restrictions. The catalogue here supplies none of that terminal
coverage. The control disproves that truncated join, not the possibility
of a future stronger all-pentagon obstruction.

## Research outcome

The component partition is exact as a definition; the local enumeration is
complete in its ten-vertex scope; the intended whole-class exclusion is
unproved. There is no certificate joining this work to nonexistence on 43
vertices. No new Ramsey bound, target graph, excluded D profile, or terminal
all-pentagon milestone follows. Source publication records this failure
without promoting it into a mathematical campaign claim.

The preceding pentagon-product exclusion, physical formulas, maximal-packing
queues, moment/PSD and separator archives are preserved and are not resumed.
The same C5[C5] object appears in the earlier
[deleted-product package](../ramsey_r55_deleted_pentagon_product/README.md);
its previous extension theorem is not a premise of this argument.
