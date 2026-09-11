# Twelve high vertices have at most three distant incidences

Let (G) be a finite simple graph with 54 vertices, 187 edges, and no
triangle or quadrilateral. Suppose exactly twelve vertices have degree
eight. The degree reduction in [proof.md](proof.md), conditional on the
published order-53 upper bound 181, gives degree counts ((16,26,12)).
Write (T=V_8), (F(v)=\{u:\operatorname{dist}(u,v)>2\}\), and

\[
a_t=|F(t)|\quad(t\in T),\qquad A=\sum_{t\in T}a_t.
\]

**Theorem. (A\le3). In particular, at least nine of the twelve
high vertices are sinks (have every vertex within distance two).**

The proof excludes every graph in the subclasses (A=4) and (A=5),
with arbitrary incidences. It does not exclude (A=0,1,2,3), assume
that all high vertices are sinks, realize a graph, or improve the numerical
interval (185\le\operatorname{ex}(54,\{C_3,C_4\})\le187).
The preceding [thirteen-high-vertex exclusion](boundary_exclusion.md)
continues to give the unconditional restriction (z\le12).

The argument below uses an exact rational certificate only to establish
(m\ge2) when (A=4). The decisive step distinguishes the individual
high-neighbor sets and an individual missed vertex. None of the earlier
SAT forest exclusions, thirteen-vertex all-sink lemma, or thirteen-vertex
rational certificates is a premise.

## Corrected identities

Put (H=G[T]), (h_t=d_H(t)), (m=e(H)),
(k=|\{t:h_t=2\}|), and (c(v)=|N(v)\cap T|), including (c(t)=h_t)
when (t\in T). Let (q) count distant unordered pairs within (T),
and let (p_7) count distant pairs between (T) and (V_7). Set

\[
s_v=\sum_{u\sim v}(d(u)-6),\qquad
\epsilon_v=\begin{cases}s_v-8&v\in V_6,\\s_v-7&v\in V_7,\end{cases}
\qquad R=\sum_{t\in T}h_ta_t.
\]

The radius-two ball identity gives (s_t=5-a_t). In particular
(h_t\le2); if (h_t=2), then (a_t\le1). Therefore

\[
R\le A+k. \tag{1}
\]

The degree-class neighbor counts of a high vertex are
((3+a_t+h_t,5-a_t-2h_t,h_t)). Hence

\[
\sum_{V_6}c=36+A+2m,\qquad \sum_{V_7}c=60-A-4m. \tag{2}
\]

Every high pair is an edge, has a unique common neighbor, or is distant.
The high common neighbors account for (k), so

\[
\sum_{V_6\cup V_7}\binom{c(v)}2=66-m-k-q.
\]

Combining this with (2) gives the **exact nonnegative inventory**

\[
\sum_{V_6}\frac{(c-3)(c-2)}2+
\sum_{V_7}\frac{(c-1)(c-2)}2=8-m-k-q-A=:B. \tag{3}
\]

Both summands are nonnegative at every integer (c\ge0).
A six-vertex with (c=4,5) costs respectively 1,3; a seven-vertex
with (c=4) costs 3. The zero-cost values are (c=2,3) on (V_6)
and (c=1,2) on (V_7).

The weighted gap from [proof.md](proof.md) is now

\[
Q+\sum_{t\in T}a_t(a_t+4)+2U=28,\qquad
Q=\sum_{V_6}\epsilon^2+\sum_{V_7}\epsilon(\epsilon-1), \tag{4}
\]

where (U=\sum_{\{u,v\}\text{ distant}}(d(u)-6)(d(v)-6)\ge0).
In particular (2U\ge4p_7+8q), (A\le5), and (a_t\le3).
Writing (P=\sum\max(\epsilon,0)) and
(N=\sum\max(-\epsilon,0)) on the low vertices gives (N\le Q).

The two epsilon balances, with the nonsink corrections retained, are

\[
\sum\epsilon=4+A,\qquad
\sum c\epsilon=2m+R-p_7-4q. \tag{5}
\]

