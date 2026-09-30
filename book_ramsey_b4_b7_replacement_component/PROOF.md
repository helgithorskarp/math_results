# Component, coverage and host-order proof

All graphs are simple and finite. Red-edge codegrees are at most three,
and blue-edge codegrees at most six; call such a graph valid. This is
equivalent to avoiding ordinary red B4 and blue B7. Validity is hereditary
under vertex deletion. Isomorphisms preserve the colors.

## 1. The reconfiguration graph

On the fixed set V={0,...,20}, let R2 have every valid red graph as a
vertex. Two different graphs G,G' are adjacent if every pair in their
symmetric difference meets some S contained in V with |S|<=2. This
allows arbitrarily many pair colors to change in one move. All
intermediate vertices of an R2 path are required to be valid.

Let H be the precise fixture in h21.json, and let A,B,D,E be the toggled
graphs in templates.json. The certificate checker verifies all five
graphs are valid. We prove that the R2 component of H is precisely
their relabelings, and has exactly 5 * 21! labeled graphs.

## 2. Complete adjacency domains

Fix any valid induced core C on r vertices. D(C) consists of all subsets
P of V(C) such that a new vertex whose red neighbors are precisely P
makes a valid graph C+z. Write x_u=1 for a red edge zu.

An old red edge uv with three red common neighbors imposes
not x_u or not x_v. An old blue edge uv with six blue common neighbors
imposes x_u or x_v. Every old spine is handled by these necessary
clauses: one added vertex contributes at most one page, so a
nonsaturated spine cannot violate its cap. All new spines zu must
additionally be checked at a complete assignment.

The generator closes assignments under implications of these binary
clauses, then splits an unassigned variable into its blue and red values.
Both children are retained. The tree grammar is

    'C'                          # forced contradiction
    'I'                          # complete pattern is invalid
    ['V', mask]                  # complete valid pattern
    [variable, blue_child, red_child]

Reachability forces only logical consequences. A forced contradiction
has no satisfying extension; every consistent incomplete assignment is
split both ways; every complete assignment is checked against all spines.
Thus the tree covers every pattern of D(C), with no root assumption or
graph symmetry pruning.

The checker independently derives clauses by enumerating page vertices
and propagates them by clause scanning. At each split it requires the
variable to be unassigned and checks both children. A conflict leaf must
actually conflict. Every complete leaf is checked by reconstructing its
graph from edge sets, and no incomplete assignment may terminate as a
valid or invalid complete leaf. Induction over this checked tree proves
complete coverage. Domain lists are sorted and compared entry by entry.

For each of H,A,B,D,E all 210 deleted pairs must occur exactly once in
lexicographic order. Bits of a pattern refer to the increasing order of
retained original labels. These explicit checks supply cohort coverage,
separately from coverage of each domain.

## 3. Complete pairs and exact membership

For each core C=K-S of order 19, test every unordered pair P,Q of its
complete domain, including P=Q, with both colors of the joining edge.
Exchanging the two added vertices is the only pair symmetry used: this
fixes C and preserves validity and the isomorphism class of the result.
The checker reconstructs every tested 21-vertex graph from sets and
compares the complete pair/color list with the certificate.

Every valid pair result includes a target in {H,A,B,D,E} and a list of
21 image vertices. The checker requires that list to be a permutation
of 0,...,20 and that it carries the entire completed red edge set to
the target's exact edge set. This positive bijection certifies class
membership. The generator finds these witnesses with discrete color
refinement, but its ordering is not trusted by the checker. A failure
to find a witness aborts generation; it cannot be treated as closure.

The complete checked transition counts are:

| Source | H | A | B | D | E |
| --- | ---: | ---: | ---: | ---: | ---: |
| H | 210 | 21 | 21 | 0 | 0 |
| A | 21 | 210 | 21 | 0 | 0 |
| B | 21 | 21 | 210 | 3 | 0 |
| D | 0 | 0 | 3 | 210 | 39 |
| E | 0 | 0 | 0 | 39 | 210 |

An entry counts colored completions across indexed cores, after
quotienting only the exchange of the two new vertices. It is not a
count of distinct labeled R2 neighbors. The absence of target classes
outside this table is established by complete pair testing and explicit
isomorphisms, not by the counts themselves.

## 4. Closure, connectivity and exact component

