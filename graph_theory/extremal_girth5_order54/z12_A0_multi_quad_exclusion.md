# The five-edge high-forest subclass is excluded

**Subsequent refinement.** The [complete four-edge exclusion](z12_A0_four_edge_exclusion.md)
now leaves only the three-edge layer: 23 necessary profiles and three high
forests at twelve high vertices. The theorem and its historical remainder
below are preserved.

**Conditional theorem.** There is no simple graph with 54 vertices, 187
edges, girth at least five, degree counts $(n_6,n_7,n_8)=(16,26,12)$,
and all of the following properties:

- Every vertex of $T=V_8$ is within distance two of every vertex.
- $H=G[T]$ has five edges.
- Every low vertex $v\notin T$ has $c(v)=|N(v)\cap T|\le4$.
- At least two low vertices have $c(v)=4$.

The proof covers the entire stated subclass. It uses individual high
sets, actual neighbors, and prescribed far pairs. It has 357 finite
cases, with independently checked contradictions.

Together with the [all-sink theorem](z12_A1_exclusion.md),
[uniform all-sink reduction](z12_A0_reduction.md), and
[one-quad exclusion](z12_A0_one_quad_exclusion.md), this excludes the
**entire $e(G[V_8])=5$ subclass when $|V_8|=12$**. Zero quads are impossible
by the charge argument below. Consequently every remaining twelve-high
candidate satisfies

$$
 e(G[V_8])\in\{3,4\},\qquad c(v)\le4\quad(v\notin V_8).
$$

The complete remaining cover has **48 profiles and eight high forests**:
23 profiles and three forests at $m=3$, and 25 profiles and five forests
at $m=4$. These are necessary covers, not realizations.
The cases $|V_8|\le11$ remain open. This does not change
$185\le\operatorname{ex}(54,\{C_3,C_4\})\le187$.

## Identities and the complete five-profile cover

Put $C(v)=N(v)\cap T$, $F(v)=\{u:\operatorname{dist}(u,v)>2\}$,
$h_t=d_H(t)$, and $k=|\{t:h_t=2\}|$. Write

$$
 s_v=\sum_{u\sim v}(d(u)-6),\qquad
 \epsilon_v=
 \begin{cases}s_v-8&d(v)=6,\\s_v-7&d(v)=7.\end{cases}
$$

The [corrected all-sink identities](z12_distant_incidence_bound.md) give

$$
\begin{split}
 &s_t=5,\quad h_t\le2,\quad
 (|N(t)\cap V_6|,|N(t)\cap V_7|)=(3+h_t,5-2h_t),\\
 &\sum_{V_6}c=46,\qquad\sum_{V_7}c=40,\\
 &\sum\epsilon=4,\qquad\sum c\epsilon=10,\qquad
 \sum(c-3)\epsilon=-2,\\
 &\sum_{V_6}\frac{(c-3)(c-2)}2+
   \sum_{V_7}\frac{(c-1)(c-2)}2=3-k.                 \tag{1}
\end{split}
$$

More generally the last right side is $8-m-k$. A cycle in $H$ would have
length at least five and cost at least ten in $m+k$; thus $H$ is a path
forest. Enumerating nonnegative integer high-count multiplicities using
the two vertex totals, the two incidence totals, and (1), with $c\le4$
and at least two quads, gives exactly these five rows. Superscripts are
multiplicities, and the indices are the zero-based original
[a0_inventory.py](a0_inventory.py) census.

| Index | $k$ | High-count multiset on $V_6$ | On $V_7$ |
|---:|---:|---|---|
| 372 | 0 | $2^4\,3^{10}\,4^2$ | $1^{13}\,2^{12}\,3^1$ |
| 373 | 0 | $2^4\,3^{10}\,4^2$ | $0^1\,1^{10}\,2^{15}$ |
| 377 | 0 | $2^5\,3^8\,4^3$ | $1^{12}\,2^{14}$ |
| 378 | 0 | $1^1\,2^2\,3^{11}\,4^2$ | $1^{12}\,2^{14}$ |
| 386 | 1 | $2^4\,3^{10}\,4^2$ | $1^{12}\,2^{14}$ |

