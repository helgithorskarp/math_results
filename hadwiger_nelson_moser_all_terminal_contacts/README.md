# All terminal contacts to a disjoint Moser connector are four-colourable

**Theorem.** Every terminal-only assembly of the specified seven-point Moser
spindle M and full archived Parts A159/B214 gadgets on at most **508
vertices** is four-colourable, provided **M is vertex-disjoint from every
gadget copy**. Gadget interiors must be private and all new unit edges must
be confined to M and the designated terminals, as defined precisely below.
There is no restriction to single contacts or a finite terminal-triangle
placement class. Arbitrary real translations, rotations, reflections and
shared terminals between gadget copies are allowed.

In fact the fixed spindle colouring **0123132**, in the coordinate order
below, extends to every covered assembly. This does not assert a single
colouring of all possible terminal placements simultaneously. It closes
the mixed-contact interface left by the preceding two connector results,
including the raw `7+3*159=484` construction under these hypotheses.

No five-chromatic graph or record improvement is obtained. A terminal
coincident with a spindle vertex, an interior contact, an overlap involving
a gadget interior, a reduced gadget, or a different connector is outside
this theorem. In particular, vertex-disjointness from M is an essential
stated hypothesis, not a consequence of the vertex budget.

## Fixed spindle and the exact double-neighbour set

In complex coordinates set

```text
u=1, v=(1+i*sqrt3)/2, rho=(5+i*sqrt11)/6,
M=[0,u,v,u+v,rho*u,rho*v,rho*(u+v)].
```

All indices of M are zero-based in this order. Its complete unit graph has
11 edges, and the displayed four-colouring is proper. A common isometry of
the whole assembly changes none of the conclusions.

Let C be the set of all points at unit distance from at least two distinct
vertices of M, and put D=C minus M. The [exact certificate](certificate.json)
proves the following finite geometric facts:

| Object | Exact value |
|---|---:|
| C | 25 points |
| D | 18 points |
| M-neighbours of every D point | exactly 2 |
| Complete unit graph on C | 53 edges |
| Unit graph on D | C4 + 2K2 + 10 isolated vertices |
| Pairs of D points at distance sqrt7 | 4 disjoint pairs |
| Pairs of D points at distance 3 | none |

These are exact distinct-point and distance statements. Coordinates are
integers divided by 12 in the basis `1,sqrt3,sqrt11,sqrt33`. No interval or
rounded-coordinate identification is used in this package.

Completeness follows from a small positive certificate. For every one of
the 21 pairs of distinct spindle points, it supplies **two distinct**
points of C lying on both unit circles. Two different circles have at most
two intersections, so these two witnesses exhaust the possible common
neighbours of that pair. Every point with at least two M-neighbours occurs
for some pair. The checker verifies that the union of all witnesses is
exactly the listed 25 points and that M is contained in it. Thus every
point outside M with two or more M-neighbours lies in D; the full neighbour
check then proves that no such external point has three M-neighbours.

For production, most circle pairs can be constructed from a common
spindle neighbour r: the other intersection is p+q-r. The bridge pair
M[3],M[6] has no common neighbour inside M, so its two equilateral
completions are constructed directly. The independent proof checker
trusts neither case selection nor these formulas: it verifies both exact
intersection witnesses for all 21 pairs.

## Available colour lists

Fix f on M to the colour string 0123132. At any external terminal x, use

```text
L(x) = {0,1,2,3} minus {f(m): m in M, distance(x,m)=1}.
```

A point outside D and outside M has at most one spindle neighbour, so its
list has size at least three. Every D point has a list of size two or
three. Of the 18 points of D, **15 have two-element lists and three have
three-element lists**.

Let S be the 15 points with two-element lists. The complete unit graph on
S is exactly **P3 plus 12 isolated vertices**. At the two edges of this
P3, the endpoint lists are different. These facts are checked exactly.
In the order of D obtained by deleting M from the sorted C coordinate
list, the nontrivial path has centre 8 and leaves 12,13, with lists

