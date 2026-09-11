# The entire four-edge all-sink layer is excluded

**Subsequent refinement.** The [complete three-edge exclusion](z12_A0_three_edge_exclusion.md)
now closes every twelve-high candidate. The theorem and historical
three-edge remainder below are preserved.

**Conditional theorem.** There is no simple graph with 54 vertices,
187 edges, girth at least five, degree counts $(n_6,n_7,n_8)=(16,26,12)$,
and all of the following properties:

- Every vertex of $T=V_8$ is within distance two of every vertex.
- $H=G[T]$ has four edges.
- Every low vertex $v\notin T$ has $c(v)=|N(v)\cap T|\le4$.

The proof covers the **entire stated layer**. Its raw necessary inventory
has 73 profiles. Human arguments exclude 57 profiles; the remaining 16
are covered by 3,721 incidence cases, all independently refuted.
The complete orbit audit covers 11,489,820 labeled quad families with
their degree roles retained.

Together with the [all-sink theorem](z12_A1_exclusion.md),
[uniform all-sink reduction](z12_A0_reduction.md), and
[complete five-edge exclusion](z12_A0_multi_quad_exclusion.md), this gives
the following campaign corollary. Every remaining twelve-high candidate has

$$
 e(G[V_8])=3,\qquad c(v)\le4\quad(v\notin V_8).
$$

Its necessary cover consists of **23 profiles and three high forests**:
$3P_2+6K_1$, $P_3+P_2+7K_1$, and $P_4+8K_1$. None is asserted realizable.
All cases with at most eleven high vertices remain open.
The numerical interval remains
$185\le\operatorname{ex}(54,\{C_3,C_4\})\le187$.

## Identities and the complete raw inventory

Put $C(v)=N(v)\cap T$, $F(v)=\{u:\operatorname{dist}(u,v)>2\}$,
$h_t=d_H(t)$, and $k=|\{t:h_t=2\}|$. Let

$$
 s_v=\sum_{u\sim v}(d(u)-6),\qquad
 \epsilon_v=
 \begin{cases}s_v-8&d(v)=6,\\s_v-7&d(v)=7.\end{cases}
$$

The [corrected all-sink identities](z12_distant_incidence_bound.md) give,
with $m=e(H)=4$,

$$
\begin{split}
 &s_t=5,\quad h_t\le2,\quad
 (|N(t)\cap V_6|,|N(t)\cap V_7|)=(3+h_t,5-2h_t),\\
 &\sum_{V_6}c=44,\qquad \sum_{V_7}c=44,\\
 &\sum\epsilon=4,\qquad \sum c\epsilon=8,\qquad
 \sum(c-3)\epsilon=-4,\\
 &\sum_{V_6}\frac{(c-3)(c-2)}2+
   \sum_{V_7}\frac{(c-1)(c-2)}2=4-k.                 \tag{1}
\end{split}
$$

For general $m$ the last right side is $8-m-k$. The summands are
nonnegative at integer $c$. A cycle in $H$ would have length at least
five and cost at least ten in $m+k$, so $H$ is a path forest.

A quad means a low vertex whose high set has size four. Enumerating
nonnegative integer multiplicities with the two vertex totals, the two
incidence totals, (1), and $c\le4$ gives:

| Quad type | Raw profiles | Treatment |
|---|---:|---|
| No quads | 33 | Charge and far partitions |
| Unique quad at degree six | 20 | Eight-point pair saturation |
| Unique quad at degree seven | 4 | Quad far capacity |
| At least two quads | 16 | Complete incidence refutations |

This is the **raw** four-edge inventory. It does not import the preceding
campaign's narrower 25-profile filter. The original
[a0_inventory.py](a0_inventory.py) census and a different
[charged-multiplicity enumeration](a0_independent.py) agree entry by entry
on all 403 original profiles, including this 73-profile slice.
The [finite verifier](verify_four_edge_layer.py) records every raw row
and its bucket.

The 16 multiple-quad rows are below. Indices are zero-based in the
original census; superscripts give multiplicities.

