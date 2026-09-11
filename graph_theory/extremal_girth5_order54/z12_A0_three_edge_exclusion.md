# The three-edge layer closes the twelve-high boundary

**Conditional theorem.** There is no simple graph with 54 vertices,
187 edges, girth at least five, degree counts $(n_6,n_7,n_8)=(16,26,12)$,
and all of these properties:

- Every vertex of $T=V_8$ is within distance two of every vertex.
- $H=G[T]$ has three edges.
- Every low vertex $v\notin T$ has $c(v)=|N(v)\cap T|\le4$.

This is a **complete layer exclusion**. The raw inventory contains 121
profiles: 82 are excluded by human arguments. The other 39 profiles have
135 normalized quad cases. A new structural lemma excludes 84 of those
cases; the remaining 51 have independently checked contradictions.

Together with the [all-sink theorem](z12_A1_exclusion.md),
[uniform reduction](z12_A0_reduction.md), and the complete
[five-edge](z12_A0_multi_quad_exclusion.md) and
[four-edge](z12_A0_four_edge_exclusion.md) exclusions, this excludes
**every twelve-high candidate**. Combining with the preserved
[thirteen-high exclusion](boundary_exclusion.md) and
[degree reduction](README.md), every remaining 187-edge candidate has

$$
 (n_6,n_7,n_8)=(z+4,50-2z,z),\qquad 0\le z\le11.
$$

No graph is realized and the numerical interval
$185\le\operatorname{ex}(54,\{C_3,C_4\})\le187$ is unchanged.
All remaining $z\le11$ cases are open.

## Complete inventory and individual incidence identities

Write $C(v)=N(v)\cap T$, $h_t=d_H(t)$,
$k=|\{t:h_t=2\}|$, and $F(v)=\{u:\operatorname{dist}(u,v)>2\}$.
For low vertices set

$$
 s_v=\sum_{u\sim v}(d(u)-6),\qquad
 \epsilon_v=
 \begin{cases}s_v-8&d(v)=6,\\s_v-7&d(v)=7.\end{cases}
$$

The [corrected identities](z12_distant_incidence_bound.md), specialized
to the theorem's hypotheses, give

$$
\begin{split}
 &s_t=5,\qquad h_t\le2,\qquad
 (|N(t)\cap V_6|,|N(t)\cap V_7|)=(3+h_t,5-2h_t),\\
 &\sum_{V_6}c=42,\qquad\sum_{V_7}c=48,\\
 &\sum\epsilon=4,\qquad\sum c\epsilon=6,\qquad
 \sum(c-3)\epsilon=-6,\\
 &\sum_{V_6}\frac{(c-3)(c-2)}2+
   \sum_{V_7}\frac{(c-1)(c-2)}2=5-k.                         \tag{1}
\end{split}
$$

Here $H$ is a path forest with three edges, so $k\in\{0,1,2\}$.
The three possibilities are $3P_2+6K_1$, $P_3+P_2+7K_1$, and $P_4+8K_1$.

Let $n_{dc}$ count degree-$d$ vertices with high-count $c$. The
nonnegative integer solutions of the two vertex totals, two incidence
totals and (1), with $c\le4$, form the raw inventory:

| Quad type | Profiles |
|---|---:|
| No quads | 42 |
| Unique quad at degree six | 30 |
| Unique quad at degree seven | 10 |
| At least two quads | 39 |

A quad is a low vertex with high-count four. The 39 multiple-quad
profiles are distributed as follows:

| $k$ | Six-quads | Seven-quads | Profiles |
|---:|---:|---:|---:|
| 0 | 1 | 1 | 3 |
| 0 | 2 | 0 | 10 |
| 0 | 2 | 1 | 1 |
| 0 | 3 | 0 | 6 |
| 0 | 4 | 0 | 3 |
| 0 | 5 | 0 | 1 |
| 1 | 1 | 1 | 1 |
| 1 | 2 | 0 | 6 |
| 1 | 3 | 0 | 3 |
| 1 | 4 | 0 | 1 |
| 2 | 2 | 0 | 3 |
| 2 | 3 | 0 | 1 |

The complete numerical rows are in the
[compact evidence](three_edge_expected.json). The original
[a0_inventory.py](a0_inventory.py) recursion and the different
[charged-multiplicity enumeration](a0_independent.py) agree entry by entry
on the full 403-profile census, including these 121 rows. No preceding
23-profile filter is used as a premise.

