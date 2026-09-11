# All twelve degree-eight vertices are sinks at order 54

**Theorem.** Let $G$ be a finite simple graph with 54 vertices, 187 edges,
girth at least five, and twelve degree-eight vertices. Put
$T=V_8$, $F(v)=\{u:\operatorname{dist}(u,v)>2\}$, and
$A=\sum_{t\in T}|F(t)|$. Then **$A=0$**: every vertex is within distance
two of each of the twelve high vertices.

The [preceding theorem](z12_A2_exclusion.md) gives $A\le1$.
This proof excludes **the entire $A=1$ subclass**, for both possible
degrees of the missed vertex and every high induced graph.
Its new ingredients are individual high-neighborhood partitions and a
complete inventory of 91 integer profiles. No new solver certificate
or graph enumeration is used.

The numerical interval remains
$185\le\operatorname{ex}(54,\{C_3,C_4\})\le187$.
The all-sink case $z=12,A=0$ and the cases $z\le11$ remain unresolved.
This is a structural restriction, not a construction or an exclusion of
the entire twelve-high case.

## The unique missed vertex and the exact inventory

Assume $A=1$. There is a unique high nonsink $r$ with $F(r)=\{x\}$.
The other eleven high vertices are sinks. As proved in the preceding work,
$d(x)\in\{6,7\}$ and $C(x)=\varnothing$, where
$C(v)=N(v)\cap T$ and $c(v)=|C(v)|$. Indeed, a high-high far pair would
contribute two to $A$, and the high/high commutator prevents any high sink
from being adjacent to $x$.

Write $H=G[T]$, $m=e(H)$, $k=|\{t:d_H(t)=2\}|$, $h=d_H(r)$,
and $p=[d(x)=7]$. The [degree reduction](proof.md) gives
$(n_6,n_7,n_8)=(16,26,12)$.
For low vertices define
$s_v=\sum_{u\sim v}(d(u)-6)$ and
$\epsilon_v=s_v-8$ on $V_6$, $\epsilon_v=s_v-7$ on $V_7$.
The [corrected identities](z12_distant_incidence_bound.md) specialize to

$$
\begin{split}
 &d_H(t)\le2,\qquad
 \sum_{V_6}c=37+2m,\quad \sum_{V_7}c=59-4m,\\
 &\sum\epsilon=5,\qquad
 \sum c\epsilon=2m+h-p,\qquad
 \sum(c-3)\epsilon=2m+h-p-15,\\
 &\sum_{V_6}\frac{(c-3)(c-2)}2+
   \sum_{V_7}\frac{(c-1)(c-2)}2=7-m-k=:B,\\
 &Q+2U=23,\qquad Q\le23-4p,\\
 &Q=\sum_{V_6}\epsilon^2+\sum_{V_7}\epsilon(\epsilon-1).
\end{split}                                                        \tag{1}
$$

Here $U=\sum_{\{u,v\}\text{ far}}(d(u)-6)(d(v)-6)\ge0$.
There are no high-high far pairs, and the sole high-low far pair contributes
$4p$ to $2U$. Also $\sum h_t|F(t)|=h$, explaining both corrections in (1).

The mandatory $c=0$ vertex costs three inventory units if $d(x)=6$,
one if $d(x)=7$. Thus $m+k\le4$ or $m+k\le6$, respectively.
Every cycle in $H$ would have length at least five and contribute at
least ten to $m+k$. Consequently $H$ is a path forest. For $m=0$, $k=h=0$.
For $m>0$, $0\le k\le m-1$, and we use the safe bound

$$
 h\le h^*=
 \begin{cases}2&k>0,\\1&k=0,\ m>0,\\0&m=0.\end{cases}                \tag{2}
$$

No specific labeling, matching, or position of $r$ is assumed here.

The complete inventory is small. If $n_{dc}$ counts degree-$d$ vertices
with high count $c$, the nonzero inventory costs are

| $(d,c)$ | $(6,0)$ | $(6,1)$ | $(6,4)$ | $(6,5)$ | $(6,6)$ | $(7,0)$ | $(7,3)$ | $(7,4)$ | $(7,5)$ |
|---|---|---|---|---|---|---|---|---|---|
| cost | 3 | 1 | 1 | 3 | 6 | 1 | 1 | 3 | 6 |