Consider an R2 move from a graph isomorphic to a template K. Transport
the labels so that its starting graph is exactly K. Enlarge the set
meeting all changed pairs to a two-element S if necessary. The ending
graph induces exactly K-S on the other 19 vertices. It is one of the
complete pair results just checked, hence is isomorphic to a template.
Thus the union of these five isomorphism classes is closed under R2
adjacency. Induction over arbitrary finite paths gives containment of
the H component in that union.

The opposite containment uses explicit valid moves:

    H -> A: changed pairs meet {16};
    H -> B: changed pairs meet {16};
    B -> D: changes (3,10),(3,19),(11,19), meeting {3,19};
    D -> E: changes (0,17), meeting {0}.

All five templates therefore lie in the component. Swapping any two
vertex labels of any valid graph changes only pairs meeting those two
vertices and produces another valid graph. Every permutation is a
sequence of such transpositions. Consequently every relabeling of
every template also lies in the component. This proves exact equality.

After quotienting R2 by color-preserving isomorphism and removing
self-adjacency, its component graph has exactly edges H-A,H-B,A-B,B-D,D-E.
The table's positive entries prove these adjacencies. A quotient edge
with any alternative label alignment would, after transporting its
starting labels, appear in the same exhaustive source-template cohort;
the zero entries therefore also exclude those alignments.

## 5. Distinct classes and labeling count

Initially color every vertex by its red degree, using shared codes
across the five templates. At each refinement round its new color is
the pair of its old color and the vector of counts of neighbors in
each old color. Equal signatures get equal codes across all templates.
Isomorphisms preserve these colors, by induction on the number of rounds.
Automorphisms preserve them by the same argument.

The checker computes three exact rounds, resulting in 105 different
colors across the 105 template vertices. In particular, each template
has 21 uniquely colored vertices and the five color multisets differ.
The templates are pairwise nonisomorphic, and every automorphism fixes
each vertex, so every automorphism group is trivial.

The action of the 21! label permutations on each template is therefore
free and gives 21! distinct labeled graphs. The five orbits are disjoint.
The exact component has 5 * 21! labeled graphs. No enumeration of that
large labeled component is assumed or required.

## 6. Maximum valid host order

For any core C define a compatibility graph Gamma on D(C): distinct
patterns are adjacent if either joining color makes their two-vertex
extension valid. Record a loop if equal patterns can work. The checker
verifies that every one of the 1,050 Gamma graphs has no loops and no
triangles. Repeated colored edges are treated as a single uncolored
adjacency here; both colors were checked independently.

Any valid host G containing an induced copy of C has each outside
pattern in D(C), by hereditary validity. Every two outside vertices give
a compatible pair. Without loops their patterns are distinct, and
therefore form a clique in Gamma. Triangle-freeness bounds the outside
set by two. For r=19 this proves |V(G)|<=21. Template K attains 21 for
each C=K-S, so the maximum is exactly 21.

This argument uses compatibility as a necessary condition. It never
assumes that pairwise compatibility suffices for a larger extension.
Core labels can be transported along any isomorphism, so the statement
covers every induced copy of every indexed core.

For any hypothetical valid 22-vertex witness, delete any vertex and
compare the remaining labeled graph with any relabeling of any template.
The graph of differing pairs has vertex-cover number at least three:
otherwise the unchanged 19 vertices induce one of the excluded cores.
In particular, no valid21 path of two-vertex replacements from H can
reach a graph that extends to 22, nor can arbitrary final rewiring on
two old vertices and an added vertex do so.

## 7. Reproducibility and trust

All source, the primary fixture, manifest and compact expected output
are self-contained. The temporary tree with isomorphism witnesses is
regenerated locally and is not a required external certificate corpus.
The checker does not import generator code, canonicalization routines
or solver verdicts. Exact integer masks and explicit set operations
are used. A literal sweep of all 2^19 patterns for E-{16,19} independently
reproduces the largest 34-pattern domain. Malformed coverage and
isomorphism certificates are rejected by the supplied controls.

The finite computation is checked by these programs. The bridges from
trees to coverage, permutations to isomorphism, one-step closure to
paths, invariant colors to rigidity, and compatible cliques to host
order are the written arguments above. They are not proof-assistant
formalized. These are author checks, not an independent peer-review
verdict. The theorem does not exclude other valid 21-vertex components
or settle the global 22-versus-23 Ramsey gap.
