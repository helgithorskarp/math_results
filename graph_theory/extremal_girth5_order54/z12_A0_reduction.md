# A uniform incidence reduction for twelve high sinks

**Theorem.** Let $G$ be a simple graph on 54 vertices with 187 edges,
girth at least five, and twelve degree-eight vertices. Write
$T=V_8$, $C(v)=N(v)\cap T$, $c(v)=|C(v)|$, and $H=G[T]$.
Then

$$
 3\le e(H)\le5,\qquad c(v)\le4\quad(v\notin T).
$$

Every high vertex is a radius-two sink by the
[preceding theorem](z12_A1_exclusion.md). The new proof covers the
**entire all-sink subclass**: it excludes every large high-neighborhood,
all high forests with at most two edges, and every six-edge high forest.
Exactly twelve possible high forests and 63 necessary low high-count
profiles remain. These are complete covers, not assertions of realizability.

This does **not** exclude the whole twelve-high subclass or improve
$185\le\operatorname{ex}(54,\{C_3,C_4\})\le187$.
The cases $z\le11$ remain open as well.
The decisive six-edge contradiction uses individual vertices: a seven-vertex
would need five distinct neighbors from a class of four.

There are eleven new exact rational certificates, applied only to a complete
cover of the six-edge profiles. Their models include the realizability
condition that a degree-six vertex's far high-counts must be the degrees
of a simple graph. Floating feasibility or infeasibility is never proof.

## Exact all-sink identities and the complete inventory

Let $F(v)=\{u:\operatorname{dist}(u,v)>2\}$,
$m=e(H)$, and $k=|\{t:d_H(t)=2\}|$. Degree counts are $(16,26,12)$.
Put $s_v=\sum_{u\sim v}(d(u)-6)$ and
$\epsilon_v=s_v-8$ on $V_6$, $\epsilon_v=s_v-7$ on $V_7$.
The [corrected identities](z12_distant_incidence_bound.md), now with $A=0$,
give

$$
\begin{split}
 &s_t=5,\quad d_H(t)\le2,\quad
 (|N(t)\cap V_6|,|N(t)\cap V_7|)=(3+d_H(t),5-2d_H(t)),\\
 &\sum_{V_6}c=36+2m,\quad \sum_{V_7}c=60-4m,\\
 &\sum\epsilon=4,\quad \sum c\epsilon=2m,\quad
 \sum(c-3)\epsilon=2m-12,\\
 &\sum_{V_6}\frac{(c-3)(c-2)}2+
   \sum_{V_7}\frac{(c-1)(c-2)}2=8-m-k,\\
 &Q+2U=28,\quad
 Q=\sum_{V_6}\epsilon^2+\sum_{V_7}\epsilon(\epsilon-1).
\end{split}                                                       \tag{1}
$$

Here $U$ is the sum of $(d(u)-6)(d(v)-6)$ over unordered far pairs.
All far pairs are low-low; hence $U$ is precisely the number of far
seven-seven pairs.

The nonnegative inventory in (1) gives $m+k\le8$.
A cycle in $H$ would have length at least five and cost at least ten in
$m+k$. Thus $H$ is a path forest. If $m=0$, then $k=0$; otherwise
$0\le k\le m-1$.

For each such $m,k$, impose the two vertex totals, the two $c$-totals, and
the inventory in (1). Enumerate all nonnegative integer multiplicities
$n_{dc}$. This gives **403 profiles**. In fact none has $m>6$.
The first implementation recursively assigns every $c=0,\ldots,d$,
tracking the three totals separately.
An independent implementation enumerates charged multiplicities of types

$$
 (6,0),(6,1),(6,4),(6,5),(6,6),(7,0),(7,3),(7,4),(7,5)
$$

with costs $3,1,1,3,6,1,1,3,6$, then solves for the four zero-cost
multiplicities $n_{62},n_{63},n_{71},n_{72}$.
No larger possible $c$ has cost below ten.
The two complete censuses agree entry for entry.

