# A deleted pentagon product cannot occur in a Ramsey graph on 43 vertices

Let **H = C5[C5] minus one vertex**, where brackets mean the lexicographic
product. Every 43-vertex graph containing H as an induced subgraph has a
clique or an independent set of order 5.

This excludes the **entire global extension family**: fix an induced copy
of H on 24 labeled vertices and leave all 627 other physical pairs free.
There are exactly 2^627 distinct graphs for that fixed embedding. The
statement also covers every relabeling and color reversal. No symmetry,
degree profile, chosen neighborhood, or external graph catalog is assumed
for the full 43-vertex graph. No union cardinality over embeddings is claimed.

The proof classifies every one-vertex attachment, then couples **all 19
outside vertices** through their forced incidences. It is not merely a
local attachment witness. H itself is a valid (5,5;24) graph and has 14,641
admissible one-vertex extensions, so one-vertex feasibility does not settle
the global family. No new Ramsey-number bound, maximum extension order,
sharpness, or historical priority is claimed.

## The physical core

Use pairs (i,j) with 0 <= i,j < 5, encoded by 5i+j, and delete (4,4). The remaining
labels are 0..23. Within each five-vertex bag, adjacency is the pentagon;
between different bags, all pairs use the color of their outer pentagon
pair. Thus bags 0,1,2,3 are full pentagons, and bag 4 is the path

    20 -- 21 -- 22 -- 23.

Its endpoints 20,23 are nonadjacent; its middle pair 21,22 is adjacent.
H has 138 red and 138 blue pairs. Each color has 105 four-cliques and no
five-clique: a monochromatic clique meets at most two bags and uses at most
two vertices in either bag.

The affine map (i,j) -> (2i+1,2j+1) modulo 5 fixes the deleted point and is an
isomorphism from H to its complement. Its 276 pair identities are checked.
This is a property of the **core** and imposes no automorphism on any
43-vertex extension.

## Complete attachment proof

For a new vertex x and each bag i, put:

- i in R if x's red neighbors in that bag contain a red edge;
- i in B if x's blue neighbors in that bag contain a blue edge.

If adjacent outer bags both lie in R, their two red pairs together with x
form a red K5. Hence R is independent in the outer pentagon, so |R|<=2.
If a blue outer pair has both bags in B, its two blue pairs and x form a
blue K5. Hence B is a clique in the red outer pentagon, so |B|<=2.

Every full pentagon bag belongs to R union B. Otherwise x's red neighbors
there would be independent and its blue neighbors a red clique. Each such
set has at most two vertices, and they cannot partition all five vertices.
The four full bags therefore exhaust the capacity |R|+|B|<=4. In an
admissible attachment they are disjointly assigned to R and B, and the
remaining path bag belongs to neither.

On P4, a partition into an independent red-neighbor set and a clique of
blue neighbors is unique: the red set is its two endpoints, and the blue
set its two middle vertices. Indeed both sets must have size two; of the
three possible blue edges only the middle edge leaves an independent pair.
Consequently **every admissible x is red to 20,23 and blue to 21,22**.

For the exact count, R={0,3} and B={1,2} is the only partition of the four
full bags compatible with the two outer constraints. On either R bag,
x's blue neighbors may be any clique of C5: the empty set, one of five
singletons, or one of five edges, giving 11 choices. On either B bag,
x's red neighbors may be any independent set of C5, also 11 choices.
The path pattern is fixed. All 11^4=14,641 choices are admissible because
a four-clique in H consists of two edges in a monochromatic outer pair.
These observations prove both directions of the classification.

## Global obstruction

Suppose a 43-vertex extension G had no monochromatic K5. Every outside
vertex has an admissible attachment, so all 19 outside vertices are red
to 20 and blue to 21. The graph on those19 vertices must therefore have
neither a red K4 nor a blue K4. This contradicts R(4,4)<=18.

For completeness, that classical bound has a short self-contained proof.
First R(3,3)<=6 by taking three neighbors of one color at a vertex and
examining their three pairs. Now suppose a triangle-free graph on nine
vertices has no independent four-set. Every degree is at most three. If
a vertex has degree at most two, six of its nonneighbors contain an
independent triple by R(3,3)<=6; adding the vertex gives an independent
four-set. Thus all nine degrees would be three, contradicting handshaking.
This proves R(3,4)<=9. In any coloring on 18 vertices, one vertex has at
least nine neighbors in one color. Their graph contains a triangle in that
color or a four-clique in the other color, yielding a monochromatic K4.

This universal argument proves the family exclusion. The finite checks
below validate its attachment kernel and physical interpretation; they
do not enumerate all 2^627 full graphs or all graphs on 19 vertices.

## Exact certificate and independent algorithm

`derive.py` classifies bag patterns by the two activity bits. A C5 has
status counts (0,11,11,10), and P4 has counts (1,7,7,1), in order
(neither,red-only,blue-only,both). It checks all 4^5=1024 status words,
including zero-weight words. Only (1,2,2,1,0) has positive admissible weight.
The resulting star list has 14,641 elements; 16,762,575 of the 2^24 stars
are rejected. `certificate.json` stores the compact factors and hashes,
not a large list of every star.

