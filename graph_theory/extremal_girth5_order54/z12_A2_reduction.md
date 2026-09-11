# Two missed high incidences force two specific paths

**Theorem.** Let $G$ be a finite simple graph with 54 vertices, 187 edges,
girth at least five, and twelve degree-eight vertices. Put
$T=V_8$, $F(v)=\{u:\operatorname{dist}(u,v)>2\}$,
$A=\sum_{t\in T}|F(t)|$, and $C(v)=N(v)\cap T$.
If $A=2$, then all the following hold.

* There are exactly two nonsinks $r_1,r_2\in T$. There are distinct
  degree-seven vertices $x_1,x_2$ such that
  $F(r_1)=\{x_2\}$, $F(r_2)=\{x_1\}$, and $C(x_i)=\{r_i\}$.
* Each $r_i$ has a unique high neighbor $p_i$, which is a sink.
  The six distinct vertices induce exactly two disjoint paths
  $p_1-r_1-x_1$ and $p_2-r_2-x_2$.
* Each $x_i$ has degree-class neighbor counts $(1,5,1)$ in degrees
  six, seven, eight. The corresponding counts at $r_i$ and $p_i$
  are $(5,2,1)$ and $(4,3,1)$.
* $H=G[T]$ is a matching of four or five edges. The complete low
  high-neighbor-count profiles are exactly the two rows below as a
  **necessary cover**. Neither row is asserted realizable.

| $m=e(H)$ | Degree-six $c=\lvert C(v)\rvert$ counts | Degree-seven $c$ counts |
|---|---|---|
| 4 | $2^4\,3^{10}\,4^2$ | $1^{10}\,2^{16}$ |
| 5 | $2^1\,3^{14}\,4^1$ | $1^{14}\,2^{12}$ |

The [preceding theorem](z12_A3_exclusion.md) gives $A\le2$.
Thus every surviving twelve-high-vertex candidate either has $A=0,1$,
or has the entire incidence structure just described. This result closes
all other $A=2$ configurations, including a distant high-high pair,
a single nonsink, shared missed endpoints, and every case with a
missed degree-six vertex. It **does not exclude all $A=2$ graphs** or the
whole $z=12$ subclass. The numerical interval remains
$185\le\operatorname{ex}(54,\{C_3,C_4\})\le187$.

There are 36 exact rational certificates: three integral prerequisites and
33 contradictions. The proof covers actual missed incidences before using
colored type relaxations. It assumes no automorphism, known-graph extension
base, or realizability of a type solution.

## Corrected identities and a fresh prerequisite

The degree reduction in [proof.md](proof.md), importing the published
order-53 upper bound 181, gives degree counts $(16,26,12)$. We use the
[corrected identities](z12_distant_incidence_bound.md). Write
$a_t=|F(t)|$, $h_t=d_H(t)$, $k=|\{t:h_t=2\}|$,
$\rho=\sum h_ta_t$, and $q$ for the number of distant unordered pairs
inside $T$. Let $p_7$ count distant high-to-seven pairs. Put
$s_v=\sum_{u\sim v}(d(u)-6)$, and
$\epsilon=s-8$ on $V_6$, $\epsilon=s-7$ on $V_7$.
For $A=2$,

$$
\begin{split}
 &h_t\le2,\quad a_t=5-s_t,\quad \rho\le2+k,\\
 &\sum_{V_6}c=38+2m,\quad \sum_{V_7}c=58-4m,\\
 &\sum\epsilon=6,\quad\sum c\epsilon=2m+\rho-p_7-4q,\\
 &\sum_{V_6}\phi_6(c)+\sum_{V_7}\phi_7(c)=6-m-k-q=:B,\\
 &\phi_6(c)=(c-3)(c-2)/2,\quad\phi_7(c)=(c-1)(c-2)/2,\\
 &Q+\sum_{t\in T}a_t(a_t+4)+2U=28,\\
 &Q=\sum_{V_6}\epsilon^2+\sum_{V_7}\epsilon(\epsilon-1),
 \quad U=\sum_{\{u,v\}\text{ distant}}(d(u)-6)(d(v)-6),\\
 &2U\ge4p_7+8q.
