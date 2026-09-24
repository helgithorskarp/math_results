# A 24-vertex tournament without a strong Seymour vertex

A vertex x is **strong Seymour** if the directed bipartite graph from its
out-neighborhood N+(x) to its *exact* second out-neighborhood N++(x) has a
matching covering N+(x). Exact second neighbors exclude x and N+(x).

## Three cyclic layers

Use indices modulo 3. There are nine clusters A_i, B_i, C_i, of sizes a, b,
c respectively, where a,b,c are positive integers. Orient every cross-cluster
pair uniformly by these rules:

* Each layer is cyclic: A_i -> A_(i+1), B_i -> B_(i+1), C_i -> C_(i+1).
* Every B cluster dominates every A cluster.
* C_i -> A_i, and A_i -> C_j for i != j.
* B_i -> C_i, and C_i -> B_j for i != j.

This nine-vertex quotient is isomorphic to the earlier base D_0 in Austin
Gibbons's constant-nine construction. In our cluster order
(A0,A1,A2,B0,B1,B2,C0,C1,C2), the map to his labels is
(6,4,5,0,2,8,7,1,3). His balanced weights correspond to (a,b,c)=(1,1,3).
The new construction reweights the same quotient to (1,2,5), crossing both
Hall-deficiency thresholds while preserving the previously deficient roots.
We do not claim the quotient itself as new.

Inside every cluster choose any tournament. These rules specify exactly one
direction for every pair of distinct vertices.

**Construction theorem.** If b>a and c>2b, the resulting tournament has no
strong Seymour vertex, regardless of the internal tournaments. In particular,
(a,b,c)=(1,2,5) gives a 24-vertex example. Scaling these parameters gives
examples of order 24t for every positive integer t, with the displayed Hall
deficiencies at least t. Adding a transitive set of vertices that dominates
the whole example gives an example at every order n>=24.

This improves the 36-vertex construction attributed to David Dzitsoev in
Bai--Li--Park, Remark 3.1 of arXiv:2607.18047v2. Together with the separately
accepted graph theorem through order 15, it gives **16 <= m <= 24** for the
minimum no-strong tournament order. The proof here establishes the upper
bound; the lower bound is imported, and 24 is not claimed minimal among all
tournaments. See [SOURCES.md](SOURCES.md).

## Nine Hall witnesses, in three rows

For any root x in the indicated cluster, take S to be the union of the
clusters in the second column. Its neighbors within N++(x) are exactly the
union of the clusters in the third column.

| Root cluster | Source clusters S | Neighbor clusters in N++(x) | Deficiency |
|---|---|---|---|
| A_i | C_(i+1) | B_i, B_(i+2) | c-2b |
| B_i | A_(i+2), B_(i+1), C_i | B_(i+2), C_(i+1) | a |
| C_i | A_i, B_(i+1), B_(i+2), C_(i+1) | A_(i+1), A_(i+2), B_i, C_(i+2) | b-a |

The orientation rules give each row directly. All source clusters are
out-clusters of the root. Their vertices have no arc back into the root's
own cluster. Consequently, internal exact second neighbors create no extra
neighbors of S. All other neighbors of S in N++(x) are the external clusters
shown, with every vertex reached. Thus this table holds for arbitrary
internal tournaments, not just transitive ones.

All three differences are positive under the hypotheses. A matching covering
N+(x) would restrict to distinct neighbors for every vertex of S, contradicting
|S|>|Gamma(S)|. This proves the construction theorem without computation.
At (1,2,5), the witness sizes are 5>4, 8>7, and 10>9, respectively.

For the assertion at every n>=24, old vertices have neither first nor second
out-neighbors in the added dominating set. Every added vertex has all 24 old
vertices as out-neighbors, but those vertices have no out-neighbor in that
vertex's exact second neighborhood. Hence the new vertices are also nonstrong.

## Exact classification of the transitive-fibre family

Now make all nine internal tournaments transitive. Define Delta_X as the
maximum weighted Hall deficiency at the quotient root X, including the empty
source set, with weights a,b,c on the three layers. Then

    Delta_A = max(0, c-2b),
    Delta_B = max(a, 3a-c),
    Delta_C = max(0, b-a).

A vertex with r later vertices in its own transitive cluster has maximum
Hall deficiency r+Delta_X in the expanded tournament. In particular, the
number of strong vertices is exactly

    3 * 1[c <= 2b] + 3 * 1[b <= a].

