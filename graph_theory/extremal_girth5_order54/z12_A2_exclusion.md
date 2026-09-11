# Two high distant incidences are impossible at order 54

**Theorem.** Let $G$ be a finite simple graph with 54 vertices, 187 edges,
girth at least five, and twelve degree-eight vertices. Write
$T=V_8$, $F(v)=\{u:\operatorname{dist}(u,v)>2\}$, and
$A=\sum_{t\in T}|F(t)|$. Then

$$
 A\le1.
$$

In particular, **at least eleven of the twelve high vertices are sinks**,
meaning that every vertex is within distance two of each of them.

The preceding [five-matching exclusion](z12_A2_matching_exclusion.md)
reduced $A=2$ to one four-edge matching profile with two overlapping
four-element high neighborhoods. The argument below closes that **entire
remaining subclass**, for every choice of their common high point and all
other vertex incidences. Together with the earlier
[$A\le2$ theorem](z12_A3_exclusion.md), it proves the statement.

This is a human closing proof importing the preceding exact
[A2 classification](z12_A2_reduction.md) and incidence identities.
The finite enumerations below check its elementary colored-edge packing
and its full local cover. No new solver certificate is used.
The numerical interval remains
$185\le\operatorname{ex}(54,\{C_3,C_4\})\le187$.
The cases $A=0,1$ at $z=12$ and the cases $z\le11$ remain open.

## The residual incidence structure

Suppose $A=2$. The preceding classification and matching exclusion give

$$
\begin{split}
 &(n_6,n_7,n_8)=(16,26,12),\qquad G[T]=4P_2+4K_1,\\
 &V_6:\quad c=2^4\,3^{10}\,4^2,\qquad
 V_7:\quad c=1^{10}\,2^{16},
\end{split}                                                    \tag{1}
$$

where $C(v)=N(v)\cap T$, $c(v)=|C(v)|$, and the exponents indicate
multiplicities. There are exactly two nonsinks $r_1,r_2$ and two
degree-seven vertices $x_1,x_2$ such that
$F(r_1)=\{x_2\}$, $F(r_2)=\{x_1\}$, and $C(x_i)=\{r_i\}$.
Each $x_i$ has neighbor-degree counts $(1,5,1)$.

Let $q_1,q_2$ be the two six-vertices with $c=4$ and write

$$
 Q_1=C(q_1)=\{p\}\cup B_1,\qquad
 Q_2=C(q_2)=\{p\}\cup B_2,\qquad
 O=T\setminus(Q_1\cup Q_2).                                   \tag{2}
$$

Here $|B_1|=|B_2|=3$, $|O|=5$, and all displayed parts are disjoint.
No role is assigned to $p$ in the high matching or in the set of nonsinks.

Distinct low vertices' high sets intersect in at most one point, by the
absence of four-cycles. Far vertices have disjoint high sets.
In particular, no high two-set or triple can occur at two distinct low
vertices.

Put $s_v=\sum_{u\sim v}(d(u)-6)$ and let
$\epsilon_v=s_v-8$ on $V_6$, $\epsilon_v=s_v-7$ on $V_7$.
The corrected identities specialize to

$$
 \sum_{V_6\cup V_7}\epsilon_v=6,\qquad
 \sum_{V_6\cup V_7}c(v)\epsilon_v=8,\qquad
 \sum_{V_6\cup V_7}(c(v)-3)\epsilon_v=-10.                      \tag{3}
$$

For a seven-vertex, $|F(v)|=4-\epsilon_v$. Its exact individual cover is

$$
 [t\in C(v)]+\sum_{u\in F(v)}[t\in C(u)]
   =1+|F(t)\cap N(v)|,\qquad t\in T.                           \tag{4}
$$

Thus its own high set and its far vertices' high sets cover $T$.
The two nonsinks may cause additional multiplicity; we retain that
correction throughout.

## At least ten bad vertices and a complete three-way split

On $V_6$, the local range $2c-8\le\epsilon\le c-2$ makes
$(c-3)\epsilon$ nonnegative for every $c=2,3,4$ in (1).
The only negative seven-types are
$(c,\epsilon)=(1,1),(2,1),(2,2)$.

