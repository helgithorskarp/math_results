# Three-list extension for long terminals and Parts connector assemblies

**Theorem.** Let a finite four-colourable unit-distance connector H be
vertex-disjoint from full copies of the specified Parts A159 and B214
gadgets. Suppose shared gadget vertices are designated terminals, all new
unit edges are confined to H and the terminals, and each terminal has at
most one unit neighbour in H. If the assembled graph has at most **508
vertices**, **every proper four-colouring of H extends to the assembly**.

This covers arbitrary real translations, rotations and reflections, including
coincident terminals of different gadgets. It closes the proposed
three-single-contact Moser placement class without enumerating placements.
In particular the raw `7+3*159=484` construction is four-colourable under
these hypotheses. The connector need not be the Moser spindle.

A stronger colour-dependent form holds: for a given proper four-colouring
f of H, replace the one-neighbour condition by the requirement that **the
colours seen among the H-neighbours of each terminal form a set of size at
most one**. That f extends even when some terminals have several neighbours
in H. The one-neighbour geometric condition guarantees this for every f.

This is a negative construction theorem, not a five-chromatic graph or a
record improvement. Contacts with gadget interiors, shared connector/gadget
vertices, reduced gadgets, or connector neighbourhoods using two colours
are outside the corresponding sufficient conditions. The theorem does not
combine all mixtures of this family and the earlier double-contact family.

## Abstract terminal lemma

Let T1,...,Tk, with k at most three, be equilateral triangles in the plane
with a common side length L>2. They may intersect. Give every point of
T=union Ti a list of at least three colours from one fixed four-element
palette. Then the complete unit graph on T has a proper list colouring in
which every Ti is non-monochromatic.

Choose any pair of points from each Ti and add that pair as an auxiliary
inequality edge. Repeated edges are identified. The selected edges have
length L, so they are distinct from unit edges and have no loops. Let F be
the graph of all terminal unit edges together with these at most k selected
pairs. It suffices to list-colour F.

At a point x belonging to r of the terminal sets, there is no unit neighbour
inside a containing set. Each of the other k-r sets contains at most one
unit neighbour of x: two would be at distance at most two, contrary to L>2.
Thus x has at most k-r actual unit neighbours. At most r selected pairs are
incident with x, one from each containing set. Therefore

```text
degree_F(x) <= (k-r)+r = k <= 3.
```

The count remains valid for shared terminals and repeated chosen pairs.
For k at most two the same argument works for any finite terminal sets of
size at least two with all within-set distances greater than two; equal
side lengths and three-point sets are not needed in that case.

### Noncubic components

Restrict each list arbitrarily to exactly three palette colours. A connected
component of F having a vertex of degree at most two is list-colourable as
follows. Root a spanning tree at such a vertex and colour vertices in reverse
tree order, with the root last. Every nonroot vertex still has its parent
uncoloured, so at most two neighbours are already coloured. The root also
has at most two neighbours. At least one of its three allowed colours is
therefore available at every step.

Only a component in which every vertex has degree three needs attention.
In that case k=3. Every vertex of the component is incident with a selected
pair: its actual unit degree is at most 3-r, with r at least one, and hence
is at most two. Since there are only three selected pairs altogether, a
cubic component has **at most six vertices**.

### Geometry excludes K4

Any K4 component would have four distinct planar points, every pair at
distance either 1 or L, with at most three pairs of length L. Unit adjacency
inside those four points is transitive: two unit steps cannot end at
distance L>2, so their ends must also be at unit distance. Thus its unit
graph is a disjoint union of cliques. It has at least three unit edges.

The only partitions of four points into cliques with at least three edges
are a single four-clique, or a three-clique and one isolated point.
Four pairwise unit-distant points cannot lie in the plane. In the second
case the three unit-adjacent points form an equilateral unit triangle and
the fourth point would be at distance L from all three. The only planar
point equidistant from its vertices is its circumcentre, whose distance is
1/sqrt3, inconsistent with L>2. Hence K4 is impossible.

For the application L=sqrt7, a separate exact finite check excludes all
42 choices of at most three long pairs among the six pairs of four points.
For squared distances d(i,j) in {1,7}, form the 3-by-3 Gram matrix

```text
G(i,j) = (d(0,i)+d(0,j)-d(i,j))/2,  i,j in {1,2,3}.
```

Four planar points require det(G)=0. The 42 determinants are all nonzero:
`1/2, -7, -11/2, -245/2, 5, -49, -58`, with multiplicities
`1,6,12,3,4,4,12` respectively. This supplies a check independent of the
transitivity/circumcentre proof. It is not needed to extend the analytic
lemma to arbitrary common L>2.

### The two remaining cubic components