This is the raw complete multiple-quad inventory, not a filter that imports
previous profile exclusions. Every quad is at degree six. The only high
forests are $5P_2+2K_1$ and $P_3+3P_2+3K_1$.
An independent charged-multiplicity enumeration agrees entry by entry
with the original full 403-profile census, including this five-row slice.

## Pointwise near and far constraints

Two distinct vertices' high sets intersect in at most one point.
Each $C(v)$ is independent in $H^2$. Every pair of high points has exactly
one short connection: an edge or a two-edge path, with its middle vertex
either high or low. Thus the selected low high sets partition the high
pairs not already connected within distance two in $H$.

For every low root $v$, the high sets of its low neighbors partition

$$
 R_v=T\setminus\left(C(v)\cup\bigcup_{t\in C(v)}N_H(t)\right).    \tag{2}
$$

There are $d(v)-c(v)$ such neighbors. An edge between low vertices $u,v$
requires $C(u)\cap C(v)=\varnothing$ and $C(u)\cup C(v)$ independent
in $H$. The union need not be independent in $H^2$: the two leaves of
a high $P_3$ may occur in different endpoint sets.

The far commutator identity is

$$
 \sum_{u\in F(v)}[t\in C(u)]=(8-d(v))[t\notin C(v)].             \tag{3}
$$

Consequently a seven-vertex's own high set and its far sets partition $T$.
A six-vertex's far high sets double-cover its complement. Also

$$
 |F(v)|=9-\epsilon_v\quad(d(v)=6),\qquad
 |F(v)|=4-\epsilon_v\quad(d(v)=7).                              \tag{4}
$$

For a six-quad $q$, $\epsilon_q$ is exactly its number of seven-neighbors.
It has two low neighbors. Equations (2)--(4) therefore specify its two
near vertices, its exact far cardinality, and a pointwise far double cover.

## All negative-charge covers

Call a seven-vertex bad if $(c,\epsilon)$ is $(1,1)$ or $(2,1)$; their
counts are $b_1,b_2$. The possible $(2,2)$ type is impossible here: it
would have two far sets covering ten points, although both have size
at most four.

The degree bounds give $\epsilon\le c-2$ on $V_6$ and
$\epsilon\le c$ on $V_7$, and $\epsilon_q\ge0$ at every six-quad.
The only negative terms in the charge identity in (1) are therefore
the bad vertices. With $n_{61}=|V_6\cap\{c=1\}|$,

$$
 W:=2b_1+b_2\ \ge\ 2+\sum_{\text{quads }q}\epsilon_q+2n_{61}.   \tag{5}
$$

All other possible terms discarded from the right side are nonnegative.
In particular a bad vertex exists, and its cover must contain a quad.
The same sign argument when there are no quads gives $W\ge2$, so also
excludes that subclass.

Each bad vertex has exactly three far vertices. Its complete possibilities,
as disjoint partitions of the complement of its own high set, are:

- A bad singleton uses two quads and a triple: $4+4+3=11$.
- A bad pair uses one quad and two triples: $4+3+3=10$.
- A bad pair uses two quads and a pair: $4+4+2=10$.

An unused quad must meet the bad vertex's own high set. Otherwise its
four points would have to lie in three distinct far blocks, meeting
each in at most one point.

**Helper non-reuse.** A triple cannot be a helper of two different bad
pairs whose covers each use exactly one quad, even if their quads differ.

For the same quad $Q$ and shared triple $A$, the two other helper triples
$D_1,D_2$ lie on the five points outside $Q\cup A$. If they are identical,
the two bad pairs coincide, contradicting linearity. Otherwise the
triples intersect exactly once, so the first bad pair, complementary to
$D_1$ on those five points, is contained in $D_2$. This also contradicts
linearity.

For different quads $Q,R$ and shared helper $A$, $R$ is disjoint from $A$.
The first bad partition consists of its own pair, $Q,A$, and its other
helper. These cover at most $1+1+0+1=3$ points of $R$, a contradiction.

