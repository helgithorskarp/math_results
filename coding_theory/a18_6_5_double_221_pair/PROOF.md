# Complete finite reduction and sharp restricted maximum

Agent: **six-code-3**, role **researcher**, 2026-09-30.
This is a written proof with exact finite computation. The completeness
bridges below are unformalized; both implementations are by this researcher.

## Statement

F consists of distinct5-subsets of an18-element set; distinct members meet
in at most2 points. Set r_x=|{B:x in B}|, lambda_xy=|{B:x,y in B}|, and
t_xy=5-lambda_xy. Assume r_x=r_y=20, lambda_xy=3, and the multisets of positive
deficits in both rows x and y are(2,2,1). Then |F|<=58, and equality is attained.
The two rows' remaining deficit neighbors can overlap arbitrarily. No
replication assumption at any other point is used.

Pair multiplicity is at most5: the3-point tails of words through a fixed pair
are disjoint subsets of the16 remaining points. At r_x=20 the deficit row
has sum85-4r_x=5. These facts require no imported point-bound theorem.

## First-star leave and high-block incidence

Shorten the20 words through x by deleting x. Their4-subsets on17 points
meet pairwise in at most1 point, and their covered pairs are distinct.
Call the shortened replications s_z=lambda_xz. The pair leave H has16 edges,
and degree16-3s_z=1+3t_xz at z.

Label the marked pair neighbor y=0, the other deficit-two neighbor a=1,
the deficit-one neighbor b=2, and the fourteen remaining points3,...,16.
Then s=(3,3,4,5^14), and H has degrees(7,7,4,1^14).
Let q count high-high edges, u count high-low edges and m low-low edges.
The two degree sums give18=2q+u and14=u+2m, hence q-m=2. Since q<=3,
the complete possibilities are q=2,m=0 or q=3,m=1.

In the first case the high core is a path; all low points attach to one
high point. In the second the core is a triangle; two low points form an
isolated pair and all other low points attach to a high point. With0 marked,
the four normal forms are:

| Shape | High core | Low cohorts attached to0/1/2 | Isolated low pair |
|---|---|---|---|
|0|01,02|3..7 / 8..13 / 14..16|none|
|1|01,12|3..8 / 9..13 / 14..16|none|
|2|02,12|3..8 / 9..14 / 15..16|none|
|3|01,02,12|3..7 / 8..12 / 13..14|15,16|

Within each cohort arbitrary relabeling is allowed. This elementary leave
catalogue is necessary baseline information; it does not assert existence.

For a path, exactly one high-high pair is covered. It belongs to exactly
one shortened block, and no block contains all three high points. Its two
low points must belong to the leave cohort of the path center. Every other
low point appears in precisely two blocks meeting high points, one for
each of its covered high-low pairs. The two high incidences can share a
block only in the unique high-pair block already accounted for.

Represent the other high blocks as vertices grouped by their high point;
each remaining low point is an edge joining its two blocks. The graph is
simple, since two different high blocks cannot share two low points. Every
vertex has degree3. Conversely each such incidence graph recovers all high
blocks, with the common block's two points kept separately. Relabeling high
blocks within their groups induces a literal low-point relabeling by edge
incidence. Thus quotienting these graphs loses no first stars and imposes
no packing automorphism.

For shape0 the three vertex groups have sizes3,2,3; the cross-edge counts
are3 between0/1,6 between0/2,3 between1/2. All408 simple cubic graphs on
these specified groups are generated. The72 permutations within the groups
give8 disjoint actual orbits. Shape1 is obtained by exchanging the two
replication-three high labels and relabeling their cohorts, retaining both
possible markings. For shape2 the groups have sizes2,2,4. Every edge joins
the first two groups to the last, so the graph is a simple cubic bipartite
graph on4+4 vertices. It is K4,4 minus a perfect matching. All24 labeled
such graphs constitute one orbit under the96 within-group row permutations.
This gives the unique high-block model used in the source.

For shape3 no high pair is covered, so there are3+3+4=10 high blocks.
Each isolated low point occurs with each high point once. They occur in
different blocks at each high point because their own pair is uncovered.
Normalize the blocks containing15 to Y0,A0,B0 and those containing16 to
Y1,A1,B1. The remaining blocks are Y2,A2,B2,B3. Every other low point again
joins its two high blocks. Those12 edges form a simple tripartite graph
with degrees(2,2,3;2,2,3;2,2,3,3). Edges within either carrier triple
Y0,A0,B0 or Y1,A1,B1 are forbidden because those blocks already share an
isolated low point. All2408 degree graphs are generated. Simultaneous
exchange of the two carrier triples and exchange of B2,B3 give an actual
group of order4. Its612 disjoint graph orbits cover all2408 graphs.

The generator uses prescribed cross-edge subsets; the checker independently
uses a vertex-neighborhood degree DFS. It regenerates every graph and
closes the row groups from elementary generators, matching each case.
The cube uniqueness is independently checked through all24 labeled graphs.

## Completing the first star

Every pair incident with a high point is now either uncovered in H or
covered by the fixed high blocks. Any remaining shortened block therefore
uses only the fourteen low points. Generate every4-subset of those points
whose six pairs avoid H and all fixed covered pairs. Require an exact cover
of the remaining pairs. Every actual first star induces such a cover;
conversely each cover gives20 blocks with precisely the desired leave and
replications. This equivalence does not assume affine geometry.

Production uses integer row bitsets and MRV pair choice. The separate
checker uses literal pair sets and always chooses the least remaining
pair. Both enumerate each cover completely and compare every resulting word.

| Shape | High-block cases | Complete stars in these cases |
|---|---:|---:|
|0|8|2, both in one case|
|1|8|2, both in one case|
|2|1|2|
|3|612|0|

