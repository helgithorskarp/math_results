# The five-edge matching is impossible at two high distant incidences

**Theorem.** Let $G$ be a finite simple graph with 54 vertices, 187 edges,
girth at least five, and twelve degree-eight vertices. Put
$T=V_8$, $F(v)=\{u:\operatorname{dist}(u,v)>2\}$, and
$A=\sum_{t\in T}|F(t)|$. If $A=2$, then $G[T]$ is a matching of
**exactly four edges**. Moreover, the two degree-six vertices with four
high neighbors have **exactly one common high neighbor**.

This excludes the **entire five-edge matching subclass**, with every
assignment of actual vertices and edges. It also excludes the whole
disjoint-four-set configuration in the remaining four-edge subclass.
The proof is a human incidence argument using the preceding exact
[A2 classification](z12_A2_reduction.md). The finite enumerations below
are independent controls for its small set-packing step.

The unrestricted question remains open:
$185\le\operatorname{ex}(54,\{C_3,C_4\})\le187$.
Cases with fewer than twelve high vertices, the twelve-high cases
$A=0,1$, and the remaining $A=2$ four-edge case are not excluded.

## Imported classification and the individual cover

Write $C(v)=N(v)\cap T$, $c(v)=|C(v)|$,
$s_v=\sum_{u\sim v}(d(u)-6)$, and
$\epsilon_v=s_v-8$ on $V_6$, $\epsilon_v=s_v-7$ on $V_7$.
The preceding classification supplies degree counts $(16,26,12)$ and:

* There are two nonsinks $r_1,r_2$ with distinct degree-seven endpoints
  $x_1,x_2$, where $F(r_1)=\{x_2\}$, $F(r_2)=\{x_1\}$,
  and $C(x_i)=\{r_i\}$. Each $x_i$ has neighbor-degree counts
  $(1,5,1)$, so $\epsilon_{x_i}=0$.
* The high graph is a matching with $m=4$ or $5$.
  A matched high sink has four six-neighbors, an isolated high sink
  has three, and each nonsink has five.
* The only two necessary low profiles are
  $V_6:2^4\,3^{10}\,4^2$, $V_7:1^{10}\,2^{16}$ for $m=4$, and
  $V_6:2^1\,3^{14}\,4^1$, $V_7:1^{14}\,2^{12}$ for $m=5$.
  Exponents denote numbers of vertices of each $c$ value.

The corrected identities specialize to

$$
 \sum_{v\in V_6\cup V_7}\epsilon_v=6,\qquad
 \sum_{v\in V_6\cup V_7}c(v)\epsilon_v=2m,\qquad
 |F(v)|=
 \begin{cases}
 9-\epsilon_v,&d(v)=6,\\
 4-\epsilon_v,&d(v)=7.
 \end{cases}                                                   \tag{1}
$$

In particular,

$$
 \sum_{v\in V_6\cup V_7}(c(v)-3)\epsilon_v=2m-18.               \tag{2}
$$

The exact pointwise identity, including the nonsink correction, is

$$
 (8-d(v))[t\in C(v)]
 +\sum_{u\in F(v)}[t\in C(u)]
 =8-d(v)+|F(t)\cap N(v)|.                                      \tag{3}
$$

It follows from the adjacency/distant-matrix commutator, as proved in
[z12_distant_incidence_bound.md](z12_distant_incidence_bound.md).
For a degree-seven vertex, its own high set and its far vertices'
high sets therefore **cover all twelve points**, possibly with
additional multiplicity at the two nonsinks. If their sizes sum to
twelve, they partition $T$ and the correction in (3) vanishes.

Distinct low vertices have high sets intersecting in at most one point:
two common high neighbors would give a four-cycle. In particular, distinct
vertices with $c\ge2$ have distinct high sets. A far pair has disjoint
high sets.

Call a seven-vertex **bad** when $(c,\epsilon)=(2,1)$, and let $b$
be their number. Such a vertex has exactly three far vertices.
It is not $x_1$ or $x_2$, so none of its far vertices is high.

## At least eight bad vertices in the five-edge case

Assume $m=5$. Let $q$ be the unique vertex with $c(q)=4$, and put
$Q=C(q)$. Every other low high set has size at most three.

On $V_6$, the local range $2c-8\le\epsilon\le c-2$ implies
$(c-3)\epsilon\ge0$ for $c=2,3,4$. On $V_7$, with $c=1,2$,
the only negative types are

$$
 (c,\epsilon)=(1,1),(2,1),(2,2).
$$

The first type has three far vertices and needs their high-set sizes
to sum to at least eleven by (3). Their maximum is $4+3+3=10$.
The last type has two far vertices and needs a sum at least ten;
their maximum is $4+3=7$. These negative types cannot be $x_i$,
since $\epsilon_{x_i}=0$, so their far sets contain only low vertices.
Both types are therefore impossible.

Thus the bad vertices supply the only negative contributions to (2),
each contributing $-1$. Since $2m-18=-8$,

$$
 b\ge8.                                                       \tag{4}
$$

For each bad vertex $y$, its three far vertices must have high-set sizes
at least ten in total. The only possible multiset is $4,3,3$.
Consequently

$$
 F(y)=\{q,u_y,v_y\},\qquad
 T=C(y)\ \dot\cup\ Q\ \dot\cup\ C(u_y)\ \dot\cup\ C(v_y),        \tag{5}
$$

where $u_y,v_y$ are degree-six vertices with $c=3$.
The union is disjoint because its sizes sum to twelve in (3).
In particular, every bad vertex determines a pair of disjoint triples
in $T\setminus Q$.