| Index | $k$ | High-count multiset on $V_6$ | On $V_7$ |
|---:|---:|---|---|
| 290 | 0 | $2^{5}\,3^{10}\,4$ | $1^{10}\,2^{15}\,4$ |
| 300 | 0 | $2^{6}\,3^{8}\,4^{2}$ | $1^{10}\,2^{14}\,3^{2}$ |
| 301 | 0 | $2^{6}\,3^{8}\,4^{2}$ | $0\,1^{7}\,2^{17}\,3$ |
| 302 | 0 | $2^{6}\,3^{8}\,4^{2}$ | $0^{2}\,1^{4}\,2^{20}$ |
| 311 | 0 | $2^{7}\,3^{6}\,4^{3}$ | $1^{9}\,2^{16}\,3$ |
| 312 | 0 | $2^{7}\,3^{6}\,4^{3}$ | $0\,1^{6}\,2^{19}$ |
| 313 | 0 | $1\,2^{4}\,3^{9}\,4^{2}$ | $1^{9}\,2^{16}\,3$ |
| 314 | 0 | $1\,2^{4}\,3^{9}\,4^{2}$ | $0\,1^{6}\,2^{19}$ |
| 320 | 0 | $2^{8}\,3^{4}\,4^{4}$ | $1^{8}\,2^{18}$ |
| 322 | 0 | $1\,2^{5}\,3^{7}\,4^{3}$ | $1^{8}\,2^{18}$ |
| 323 | 0 | $1^{2}\,2^{2}\,3^{10}\,4^{2}$ | $1^{8}\,2^{18}$ |
| 336 | 1 | $2^{6}\,3^{8}\,4^{2}$ | $1^{9}\,2^{16}\,3$ |
| 337 | 1 | $2^{6}\,3^{8}\,4^{2}$ | $0\,1^{6}\,2^{19}$ |
| 343 | 1 | $2^{7}\,3^{6}\,4^{3}$ | $1^{8}\,2^{18}$ |
| 344 | 1 | $1\,2^{4}\,3^{9}\,4^{2}$ | $1^{8}\,2^{18}$ |
| 354 | 2 | $2^{6}\,3^{8}\,4^{2}$ | $1^{8}\,2^{18}$ |

## Individual near and far partitions

Distinct vertices' high sets intersect in at most one point, and each
high set is independent in $H^2$. Every pair of high points has exactly
one short connection: an edge or a two-edge path through a high or low
vertex. The selected low high sets therefore partition all high pairs
not already joined within distance two in $H$.

For any low root $v$, its $d(v)-c(v)$ low neighbors have high sets
partitioning

$$
 R_v=T\setminus\left(C(v)\cup\bigcup_{t\in C(v)}N_H(t)\right).    \tag{2}
$$

A low edge $uv$ requires disjoint $C(u),C(v)$ and their union independent
in $H$. The union need not be independent in $H^2$; high-path leaves
in opposite endpoint sets can give an allowed five-cycle.

The far commutator identity and exact far cardinalities are

$$
 \sum_{u\in F(v)}[t\in C(u)]=(8-d(v))[t\notin C(v)],             \tag{3}
$$

$$
 |F(v)|=9-\epsilon_v\ (d(v)=6),\qquad
 |F(v)|=4-\epsilon_v\ (d(v)=7).                                \tag{4}
$$

Every far vertex is low because the highs are sinks. Thus a seven-root's
own high set and its far high sets partition $T$; a six-root's far high
sets double-cover its complement.

For a quad $q$, let $r_7(q)$ be the number of its low neighbors of degree
seven. Its exact data are:

| $d(q)$ | Low neighbors | $\epsilon_q$ | Far vertices | Far multiplicity |
|---:|---:|---:|---:|---:|
| 6 | 2 | $r_7(q)$ | $9-r_7(q)$ | 2 |
| 7 | 3 | $1+r_7(q)$ | $3-r_7(q)$ | 1 |

Both degree roles are retained in the generator.

## Negative charge and helper non-reuse