All larger possible $c$ have cost at least ten and cannot occur.
The zero-cost counts are $n_{62},n_{63},n_{71},n_{72}$.
Enumerate the nine charged multiplicities with total cost $B$ and the
mandatory endpoint, then determine these four remaining counts from
the two vertex totals and two high-incidence totals in (1). Keep precisely
the nonnegative integer solutions.

This gives **17 profiles for $d(x)=6$ and 74 for $d(x)=7$**.
An independent enumeration recursively assigns every multiplicity for
$c=0,\ldots,d$, imposing the vertex, incidence, and cost totals directly.
The two censuses agree entry for entry; the entire table is included in
[a1_exclusion_expected.json](a1_exclusion_expected.json).
The sum of the two largest low high-counts is less than ten in every row.

## Individual covers and the required negative charge

The absence of four-cycles gives

$$
 |C(u)\cap C(v)|\le1\quad(u\ne v).                                \tag{3}
$$

This includes high vertices such as $r$.
Far vertices have disjoint high sets. In particular, a high two-set or
triple cannot occur at two distinct vertices.

The corrected individual identity is

$$
 (8-d(v))[t\in C(v)]+\sum_{u\in F(v)}[t\in C(u)]
 =8-d(v)+[t=r][x\sim v],\qquad t\in T.                            \tag{4}
$$

Thus for a seven-vertex, its own set and its far vertices' sets cover $T$.
There is at most one repeated point, necessarily $r$.
The correction is retained in every case below.
We have $|F(v)|=9-\epsilon_v$ on $V_6$ and
$|F(v)|=4-\epsilon_v$ on $V_7$.

The local ranges are $2c-8\le\epsilon\le c-2$ on $V_6$ and
$2c-7\le\epsilon\le c$ on $V_7$.
Every six-vertex has $(c-3)\epsilon\ge0$.
The only negative seven-types $(c,\epsilon)$ are $(1,1),(2,1),(2,2)$.
Call their counts $b_1,b_2,b_{22}$.
None is $x$, so all of its far vertices are low.
A $(2,2)$ vertex would need two far high sets with size sum at least ten.
The complete inventory rules this out, so $b_{22}=0$.

Put $W=2b_1+b_2$.
The positive part of $\sum(c-3)\epsilon$ is at least

$$
 L_+=\sum_{c<2}n_{6c}(c-3)(c-2)
 +\sum_{c\ge4}n_{6c}(c-3)(2c-8)
 +\sum_{c\ge4}n_{7c}(c-3)(2c-7).
$$

Equation (1) therefore gives

$$
 W\ge15+p-2m-h^*+L_+.                                           \tag{5}
$$

Writing $P=\sum\max(\epsilon,0)$ and $N=\sum\max(-\epsilon,0)$,
we have $N\le Q$, $P=5+N\le28-4p$, and $W\le P+b_1$.

A high set of size at least five must itself be a far set of every
negative vertex: otherwise each of the four covering sets in (4) would
meet it in at most one point, leaving a point uncovered.
For such a vertex of degree $d$ and high count $c$, its far capacity is
at most $f=17-2c$ if $d=6$, or $f=11-2c$ if $d=7$.
Hence $b_1+b_2\le f$ and

$$
 W\le\min(2f,f+n_{71}).                                         \tag{6}
$$

If there is no set of size at least five, call the size-four sets
**quads**. Every $b_1$ vertex needs at least two quads among its three
far vertices, and every $b_2$ vertex needs at least one.
A six-quad has far capacity at most nine, a seven-quad at most three.
Thus

$$
 W\le9n_{64}+3n_{74}.                                           \tag{7}
$$

With fewer than two quads, $b_1=0$.

## One- and two-quad bounds

**One quad gives $W\le4$.**
A $b_2$ cover must be a true partition of sizes $2+4+3+3$.
The helper triples lie on the eight points outside the quad and form a
linear triple family: distinct triples intersect in at most one point.
The bad vertex injects into its unordered pair of disjoint helper triples,
since that pair determines its unique complementary high two-set.

Any linear triple family on eight points has at most four disjoint pairs.
Each point belongs to at most three triples: the triples through it use
disjoint pairs of the other seven points. Hence the family has $r'\le8$
triples. If its point degrees are $d_1,\ldots,d_8$, its number of disjoint
pairs is exactly

