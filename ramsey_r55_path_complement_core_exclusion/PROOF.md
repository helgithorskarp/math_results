# Complete exclusion of a hereditary core class

Let C be the class of finite simple graphs with no induced five-vertex path
P5 and no induced complement of P5. In particular, the word "path" below
always means an induced path. Let f(a,b) be the largest order of a graph in
C with clique number at most a and independence number at most b.

For 1 <= a,b <= 4 the exact values are

| a \ b | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| 1 | 1 | 2 | 3 | 4 |
| 2 | 2 | 5 | 7 | 10 |
| 3 | 3 | 7 | 11 | 16 |
| 4 | 4 | 10 | 16 | 25 |

The order-25 graph in the last cell is unique up to isomorphism: C5[C5],
the substitution of a five-cycle for each vertex of a five-cycle.

Consequently, **every induced subgraph on 26 vertices of a hypothetical
good43 contains a P5 or its complement**. Equivalently, deleting at most
17 vertices can never put a good43 into C. This excludes the complete
43-vertex class with a 26-vertex C core and arbitrary remaining edges.
No automorphism, degree profile, fixed parent, or chosen neighborhood is
assumed. This is not a proof that a good43 exists or that all good43s are
impossible. Extensions of the order-25 equality graph are not decided here.

## 1. Structural inputs and a prime quotient

