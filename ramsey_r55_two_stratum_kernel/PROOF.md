# Two additional strata close the fully visible five-set gap

All statements concern a simple graph, with edges red and nonedges blue.
Fix three distinct vertices E = {e0,e1,e2}. For each remaining vertex v,
write s(v) for its set of red neighbors in E. Assume throughout that

    0 < |s(v)| < 3.

The six signature classes may have arbitrary sizes, including zero.
This assumption is substantive: the theorem is not asserted when an
empty or full signature occurs. No automorphism, degree sequence,
local density equality, cell-edge quota or internal coloring of E is assumed.

Publication context: the height-2931 external five-cube-orbit classification
appeared during this bounded computation and subsumes the support lemma
below. We retain its separately derived proper-six-signature proof as
explicit independent special-case corroboration. The color-redundancy
specialization and complete degree-coupled completion interface are the
focus here. README records the source, overlap and review boundaries.

An edge is **free** if both endpoints are outside E and their signatures
are complementary. All other edges are **fixed** in a visible skeleton.
Equivalently, an edge outside E is fixed if its endpoints have the same
incidence color to at least one root. Thus it belongs to a common root
color neighborhood. Every incidence meeting E is fixed by definition.

Let S be the union of the three singleton-signature classes and P the
union of the three pair-signature classes. Every edge inside S or P is fixed.

## Theorem

A visible skeleton has no monochromatic five-set all ten of whose edges
are fixed if and only if all eight tests below pass:

1. For each of the three roots and each color c, the induced graph on
   its c-neighbors contains no c-colored K4 and no opposite-colored K5.
   These are six **full root-neighborhood** tests.
2. S contains no red K5.
3. P contains no blue K5.

In particular, if these tests pass, every monochromatic K5 in any
completion contains at least one free edge. The theorem makes no assertion
that a completion avoiding all such K5s exists.

### Proof of necessity

Every pair in a root color neighborhood is fixed: for two nonroots,
the root supplies an agreeing coordinate; pairs meeting E are fixed
by definition. A c-K4 there extends with the root to a fixed c-K5.
An opposite K5 there is itself a fixed obstruction. A K5 inside S or P
also has every edge fixed, since two singleton signatures, or two pair
signatures, cannot be complementary. Thus all eight tests are necessary.

### Signature classification

Use labels 1,2,4 for the singleton signatures and 6,5,3 respectively
for their complements. A support without a complementary pair contains
at most one member of each of the three pairs {1,6}, {2,5}, {4,3}.
Extend it, if necessary, to a choice of one from each pair. There are
exactly eight such choices. Six are the coordinate faces

    {1,3,5}, {2,4,6}, {2,3,6}, {1,4,5}, {4,5,6}, {1,2,3}.

Each face has a constant root-incidence coordinate. The remaining two
choices are {1,2,4} and {3,5,6}. Every proper subset of either of these
triples also has a constant coordinate: two distinct members agree at
one coordinate, and a singleton certainly does. Therefore a
complementary-pair-free support mixed in all three coordinates is
**exactly** one of these two triples.

### Proof of sufficiency

Consider a monochromatic K5 all of whose edges are fixed. If it meets E,
choose a root it contains. Its other four vertices violate that root's
same-color K4 test. Thus it is central.

Its signature support has no complementary pair. If a coordinate is
constant on its support, all five vertices belong to that root's color
neighborhood. The full neighborhood test rules out the K5: in the
neighborhood's own color it contains a forbidden K4; in the opposite
color it is a forbidden K5.

Otherwise the classification puts its support in S or P. There cannot
be a blue K5 in S: among five singleton signatures, one root occurs in
at most one of them (otherwise there would be at least six incidences).
That root is blue to at least four clique vertices, violating its blue
K4 neighborhood test. Dually there cannot be a red K5 in P: among the
three absent-root counts one is at most one, so some root is red to at
least four clique vertices. The only remaining possibilities are a
red K5 in S or a blue K5 in P, precisely the two additional tests. QED.

