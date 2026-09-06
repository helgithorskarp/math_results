# A global seven-vertex motif bound for Ramsey43

Let a graph be *good* if it has neither a clique nor an independent set of
order five. Let P(G) count induced pentagons by their unordered five-vertex
sets. Let J be the join K2 + C5: two adjacent vertices, each adjacent to all
five vertices of an induced pentagon. Let W(G) count unordered seven-vertex
sets inducing J or its complement. Counts are unlabelled occurrences inside
a labeled graph, with each vertex set counted once.

**Theorem.** For every good graph G on 43 vertices, writing d(v) for its red
degree and sigma = sum_v (d(v)-21)^2,

    W(G) >= 903 + 3 sigma + F(G) >= 906,
    52 P(G) >= W(G),
    P(G) >= 18.

Here F is the following explicit nonnegative integer. For every physical
pair e, let q_e count its common neighbors in the color of e, and let N_i
count pairs with q_e=i. Then

    F(G) = 2 sum_{i=0}^8 (9-i) N_i + N_12 + 4 N_13.

All 903 pairs are included, in both colors. Consequently the complete
43-vertex family W<=905 is excluded from the Ramsey target, as is the
complete family P<=17. There is no fixed neighborhood, core, degree profile,
automorphism, input catalog or restriction on the other physical edges.
The theorem does not decide a family with larger counts or improve R(5,5).

The proof consists of a small complete finite lemma followed by global
double counting. The numerical lower bounds are not asserted optimal.

## 1. Two pentagons at order ten

**Finite lemma.** Every triangle-free graph H on ten vertices with
alpha(H)<=4 has at least two distinct induced pentagons. The disjoint union
of two C5s attains two, so this particular ten-vertex bound is sharp.

We use the already proved zero-pentagon case: every triangle/C5-free graph
on ten vertices has an independent five-set. The elementary proof, including
the degree-two/C7 and cubic incidence cases, is in
[the preceding proof, Section 4](../ramsey_r55_induced_pentagon_forcing/PROOF.md).
This is an explicit proof dependency, not an inference from a catalog or an
old SAT result. Full reproduction replays that contribution's compact
checks after validating its pinned file manifest.

Thus H contains a pentagon; label it 0,1,2,3,4 cyclically. Suppose it is the
only pentagon. Any outside vertex has an independent contact set in C5,
so has at most two contacts. If it has two, they are nonadjacent around C5.
The length-three cycle path between those contacts, together with the outside
vertex, makes a second induced pentagon. It has no chord because the only
contacts are its two endpoints. Consequently every outside vertex has
either no contact or exactly one contact with the fixed C5.

Encode the five outside stars by a word of length five on 0,...,5, where 0
means no contact and i>0 means a contact with core vertex i-1. Relabeling
only the outside vertices sorts this word. There are binom(10,5)=252 sorted
words, and all ten pairs among the outside vertices remain arbitrary.
The resulting complete normalized domain has 252*2^10=258,048 physical
graphs. Sorting does not require any automorphism of a final graph: the
same permutation transports the ten arbitrary edge coordinates bijectively.

The compact certificate and the independent exhaustive checker show that
exactly 1,794 of these graphs are triangle-free and have no independent
five-set. Every one has a supplied second pentagon. This contradicts the
unique-pentagon supposition and proves the lemma.

### Finite certificate and independent coverage

Each certificate row is [word_index, outside_edge_mask, second_five_mask].
Words use lexicographic order, outside edge bits use the pairs of 5,...,9 in
lexicographic order, and the last mask names five actual vertices of 0,...,9.
The root five-set has mask 31 and is forbidden as a second witness.

The producer constructs adjacency bitsets for every graph, rejects triangles
by bit intersections, and rejects independent five-sets by recursive search.
It finds a second pentagon by enumerating five-sets.

The checker imports none of the producer. For each sorted word it represents
all 1,024 physical outside edge assignments simultaneously by truth vectors.
It generates every physical triangle condition and every physical independent
five-set condition directly from the 45 pair truth vectors. It requires exact
equality between the resulting admissible graph keys and the certificate
keys, including absence of extra or duplicate keys. For each supplied
five-set it checks all five induced degrees equal two. A simple 2-regular
graph on five vertices must be C5, so this verifies all ten physical pairs.

The checker separately generates all 6^5=7,776 labeled words, checks their
sorting maps and every induced outside edge-coordinate permutation. It also
checks all 32 possible one-vertex stars on a C5: 21 create a triangle, six
have at most one contact, and five supply a second pentagon. Nothing is
omitted on the strength of a generator's search status or a catalog count.

The full ten-vertex lemma includes the zero-pentagon dependency above. The
258,048-case computation alone proves the at-most-one-contact extension
statement; it is not presented as an enumeration of all ten-vertex graphs.

## 2. Elementary order limits

Every graph on six vertices has a triangle or an independent triple: at a
vertex, at least three incident pairs have one color; either a mutual pair
has that color, or those three vertices form a triangle of the other color.

A triangle-free graph on nine vertices with alpha<=3 would have degree at
most three at every vertex. Every set of nonneighbors has alpha<=2 and is
triangle-free, hence has at most five vertices by the six-vertex fact.
Every degree is therefore at least three. A cubic graph on nine vertices
has odd degree sum, which is impossible. Thus R(3,4)<=9.

