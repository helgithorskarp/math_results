# Complete physical cover and the first four-frame obligation

A good43 is a coloring of all 903 pairs of 43 vertices with no monochromatic
K5. For a pair uv, its own-color codegree is the number of vertices w for which
uv, uw, vw all have the same color. Let M be the maximum of these 903 numbers.

## Cover theorem

Every good43 has a representation in one of the 431 cases in `residual.json`.
The cases have M=10,11,12,13 and respectively 313,105,12,1 possible induced
common-neighborhood graphs. Catalogue completeness is an external premise.

Let d(v) be the red degree and T the total number of monochromatic triangles.
Counting mixed triangles at their two vertices incident with different colors
gives

    T = C(43,3) - (1/2) sum_v d(v)(42-d(v)).

Each summand is at most 441. Their sum is even, and 43*441=18963 is odd, so
T >= 12341-9481=2860. The sum of the own-color codegrees is 3T >= 8580.
It therefore cannot be bounded above by 903*9=8127: M>=10.

For an edge uv, its common neighborhood in the edge's color contains no
triangle of that color, since that triangle together with u,v would be a K5.
It contains no opposite-color K5 either. Thus it is a Ramsey(3,5) graph.
R(3,5)=14 implies M<=13.

Choose an edge attaining M. Complement colors if necessary and label it 0,1
in red. Put its M common red neighbors at vertices 2,...,M+1. The induced red
graph on these vertices is isomorphic to a member of the complete published
Ramsey(3,5;M) catalogue. Relabel the common neighborhood by that isomorphism.
Every other vertex has one of the three root states RB, BR, BB; RR would
increase the chosen edge's codegree. All its common-core edges and all edges
between exterior vertices remain physical decisions. Impose all physical K5
conditions and the bound M on every physical own-color codegree.

Conversely, every assignment satisfying such a case is literally a good43
and has maximum codegree M, since the chosen edge attains M. This is a
surjective cover by normalized representations. One graph can have several
representations. No claim of a disjoint partition into isomorphism classes or
of fixing a graph automorphism is made.

For k=41-M exterior vertices, the raw marked domain per catalogue case is

    3^k * 2^(M*k + C(k,2)).

This counts assignments before imposing the remaining good43 predicates. It
does not count surviving candidates or distinct unlabeled graphs.

## Exact first subset and its four-way join

The first declared subset consists of all M=13 good43 graphs admitting an
exterior vertex z with exactly five red neighbors in the common core H.
The unique Ramsey(3,5;13) graph is the cyclic graph on Z/13 with differences
1,5,8,12. If the red footprint S of z misses an independent four-set in H,
that four-set with z is a blue K5. An exhaustive 8192-subset check shows that
every transversal has at least five elements. The 65 size-five transversals
are covered by the following two disjoint orbits of the explicitly checked
automorphisms x -> mx+b, m in {1,5,8,12}:

* {0,1,2,5,6}: orbit size 52;
* {0,1,2,6,9}: orbit size 13.

After exchanging roots, z has root state A=RB or T=BB. These two choices and
the two transversal orbits give exactly the four stated frames. A graph
with several choices of z can occur in several frames; their union is exact.
Each frame leaves 27 further vertices, 783 free physical edge bits, and raw
root-state domain 3^27*2^729. All four frames must be closed to retire this
declared subset. It would still leave the other M=13 cases and all lower-M
branches unresolved.

In the combined input, z is vertex 15. All frame pairs are fixed except
0--15, 7--15 and 11--15. The first is a free Boolean A/T choice. The latter
two are opposite Booleans, selecting the two footprints. Every other pair
touching a vertex >=16 is free. This leaves 785 independent variables.
`physical.py` emits the red and blue K5 clauses for every five-set, simplified
only by this literal substitution. It adds no carrier, degree, codegree,
automorphism or imported-theorem clauses.

The resulting formula is satisfiable exactly when at least one of these
four frames has a physical good43 extension. In any such extension the
chosen edge already has codegree 13; the general upper bound just proved
ensures it has no further common red neighbor. The standalone physical
formula therefore also covers the required root-state condition without
adding it as a clause.

The unsimplified Boolean domain of the joined CNF has 2^785 assignments.
The smaller three-state raw counts above belong to the normalized semantic
cover, which already incorporates the derived RR prohibition. No CNF model
is lost by passing to that three-state domain.

`audit_physical.py` projects the actual DIMACS input under all four choice
assignments. It separately enumerates all K5 constraints in each fully fixed
frame, assigning every exterior edge its direct physical index. Matching
ordered clause counts and SHA-256 digests checks the complete four-way input
interface. This input audit is not a nonexistence certificate. An UNSAT claim
would additionally require a checked complete proof against that exact input;
a SAT claim requires decoding and directly checking all 903 physical pairs.

## What the incidence controls establish

For a fixed 16-vertex frame, let x_S be the nonnegative multiplicity of an
exterior red star S. It must avoid creating a K5 with four fixed vertices,
must not be red to both roots, and must obey the fixed part of every new
edge's codegree bound. For disjoint fixed red clique R and blue clique B,
with r=|R| and b=|B| not both zero, the vertices red to all of R and blue to
all of B form a Ramsey(5-r,5-b) graph. Hence

    sum_{S: R subset S, S disjoint B} x_S
       <= R(5-r,5-b)-1 - fixed_matching_vertices.

All Ramsey bounds used here are explicitly listed in `check.py`. In
particular the pair rows give codegree <=13, and the singleton rows give
both color degrees <=24. These are necessary conditions only: the x_S need
not be integral, and no mutual edges between exterior vertices are supplied.

The four published rational controls satisfy EVERY such row, without row
deduplication, and have total mass strictly between 27 and 29. Scaling them
down to mass 27 preserves every inequality because every right side is
nonnegative. They therefore prove that this entire necessary system cannot
exclude any of the four frames. Their validity is checked using integers;
the discovery solver's floating optimality claim is not used.

The four physical order-42 controls reproduce graphs from McKay's published
collection. Direct checks verify every K5 condition, maximum codegree 13,
and the indicated frame embedding. All four frames have 26-vertex physical
extensions. These are lower-order controls, not new constructions or good43s.

## Terminal accounting

No incidence certificate, catalogue filter, physical42 control, input audit,
unfinished proof, or solver UNKNOWN retires any good43 case. The complete
431-case ledger remains unresolved unless a separate checked terminal proof
is explicitly attached. The input specification hashes in that ledger pin
semantic case data; they are not hashes of completed CNFs or certificates.
