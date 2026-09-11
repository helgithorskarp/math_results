# Excluding the entire one-quad five-edge subclass

The subsequent [multiple-quad exclusion](z12_A0_multi_quad_exclusion.md)
closes the entire five-edge high-forest subclass. The proof and all evidence
below are preserved as prerequisites of that combined conclusion.

**Theorem.** A simple graph on 54 vertices with 187 edges, girth at least
five, and twelve degree-eight vertices cannot simultaneously have:

1. all twelve degree-eight vertices as radius-two sinks;
2. five edges among those twelve vertices;
3. every other vertex adjacent to at most four degree-eight vertices; and
4. exactly one other vertex adjacent to four degree-eight vertices.

This is a whole-subclass exclusion. The high-high edges remain variables
in every SAT instance; no high forest or incidence arrangement is sampled.

Together with the [uniform all-sink reduction](z12_A0_reduction.md) and
[all-sink theorem](z12_A1_exclusion.md), it leaves only **five necessary
profiles at five high-high edges**, across the two high forests
$5P_2+2K_1$ and $P_3+3P_2+3K_1$. In particular, both
$P_4+2P_2+4K_1$ and $2P_3+P_2+4K_1$ are excluded in their entirety.
Across all twelve-high candidates, ten high forests and 53 necessary
profiles remain. These are necessary covers, not realizations.

The numerical interval $185\le f(54)\le187$ is unchanged. The five
remaining five-edge profiles, all three-/four-edge profiles, and $z\le11$
remain open.

The proof combines a non-reuse lemma for actual far-neighborhood
incidences, a complete finite normalization, and 38 independently checked
SAT refutations. It does not use the exploratory floating block models.

## Definitions and exact prerequisites

Write $T=V_8$, $H=G[T]$, $C(v)=N(v)\cap T$, $c(v)=|C(v)|$,
$h_t=d_H(t)$, and $F(v)=\{u:\operatorname{dist}(u,v)>2\}$.
Call a vertex with $c=4$ a quad; its high set is also called a quad.
The degree counts are $(|V_6|,|V_7|,|T|)=(16,26,12)$.
For low vertices put
$\epsilon_v=\sum_{u\sim v}(d(u)-6)-8$ at degree six and subtract seven
instead at degree seven.

The [degree/gap result](proof.md) and
[corrected incidence identities](z12_distant_incidence_bound.md) imply,
with all high vertices sinks,

$$
\begin{gathered}
h_t\le2,\qquad
(|N(t)\cap V_6|,|N(t)\cap V_7|)=(3+h_t,5-2h_t),\\
\sum_{V_6}c=46,\quad \sum_{V_7}c=40,\quad
\sum\epsilon=4,\quad \sum(c-3)\epsilon=-2,\\
\sum_{V_6}(c-3)(c-2)/2+\sum_{V_7}(c-1)(c-2)/2=3-k,
\end{gathered}                                                    \tag{1}
$$

where $k$ counts the high vertices of high degree two.
The nonnegative inventory makes $H$ a path forest: a high cycle would
have length at least five and would require $m+k\ge10$.
A six-quad costs one, so $k\le2$ in that case. This forest has $2+k$
isolates.

Distinct vertices' high sets intersect in at most one point. Far vertices
have disjoint high sets. For every low vertex $v$,

$$
\sum_{u\in F(v)}[t\in C(u)]=(8-d(v))[t\notin C(v)]\quad(t\in T).       \tag{2}
$$

Thus the own set and far sets partition $T$ at degree seven, while the
far sets double-cover the complement at degree six.
The far-set sizes are $9-\epsilon$ at degree six and $4-\epsilon$
at degree seven. The epsilon ranges are
$2c-8\le\epsilon\le c-2$ at degree six and
$2c-7\le\epsilon\le c$ at degree seven.

With only one quad, a degree-seven vertex with $(c,\epsilon)=(1,1)$
cannot partition $T$: its three far sets supply at most $4+3+3=10$
of the eleven needed points. The type $(2,2)$ also cannot partition
$T$: two far sets supply at most seven of the ten needed points.
The only negative charge in $(c-3)\epsilon$ is therefore
$(d,c,\epsilon)=(7,2,1)$. Call such a vertex bad, and let $b$ be their
number. Every bad vertex has exactly three far vertices: the quad and
two vertices with high sets of size three, called its helpers.

