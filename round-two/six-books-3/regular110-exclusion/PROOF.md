# Four-column packing forces Petersen and excludes 110 red edges

Actual author **six-books-3**, role **researcher**, 2026-10-01.

## Statement and credited inputs

A coloring is **valid** if it has no ordinary red book B4 and no ordinary blue
book B7. Equivalently, every red edge has at most three common red neighbors
and every blue edge has at most six common blue neighbors. Books are not required
to be induced.

**Theorem.** There is no valid coloring of K22 whose red graph is ten-regular.
Consequently every valid coloring of K22 has at most 109 red edges.

The regular conclusion uses these committed inputs:

1. [Triangle-free red neighborhoods, lemma 8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md),
   artifact `bafkreieph2tyeefsbslbsfvs2jtv546shufx4ar3stjhca5c72lql37o4a`.
   A ten-regular valid graph on 22 vertices has triangle-free red neighborhoods.
2. [Complete local-fourteen exclusion, lemma 8638](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/local14-exclusion/PROOF.md),
   artifact `bafkreidkxsdjhx2pheg3xcq5ujblspc2l4gi5fftsj623vb7pmb2g47we4`.
   Every red edge of such a graph has exactly three common red neighbors.
   This credits the earlier positive-codegree and neighborhood-floor results
   specified in that source; those global inputs remain dependencies here.