Distinct vertices' high sets intersect in at most one point.
Every high pair has exactly one edge or two-edge connection, so

$$
 [ab\in E(H)]+|N_H(a)\cap N_H(b)|
 +|\{v\notin T:\{a,b\}\subset C(v)\}|=1.                    \tag{2}
$$

In particular each low high set is independent in $H^2$.
At a low root $v$, the high sets of its low neighbors partition

$$
 T\setminus\left(C(v)\cup\bigcup_{a\in C(v)}N_H(a)\right).    \tag{3}
$$

The far sets satisfy

$$
 \sum_{u\in F(v)}[t\in C(u)]=(8-d(v))[t\notin C(v)],          \tag{4}
$$

$$
 |F(v)|=9-\epsilon_v\quad(d(v)=6),\qquad
 |F(v)|=4-\epsilon_v\quad(d(v)=7).                          \tag{5}
$$

All far vertices are low, since the highs are sinks.
If $q$ is a quad and $r_7(q)$ counts its degree-seven low neighbors,
then its low degree, epsilon, far cardinality, and far multiplicity are:

| $d(q)$ | Low neighbors | $\epsilon_q$ | Far vertices | Multiplicity outside $C(q)$ |
|---:|---:|---:|---:|---:|
| 6 | 2 | $r_7(q)$ | $9-r_7(q)$ | 2 |
| 7 | 3 | $1+r_7(q)$ | $3-r_7(q)$ | 1 |

## Negative charge, transversals, and helper non-reuse

Call a seven-vertex bad if $(c,\epsilon)$ is $(1,1)$ or $(2,1)$,
with counts $b_1,b_2$. The possible $(2,2)$ type is impossible: its
two far high sets have size at most four and cannot cover ten points.

The elementary degree bounds give $\epsilon\le c-2$ on $V_6$ and
$\epsilon\le c$ on $V_7$. The only negative charges in (1) are therefore
the bad vertices. A six-root with $c=0$ contributes at least six,
one with $c=1$ at least two, and quad charges are given in the table.
Thus

$$
 W:=2b_1+b_2\ge
 6+n_{74}+\sum_q r_7(q)+6n_{60}+2n_{61}.                    \tag{6}
$$

All omitted charges are nonnegative. Every bad vertex has exactly
three far vertices, giving one of these disjoint partitions:

- Own singleton: two quads and a triple, $1+4+4+3=12$.
- Own pair: one quad and two triples, $2+4+3+3=12$.
- Own pair: two quads and a pair, $2+4+4+2=12$.

**Unused-quad transversal lemma.** A quad not used in such a partition
meets each of its four blocks in exactly one point.

Indeed each block is the high set of a different low vertex, hence
meets the unused quad in at most one point. The four blocks partition
all twelve high points and must cover its four points.

**Helper non-reuse.** A triple cannot be a helper of two distinct bad
pairs whose partitions each use a single quad.

If the quad is the same $Q$ and the shared helper is $A$, the two other
helper triples $D_1,D_2$ lie on five points outside $Q\cup A$.
Equality would make the two own bad pairs equal, violating linearity.
Otherwise $D_1,D_2$ meet exactly once, and the first own pair, complementary
to $D_1$ on those five points, lies in $D_2$, also violating linearity.

If the quads $Q,R$ differ, the shared helper is disjoint from $R$ in
the second partition. But $R$ is unused in the first partition and
must meet that helper once, a contradiction.
No non-reuse statement is imposed on double-quad covers.

## Human exclusion of all zero-quad and one-quad profiles

With no quad, no bad partition is possible, contrary to (6).
This excludes all 42 zero-quad profiles.

With a unique seven-quad, bad singletons are impossible and every bad
pair is far from that quad. Equation (6) requires at least seven bad
pairs, whereas the quad has at most three far vertices. This excludes
all ten such profiles.

With a unique six-quad $Q$, all bad vertices are pairs using $Q$ and
two helpers. Their own high pairs are pairwise disjoint. To see this,
compare two partitions on the eight points outside $Q$. Each helper
triple of the first meets the second own pair and its two helpers in
at most one point each; helper non-reuse ensures the helper vertices
are distinct. All three intersections must therefore be singletons.
The two disjoint first helpers exhaust the second own pair, making it
disjoint from the first own pair.

