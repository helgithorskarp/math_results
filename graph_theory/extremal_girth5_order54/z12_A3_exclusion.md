# Three high distant incidences are impossible at order 54

**Theorem.** A finite simple graph on 54 vertices, with 187 edges, girth at
least five, and exactly twelve degree-eight vertices cannot satisfy

$$
 A=\sum_{t\in V_8}|F(t)|=3,
 \qquad F(t)=\{v:\operatorname{dist}(t,v)>2\}.
$$

Together with the [preceding theorem](z12_distant_incidence_bound.md), this
proves **$A\le2$** and **at least ten of the twelve high vertices are
sinks**: each sink has every vertex within distance two. The unrestricted numerical interval remains
$185\le\operatorname{ex}(54,\{C_3,C_4\})\le187$. The cases $A=0,1,2$
and the whole twelve-high-vertex subclass remain open.

This is an exact computer-assisted exclusion of the entire $A=3$
subclass. A commutator classifies the individual high-to-missed incidences.
The last possibilities are a shared missed vertex and a forced six-cycle.
Fourteen regenerated rational certificates close all cases, with every
coefficient checked exactly. No automorphism of the full graph, known-graph
extension base, or previous SAT forest exclusion is assumed.

## Identities and the first reduction

The degree reduction in [proof.md](proof.md) imports the published
order-53 upper bound 181 and gives degree counts $(16,26,12)$.
Keep the corrected identities of the preceding theorem. Put $T=V_8$,
$H=G[T]$, $m=e(H)$, $h_t=d_H(t)$, $k=|\{t:h_t=2\}|$,
$a_t=|F(t)|$, and $\rho=\sum h_ta_t$. Let $q$ count distant
pairs inside $T$, and $p_7$ distant pairs between $T$ and $V_7$.
Write $C(v)=N(v)\cap T$, $c(v)=|C(v)|$,
$s_v=\sum_{u\sim v}(d(u)-6)$, and $\epsilon=s-8$ on $V_6$,
$\epsilon=s-7$ on $V_7$. Under $A=3$,

$$
\begin{split}
 &h_t\le2,\quad a_t=5-s_t,\quad \rho\le3+k,\\
 &\sum\epsilon=7,\quad\sum c\epsilon=2m+\rho-p_7-4q,\\
 &\sum_{V_6}\phi_6(c)+\sum_{V_7}\phi_7(c)=5-m-k-q=:B,\\
 &\phi_6(c)=\frac{(c-3)(c-2)}2,\quad
 \phi_7(c)=\frac{(c-1)(c-2)}2,\\
 &Q+\sum a_t(a_t+4)+2U=28,\quad
 Q=\sum_{V_6}\epsilon^2+\sum_{V_7}\epsilon(\epsilon-1),\quad
 2U\ge4p_7+8q.
\end{split} \tag{1}
$$

For degree six, $2c-8\le\epsilon\le c-2$ and $|F(v)|=9-\epsilon$; for degree seven, $2c-7\le\epsilon\le c$ and $|F(v)|=4-\epsilon$.

Here $U=\sum_{\{u,v\}\text{ distant}}(d(u)-6)(d(v)-6)$. All inventory terms are nonnegative integers. With
$P=\sum\max(\epsilon,0)$, $N=\sum\max(-\epsilon,0)$, we have
$P=7+N\le7+Q$. The only negative $(c-3)\epsilon$ types are the
seven-vertex types $(c,\epsilon)=(1,1),(2,1),(2,2)$. Denote their
numbers by $b_1,b_2,b_{22}$. Their negative weight satisfies

$$
 W=2b_1+b_2+2b_{22}\ge21-2m-\rho+p_7+4q. \tag{2}
$$

For every high $t$ and every $v$, the individual identity is

$$
 (8-d(v))[t\in C(v)]+\sum_{u\in F(v)}[t\in C(u)]
 =8-d(v)+|F(t)\cap N(v)|. \tag{3}