For the first, (sum s_v=sum d(v)(d(v)-6)=374); subtract the
high sum (60-A) and the low baseline (16\cdot8+26\cdot7=310).
For the second, the local weighted identity is

\[
\sum_{u\sim v}s_u=50-s_v+(d(v)-1)(d(v)-6)
 -\sum_{u\in F(v)}(d(u)-6).
\]

At a high vertex (t), substituting the displayed neighbor counts yields
(sum_{u\sim t,\ u\notin T}\epsilon_u
=h_t+sum_{u\sim_Ht}a_u-sum_{u\in F(t)}(d(u)-6)).
Sum over (t) to obtain the second equation in (5).

For degree six, (2c-8\le\epsilon\le c-2), so
((c-3)\epsilon\ge0). For degree seven,(2c-7\le\epsilon\le c),
and the only negative types ((c,\epsilon)) are ((1,1),(2,1),(2,2)).
Let their counts be (b_1,b_2,b_{22}), and write
(W=2b_1+b_2+2b_{22}) for the magnitude of their negative contribution.
Equation (5) implies

\[
W\ge12+3A-2m-R+p_7+4q. \tag{6}
\]

## Individual distant covers, allowing nonsinks

Write (C(v)=N(v)\cap T). Distinct vertices have high-neighbor sets
intersecting in at most one point. Distant vertices have disjoint such sets.
If (mathcal A) is the adjacency matrix and (mathcal F) the distant-pair
matrix, uniqueness of short paths gives

\[
\mathcal F=J-\mathcal A^2-\mathcal A+D-I,
\quad
(\mathcal A\mathcal F-\mathcal F\mathcal A)_{uv}
=(d(u)-d(v))(1-\mathcal A_{uv}).
\]

At (t\in T) and any vertex (v), this becomes

\[
(8-d(v))[t\in C(v)]+
\sum_{u\in F(v)}[t\in C(u)]
=8-d(v)+|F(t)\cap N(v)|. \tag{7}
\]

Thus (C(y)) together with the sets at its distant vertices covers
all twelve high vertices for each seven-vertex (y); multiplicities above
one are allowed by the correction. Also (|F(y)|=4-\epsilon_y), while
(|F(v)|=9-\epsilon_v) on (V_6).

Consequently type ((1,1)) needs three distant sets with total size at
least 11; type ((2,1)) needs three with total size at least 10; type
((2,2)) needs two with total size at least 10. If (B\le2), every
set has size at most four, and every size-four set belongs to a degree-six
vertex. There are at most (B) such vertices. Type ((2,2)) is impossible.
Each type ((1,1)) must be distant from at least two size-four vertices,
and each type ((2,1)) from at least one. Each of those six-vertices has
(epsilon\ge0) and at most nine distant vertices. Double counting these
**actual distant incidences**, with the indicated demands, proves

\[
W\le9B\quad(B\le2). \tag{8}
\]

## All (A=5) cases are impossible

Here (Q\le3), (p_7=q=0), and (3) gives (m+k\le3).
If (m=0), then (R=0). Equations (4)--(5) give
(P=9+N\le12). Since (W\le2P\le24), (6), which requires
(W\ge27), is impossible.

For (1\le m\le3), (B=3-m-k\le2). By (1), (6), and (8),

\[
22-2m-k\le W\le9(3-m-k).
\]

The left side exceeds the right by (7m+8k-5>0).
This covers both possible positive deficit multisets
((1,1,1,1,1)) and ((2,1,1,1)); no all-unit-deficit assumption is made.

## The only possible inventory when (A=4)

The exact certificate described below proves (m>1), so (m\ge2).
By (3), (B=4-m-k-q\ge0), hence (m\le4).
Also (1) and (6) give

\[
W\ge20-2m-k+p_7+4q. \tag{9}
\]

If (m=4), then (k=q=B=0), contradicting (8)--(9).
If (m=3), then (k+q\le1), so (8) gives (W\le9), while
(9) gives (W\ge13). If (m=2) and (k+q\ge1), then (k+q\le2),
(8) again gives (W\le9), and (9) gives (W\ge14).
Thus (m=2,k=q=0,B=2). If there were at most one size-four set,
the same incidence argument would give (W\le9), again impossible.