Call a seven-vertex bad when $(c,\epsilon)$ is $(1,1)$ or $(2,1)$,
with respective counts $b_1,b_2$. A $(2,2)$ vertex is impossible:
two far sets of size at most four cannot cover ten high points.

The degree bounds give $\epsilon\le c-2$ on $V_6$ and
$\epsilon\le c$ on $V_7$. Quad epsilon is as in the table.
The only negative terms of (1)'s charge sum are the bad vertices.
A six-root with $c=0$ contributes at least six, and one with $c=1$
at least two. Hence, writing $n_{dc}$ for high-count multiplicities,

$$
 W:=2b_1+b_2\ \ge\
 4+\sum_{\text{quads }q}\epsilon_q+6n_{60}+2n_{61}
 =4+n_{74}+\sum_q r_7(q)+6n_{60}+2n_{61}.                      \tag{5}
$$

All omitted charges are nonnegative. Every bad vertex has exactly three
far vertices, whose high sets give one of these complete alternatives:

- Own singleton: two quads and a triple, $4+4+3=11$.
- Own pair: one quad and two triples, $4+3+3=10$.
- Own pair: two quads and a pair, $4+4+2=10$.

Any unused quad must meet the bad vertex's own high set. Otherwise its
four points would have to fit in three far blocks, meeting each in at
most one point.

**Helper non-reuse.** A triple cannot help two different bad pairs whose
far partitions each use a single quad, even when the quads differ.

For a common quad $Q$ and shared helper $A$, the other helper triples
$D_1,D_2$ lie on five points outside $Q\cup A$. If equal, the two own
bad pairs are equal, violating linearity. Otherwise they intersect
exactly once; the first bad pair, complementary to $D_1$ on these five
points, is contained in $D_2$, also violating linearity.

For different quads $Q,R$ with shared helper $A$, $R$ is disjoint from $A$.
The first partition consists of its own pair, $Q,A$, and its other
helper. These cover at most $1+1+0+1=3$ points of $R$, a contradiction.
Thus single-quad covers use distinct actual helper triples globally.
No corresponding non-reuse rule is imposed on double-quad covers.

## Human exclusion of all zero-quad and one-quad profiles

With no quads, (5) requires a bad vertex, whereas every bad partition
requires a quad. This excludes all 33 zero-quad profiles.

If the unique quad is at degree seven, bad singletons are impossible.
Equation (5) gives $b_2\ge4+\epsilon_q\ge5$. Every bad pair is far from
the unique quad, but the quad has at most three far vertices. This
excludes all four such profiles.

Suppose instead the unique quad $Q$ is at degree six. Again $b_1=0$,
and (5) gives at least four bad pairs. We first show that the own high
pairs of any two such bad vertices are disjoint. In the partition of
the eight points outside $Q$ for the second bad vertex, each helper
triple of the first meets the second own pair and its two helper triples
in at most one point each. Its three points force equality in all three
intersections. The two disjoint first helpers therefore exhaust the
second own pair, making it disjoint from the first own pair.

Choose four bad pairs. They partition the eight points outside $Q$.
Their eight helper triples are distinct by non-reuse. All pair sets
inside these twelve blocks are disjoint by high-set linearity. They
contain $4+8\binom32=28$ pairs, exactly every pair on eight points.
In particular $H$ has no edge outside $Q$: such an edge would repeat
a short connection already supplied by one of these low blocks.

Since $Q$ is independent in $H$ and $H$ has four edges, all four edges
join $Q$ to its complement. Thus

$$
 \sigma(Q):=\sum_{t\in Q}h_t=4.
$$

The six-point quotas give $12+\sigma(Q)$ incidences with $Q$ at degree
six. The root $q$ itself contributes four of these; every other low
vertex meets $Q$ in at most one point. Exactly $8+\sigma(Q)$ other
six-vertices meet $Q$, leaving $15-(8+\sigma(Q))=7-\sigma(Q)=3$
outside $Q$. By (1), the six-quad costs one of the available $4-k$
units, so there are at most three degree-seven triples in the entire
graph. Therefore at most $3+3=6$ helper triples can lie outside $Q$.
The eight required helpers are impossible. This excludes all 20 profiles.