$$

It follows from the high/low entry of
$[\mathcal A,\mathcal F]_{uv}=(d(u)-d(v))(1-\mathcal A_{uv})$,
where $\mathcal A$ is adjacency and $\mathcal F$ the distant-pair
matrix. In particular the high-neighbor sets at a seven-vertex and its
far vertices cover $T$; total size twelve forces a partition. Distinct
vertices' high-neighbor sets intersect in at most one point, and distant
vertices' sets are disjoint. These are individual constraints, not just
counts of the sizes of neighborhoods.

The first new certificate, `m_at_A3`, uses all 72 degree/neighbor-count
types in [forest_constraints.py](forest_constraints.py), class sizes
$(16,26,12)$, and only the additional equality $A=3$. It yields

$$
 m\ge\frac{20075113}{12500000}>1. \tag{4}
$$

Thus $m\ge2$ and $B\le3$. This is a fresh certificate; the earlier
one conditional on $A=4$ is not used.

A six-vertex with $c=5$ would consume all three inventory units, forcing
$m=2,k=q=0$ and leaving no other set of size at least four. Every negative
type $(1,1)$ or $(2,1)$ must be far from that vertex. It has at most
seven far vertices, giving $W\le14$. But its own positive
$(c-3)\epsilon\ge4$, together with (2) and $\rho\le3$, gives
$W\ge18$. A seven-vertex with $c=4$ likewise consumes the inventory;
it has at most three far vertices. Type $(1,1)$ cannot obtain the required
eleven high neighbors from it and two sets of size at most three; type
$(2,1)$ must be far from it. Thus $W\le3$, below (2).
Larger sets are prohibited by their inventory costs. Also $(2,2)$ is
impossible: two distant sets cannot have total size at least ten when the
inventory permits at most one five-set and no accompanying four-set.

Consequently every set of size four belongs to a six-vertex, all other
sets have size at most three, and $b_{22}=0$. Write $f$ for the number
of four-sets. Each such six-vertex has at most nine far vertices. Each
$(1,1)$ requires at least two far four-sets, and each $(2,1)$ at least
one, so $W\le9f\le9B$. For $m\ge4$, the lower bound
$W\ge18-2m-k+p_7+4q$ exceeds $9B$; the difference, even dropping
$p_7$, is $7m+8k+13q-27>0$. Hence $m\le3$.
For $m=2,3$, that lower bound exceeds nine throughout the allowed
inventory range. Therefore $f\ge2$. We have proved

$$
 m\in\{2,3\},\quad m+k+q\le3,\quad 2\le f\le3. \tag{5}
$$

## A bound from two or three individual four-sets

We need the uniform bound **$b_1\le3$**, and **$b_1=0$ when $f=2$**.
With exactly two four-sets, a $(1,1)$ vertex has distant sizes $4,4,3$,
so its own singleton completes a partition of $T$. The four-sets are
disjoint. Inside their four-point complement, the far triple is the
complement of the singleton. Different singletons give triples intersecting
in two points, so all such vertices share one high neighbor $p$ and one
far triple. For any common far four-vertex, (3) bounds their number by
$2+a_p$. The number of seven-neighbors of $p$ is at most $5-a_p$.
Thus $b_1\le\min(2+a_p,5-a_p)\le3$.

If a $(2,1)$ vertex is far from just one of those disjoint four-sets,
its other far sets must be triples. Its pair and those triples cannot
cover the other four-set: each intersects it in at most one point.
If it is far from both, its own pair lies in the four-point complement
and must contain $p$, to avoid a two-point intersection with the fixed
triple. Its third far set must then contain the remaining two points of
that triple, again a forbidden intersection. This last argument permits
extra coverage in (3), not just partitions. Hence $b_1>0$ would imply
$b_2=0$ and $W\le6$, contradicting (2),(5). Therefore $b_1=0$.