There are therefore exactly two six-vertices (u,v) with (c=4),
exhausting the inventory. Using (2), the complete low profile is

\[
(6,2)^6(6,3)^8(6,4)^2,qquad (7,1)^4(7,2)^{22}, \tag{10}
\]

where entries record ((d,c)). The high graph is (2P_2+8K_1).
Every remaining low set of size three belongs to degree six.
Moreover (b_{22}=0), and (W=2b_1+b_2\ge16+p_7).

## A type-((1,1)) vertex forbids every type-((2,1)) vertex

Suppose such a vertex (y) exists. Its three distant sets have sizes
(4,4,3), and (C(y)) has size one. Their total is twelve, so (7)
forces them to be a partition. In particular (C(u),C(v)) are disjoint.
Let (K=T\setminus(C(u)\cup C(v))), a four-set. Write (C(y)=\{p\});
the third distant vertex (z) has (C(z)=K\setminus\{p\}).

All type-((1,1)) vertices have the same (p) and the same (z).
Otherwise two different three-sets in (K) intersect in two points;
equal three-sets at distinct vertices also violate the no-four-cycle
condition. Equation (7) at ((p,u)) bounds their number by (2+a_p).
They are seven-neighbors of (p), so their number is also at most
(5-a_p-2h_p\le5-a_p). Therefore

\[
b_1\le\min(2+a_p,5-a_p)\le3. \tag{11}
\]