There can be at most four disjoint pairs on eight points, whereas (6)
requires at least six. This excludes all 30 unique-six-quad profiles.
All 82 zero-quad or one-quad profiles are now closed.

## A double-quad cover must exist

Let $q=n_{64}+n_{74}\ge2$ be the number of quads, and let
$L=n_{63}+n_{73}$ count all triple high sets. The six-vertex total and
incidence sum give

$$
 n_{63}=10+2n_{60}+n_{61}-2n_{64}.
$$

Expanding the inventory in (1) gives

$$
 3n_{60}+n_{61}+n_{64}+n_{70}+n_{73}+3n_{74}=5-k.
$$

Adding these identities yields

$$
 L=15-3q-k-n_{60}-n_{70}\le9.                               \tag{7}
$$

Suppose no bad partition uses two quads. Then $b_1=0$ and every bad pair
uses two triple helpers. Helper non-reuse gives $2b_2\le L\le9$.
But (6) gives $b_2\ge6$, a contradiction. Therefore **some bad partition
uses two quads**.

Define the disjointness graph $D$ on the quads: two quads are adjacent
when their high sets are disjoint. The two quads in a double-quad
partition are adjacent in $D$. By the unused-quad transversal lemma,
every other quad meets both. Consequently that edge is an
**isolated two-vertex component of $D$**.

This excludes every quad family without such a component, independently
of the high forest and of all unknown low edges.

## Complete normalization before choosing the high edges

The new model chooses the three high edges as variables. This lets us
normalize the quad family under all permutations of the twelve high
points, instead of fixing a forest first. Quad degree roles are retained.

For a family of $q$ quads, color each high point by the subset of quad
labels containing it. A point shared by a subset $J$, $|J|\ge2$,
consumes all label pairs in $\binom J2$. Linearity says these consumed
pair sets are disjoint between shared points. Each such $J$ occurs at
most once. Enumerate all families of these subsets with pair-disjoint
consumption and at most four shared incidences at any quad. Fill each
quad to size four with private points and add unused points to reach
twelve. Reject unions larger than twelve.

This [shared-point generator](three_quad_orbits.py) is complete:
every linear quad family has exactly that shared/private decomposition.
The sorted multiset of point colors is a complete invariant up to point
permutation. Minimizing it over quad permutations preserving degree
therefore gives one representative per allowed orbit.

A different [augmentation checker](verify_three_quad_orbits.py) begins
with one quad and extends each preceding representative by **every**
four-subset of the twelve points compatible with linearity. It tests
isomorphism directly by degree-preserving quad bijections and counters
of point-membership subsets. It does not call the production canonical
key or shared-point recursion. Induction proves completeness; it checks
every augmentation orbit matches exactly one proposed representative
and that no two proposed representatives are isomorphic.

The complete orbit table is:

| Six-quads | Seven-quads | All orbits | Orbits with an isolated disjoint pair |
|---:|---:|---:|---|
| 1 | 1 | 2 | 1 |
| 2 | 0 | 2 | 1 |
| 2 | 1 | 7 | 2, 3 |
| 3 | 0 | 5 | 2 |
| 4 | 0 | 6 | 2, 3, 5 |
| 5 | 0 | 8 | 2, 4, 6, 7 |

There are 30 degree-role orbits, reused separately in the 39 profiles to
give 135 cases. The isolated-pair lemma excludes 84 cases. Exactly
**51 cases remain**, covering every possible multiple-quad profile.
The exact raw, excluded and residual case lists are in the evidence.

## Choosing the high graph and individual quad incidences

The [CNF generator](three_edge_sat.py) has a Boolean variable $H_{ab}$
for each of the 66 possible high edges, exactly three of which are
selected. Each high degree is at most two.
For each unordered pair $\{a,b\}$ and distinct middle point $w$,
a variable $P_{abw}$ is equivalent to $H_{aw}\wedge H_{bw}$.
The total of these path variables is $k$.
Equation (2) is imposed exactly, with contributions from high edges,
high paths and selected low high sets. It automatically excludes high
triangles, repeated short connections, and low sets violating
independence in $H^2$.