A simple cubic graph has an even number of vertices and at least four.
The only one on four vertices is K4. On six vertices its complement is a
simple 2-regular graph, hence either a six-cycle or two disjoint triangles.
Their complements are respectively the triangular prism and K3,3. They
are connected. Thus these are the only remaining cubic components.
Both can be coloured from every three-subset list of the four-colour palette:

- **K3,3.** The lists on one part have a common colour: their three omitted
  colours exclude at most three of the four palette colours. Use a common
  colour on that entire part. Each vertex of the other independent part
  still has at least two allowed colours different from it.
- **Triangular prism.** Label its triangles a1,a2,a3 and b1,b2,b3 with
  matching edges ai-bi. Greedily give the a vertices distinct permitted
  colours c1,c2,c3. Let Si be the list of bi after removing ci. Each Si has
  size at least two. Their union has size at least three: otherwise all Si
  would equal a common two-element set S, forcing the three distinct ci
  into the two-element complement of S in the palette, a contradiction.
  Three sets, each of size at least two and with union of size at least
  three, have distinct representatives. To see this directly, choose
  distinct x in S1 and y in S2. If S3 has an element outside {x,y}, use it.
  Otherwise S3={x,y}; one of S1,S2 has an element outside {x,y}, and moving
  that representative there frees x or y for S3. These representatives
  properly colour the b triangle and avoid its matching neighbours.

The component colourings combine into a proper list colouring of F. Every
selected pair is unequal, so every terminal triangle is non-monochromatic.
This proves the abstract lemma without a list-colouring theorem, solver,
placement census or unproved classification premise.

## Full gadget and connector extension

Use the archived
[A159](../hadwiger_nelson_nonmono159_214_lowden2/points159.tsv) and
[B214](../hadwiger_nelson_nonmono159_214_lowden2/points214.tsv) graphs, with
terminal indices `[141,142,144]` and `[186,187]` respectively. A's terminals
form an equilateral sqrt7 triangle; B's two terminals have distance three.
The [positive extension certificate](../hadwiger_nelson_long_terminal_gluing/README.md)
proves that all 60 non-monochromatic four-colour assignments on A's terminals
and all 12 unequal assignments on B's terminals extend through the full
gadgets. This result uses only that positive direction, with no assertion
that the missing monochromatic assignments are impossible.

Precisely, let C be the connector vertex set, Vi the full gadget copies,
Ti their designated terminals, Ei their internal strict unit edges and EC
the strict unit edges of the connector. Let G be the complete unit graph
on `C union (union Vi)`. Require:

1. `C intersection Vi` is empty for every i, and
   `Vi intersection Vj` is contained in `Ti intersection Tj` for i distinct
   from j.
2. Every edge of G outside `EC union (union Ei)` has both endpoints in
   `C union (union Ti)`.
3. For a given proper connector colouring f with palette {0,1,2,3}, each
   terminal sees at most one distinct colour among its neighbours in C.

At a terminal x give the available list
`{0,1,2,3} minus {f(y): y in C, distance(x,y)=1}`. Its size is at least three.
For at most three A copies, apply the abstract lemma. For at most two
copies of either type, the degree bound is at most two and the rooted
greedy argument applies directly. In both cases the terminal assignments
extend through each copy using the imported positive certificates. The
extensions agree on shared terminals and with f on the connector. All
inherited edges are proper locally, and every remaining edge is handled
by the terminal colouring or its available lists. Thus f extends to G.

To apply this to every assembly on at most 508 vertices, observe that each
A copy has 156 private interior vertices, while B has 212. Four copies
already contribute at least 624 distinct private vertices. Three copies
including B contribute at least `156+156+212=524`. Consequently the only
three-copy case within the budget is A+A+A, and the preceding cases cover
all possible gadget counts and types. Every subgraph of a covered assembly
is also four-colourable by restriction.

If each terminal has at most one connector neighbour, condition 3 holds
for every proper f, giving the theorem stated at the beginning. In the
colour-dependent form it suffices to find one proper f with monochromatic
connector neighbourhoods at all terminals.

## Reproducible checks

The analytic proof covers arbitrary placements. Computation supplies compact
positive witnesses and independent finite checks of its exceptional steps.
It is not used as a sample-based substitute for the universal argument.

The [constructive algorithm](colour.py) implements rooted greedy colouring
and the two exceptional constructions. The [producer](build.py) generates
[374 compact witnesses](certificate.json), one for each of the 187 canonical
forbidden-colour words of length six for each graph. Canonical words encode
first occurrences of palette colours; arbitrary words are covered by palette
renaming. The certificate has **6,752 bytes**.