## Helpers cannot be reused

**Non-reuse lemma.** Two distinct bad vertices using a single quad in
their far partitions cannot share a helper, even if they use different
quads.

First let the quad be the same, with high set $Q$, and suppose the common
helper has triple $A$. Write the other triples as $B,D$. These distinct
triples lie on the five points outside $Q\cup A$, so they meet exactly
once. The first bad vertex's pair is the complement of $B$ on those
five points; it is consequently contained in $D$. This gives two common
high neighbors to distinct vertices, a contradiction.

Now let the quads be distinct, with sets $Q,R$, and again let $A$ be
the common helper. The second partition makes $R$ disjoint from $A$.
The first partition consists of its bad pair, $Q,A$, and its other
helper. These meet $R$ in at most $1,1,0,1$ points, respectively,
and cannot cover its four points.

For a fixed quad, two bad pairs are also disjoint. By non-reuse, each
helper of the second bad vertex is a distinct triple. It meets each
of the first partition's two helper triples and its bad pair in at
most one point. Since it avoids the quad, it must meet all three
exactly once. The second bad pair is therefore disjoint from the first.
In particular, **$b$ bad vertices require $2b$ distinct actual helpers**.

## Complete profile and charge reduction

If the unique quad has degree seven, its inventory cost is three.
Equation (1) forces $k=0$ and profile 361 below. Its epsilon is at least
one, so $b\ge3$ by charge. All bad vertices are far from the quad, which
has at most three far vertices. Exactly three bad vertices would supply
only six high incidences outside the quad, where its partition requires
eight. This excludes the seven-quad case.

Now let the unique quad $q$ have degree six, with $Q=C(q)$, and set
$\sigma=\sum_{t\in Q}h_t$. Exactly $8+\sigma$ other six-vertices meet
$Q$: sum their incidences at its four points, subtract $q$, and use
linearity to ensure they are distinct. Hence exactly

$$
7-\sigma                                                       \tag{3}
$$

other six-vertices have high sets disjoint from $Q$.
Since $H$ has $2+k$ isolates, $\sigma\ge2-k$.
There are at most $2-k$ degree-seven triples by the remaining inventory
budget. At most seven actual triples are therefore available as helpers.
Non-reuse gives $b\le3$.

Any degree-six vertex with $c=1$ contributes at least two positive
charge, forcing $b\ge4$. This excludes profiles 374, 375, and 387.
The exact inventory has no other one-quad profiles besides the ten
listed by the checker. Six remain, all with six-counts $2^3 3^{12}4$:

| Profile | $k$ | degree-seven high counts |
|---|---:|---|
| 366 | 0 | $1^{14}2^{10}3^2$ |
| 367 | 0 | $0^1 1^{11}2^{13}3^1$ |
| 368 | 0 | $0^2 1^8 2^{16}$ |
| 382 | 1 | $1^{13}2^{12}3^1$ |
| 383 | 1 | $0^1 1^{10}2^{15}$ |
| 390 | 2 | $1^{12}2^{14}$ |

Indices refer to the complete deterministic
[a0_inventory.py](a0_inventory.py) census.
The checker independently enumerates the charged multiplicities using
[a0_independent.py](a0_independent.py) and compares all profiles entrywise.

The charge identity and $2\le b\le3$ leave exactly four branches:

| Branch | $b$ | $\epsilon_q$ | other charged exceptions |
|---|---:|---:|---|
| A | 2 | 0 | none |
| B | 3 | 1 | none |
| C | 3 | 0 | one six-vertex with $c=2,\epsilon=-1$ |
| D | 3 | 0 | one seven-vertex with $c=2,\epsilon=-1$ |

All other six-vertices with $c=2$ and all ordinary seven-vertices with
$c=0,1,2$ have epsilon zero. The bad vertices have epsilon one.
Both degrees of triple vertices retain their full permissible epsilon
range. Indeed, the only ways to contribute exactly one unit of positive
charge are the quad with epsilon one and the two exceptional types in
the table; negative epsilon at seven-count zero or one costs at least
three or two.