`check.py` imports no producer or extractor. It constructs the physical
core by explicit cycles and complete cross-bag pairs, enumerates all its
four-cliques, and builds the literal extension CNF:

    one negative four-literal clause per red core K4;
    one positive four-literal clause per blue core K4.

It has 24 variables and 210 clauses. A complete two-way DPLL recursion
with unit propagation enumerates every satisfying star, using 29,481
recursive nodes. This is a different enumeration from the activity
factorization. The **entire sets agree entry by entry**, and every model
has the four forced incidences. No native SAT solver is used or trusted.
The star-set SHA256, sorting integer masks and appending one newline each, is

    625ef99f2d50b15f2ed4c08d711229bc14ee0b25732651667d84b2542cb1b322.

The checker also literally checks all 42,504 five-subsets of H and its
self-complementary relabeling. It checks every compact factor, status word,
count and digest rather than accepting the expected aggregate alone.

## Full physical extractor

`extract.py` takes a JSON graph with fields `n: 43`, `red_edges`,
`core_embedding` (24 distinct labels in the stated core order), and
`core_color` (1 means the core's red edges are physical red; 0 means blue).
It validates every core pair. Finding an embedding is not implemented;
the caller supplies one. Wrong-family inputs are rejected, not assigned
a Ramsey verdict.

If an outside star contains a forbidden core K4, the extractor returns the
corresponding physical K5. Otherwise it checks the forced incidences for
all 19 outside vertices, finds a monochromatic four-set outside, and adds
the appropriate core endpoint or middle vertex. The output gives five
actual labels and their color. `verify.py` imports neither extractor nor
producer: it checks the input core with an explicit pentagon edge table
and verifies all ten physical witness pairs.

`fixtures.json` holds four expressly **non-Ramsey** 43-vertex inputs and
certificates, covering both extraction mechanisms and both orientations
with scrambled labels. They are reproducible fixtures, not construction
candidates or positive feasibility claims. The control suite checks 64
full 43-vertex inputs: 32 use arbitrary stars and 32 use admissible stars;
within each half both orientations and 16 fixed seeds are used. Global
outside edges remain independently specified by the deterministic generator.
This is a test protocol, not representative sampling or a full search.

Further controls compare DPLL's complete model sets to literal truth
tables on 512 bounded formulas, reject four kernel-certificate and four
physical-certificate mutations, and reject eight malformed graphs in both
extractor and verifier. Ordinary and `-O` outputs agree byte-for-byte.
These are author-written independent algorithmic checks, not peer review
or proof-assistant formalization.

## Reproduction

Python 3.11.2 standard library; no packages, external data, solver,
private input, build, or omitted large artifact. From this directory:

```sh
python3 -B reproduce.py
```

It checks `SHA256SUMS`, regenerates the compact certificate, runs the
independent kernel check and controls in both ordinary and optimized mode,
and compares every output byte with the committed expected files. Expected:
`VERIFIED_H24_WHOLE_GLOBAL_FAMILY_PACKAGE`. Runtime is a few seconds.
The 64 test graphs and four stored fixtures are regenerated deterministically.

For a supplied input/certificate pair:

```sh
python3 -B extract.py graph.json > witness.json
python3 -B verify.py graph.json witness.json
```

Witness extraction does not require certificate.json or the DPLL routine;
its guarantee is the displayed universal proof. Trust remains in that
unformalized proof, the code and parsing, exact Python semantics and
ordinary hardware. Hashes establish artifact identity, not mathematical
correctness.

## Literature, shared context and limits

Pentagon lexicographic products are classical Ramsey constructions; see
[Y. Wigderson's PCMI 2025 Homework 8, optional problem 3](https://ywigderson.math.ethz.ch/math/static/pcmi2025/Homework8.pdf)
for the product rule and clique/independence construction. The same source
is background for the choice of H, not a claim that it proves this exact
extension obstruction. [Angeltveit--McKay](https://arxiv.org/html/2409.15709v2)
provides primary context for exact Ramsey extension methods. Limited live
searches and a targeted Discovery Net title check found no matching claim;
this is not a historical-priority assertion. No novelty is claimed for
C5 products, the small Ramsey bounds, DPLL, or the general counting method.

The new complete M214 root 375 exclusion at height 3445 supplies related
campaign context and also displays the elementary R(3,4) argument. This
proof rederives that small bound; it imports none of that root's source,
formula or certificate. Its independent acceptance at height 3453 was read
before publication. The teammate's C3 phase obstruction at height 3429 is a
separate family. The M215 profile-C all-UNKNOWN checkpoint remains parked.
No cut/rank consequence, catalog-switching extension, fixed H92/H93
neighborhood, 104-edge lift, or six-neighborhood gluing is resumed here.

The result excludes graphs **containing H**. It does not force H into a
hypothetical Ramsey graph, reduce the inherited 66 degree profiles/271
anchored splits, decide any other complete M-slice, or produce a 43-vertex
Ramsey graph. No smaller core, edge perturbation, maximum extension order,
or next proof phase is part of this contribution.