Profile indices below are zero-based entries of the deterministic
[a0_inventory.py](a0_inventory.py) generator. The checker reconstructs
all of them, including every rejected row; indices never stand in for
an unprovided external dataset.

## Individual partitions and double covers

Distinct vertices' high sets intersect in at most one point.
Far vertices have disjoint high sets.
For every low vertex $v$ and $t\in T$, the commutator identity becomes

$$
 (8-d(v))[t\in C(v)]+\sum_{u\in F(v)}[t\in C(u)]=8-d(v).          \tag{2}
$$

Thus a seven-vertex's own high set and its far high sets **partition $T$**.
A six-vertex's far high sets avoid its own set and cover its complement
**exactly twice**. Also

$$
 |F(v)|=9-\epsilon_v\ (d(v)=6),\qquad
 |F(v)|=4-\epsilon_v\ (d(v)=7).                                \tag{3}
$$

The local epsilon ranges are $2c-8\le\epsilon\le c-2$ on $V_6$ and
$2c-7\le\epsilon\le c$ on $V_7$.
The only negative contributions to $(c-3)\epsilon$ are seven-types
$(c,\epsilon)=(1,1),(2,1),(2,2)$, with counts $b_1,b_2,b_{22}$.
Set $W=2b_1+b_2+2b_{22}$. From (1),

$$
 W\ge12-2m+L_+,\quad
 L_+=\sum_{c<2}n_{6c}(c-3)(c-2)
 +\sum_{c\ge4}n_{6c}(c-3)(2c-8)
 +\sum_{c\ge4}n_{7c}(c-3)(2c-7).                              \tag{4}
$$

There is only one inventory whose largest two low high-counts sum to ten
or more: profile 89 has $m=2,k=0$,
six-counts $2^{12}3^2 5^2$, and seven-counts $2^{26}$.
Each negative vertex must be far from each five-vertex: otherwise its
cover meets that five-set in at most one point per covering block.
Each five-vertex has at most seven far vertices. Consequently
$b_2+b_{22}\le7$ and $W\le14$, below the required sixteen.
This excludes that profile and proves **$b_{22}=0$ everywhere**.

Write $P=\sum\max(\epsilon,0)$ and $N=\sum\max(-\epsilon,0)$.
Then $N\le Q$, $P=4+N\le32$, and $W\le P+b_1$.
If a set of size at least five occurs, every negative vertex must be far
from its vertex. Its far capacity is at most
$f=17-2c$ on $V_6$ or $f=11-2c$ on $V_7$; hence
$W\le\min(2f,f+n_{71})$.

If all sets have size at most four, call size-four sets **quads**.
Every $b_1$ vertex requires two quads and every $b_2$ vertex at least one,
so $W\le9n_{64}+3n_{74}$. With fewer than two quads, $b_1=0$.
Three further bounds, rederived for the exact covers (2), are useful:

- One quad gives $W\le4$. Each bad two-set injects into a disjoint pair of
  actual triples on the eight outside points. Every linear triple family
  there has at most four disjoint pairs, by the
  [all-size bound](z12_A1_exclusion.md#one--and-two-quad-bounds).
- Two quads give $W\le6$. If $b_1>0$, the quads, a fixed triple, and a
  fixed singleton partition $T$; the double cover bounds $b_1\le2$,
  and the complementary-triple argument forbids $b_2$. Otherwise,
  disjoint quads force every bad two-set into their four-point complement,
  where a quad's double cover permits at most four. Intersecting quads
  give two single-quad categories, each of size at most three by the
  [colored-edge lemma](z12_A2_exclusion.md#a-colored-edge-packing-lemma-on-five-points).
  The both-quad category is impossible because the far sets must be disjoint.
- Three quads give $W\le9$. In their intersection graph, a singleton cover
  forces a path and uses its leaves. A single-quad bad cover requires a
  vertex of degree two; each such category has size at most three.
  A double-quad bad cover requires the two disjoint leaves of a path
  and admits at most four bad two-sets. If singleton covers occur,
  that double-leaf category is forbidden, and $b_1\le2$.
  Thus a path gives $W\le7$, a triangle gives $W\le9$, and zero or one
  intersection edge gives $W=0$. These are the exact-cover specializations
  of the complete incidence analysis in the preceding proof.

For each profile combine these upper bounds, $W\le32+b^*$,
$W\le2b^*+n_{72}$, and (4), with $b^*=n_{71}$ except when fewer
than two quads force $b_1=0$.
They reject **303 profiles**, retaining 100 including profile 89,
which was deliberately reserved for the preceding $b_{22}$ argument.
The following sections close the complete large-set and small-$m$ residues.

## Every high-neighborhood of size at least five is impossible

Among the 100 rows, exactly fifteen have a set of size at least five.
Apart from profile 89, each has a unique six-vertex $q$ with
$Q=C(q)$ of size five, $\epsilon_q\ge2$, and $f=|F(q)|\le7$.
All negative vertices belong to $F(q)$.

First suppose there is no quad.
Every other high set has size at most three, while the double cover
outside $Q$ needs fourteen incidences. Hence

$$
 14\le b_1+2b_2+3(f-b_1-b_2)=3f-W,\qquad W\le7.                \tag{5}
$$

This excludes every such row except profile 376:

$$
 m=5,\ k=0,\qquad V_6:2^4 3^{11}5^1,\quad V_7:1^{12}2^{14}.    \tag{6}
$$

Here $H$ is a five-edge matching plus two isolates.
The five points of $Q$ have at least eighteen six-incidences, because at
least three are matched. Removing $q$'s five incidences leaves at least
thirteen **distinct** other six-vertices meeting $Q$.
Thus at most two of the fifteen other six-vertices have high triples
entirely outside $Q$. There are no seven-triples.

Every $b_1$ uses $q$ and two disjoint such triples.
Every $b_2$ uses $q$, one such triple, and a two-set. We need $W\ge6$.
If there is at most one outside triple, $b_1=0$ and every bad two-set
avoids it. The double cover at $q$ on the remaining four points permits
at most four bad vertices. If the two triples meet at $p$,
$b_1=0$ and every bad two-set avoids $p$.
Two other vertices in $F(q)$ are needed to double-cover $p$, so $b_2\le5$.
If the two triples are disjoint, all singleton negatives share the
remaining point and $b_1\le2$. No $b_2$ is possible: its own pair
contains the remaining point and one point of the unused triple,
forcing its pair helper to share the other two points with that triple.
Each case contradicts $W\ge6$.

The other large-set residues are precisely profiles 194, 210, 253, 319.
They have one or two quads, all at degree six; the first three have
$m=3$ and require $W\ge10$, while profile 319 has $m=4$ and requires $W\ge8$.

If a quad $R$ is disjoint from $Q$, every negative vertex must also be
far from its vertex: otherwise the other three covering blocks could
cover at most three of its four points.
The double cover at $q$ must contain the quad vertex itself;
without it, eight far vertices would be needed to cover $R$ twice,
exceeding $f\le7$.
After that quad covers $R$ once, at least four additional far vertices
must meet $R$. Negative vertices avoid $R$, so at most $f-5\le2$ of
them remain, giving $W\le4$, a contradiction.

Every remaining quad therefore intersects $Q$ once.
Fix one, $R$, and put $B=R\setminus Q$, $O=T\setminus(Q\cup R)$,
of sizes three and four. A singleton negative's two far triples
each consist of one point of $B$ and an edge on $O$.
Actual triples form a simple properly three-edge-colored graph on four
points. Such a graph has at most one disjoint differently colored edge pair:
two pairs would form a four-cycle with both adjacent and opposite edges
differently colored, requiring four colors.
Thus all singleton negatives have the same point and $b_1\le2$.
It follows that $W\le f+b_1\le9$, excluding the three $m=3$ profiles.

In profile 319 there is just one quad.
Every negative vertex's own set meets $B$ exactly once, because its
partition must cover the three points of $B$ using its own set and its
two far blocks besides $Q$.
The double cover at $q$ gives $b_1+b_2\le6$.
Together with $W\ge8$ and $b_1\le2$, equality forces
$b_1=2,b_2=4$ and six negative vertices in $F(q)$.
One other far vertex remains. The four bad pairs contribute four
incidences on $O$, the singleton negatives none. To double-cover $O$,
that final vertex must have high set exactly $O$.
This would be a quad disjoint from $Q$, whereas the only quad is $R$.
The contradiction proves **$c(v)\le4$ for every low vertex**.

## All high forests with at most two edges are impossible

The initial arithmetic already excludes $m=0,1$.
After the large-set exclusion, the twelve residual $m=2$ profiles have
three or four quads.

With three quads, there are at most five actual high triples in total,
including both low degrees, and (4) requires $W\ge8$.
An intersection path gives $W\le7$; a triangle has only single-quad
bad vertices.
A pair of disjoint helper triples can serve at most one quad: two
quads in their six-point complement would intersect in at least two points.
It then determines a unique bad two-set.
A linear family of $t\le5$ triples on twelve points has at most

$$
 \binom t2-\max(0,3t-12)\le7
$$

disjoint pairs. This follows from
$|\bigcup C_i|\ge3t-\sum_{i<j}|C_i\cap C_j|$.
So the triangle case also has $W\le7$.

The four-quad profiles have at most two helper triples.
Let $D$ be the disjointness graph of their high sets.
A singleton cover forces its selected pair to be the only edge of $D$;
every other quad contains the singleton point and meets both selected quads.
All singleton negatives share their point and triple, so $b_1\le2$,
and the complementary-triple argument forbids double-quad bad vertices.
There is at most one single-quad bad vertex from the at most two triples,
giving $W\le5$.

If $b_1=0$, a double-quad bad cover can use only an **isolated edge**
of $D$: each unused quad must meet both selected quads.
Each such edge supports at most four bad two-sets.
A single-quad bad cover requires an isolated vertex of $D$ and again
there is at most one in total.
Unless $D$ is a perfect matching, this gives $W\le5$.
For a perfect matching, only the two double-quad categories are possible,
so $W\le8$.

Every four-quad row requires $W\ge8$.
Those requiring more are excluded. In the two equality rows, 70 and 129,
there are fewer than four high-singleton vertices in the whole graph.
Each double-quad category must have four bad vertices.
At a quad $q$, their eight high incidences saturate the double cover
on the four points outside that quad and its disjoint partner.
The other at most five far vertices must lie within the partner quad.
By linearity, only the partner itself can contribute more than one point.
To supply eight incidences, all five vertices are needed:
the partner quad and **four distinct singleton vertices**.
The inventory has too few singletons. This excludes the equality cases,
and proves **$m\ge3$**.

## A local realizability condition for the six-edge cover

Fix a six-vertex $v$.
For every $t\in T\setminus C(v)$, equation (2) supplies exactly two
vertices of $F(v)$ containing $t$ in their high sets.
Join those two far vertices by an auxiliary edge labeled $t$.
No loop occurs. Two labels cannot give the same edge, since two distinct
vertices cannot share two high neighbors.
The auxiliary graph is therefore simple, with

$$
 |V|=9-\epsilon_v,\quad |E|=12-c(v),\quad
 \{\text{vertex degrees}\}=\{c(u):u\in F(v)\}.                  \tag{7}
$$

This includes zero-degree auxiliary vertices.
Consequently the far high-count list must be graphical, not merely have
the right length and sum.

Adjacent low vertices $u,v$ have $C(u)\cup C(v)$ independent in $H$:
an intersection creates a triangle and an edge between the sets creates
a four-cycle. The path forest $H$ has $m-k$ nontrivial components;
selecting one edge from each gives a matching of size $m-k$.
Thus every independent set has size at most $12-m+k$, and

$$
 c(u)+c(v)\le12-m+k\qquad(u\sim v,\ u,v\notin T).               \tag{8}
$$

These are constraints on actual incidences. Their use in the following
finite relaxation asserts only necessity.

## The eleven exact six-edge certificates

The complete inventory has ten $m=6$ profiles, indices 393 through 402.
The model in [a0_far_models.py](a0_far_models.py) retains every type
$\tau=(d,(a,b,c))$ permitted by its profile, the radius-two ball bound,
and $s_t=5$ for high types.

Nonnegative variables $X_\tau$ count vertices.
For admissible type pairs, $Y_{\tau\sigma}$ counts edges;
a diagonal variable counts internal edges twice.
A low-low type pair is omitted only when it violates (8).
Class totals, cross-class handshakes, type-to-degree neighbor balances,
and class-pair edge-plus-two-path capacities are imposed.

For a type-$\tau$ vertex, the exact class-ball identity is

$$
 \sum_{u\sim v}|N(u)\cap V_j|+|N(v)\cap V_j|
 +|F(v)\cap V_j|
 =n_j+(d(v)-1)[d(v)=j].                                      \tag{9}
$$

Every high root has zero far count, and every root has zero far high count.
These instances are imposed as equalities.
For the other instances the basic model first uses far-count nonnegativity.

Now group low vertices by $(d,c)$, with their profile multiplicities $n_g$.
For every low type $\tau$, enumerate all integer far patterns
$\pi=(\pi_g)$ satisfying

$$
 \sum_g\pi_g=|F(v)|,\quad
 \sum_g c_g\pi_g=(8-d(v))(12-c(v)),\quad
 0\le\pi_g\le n_g-[g=(d(v),c(v))].                            \tag{10}
$$

For $d(v)=6$, retain only patterns whose high-count degree list is
graphical, as required by (7). The generator checks all the degree-list
inequalities
$\sum_{i\le r}d_i\le r(r-1)+\sum_{i>r}\min(r,d_i)$.
Their necessity follows by counting edges incident to the $r$ vertices.
The independent checker instead uses Havel--Hakimi degree reduction.
The complete retained pattern lists agree entry for entry.

A variable $Z_{\tau,\pi}$ counts vertices of type $\tau$ with pattern $\pi$.
Impose $\sum_\pi Z_{\tau,\pi}=X_\tau$.
Use the pattern's far degree-class counts to make both low instances
of (9) exact.
Finally impose symmetry of far incidences between each two distinct
$(d,c)$ groups. Diagonal group incidences are already counted from
each endpoint and need no cross-group equality.
Every graph supplies such variables; no integral relaxation solution
is asserted to realize a graph.

Eight certificates exclude every $m=6$ profile except 395 and 401.
Profile 401 has one six-quad. Its epsilon is one of $0,1,2$,
since it has exactly two low neighbors.
Three additional certificates exclude all three cases.
This is a complete cover of every six-edge high forest and low profile,
apart from the single row closed below.

For all variables together,

$$
 \sum X+\sum Y+\sum Z\le54+374+42=470.                         \tag{11}
$$

The budget **470**, rather than the earlier 428, includes the new patterns.
Equality multipliers are unrestricted and upper-row multipliers nonpositive.
Let $b$ be the combined right side and $\delta$ the maximum of zero and
every combined column coefficient. Then a graph would imply
$0\ge b-470\delta$.
All eleven supplied duals have strictly positive exact corrected bounds.
They are recorded in [a0_expected.json](a0_expected.json).

## The final six-edge profile is impossible

The surviving profile 395 is

$$
 H=6P_2,\qquad V_6:c=3^{16},\qquad V_7:c=0^2 1^{12}2^{12}.      \tag{12}
$$

There is no quad, so no negative type is possible.
The charge sum in (1) is zero. Every seven-vertex has nonnegative charge,
and its $c-3$ is nonzero, so all seven epsilons are zero.

Each of the twelve $c=1$ seven-vertices has four far vertices whose
high-counts must be $3,3,3,2$.
Thus each has a far $c=2$ seven-vertex, giving $U\ge12$.
Now $Q\le4$, while
$\sum_{V_6}\epsilon=4$ and
$\sum_{V_6}\epsilon^2\ge\sum_{V_6}\epsilon$.
Equality holds throughout:
$Q=4,U=12$, four six-vertices have epsilon one and the other twelve zero.

Each $c=2$ seven-vertex also needs a far seven-vertex:
four far six-triples alone would have high-count sum twelve instead of ten.
The twelve far seven-seven pairs therefore form a perfect matching
between the $c=1$ and $c=2$ classes.
Every such vertex has exactly one far seven-vertex.

Call the four positive-epsilon six-vertices $P$.
Their neighbor-degree counts are $(0,3,3)$; the other twelve
six-vertices have counts $(1,2,3)$.
For a seven-vertex $y$ of high count $c=1$ or $2$,
$\epsilon_y=0$ gives neighbor counts $(c,7-2c,c)$.
The local weighted identity

$$
 \sum_{u\sim y}s_u=50-s_y+6-\sum_{u\in F(y)}(d(u)-6)
$$

then gives

$$
 \sum_{u\sim y,\ d(u)=6}\epsilon_u=c-1.                       \tag{13}
$$

Indeed the baseline neighbor sum is $49-c$, the right side is $48$,
and all seven epsilons vanish.
Thus every $c=2$ seven-vertex has **exactly one neighbor in $P$**.

Choose a $c=0$ seven-vertex $x$.
Its epsilon zero means all seven neighbors have degree seven.
Since all high vertices are within distance two of $x$, uniqueness of
short paths gives $\sum_{y\sim x}c(y)=12$.
Each summand is at most two, so at least five neighbors have $c=2$.
Their neighbors in $P$ must be distinct: sharing one makes the four-cycle
$x,y,p,y',x$.
But $|P|=4$. This contradiction excludes (12), and hence **every $m=6$ graph**.

## Complete remaining frontier and reproduction

The 63 remaining necessary profiles have $3\le m\le5$ and $c\le4$.
There is at least one quad, since otherwise $W=0$ contradicts
$W\ge12-2m>0$.
Their high forests, with isolated vertices added to total twelve, are:

| $m$ | Nontrivial path orders |
|---|---|
| 3 | $(2,2,2)$; $(2,3)$; $(4)$ |
| 4 | $(2,2,2,2)$; $(2,2,3)$; $(2,4)$; $(3,3)$; $(5)$ |
| 5 | $(2,2,2,2,2)$; $(2,2,2,3)$; $(2,2,4)$; $(2,3,3)$ |

The expected record lists every profile and every forest explicitly.
The count 63 is the remaining cover proved here; exploratory stronger
relaxations are not silently used to shrink it.

Regenerate the eleven certificates outside the repository using
CPython 3.11.2, NumPy 2.4.6 and SciPy 1.15.3
([pinned requirements](requirements-a3.txt)).
Verification uses CPython 3.11+ and its standard library:

~~~sh
python3 -m venv /tmp/order54-a0-env
/tmp/order54-a0-env/bin/pip install -r requirements-a3.txt
/tmp/order54-a0-env/bin/python generate_a0_certificates.py --output /tmp/order54-a0-certificates.json
python3 verify_a0.py --certificates /tmp/order54-a0-certificates.json > /tmp/order54-a0-check.json
cmp /tmp/order54-a0-check.json a0_expected.json
python3 -O verify_a0.py --certificates /tmp/order54-a0-certificates.json > /tmp/order54-a0-check-O.json
cmp /tmp/order54-a0-check-O.json a0_expected.json
~~~

The checker compares independently reconstructed types, admissible edges,
every matrix row and column, and all 2,190 pattern columns in the eleven
cases. It checks 5,777 total case-columns with exact rational arithmetic.
Four corrupted certificates must be rejected, including one that
incorrectly reuses the budget 428.

Finite incidence controls cover all 19,800 normalized ordered four-quad
families, 8,856 singleton templates, and 34,848 double-quad templates.
They verify the disjointness-graph classifications and the equality cover.
Further controls exhaust all 4,096 four-point edge-color words
(478 proper colorings), and all 385 linear pairs of triples on seven points.
Actual-graph controls use the existing 185-edge fixture and its edge
deletions, retaining 185 graphs with a nonempty set of high sinks.
They check 8,530 individual low-root covers and construct the simple
auxiliary graphs with 1,668 edges in total.

These controls are not order-54 extremal witnesses.
The remaining trust boundaries are the imported order-53 upper bound,
the preceding all-sink theorem, the written incidence reductions,
unformalized exact Python, and hardware.
The two algorithmic implementations are internal independent checks,
not external peer review or formal verification.
The new conditional A0 reduction uses the degree reduction and corrected
identities; the earlier A1/A2 certificates enter only through the theorem
that all twelve high vertices are sinks.

An exploratory full-realization SAT run on (12) ended UNKNOWN at its
300,000-conflict budget after 102.10 seconds. It supplies no premise.
The human contradiction (13) makes that search unnecessary.
Other exploratory feasible relaxations likewise supply no graph.
All generated bundles, CNF, and logs remain outside Git.
Historical priority and a numerical extremal improvement are not claimed.

## Elementary packing details used in the reduction

These details make the conditional all-sink proof independent of the
earlier A1/A2 classification certificates.

For a linear triple family on eight points, every point lies in at most
three triples, so there are at most eight triples. With $r$ triples and
point degrees $d_i$, the number of disjoint pairs is
$\binom r2-\sum_i\binom{d_i}2$. Convexity of the integer function
$\binom x2$, at fixed sum $3r$, gives upper bounds
$0,0,1,2,2,3,3,3,4$ for $r=0,\ldots,8$.

For the colored-graph bound on five points, each of three color classes
is a matching of size at most two, so the graph has $r\le6$ edges.
If its vertex degrees are $d_i$ and its color-class sizes are $a_j$,
the number of disjoint differently colored edge pairs is exactly
$\binom r2-\sum_i\binom{d_i}2-\sum_j\binom{a_j}2$.
Integer convexity, using sums $2r$ and $r$, gives upper bounds
$0,0,1,2,2,3,3$ for $r=0,\ldots,6$.
The triple-to-edge encoding is simple and properly colored because
repeated edges or incident same-colored edges would make two high triples
share two points. A bad two-set injects into its helper pair because
the complementary high two-set is unique.

For the complementary-triple obstruction, two disjoint quads in a
singleton cover leave a four-point complement $\{p\}\cup Z$, with $Z$
a triple. Different such triples would intersect twice, so every singleton
cover uses this same $p,Z$. A double-quad bad vertex has a high two-set
in that complement; linearity forces it to contain $p$ and one point
of $Z$. Its final helper must contain the other two points of $Z$.
It cannot be a different vertex by linearity, or the vertex of $Z$ itself
by far-disjointness. Thus these two negative categories cannot coexist.

With three quads, a double-quad bad cover uses two disjoint quads.
The third quad meets both selected quads and has two points in their
four-point complement. The bad two-set must contain one of those points
and one of the other two, leaving at most four possible bad two-sets.
A single-quad cover meets each of the two other quads, so its selected
quad has degree two in the intersection graph. The colored-graph bound
applies to each such category. A singleton cover forces the path shape
and uses its leaves; the preceding obstruction then removes the
double-leaf category. This proves the bounds used above for every
intersection shape and both possible degrees of a quad vertex.

## Recorded exact replay

The regenerated eleven-certificate bundle matched the original byte for byte.
It is 109,272 bytes and remains outside Git.
Normal and optimized CPython 3.11.2 checks took
2.51 and 2.75 seconds,
with peak child resident memory 26,140 KiB.
Their 26,585-byte outputs agree, with SHA-256

~~~text
0c0fc2d434f381b73e4c93d75ae00bd0a6294f67b3794a40be99ba8cad0d507b
~~~