The opposite-color K5 part of the six tests cannot simply be omitted
from this proof. Nor does root validity by itself settle the two extra
strata. The two eight-vertex fixtures in fixtures.json each pass all six
full root-neighborhood tests but have exactly one central K5: respectively
a red clique with singleton multiplicities (3,1,1), or a blue clique
with pair multiplicities (3,1,1). Each passes the other extra test.
These show the two tests are individually necessary in the stated
arbitrary-size theorem, not that they are independent inside every
particular 43-vertex degree/signature profile. Eight vertices are the
smallest possible for three roots and a disjoint central five-set.

## Complete residual formula, not a width prefix

Give each free edge e a binary variable x_e, equal to one for red.
For every five-set F and color c, discard the potential c-K5 if any
fixed edge of F has the opposite color. Otherwise, with D(F) the free
edges in F, impose

    red:  OR over e in D(F) of NOT x_e;
    blue: OR over e in D(F) of x_e.

An empty clause is a fixed K5. This formula, including every five-set
and both colors, is equivalent to the Ramsey condition directly from
the definition, whether or not preflight passes. The theorem above says
that preflight passes exactly when no clause is empty. Passing preflight
does not mean the remaining nonempty formula is satisfiable.

The invisible graph on F is a disjoint union of complete bipartite
graphs, one for each complementary signature pair. If the occupied
sizes in those blocks are a_i,b_i, then

    |D(F)| = sum_i a_i b_i,   sum_i(a_i+b_i) <= 5.

If only one block contributes edges, its two positive sizes have sum
at most five, and its possible products are 1,2,3,4,6. If two blocks
contribute, their sizes use at least four vertices. With four vertices
the total is 1+1=2; with five it is at most 2+1=3. Three contributing
blocks need six vertices. Hence the only nonzero clause widths are
1,2,3,4,6; width five is impossible. All widths are attained by proper
signature multisets. There is no claim that widths one or two suffice.
Clauses can couple different complementary blocks.

## Individual degree interface

Each central vertex belongs to exactly one complementary pair of
signature classes. Once fixed edges are chosen, its remaining red
degree is the target degree minus its fixed red degree. Realizing the
individual degrees alone therefore factors into three independent
bipartite margin problems. Root degrees must already be correct.
If a vertex's margin is outside [0, opposite-class size], or a block's
two total margins differ, that block is impossible.

For completeness, kernel.py supplies an exact integral augmenting-path
algorithm: source-to-left capacities are left margins, left-to-right
capacities are one, and right-to-sink capacities are right margins.
Every augmenting path increases integral flow by one, so the procedure
terminates after at most the sum of the left margins augmentations.
When no augmenting path remains, the vertices reachable from the source
have no positive residual arc leaving them. Original outgoing arcs
across this cut are saturated and original incoming arcs carry zero;
flow conservation gives cut capacity equal to the current flow value.
Every feasible bipartite realization would carry the required total
across this cut. Thus either the chosen unit edges realize all margins,
or the smaller cut is an elementary infeasibility certificate.

The verifier checks chosen edges and cut capacities directly, without
running the producer's flow algorithm. No external max-flow or Ramsey
theorem is imported. Factoring degrees does **not** factor the Ramsey
formula: the clause constraints must hold simultaneously with the margins.

## Application scope

For the retained 43-vertex seed, the six cell sizes are (8,8,6,10,4,4)
for masks (1,2,3,4,5,6). Thus |S|=26, |P|=14, and the free blocks have
sizes 8x4, 8x4 and 6x10, totaling 124 variables. The reduction applies
to any choice of its visible skeleton, not just to the retained graph.
It also applies to other proper-six-signature cell sizes. It does not
cover all 470 aggregate cases without checking their signature hypotheses.

The retained seed itself fails preflight. Its 144 fixed K5s comprise
96 lying in at least one root color neighborhood and 48 outside every
one: 20 red singleton-stratum K5s and 28 blue pair-stratum K5s. The full
extra tests count 41 red singleton K5s and 39 blue pair K5s, including
overlap with the root-neighborhood failures. These are entry-level
classifications of known defects, not a new local-search lower bound.
No 43-vertex skeleton passing these eight tests is constructed here.