Production uses2491 nodes, maximum34 in one case. The separate fixed-pair
enumeration uses36267 nodes, maximum2392. Each positive case's two solutions
are exchanged by the literal transposition of its common high-pair block's
two low points:3/4,9/10 or15/16. Consequently one template per marked shape
0/1/2 covers every first star. The high-core triangle cannot occur.
Without the marking, shapes0 and1 coincide under high-label exchange,
while shape2 has a different degree at its leave-path center. Hence there
are exactly two unmarked types and three types with a replication-three
point marked. The three explicit templates are in expected.json.

## Coupling the second star

Restore x=17 and mark y=0. The three words through xy have disjoint3-point
tails, covering9 of the16 other points. Since y has the same deficit row,
its shortened star is also one of the three classified marked templates,
where the marked shortened point is now x.

For each of the nine ordered template pairs map the second template's
marked point0 to17. Its three marked-point tails must map to the first
star's three common xy tails. There are3!*(3!)^3=1296 choices. The other
seven template points can map bijectively to the seven remaining old points
in7!=5040 ways. These choices cover every possible second star, including
all overlaps of the other deficit neighbors. Different maps can produce
the same actual star; actual20-word sets are deduplicated.

Production prunes a partial map only when a partially restored noncommon
word already meets a first-star word in at least3 points. Adding points
cannot repair that intersection. The checker uses a complete permutation
scan with no partial-word or recursive pruning. It scans exactly6531840
full maps in every template pair,58786560 in total. Accepted map counts
are0,0,192,0,108,72,192,72,80. Every actual second-star word set agrees.

The actual second-star counts, with first/second shapes as row/column, are:

| |0|1|2|
|---|---:|---:|---:|
|0|0|0|48|
|1|0|18|18|
|2|32|12|20|

There are148 normalized joint stars. Every union has37 words. The listed
first-star permutation groups of orders6,6,4 fix x,y and the remaining
two high labels and preserve all20 first-star words. Closure and literal
word transport are checked; no assumption that the entire code has an
automorphism is made. Their explicit image orbits partition all148 second
stars into31 cases. The checker verifies every permutation and each orbit's
full membership, so completeness of a claimed full automorphism group is
not needed for this additional quotient.

## Residual maximum and attainment

Both complete stars already contain every word through x or y. Thus any
further word is a5-subset of the16 other points. Test all4368 such subsets
against every word of the37-word union. The resulting candidate counts
are74..116. Two candidates are adjacent exactly when they meet in at most2
points. Every completion is a clique in this graph, and every clique gives
a completion. Relabeling within a checked joint-star orbit preserves this
graph and its packing maximum.

Production computes maximum cliques with exact integer proper-color bounds.
The color classes are independent sets in the compatibility graph. Every
clique uses at most one vertex per class. Reverse-color-order branching
includes a vertex and then deletes it; every clique has a unique greatest
chosen vertex, so the recursion covers every clique. Color-count pruning
only discards branches that cannot improve an already checked witness.
On the31 cases the maxima are16/17/18/19/20/21 in4/3/9/5/7/3 cases.
The computation uses223205 nodes in total, maximum36425 in one case.

The separate checker regenerates every candidate by literal intersections
and reconstructs conflicts through shared triples. It verifies every
conflict edge against literal intersection. Its binary inclusion/exclusion
search asks whether an independent set of22 exists in the conflict graph.
It bounds each state by a greedy partition into actual conflict cliques;
at most one member of an independent set lies in each class. The include
branch deletes the chosen vertex and all its conflicts; the exclude branch
deletes only that vertex. These branches partition all possible independent
sets. All31 cases return false, in8253 nodes total, maximum1185 in one case.
This independently establishes the common residual upper21, without claiming
an independent computation of every smaller individual maximum.

Therefore |F|<=37+21=58. The supplied58-word fixture is checked directly for
distinctness, weights and every pair intersection. Its centers17 and0 have
replication20, pair multiplicity3, and respectively deficits
{0:2,1:2,2:1} and {17:2,15:2,2:1}. Thus it satisfies every hypothesis and
attains58. In particular overlap of the other deficit neighbors is allowed.

## Global consequence and trust boundaries

The restricted theorem implies that in a code of size at least59 two
saturated(2,2,1) rows cannot join at a deficit-two edge. For a72-word code,
Brouwer's primary A(17,6,4)=20 theorem forces all18 point replications20.
Code-1's support-minimum-three theorem restricts every positive row to
(3,1,1),(2,2,1),(2,1,1,1) or(1,1,1,1,1). A deficit-two neighbor of a
(2,2,1) row can have only(2,2,1) or(2,1,1,1); the present theorem excludes
the former. Both such neighbors must therefore have(2,1,1,1).
These imported results are used only for this global consequence.

All mathematical operations are exact sets or integers. Floating-point
elapsed time only implements operational guards. No solver, timeout,
UNKNOWN status or resource failure is interpreted as an exclusion.
The fixed native matrix dimensions cover1334 rows and120 compressed pair
columns on17 points; their array and mask bounds are explicit. The change
from preceding sixteen-point inputs does not raise search or resource guards.
Each mathematical cover/transport fiber and each Python search retains the
200000-node/ten-second guard. No published case reaches it.

The small expected manifest records reproducible counts/digests/templates;
it is not a standalone nonexistence certificate. Generated full domains,
matrices, binary outputs and logs stay in private work storage. Correctness
uses the written degree, incidence, quotient, transport, recursion and
completion bridges as well as the supplied executables. These bridges are
not formalized, and the separate checks are same-author checks. No
independent peer review of this result is claimed. The global interval
69<=A(18,6,5)<=72 remains unchanged.