```text
L(8)={0,1}, L(12)={0,3}, L(13)={0,2}.
```

The available lists are disjoint at the endpoints of **each** sqrt7 pair
in D. Those pairs, in the same D indexing, are

```text
(0,17), (1,15), (3,7), (4,9).
```

Consequently any equilateral sqrt7 terminal triangle containing two D
points is automatically non-monochromatic in every colouring from its
available lists. A distance-three terminal pair cannot contain two D
points at all. These two observations handle the contacts that were not
covered by the earlier three-list extension theorem.

## A list-colouring lemma

We use the classical degree-choosability theorem from Erdős, Rubin and
Taylor, *Choosability in graphs*, Congressus Numerantium 26 (1980),
[printed page 142, in the original paper](https://users.renyi.hu/~p_erdos/1980-07.pdf).
In its standard block formulation, a connected graph is colourable from
every assignment of lists having at least the respective vertex degrees
unless all its blocks are cliques or odd cycles. A connected graph whose
blocks have those forms is called a Gallai tree. Bridges count as K2
blocks. This classical theorem is an explicit imported mathematical
premise; it is not attributed to the present computation.

Here is the additional lemma needed for the construction.

**Lemma.** Let F be a finite simple K4-free graph of maximum degree at
most three, with lists satisfying `|L(x)| >= max(2,degree_F(x))`. Let S be
the vertices with two-element lists. Suppose F[S] is bipartite and has no
induced four-vertex path, and adjacent vertices of S have different lists.
Then F has a proper list colouring.

**Proof.** Work in one connected component Q. If some vertex has a list
strictly larger than its degree, root a spanning tree there and colour in
reverse tree order, leaving the root last. Each other vertex still has
its parent uncoloured and therefore has fewer coloured neighbours than
list entries. The root has more list entries than neighbours. This colours
Q. Thus only the case `|L(x)|=degree_Q(x)` at every vertex remains.
In that case the minimum degree is at least two and every degree-two
vertex belongs to S.

If Q is not a Gallai tree, the imported degree-choosability theorem gives
a list colouring. Suppose Q is a Gallai tree. A block larger than K3
cannot be a clique: K4 is excluded, and larger cliques exceed the degree
bound. A single-block Q cannot be K1 or K2 because of its minimum degree;
it cannot be an odd cycle (including K3), because all its vertices would
have degree two and lie in the bipartite graph F[S].

Hence Q has at least two blocks. Take a leaf block B, with unique cut
vertex x. If B were K2, its noncut vertex would have degree one, again
impossible. Therefore B is an odd cycle. Every vertex of B other than x
has degree two in Q and belongs to S. If B had length at least five,
four consecutive vertices of B-x would induce a four-vertex path in
F[S]. This is impossible: a cycle block has no chord, and the subgraph
on its noncut vertices is induced. Thus B is a triangle with noncut
vertices a,b in S.

Delete a,b. The remaining graph is connected, all lists still have at
least the remaining degrees, and x has a strict surplus because it lost
two neighbours. The rooted greedy argument therefore colours the whole
remainder. Let its colour at x be c. Each of L(a)-{c}, L(b)-{c} is nonempty.
They fail to admit unequal choices only if both are the same singleton,
which would force `L(a)=L(b)={c,d}` for some d. The lists are different
by hypothesis. Thus the colouring extends to a,b and hence all of Q.
Components combine independently, proving the lemma.

The lemma works over any finite palette. Our application has four colours.
The code separately checks all 120 ordered pairs of different two-element
subsets of that palette with all choices of c. It also verifies that equal
two-lists can fail, so that compatibility condition is not silently dropped.

## Applying the lemma to all terminal contact patterns

First take at most three A terminal triangles, or at most two terminal
sets of either gadget type. Denote them by Ti, their union by T and the
number of sets by k. All within-set distances are greater than two.
Construct an auxiliary graph F on the actual points of T as follows:

- Include **every** unit edge between terminals.
- For an A triangle with at least two points in D, add no inequality edge:
  its non-monochromaticity is already forced by disjoint available lists.
- For any other A triangle, choose the pair of terminals outside D if it
  has one D point, or any pair if it has none. Add that pair as an inequality.
- For a B pair, add its pair as an inequality. It has at most one D point,
  because there is no distance-three pair in D.

Thus at most one auxiliary inequality is added per terminal set, and
**no auxiliary edge joins two points of D**. Shared terminals and repeated
selected pairs cause no problem: vertices and edges are identified in F.
A proper list colouring of F makes every terminal set non-monochromatic.

At a terminal in r of the k sets, its unit degree is at most k-r. There
is no unit neighbour inside a containing set, and each other set contains
at most one, by the triangle inequality and within-set separation greater
than two. At most r chosen inequality edges are incident with it. Therefore
`degree_F(x)<=k<=3`.

When k=3 all sets are A triangles in the application below, so no selected
edge is incident with D; a D vertex consequently has degree at most k-r,
which is at most two. When k is at most two, the general bound already
puts every degree at most two, including B endpoints in D. Thus every
terminal's available list has at least its auxiliary degree and at least
two entries.

The vertices of F with two-element lists form exactly T intersect S. Since
no selected edge joins two D points, their induced graph is an induced
subgraph of the complete unit graph on S. It is therefore bipartite and
has no induced P4, and the endpoint lists on every such edge are different.

It remains to exclude K4 from F. If k is at most two, the degree bound
already excludes it. If k=3, every auxiliary edge has length sqrt7 and
there are at most three. In a hypothetical K4 each pair of points has
distance either one or sqrt7. Unit adjacency among the four points is
transitive, since two unit steps have length at most two, less than sqrt7.
Its unit graph is therefore a union of cliques and has at least three
edges. The only possibilities are four pairwise unit points, impossible
in the plane, or an equilateral unit triangle and a point equidistant at
sqrt7 from all its vertices. The latter point would have to be the
circumcentre, at distance 1/sqrt3. This too is impossible.

All hypotheses of the list-colouring lemma now hold. Its colouring of F
is proper on every terminal unit edge, avoids every adjacent spindle
colour, and makes each A or B terminal set non-monochromatic. This is a
proof for arbitrary actual placements; no exhaustive triangle-placement
or three-copy census is a premise.

## Lifting and the 508-vertex bound

Use the complete unit graphs of the archived
[A159](../hadwiger_nelson_nonmono159_214_lowden2/points159.tsv) and
[B214](../hadwiger_nelson_nonmono159_214_lowden2/points214.tsv) coordinate
sets. Their designated terminal indices are `[141,142,144]` and
`[186,187]`, with distances sqrt7 and three respectively. The
[positive extension certificates](../hadwiger_nelson_long_terminal_gluing/README.md)
prove that all 60 non-monochromatic A terminal assignments and all 12
unequal B terminal assignments extend through the full gadgets. Only this
positive direction is used; no monochromatic-pattern refutation is a
premise or newly established result.

Precisely, let Vi be each full gadget copy, Ti its terminal set, Ei its
internal strict unit edges and EM the spindle's unit edges. Let G be the
complete unit graph on `M union (union Vi)`. Require:

1. `M intersection Vi` is empty for every i; for distinct i,j,
   `Vi intersection Vj` is contained in `Ti intersection Tj`.
2. Every edge of G outside `EM union (union Ei)` has both endpoints in
   `M union (union Ti)`.
3. G has at most 508 vertices.

A copy of A has 156 private interior vertices and B has 212. Four copies
already have at least 624 private vertices; three including B have at
least `156+156+212=524`. Thus the only possible three-copy case is A+A+A,
and every other covered case has at most two copies. These are exactly
the terminal cases proved above. The case of no gadgets is just M.

Apply the terminal colouring and independently extend it through each
full copy using the positive certificates. Shared points are terminals,
so the assignments agree. Inherited edges are proper inside their copy
or M, and every new edge is handled by the terminal colouring or its
available list. This proves G four-colourable with the fixed spindle
precolouring. Restricting gives a four-colouring of every subgraph of G.

## Reproduction and exact verification

The [producer](build.py) imports the pinned rational-tower arithmetic of the
previous positive-extension checker and generates the compact 1,527-byte
certificate. The [separate checker](verify.py) imports no producer or
inherited arithmetic. It reconstructs M directly by complex multiplication
and uses a generic multiplication table for Q(sqrt3,sqrt11), with rational
coefficients. It verifies all circle witnesses instead of reusing the
producer's reflection/equilateral construction.

The independent audit checks all **300 pairs** of the 25 distinct points,
all **84 unit equalities** in the two-witness coverage of the 21 spindle
pairs, every external M-neighbour set, the entire D unit graph and the
sqrt7/distance-three pair lists. It verifies bipartiteness and all **3,060
four-point subsets** for the absence of an induced P4, then independently
checks the smaller two-list graph, all four disjoint long-pair lists and
all six unit-pair compatibility conditions. All 120 leaf-triangle list
cases and three malformed-certificate rejection controls pass.

From the repository root with Python 3.11.2 and the standard library:

```bash
python3 -B hadwiger_nelson_moser_all_terminal_contacts/build.py --out /tmp/hn-moser-all
python3 -B hadwiger_nelson_moser_all_terminal_contacts/verify.py --work /tmp/hn-moser-all
python3 -B hadwiger_nelson_long_terminal_gluing/build.py --out /tmp/hn-positive-gadgets
python3 -B hadwiger_nelson_long_terminal_gluing/verify.py --work /tmp/hn-positive-gadgets
```

The two build output directories must be new. Assertions must be enabled
for the inherited positive-extension scripts. The new checker uses explicit
exceptions; normal and optimized executions produce identical reports.
[Expected checks](expected.json), [validation and pinned inputs](validation.json)
and [source hashes](SHA256SUMS) accompany the source.

Certificate generation takes about 0.008 seconds and the separate audit
0.23 seconds on one thread. Peak memory was not measured. The imported
positive replay checks 35,352 exact coordinate-pair norms and all 72
terminal assignments, totalling 50,484 expanded edge inequalities. There
are **zero native solver queries**. Generated state and the downloaded
historical paper remain local; no large data file or omitted proof trace
is needed to reproduce this result.

Trust lies in the classical degree-choosability theorem, the ordinary
circle-intersection, block, separation and gluing arguments, exact coordinate
transcription and field-basis injectivity, Python integer/Fraction behaviour,
complete loops and positive certificate decoding. The new checker is a
separate author-run implementation, not external acceptance or formalization.
External review of this new theorem is pending.

## Decision and remaining construction boundary

The [accepted double/single-contact result](../hadwiger_nelson_moser_terminal_connector_review1/README.md)
and the [single-contact extension theorem](../hadwiger_nelson_single_contact_extension/README.md)
left mixed contact types open. This theorem closes **all** contact types
under the current spindle-disjoint, private-interior hypotheses. There is
no reason to enumerate another terminal placement class within that family.
The earlier double-contact theorem also allowed some terminal coincidences
with M and arbitrarily many copies; those extra cases are not claimed as
consequences of this size-restricted disjoint theorem.

A concrete remaining boundary is allowing a gadget terminal to coincide
with a spindle vertex while keeping all other interactions terminal-only.
Such a terminal is precoloured and may see three or four spindle neighbours,
so the present available-list argument does not apply. That phase is
**unstarted**. Interior contacts, reduced gadgets and a different geometric
construction are also possible escapes requiring separate work. This pass
does not begin them.

The shared refresh found HN-2's [complete H514 core propagation](../hadwiger_nelson_heule514_core_propagation/README.md):
68,378 residual graphs are now certified four-colourable, leaving an exact
family of 190,536 unresolved cores. That separate certification result
supplies no premise here and is not duplicated.

Primary-source calibration on 2026-09-06: Parts'
[paper](https://arxiv.org/html/2010.12665v2) and
[Haugland's current manuscript](https://arxiv.org/html/2608.04542v4) report
509 vertices as the record. This result does not improve it.