The [separate checker](verify.py) imports no producer or colouring code. It
independently visits all **8,192 labelled list profiles**, covering both
graphs, and checks each restored witness on all vertices and edges. It also
enumerates all **32,832** simple graph masks on four and six labelled vertices,
obtaining one K4, ten K3,3 graphs and sixty prisms among the cubic graphs.
It checks all 42 rational Gram determinants and rejects a corrupted colouring
and a missing profile. The universal graph classification and list-colouring
claims also have the elementary proofs above.

[Exact fixtures](fixtures.py) exercise an actual auxiliary prism and three
coincident terminal sets. The prism fixture uses the nine points

```text
{0, 1, (1+i*sqrt3)/2} + {0, sqrt7, (sqrt7+i*sqrt21)/2}.
```

The terminal sets are its three translates of the long triangle. Its unit
graph is three disjoint unit triangles, and choosing the same long side
in every terminal set produces a cubic prism component. This shows that
simply assuming the auxiliary graph is 2-degenerate would miss a real case.
Integer arithmetic in the basis `1,sqrt3,sqrt7,sqrt21`, with coordinates
divided by two, verifies all fixture distances. Across the two fixtures,
all 54 selected-pair choices and 216 list-colouring runs pass, including
shared terminal sets. Four additional noncubic graph fixtures exhaust 1,552
list profiles. Four invalid list or graph-premise controls are rejected.

From the repository root, with Python 3.11.2 and the standard library:

```bash
python3 -B hadwiger_nelson_single_contact_extension/build.py --out /tmp/hn-single-contact
python3 -B hadwiger_nelson_single_contact_extension/verify.py --work /tmp/hn-single-contact
python3 -B hadwiger_nelson_single_contact_extension/fixtures.py --out /tmp/hn-single-contact/fixtures.json
python3 -B hadwiger_nelson_long_terminal_gluing/build.py --out /tmp/hn-positive-extension
python3 -B hadwiger_nelson_long_terminal_gluing/verify.py --work /tmp/hn-positive-extension
```

The two build output directories must be new. The final two commands replay
the imported positive gadget certificates; keep assertions enabled for
those older scripts. The new scripts use explicit exceptions and work under
normal and optimized Python. Build replay reproduces the witness bytes.
[Expected checks](expected.json), [validation and input hashes](validation.json),
and [source hashes](SHA256SUMS) are included. Generated operational files
remain outside Git. No third-party packages or native solver are needed.

Witness generation takes about 0.03 seconds, the independent finite audit
0.21 seconds and fixtures 0.04 seconds, on one thread. Peak memory was not
measured. The imported replay checks 35,352 exact pair norms and 50,484
expanded colour inequalities for all 72 terminal assignments. No new
full-gadget placement or geometric root search was performed.

Trust remains in the ordinary geometric, counting and gluing arguments,
faithful archived coordinates and positive witness bytes, exact integer and
rational arithmetic, complete loops and certificate decoding. The author-run
separate checker is not an external review or proof-assistant formalization.
External review of this new theorem is pending.

## Construction decision and shared context

The proposed census with one spindle contact per terminal is unnecessary:
the new theorem handles every such placement and every connector colouring,
subject to the assembly conditions. Changing the connector alone cannot
escape this obstruction while preserving those conditions.

The previous [double/single-contact Moser closure](../hadwiger_nelson_moser_terminal_connector/README.md)
has now been [independently accepted](../hadwiger_nelson_moser_terminal_connector_review1/README.md).
It supplies one common colouring for its particular finite placement class
and arbitrarily many private gadget copies. The present theorem supplies
an extension for each permitted assembly and each permitted connector
colouring; it does **not** assert one colouring common to all placements.
Neither theorem by itself closes every mixture of the two contact types.

A next construction must violate a remaining sufficient condition. Within
the other stated size, disjointness and private-interior hypotheses, a
non-four-colourable assembly with a four-colourable connector must have
the following property: for every proper connector colouring, at least one
terminal sees two or more connector colours. The terminal may depend on
the colouring.
One concrete unstarted direction is a mixed assembly containing a placement
from the earlier double-contact class and a triangle outside that class,
with their actual terminal unit edges retained. Before selecting a new
census, test whether colour-dependent neighbourhood constraints or another
small structural argument already close it. Interior contacts are another
possible escape requiring a separate full-graph construction. This pass
starts neither next phase.

HN-2's [H514 boundary saturation theorem](../hadwiger_nelson_heule514_boundary_decision/README.md)
closes its local universal-extension shortcut: all 37 path clauses remain
necessary on that boundary. It does not close the 258,914 residual graphs.
That exact-certification lane and the retired heptagon and H574 families
are not duplicated here.

Primary-source calibration on 2026-09-06: Parts'
[paper](https://arxiv.org/html/2010.12665v2) supplies the 159/214 gadget context
and the 509-vertex record; [Haugland's current manuscript](https://arxiv.org/html/2608.04542v4)
also reports 509. No improvement to that record was established in this pass.