A $(1,1)$ vertex has three far vertices whose high sets must total at
least eleven points by (4). It cannot be an $x_i$, since
$\epsilon_{x_i}=0$. Its far vertices therefore all have low degree.
The only possible far-size multiset is $4,4,3$; but the two four-sets
overlap, so those far sets together with its own singleton cover at most
eleven distinct points. This is impossible.

A $(2,2)$ vertex has two far vertices and needs their high-set sizes
to total at least ten, while even $4+4=8$. It is also impossible.

Call a seven-vertex **bad** when $(c,\epsilon)=(2,1)$, and denote the
set of such vertices by $\mathcal B$. Each contributes $-1$ to (3);
all other contributions are nonnegative. Hence

$$
 |\mathcal B|\ge10.                                           \tag{5}
$$

A bad vertex $y$ has three far vertices, none high. Their high-set
sizes total at least ten, so at least one is $q_1$ or $q_2$.
Partition $\mathcal B$ into $\mathcal B_1,\mathcal B_2,\mathcal B_{12}$,
according as $F(y)$ contains only $q_1$, only $q_2$, or both.
These categories are exhaustive and mutually exclusive.

If $y\in\mathcal B_i$, its far sizes are necessarily $4,3,3$.
Their sum with $c(y)=2$ is exactly twelve, so (4) is a true partition:

$$
 T=C(y)\ \dot\cup\ Q_i\ \dot\cup\ C(u_y)\ \dot\cup\ C(v_y).
                                                                    \tag{6}
$$

The helpers $u_y,v_y$ are six-vertices with $c=3$.
For $j\ne i$, the three points of $B_j=Q_j\setminus Q_i$ are spread
among $C(y),C(u_y),C(v_y)$. Each block meets $Q_j$ in at most one point,
so each contains exactly one point of $B_j$.
Consequently each helper triple is of the form

$$
 \{b\}\cup e,\qquad b\in B_j,\quad e\in\binom O2.               \tag{7}
$$

This is the full single-four-set case, with no symmetry restriction.

If $y\in\mathcal B_{12}$, its third far set cannot have size at most
two: its own two-set, $Q_1\cup Q_2$, and that set would cover at most
$2+7+2=11$ points. Thus it is a triple $D_y$, with

$$
 D_y\subseteq O,\qquad C(y)=O\setminus D_y.                    \tag{8}
$$

Indeed the sizes in (4) total thirteen, and the common point $p$ of the
quads already accounts for one repeated point. There can be no further
overlap. Equation (4) then additionally forces $p$ to be a nonsink and
$y$ adjacent to its missed endpoint. We do not need this further
restriction for the upper bound below; allowing every role of $p$
only enlarges the counted possibilities.

## A colored-edge packing lemma on five points

**Lemma.** A simple graph on five vertices with a proper edge coloring
using at most three colors has at most three unordered pairs of edges
that are disjoint and have different colors.

Let $r$ be its number of edges, $d_1,\ldots,d_5$ its vertex degrees,
and $a_1,a_2,a_3$ the sizes of its color classes, including empty classes.
Every color class is a matching of size at most two, so $r\le6$.
The desired number is exactly

$$
 P=\binom r2-\sum_{\nu=1}^5\binom{d_\nu}{2}
             -\sum_{\gamma=1}^3\binom{a_\gamma}{2}.           \tag{9}
$$

The first subtraction removes incident edge pairs; the second removes
same-color pairs, which are disjoint because the coloring is proper.
There is no overlap between these two subtractions.

For integer entries of fixed sum, the sum of $\binom x2$ is minimized
by entries differing by at most one: moving one unit from $x$ to $y$
when $x\ge y+2$ lowers the sum by $x-y-1$.
Using $\sum d_\nu=2r$ and $\sum a_\gamma=r$ gives:

| $r$ | Lower bound for vertex sum | Lower bound for color sum | Upper bound for $P$ |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 2 | 0 | 0 | 1 |
| 3 | 1 | 0 | 2 |
| 4 | 3 | 1 | 2 |
| 5 | 5 | 2 | 3 |
| 6 | 9 | 3 | 3 |

This proves the lemma. The bound three is attained in this abstract
colored-graph problem; it does not assert an order-54 graph realization.

## At most eight bad vertices

Fix $i$ and collect all actual helper triples of the form (7).
Represent $\{b\}\cup e$ by edge $e$ on the five points $O$, colored by $b$.