\end{split} \tag{1}
$$

All inventory terms are nonnegative integers. The local ranges are
$2c-8\le\epsilon\le c-2$ on six-vertices and
$2c-7\le\epsilon\le c$ on seven-vertices. Write
$P=\sum\max(\epsilon,0)$ and $N=\sum\max(-\epsilon,0)$ on low
vertices. Then $P=6+N\le6+Q$.
The only negative $(c-3)\epsilon$ types are seven-vertex types
$(c,\epsilon)=(1,1),(2,1),(2,2)$, with counts $b_1,b_2,b_{22}$.
Their weight $W=2b_1+b_2+2b_{22}$ obeys

$$
 W=18-2m-\rho+p_7+4q+
       \sum_{(c-3)\epsilon>0}(c-3)\epsilon. \tag{2}
$$

The first certificate is a **fresh $A=2$ computation**, on all 72
ordinary degree/neighbor-count types and 1,638 admissible type-edge columns
in [forest_constraints.py](forest_constraints.py). Only $A=2$ is added
to that ordinary model. It proves

$$
 m\ge65040081/50000000>1,\qquad\text{hence }m\ge2. \tag{3}
$$

Neither the $A=3$ nor the $A=4$ numerical certificate is transferred.
Consequently $B\le4$. In particular, no high-neighbor set exceeds five,
a five-set can only be a six-vertex and costs three units, and two five-sets
are impossible. Type $(2,2)$ needs two distant high-neighbor sets with
sum of sizes at least ten, while the inventory allows at most $5+4=9$.
Thus **$b_{22}=0$** throughout the proof.

## Individual covers and the distant high-high case

The actual vertex identity is

$$
 (8-d(v))[t\in C(v)]+\sum_{u\in F(v)}[t\in C(u)]
 =8-d(v)+|F(t)\cap N(v)|. \tag{4}
$$

It follows from the adjacency/distant-matrix commutator
$[\mathcal A,\mathcal F]_{uv}=(d(u)-d(v))(1-\mathcal A_{uv})$.
A seven-vertex's own set and its distant vertices' sets cover $T$.
Distinct vertices' sets intersect in at most one point; distant vertices'
sets are disjoint. A $(1,1)$ vertex has three far vertices and needs total
far-set size at least eleven; a $(2,1)$ vertex needs at least ten.

We use the two- and three-four-set arguments proved in the preceding work.
With exactly two size-four sets, both at six-vertices, a $(1,1)$ vertex
forces a $1+4+4+3$ partition. All such vertices then have the same singleton
$p$ and far triple. Their number is at most
$\min(2+a_p,5-a_p)\le3$. The intersection bound forbids every $(2,1)$
vertex in their presence, including covers with the correction in (4).
Thus $b_1>0$ would give $W\le6$. With exactly three six-vertex four-sets
and no larger set, the three-set intersection argument instead gives
$b_1\le3$. These are statements about individual sets. Their use below
always checks the inventory and the needed lower bound on $W$.

Suppose $q=1$. Both nonsinks have deficit one and miss each other.
For a high sink $s$, the high/high commutator gives
$N(s)\cap F(t)=\varnothing$. Thus neither nonsink has a high neighbor,
so $\rho=0$, $p_7=0$, $Q\le10$, and

$$
 B=5-m-k,\qquad W\ge22-2m,\qquad P\le16. \tag{5}
$$