Thus the transitive family has no strong vertex **if and only if** b>a and
c>2b. Its minimum order is exactly 24, attained only at (a,b,c)=(1,2,5):
a>=1, b>=a+1, c>=2b+1 imply a+b+c>=8, with equality forcing these values.
This minimum is only within the stated family.

Here is a complete calculation of the deficiencies. If I is a set of
out-clusters, let Gamma(I) be its neighbors among the root's exact quotient
second neighbors. Replace I by its closure consisting of all out-clusters
whose neighbor sets are contained in Gamma(I). This preserves Gamma(I) and
can only increase its weight. Therefore only closed source sets are needed.
At index 0 the nonempty closed source sets and their defects are exactly:

| Root | Closed source set | Defect |
|---|---|---|
| A_0 | A_1,C_1,C_2 | c-3b |
| A_0 | A_1,C_2 | -2b |
| A_0 | A_1,C_1 | -2b |
| A_0 | C_1 | c-2b |
| A_0 | A_1 | -c |
| B_0 | A_0,A_1,A_2,B_1,C_0 | 3a-c |
| B_0 | A_2,B_1,C_0 | a |
| B_0 | A_0,A_1,A_2 | 3a-2c |
| B_0 | A_2 | a-c |
| B_0 | A_1 | a-c |
| C_0 | A_0,B_1,B_2,C_1 | b-a |
| C_0 | A_0,C_1 | -b |
| C_0 | A_0,B_1 | b-a-c |
| C_0 | B_1 | b-2a |
| C_0 | A_0 | -c |

For example, these lists can be checked by taking all subsets of the 3, 5,
and 4 out-clusters, respectively, computing their neighbor unions from the
orientation rules, and retaining exactly the fixed points of closure. This
is 56 subsets including the three empty sets. The table, together with the
empty defect zero and positivity of a,b,c, gives the displayed maxima.
The other six quotient roots follow by cyclic symmetry.

To pass from weighted quotient Hall defects to the expanded tournament,
a source subset meeting given external clusters can be enlarged to contain
those entire clusters without changing its external neighbor set. This
can only increase its deficiency. For a vertex with r later internal
vertices, the exact second neighborhood consists entirely of external
clusters. Each of the r internal sources has no neighbor there, whereas the
external matching problem is precisely the weighted quotient problem.
Hence its maximum deficiency is r+Delta_X. Hall's theorem, or equivalently
its maximum-matching deficiency form, proves the classification.

## Asymmetric certificate and its exact bound

The nine clusters need not have equal weights within each layer for the
same nine displayed Hall sets to be useful. Let M be the 9-by-9 signed
incidence matrix of those source sets minus their neighbor sets, in the
order A_0,A_1,A_2,B_0,B_1,B_2,C_0,C_1,C_2. For arbitrary positive integer
cluster sizes w, the sufficient certificate is Mw>=1.

The exact identity

    (1,1,1,4,4,4,3,3,3) M = (1,1,1,1,1,1,1,1,1)

gives sum(w)>=24. Our vector w=(1,1,1,2,2,2,5,5,5) satisfies Mw=1.
Also det(M)=13, so equality in this bound forces this unique vector. The
coefficient identity and determinant are checked with exact rational
arithmetic in verify.py. This proves optimality for these *selected nine
inequalities*, not for every possible Hall certificate on this quotient
and not for unrestricted tournaments.

## Verification and trust

The construction theorem is the explicit orientation and three-row Hall
argument above. The unbounded classification uses the finite symbolic table
and Hall's theorem. Neither result relies on a solver's optimality or an
exhaustive search through all tournaments.

The source includes a 24-by-24 literal adjacency matrix (rows are tails;
entry 1 means the row vertex beats the column vertex), the nine-row JSON
certificate, a constructor, and two separately written verification paths.
The primary checker validates the Hall sets for every vertex, checks the
primal/dual arithmetic, tests arbitrary balanced internal fibres and scale 2,
and rejects malformed and damaged inputs. The independent checker imports
none of that code: it reads the literal matrix, exhausts all 110,592 Hall
subsets across its 24 roots, and compares their maximum defects with direct
maximum matchings. It independently builds the cyclic family and audits the
universal formula for all 216 triples 1<=a,b,c<=6, covering 6,804 vertices.
These finite runs corroborate the universal proof; they do not replace it.

Trust boundaries are the elementary written proof, Hall's theorem, and, for
reproduction, the readable CPython integer/set/Fraction implementations and
standard SHA-256. OR-Tools helped discover quotient weights, but no solver,
external dataset, large certificate, or private input is required to verify
the claims. This is internally checked research, not an independent peer
review or a proof-assistant formalization.
