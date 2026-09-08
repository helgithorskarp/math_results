# Forced induced paths in Ramsey43 neighborhoods

All graphs are finite and simple. A good43 graph has 43 vertices and contains
neither a clique of size 5 nor an independent set of size 5. Here a path always
means an **induced** path; P5 has five vertices, four edges, and six nonedges.

## Imported result and the complete finite bridge

We use Theorem 7 of Kathie Cameron, Jan Goedgebeur, Shenwei Huang, and Yongtang
Shi, [*k-Critical Graphs in P5-Free Graphs*, arXiv:2005.03441v1](https://arxiv.org/html/2005.03441):
every 5-vertex-critical graph with no induced P5 and no K4 is isomorphic to one
of the two graphs G1 and G2 in that paper's Appendix. Their adjacency lists,
on 13 and 14 vertices respectively, are transcribed in `INPUTS.json`.
The published classification includes computer-assisted steps and is an
imported theorem, not a computation reproduced by this package.

**Lemma.** Every 18-vertex graph with neither a K4 nor an independent 5-set
contains an induced P5.

**Proof.** Suppose H is a counterexample. Every color class of a proper
vertex coloring has size at most 4. Thus H cannot be colored with four colors,
since 18 > 4*4. Choose an inclusion-minimal vertex subset S for which H[S] is
not four-colorable. Deleting any vertex makes it four-colorable; giving that
vertex a new color shows that H[S] is five-colorable. Consequently H[S] is
5-vertex-critical. It remains P5-free and K4-free, so the imported theorem
identifies H[S] as G1 or G2.

Relabel S as the first 13 or 14 vertices. Every edge not contained in S is
free in the corresponding formula in this package. The two formulas are
unsatisfiable, as established by the audited encodings and the accompanying
RUP proofs. Thus neither complete extension family contains H. This is a
contradiction. This argument covers disconnected H as well. QED.

## Exact encoding and proof certificates

For each case, fix only the edges and nonedges inside the specified core.
Every other unordered pair in the 18-vertex graph is a separate Boolean
variable: true means edge. Variables follow lexicographic pair order. There
are 75 variables for G1 and 62 for G2. No auxiliary variables, degree bounds,
symmetry clauses, restrictions on the new vertices, or restrictions on the
complementary induced path are imposed.

For every four-set, add the clause containing the negatives of its six edge
variables, forbidding a K4. For every five-set, add the disjunction of all
ten edge variables, forbidding an independent set. For every one of the 60
undirected Hamiltonian paths on each five-set, add the clause with negative
literals on its four path edges and positive literals on its six other
pairs. It forbids exactly that induced path pattern. Substitute all fixed
core values, discard satisfied clauses, remove false constant literals, and
deduplicate. These operations preserve the full extension family exactly.

`build.py` generates path patterns from permutations. `audit.py` independently
classifies all 1,024 five-vertex edge words using degrees and connectivity,
then reconstructs the entire clause set directly from the forbidden truth
patterns. Its exact set comparison checks both missing and extra clauses.
Both cores themselves have zero K4, independent-five, or induced-P5
obstructions, so neither conclusion is a trivial inconsistent-core encoding.

| Core | Free physical pairs | Distinct clauses | RUP additions | Text proof bytes |
| --- | ---: | ---: | ---: | ---: |
| G1 | 75 | 57,596 | 275 | 7,898 |
| G2 | 62 | 34,197 | 77 | 1,434 |

One CaDiCaL call per formula returned UNSAT, with limits of 500,000 conflicts
and 600 seconds. The two binary DRAT proofs passed drat-trim. The committed
text versions preserve all additions and deletions; they also pass drat-trim.
`check_rup.py` checks every addition by reverse unit propagation, without a
solver or native library. It deliberately retains deleted clauses, which is
sound: a clause already justified by the original formula may continue to be
used in later implications. All additions are RUP; no general RAT inference
is needed. The final added empty clause certifies unsatisfiability.

The hashes and expected clause/proof counts are in `EXPECTED.json`;
`VALIDATION.json` records tools and discovery receipts. The formula generator,
independent formula audit, and RUP verifier use exact integer/Boolean logic.
This remains a checked computational proof with an imported classification,
not a formal proof-assistant development.

## Global physical consequence

Let G be any good43 graph and v any vertex. The classical upper bound
[R(4,5) <= 25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf) gives
18 <= d_G(v) <= 24: a neighborhood with 25 vertices would contain a K4
or independent 5-set, and applying the same argument in the complement
bounds the nonneighborhood by 24.

The graph induced by N_G(v) has no K4, because adjoining v would give a K5;
it also has no independent 5-set. The lemma therefore implies:

**Theorem.** Every 18-vertex subset of every neighborhood in a good43 graph
contains an induced P5. The same statement holds in the complement.

In particular, every vertex has an induced P5 among its neighbors in each
color. Hence there is no good43 graph whose red graph is P5-free, and no
good43 graph whose blue graph is P5-free. These are complete global families:
there is no fixed core, symmetry, seed graph, or repair radius in the statement.
More strongly, a P5-free induced subset of a neighborhood has at most 17
vertices, so deleting vertices to remove all induced P5s from that neighborhood
requires at least d_G(v)-17 deletions.

There is also a direct incidence count. If p(v) counts induced P5 five-sets
inside a neighborhood of size d, count pairs (T,P), where |T|=18 and P is an
induced P5 contained in T. Every T contains at least one P, and each P is in
exactly binomial(d-5,13) such T. Therefore

    p(v) >= ceil(binom(d,18)/binom(d-5,13))
          = ceil(binom(d,5)/binom(18,5)).

| d | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Minimum p(v) | 1 | 2 | 2 | 3 | 4 | 4 | 5 |
| Minimum vertex deletions to remove every P5 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |

The red and blue degrees sum to 42. The two incidence lower bounds therefore
sum to at least 6 at each vertex, yielding at least 258 pairs consisting of a
root vertex and an induced P5 in one of its two monochromatic neighborhoods.
This counts rooted incidences; it is not a claim about 258 distinct unrooted
paths or vertex-disjoint configurations.

These are necessary structural conditions only. They produce no good43
graph and establish no new numerical lower bound for R(5,5). We make no
claim of historical priority for the restricted Ramsey lemma.