We import Fouquet's theorem: a graph in C is either C5-free, is C5, or
has a proper homogeneous set (module). A module is a set M such that every
vertex outside M is complete or anticomplete to M; proper means
2 <= |M| < |V(G)|. The precise input is Theorem 2.1 in
[Chudnovsky, Esperet, Lemoine, Maceli, Maffray and Penev,
Graphs with no induced P5 or complement-P5, 2014](https://web.math.princeton.edu/~mchudnov/decompP4CP4.pdf),
which attributes it to [Fouquet, 1993](https://www.sciencedirect.com/science/article/pii/0012365X93905396).
Neither proof is rerun or formally verified by this package.

A C5-free member of C is perfect: an induced cycle of length at least
six contains a P5, and an induced complement of such a cycle contains a
complement-P5. Thus it has no odd hole or odd antihole. We import the
[Strong Perfect Graph Theorem, Theorem 1.2](https://annals.math.princeton.edu/wp-content/uploads/annals-v164-n1-p02.pdf)
for this implication. Perfect means that every induced subgraph has
chromatic number equal to clique number. This substantial classical
theorem is an explicit trust boundary, not a computational conclusion here.

For any G in C with at least two vertices, partition V(G) into nonempty
modules M_i, with at least two parts, minimizing the number of parts.
Such a partition exists (singletons suffice). Its quotient Q records the
uniform adjacencies between parts. If Q had a proper module, merging the
corresponding parts would contradict minimality. Hence Q is prime.
Choosing one representative from each part shows Q is in C. The two
imported facts imply that Q is either perfect or C5.

Write a=omega(G), b=alpha(G), p_i=omega(G[M_i]), q_i=alpha(G[M_i]).
The exact substitution identities are

    a = max over cliques K of Q of sum_{i in K} p_i,
    b = max over stable sets S of Q of sum_{i in S} q_i.       (1)

Indeed a clique (respectively stable set) meets only a clique (respectively
stable set) of quotient parts, and maximum sets in compatible parts can
be united. All p_i,q_i are positive. Also (p_i,q_i) != (a,b): a vertex
outside the proper part M_i would increase p_i if complete to it, or q_i
if anticomplete. Thus p_i+q_i < a+b. This strict decrease is what makes
the finite induction valid; we do not assume away a difficult large part.

## 2. Weighted perfect-quotient inequality

When Q is perfect, (1) implies

    sum_i p_i q_i <= ab.                                    (2)

Here is the classical replication argument, included to justify the weights.
Replicating a vertex v means adding an adjacent twin v'. Replication
preserves perfection. To see this by induction on the graph order, all
proper induced subgraphs containing the twins are perfect by induction;
the others are induced subgraphs of the original perfect graph. In a
perfect graph take an optimal color class S containing v. In the replicated
graph S meets every maximum clique: a maximum clique containing v'
contains v as well, while a maximum clique avoiding v' either has original
maximum size and meets S, or cannot have the larger replicated maximum
size. Deleting S reduces the clique number, and the perfect proper
induced remainder can be colored optimally. Adding S gives an optimal
coloring of the whole replicated graph. This proves the induction.

Replace vertex i of Q by a clique of p_i twins. The resulting perfect
graph has clique number a by (1), so it has an a-coloring. For each color
class, its supporting vertices in Q form a stable set, and the sum of
their q_i is at most b. Vertex i occurs in exactly p_i different color
classes. Summing gives (2). No irrational, fractional, or numerical
optimization is involved. Applying (2) to a nonperfect quotient would be
incorrect: for C5 with all weights one its left side is 5 and ab=4.

## 3. A closed exact induction

Let F(a,b) denote the entries of the displayed table. For (a,b)!=(1,1) set

    rho(a,b) = max F(p,q)/(pq),
               1<=p<=a, 1<=q<=b, (p,q)!=(a,b).             (3)

For (1,1) the maximum is empty and is set to zero. Assume all smaller
parameter sums have been proved. In a perfect quotient, (2) and the
proper-part observation give

    |G| = sum_i |M_i| <= sum_i F(p_i,q_i)
         <= rho(a,b) sum_i p_iq_i <= rho(a,b) ab.            (4)

In a C5 quotient, number the parts cyclically by i in Z/5Z. Equation (1)
gives exactly the needed restrictions

    p_i+p_{i+1} <= a,     q_i+q_{i+2} <= b.                 (5)

Every p_i is between 1 and a-1, and every q_i between 1 and b-1. Thus the
cycle contribution is at most the maximum of sum_i F(p_i,q_i) over the
finite vectors (5). All child entries have smaller parameter sum.
The singleton case supplies 1. The arithmetic certificate checks

    F(a,b) = max(1, floor(ab rho(a,b)), cycle maximum).     (6)

This is a valid upper-bound induction for all graphs, using their actual
clique and independence numbers. The displayed table is coordinatewise
nondecreasing, so it also bounds graphs specified using upper caps.

The nontrivial rows, up to transposing colors, are:

| (a,b) | rho | perfect bound | cycle bound | admissible vectors |
|---|---:|---:|---:|---:|
| (2,2) | 1 | 4 | 5 | 1 |
| (2,3) | 5/4 | 7 | 7 | 11 |
| (2,4) | 5/4 | 10 | 10 | 57 |
| (3,3) | 5/4 | 11 | 11 | 121 |
| (3,4) | 5/4 | 15 | 16 | 627 |
| (4,4) | 4/3 | 21 | 25 | 3249 |

[TABLE.json](TABLE.json) records all 16 rows and **every** maximizing
labeled pair of cycle vectors. The producer enumerates vectors separately
at each cap. The independent checker instead visits all 3^10=59,049
ten-coordinate vectors, computes weighted maxima over all literal cliques
and stable sets of C5, and filters at four. There are 3,249 admissible
vectors and 4,761 incidences with cap rows. Rational envelopes are checked
by integer cross multiplication. Maximizing vectors are compared entry
by entry, including the unique top vector p=q=(2,2,2,2,2).

The asymmetric value 16 matters: the trial bound F(3,4)<=15 is false.
Two C5 parts and three independent pairs arranged on C5 attain 16. This
is why rho(4,4) is 4/3, not 5/4. The checker rejects the false bound 15.

## 4. Attainment and unique equality at 25

For a=1 use b independent vertices; for b=1 use a clique. For every other
table cell a maximizing cycle vector attains F(a,b) by substituting the
previously constructed graphs of types (p_i,q_i). The exact adjacency
words and substitution trees of all 16 witnesses are in
[WITNESSES.json](WITNESSES.json). Each is checked directly for its order,
clique and independence numbers, and for absence of both forbidden paths.
Thus attainment does not depend on assuming that a count vector is a graph.
These are small boundary graphs, not good43 candidates or extension claims.

At (4,4), a perfect quotient has order at most 21, strictly below 25.
The unique maximizing cycle vector has every part of type (2,2), and
equality forces each part to have five vertices. A graph on five vertices
with no triangle or independent triple is C5: every vertex has degree
at most two and at least two, and the only simple 2-regular graph on five
vertices is C5. Hence equality is exactly C5[C5]. The supplied labeled
graph has 25 vertices, 150 edges and degree 12 at every vertex. Its
53,130 five-sets contain neither a monochromatic K5 nor either forbidden
path. This standard iterated-cycle construction is not claimed new.

## 5. Complete physical family and handoff

Given a full graph on 43 labeled vertices and a specified 26-set S, the
family condition is G[S] in C. All edges touching the other 17 vertices
are arbitrary. If the full graph were good, G[S] would have omega,alpha<=4,
contradicting |S|=26>25. This is a complete class exclusion; there is no
remaining aggregate survivor, capped solver status, or unexamined case in
this implication.

Every good43 therefore needs at least 18 vertex deletions to remove all
induced P5 and complement-P5 copies together. It also has four vertex-
disjoint copies from this pair of patterns: greedily remove one while
43,38,33,28 vertices remain, each more than 25. These are immediate global
forcing corollaries, not a new carrier enumeration or a solver experiment.

[interface.py](interface.py) inspects all five-sets of a supplied core.
It returns either a literal path certificate proving that this core is
outside the excluded class, or a monochromatic-five certificate after
confirming the whole core is in C. The former gives no target verdict and
does not decide whether another 26-set is in C. The latter independently
certifies that the full physical graph fails good43.
[verify_certificate.py](verify_certificate.py) checks all ten relevant
physical pairs using a separate closed-form pair index.

No physical packing task is claimed solved by this contribution; all
2,189,178 h3887 tasks remain undecided. No density percentage or search
runtime improvement is inferred. The h3897/h3909 connectivity theorem and
its accepted reviews remain valid complementary evidence, not premises.
The h3921 failed triangle-support gate remains parked. This closes the
declared class decision before any other forbidden-pattern phase.

The result is a finite specialization of classical hereditary-graph
decomposition, with a reproducible target-facing consequence. No historical
priority, independent peer review, or proof-assistant formalization is claimed.