With three four-sets, a $(1,1)$ vertex uses either two of them and a
triple, or all three. In the first case the chosen pair is disjoint.
The unused four-set must meet each chosen set once and their complement
twice, one of those latter points being the singleton $p$. Thus the
intersection graph of the three four-sets is a path, with a unique
disjoint pair. Different choices of $p$ again yield incompatible triples.
In the second case the three four-sets have union eleven, with $p$
outside it. Their intersection graph has exactly one edge. These two
intersection patterns cannot coexist. All $(1,1)$ vertices consequently
share a fixed $p$ and a fixed far four-vertex, giving the same bound three.

The checker independently examines 294 normalized configurations of three
four-sets and all 349 possible singleton templates. For two four-sets it
reuses the separately enumerated partition/cover controls from the preceding
proof. No automorphism of $G$ is assumed by normalizing these small sets.

Since $A=3$, $q\le1$. If $q=1$, (5) forces $m=2,k=0,f=2$.
Then $b_1=0$, $W=b_2\ge18+p_7$, whereas (1) gives
$b_2\le P\le12-4p_7$. Thus **$q=0$**.

## Complete cover of the missed-vertex incidences

Let $R=\{t\in T:a_t>0\}$, $S=T\setminus R$, and
$X=\bigcup_{t\in R}F(t)$. As $q=0$, $X\subset V_6\cup V_7$.
The high/high commutator with a sink $s\in S$ gives
$N(s)\cap F(t)=\varnothing$. Therefore

$$
 C(x)\subset R\quad(x\in X). \tag{6}
$$

The possible positive deficit lists are $(3),(2,1),(1,1,1)$. To cover
all incidences, create three far slots with those owners, partition the
slots into the distinct vertices $X$, and require that slots of the same
owner lie in distinct parts. First-occurrence labels give a canonical
naming of $X$, without assuming symmetry of the graph. Enumerate every
possible $R$-to-$X$ edge, excluding the prescribed far pairs. The
high/high entries of the commutator require

$$
 \sum_{x\in F(u)}[t\sim x]=\sum_{x\in F(t)}[u\sim x]
 \quad(t,u\in R). \tag{7}
$$

Also two distinct $X$-vertices cannot have two common high neighbors.
There are exactly 21 resulting labeled incidence frames and 130 assignments
of degrees six/seven to their $X$-vertices. This is a complete tiny cover,
not a sample or a search restricted to selected high forests.

For clarity, the additional exact filters in this cover are as follows.
For each $(m,k)\in\{(2,0),(2,1),(3,0)\}$ and $f=2,3$, require

$$
\begin{split}
 &f+\sum_{x\in X}\phi_{d(x)}(c(x))\le5-m-k,\\
 &Q_*=28-\sum a_t(a_t+4)-4p_7
       \ge\sum_{x\in X\cap V_6}(2-c(x))^2,\\
 &21-2m-\rho_*+p_7+
       \sum_{x\in X\cap V_6}(c(x)-3)(c(x)-2)
       \le7+Q_*+\begin{cases}0&f=2,\\3&f=3.\end{cases}
\end{split} \tag{8}
$$

Here $c(x)\le|R|-1\le2$. The first inequality pays the inventory of
distinct endpoints. The second uses their minimum six-vertex gap costs.
In the third, the six-endpoint sum is a lower bound on their positive
$(c-3)\epsilon$ contribution, while $W\le P+b_1\le7+Q_*+b_1$.
Usually $\rho_*=3+k$. If all three deficits are one and the frame forces
$R$ independent, use $\rho_*=m$: every edge of $H$ has at most one
endpoint in $R$. Independence is certified for a pair either by a common
$X$-neighbor (an edge would make a triangle), or by a two-step path from
a prescribed far pair (an edge would destroy that far relation).

The checker tests all 780 such bounded cases, with exact integers. Precisely
19 labeled cases survive; they have the following two forms. The table and
the rules above specify the full computation-to-graph implication.