As a finite positive control of the saturation argument, normalize the
four disjoint own pairs on eight points. Each complementary helper pair
is a pair of transversals of the other three own pairs. The verifier
checks all $4^4=256$ choices: eight linear frames exist, and each covers
all 28 pairs. This controls the counting mechanism; no frame is claimed
to extend to a graph.

## A disjoint helper and neighbor bound

For any quad $q$ with high set $Q$ and $\sigma=\sum_{t\in Q}h_t$,
point quotas and linearity give the exact numbers of other low vertices
whose high sets are disjoint from $Q$:

$$
 D_6(Q)=4-\sigma+3[d(q)=6],\qquad
 D_7(Q)=6+2\sigma+3[d(q)=7].                                 \tag{6}
$$

Indeed the total six-incidences on $Q$ are $12+\sigma$, with four supplied
by $q$ if it has degree six. Subtract the resulting number of other
six-vertices meeting $Q$ from $16-[d(q)=6]$. The seven-incidences are
$20-2\sigma$, giving the second formula in the same way.

Let $a_q$ count the degree-six triple helpers used by chosen single-quad
bad covers at $Q$. They are distinct by non-reuse. Let $r_q$ count
degree-six low neighbors of $q$ whose high sets are not triples.
Both sets are outside $Q$, and they are disjoint by high-set size.
Consequently

$$
 a_q+r_q\le D_6(Q).                                          \tag{7}
$$

This distinguishes demands on actual individual quad incidences.
It is valid at either quad degree and is used for 17 residual cases.

## Complete colored-quad orbit cover

Label high points $0,\ldots,11$. The five possible four-edge forests,
with unused points isolated, are:

| Forest ID | Nontrivial path lengths in vertices | Edges |
|---:|---|---|
| 0 | $(2,2,2,2)$ | $01,23,45,67$ |
| 1 | $(3,2,2)$ | $01,12,34,56$ |
| 2 | $(4,2)$ | $01,12,23,45$ |
| 3 | $(3,3)$ | $01,12,34,45$ |
| 4 | $(5)$ | $01,12,23,34$ |

The last forest has only human-excluded profiles. The
[orbit generator](four_edge_orbits.py) enumerates linear families of
four-sets independent in $H^2$, with each quad marked by its degree.
For a family, color each high point by its quad-membership bit mask.
Record the color sequence of each path up to reversal, together with
its length, and sort components. Minimize over quad permutations
preserving degree roles. This is a complete invariant of colored path
forests: equality supplies a component isomorphism and exactly an
allowed high-forest automorphism. Extending representatives by every
admissible next quad preserves complete coverage.

The [independent orbit checker](verify_four_edge_orbits.py) reconstructs
high adjacency, enumerates admissible bit masks, and counts every labeled
linear family by a clique-count recursion. It then traverses each proposed
orbit using explicit path reversals and swaps of equal-length components.
It never uses the production canonical-key function. Distinct orbit
minima prove disjointness; the sum of traversed orbit sizes equals the
independent labeled count, proving completeness. For mixed degrees,
the labeled count keeps the two roles distinct.

| Forest ID | Six-quads | Seven-quads | Four-sets | Labeled families | Orbits |
|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | 321 | 59,424 | 58 |
| 0 | 2 | 0 | 321 | 29,712 | 37 |
| 0 | 3 | 0 | 321 | 937,992 | 264 |
| 0 | 4 | 0 | 321 | 9,729,792 | 1,411 |
| 1 | 2 | 0 | 295 | 24,390 | 100 |
| 1 | 3 | 0 | 295 | 667,140 | 810 |
| 2 | 2 | 0 | 282 | 21,615 | 80 |
| 3 | 2 | 0 | 270 | 19,755 | 48 |

These eight families contain 2,808 orbit representatives. Reusing the
applicable complete orbit list separately for each of the 16 profiles
gives 3,721 cases. Profile 354 uses both forest IDs 2 and 3. No other
forest/profile combination is omitted.

## Three necessary models and the graph-to-CNF direction