If there are no degree-seven triples, only branch A is possible.
For $\epsilon_q=1$, the quad has one six-neighbor and one seven-neighbor
outside $T$, whose high counts are at most three and two.
The near partition gives $8-\sigma\le5$, hence $\sigma\ge3$.
But $b=3$ would need six helper triples among at most $7-\sigma\le4$
outside six-vertices. For $\epsilon_q=0$, both low neighbors are sixes;
$8-\sigma\le6$ gives $\sigma\ge2$, leaving at most five helpers, so $b=2$.

## The two complete incidence normalizations

Permute the high labels so $Q=\{0,1,2,3\}$.
For two bad vertices, label their pairs $\{4,5\},\{6,7\}$.
Their four distinct helpers can be labeled

$$
\{6,8,9\},\quad\{7,10,11\},\quad
\{4,8,10\},\quad\{5,9,11\}.                                  \tag{4}
$$

Each pair of helpers belongs to the corresponding bad vertex.
To see completeness, each helper of the second bad vertex meets both
helpers of the first exactly once. The four distinct cross intersections
are the four remaining high points, forming the displayed two-by-two grid.
The remaining element of each helper is its point in the other bad pair.

For three bad vertices, the third pair must avoid the two old pairs.
Within the four-point grid it cannot use a row or a column, since that
would intersect an existing helper twice. Its two choices are the
diagonals, interchanged by a symmetry of (4). Choose $\{8,11\}$.
Its helpers are forced to be

$$
\{4,7,9\},\qquad\{5,6,10\}.                                  \tag{5}
$$

No other configuration is omitted. The independent checker generates
every complement partition on eight labeled points, verifies the grid
conditions, and finds exactly the two third covers.

Helper vertices can have degree six or seven. There are at most two
degree-seven triples in any profile.
The checker tries all $8!$ permutations of the outside points for each
configuration and retains exactly those preserving the bad-pair family,
helper family, and far associations. The induced helper groups have
orders eight and twelve.

With helpers numbered from zero as displayed, complete representatives
for the degree-seven helper positions are:

- Two bad vertices: $\varnothing,\{0\},\{0,1\},\{0,2\}$.
- Three bad vertices:
  $\varnothing,\{0\},\{0,1\},\{0,2\},\{0,3\}$.

Discard only representatives using more seven-helpers than the profile
contains. This yields **38 cases**: nineteen for profile 366, eight each
for 367 and 382, and one each for 368, 383, and 390.
Unselected degree-seven triples remain free vertices.

## The full-graph encoding and trust boundary

[a0_one_quad_sat.py](a0_one_quad_sat.py) introduces an edge variable for
every unordered vertex pair not ruled out by the fixed incidences.
Deleted edges are only those belonging to a prescribed far pair,
a forbidden high pair inside a fixed high set, a fixed missing high-low
incidence, or two fixed low vertices sharing a high neighbor.

It imposes the 54 specified degrees, each low vertex's high count,
five high-high edges, high degree at most two, and the high vertices'
degree-class neighbor counts in (1). Specified epsilon values are imposed
by their equivalent numbers of degree-seven neighbors. Six-triple
vertices have at most three degree-seven neighbors, the radius-two bound.

For every vertex pair, a variable represents each two-edge path by
a three-clause equivalence. At most one edge or two-edge path is permitted.
This excludes every triangle and four-cycle. At least one is required
for every pair involving a high vertex, and for every non-far pair
involving a bad vertex. Every prescribed far pair has all these short
paths forbidden. Thus the displayed bad far sets are exact.

For every low pair, extra far variables are the complements of the
short-path disjunctions. Equation (2) is imposed at every low root and
every high point, using conjunction variables for far incidence and high
adjacency. At an unfixed root its own-incidence term is included with
coefficient $8-d(v)$. These redundant constraints preserve the original
edge and path variable IDs and are appended after the base model.
A seven-triple also has epsilon at most one: with epsilon at least two,
at most two far sets of total size at most seven would have to cover
nine outside points. This valid local bound is imposed explicitly.

