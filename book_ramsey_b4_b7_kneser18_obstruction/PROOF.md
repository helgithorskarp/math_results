# Induced 18 Kneser-core obstruction

Author: **six-books-3**, role **researcher**, 2026-09-30.

**Theorem.** Let K have the 21 two-element subsets of {0,...,6} as vertices,
with a red edge precisely between disjoint subsets. For every S contained
in V(K) with |S|=3, the maximum order of a red/blue coloring that contains
an induced color-preserving copy of K-S and contains neither a red B4
nor a blue B7 is 21.

Books are ordinary, noninduced subgraphs: edges between pages have no
effect on this statement. Write tau(1)=3 and tau(0)=6, with red encoded 1
and blue 0. A coloring is valid exactly when each color-c spine has at most
tau(c) common neighbors joined to both endpoints in color c. Validity is
hereditary under vertex deletion.

**Core coverage.** Three distinct root edges of K7 form exactly one of a
triangle, a three-edge star, a three-edge path, a two-edge path together
with a disjoint edge, or a three-edge matching. This is the classification
of simple graphs with three edges after omitting isolated vertices:
the connected case is a triangle or one of the two three-edge trees;
otherwise a two-edge component or three one-edge components remain.
Any isomorphism between two such root graphs extends to a permutation of
all seven points. This permutation preserves disjointness, hence colors
in K. It carries their induced 18 cores to each other.

Order the 21 root edges lexicographically. The representative deleted
vertex sets are {0,1,6}, {0,1,2}, {0,6,11}, {0,1,15}, {0,11,18},
respectively. Their root-point stabilizers have orders 144,36,12,8,48;
their orbits therefore have sizes 35,140,420,630,105. Alternatively these
counts are binom(7,3), 7*binom(6,3), binom(7,4)*12,
7*binom(6,2)*binom(4,2), and binom(7,6)*15. They sum to 1330=binom(21,3).
The checker independently enumerates all 5040 root-point actions and
checks that their five disjoint deleted-set orbits exhaust all 1330 sets.
These are symmetries of the fixed seed used to cover cores. The theorem
assumes no automorphism of the coloring being extended.

**Complete one-vertex domains.** For a representative core C on labels
0,...,17, let D(C) consist of all masks p in {0,...,2^18-1} for which adding
one vertex, red to precisely the set P(p) of its 1-bits, leaves a valid
coloring. A saturated core spine uv of color c imposes the clause
not(x_u=c and x_v=c) on the new incident colors. The generator branches
on both values of every unforced variable and propagates these clauses
by implication reachability. Its tree has three leaf types: C for a
propagation conflict, I for a full assignment that fails the complete
spine test, and [V,p] for a full valid assignment. Every internal node
contains both children. Thus no unsaturated-spine or new-spine test is
replaced by the clause filter.

The checker reconstructs the clauses from explicit sets of pages. It
performs repeated clause scanning, checks the precise justification of
every conflict, checks both children at every split, and evaluates every
full assignment by a separate set-based graph test. It obtains the exact
sorted D(C), entry for entry. The five domains have sizes 1097,622,543,254,58.
The complete trees have 30437 nodes and 15221 full clause models in total.
An additional unpruned sweep of all 2^18 masks for each core agrees
entrywise with these domains.

**Exact pair compatibility.** Distinct or equal patterns p,q and a joining
color c define a unique coloring C+p+q. All unordered pairs of patterns,
including repetition, and both joining colors are tested. The generator
checks the new-new spine, all old-new spines, and all old-old spines by
exact bit operations. The independent checker uses the following
equivalent residual-capacity formulation, with sets rather than bit rows.

Let A_u and B_u be the red and blue neighbor sets of u in C. For p, define

    R(p)={u in P(p): |A_u intersect P(p)|=3},
    Q(p)={u outside P(p): |B_u intersect (V(C)-P(p))|=6}.

These are the old-new spines already saturated in C+p. A red joining edge
is allowed at all old-new spines exactly when P(q) misses R(p) and P(p)
misses R(q). A blue joining edge is allowed exactly when V(C)-P(q) misses
Q(p) and V(C)-P(p) misses Q(q). A spine unsaturated in C+p can gain at most
one page from q, so these are the entire old-new tests. The new-new spine
requires |P(p) intersect P(q)|<=3 for red and
|(V(C)-P(p)) intersect (V(C)-P(q))|<=6 for blue.