A six-vertex five-set would force $m=2,k=0,B=3$. It has at most seven
far vertices and is required by every negative type, giving $W\le14$,
while its own positive contribution is at least four, giving $W\ge22$.
A seven-vertex four-set similarly exhausts the inventory: it has at most
three far vertices, no $(1,1)$ can be covered, and $W\le3$.
Both are impossible. All remaining four-sets belong to six-vertices;
let their number be $f$. They have at most nine far vertices each, hence
$W\le9f\le9B$. This contradicts (5) for $m\ge4$, and requires
$f\ge2$ for $m=2,3$.

If $f=2$, the preceding partition argument forces $b_1=0$.
For $m=2$, $W=b_2\ge18>P$. For $m=3$, necessarily $k=0$, and
$W=b_2=P=16$, $N=Q=10$. Equality in (2) forces every positive
$(c-3)\epsilon$ contribution to vanish. Equality $N=Q$ permits
negative epsilon only at six-vertices with $\epsilon=-1$, and vanishing
positive contribution forces $c=3$. Hence ten such vertices are needed.
But inventory and the high/six handshake give only eight $c=3$ six-vertices.

If $f=3$, then $m=2,k=0$. The same handshakes give only two $c=1$
seven-vertices, so $b_1\le2$. Now $18\le W\le P+b_1\le18$.
Again $N=Q=10$ and (2) has no positive term, requiring ten negative
$c=3$ six-vertices, whereas this profile has only four. This proves
**$q=0$**, with no solver status used for the closing argument.

## Complete cover of the two missed incidences

Let $R=\{t:a_t>0\}$, $S=T\setminus R$, and
$X=\bigcup_{t\in R}F(t)$. Now $X\subset V_6\cup V_7$.
The high/high commutator with any $s\in S$ gives

$$
 C(x)\subset R\quad(x\in X),\qquad
 |N(t)\cap F(u)|=|N(u)\cap F(t)|\quad(t,u\in R). \tag{6}
$$

The complete possibilities are these four families.

| Family | Nonsinks and missed endpoints | Forced incidences |
|---|---|---|
| `one` | One nonsink misses two distinct vertices | Every endpoint has $c=0$ |
| `shared` | Two unit-deficit nonsinks miss one common vertex | The endpoint has $c=0$ |
| `zero` | Two unit-deficit nonsinks miss distinct vertices | Both endpoints have $c=0$ |
| `matching` | Two unit-deficit nonsinks miss distinct vertices | $r_1x_1,r_2x_2$ are edges, $F(r_1)=\{x_2\}$, $F(r_2)=\{x_1\}$ |

For distinct endpoints, (6) makes the two possible cross-adjacency bits equal.
In the last family $R$ and $X$ are independent. Moreover **no vertex
outside $R\cup X$ can have both an $R$-neighbor and an $X$-neighbor**:
the relevant pair is either an actual edge, producing a triangle, or a
prescribed far pair, producing a forbidden two-step path.

An independent exact enumeration checks every identification of the two far
slots, all degree-six/seven assignments, and all possible edges in the small
core. It finds 33 labeled cases: one high-high case, eight `one`, four
`shared`, sixteen `zero`, and four `matching`. No graph automorphism is
assumed. The merged color models below contain every labeling, without
fixing edges within $R$ or within $X$ in the first three families.

For `one` and `zero`, the number $p$ of degree-seven endpoints is
$0,1,2$; for `shared` it is $0,1$. Eight exact certificates exclude
these entire families. Shared endpoints are counted twice in $p_7$.
Every survivor is therefore in the `matching` family, with $p_7=p$.

## Complete matching-profile cover and its individual bounds

Here $R$ consists of two nonadjacent unit-deficit vertices, and each
endpoint has $c=1$. Thus

$$
 \rho\le\min(m,2+k),\qquad Q\le18-4p,\qquad B=6-m-k. \tag{7}
$$

The high graph has maximum degree two and contains no cycle: a cycle would
have length at least five and already contribute at least ten to $m+k\le6$.
Consequently $2\le m\le6$, $0\le k\le m-1$.
The only nonzero-inventory low types that can occur are