$$
 \binom {r'}2-\sum_{i=1}^8\binom{d_i}{2}.
$$

The integer convexity bound with $\sum d_i=3r'$ gives the respective upper
bounds $0,0,1,2,2,3,3,3,4$ for $r'=0,\ldots,8$.
This covers all family sizes, extending the earlier bound for at most
five triples.

**Two quads give $W\le9$; if $b_1>0$, then $W\le6$.**
Let their sets be $Q_1,Q_2$.
A $b_1$ cover must partition $T$ into $Q_1,Q_2$, a triple $Z$,
and its singleton $\{p_0\}$. In particular the quads are disjoint.
Every such vertex uses the same $Z,p_0$: different triples on the
four-point complement would intersect in at least two points.
If a quad has degree seven, its far capacity gives $b_1\le3$.
Otherwise apply (4) at a six-quad, at $p_0$ outside it, to obtain

$$
 b_1\le2+[x\sim q_i]\le3.                                      \tag{8}
$$

In this situation no $b_2$ vertex exists. Such a vertex must use both
quads: a cover using just one would leave the other four-set to be covered
by three sets, each meeting it at most once.
Its own two-set lies in $\{p_0\}\cup Z$ and meets $Z$ at most once,
so contains $p_0$ and one point of $Z$. Its third far set must contain
the remaining two points of $Z$, violating (3). If that set is $Z$
itself, far-disjointness instead fails. This argument also permits the
extra multiplicity in (4). Hence $W=2b_1\le6$.

When $b_1=0$ and the quads are disjoint, every bad vertex is far from both,
giving $W=b_2\le9$.
If the quads intersect, the
[colored-edge argument](z12_A2_exclusion.md#at-most-eight-bad-vertices)
gives $b_2\le3+3+2=8$.
For completeness, each single-quad group uses two triples in a partition.
Relative to the other quad, a triple consists of one of three color points
and an edge on the five points outside both quads. Actual triples form a
simple properly three-edge-colored graph. There are at most three disjoint
differently colored edge pairs, by the lemma proved in that source.
Each both-quad bad vertex instead needs a distinct linear triple on the
five outside points, and at most two can coexist.
The helper degrees do not enter this reasoning; only their actual high
sets matter.

## The six remaining profiles

For every inventory row combine (5) with (6), when applicable, or (7)
and the one-/two-quad bounds. Also impose
$W\le28-4p+b^*$ and $W\le2b^*+n_{72}$, where $b^*=n_{71}$
except that $b^*=0$ with fewer than two quads and no larger set.

These explicit integer inequalities exclude all 17 degree-six endpoint
profiles and 68 of the 74 degree-seven endpoint profiles.
Exactly the following six rows remain. Exponents are multiplicities;
all omitted counts are zero. The last column gives the lower and upper
bounds used in this inventory pruning.

| Row | $m$ | $k$ | $V_6$ high counts | $V_7$ high counts | $(L,U)$ |
|---|---|---|---|---|---|---|
| I | 2 | 0 | $2^{10}3^3 4^3$ | $0^1 2^{24}3^1$ | $(11,24)$ |
| II | 3 | 0 | $2^7 3^7 4^2$ | $0^1 1^4 2^{20}3^1$ | $(9,9)$ |
| III | 3 | 0 | $2^7 3^7 4^2$ | $0^2 1^1 2^{23}$ | $(9,9)$ |
| IV | 3 | 0 | $2^8 3^5 4^3$ | $0^1 1^3 2^{22}$ | $(9,27)$ |
| V | 3 | 1 | $2^7 3^7 4^2$ | $0^1 1^3 2^{22}$ | $(8,9)$ |
| VI | 4 | 0 | $2^5 3^9 4^2$ | $0^1 1^7 2^{18}$ | $(7,9)$ |

In all six, $x$ has degree seven and every quad has degree six.
Let $a=|N(x)\cap V_6|$. Since $c(x)=0$,
$\epsilon_x=-a$, so $x$ contributes $3a$ to the positive charge.
Using the actual value of $h$ in (1) gives

$$
 W\ge16-2m-h+3a.                                               \tag{9}
$$

At $x$, the correction in (4) vanishes because $x$ is not adjacent to itself.
Thus the sets at the $4+a$ vertices of $F(x)$ **partition $T$**.
One of these vertices is $r$ and all the others are low.
In particular, if $a=0$,

$$
 T=C(r)\ \dot\cup\ C(u)\ \dot\cup\ C(v)\ \dot\cup\ C(w),
 \qquad F(x)=\{r,u,v,w\}.                                     \tag{10}
$$

This partition is the additional individual constraint that closes the
entire inventory.

## Closing the four two-quad profiles

For rows II, III, V, VI, (9) has base $16-2m-h\ge7$.
Thus $b_1>0$ contradicts $W\le6$; we have $W=b_2\le9$.
Equation (9) then forces $a=0$.

First suppose $k=0$, covering rows II, III, VI.
Here $h\le1$, so the three low blocks in (10) must total at least eleven.
There are only two quads, and all other high sets have size at most three.
Therefore $h=1$ and those three blocks are both quads and a triple $Z$.
The quads are disjoint.

Every bad vertex is far from both quads. Its own two-set lies in their
four-point complement, partitioned into the singleton $C(r)$ and the triple
$Z$. It meets each block in at most one point, so there are at most three
possible two-sets. Distinct bad vertices require distinct two-sets.
Hence $b_2\le3<7$, a contradiction.

In row V, $m=3,k=1,h\le2$. Equation (9) and $W\le9$ show that the
total positive charge, now that $a=0$, is at most one.
Each six-quad contributes its nonnegative $\epsilon$.
At least one quad $q$ therefore has $\epsilon_q=0$.
At a degree-six vertex with $c=4$, $\epsilon_q=|N(q)\cap V_7|$.
Thus this quad has no seven-neighbor.
All neighbors of $x$ are seven-vertices, so $q$ is neither adjacent to $x$
nor shares a neighbor with it: **$q\in F(x)$**.

If the quads intersect, $W\le8$ together with $W\ge10-h$ forces
$h=2,W=8$ and zero total positive charge. Both quads then have
$\epsilon=0$ and belong to $F(x)$, contradicting the partition (10).

If the quads are disjoint, the other quad also belongs to $F(x)$.
Otherwise it is disjoint from $C(q)$ and meets the other three blocks
of (10) in at most one point each, failing to cover its four points.
Now the four-point complement of the quads partitions into $C(r)$
of size $h$ and one other block of size $4-h$.
We must have $h=1$ or $2$; $h=0$ would require a third quad.
A bad two-set meets both blocks at most once, so there are at most
$h(4-h)\le4$ possibilities. Thus $b_2\le4<8$, another contradiction.

## Closing the two three-quad profiles

Rows I and IV have $m=2$ or $3$, $k=0$, $h\le1$, and $n_{71}\le3$.
Write $Q_1,Q_2,Q_3$ for the quads and let $J$ be their intersection graph.
Its edges mean intersection in one point.
We first prove **$W\le11$**, retaining every possible correction at $r$.

A $b_1$ vertex uses either two quads and a triple, or all three quads.
In the first case its cover is a $1+4+4+3$ partition.
The unused quad must meet all four partition blocks, so it meets both
selected quads. Hence $J$ is a path and the selected quads are its leaves.
In the second case the three quads have union of size eleven.
Their total size is twelve, so $J$ has exactly one edge.

A $b_2$ vertex uses one or two quads.
It cannot use all three because the size sum with its own two-set would
be fourteen, exceeding the total multiplicity at most thirteen in (4).

If it uses one quad, the cover is a $2+4+3+3$ partition.
Each unused quad must meet the selected quad; otherwise three remaining
blocks could cover at most three of its points. Thus the selected vertex
has degree two in $J$. For each possible selected quad there are at most
three bad vertices, by the same colored-edge lemma as above, using either
intersecting quad to define the colors.

Suppose it uses two disjoint quads.
The unused quad must meet both: the bad two-set and the third far set can
cover at most two additional points. Thus $J$ is a path with the selected
quads as leaves. The unused quad has exactly two points in the four-point
complement of the leaves. The bad two-set meets this two-set exactly once,
because it and the third far set together cover those two points, each
meeting the unused quad at most once.
There are at most $2\cdot2=4$ possible bad two-sets in this category.

Suppose instead it uses two intersecting quads.
Their intersection is the unique repeated point, so must be $r$.
The third far set is a triple in the five-point complement of their union;
the bad two-set is its complement there.
The unused quad must meet both selected quads at **distinct** points:
otherwise it has at least three points outside their union, but the bad
two-set and helper triple cover at most one of those points each.
Hence $J$ is a triangle with three distinct pairwise intersection points.
For fixed $r$, at most one quad pair is eligible.
That pair supports at most two bad vertices, by the five-point linear
triple bound.

These observations give the following bounds:

| Shape of $J$ | Upper bound for $W$ |
|---|---|
| No edges | 0 |
| One edge | $2n_{71}\le6$ |
| Two edges, a path | 9 |
| Three edges | $3+3+3+2=11$ |

For the path bound, if $b_1=0$ there are at most three single-quad bad
vertices at the center and four double-quad bad vertices using the leaves.
Thus $W\le7$.
If $b_1>0$, all such singleton vertices use the same triple and singleton
outside the leaf quads. The two-quad argument following (8) forbids every
double-leaf bad vertex in their presence. Hence
$W\le2n_{71}+3\le9$.
When $a=0$, neither six-quad is adjacent to $x$, and (8) improves
$b_1\le2$, so the path bound improves to **$W\le7$** in both cases.

Equation (9) requires $W\ge9+3a$.
The universal upper bound eleven therefore forces $a=0$.
Now (10) has $h\le1$ and three low blocks totaling at least eleven.
It must contain at least two quads, and these must be disjoint.
Thus $J$ cannot be a triangle.
The other three shapes at $a=0$ all have $W\le7$, contradicting $W\ge9$.

All six profiles are excluded. Together with the complete inventory,
this proves $A=1$ impossible. The preceding $A\le1$ theorem now gives $A=0$.

## Reproduction and scope of the checks

[verify_a1_exclusion.py](verify_a1_exclusion.py) uses CPython 3.11 or later
and the standard library, importing the existing colored-graph checker.
It checks:

- All 91 integer profiles by two different complete algorithms, comparing
  their entries and publishing the entire inventory with its pruning bounds.
- The local charge signs, far-size obstruction, six terminal profiles,
  and their final integer inequalities.
- All $4^8$ degree words in the eight-point triple convexity bound.
- All 8,326 properly three-edge-colored simple graphs on five points,
  using the preceding checker's ordered-matching and edge-word enumerations.
- All 294 normalized three-quad arrangements. The first quad is fixed;
  the second is either disjoint or intersects it once, with every possible
  third quad retained. This is a complete cover under relabeling, not an
  enumeration of unlabelled isomorphism classes.
- Every permissible two-/three-point helper set in these arrangements:
  349 singleton templates, 13,176 single-quad bad templates,
  4,368 disjoint-double-quad templates, and 1,620 intersecting-double-quad
  templates. It checks the intersection-graph classifications, the
  repeated point, the four-two-set bound, and the coexistence obstruction.

From this directory:

~~~sh
python3 verify_a1_exclusion.py > /tmp/order54-a1.json
cmp /tmp/order54-a1.json a1_exclusion_expected.json
python3 -O verify_a1_exclusion.py > /tmp/order54-a1-O.json
cmp /tmp/order54-a1-O.json a1_exclusion_expected.json
~~~

These finite controls do not enumerate order-54 graphs and do not supply
external peer review or formal verification. The complete inventory
census is an exact computational part of this proof; the written
incidence reductions and covering arguments remain human mathematics.
The combined all-sink theorem imports the preceding $A\le1$ result and
its dependency chain, including the 36 exact certificates in the $A=2$
classification and the published order-53 upper bound.
The new conditional $A=1$ exclusion itself needs only the degree reduction
and corrected identities, not those $A=2$ solver models.

Exploratory linear programs helped find the route but establish no part
of this proof. Their candidate duals and feasible relaxations remain in
scratch and are not promoted to verified certificates or graph witnesses.
Historical priority is not asserted. The remaining realization problem is
the whole all-sink subclass $z=12,A=0$.

## Recorded verification

Normal and optimized CPython 3.11.2 runs produced byte-identical output
in 3.46 and 3.53 seconds, respectively,
with peak child resident memory 22,744 KiB. The complete expected
record is 38,475 bytes. Its SHA-256 is

~~~text
3747dec85fe2224e97e3fad42f614edf7a6ccaa50f3c890e2360af430487e131
~~~