For old-old spines, each added vertex contributes at most one page. A
core-saturated spine receives no page from either individually valid
pattern. A spine at least two below its cap cannot overflow from two
vertices. The remaining spines have core codegree tau(c)-1. For each p,
record the set F(p) of such spines whose two incident colors from p
both equal the spine color. The entire old-old test is F(p) intersect
F(q)=empty. This proves equivalence of the checker's residual tests to
a complete graph test. The checked lists of colored pairs agree entrywise,
with 58941,9768,7760,3780,1038 entries. No compatible pair has equal patterns.
A separate full-graph control checks all 3422 pair-color tests for the
58-pattern matching core, including its repeats.

**The complete four-vertex frontier.** Let Gamma(C) have vertex set D(C),
with two patterns adjacent if at least one joining color is compatible.
It has no loops. In any valid host containing C, every outside vertex has
a pattern in D(C), and every pair of outside vertices gives a compatible
pair. Therefore their patterns are distinct and pairwise adjacent. If
the host has at least 22 vertices, choose any four outside vertices; their
patterns form a four-clique in Gamma(C). Sort these four patterns by their
indices in D(C), and retain their actual six joining colors. Every color
must belong to the appropriate compatible-pair list.

The generator enumerates all four-cliques and Cartesian products of their
allowed joining colors. The checker independently builds four-cliques by
recursive common-neighbor intersection and checks all 64 joining masks
at each four-clique. In the following table, colored pairs count
(i,j,c), whereas graph edges count the pair(i,j) once. The last column
counts color assignments surviving every pair test, not valid colorings.

| Deleted root type | Gamma edges | Four-cliques | Pair-compatible joining assignments |
|---|---:|---:|---:|
| Triangle |58941|952|952|
| Star |9744|142|142|
| Path |7654|46|92|
| Wedge and disjoint edge |3720|40|40|
| Matching |1011|432|432|

Pairwise validity need not imply validity of all four added vertices;
the remaining 1658 assignments are precisely the last finite domain
that needs to be excluded.

**The 62 short book certificates.** For each representative deletion S,
enumerate the subgroup of root-point permutations preserving S as a set.
Each such action preserves the core, permutes D(C), and carries a sorted
four-pattern tuple and its joining colors to another such tuple. The
outside vertices are reordered with their transformed patterns. Taking
orbits gives 16,10,18,7,11 representative assignments. These are orbits
under the specified root stabilizers; no assertion about the full
automorphism groups of the induced cores is needed.

For each orbit, [obstructions.json](obstructions.json) records four
indices into D(C), the six joining bits in the order
(0,1),(0,2),(0,3),(1,2),(1,3),(2,3), a spine, four or seven pages,
and the orbit size. The full 22-vertex coloring is decoded using core
labels 0..17 and added labels 18..21. The checker verifies directly that
all listed pages are distinct, exclude the spine, and meet both endpoints
in its color. Each representative therefore contains a red B4 or blue B7.

The checker verifies each core permutation as an exact colored-graph
automorphism and each domain action as a bijection. For every image of
every representative it reconstructs both 22-vertex graphs and verifies
the full colored-graph isomorphism, including all joining colors. It
checks that the obstruction orbits are disjoint and that their union is
exactly the entire 1658-assignment frontier. Hence all these assignments
are invalid. This excludes any host of order 22 or larger by the preceding
four-vertex reduction. The known valid K contains each C as an induced
subgraph and has order 21, proving attainment and the theorem.

**A consequence for comparisons with the seed.** In any hypothetical
valid 22-vertex coloring G, delete any one vertex and identify the other 21
vertices with V(K) by any bijection. The graph of pairs whose colors
differ from K has vertex-cover number at least four. Otherwise pad a
cover to three vertices; on the other 18 vertices the colors agree with
K-S. This is a forbidden induced core in G. The consequence holds for
every deletion and every labeling. It supplies a necessary escape
condition for a hypothetical witness.

**Reproducibility and trust.** The [README](README.md) gives the three
commands. [expected.json](expected.json) includes exact per-core counts,
orbit sizes and projection SHA256
`8cda3a6a61fb9d5ba534800ef25db4484d3051edfc63a5aa8e50f85a1de4b69d`.
This hashes the ordered name/deleted/domain/pair-color/obstruction
projection using compact JSON. The normalized red-edge seed SHA256 is
`8c7174eabad638fb4f0818657b884372c3b780030aae4f20fb6ce1896b753a53`.
All arithmetic is exact. The proof tree and complete pair lists are
regenerated privately, about 1.14 MB, rather than published as a corpus.

The negative controls reject incomplete status, a missing core, a false
conflict, an omitted pair, a false page, a wrong orbit size and an
uncovered orbit. These checks support the implementation; the written
reductions explain why its finite domain is complete. Python code,
interpretation of the certificates, and the unformalized mathematical
bridges are the trust boundary. The primary sources and prior scoped
work are attributed in the README. The known seed is not a new
construction, and this theorem does not close the unrestricted
22-versus 23 Ramsey gap.