Any type-((2,1)) vertex (y') must be distant from (u) or (v).
By symmetry take (u).

If it is not distant from (v), its distant sets must have sizes
(4,3,3). Including its own pair gives total twelve, hence a partition.
The four points of (C(v)), disjoint from (C(u)), must lie in the pair
and the two triples. Each of those three sets meets (C(v)) in at most
one point, an impossibility.

If it is distant from both (u,v), its own pair lies in (K). It meets
(C(z)=K\setminus\{p\}) in at most one point, so it contains (p).
The third distant set must cover the other two points of (K), both in
(C(z)). This third vertex cannot be (z), because (C(z)) intersects
(C(y')); a vertex distant from (y') has a disjoint high-neighbor set.
Thus two distinct vertices have high-neighbor sets meeting in two points,
again impossible. This argument also covers a third distant set of size
three and a nonzero correction in (7).

It follows that (b_2=0). Now (11) gives (W\le6), contradicting
(W\ge16+p_7). Hence **(b_1=0)**.

## Equality forces an impossible individual missed vertex

We now have (W=b_2\ge16+p_7). On the other hand, (4)--(5) give

\[
b_2\le P=8+N\le8+Q\le16-4p_7.
\]

Equality is forced throughout: (p_7=0), (b_2=P=16), (N=Q=8),
(sum a_t(a_t+4)=20), and (U=0). Thus exactly four high vertices
have (a_t=1), and the other eight are sinks. All positive low epsilons
are the sixteen type-((2,1)) vertices. Every negative epsilon is (-1)
at a six-vertex: these are precisely the equality cases of (N\le Q).

Let (E_+=\sum_{(c-3)\epsilon\ge0}(c-3)\epsilon\ge0).
Equation (5) yields (E_+-16=R-20). Since (R\le A+k=4), we obtain
(R=4) and (E_+=0). With (k=0), every nonsink high vertex therefore
has (h=1). The four nonsinks are exactly the endpoints of the two
edges of (H).

Choose a nonsink (t), its unique high neighbor (t'), and its unique
distant vertex (x). Since (p_7=q=0), (x\in V_6). For any high
sink (s), the high-high commutator gives (|N(s)\cap F(t)|=0).
Thus (x) has no high-sink neighbor. Also (x) is adjacent to neither
(t) nor (t'), because either would put it within distance two of (t).
Its high neighbors must consequently be among the endpoints of the
other edge of (H). But (10) requires (c(x)\ge2), so it is adjacent
to both endpoints of that edge. This creates a triangle. The contradiction
closes every (A=4) case and proves the theorem.

## Exact auxiliary certificate and reproduction

The [certificate](z12_four_defects_certificate.json) uses the existing
necessary type-incidence model in [forest_constraints.py](forest_constraints.py),
rebuilt with class sizes ((16,26,12)) and with no imposed edge bound.
It retains **all 72 locally allowed degree/neighbor-count types**, including
all nonsink high types. There are 1,638 type-edge variables and 222 upper
inequalities. The sole added equality is
(sum_{i:d_i=8}(5-b_i-2c_i)X_i=4), giving 223 equalities.

Here (X_i) counts vertices of type (i=(d_i,(a_i,b_i,c_i))).
For (i<j), (Y_{ij}) counts edges between types; (Y_{ii}) counts
internal edges twice. The equalities express class sizes, class handshakes,
and the neighbor-type totals at each type. The upper inequalities are the
six degree-class pair capacities and, for each type (i) and class (j),

\[
\sum_{v\text{ type }i}\sum_{u\sim v}n_j(u)
\le X_i\bigl(n_j-n_j(i)+(d_i-1)[d_i=j]\bigr).
\]

The latter count the class-(j) vertices in the disjoint radius-two ball,
with the return-to-start multiplicity removed. This proves the necessary
graph-to-model implication. No converse or realization claim is needed.

The nonnegative-variable budget is (sum X_i+sum Y_{ij}\le54+374=428).
The objective is (m=\frac12sum_{d_i=8}c_iX_i). Equality multipliers are
unrestricted and upper-inequality multipliers are nonpositive. Summing the
stored exact rational multipliers gives right-hand side (981743/500000).
The largest excess over an objective coefficient, across **every** column,
is (11/500000). Paying this excess against the full variable budget gives

\[
m\ge\frac{981743}{500000}-428\frac{11}{500000}
 =\frac{195407}{100000}>1.
\]

From this directory, CPython 3.11+ and its standard library suffice:

```sh
python3 verify_z12_distant_incidence.py
python3 -O verify_z12_distant_incidence.py
```

Both must match [z12_distant_incidence_expected.json](z12_distant_incidence_expected.json).
The checker reconstructs all certificate columns in two ways, retains
nonsink types, checks the local signs and deficit cases, and exhausts the
small set arguments in the proof. Definition-level graph controls include
the existing 185-edge graph, all 185 single-edge deletions, and two
selected multiple-edge deletions, so the
correction term is tested on actual high nonsinks, with values zero
through three. The controls are not
187-edge witnesses and do not establish the theorem by extrapolation.

[generate_z12_four_defects_certificate.py](generate_z12_four_defects_certificate.py)
records the optional floating-point discovery calculation. It requires
NumPy 2.4.6 and SciPy 1.15.3 in the original run; solver success or
infeasibility is not used in the proof. Run it with `python3 generate_z12_four_defects_certificate.py --output /tmp/z12-four-defects.json`.
Regenerated multipliers may differ;
the committed certificate is checked using exact rational arithmetic.

Trust remains in the imported order-53 bound, the written reductions,
unformalized exact checker and model, Python, and hardware. There is no
new SAT trace, exhaustive 54-vertex graph search, or formal proof assistant.
The [Afzaly--McKay catalogue](https://users.cecs.anu.edu.au/~bdm/data/extremal.html)
and [2025 primary preprint](https://arxiv.org/html/2508.05562v1), checked
2026-09-10, retain the stated numerical frontier. The catalogue's listed
order-53 graphs are not assumed to be a complete extension base. No
matching twelve-high-vertex restriction was found in the narrowly checked
sources or Discovery Net; historical priority is not established.

The next unclosed incidence boundary is (A=3), with positive deficit
multisets ((3),(2,1),(1,1,1)). The cases (A\le2) and the all-sink
case also remain open. The corrected identities above apply throughout
(z=12), without transferring the thirteen-high-vertex constants.