## At most five available triples, and at most three disjoint pairs

There are ten matched and two isolated high vertices. Each matched high
vertex has at least four six-neighbors; each isolated high vertex has
three. Therefore the four high points in $Q$ have at least

$$
 \sum_{t\in Q}|N(t)\cap V_6|\ge 2\cdot3+2\cdot4=14             \tag{6}
$$

six-incidences in total. The vertex $q$ accounts for four. Every other
six-vertex accounts for at most one, by the four-cycle restriction.
Hence at least ten distinct six-vertices other than $q$ meet $Q$.

There is just one $c=2$ six-vertex. At least nine of the fourteen
$c=3$ six-vertices must therefore meet $Q$. At most **five** of their
triples lie wholly in the eight-point set $T\setminus Q$.

We use the following elementary packing fact.

**Packing fact.** A family of at most five distinct three-subsets of an
eight-element set, any two intersecting in at most one point, has at most
three disjoint unordered pairs.

For a family of size $r\le3$ this follows from $\binom r2\le3$.
For $r=4,5$, let $I$ count its intersecting pairs. Since each nonempty
pairwise intersection has size one, the two-term union inequality gives

$$
 8\ge\left|\bigcup B_i\right|\ge3r-I.
$$

Thus the number of disjoint pairs is at most
$\binom r2-(3r-8)$, which is two for $r=4$ and three for $r=5$.

Finally the assignment $y\mapsto\{C(u_y),C(v_y)\}$ in (5) is injective.
The pair and $Q$ uniquely determine its complementary two-set $C(y)$.
Two distinct bad vertices with that same two-set would form a
four-cycle with its high points. Applying the packing fact gives

$$
 b\le3,
$$

contradicting (4). This proves the entire $m=5$ exclusion.

## The two four-sets in the remaining case must intersect

Now $m=4$, with two degree-six four-sets $Q_1=C(q_1)$ and $Q_2=C(q_2)$.
The preceding A2 proof's two-four-set argument shows that the
$(c,\epsilon)=(1,1)$ seven-type is absent: its presence would force
weighted negative contribution at most six, whereas (2) requires at
least ten. The same proof excludes $(2,2)$ throughout $A=2$.
Thus (2) gives $b\ge10$.

Suppose $Q_1$ and $Q_2$ were disjoint. A bad vertex cannot have three
far vertices all of $c\le3$, since their sum would be at most nine.
If its far set contained exactly one of $q_1,q_2$, its far sizes would
be $4,3,3$, and (3) would give a partition as in (5).
The other four-set is disjoint from the first one and intersects each
of the other three partition blocks in at most one point. It would
then have at most three points, a contradiction.

Every bad vertex is therefore far from **both** $q_1$ and $q_2$.
But $q_1$ has degree six and $c=4$, hence $\epsilon_{q_1}\ge0$ and
$|F(q_1)|=9-\epsilon_{q_1}\le9$. This gives $b\le9<10$.
So the two four-sets intersect, and their intersection has size exactly
one by the four-cycle restriction. No assumption about the class of
that common high neighbor is made.

## Reproduction, scope, and next case

The [standard-library checker](verify_a2_matching.py) verifies the local
sign and far-size cases, every allowed labeled placement of the unique
four-set in the high five-edge matching, and the disjoint-four-set
partition obstruction. It also enumerates **all 138,097 labeled linear
triple families of sizes zero through five on eight points**.

A bitset clique enumeration and a direct subset enumeration using Python
sets compare every family entry for entry. The family counts by size are
$1,56,1120,10080,42840,84000$. Their maximum disjoint-pair counts are
$0,0,1,2,2,3$. An abstract five-triple example attains three; it is not
an order-54 graph. No symmetry quotient, solver, external package, or
floating-point arithmetic is used by this checker.

Run from this directory with CPython 3.11 or later:

~~~sh
python3 verify_a2_matching.py > /tmp/order54-a2-matching.json
cmp /tmp/order54-a2-matching.json a2_matching_expected.json
python3 -O verify_a2_matching.py > /tmp/order54-a2-matching-O.json
cmp /tmp/order54-a2-matching-O.json a2_matching_expected.json
~~~

The [compact expected record](a2_matching_expected.json) records every
family count and stream hash. These controls support the human proof;
they do not enumerate all graphs or formally verify its graph-to-set bridge.
The imported A2 classification still depends on the 36 exact rational
certificates and checks specified in its own proof. The complete dependency
chain also imports the published order-53 bound. No prior SAT forest
exclusion is used in the new closing argument.

An initial full individual-incidence SAT pilot stopped at its 45-second
limit with unknown status. It supplied no mathematical conclusion. Its
restartable source and generated state are preserved in local scratch;
the proof above does not use that experiment.

The next unresolved case is the **entire $A=2,m=4$ subclass with the two
four-sets intersecting once**, with all remaining edges free. The
known two sink–nonsink–seven paths and the profile
$V_6:2^4\,3^{10}\,4^2$, $V_7:1^{10}\,2^{16}$ remain required.
Neither its realization nor its exclusion is asserted here.

Both normal and optimized checks passed with byte-identical output, SHA-256
edf2be5ad56a2830581887b36cbfb3e59124b871d124f0cdf6206ec26bc2a3db.
On CPython 3.11.2 they took 6.78 and 6.77 seconds, with peak resident
memory 39,888 KiB. The checks include 280 high four-set placements
and both intersection possibilities for the unique $c=2$ six-vertex,
as well as 280 disjoint-four-set partition candidates.
