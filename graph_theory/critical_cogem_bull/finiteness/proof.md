# Finiteness of critical co-gem/bull-free graphs

All graphs are finite and simple, and all forbidden subgraphs are induced.
Write `crit_k(F)` for the isomorphism classes of nonempty graphs `G` with
`chi(G)=k`, with `chi(G-v)<k` for every vertex `v`, and containing no member
of `F`. A co-gem is `P4+P1`; a gem is its complement. The bull is a triangle
with two pendant vertices attached to different triangle vertices. The
triangular prism is two triangles joined by a matching; its complement is
`C6`.

## 1. The whole-class conclusion and its provenance

**Theorem A.** For every integer `k>=1`, there are only finitely many
`k`-vertex-critical (co-gem,bull)-free graphs.

The deduction has two ingredients, which must be distinguished:

1. Our earlier [critical exclusion theorem](../prism_reduction/proof.md),
   Corollary 3: every vertex-critical (co-gem,bull)-free graph is `C6`-free,
   with no restriction on its order or chromatic number.
2. **Prior theorem**, Beaton--Cameron (2026),
   [Theorem 3.9](https://arxiv.org/html/2608.20045v1): for every `ell>=0`
   and `k,n>=1`, the class
   `crit_k(P4+ell P1, complement(L(K_{2,n})))` is finite.

To specialize the second ingredient, the vertices of `L(K_{2,3})` are
the six edges of `K_{2,3}`. Three edges meet each vertex in the part of
size two, producing two triangles in the line graph. Between these
triangles exactly the three pairs meeting the same vertex in the other
part are adjacent. Thus `L(K_{2,3})` is the prism, and its complement is
`C6`. Set `ell=1,n=3`. The first ingredient gives the containment

\[
 \operatorname{crit}_k(\text{co-gem},\text{bull})
 \subseteq \operatorname{crit}_k(\text{co-gem},C_6).
\]

The right-hand side is finite by the prior theorem, proving Theorem A.
In particular, this covers **every** critical
`(co-gem,bull,C6)`-free graph containing `P5`.

The finiteness of the larger co-gem/`C6` class is not a new result here.
The new conclusion is its applicability to the bull case through the
unrestricted exclusion theorem. The next sections make the order bound
effective and give a direct structural proof of the specialized prior
finiteness statement. They do not assert priority for that statement.

## 2. An effective threshold from prime-graph Ramsey theory

A module is a nonempty vertex set such that each outside vertex is either
complete or anticomplete to it. A graph is prime if it has no module of
size between two and one less than its order. This convention allows the
graphs of orders one and two to be prime.

Let `N(t)` be the threshold in Chudnovsky--Kim--Oum--Seymour (CKOS),
[*Unavoidable induced subgraphs in large graphs with no homogeneous sets*,
Theorem 1.2](https://web.math.princeton.edu/~mchudnov/largeprime.pdf), for
`t>=3`. Their proof supplies the following specific choice. Here
`R(s1,...,sr)` is the multicolor clique Ramsey number with the indicated
color-specific targets:

\[
\begin{aligned}
 g(t)&=4^{t-2}(t+1)+2(t-2)+1,\\
 h(t,u,2)&=t,\\
 h(t,u,i)&=(t-1)R(t,t,t,t,t,t,t,u,u,h(t,u,i-1))+1\quad(i>2),\\
 f(t,a,b)&=2^{R(a+t,\,2t-1,\,t+b,\,t+b-1)+1},\\
 M(t)&=f(t,h(t,g(t),t),g(t)),\\
 N(t)&=R(M(t),M(t)).
\end{aligned}
\]

These are CKOS Propositions 3.1, 4.1 and 5.1 and the proof of Theorem 1.2,
not newly obtained Ramsey estimates. The recurrence contains seven copies
of `t` before the two copies of `u`. It specifies a finite computable
integer: Ramsey numbers themselves can be computed by finite exhaustive
search. No value of this enormous expression is evaluated or claimed
optimal here.

**Lemma B (chains).** In a gem-free graph with independence number at most
`k`, every chain has length at most `10k+4`.

A chain of length `m` is a sequence `v0,...,vm` such that, for `i>=1`,
`v(i-1)` is either the unique neighbor or the unique nonneighbor of `vi`
among its predecessors. Encode step `i` by zero in the first case and
one in the second case. At `i=1`, this assigns zero to an edge and one to
a nonedge.

Let `z` be the number of zero steps. Among their indices, take a parity
class of size at least `ceil(z/2)`. The corresponding vertices form an
independent set: two indices have difference at least two, and the later
zero-step vertex has no earlier neighbor except its immediate predecessor.
Consequently `z<=2k`.

Five consecutive one steps, at indices `i,...,i+4`, induce the complement
of a six-vertex path on `v(i-1),...,v(i+4)`: consecutive vertices are
nonadjacent and all other pairs adjacent. In that graph, the first four
vertices induce a `P4` (the complement of `P4`), and the last vertex is
complete to them. This is a gem. Thus every run of one steps has length
at most four. There are at most `z+1` runs, whence

\[
 m\le z+4(z+1)\le10k+4.
\]

Complementation exchanges zero and one steps, so the complement of any
chain graph is also a chain graph. The lemma applies to chain graphs in
either orientation of CKOS's theorem.

**Lemma C (prime bound).** If `H` is prime, gem-free and prism-free, and
`alpha(H)<=k`, then `|V(H)|<N(10k+5)`.

Put `t=10k+5`. CKOS's theorem states that a prime graph with at least
`N(t)` vertices contains one of seven graph types or its complement.
The following exclusions cover every type and both orientations.

| CKOS type `F` | Obstruction in `F` | Obstruction in its complement |
| --- | --- | --- |
| One-subdivision of `K_{1,t}` | The `t` leaves are independent. | A gem, as explained below. |
| `L(K_{2,t})` | Three matching pairs induce a prism. | One of the two original cliques becomes an independent set of size `t`. |
| Thin spider with `t` legs | Its legs are independent. | Its original clique becomes an independent set of size `t`. |
| Bipartite half-graph of height `t` | Either part is independent. | A gem, as explained below. |
| `H'_{t,I}` | Its independent part has size `t`. | Its clique part becomes an independent set of size `t`. |
| `H*_t` | Its independent part has size `t`. | Its clique part becomes an independent set of size `t`. |
| Graph induced by a chain of length `t` | Lemma B. | Lemma B, since complementation preserves chains. |

For the subdivided star, denote its center by `c`, middle vertices by
`a1,...,at`, and leaves by `b1,...,bt`. The vertices `b1,a1,c,a2,b3`
induce `P4+P1`. Its complement therefore contains a gem.

For the half-graph, use independent parts `a1,...,at` and `b1,...,bt`,
with `ai bj` an edge exactly when `i>=j`. The vertices `a1,b1,a2,b2,b3`
induce `P4+P1`. Again its complement contains a gem. The two modified
half-split graphs in the table keep the original independent part and
clique part, each of size `t`; their one additional vertex is irrelevant
to these two obstructions.

Since `t>k` and `t>=3`, every listed possibility is forbidden. This proves
Lemma C. Notice that it needs no bull-free assumption.

## 3. Critical modules give a direct order bound

**Lemma D.** Every module of a vertex-critical graph induces a
vertex-critical graph.

Let `G` be `k`-critical and `M` a module with `chi(G[M])=r`. If deleting
some `v` from `M` left its chromatic number equal to `r`, a coloring of
`G-v` with at most `k-1` colors would use at least `r` colors on `M-v`.
Select `r` of these colors and use them to color `G[M]`. Each outside
vertex complete to `M` avoids all these colors already; outside vertices
anticomplete to `M` cause no conflict. This extends to a coloring of `G`
with at most `k-1` colors, a contradiction. Singleton modules are immediate.

**Lemma E.** In a co-connected, co-gem-free vertex-critical graph, every
proper module induces a clique. Contracting the maximal true-twin classes
therefore gives a prime graph.

Co-connected means that the complement is connected. Let `M` be a proper
module. Some vertex outside `M` is anticomplete to `M`: otherwise all edges
of the cut would be present and the complement would be disconnected.
An induced `P4` inside `M`, together with such a vertex, would be a co-gem.
Thus `G[M]` is `P4`-free. By Lemma D it is vertex-critical. `P4`-free graphs
are perfect, and a perfect vertex-critical graph must be a clique: a
maximum clique already needs all its colors, so there is no vertex outside
it. This proves the first assertion.

Two vertices are true twins when their closed neighborhoods are equal.
The maximal equivalence classes are cliques and modules. Between any two
classes all edges or no edges are present, so choosing one representative
of each class defines an induced quotient `Q`.

Suppose a proper nontrivial module `U` existed in `Q`. The union `W` of
the corresponding classes would be a proper module in `G`, hence a clique
by the first assertion. All classes indexed by `U` are thus mutually
complete, and vertices outside `W` have the same adjacency to all of `W`.
Every two vertices in `W` are true twins in `G`. They should belong to a
single maximal class, contradicting `|U|>=2`. Hence `Q` is prime.

**Theorem F (effective bound).** Every `k`-vertex-critical
`(co-gem,C6)`-free graph satisfies

\[
 |V(G)|\le B(k):=k\bigl(N(10k+5)-1\bigr).
\]

Partition `V(G)` into the vertex sets `V1,...,Vs` of the connected
components of its complement. The corresponding induced graphs `Gi` are
complete join factors. Write `ki=chi(Gi)`. Chromatic number adds across
a join, so `sum ki=k`; criticality of `G` implies that each `Gi` is
`ki`-critical. Each `Gi` is co-connected and co-gem-free.

Apply Lemma E to `Gi`, obtaining its prime true-twin quotient `Qi`.
It is an induced subgraph of `Gi` and therefore remains co-gem-free and
`C6`-free. Its complement `Hi` is prime, gem-free and prism-free, with
`alpha(Hi)=omega(Qi)<=ki<=k`. Lemma C gives `|Qi|<=N(10k+5)-1`.
Each true-twin class is a clique of size at most `ki`, so

\[
 |V(G)|=\sum_i |V(G_i)|
 \le\sum_i k_i|V(Q_i)|
 \le k\bigl(N(10k+5)-1\bigr).
\]

The same global `k` was used in every quotient bound, so no monotonicity
assumption on the threshold function is needed. The argument includes
singletons and complete graphs. By the unrestricted critical `C6`
exclusion, the bound applies to every critical (co-gem,bull)-free graph.

The elementary fact about `P4`-free graphs used above also follows from
the Strong Perfect Graph Theorem: an odd hole or odd antihole of length
at least five contains an induced `P4`, since `P4` is self-complementary.

## 4. What this closes, and what it does not

Theorem A answers the bull instance of the finiteness question in
Beaton--Cameron (2025), Section 7. Theorem F supplies an all-order finite
reduction for the entire residual class, including every `P5`-containing
candidate. In principle, one can enumerate all simple graphs up to `B(k)`,
test the forbidden subgraphs, and compute chromatic numbers exactly to
obtain the complete critical class for any fixed `k`. This is a terminating
procedure, not a practical enumeration proposal.

The selected stronger equality
`crit_k(co-gem,bull)=crit_k(P3+P1)` for every `k` is **not proved**.
Our [earlier amplification theorem](../proof.md) establishes the equality
after adding `P5`-freeness; excluding `P5` from the full class is still
an open obligation in this work. The unrestricted `k=7` decision has not
been executed. The huge bound `B(7)` is not a short computational route
to that decision and does not justify assuming the known 13-vertex bound
for the `P3+P1`-free class on the larger class.

The combined package now contains a sharp `P5`-free characterization,
unrestricted prism-component perfection and critical `C6` exclusion, and
the resulting whole-class finiteness theorem. The research lane is parked
at the end of the contracted third mathematical pass; no continuation on
bounded residual cases is implied.

## 5. Trust boundary

The new bridge and bound are ordinary written mathematics, not a formal
proof-assistant derivation. Theorem A imports Beaton--Cameron Theorem 3.9
and our prior computer-assisted critical exclusion. Theorem F instead
imports CKOS Theorem 1.2 with its constructive threshold, and the standard
perfection of cographs. The prior critical exclusion uses SPGT and a
compact complete local obstruction certificate; its source, checker,
certificate and limitations remain in `../prism_reduction` unchanged.

`controls.py` verifies the named family embeddings, chain witnesses, and
small examples exposing the module hypotheses. These controls do not
prove completeness at arbitrary order and are not independent peer review.
No new SAT run, finite graph census, floating-point computation, or
unverified solver trace is a premise of the finiteness conclusion.