$$
 (6,0),(6,1),(6,4),(6,5),(7,0),(7,3),(7,4),
$$

of costs $3,1,1,3,1,1,3$. Their total cost is $6-m-k\le4$.
The zero-cost types are $(6,2),(6,3),(7,1),(7,2)$.
At least $2-p$ six-vertices have $c=1$; at least $p$ seven-vertices
have $c=1$. Enumerating the charged multiplicities and solving the degree
and high-neighbor handshakes gives respectively **16, 40, 94** profiles
for $p=0,1,2$. The checker independently obtains the same cover by
multisets of charged types and direct integer handshake tests.

Write $n_{dc}$ for the profile multiplicities, $n_5=n_{65}$,
$n_4=n_{64}$, and $n_{74}$ as usual. Each six-vertex four-set can
support at most nine far incidences, a seven-vertex four-set at most three,
and a six-vertex five-set at most seven. If no five-set occurs, each
$(1,1)$ needs two four-sets and each $(2,1)$ one. If a five-set occurs,
it is unique and at most one other four-set is allowed; every $(1,1)$
must be far from the five-set. Therefore

$$
 W\le14n_5+9n_4+3n_{74}. \tag{8}
$$

Let $b^*$ bound $b_1$. Start with $b^*=n_{71}$; cap it at seven
when a five-set occurs. Without a five-set, set it to zero if fewer than
two four-sets occur. With exactly two six-vertex four-sets and no seven
four-set, also set it to zero: the partition argument would otherwise give
$W\le6$, while (2), $m+k\le4$, and $\rho\le2+k$ give $W\ge8$.
With exactly three six-vertex four-sets and no seven four-set, cap it at three.
Four four-sets are allowed; no three-set lemma is applied to that case.

A lower bound on the positive term of (2), computed separately for every
profile, is

$$
 L_+=\sum_{c<2}n_{6c}(c-3)(c-2)
 +\sum_{c\ge4}n_{6c}(c-3)(2c-8)
 +\sum_{c\ge4}n_{7c}(c-3)(2c-7). \tag{9}
$$

Every profile must satisfy

$$
 18-2m-\min(m,2+k)+p+L_+
 \le W\le
 \min(14n_5+9n_4+3n_{74},\ 24-4p+b^*,\ 2b^*+n_{72}). \tag{10}
$$

These integer inequalities remove 127 profiles. Exactly $1,5,17$ remain
for $p=0,1,2$. Their complete records are reconstructed by the checker;
21 exact colored-model refutations leave precisely the two theorem rows,
both with $p=2$, $k=0$, and $m=4,5$. This is complete profile coverage,
not a selection of favorable histograms.

## Graph meaning of the colored models

[a2_models.py](a2_models.py) uses classes $B_6,B_7,S,R,X_6,X_7$, omitting
empty endpoint classes. If $r=|R|$, $x=|X|$, and $p=|X_7|$, their
sizes are $(16-x+p,26-p,12-r,r,x-p,p)$, with their indicated degrees.
A type records its class and full vector $\nu$ of neighbor counts in these
classes. Types respect class sizes and neighbor-degree sum at most 53.
An $S$-type has neighbor-degree sum 53 and no $X$-neighbor; an $R$-type
has sum 51 for `one` and 52 otherwise. Endpoints have no $S$-neighbor.
The exact $R$-to-$X$ counts and the last family's independence/mixed-neighbor
restriction are imposed before enumerating types. A specified profile
permits only its listed low $(d,c)$ types.

For each type $\tau$, $X_\tau$ counts vertices. $Y_{\tau\sigma}$
counts edges between distinct types; diagonal variables count internal edges
twice. Variables are nonnegative. We impose class totals, class handshakes,
exact type-to-class neighbor balances, and class-pair edge-plus-two-path
capacities. Diagonal pair capacities are doubled. These are necessary
constraints of every graph, with no converse asserted.

For a root of class $i$, the individual class-ball identity is