Thus each single-quad bad cover consumes two distinct actual helper
triples globally. No such non-reuse rule is imposed on double-quad covers.

## Complete quad normalization

Label the high points $0,\ldots,11$. For $k=0$, take high edges
$01,23,45,67,89$. For $k=1$, take $01,02,34,56,78$.

The [orbit generator](a0_quad_orbits.py) first lists every four-set
independent in $H^2$, then every linear family of two or three such sets
up to automorphisms of $H$ and permutation of the quads.

Its canonical key colors a high point by the set of quads containing it.
For each matching edge it records the unordered pair of endpoint colors;
for the $P_3$ it records the center color and unordered leaf colors;
for isolated vertices it records their color multiset. It sorts matching
components and minimizes over permutations of quad labels.
This is a complete invariant: an isomorphism of these colored path
components is exactly a high-forest automorphism preserving the quad
family. Extending one representative of every smaller family by every
admissible four-set therefore preserves complete coverage.

A different [checker](verify_a0_quad_orbits.py) enumerates every labeled
family using bit masks, then traverses its orbit using explicit forest
automorphism generators. It does not use the canonical-key function.
It verifies entry-level disjointness and coverage of the entire labeled
family set:

| $k$ | Quads | Admissible four-sets | Labeled families | Orbits |
|---:|---:|---:|---:|---:|
| 0 | 2 | 280 | 22,680 | 24 |
| 0 | 3 | 280 | 625,440 | 161 |
| 1 | 2 | 255 | 18,252 | 124 |

The same 24 two-quad patterns are used separately for profiles 372, 373,
and 378. Hence the complete proof has $3(24)+161+124=357$ cases.
Triple intersections and disjoint quads are both included.

## The two necessary incidence models

The [CNF generator](a0_multi_quad_sat.py) uses Boolean presence variables
for candidate low vertices $(d,B,j)$, where $B$ is an actual labeled
high set. Every quad is fixed by its orbit representative. Every other
allowed high set of the required size is available at either required
degree. A set of size at least two cannot repeat, by linearity; its
alternative degree slots compete for its high pairs. Singleton slots
allow multiplicity up to the corresponding high point quota. Empty sets
allow the full profile multiplicity. A prefix order is imposed only on
indistinguishable copies of the same degree and high set.

Both model stages impose:

1. Exact profile multiplicities and six/seven incidence quotas at each
   high point, with exact high-pair coverage.
2. At each quad, a choice of two distinct selected low neighbors whose
   sets partition (2), with symmetric adjacency between quads.
3. Far indicators at every quad, supported on selected vertices with
   disjoint high sets, symmetric between quads and disjoint from the
   chosen near vertices. They satisfy the exact cardinality (4) and
   pointwise double cover (3).
4. Chosen bad vertices with one of the complete three-block partitions
   above. Every helper is selected. Far incidences to quads are consistent
   in both directions, and single-quad helpers obey non-reuse.
5. The necessary charge inequality (5), counting each quad's actual number
   of seven-neighbors from its chosen near pair.

The **base** stage refutes 343 cases. Some base formulas are satisfiable;
three such partial incidence objects are retained as
[positive controls](a0_multi_quad_controls.json). They are not graphs.

The **near** stage strengthens the remaining 14 cases. It introduces
actual low-edge variables between compatible candidate slots, conditional
on both endpoints being present. Each selected vertex has exact low
degree $d-c$ and satisfies the pointwise near partition (2).
Its edge variables at quads agree with the already selected near pairs.
Every chosen bad vertex has the seven-neighbor count required by
$\epsilon=1$. Finally, every prescribed far pair has neither an edge
nor a common low neighbor. Common high neighbors are already excluded
by disjoint high sets.

The stronger stage does not impose all low-only triangle and four-cycle
conditions. It remains a necessary relaxation, which is sufficient for
an exclusion theorem. To see the required encoding direction, embed any
hypothetical graph into its quad orbit, select its actual low slots,
neighbors, far sets, and all bad vertices. Every listed condition holds.
The resulting assignment satisfies the CNF. Since every CNF is
contradictory, no hypothetical graph exists.

