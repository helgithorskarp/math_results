# Terminal coincidences close the full terminal-only Moser–Parts family

**Theorem.** Every terminal-only assembly of the specified Moser spindle M
and full archived Parts A159/B214 gadgets on at most **508 vertices** is
four-colourable, with **terminal coincidences with M allowed**. Gadget
interiors remain private, and every additional unit edge is confined to M
and designated terminals; the precise hypotheses are below. Arbitrary real
translations, rotations, reflections, mixed terminal-contact patterns and
shared terminals between copies are covered.

The fixed spindle colouring **0123132** extends to each covered assembly.
This removes the spindle-disjointness hypothesis from the
[all-contact theorem](../hadwiger_nelson_moser_all_terminal_contacts/README.md).
It closes the remaining terminal-coincidence boundary without a placement
census. It does not assert one common colouring of all possible terminal
placements simultaneously. No five-chromatic graph or record improvement
is obtained.

## Inputs and exact scope

Use complex coordinates

```text
u=1, v=(1+i*sqrt3)/2, rho=(5+i*sqrt11)/6,
M=[0,u,v,u+v,rho*u,rho*v,rho*(u+v)].
f(M[0..6])=[0,1,2,3,1,3,2].
```

M has seven distinct vertices and eleven complete unit edges. This fixed
colouring is proper. A common isometry of the whole assembly is harmless.

Use the archived [A159 coordinates](../hadwiger_nelson_nonmono159_214_lowden2/points159.tsv)
with terminal indices `[141,142,144]`, an equilateral triangle of side sqrt7,
and [B214 coordinates](../hadwiger_nelson_nonmono159_214_lowden2/points214.tsv)
with terminal indices `[186,187]`, a pair at distance three. Indices are
zero-based. The [positive extension certificates](../hadwiger_nelson_long_terminal_gluing/README.md)
show that all 60 non-monochromatic A terminal assignments and all 12 unequal
B terminal assignments extend through the corresponding full gadget.
Only that positive implication is used, not an advertised prohibition of
monochromatic terminal patterns.

Let Vi be each full isometric gadget copy, Ti its terminal set, Ei its
complete internal unit edges, and EM the spindle unit edges. Let G be the
complete unit graph on `M union (union Vi)`. Require:

1. `M intersection Vi` is contained in Ti for every i, and for distinct i,j,
   `Vi intersection Vj` is contained in `Ti intersection Tj`.
2. Every edge of G outside `EM union (union Ei)` has both endpoints in
   `M union (union Ti)`.
3. G has at most 508 vertices.

Thus copies can meet one another or M at designated terminals. Their
interiors do not overlap any other copy or M. Inherited edges from a shared
terminal to its own gadget interior are allowed; hypothesis 2 restricts
**additional** edges. It excludes extra interactions involving an interior.
Reduced gadgets, other connectors and omitted internal edges are not used
to define this family, although every subgraph of a covered G is also
four-colourable by restriction.

A159 has 156 private interior vertices and B214 has 212. Four copies
already require at least 624 private vertices, and three copies including
B require at least `156+156+212=524`. Hence at most three copies occur,
and the only three-copy case is A+A+A. Coincidences with M cannot reduce
these private-interior bounds.

## The new exact geometric observation

Let D be the set of points outside M with at least two unit neighbours in
M. The parent [geometry certificate](../hadwiger_nelson_moser_all_terminal_contacts/certificate.json)
proves D consists of exactly 18 points, each with exactly two M-neighbours.
Completeness is certified by two distinct exact circle intersections for
each of the 21 spindle pairs. Its full proof and checker were replayed in
this pass.

The new [certificate](certificate.json) lists every squared-distance
numerator for the following complete domains:

| Pair domain | Pairs checked | Distance sqrt7 | Distance 3 |
|---|---:|---:|---:|
| Distinct unordered M pairs | 21 | 0 | 0 |
| M times D | 126 | 0 | 0 |

Coordinates use integer numerator vectors divided by12 in the positive
basis `1,sqrt3,sqrt11,sqrt33`. The squared-distance vectors in the new
certificate are divided by144. Thus the forbidden vectors are exactly
`[1008,0,0,0]` and `[1296,0,0,0]`. All 147 entries are compared individually
by separate exact arithmetic; these are not tolerance-based exclusions.

Two consequences are decisive:

- Each A or B terminal set contains at most one point of M.
- If a terminal set contains a point of M, every other terminal in that
  set lies outside D and therefore has at most one M unit neighbour.

Both statements hold for arbitrary real placements: the finite computation
classifies the fixed exceptional set D, not a sampled collection of gadget
orientations.

## Inherited list lemma

Fix f on M as above. For every free terminal x outside M, set

```text
L0(x)={0,1,2,3} minus {f(m): m in M and distance(x,m)=1}.
```

Outside D these lists have at least three colours. On D they have two or
three. The parent exact certificate also proves:

- At every distance-sqrt7 pair in D the available lists are disjoint.
- D has no distance-three pair.
- The fifteen D points with two-element lists induce the unit graph
  P3 plus twelve isolated vertices. Lists differ at adjacent vertices
  of this graph.