$$
 \sum_{u\sim v}\nu_j(u)+\nu_j(v)
 =n_j+(d(v)-1)[i=j]-|F(v)\cap\text{class }j|. \tag{11}
$$

Use equality whenever the missed-class count is known; otherwise use its
nonnegativity. Every root misses zero $S$-vertices. Non-endpoints miss zero
$R$-vertices; an endpoint misses one, except in `shared`, when it misses
both. An $S$-root misses nothing. An $R$-root misses no bulk, $S$, or
$R$ vertex. In `one` and `shared` it misses all endpoints. In `matching`
it misses exactly the endpoints to which it is not adjacent, so the missed
count in endpoint class $j$ is $n_j-\nu_j$. In `zero` this exact
endpoint-class count is used when the endpoints have the same degree;
otherwise the separate upper inequalities suffice.

Summing (11) over a type gives linear rows in $X,Y$. The models also impose
(1), the appropriate gap upper bound, and (3). Matching-profile cases add
$m,k$, the full profile, $b_{22}=0$, (8), and the stated $b_1$ bounds.
Every removed type is forbidden by proved hypotheses. Every column that
remains, including types subsequently forced to zero by an explicit upper
row, participates in the exact certificate check.

## High partners and endpoint degrees

In either surviving row $H$ is a matching, so the two nonsinks have
$h\in\{0,1\}$ and $\rho\in\{0,1,2\}$. Three additional exact
certificates exclude $(m,\rho)=(4,0),(5,0),(5,1)$ by adding just the
equality for the total high degree of $R$ to the corresponding colored model.

For $(m,\rho)=(4,1)$, distinguish the paired nonsink $r_1$, its high
partner $p_1$, the isolated nonsink $r_2$, and the two endpoints.
Their induced core has only $r_1x_1,r_2x_2,r_1p_1$.
The remaining nine high vertices are sinks. None is adjacent to the core:
all high degrees in the core have already been supplied, and no sink meets
an endpoint. This statement fixes only edges forced by the matching.

[a2_partner_model.py](a2_partner_model.py) uses singleton classes for these
five vertices, plus the remaining six-, seven-, and high-sink classes.
Core adjacencies and neighbor-degree sums are fixed. A type cannot have both
ends of a core edge or a prescribed far pair as neighbors. If two core
vertices already have a common core neighbor, no other vertex can be a common
neighbor. In particular $p_1,x_1$ already share $r_1$, a constraint
invisible in a single undifferentiated sink class. All rows of (11) with a
high root or high target are now exact, using each specified far relation.
The low profile, (1), and $m=4$ are imposed as before. An exact certificate
with margin $11339571/50000000>0$ excludes this entire incidence case.
Thus **$\rho=2$** in both surviving rows, proving the two high partners.

Finally $b_1=0$ in these rows. At a seven-endpoint with $c=1$, this gives
$\epsilon\le0$. If $a_x=|N(x)\cap V_6|$, the degree counts give
$\epsilon_x=1-a_x$, hence $a_x\ge1$. With $\rho=2$, two exact
objective certificates give

$$
 \sum_{x\in X}(2-a_x)\ge
 \begin{cases}
 161601/125000>1,&m=4,\\
 159994449/100000000>1,&m=5.
 \end{cases} \tag{12}
$$

There are two endpoints, so the integer sum $a_{x_1}+a_{x_2}<3$.
Both summands are at least one, proving $a_{x_1}=a_{x_2}=1$, and the
remaining five neighbors at each endpoint have degree seven. The other
neighbor counts in the theorem follow from the high local counts
$(3+a_t+h_t,5-a_t-2h_t,h_t)$. This completes the necessary classification.

## Exact evidence, reproduction, and remaining work