Candidate low vertices are slots $(d,B,j)$ with actual labeled high
set $B$. All quads are fixed by their orbit. Every smaller set of a
required size and degree is available if it meets each quad in at most
one point. A set of size at least two cannot repeat; its alternative
degree slots compete for their high pairs. Singleton multiplicity is
allowed up to five, the maximum of either degree-specific high-point
quota. Empty sets allow the full profile count. Prefix order applies
only to indistinguishable same-degree copies.

The model imposes exact profile counts and, at each high point,

$$
 \sum_{\substack{v\in V_6\\t\in C(v)}}1=3+\sum_{u\ne t}H_{tu},
 \qquad
 \sum_{\substack{v\in V_7\\t\in C(v)}}1=5-2\sum_{u\ne t}H_{tu}. \tag{8}
$$

For every quad $q$ and compatible low slot $v$, a variable $N_{qv}$
specifies actual adjacency to that quad and requires the slot selected.
It is symmetric on pairs of quads and has exact sum $d(q)-4$.
For every $t\notin C(q)$ the model imposes

$$
 \sum_{\substack{v\notin T\\t\in C(v)}}N_{qv}
       +\sum_{a\in C(q)}H_{at}=1.                           \tag{9}
$$

This is the pointwise near partition (3), including its dependence on
the chosen high graph. Far variables at quads require selected endpoints
with disjoint high sets, are symmetric on quad pairs, are disjoint from
the near variables, and satisfy (4)--(5) exactly.

Chosen bad vertices use one of the complete four-block partitions above.
Every far endpoint is selected, quad far incidences agree in both
directions, unused quads meet every block once, and single-quad helpers
are not reused. The charge inequality (6) counts the seven-neighbors
of each quad from its $N$ variables.

This **base** model refutes 49 of the 51 cases.

## The two packing cases

For a quad $q$ with $Q=C(q)$, put $\sigma(Q)=\sum_{t\in Q}h_t$.
Point quotas and linearity give exactly

$$
 |\{v\in V_6:v\ne q,\ C(v)\cap Q=\varnothing\}|
       =4-\sigma(Q)+3[d(q)=6].                             \tag{10}
$$

The total six-incidences on $Q$ are $12+\sigma(Q)$. Remove the four
incidences contributed by $q$ when it is a six-vertex; every other
six-vertex meeting $Q$ contributes exactly one. Subtraction from
$16-[d(q)=6]$ gives (10).

The distinct degree-six triple helpers of chosen single-quad bad
partitions at $Q$ and the degree-six neighbors of $q$ whose high sets
are not triples are disjoint sets of vertices outside $Q$.
If their counts are $a_q,r_q$, then

$$
 a_q+r_q+\sigma(Q)\le4+3[d(q)=6].                           \tag{11}
$$

The **packing** stage appends (11), using the high-edge variables for
$\sigma(Q)$. It refutes the two residual cases **(179,2)** and
**(243,2)**, where the second entry is the quad-orbit index above.
The remaining 49 cases use base. Every orbit retains all high-edge
choices satisfying its profile, including all relevant forest shapes.

For the required graph-to-CNF direction, take any hypothetical graph
under the theorem's assumptions. Its raw profile is among the 121
listed. Human arguments exclude the 82 zero/one-quad profiles. For
a multiple-quad profile, the graph's quads give a normalized orbit;
the isolated-pair lemma places it in the 51-case residual cover.
Select its actual high edges, low slots, quad neighbors, far sets and
all bad vertices. Prefix-order indistinguishable copies. Every imposed
condition follows from (1)--(11) and the proved helper lemmas, so the
assignment extends through the cardinality encodings to satisfy that
case. All 51 cases are contradictory. This proves the entire layer
exclusion.

The model need not impose all low-only triangle and four-cycle
conditions. It is a necessary incidence relaxation; no satisfying
partial assignment would by itself be a graph realization.

## Reproduction and independent controls

Use CPython 3.11.2 and python-sat 1.8.dev24, from this directory:

~~~sh
python verify_three_edge_layer.py
python -O verify_three_edge_layer.py
python verify_three_edge_encoding.py
python reproduce_three_edge_layer.py \
  --work /absolute/path/outside-repository/three-edge \
  --checker /absolute/path/to/drat-trim
~~~