We use the following proved abstract lemma from the
[parent proof](../hadwiger_nelson_moser_all_terminal_contacts/README.md):
a finite simple K4-free graph F of maximum degree at most three is
list-colourable if `|L(x)|>=max(2,degree_F(x))`, and the vertices with
two-element lists induce a bipartite graph with no induced P4, with
different lists at adjacent such vertices.

Its proof uses the classical degree-choosability theorem to reduce tight
components to Gallai trees. K4 is excluded, long odd leaf cycles would
induce P4 in the two-list set, and the remaining leaf triangle extends
because its two noncut vertices have different two-element lists. This
abstract lemma, including its classical theorem premise, is inherited
rather than newly established by the 147 distance checks.

We also use a simple greedy fact with **no minimum list size of two**:
if Q is connected, every list has at least the vertex degree, and some
vertex z has strictly more list entries than its degree, then Q is
list-colourable. Root a spanning tree at z and colour in reverse tree
order. Each nonroot vertex has its parent still uncoloured, while z has
a spare colour even after all its neighbours are coloured. This includes
a singleton component with a one-element list.

## Free-terminal auxiliary graph

Write `U=(union Ti) minus M` and let k be the number of terminal sets.
For an A triangle meeting M, select the pair of its other two vertices;
both are outside D by the new geometric observation. For an A triangle
not meeting M, use these choices:

- If at least two vertices lie in D, choose no pair: disjoint lists
  already make the triangle non-monochromatic.
- If exactly one vertex lies in D, select the other two.
- If none lies in D, select any pair.

For a B pair disjoint from M, select its pair. A B pair meeting M is called
anchored: write it as `{m,x}` with `m in M` and `x in U`. Select no edge
for this pair; instead delete f(m) from x's list.

Let F on U contain every actual unit edge between free terminals and all
selected pairs. Identify coincident points and repeated edges. For each
x let b(x) count the anchored B sets containing x, and put

```text
L(x)=L0(x) minus {f(m): {m,x} is an anchored B terminal set}.
```

Counting b by sets, even when two anchor colours agree, gives a valid
upper bound on the number of removed colours. Any proper list colouring
of F makes every A or B terminal set non-monochromatic, respects f at
coincident terminals, and handles all unit contacts with M.

## Degree and list bounds, including shared anchored endpoints

Let a free terminal x belong to r of the k terminal sets. It has no unit
neighbour in a containing set. Each other set supplies at most one unit
neighbour: two would be at distance at most two from each other, whereas
every within-set distance is greater than two. Its free-terminal unit
degree is therefore at most k-r. This bound remains valid when another
set contains a point of M, because M is removed from U.

At most `r-b(x)` selected pairs are incident with x, because anchored B
sets select no pair. Consequently

```text
degree_F(x) <= (k-r)+(r-b(x)) = k-b(x).
```

If k=3, all copies are A, so b is identically zero. No selected edge
touches D. Thus a D vertex has degree at most `k-r<=2`, and every other
vertex has degree at most three. All lists satisfy the degree bounds.

If k<=2 and b(x)=0, the degree is at most two and the list has at least
two colours. If b(x)>0, x lies outside D by the distance-three observation;
its original list has at least three colours. Hence

```text
|L(x)| >= 3-b(x) > 2-b(x) >= degree_F(x).
```

Here b is at most two. In particular, if two anchored B sets share x,
its list may have only one colour, but its auxiliary degree is zero.
This boundary cannot be handled by blindly applying a global two-list
minimum; the strict-surplus greedy argument handles it instead.

Every component containing a vertex with b>0 is colourable by that greedy
argument: all vertex lists have at least their degrees, and that vertex
has strict surplus. Remove these components from consideration. On each
remaining component b is identically zero, so L equals L0 and every list
has at least two entries and at least the respective degree.

## Completing the proof

No selected edge joins two D points. This is explicit for A selections,
and follows for B from the absence of distance-three pairs in D. Therefore
the vertices with two-element lists in any remaining component induce a
subgraph obtained by deleting vertices from the parent's P3 plus isolated
vertices. It is bipartite, has no induced P4, and adjacent two-lists differ.

F is K4-free. For k<=2 this follows from its maximum degree of two.
For k=3, all selected edges have length sqrt7 and there are at most three.
In a hypothetical K4, every pair has distance one or sqrt7. Two unit steps
cannot join a sqrt7 pair, so unit adjacency is transitive and the unit
graph is a union of cliques. At least three of the six edges are unit,
leaving only K4 itself, impossible as a planar unit graph, or a unit
equilateral triangle with a fourth point at distance sqrt7 from each
vertex. A point equidistant from a noncollinear equilateral triangle is
its circumcentre, whose distance is 1/sqrt3, again impossible.

The inherited list lemma now colours every remaining component.
Combine them with the greedily coloured components and f on M.
Every terminal set is non-monochromatic. Extend independently through
each full gadget using the positive terminal certificates. Shared points
are terminals and already have consistent colours. Inherited edges are
proper within their copy or M, and hypothesis 2 puts every additional edge
among vertices whose colours have already been made proper. This proves
the theorem. For k=0 the graph is M itself.

## Reproduction and validation