[generate_a2_certificates.py](generate_a2_certificates.py) regenerates the
36 certificates with CPython 3.11.2, NumPy 2.4.6 and SciPy 1.15.3; the pinned
requirements are [requirements-a3.txt](requirements-a3.txt). It uses the
published generic dual-construction helper in
[generate_a3_certificates.py](generate_a3_certificates.py).
[verify_a2.py](verify_a2.py) needs only the Python standard library.
The [compact expected record](a2_expected.json) contains every exact bound,
case dimension, certificate hash, and the coverage and control summaries.

For equality multipliers of either sign and nonpositive upper-row multipliers,
let $c$ be the combined column vector and $b$ the combined right side.
If $o$ is the objective vector, put
$\delta=\max(0,\max_i(c_i-o_i))$. Every graph has
$\sum X+\sum Y\le54+374=428$, so $o\cdot(X,Y)\ge b-428\delta$.
Contradictions use $o=0$ and a strictly positive corrected bound. The
$m$ and endpoint objectives require a corrected bound strictly greater
than one. All half-integral model coefficients are doubled and accumulated
with Python integers; floating infeasibility reports never establish a claim.

From this directory, with generated state outside Git:

```sh
python3 -m venv /tmp/order54-a2-env
/tmp/order54-a2-env/bin/pip install -r requirements-a3.txt
/tmp/order54-a2-env/bin/python generate_a2_certificates.py --output /tmp/order54-a2.json
python3 verify_a2.py --certificates /tmp/order54-a2.json > /tmp/order54-a2-check.json
cmp /tmp/order54-a2-check.json a2_expected.json
python3 -O verify_a2.py --certificates /tmp/order54-a2.json > /tmp/order54-a2-check-O.json
cmp /tmp/order54-a2-check-O.json a2_expected.json
```

The generated bundle remains in scratch. Public source and compact expected
results reproduce it; no bulky solver output or binary is published. The
checker independently enumerates types by neighbor multisets and reconstructs
rows from incident edges. It also independently enumerates charged profiles,
all 33 far-core cases, the high-high terminal equalities, and the elementary
endpoint integrality step; four corrupted certificates must be rejected.
Inherited individual-set controls cover 294 three-four-set configurations
and 349 singleton templates. Generic colored identities are checked on 354
actual graphs with 6,766 class-ball equations. Those controls are not new
187-edge witnesses or a substitute for the written graph-to-model proof.

The prior $A\le3$ theorem received an independent acceptance review at
Discovery Net height 4361. An independent review of the subsequent $A=3$
exclusion also accepted its stated scope; neither review certifies this new
classification.
Its reported form-feed typo before `frac12` was repaired without changing
mathematics. Trust in this result remains in the imported order-53 bound,
the corrected identities and written reductions, exact but unformalized
Python, and hardware. The independent model implementations share their
mathematical premises. Historical priority is not established.

The [primary catalogue](https://users.cecs.anu.edu.au/~bdm/data/extremal.html)
and the [2025 primary paper](https://arxiv.org/html/2508.05562v1) supply the
working numerical frontier. The remaining two configurations still need a
realization decision. Pilot relaxations with individually distinguished high
partners and the now-forced endpoint degrees remain feasible numerically;
this is only exploratory evidence and supplies neither a graph nor an exact
relaxation witness. The next phase should assign the actual remaining
incidences, beginning with these two fully specified high-matching subclasses.

## Recorded regeneration and exact check

All 36 certificates regenerated from the delivered source matched the pilot
records entry for entry. Regeneration took 299.37 seconds, with peak
resident memory 255,356 KiB. The normal and optimized verifier
runs both passed and gave byte-identical output, SHA-256
`668f28e49e111c53bc3a0657b093e971c2c699c46d5d1a2981ed44935369f7b5`.

The independent reconstruction checks 35 colored models and
394,084 colored case-columns, plus the ordinary 1,710-column
prerequisite. The generated bundle is 2,675,046 bytes and remains
outside Git. The public expected record is compact and contains all 36
individual certificate hashes and corrected bounds.
