# Physical three-card joins: exact scope and a failed shortcut

This note records a failed endpoint approach, not an improvement to R(5,5).
Write `good(s,n)` for a red/blue colouring of the pairs of an n-element set
with no monochromatic s-set, and `goodn` for `good(5,n)`. Red pairs form a
simple graph; a blue clique is an independent set of that graph.

## 1. Three actual cards suffice when their omitted labels are mixed

**Lemma.** Suppose a,b,c are distinct vertices of G, their induced triangle
has both colours, and G-a, G-b, G-c are good(s,n-1). Then G is good(s,n).

**Proof.** A monochromatic s-set of G would have to contain a, b and c:
if it omitted any one of them, it would occur in the corresponding good
card. Containing all three contradicts the mixed triangle. This proves
the assertion. Conversely all cards of a good graph are good. Thus these
three physically compatible cards certify all remaining cards as well.

Every good44 contains an induced red P3. Indeed, a P3-free graph is a
disjoint union of cliques: a shortest path between two nonadjacent vertices
in a connected component would start with an induced P3. Each clique in a
good graph has size at most four, and there are at most four components
(one vertex from five components is a blue K5). Such a graph has at most
16 vertices. Consequently an arbitrary hypothetical good44 can be labelled
with anchors a,b,c such that ab and bc are red and ac is blue. This uses
neither a graph automorphism nor a selected symmetric family.

The basic deletion-cover argument is elementary and overlaps the principle
in Lehavi's Theorem 1; see DEPENDENCIES.md. No priority claim is made.

## 2. The complete physical star relation

Fix any good(s,n-3) core H with vertex set V. A star S is the subset of V
joined in red to one new vertex; all other new-to-core pairs are blue.
Let F(H) consist of all S such that

1. H[S] has no red K_(s-1), and
2. H[V\S] has no blue K_(s-1).

These are exactly the stars whose one-vertex extensions are good. Define
two symmetric relations on the entire F(H):

    R(S,T) iff H[S intersection T] has no red K_(s-2),
    B(S,T) iff H[V\(S union T)] has no blue K_(s-2).

If two new vertices have stars S,T and their mutual pair is red, their
two-vertex extension is good exactly when R(S,T) holds. A forbidden set
using neither or only one new vertex is already ruled out. A forbidden
set using both must be red, and its remaining s-2 vertices lie in S
intersection T. The blue version is identical with common blue neighbors.

**Exact whole-target equivalence.** A good44 exists if and only if there is
some good41 H and stars A,B,C in its full domain F(H) with

    R(A,B), R(B,C), B(A,C).                       (1)

For necessity choose the red P3 in Section 1 and delete its three vertices.
For sufficiency add the red P3 with these stars. The three pair conditions
make the three good43 cards good, and Section 1 applies. Equivalently, a
direct forbidden-set check partitions according to the number of anchors:
zero is checked in H, one in F(H), two by the three relations, and three
is impossible because the root triangle is mixed.

No catalogue is part of (1), and no restriction on H or its order-41
isomorphism type is permitted. All 44 deletions are simultaneous in the
resulting labelled graph; an abstract deck of unrelated cards would not
suffice. However, this equivalence by itself does not decide existence.

An exact terminal obstruction would prove, for **every** good41 H and
**every** blue-compatible pair A,C in F(H),

    N_R(A) intersection N_R(C) = empty.           (2)

The pass did not establish (2), a complete core cover for checking it, or
a near-term bound on that work. The reduction still has 820 core pair
bits and 123 attachment bits, all 943 physical bits left after fixing a
red P3 in the order-44 problem. This is a representation count, not a
complexity lower bound or a claim that a faster argument is impossible.

## 3. A uniform physical counterexample to arc consistency on subdomains

Here arc consistency means: each retained value at each of the three
anchors has some compatible retained value at each neighboring anchor.
This is stronger than merely having three nonempty pair relations.

**Proposition.** For every s>=5 there is a good(s,4s-8) core H and prescribed
two-element star domains at the three anchors of a red P3 such that:

- Every retained star is unary valid.
- Each retained value has a support in each of the two other domains.
- The three exact physical pair relations have no common triple.
- The same core nevertheless has a good(s,4s-5) extension if an omitted
  unary-valid star is allowed.