3. J. I. Hall, *Locally Petersen graphs*, Journal of Graph Theory **4** (1980),
   173–187, [doi:10.1002/jgt.3190040206](https://doi.org/10.1002/jgt.3190040206).
   Hall's existing theorem classifies all connected locally Petersen graphs.

The edge-bound consequence additionally uses
[maximum red degree ten, lemma 8012](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md),
artifact `bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi`.
Its degree bound is imported, not reproved here.

## 1. The miss-incidence identities

Suppose G is a hypothetical ten-regular valid red graph on 22 vertices. Fix a
vertex v. Put A=N_R(v), of size ten, and let B be its eleven blue neighbors.
The graph J=G[A] is cubic by 8638 and triangle-free by 8541.

For i in A put W_i=B minus N_R(i). Since i has red neighbors v, three in A,
and therefore six in B,

    |W_i|=5.                                                   (1)

For b in B put Z_b={i in A : b in W_i}. These are arbitrary binary ten-point
rows; no size bound, enumeration or condition on G[B] will be needed. Define
S_ij=|W_i intersect W_j| for distinct i,j in A, and c_ij=|N_J(i) intersect N_J(j)|.

If ij is red, its common red neighbors are v, its c_ij common neighbors in A,
and its common red neighbors in B. The last count is

    11-|W_i union W_j| = 1+S_ij.

Thus red-book avoidance gives S_ij<=1-c_ij; because J is triangle-free,

    S_ij<=1 on a red J pair.                                  (2)

If ij is blue, the common blue neighbors in A number
8-(3+3-c_ij)=2+c_ij. The common blue neighbors in B number S_ij; v is red
to both endpoints. Blue-book avoidance gives

    S_ij<=4-c_ij on a blue J pair.                             (3)

These are ordinary common-neighbor counts. No positive-semidefinite assertion
about a capped Gram matrix is used.

## 2. Four columns rule out every local four-cycle

For any four-set L in A, write t_b=|Z_b intersect L|. From (1),

    sum over b in B of t_b = 20,
    sum over unordered pairs ij in L of S_ij = sum_b binom(t_b,2).

For each integer t from zero through four,

    binom(t,2)-t+1 = (t-1)(t-2)/2 >= 0.

Summing over the eleven rows gives the general four-column inequality

    sum over pairs ij in L of S_ij >= 20-11 = 9.               (4)

Suppose J has a four-cycle on L. Triangle-freeness rules out its two chords.
Its four red edges each have capacity at most one by (2). Each of the two
opposite blue pairs has at least two common J neighbors, so has capacity at
most two by (3). Therefore

    sum over pairs ij in L of S_ij <= 4+2+2 = 8,               (5)

contradicting (4). Hence J has no four-cycle. This argument covers every
four-set, every choice of root, and every binary miss-incidence matrix.

## 3. The elementary Moore construction identifies Petersen

Choose a vertex r of the cubic, triangle-free, four-cycle-free graph J. Its
three neighbors x1,x2,x3 are independent. Each xi has two other neighbors.
All six of these points are distinct: overlap would give a four-cycle through
r; a point among the other xj would give a triangle. The ten points have now
all been accounted for.

Each of the six remaining points is adjacent to exactly one xi. Another such
adjacency would again give a four-cycle through r. Its two other neighbors
therefore lie among the six points. Their induced graph is a simple
two-regular triangle-free graph on six points, hence a single six-cycle.
The two points attached to any xi cannot be adjacent along that cycle
(a triangle through xi), or at cycle distance two (a four-cycle through xi).
They must be opposite. Thus the three opposite pairs on this six-cycle are
attached to x1,x2,x3, which are attached to r. This uniquely describes the
Petersen graph, equivalently the graph on two-subsets of a five-set with
adjacency when the subsets are disjoint.

Every red neighborhood of G is therefore Petersen.

## 4. Hall's known classification closes the regular case

The red graph G is connected. Indeed, if a red connected component has order s,
the two sets of nine neighbors other than each other on any red edge lie in
its s-2 other points. Their intersection is at least 18-(s-2)=20-s.
Red-book avoidance bounds this intersection by three, giving s>=17.
Every ten-regular component contains an edge; two such components cannot fit
in 22 points.

Hall's theorem applies to this connected graph with Petersen at **every**
vertex. Its three possibilities have orders 21, 63 and 65. To make the
literature bridge directly readable, A. M. Cohen's primary survey,
[*Local recognition of graphs, buildings, and related geometries*](https://ir.cwi.nl/pub/2362/2362D.pdf)
(1990), printed page 87, states Hall's proposition and identifies the models
as the complement of J(7,2), its three-cover, and the graph on 65 specified
involutions. The first order is binom(7,2)=21 and its three-cover has 63 points.
None has 22 points. This is the required contradiction.

The local-to-global classification is an imported 1980 theorem, not a new
classification claim or a computational certificate. The publisher's abstract
and Cohen's complete proposition were rechecked live on 2026-10-01. The original
journal PDF did not load in this session; no replay of Hall's proof is claimed.

Finally, 8012 bounds every red degree by ten. A 22-vertex graph with 110 red
edges would have degree sum 220 and hence every degree ten, just excluded.
Thus every valid 22-vertex graph has at most 109 red edges.

## Validation, novelty and limits

The new contribution is the four-column obstruction, its locally Petersen
reduction, and the resulting regular-case/109-edge consequences after crediting
the specified campaign lemmas and Hall's theorem. The regular exclusion was
not found in the bounded relevant committed graph or searched primary Book
sources. No claim of priority over all literature is made.

Two exact standard-library implementations reproduce the known six connected
triangle-free cubic ten-point graphs from the primary
[House of Graphs graph6 list](https://houseofgraphs.org/data/cubics/Generated_graphs.10.04.g6).
The first uses eight rooted cross-incidence profiles and 11 rooted classes;
the second compares all normalized labels with all 21,780 forward-star graphs.
The five non-Petersen classes each have an explicit four-cycle of capacity
seven or eight; the Petersen class has none. A separate integer DP obtains
the packing minimum nine. The proof above requires neither census nor solver.
The included checks also reproduce the primary 21-vertex construction exactly.

The ordinary bridges here are unformalized. The earlier imported 8638 remains
computer-assisted; the code here does not reverify it. Independent review of
this new contribution is pending. No valid coloring on 22 points is constructed,
and irregular graphs with at most 109 red edges remain unresolved. The current
primary literature bound **22 <= R(B4,B7) <= 23** is unchanged:
[Lidicky et al., Table 1](https://arxiv.org/pdf/2407.07285) and
[Radziszowski's survey, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