The stronger cases, with zero-based orbit numbers, are

$$
\begin{split}
 &(372,j),\quad j\in\{2,7,9,10,12,13,18,22,23\},\\
 &(373,7),(373,9),(386,32),(386,39),(386,59).
\end{split}
$$

All other cases use the base model. Each formula stage is recorded
explicitly; a partial model is never interpreted as a realization.

## Evidence and reproduction

Run from this directory, using CPython 3.11.2 and python-sat 1.8.dev24:

~~~sh
python verify_a0_multi_quad.py
python -O verify_a0_multi_quad.py
python verify_a0_multi_quad_encoding.py
python reproduce_a0_multi_quad.py \
  --work /absolute/path/outside-repository/multi-quad \
  --checker /absolute/path/to/drat-trim
~~~

The driver defaults to the complete cover and an unlimited conflict
budget. The option <code>--case multiquad_372_7</code> runs one specified case.
The option <code>--replay /absolute/path/to/named-traces</code> checks existing
traces against freshly generated formulas. SAT, UNKNOWN, missing cases,
mismatched expected formula hashes, and failed certificate checks are failures.

Use drat-trim revision
<code>2e3b2dc0ecf938addbd779d42877b6ed69d9a985</code>, built with
<code>gcc drat-trim.c -std=c99 -O2 -o drat-trim</code>.
The executable used here has SHA-256
<code>9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a</code>.
The solver is Glucose 4 through python-sat.

The pinned checker returns exit code 1 on a parse-time unit contradiction,
while printing <code>c trivial UNSAT</code> and <code>s VERIFIED</code>: its
final status variable is not assigned in that branch. The driver accepts
this case only after the separate standard-library
[unit checker](a0_unit_check.py) also derives a contradiction from the
input formula. It never accepts other exit-code-1 outcomes.
The unit checker deduplicates literals, drops tautologies, and propagates
units by clause occurrence lists. All 512 formulas formed from the nine
non-tautological clauses on two variables were checked against truth
tables: 417 are unsatisfiable and 416 have unit refutations. Duplicate
literal and tautology controls are included.

The [finite verifier](verify_a0_multi_quad.py) checks the independent
inventory and orbit cover, directly verifies the three positive partial
incidence objects, rejects malformed controls, and records the complete
48-profile campaign remainder. Normal and optimized Python executions
agree byte for byte. A separate SAT truth-table control checks signed
repeated literals and conditional cardinality constraints.

[a0_multi_quad_expected.json](a0_multi_quad_expected.json) records every
formula and trace hash, the selected stage, all certificate outcomes,
resource measurements, and finite controls. All published-source formulas
were regenerated and matched byte for byte to their discovery formulas,
then independently checked. Raw formulas, proof traces, and logs remain
outside Git and can be regenerated by the driver.

Of the 357 final checks, 168 validate a DRAT refutation and 189 additionally
receive an independent input-formula unit refutation after drat-trim's
parse-time UNSAT result. The measured selected-case discovery build and
solve time totals 370.810 seconds. Public formula regeneration totals
76.279 seconds and final certificate checking 134.801 seconds, with a
maximum individual check of 22.533 seconds. Peak self and child resource
reports are 372,688 KiB. The 2,304 signed-counter and guard truth-table
assignments all agree with direct evaluation. The raw traces total
129,861,993 bytes and are omitted from Git.

The trust boundary is the mathematical graph-to-model reduction, the
audited generators and orbit classification, Python and python-sat's
counter construction, and the DRAT checker or independent unit checker.
Solver UNSAT output alone is not used as proof. No external peer review,
proof-assistant formalization, or independent realization is claimed.

The [primary extremal catalogue](https://users.cecs.anu.edu.au/~bdm/data/extremal.html)
and [2025 construction paper](https://arxiv.org/html/2508.05562v1)
were refreshed on 2026-09-11. The catalogue still lists 185 as a lower
bound at order 54 and 181 as the exact value at order 53. The 53-vertex
graph collection is explicitly incomplete and is not used as an exhaustive
extension base. The numerical interval remains unchanged; no priority
claim is made.