This is a **simple** graph: distinct triples with the same edge $e$
would share its two high points, which is impossible.
Its coloring is **proper**: two triples of the same color sharing
an endpoint of $e$ would share that high point and their color point.

For $y\in\mathcal B_i$, the two helper triples in (6) are disjoint,
so their edges are disjoint and their colors different.
The assignment from $y$ to this unordered edge pair is injective:
the pair of triples and $Q_i$ determine the complementary two-set $C(y)$,
which cannot be shared by two distinct low vertices.
The colored-edge lemma therefore gives

$$
 |\mathcal B_1|\le3,\qquad |\mathcal B_2|\le3.                  \tag{10}
$$

For $\mathcal B_{12}$, equation (8) assigns each vertex a distinct
triple in the five-point set $O$. These triples intersect pairwise in
at most one point. There are at most two such triples: three would
have union of size at least $3\cdot3-3=6$, exceeding five.
Thus

$$
 |\mathcal B_{12}|\le2,\qquad
 |\mathcal B|\le3+3+2=8<10.                                   \tag{11}
$$

This contradicts (5) and closes every remaining $A=2$ incidence
configuration. Since $A\le2$ was already established, $A\le1$ follows.

## The next single-incidence target

If $A=1$, there is a unique nonsink $r\in T$ with $F(r)=\{x\}$,
where $x$ has degree six or seven and **no high neighbors**.
A high-high distant pair would contribute two to $A$, so $x\notin T$.
For every other high vertex $t$, the high/high commutator gives

$$
 0=(\mathcal A\mathcal F-\mathcal F\mathcal A)_{tr}
   =|N(t)\cap F(r)|,
$$

because $F(t)$ is empty and $d(t)=d(r)=8$.
Hence $t$ is not adjacent to $x$; neither is $r$, since they are far.
This proves $C(x)=\varnothing$.

The next exact target is the entire $A=1$ subclass, covering both possible
degrees of $x$ and every high induced graph. Neither that subclass nor
$A=0$ is excluded here.

## Reproducible finite controls and trust boundary

[verify_a2_exclusion.py](verify_a2_exclusion.py) uses CPython 3.11 or later,
standard library only. It compares two complete enumerations, entry for
entry, of all **8,326 properly three-edge-colored simple graphs on five
labeled vertices**, with three named colors and absent edges allowed.

One method selects three ordered matchings from the 26 matchings on five
points; the other checks all $4^{10}$ edge-color words directly.
Counts by edge number $0,\ldots,6$ are
$1,30,315,1440,2970,2700,870$. The computed maxima in (9) are
$0,0,1,2,2,3,3$. For each colored graph the checker also reconstructs the
actual high triples and compares disjoint-pair counts with their partitions.

Further controls enumerate all 125 possible helper triples relative to
the two overlapping quads, all 90 single-quad templates for each quad,
and all ten double-quad templates. They verify the vanished correction
in (6) and its unique extra incidence at $p$ in (8).
All 1,024 families of triples on five points are checked; 26 are linear
and their maximum size is two. The integer convexity table, local negative
types, and every possible far-size multiset are also checked.

From this directory:

~~~sh
python3 verify_a2_exclusion.py > /tmp/order54-a2-exclusion.json
cmp /tmp/order54-a2-exclusion.json a2_exclusion_expected.json
python3 -O verify_a2_exclusion.py > /tmp/order54-a2-exclusion-O.json
cmp /tmp/order54-a2-exclusion-O.json a2_exclusion_expected.json
~~~

The [compact expected record](a2_exclusion_expected.json) preserves the
full colored-graph histogram and stream hash, table, and cover checks.
There is no symmetry quotient, floating arithmetic, solver status, or
assumed graph realization in these controls.

These are internal independent algorithmic checks, not external peer review
or formal verification of the human proof. The graph-to-cover bridge and
the arguments above remain written mathematics. The dependency chain
imports the A2 classification's 36 exact rational certificates, the earlier
A3 exclusion, the corrected degree identities, and the published order-53
bound; their own reproducibility and trust boundaries remain in the linked
proofs. No historical priority claim is made.

Normal and optimized runs passed with byte-identical output, SHA-256
c02dad937277481f13afb3fbb1568be566a1ac2720be34d60788aca1f82bbb6e.
On CPython 3.11.2 they took 2.88 and 2.98 seconds, with peak resident
memory 19,116 KiB.