The [generator](four_edge_sat.py) has presence variables for candidate
low vertices $(d,B,j)$, where $B$ is an actual labeled high set. The quad
orbit fixes all size-four sets, retaining their degree roles. All other
allowed sets at required degrees are available. Sets of size at least
two cannot repeat by linearity; alternative degree slots compete for
their high pairs. Singleton multiplicity is allowed up to its high point's
degree-specific quota, and empty sets up to the full profile count.
Prefix order only normalizes indistinguishable same-degree copies.

Every stage includes the following conditions:

1. Exact degree/high-count multiplicities, exact degree-specific quotas
   at every high point, and exact high-pair coverage.
2. At each quad, a choice of its two or three distinct low neighbors
   satisfying (2). Adjacency between quads is symmetric.
3. Quad far indicators on selected vertices with disjoint high sets,
   symmetric between quads, disjoint from chosen neighbors, satisfying
   the exact cardinality and point multiplicity in (3)--(4).
4. Chosen bad vertices with complete three-block far partitions.
   Every used slot is selected. Quad far incidences agree in both
   directions, unused quads meet the own set, and single-quad helpers
   are not reused.
5. Inequality (5), counting each quad's actual seven-neighbors in its
   selected near tuple.

The **base** stage refutes 3,702 cases. The **packing** stage appends
(6)--(7) and refutes these 17 cases, denoted (profile, forest, orbit):

~~~text
(300, 0, 2)
(300, 0, 4)
(300, 0, 5)
(301, 0, 0)
(301, 0, 2)
(301, 0, 4)
(301, 0, 5)
(302, 0, 0)
(313, 0, 0)
(313, 0, 2)
(336, 1, 0)
(336, 1, 1)
(336, 1, 2)
(336, 1, 3)
(336, 1, 4)
(336, 1, 6)
(336, 1, 19)
~~~

The **near** stage is applied to (300,0,0) and (300,0,11). It appends
actual low-edge variables to the base stage; it does not require the
packing stage. Edges require both endpoints present. Every selected
vertex has exact low degree $d-c$ and satisfies (2) at each individual
high point. Edge variables at quads agree with their chosen near tuples.
Chosen bad vertices have the seven-neighbor count $8-2c$ required by
$\epsilon=1$. Every prescribed far pair has neither an edge nor a common
low neighbor. Common high neighbors were already excluded by disjoint
high sets. Both near formulas are refuted.

Not every low-only triangle/four-cycle condition is imposed. This is a
necessary relaxation, sufficient for exclusion. For completeness of the
encoding direction, take any hypothetical graph in the theorem's scope.
Its inventory gives one of the 73 raw profiles. The human arguments
exclude 57. For any remaining profile, label its high forest and quads
by the appropriate orbit representative, select its actual low slots,
near tuples, far indicators, and all bad vertices. Indistinguishable
copies can be prefix ordered. Equations (1)--(7) and helper non-reuse
hold in the graph, so the selection satisfies the prescribed stage.
The auxiliary cardinality variables can be extended to satisfy the
standard counter encoding. This contradicts the independently checked
unsatisfiability of that case. The full four-edge layer is excluded.

Two satisfiable partial incidence objects, one at base and one at packing
for case (300,0,11), are retained as [positive controls](four_edge_controls.json).
A direct combinatorial checker verifies their selected vertices, exact
near/far incidences, bad partitions, helper non-reuse, and charge; the
packing fixture also satisfies (6)--(7). They are not graph realizations.
Their existence verifies that the early relaxations are nonvacuous.

## Reproduction, compact evidence, and trust boundary

From this directory, use CPython 3.11.2 and python-sat 1.8.dev24:

~~~sh
python verify_four_edge_layer.py
python verify_four_edge_layer.py --finite-only
python -O verify_four_edge_layer.py --finite-only
python verify_four_edge_encoding.py
python reproduce_four_edge_layer.py \
  --work /absolute/path/outside-repository/four-edge \
  --checker /absolute/path/to/drat-trim
~~~