The [producer](build.py) uses pinned inherited nested-quadratic arithmetic.
The [separate checker](verify.py) imports no producer or inherited code.
It expands squarefree radicals using

```text
sqrt(r)*sqrt(s)=gcd(r,s)*sqrt(r*s/gcd(r,s)^2),
```

with ordinary Python integers. It recomputes every squared distance and
compares all 147 certificate rows, including ordering and domain coverage.
The inherited geometry certificate is SHA-pinned; its completeness proof
is an explicit premise and is separately replayed.

The checker also exhausts 100 palette cases. There are five possibilities
for the initially forbidden M-neighbour colour (none, or one of four),
and ordered anchor-colour sequences of length b=1 or2, with repetition
allowed. The 20 and 80 cases establish minimum remaining list sizes two
and one respectively, and check the singleton boundary. These cases
audit list removal; the universal graph-colouring and geometric-placement
arguments are the analytic proof above. Three malformed certificates
(wrong distance, missing pair, wrong dependency hash) are rejected.

From the repository root, with Python 3.11.2 and the standard library:

```bash
python3 -B hadwiger_nelson_moser_terminal_coincidences/build.py --out /tmp/hn-moser-coincidences
python3 -B hadwiger_nelson_moser_terminal_coincidences/verify.py --work /tmp/hn-moser-coincidences
python3 -B hadwiger_nelson_moser_all_terminal_contacts/build.py --out /tmp/hn-moser-parent
python3 -B hadwiger_nelson_moser_all_terminal_contacts/verify.py --work /tmp/hn-moser-parent
python3 -B hadwiger_nelson_long_terminal_gluing/build.py --out /tmp/hn-gadget-positive
python3 -B hadwiger_nelson_long_terminal_gluing/verify.py --work /tmp/hn-gadget-positive
```

Build output directories must be new. The new checker uses explicit
exceptions, and normal and optimized executions give identical reports.
Keep assertions enabled for the inherited positive-extension scripts.
The new certificate is **2,666 bytes**, with SHA256

```text
d1230606da52f17d5e74e608a04b3123951c4bcf72e1d780f1e40f742cbe5190
```

[Expected results](expected.json), [validation and pinned inputs](validation.json)
and [source hashes](SHA256SUMS) accompany the source. Generation takes
about 0.003 seconds and the separate new audit 0.007 seconds on one thread;
peak memory was not measured. The parent replay checks 300 exact pair
norms, 84 circle equalities, 3060 four-subsets and 120 leaf-triangle list
cases. The positive gadget replay checks 35352 pair norms, 72 terminal
assignments and 50484 expanded edge inequalities. There are **zero native
solver queries**, no new full-gadget placement graph, and no omitted large
certificate or background computation.

Trust lies in the inherited exact geometry, positive extension and
degree-list lemmas; faithful coordinates and field-basis injectivity;
Python integer arithmetic and complete finite loops; and the ordinary
separation, greedy, K4-exclusion and gluing arguments. Separate arithmetic
is author-run validation, not external acceptance or formalization.
External review of this strengthening remains pending.

## Construction decision and shared context

All terminal-only placements in this fixed Moser/full-A159/B214 family at
the target order are now closed, including coincidences. No further
single-contact, mixed-contact or coincidence stratum of this family needs
enumeration. The [accepted older double-contact result](../hadwiger_nelson_moser_terminal_connector_review1/README.md)
also treated some assemblies with arbitrarily many A copies; that extra
copy-count scope is not claimed by this target-order theorem.

A non-four-colourable construction on at most 508 vertices using these full
gadgets and this connector must have additional interactions involving
interiors or interior overlaps.
Changing the connector or reducing a gadget is also outside the theorem.
A useful next step is a bounded actual interior-contact mechanism, chosen
before any larger placement enumeration. That phase is **unstarted**;
this pass ends at the completed terminal-only closure. The retired centered
heptagon family and HN2's separate H514 certification are not reopened.

The startup refresh found no new overlapping contribution through graph
height 3245. The single prepublication refresh reached height 3249 and found
an [independent acceptance of the parent theorem](../hadwiger_nelson_moser_all_terminal_contacts_review1/README.md)
at height 3248. That review checks the geometry, degree-list proof and all
positive gadget extensions. It covers the parent disjoint case, while
external review of this coincidence strengthening remains pending. HN2's [complete H514 core propagation](../hadwiger_nelson_heule514_core_propagation/README.md)
remains separate. Its subsequently published [77-profile pilot](../hadwiger_nelson_heule514_profile_pilot/README.md),
read during the final repository check, certifies 181562 of the 190536
cores four-colourable by a full positive-cover audit. Exactly 8974 unresolved
cores remain: 817 of order 507 and 8157 of order 508. This is an exact
remaining-family reduction, not H514 closure or a target graph. Its next
complete-family decision is unstarted in that durable handoff. Neither
HN2 result supplies a premise here.

Primary calibration on 2026-09-06: [Parts](https://arxiv.org/html/2010.12665v2)
and [Haugland's current manuscript](https://arxiv.org/html/2608.04542v4)
report 509 vertices as the record. This theorem does not improve it.