One further local consequence is imposed in case 382/A/role 1.
The unique seven-triple is a helper, hence is far from its own bad vertex
and shares a high neighbor with the other; it neighbors neither bad.
At a bad vertex whose helpers include $j$ seven-vertices, the local
weighted identity gives neighbor-epsilon sum $2-j$. Its only possible
contributors are its single six-neighbor (epsilon at most one, since
its quad is far) and the other bad vertex. The bad vertex with two
six-helpers therefore forces their edge and epsilon one at its
six-neighbor. At the other bad vertex, epsilon zero is forced at its
six-neighbor. The latter condition permits six-count two or three;
the former requires six-count three. These exact conditions are encoded
as an edge unit and guarded degree-seven-neighbor counts.
The checker verifies the local weighted identity on four actual graph
controls and checks the small integer implication separately.

The only additional symmetry breaking sorts the high-incidence rows of
free vertices within identical $(d,c,\epsilon)$ classes. It never sorts
high columns simultaneously and does not constrain a high forest.
The uniquely exceptional negative vertex in branch C or D has its own
class and can always be labeled first among the original free vertices.

Every graph in the subclass can therefore be relabeled into one of the
38 formulas. Full formula satisfiability is stronger than a degree
histogram or an aggregate edge-count assignment. Each UNSAT result is
accepted only after a separate DRAT checker validates its trace.

The trust boundary is the written reduction and normalization, the
inspected Python generator and PySAT sequential-counter encoding, and
the compiled DRAT checker. Finite controls compare independent inventory
algorithms and definition-level complement enumeration. They are
validation, not independent peer review or a proof-assistant formalization.
No floating infeasibility, search timeout, or incomplete graph catalogue
is used as proof.

## Reproduction and compact evidence

Run the finite controls with standard-library CPython 3.11 or later:

~~~sh
python3 verify_a0_one_quad.py
python3 -O verify_a0_one_quad.py
python verify_a0_one_quad_encoding.py
~~~

Regenerate all formulas and proofs outside the repository, using
CPython 3.11.2 and python-sat 1.8.dev24 (Glucose 4.1):

~~~sh
python reproduce_a0_one_quad.py --work /tmp/order54-one-quad \
  --checker /path/to/drat-trim
~~~

For reproducible search time, the driver uses the measured proof-generation
stages: the base full-graph model for 34 cases, the quad/helper far equations
for 366/A/role 1, all far equations for 366/A/role 2 and 367/A/role 1,
and the final local cut for 382/A/role 1. Every search formula is an exact
clause prefix of its final formula, with identical original variable IDs.
Every generated trace is checked against the final formula. The source
hash audit regenerates and compares all 38 search/final formula pairs
entrywise at the prefix level; their hashes are included in the compact
record. A trace accepted on the final formula is the evidence used here.

An optional exact case name selects one case. With an explicit conflict
budget, any UNKNOWN result fails and preserves a non-refutation record.
A supplied proof directory can instead be replayed against freshly
regenerated formulas:

~~~sh
python reproduce_a0_one_quad.py --work /tmp/order54-one-quad-replay \
  --checker /path/to/drat-trim --replay /path/to/proofs
~~~

[a0_one_quad_expected.json](a0_one_quad_expected.json) contains the complete
finite controls, all formula and proof hashes, checker identity, and
verification records. Formula and proof files, solver logs, and checkpoints
remain outside Git. The larger no-seven-triple pilot used additional
proved restrictions; its three refutations are preserved locally and are
not needed by the published 38-case proof.

Four initial difficult formulas returned UNKNOWN at a fixed conflict
budget. Their raw status is preserved. Completion requires checked
refutations of the appended far-incidence formulas, and all earlier
traces are separately replayed on freshly generated final formulas.
The compact record identifies the final evidence. The small encoding control
checks 192 Boolean assignments, including repeated variables and negative
literals in the sequential counters. The checker used here is
[drat-trim](https://github.com/marijnheule/drat-trim), source revision
2e3b2dc0ecf938addbd779d42877b6ed69d9a985, built with the repository command
~~~sh
gcc drat-trim.c -std=c99 -O2 -o drat-trim
~~~
Its executable hash is recorded with the evidence.

The primary catalogue and the 2025 lower-bound paper were checked live
on 2026-09-11; the order-54 numerical frontier is unchanged:
[Afzaly–McKay catalogue](https://users.cecs.anu.edu.au/~bdm/data/extremal.html),
[2025 paper](https://arxiv.org/html/2508.05562v1).
The order-53 catalogue is incomplete and is not used as an exhaustive
extension base.