This is a counterexample for prescribed **subdomains** of F(H), not for the
entire F(H), and not an order-44 obstruction. Path consistency detects it.

### Construction and validity of the core

Put k=s-2. Take four disjoint bags R0,R1,W0,W1 of size k, labelled by
indices 0,...,k-1. The red edges are precisely:

- All pairs within each R bag.
- The matching R0_i R1_i.
- All pairs between W0 and W1; neither W bag has internal red edges.
- The matching Rr_i Ww_i for each r,w in {0,1}.

All other pairs are blue. Thus H has 4k vertices and 2k^2+4k red edges.

Its blue clique number is k. Such a clique contains at most one vertex
from each R bag, and vertices from at most one W bag. If it contains one
R vertex, that index is forbidden in its W bag. If it contains two R
vertices, their indices differ (the matching is red), and both indices
are forbidden in its W bag. In each case its total size is at most k.
An entire W bag attains k.

Its red clique number is max(k,4). A clique without W vertices has size
at most k, unless it spans both R bags, in which case it has at most two
vertices. A clique using W vertices has at most one from each W bag;
any R vertices in it must share the index of each W vertex. It therefore
has at most two R and two W vertices. Four vertices of one common index,
one per bag, attain four, and an R bag attains k. Because k>=3,
max(k,4)<=k+1=s-1. The core is good(s,4k).

### The domains and their exact relations

For i in {0,1}, set

    A_i = R_i union W_(1-i),
    B_i = R_i.

Give a and c the domain {A_0,A_1}, and b the domain {B_0,B_1}.
Every one of these stars is unary valid. In an A_i red neighborhood,
the R clique has size k, the W bag is independent, and cross edges form
a matching, so the largest red clique is k. The complement is the same
type of two-bag graph and has blue clique number k. A B_i red neighborhood
is K_k, and its blue neighborhood is an induced subgraph of H, whose blue
clique number is k. All relevant clique sizes are below s-1=k+1.

For the red pair ab, identical bits i at a and b put the red K_k R_i in
the common red neighborhood, making a red K_s with a,b. Different bits
give an empty common red neighborhood. Thus ab is compatible exactly
when its two bits differ. The red pair bc has the same relation.

For the blue pair ac, identical bits i leave the blue K_k W_i in the
common blue neighborhood. Different bits give complementary stars A_0
and A_1, so the common blue neighborhood is empty. Thus ac too is
compatible exactly when its two bits differ. All three exact relations
are the matrix

    0 1
    1 0.

Every value has its opposite as a support in each other domain. But
three binary values cannot be pairwise different. All eight possible
triples fail. A literal forbidden-set witness is R_i together with ab
when a=b=i, R_i with bc when b=c=i, and otherwise W_i with ac (then a=c=i).
Each witness has size k+2=s. This proves the first three conclusions.

### Why this does not obstruct the full star domain

The empty star is unary valid: it has no red neighbors and H has no blue
K_(s-1). Use A_0 at a, the empty star at b, and A_1 at c. Both common red
neighborhoods are empty, and the common blue neighborhood of a,c is
empty. Section 2 gives a good(s,4k+3) graph. This proves the last conclusion
and shows why dropping the subdomain qualification would be false.

For s=5 the control has a 12-vertex core with 30 red edges, four distinct
unary-valid stars on 13 vertices, six valid pair graphs on 14 vertices,
and no valid triple in the prescribed domains on 15 vertices. The
positive control is a good15. These orders have no claimed connection
to excluding the good41 cores required by the order-44 target.

## 4. What the pass decides

The physical join (1) covers the entire target, but (2) remains unproved.
The uniform proposition rejects the proposed generic shortcut that arc
consistency on physical star subdomains would close a join. It does not
reject full-domain arc consistency specifically at order41, all stronger
propagation, or a future complete core decomposition. The existing
committed three-block gluing result had already rejected pairwise
nonemptiness; the present counterexample is a physical realization of
the familiar binary odd-cycle obstruction at the stronger arc-consistency
level. It is not presented as a paper-scale Ramsey advance.

No good44 was found, no complete order-44 class was excluded, and no
quantitatively finishable complete-class reduction was demonstrated.
The second and final contracted deletion-lift gate is therefore **not met**.
The two-pass program is preserved and stopped. Reassignment within
R(5,5), rather than another consistency-level extension, is recommended.