| Form | Far sets and actual high-neighbor sets | Remaining degrees and high graph |
|---|---|---|
| Shared endpoint | $F(t_1)=F(t_2)=\{x\}, F(t_3)=\{y\}$; $C(x)=\{t_3\}, C(y)=\{t_1,t_2\}$ | $d(x)=d(y)=6$, $m=2,k=0,f=2$; $R$ independent |
| Six-cycle | Three distinct $x_i$, $F(t_i)=\{x_i\}$, $C(x_i)=R\setminus\{t_i\}$ | All $x_i$ have degree six, or exactly one has degree seven; $R$ independent |

Thus there are exactly three nonsinks, each with one missed vertex, in
every surviving frame. In the six-cycle form, the bipartite graph on
$R\cup X$ is $K_{3,3}$ minus a perfect matching, hence a six-cycle.
The shared endpoint has three labeled versions in the bounded cover; the
six-cycle forms have respectively four and twelve, including the choices
of $(m,k,f)$. Multiplicity in this necessary cover is harmless.

One can also see the pruning directly. A degree-six endpoint with $c=0$
costs three inventory units; a seven-endpoint with $c=0$ costs one, and
a six-endpoint with $c=1$ costs one. Only one unit can remain after the
two four-sets. Repeated far endpoints and the low-degree possibilities
therefore eliminate most frames. In the independent, all-unit-deficit
frames, two or more high-to-seven far incidences contradict
$W\ge21-3m+p_7$ and $W\le20-4p_7+b_1$. The finite cover retains all
boundary equalities, both vertex degrees, and shared endpoints.

## The shared endpoint and the complete low-profile list

In the shared form the $c=1$ six-vertex spends the last inventory unit.
The two handshakes
$\sum_{V_6}c=39+2m$, $\sum_{V_7}c=57-4m$ force profile `six1` below.
Here entries are multiplicities at the indicated $c$, within each degree.
The zero-inventory values are $c=2,3$ for degree six and $c=1,2$ for
seven; the only other single-unit types are $(6,1),(7,0),(7,3)$.
These facts enumerate the **complete six-profile cover** for the six-cycle:

| Name | $m,k$ | Degree-six $c$-profile | Degree-seven $c$-profile |
|---|---|---|---|
| six1 | 2,0 | $1^1 2^5 3^8 4^2$ | $1^3 2^{23}$ |
| threefour | 2,0 | $2^8 3^5 4^3$ | $1^3 2^{23}$ |
| sev0 | 2,0 | $2^7 3^7 4^2$ | $0^1 1^1 2^{24}$ |
| sev3 | 2,0 | $2^7 3^7 4^2$ | $1^4 2^{21}3^1$ |
| P3 | 2,1 | $2^7 3^7 4^2$ | $1^3 2^{23}$ |
| 3P2 | 3,0 | $2^5 3^9 4^2$ | $1^7 2^{19}$ |

Certificate `shared_six_endpoint` refutes the ordinary degree-type model
with profile `six1`, high degree counts $8,4,0$ at $h=0,1,2$,
high $s\in\{4,5\}$, $A=3$, $\rho\le2$, $b_1=b_{22}=0$.
It has exact contradiction margin $572223/100000000>0$. All these
conditions were proved above; no unproved ordinary-edge placement is fixed.

## The six-cycle attachment model and its graph meaning

Put $p=|X\cap V_7|\in\{0,1\}$. Partition the actual vertices into

$$
 (B_6,B_7,S,R,X_6,X_7),\qquad
 (|B_6|,|B_7|,|S|,|R|,|X_6|,|X_7|)
 =(13+p,26-p,9,3,3-p,p).
$$

Omit the empty last class when $p=0$. Their degrees are respectively
$6,7,8,8,6,7$. The following type restrictions follow from the actual
six-cycle, triangle/quadrilateral exclusion, and the far sets:

- $R$ and $X$ are independent, and every vertex of either has two
  neighbors in the other. No vertex of $X$ has a neighbor in $S$.
- Every vertex outside $X$ has at most one $R$-neighbor, except the
  already specified $R$-vertices, which have none. Indeed every pair
  of $R$-vertices already has its unique common neighbor in $X$.
- Every vertex outside $R$ has at most one $X$-neighbor; the vertices
  in $X$ have none. Every pair in $X$ already has a common neighbor in $R$.
- An $S$-vertex has neighbor-degree sum 53, and an $R$-vertex has
  neighbor-degree sum 52. Every type has neighbor-degree sum at most 53.

A type consists of its class $i$ and its entire vector $\nu$ of
neighbor counts in these classes. Enumerate all nonnegative integer
vectors of sum $d_i$, respecting the class sizes, the displayed
restrictions, the selected low profile, and the already excluded type
$(7,c=2,\epsilon=2)$. This covers every vertex type in a possible graph.

As before, $X_\tau$ counts vertices of type $\tau$; $Y_{\tau\sigma}$
counts edges between distinct types, and counts internal edges twice on
the diagonal. All variables are nonnegative. Class totals, class handshakes,
and the neighbor-type totals at each type are equalities. All class-pair
edge-plus-two-path capacities are upper inequalities. Diagonal capacities
are doubled, so their right sides are $n_i(n_i-1)$; off-diagonal right
sides are $n_in_j$.

For a vertex $v$ of type $\tau=(i,\nu)$, the exact class-ball identity is

$$
 \sum_{u\sim v}\nu_j(u)+\nu_j
 =n_j+(d_i-1)[i=j]-|F(v)\cap\text{class }j|. \tag{9}
$$

When the last term is unknown we use its nonnegativity. Its exact value
is known in these cases, and the model imposes the corresponding equality:

| Root type | Target class | Number missed |
|---|---|---|
| Any | $S$ | 0 |
| Any outside $X$ | $R$ | 0 |
| $X$ | $R$ | 1 |
| $S$ | Every class | 0 |
| $R$ | $B_6,B_7,S,R$ | 0 |

These are genuine individual-incidence constraints before summing over a
type. In particular a neighbor of an $X$-vertex outside $R$ cannot
supply another short path to $R$. Omitting these equalities leaves
feasible coarser relaxations; they are consequential to the new proof.
Finally impose the selected low profile, $m,k$, and $b_1=0$ for two
four-sets or $b_1\le3$ for three. No graph realization of a feasible
relaxation is asserted or needed.

The twelve cases $p\in\{0,1\}$ times the six profiles are all exactly
infeasible. This covers every attachment to the six-cycle, not merely
selected aggregate witnesses. The shared and six-cycle exclusions finish
all frames, proving $A\ne3$.

## Exact certificates, reproduction, and trust

[a3_models.py](a3_models.py) defines the fourteen necessary instances.
[generate_a3_certificates.py](generate_a3_certificates.py) regenerates
rational multipliers, and [verify_a3.py](verify_a3.py) checks them with
integer arithmetic. For each contradiction, unrestricted equality
multipliers and nonpositive upper-inequality multipliers give coefficient
vector $c$ and right side $b$. With
$\delta=\max(0,\max c_i)$, the nonnegative-variable budget
$\sum X+\sum Y\le54+374=428$ proves a contradiction whenever
$b-428\delta>0$. For `m_at_A3`, replace $c_i$ by its excess over the
objective coefficient for $m$, and require $b-428\delta>1$.
Every column is included. Shared-case zero-type restrictions are explicit
upper rows, not silently discarded columns.

All multipliers have denominator $10^8$. Model coefficients are integers
or half-integers. The verifier doubles them and performs all accumulated
column arithmetic with Python integers; only final display uses rational
fractions. A floating solver's infeasibility report is never used as proof.
Some preliminary runs reported numerical difficulty; the exact phase-I
certificates below are the evidence for those cases too.