A triangle-free graph on fourteen vertices with alpha<=4 has maximum degree
four. Its nonneighbors at any vertex are triangle-free with alpha<=3, so
number at most eight. Every degree would therefore be at least five, a
contradiction. Hence a triangle-free graph with alpha<=4 has order at most
thirteen. Its maximum degree is at most four, so its edge count is at most
twice its order and at most 26. These bounds use no imported Ramsey table.

## 3. A hereditary cycle-count bound

Write p(H) for the number of induced pentagons in a triangle-free graph H
with alpha<=4. By Section 2 its order q is at most thirteen. Section 1 gives
p(H)>=2 at q=10. For q>10, sum the pentagon counts over all q vertex-deleted
subgraphs. Every pentagon survives exactly q-5 deletions. Consequently,
if L(q-1) is a valid lower bound, then

    (q-5) p(H) >= q L(q-1).

Integer rounding gives the valid bounds

| q | 0 through 9 | 10 | 11 | 12 | 13 |
|---|---:|---:|---:|---:|---:|
| L(q) | 0 | 2 | 4 | 7 | 12 |

We claim sharpness only at ten; the other entries need not be sharp.
For every q in 0,...,13,

    L(q) = 2(q-9) + f(q),

where f(q)=2(9-q) for q<=8, f(9)=f(10)=f(11)=0, f(12)=1, and f(13)=4.
In particular every f(q) is nonnegative.

## 4. Exact global incidence identity

For each pair e of a good G, let H_e be its common-neighbor graph in the
color of e. H_e has no triangle of that color: such a triangle plus e would
be a monochromatic five-clique. Nor can H_e contain an independent five-set
in that color. Thus Sections 2 and 3 apply to every physical pair, including
blue pairs, with q_e=|H_e|<=13.

A pentagon inside H_e, together with e, induces J in the color of e.
Conversely every induced J or complementary J has exactly one such anchor
pair. For J, its two degree-six vertices are the pair; the five others have
degree four. In the complement, the two degree-zero vertices are the pair
and the others have degree two. There cannot be a second anchor or an
opposite-color anchor on the same seven-set. Since the complement of C5 is
C5, the core is an induced pentagon in G in either case. Therefore

    W(G) = sum_e p(H_e) >= sum_e L(q_e)
         = 2 sum_e q_e - 18 binom(n,2) + sum_e f(q_e).       (1)

Let M count monochromatic triangles of G in both colors. Every such
triangle contributes to three q_e, so sum_e q_e=3M. Counting differently
colored incident wedges gives Goodman's exact identity

    M = binom(n,3) - (1/2) sum_v d(v)(n-1-d(v)).

If D=sum_v (2d(v)-(n-1))^2, completing the square gives

    24 M = n(n-1)(n-5) + 3D.

Substituting in (1), the completely global inequality is

    4 W(G) >= n(n-1)(n-41) + 3D + 4 sum_e f(q_e).          (2)

At n=43, D=4 sigma, so (2) is W>=903+3 sigma+F.
The integer sigma is odd: d^2 is congruent to d modulo two, the total degree
is even, and 43*21^2 is odd. Hence sigma>=1, giving W>=906. We have not
assumed a regular graph or restricted its actual degree sequence.

## 5. Controlling repeated use of a pentagon

For each induced pentagon P define U_R(P) and U_B(P) to be the vertices
outside P joined to every member of P by red and blue pairs, respectively.
In color c, U_c(P) has no triangle: such a triangle joins a c-edge of P to
a c-K5. It has no independent five-set in that color either. Section 2
therefore gives |U_c(P)|<=13 and e_c(U_c(P))<=26.

The anchors using P are exactly the red edges inside U_R(P) and the blue
edges inside U_B(P). Double counting by their core instead of their anchor
gives

    W(G) = sum_P [e_R(U_R(P)) + e_B(U_B(P))] <= 52 P(G).

One may retain the stronger intermediate necessary condition

    W(G) <= 2 sum_P (|U_R(P)|+|U_B(P)|) <= 52 P(G).

Together with W>=906, this proves P>=ceil(906/52)=18. Multiplicity 52 is a
safe upper bound; simultaneous attainability of both 26-edge terms is not
claimed. No division by the ten cycle automorphisms or by the two anchor
orientations occurs anywhere: all the objects counted are vertex sets.

## Scope, controls and trust

This is a computer-assisted finite lemma with an ordinary unformalized
global proof. The proof uses the preceding elementary ten-vertex
zero-pentagon lemma, exhaustive physical coverage of the new unique-pentagon
case, exact integer arithmetic, Python semantics and ordinary hardware.
There is no SAT verdict, floating-point relaxation, external catalog
completeness premise or omitted large certificate. No external peer review
or proof-assistant formalization of the new result is claimed.

The global audit counts W both by all physical pairs and by all pentagons.
Controls independently examine all 2,048 physical eleven-bit extensions of
a rooted C5 on seven vertices, using an adjacency matrix and the complementary
pair. They verify the two-cycle sharp example, all subset-count arithmetic,
and a certified 40-vertex good graph, its complement and a scrambled labeling.
Nine damaged certificates and six malformed edge lists are rejected.

The 40-vertex control has 12,477 pentagons and 7,670 copies counted by W.
These are properties of that smaller example, not target evidence or a
claim that the lower bounds are close to extremal. No new 43-vertex graph,
better defect count, global degree-slice decision, exclusion of all target
graphs or improvement of a Ramsey-number bound follows here. No parked
neighborhood or SAT instance was reopened.