The complete finite verifier reconstructs the inventory and every orbit.
Normal and optimized finite-only outputs agree byte for byte.
There are 48 small direct-reference near-partition comparisons, totaling
222 partitions, including repeated empty slots and roots with three
low neighbors. Degree-seven quad far-cardinality rows are checked
separately. Two malformed fixtures are rejected.
The signed/repeated-literal and guarded-counter truth-table control
checks 4,608 assignments.

Use drat-trim revision
<code>2e3b2dc0ecf938addbd779d42877b6ed69d9a985</code>, built with
<code>gcc drat-trim.c -std=c99 -O2 -o drat-trim</code>.
The executable used here has SHA-256
<code>9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a</code>.
The solver is Glucose 4 through python-sat.

The driver defaults to all 3,721 cases and unlimited conflicts.
For one case, add <code>--case four_300_0_11</code>; this reports a partial
run honestly. The option <code>--replay /absolute/path/to/named-traces</code>
checks retained DRUP traces against freshly generated inputs.
SAT, UNKNOWN, failed checks, or a complete-run input-manifest mismatch
are failures; satisfiable partial selections are preserved outside Git.

Before running a solver on base or packing formulas, the driver tries
the separate [unit checker](a0_unit_check.py). A contradiction derived
from the input formula itself is an exact certificate and requires no
solver trace. This checker deduplicates literals, removes tautologies,
and propagates units by clause occurrence lists. It agrees with direct
truth tables on all 512 formulas over the nine non-tautological clauses
on two variables: 417 are unsatisfiable and 416 have unit refutations.
Duplicate-literal and tautology controls also pass.
The two large near formulas go directly to DRAT checking.
Every accepted DRAT check must return zero and print VERIFIED.
End-to-end driver controls pass for a unit case (312,0,206), a base
DRAT case (290,0,0), a packing case (300,0,5), and a near case (300,0,11).

All 3,721 formulas regenerated from the public generator are byte-identical
to their independently checked discovery inputs. There are **3,172 input
unit refutations and 549 checked DRAT refutations**, including 17 packing
and two near cases. No solver UNSAT answer alone is accepted.

The [compact evidence](four_edge_expected.json) records the raw inventory,
human partition, orbit counts and orbit-record digests, exact case/stage
cover, input-formula manifest, certificate-provenance manifest, controls,
versions, and measurements. Each input-manifest row is
(case, stage, variables, clauses, slots, edge variables, formula SHA-256),
in case-generator order. Group and whole digests hash JSON with sorted
keys and separators comma/colon. The reproduction driver compares the
complete regenerated input manifest exactly. Certificate rows are
(case, method, certificate SHA-256), using the formula hash for unit
refutations and trace hash for DRAT. Trace digests record this run's
provenance; freshly generated valid proofs may differ.

The whole input-manifest SHA-256 is
<code>16ea911b9d06bba10a03159523cbc7f2715b894ed2e6048228fec42d825c68f0</code>.
Selected-case discovery building/solving totaled 515.821 seconds,
public input rebuilding 440.044 seconds, and final parsing/unit/checking
441.596 seconds, with a maximum individual check of 15.794 seconds.
The orbit audit visits one orbit at a time and its original full run took
182.317 seconds. Formulas range from 8,695 to 611,148 variables and
17,105 to 1,365,808 clauses. Raw discovery traces total 431,389,983 bytes.
All raw formulas, traces, logs, exploratory SAT/UNKNOWN results, and
verbose per-case records remain outside Git and are regenerable.

The trust boundary is the human graph-to-model reduction, audited
inventory/orbit/candidate generators, Python, python-sat's cardinality
encoding, and the independent unit or DRAT checker. The positive controls
do not establish realization. No proof-assistant formalization, external
peer review, or historical priority claim is made.

The [primary extremal catalogue](https://users.cecs.anu.edu.au/~bdm/data/extremal.html)
and [2025 construction paper](https://arxiv.org/html/2508.05562v1)
were refreshed on 2026-09-11. The catalogue remains byte-identical to the
previously verified copy, listing lower bound 185 at order 54 and exact
value 181 at order 53. Its 53-vertex graph collection is incomplete and
is not used as an exhaustive extension base.