The driver defaults to all 51 residual cases and unlimited conflicts.
It checks the whole input manifest against
[three_edge_expected.json](three_edge_expected.json). To run one case,
add <code>--case three_179_2</code>; the result is explicitly partial.
The option <code>--replay /absolute/path/to/named-traces</code> checks
retained DRUP traces against regenerated inputs. SAT, UNKNOWN, failed
checks, and complete-run input-manifest mismatches fail visibly.

Use drat-trim revision
<code>2e3b2dc0ecf938addbd779d42877b6ed69d9a985</code>, built with
<code>gcc drat-trim.c -std=c99 -O2 -o drat-trim</code>.
The executable used here has SHA-256
<code>9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a</code>.
The solver is Glucose 4 through python-sat.

There are **five independent input-formula unit refutations and
46 checked DRAT refutations**. The separate
[unit checker](a0_unit_check.py) propagates deduplicated non-tautological
clauses. It agrees with truth tables on all 512 formulas over the nine
non-tautological clauses on two variables: 417 UNSAT and 416 unit
refutations. Every DRAT check must return zero and print VERIFIED.
Solver UNSAT output alone is never used as proof.

The [finite verifier](verify_three_edge_layer.py) checks the entire
raw inventory, the exact triple identity (7), all 135/84/51 case lists,
and the independent 30-orbit augmentation audit. Normal and optimized
outputs agree byte for byte. A separate high-edge control examines
all $\binom{66}{3}=45,760$ labeled three-edge choices: 1,980 have degree
above two and 220 have repeated short connections. The remaining
43,560 are exactly 13,860 matching forests, 23,760 forests of type
$P_3+P_2$, and 5,940 paths $P_4$, with the unused points isolated.

The signed high-point quota control checks 144 assignments directly
against (8); eight assignments check the high-path conjunction.
The general signed/repeated-literal and guarded-cardinality control
checks 4,608 assignments.

The [positive-control bridge](three_edge_positive_control.py) takes
the two independently checked
[four-edge partial incidence objects](four_edge_controls.json),
normalizes their quads under the new full point symmetry, fixes their
actual high edges and every main incidence variable, and verifies that
the generalized encoder accepts both base and packing assignments.
This checks the new unknown-high-graph encoding on nonvacuous data.
The production driver and theorem cases always require $m=3$; $m=4$
is enabled solely for this control. Two malformed direct fixtures are
rejected. These controls are partial incidence objects, not graphs.

All 51 public-source formulas were regenerated and matched their
independently checked discovery inputs. The complete publication
driver was also run end to end over all 51 cases, with exact manifest
agreement and independent contradiction checks. The complete replay reports
a peak resident set of 159,544 KiB for both self and child resource records.

The evidence records every formula and trace hash, stage, check method,
the finite cover, versions and resource measurements. Input-manifest
rows are (case, stage, variables, clauses, slots, high-edge variables,
formula SHA-256), in case-generator order. Digests use JSON with sorted
keys and comma/colon separators. The whole input-manifest SHA-256 is
<code>4ad51eb31a23bb0a03d163f9d17d47ea695bf8a990dbe52c6a16cc42fb92843b</code>.
Fresh valid DRAT traces may differ; formula hashes and the complete
case cover must agree.

Selected-case discovery building/solving totaled 36.130 seconds;
public formula regeneration 14.617 seconds; and independent
parsing/unit/checking 39.952 seconds. The maximum individual check was
9.619 seconds. Formulas range from 21,035 to 49,199 variables and
44,217 to 100,625 clauses. Original selected traces total 49,145,395
bytes and remain outside Git, with all raw formulas, logs and exploratory
budget-limited outcomes. The reproduction driver regenerates them.

The trust boundary is the human graph-to-model reduction, complete
inventory and quad classifications, Python, python-sat's cardinality
encoding, and independent unit/DRAT checking. No external peer review
or proof-assistant formalization is claimed. The numerical extremal
problem remains open.

The [primary extremal catalogue](https://users.cecs.anu.edu.au/~bdm/data/extremal.html)
and [2025 construction paper](https://arxiv.org/html/2508.05562v1)
were refreshed on 2026-09-11. The catalogue lists lower bound 185 at
order 54 and exact value 181 at order 53. Its incomplete order-53 graph
collection is not used as an exhaustive extension base. No historical
priority claim is made.