The generated 726,930-byte certificate bundle remains outside Git. Public
source and the [compact expected record](a3_expected.json) suffice to
regenerate and check it. From this directory, using CPython 3.11.2:

```sh
python3 -m venv /tmp/order54-a3-env
/tmp/order54-a3-env/bin/pip install -r requirements-a3.txt
/tmp/order54-a3-env/bin/python generate_a3_certificates.py --output /tmp/order54-a3.json
python3 verify_a3.py --certificates /tmp/order54-a3.json > /tmp/order54-a3-check.json
cmp /tmp/order54-a3-check.json a3_expected.json
python3 -O verify_a3.py --certificates /tmp/order54-a3.json > /tmp/order54-a3-check-O.json
cmp /tmp/order54-a3-check-O.json a3_expected.json
```

The pinned discovery environment uses NumPy 2.4.6 and SciPy 1.15.3.
The generator refuses to overwrite its output. All fourteen certificates
were regenerated afresh in 31.25 seconds (peak resident memory 121,700 KiB)
and matched entry for entry. The two exact checks agree; their common output
has SHA-256
`d7653a3e249cde5c9f4407e81523a741e4884e42502ed9fd31eb39ba3974800b`. A different numerical-library build may produce other valid duals;
the exact inequalities, rather than historical dual hashes, establish the
mathematics, but changed evidence must be inspected and checked.

The checker independently enumerates colored types by neighbor multisets
instead of recursive compositions, and independently reconstructs rows
from their incident type-edges instead of the production column filling.
All 67,581 colored-model columns agree, as do the 1,710 columns of the
unrestricted degree model. It also checks the complete six-profile cover,
all 21 frames and 780 bounded cases, and rejects four corrupted certificates.
Generic class-ball and pair-capacity identities are checked directly on
354 actual graphs, with 6,766 exact class-ball equations. These controls
support the implementation; they are not 187-edge witnesses or substitutes
for the graph-to-model proof.

Trust remains in the imported order-53 bound, the preceding corrected
identities, the written reductions and extraction arguments, unformalized
exact code, Python and hardware. NumPy/SciPy are needed to regenerate
candidate multipliers, but their floating conclusions are outside the
exact proof boundary. The two model implementations share the mathematical
reduction. There is no proof-assistant formalization or new external review.
No large search output, certificate bundle, binary, or private graph data
is part of the publication.

The [primary catalogue](https://users.cecs.anu.edu.au/~bdm/data/extremal.html)
was checked again on 2026-09-11 and is unchanged. The
[2025 primary paper](https://arxiv.org/html/2508.05562v1) gives the broader
finite-frontier context. The narrowly searched sources and committed graph
contained no matching restriction; no historical-priority claim is made.
The next boundary is $A=2$, with positive deficits $(2)$ or $(1,1)$.
The present certificates are conditional on $A=3$, and cannot be reused
unchanged there.

## Regenerated exact margins

| Case | Exact corrected lower bound / contradiction margin |
|---|---|
| `m_at_A3` | `20075113/12500000` |
| `shared_six_endpoint` | `572223/100000000` |
| `cycle_p0_six1` | `40600473/50000000` |
| `cycle_p0_threefour` | `42702019/100000000` |
| `cycle_p0_sev0` | `77486787/100000000` |
| `cycle_p0_sev3` | `31401737/50000000` |
| `cycle_p0_P3` | `19423271/20000000` |
| `cycle_p0_3P2` | `332663/12500000` |
| `cycle_p1_six1` | `85324267/100000000` |
| `cycle_p1_threefour` | `6639133/12500000` |
| `cycle_p1_sev0` | `10969197/10000000` |
| `cycle_p1_sev3` | `18146133/20000000` |
| `cycle_p1_P3` | `24931629/25000000` |
| `cycle_p1_3P2` | `585667/4000000` |
