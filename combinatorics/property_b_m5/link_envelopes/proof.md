# Link-union envelopes and a degree barrier for Property B

11 September 2026. Exact computer-assisted theorems; all hypergraphs are finite and simple. A hypergraph is *pair-covered* if every two distinct vertices belong to an edge. Property B means that every edge can be made nonmonochromatic by a red/blue vertex coloring.

**Theorem A (degree barrier).** A pair-covered 5-uniform hypergraph with at most 33 edges and minimum degree at most six has Property B.

**Theorem B (complete vertex classes).** Every pair-covered 5-uniform hypergraph on 19 or 25 vertices with at most 34 edges has Property B.

**Theorem C (spanning links).** In a 5-uniform hypergraph on 25 vertices, call a vertex *spanning and linear* if its incident edges, after that vertex is removed, partition the other 24 vertices into six four-sets. Such a hypergraph has Property B whenever it has at most \(m\) edges and at least \(s\) spanning linear vertices, for

\[
(s,m)=(3,33),\ (4,34),\ (5,35).
\]

Theorems A–C are proved using general link-union and forest bounds below. They add a structural restriction and complete classes at several edge counts to the preceding unrestricted lower bound \(m(5)\ge33\). **They do not prove \(m(5)\ge34\).**

## 1. Greedy coloring and conditional link unions

Start with every vertex red, process an ordering, and turn a vertex blue if it is the last vertex of an otherwise red edge. No red edge remains. If a blue edge \(F\) remains, its first vertex \(u\) was turned blue by some edge \(E\), so
\(E\cap F=\{u\}\) and \(\max E=u=\min F\).
Thus it suffices to find an ordering without a *critical vertex*: one that is last in some edge and first in another. This is the established Pluhár greedy obstruction, as used by Grill–Linzmayer [1].

Fix \(s\) marked vertices at distinct positions in the ordering. Let \(N=v-s\), and uniformly permute the free vertices. Write \(x_A\) for the number of edges whose marked trace is \(A\). At a marked position \(k\), corresponding to \(u\), each incident edge contributes a free set \(F_i\) of size
\(a_i=5-|A_i|\). Its fixed vertices determine whether it is eligible to be last at \(u\), first at \(u\), both, or neither. Denote this eligibility by a flag \(f_i\in\{0,1,2,3\}\).

Let \(L\) free positions precede \(u\). The set \(C\) of free vertices placed there is a uniform \(L\)-subset of an \(N\)-set. The critical event is exactly

\[
\bigl(\exists i:\ f_i\text{ permits left and }F_i\subseteq C\bigr)
\quad\text{and}\quad
\bigl(\exists j:\ f_j\text{ permits right and }F_j\cap C=\varnothing\bigr). \tag{1}
\]

Extra intersections are automatically excluded: the same free vertex cannot be on both sides. Summing probabilities over edge pairs overcounts (1), sometimes substantially.

**Link-envelope lemma.** Suppose \(\bigcup_i F_i\) is the full \(N\)-set. The maximum probability of (1), over every such family with prescribed sizes and eligibility flags, is given by the finite signature enumeration below. Consequently this maximum is a valid upper bound at a marked vertex in a pair-covered hypergraph.

For a free vertex \(w\), its incidence signature is the nonempty set
\(I(w)=\{i:w\in F_i\}\). Put

\[
e=\sum_i a_i-N=\sum_w(|I(w)|-1).
\]

Enumerate all multisets of signatures of size at least two with total cost
\(\sum_I(|I|-1)=e\), subject to each row \(i\) occurring at most \(a_i\) times. Fill its remaining \(a_i\) incidences by singleton signatures \(\{i\}\). This gives exactly all incidence matrices with the prescribed row sizes and no uncovered column, up to labeling the free vertices. Signatures may repeat: they then denote distinct free vertices with identical incidences. Allowing repeated free sets or ignoring constraints imposed by other marked vertices only enlarges the maximum, which is harmless for an upper bound.

For each resulting matrix, let \(q\) be the number of nonsingleton columns. Enumerate their \(2^q\) assignments to left/right. For row \(i\), let \(h_i\) be its number of singleton columns. A dynamic program chooses \(j_i\) of these to lie left, with weight \(\binom{h_i}{j_i}\), recording the total left size and whether a left-eligible and a right-eligible edge have become monochromatic on their required sides. The coefficient with total left size \(L\) and both flags present counts exactly the subsets in (1). Divide by \(\binom NL\), then take the maximum over the incidence matrices.

This proves both soundness and completeness of the envelope calculation. Its cost is controlled by incidence excess, not by the number of full hypergraphs. The implementation uses envelopes when \(e\le3\), and retains the ordinary pair bound otherwise. The lemma itself has no excess-three restriction and works for arbitrary edge sizes and eligibility flags. In uniformity \(r\), simply replace \(5-|A_i|\) by \(r-|A_i|\).

At unmarked positions we retain the elementary conditional first-edge, last-edge, and critical-pair bounds. For clarity, if a trace \(A\) has \(a=r-|A|\) free vertices, its last-edge probability numerator is
\(a(L)_{a-1}(N-a)!\), with common denominator \(N!\). The first-edge formula uses \(R\). For disjoint eligible traces \(A,B\), a particular pair intersecting exactly in the free pivot has numerator
\((L)_{a-1}(R)_{b-1}(N-a-b+1)!\).
There are at most \(x_A(x_B-\mathbf1_{A=B})\) such ordered pairs. At a marked pivot, the corresponding numerator is \((L)_a(R)_b(N-a-b)!\) when the fixed intersection is exactly that pivot. Impossible configurations have coefficient zero. Taking the minimum of these bounds, one, and the link envelope at each position, then summing over positions, bounds greedy failure. A value strictly below one proves Property B. The original coefficient source is preserved in `../model.py` and explained in the [preceding proof](../proof.md).

## 2. A packing-sensitive forest bound for tails

We also strengthen the treatment of edges lying wholly before or after a marked block. Let \(\mathcal F\) be \(n\) distinct \(r\)-subsets of an \(N\)-set, where \(N\ge2r\). For a uniform \(L\)-subset \(C\), let \(A_E\) mean \(E\subseteq C\) or \(E\cap C=\varnothing\). Set \(R=N-L\) and

\[
p=\frac{\binom Lr+\binom Rr}{\binom Nr}.
\]

For distinct edges with intersection size \(i\), the exact probability of \(A_E\cap A_F\) is

\[
p_i=\frac{\binom{N-2r+i}{L-2r+i}+\binom{N-2r+i}{L}
 +2\mathbf1_{i=0}\binom{N-2r}{L-r}}{\binom NL},\quad 0\le i<r. \tag{2}
\]

Use zero for impossible binomial coefficients. The final term counts the two opposite-side possibilities for disjoint edges; it must not be omitted.

Let \(q_0=\min_{0\le i<r}p_i\), and \(q_t=\min_{t\le i<r}p_i\) for \(1\le t<r\). These numbers are nondecreasing. An upper bound \(K_t\) on the size of an \(r\)-uniform family with pairwise intersections at most \(t-1\) is obtained as follows. Such a family of size \(c\) satisfies

\[
c\binom rt\le\binom Nt.
\]

Writing \(cr=N a+b\), \(0\le b<N\), convexity of integer vertex degrees also gives

\[
N\binom a2+ba\le(t-1)\binom c2. \tag{3}
\]

Take \(K_t\) to be the largest positive integer satisfying these two necessary conditions. No assertion of existence of a family of size \(K_t\) is needed.

**Tail-forest lemma.** For \(n\ge1\),

\[
\Pr\Bigl(\bigcup_{E\in\mathcal F}A_E\Bigr)
\le np-(n-1)q_0-
\sum_{t=1}^{r-1}\max(0,n-K_t)(q_t-q_{t-1}). \tag{4}
\]

For \(n=0\), the bound is zero.

To prove it, recall the spanning-forest union inequality: for events indexed by the vertices of any forest \(T\),
\(\Pr(\cup A_i)\le\sum_i\Pr(A_i)-\sum_{ij\in T}\Pr(A_i\cap A_j)\).
Pointwise, the number of present vertices minus the number of forest edges joining present vertices is at least the indicator of a nonempty present set. Taking expectations proves the inequality. Its optimized spanning-tree form is classical Hunter [2].

Join two members of \(\mathcal F\) in \(G_t\) if they intersect in at least \(t\) points. Representatives from different components form a family with pairwise intersections below \(t\); hence \(G_t\) has at most \(K_t\) components. Kruskal's algorithm, processing larger intersections first and completing to a spanning tree, simultaneously selects \(n-c(G_t)\) edges inside each nested graph \(G_t\). Lower-bound these edge weights by (2) at their successive thresholds. The resulting forest correction is the quantity subtracted in (4).

This is a uniform bound over all families with the stated parameters. It does not require constructing their intersection graph.

## 3. A forest correction inside one link

Consider a pair-covered \(r\)-uniform hypergraph, a vertex \(u\) of degree \(d\), and its \(d\) distinct \((r-1)\)-element link sets on \(N=v-1\) vertices. Their incidence excess is \(e=(r-1)d-N\). Their total pairwise intersection size is at least \(e\), since \(\binom c2\ge c-1\) for each positive multiplicity \(c\). Distinct link sets intersect in at most \(r-2\) points. Thus the number \(t\) of ordered disjoint link pairs is at most

\[
T=d(d-1)-2\left\lceil\frac e{r-2}\right\rceil. \tag{5}
\]

Assume \(r\ge3\), \(N\ge3(r-1)\), and put \(a=r-1\). With \(L\) free vertices before \(u\) and \(R=N-L\) after it, each ordered disjoint pair has critical-event probability

\[
P=\frac{(L)_a(R)_a(N-2a)!}{N!}.
\]

Form a bipartite graph with a left and right copy of every link set; its edges are the ordered disjoint pairs. Events corresponding to edges sharing a left or right endpoint have intersection probability at least

\[
Q=\min\left\{
\frac{(L)_a(R)_{2a}(N-3a)!}{N!},
\frac{(L)_{2a}(R)_a(N-3a)!}{N!}
\right\}. \tag{6}
\]

Indeed, on the side with two link sets their union has size at most \(2a\), and it is disjoint from the shared set on the other side. Requiring additional specified vertices on one side can only decrease the probability. Each component of this bipartite graph containing an edge has at least two vertices, so there are at most \(d\) such components. Its line graph consequently has a spanning forest with at least \(t-d\) edges when \(t>d\). Applying the forest inequality gives

\[
\Pr(u\text{ critical})\le tP-\max(0,t-d)Q
\le TP-\max(0,T-d)Q. \tag{7}
\]

The final substitution is valid because \(P\ge Q\). We may also take the minimum with either single-side union bound and one.

Place \(u\) in the central position. A critical vertex earlier than \(u\) requires an edge avoiding \(u\) wholly on the left; one later requires such an edge wholly on the right. Therefore (4), for the \(m-d\) edges avoiding \(u\), plus (7), bounds the whole failure probability. `forest.py` evaluates this formula exactly.

The resulting complete ranges needed here are:

| \(v\) | \(m\) | Minimum degrees covered | Maximum failure bound |
|---|---:|---|---:|
| 19 | 34 | 5, 6, 7, 8 | \(12047/12155\) |
| 20 | 33 | 5, 6 | \(45921/46189\) |
| 21 | 33 | 5, 6 | \(417/418\) |

All are strictly below one.

## 4. Complete coverage of low degrees

A pair-covered 5-uniform hypergraph of minimum degree at most six has at most 25 vertices, since a minimum-degree vertex covers at most four other vertices per incident edge. At most eight vertices can be split into classes of size at most four. For 9–18 vertices, the balanced-coloring union bound is below one at 33 edges; the integer inequalities are replayed.

For larger vertex counts, pad to 33 edges **avoiding a chosen minimum-degree vertex**. There are enough unused five-subsets avoiding it. Pair coverage is retained, and the minimum degree remains at most six. It therefore suffices to handle exactly 33 edges. The preceding table covers 19–21 vertices.

For 22–25 vertices, the minimum degree is six. Choose vertices in nondecreasing degree order, with arbitrary tie-breaking. The first three degrees satisfy

\[
\left\lceil\frac{v-1}{4}\right\rceil\le d_1\le\left\lfloor\frac{165}{v}\right\rfloor,
\qquad
d_i\le\left\lfloor\frac{165-\sum_{j<i}d_j}{v-i+1}\right\rfloor.
\]

Enumerate pair codegrees between one and the smaller endpoint degree, then the triple codegree between zero and the smallest pair codegree. Inclusion–exclusion uniquely determines all eight trace counts. Retain nonnegative vectors and require that every marked vertex cover all outside vertices.

For an unclosed vector on \(s\) vertices, add the next least-degree vertex, with degree between the previous degree and
\(\lfloor(165-\sum_{i=1}^s d_i)/(v-s)\rfloor\). Enumerate every split \(0\le y_A\le x_A\), \(\sum_A y_A=d\), into traces without and with the new vertex. Discard only a trace of size above five, an uncovered marked pair, or a violation of

\[
\sum_{A\ni i}x_A(5-|A|)\ge v-s,
\qquad
\sum_Ax_A\binom{5-|A|}{2}\ge\binom{v-s}{2}.
\]

Thus every real hypergraph follows a retained branch. A coloring certificate on any projection or permutation of the marked set closes that branch. At five vertices, 11 explicitly recorded noncentral position certificates supplement the central bounds. They are recalculated exactly; no heuristic runs in verification.

All branches close by coloring at 22, 24, and 25 vertices. At 23 vertices the replay leaves precisely three canonical five-vertex traces. Each has degrees \((6,7,7,7,7)\). In every remaining trace, an edge containing the degree-six vertex contains at most two of the four degree-seven vertices. The replay checks these assertions entry by entry.

Suppose a noncolorable hypergraph remains at 23 vertices. There is a unique degree-six vertex \(u\); otherwise some choice of the five least-degree vertices would contain two degree-six vertices, contrary to the residual types. The other 22 vertices have degree at least seven. Since their degree sum, together with \(u\), is 165, there are at most
\(165-(6+22\cdot7)=5\) vertices of degree above seven. At least 17 vertices therefore have degree seven.

Any four of these 17 may be selected after \(u\), by tie-breaking among least degrees. If an edge through \(u\) contained three degree-seven vertices, selecting those three and a fourth would give a forbidden trace of size at least four through \(u\). Every edge through \(u\) consequently contains at most two degree-seven vertices. Its six incident edges cover at most twelve such vertices, but pair coverage requires them to cover all seventeen. This contradiction proves Theorem A.

## 5. Spanning links and the range 33–35

Let \(S\) consist of \(s\) spanning linear vertices on a 25-vertex set. Every pair with an endpoint in \(S\) lies in exactly one edge. The traces of size at least two partition the pairs of \(S\) into complete graphs, with block sizes two through five. For a block its trace count is one. The singleton count at a vertex is six minus the number of incident blocks, and the empty count is \(m\) minus all nonempty counts.

The verifier enumerates every pair partition by choosing the block containing the first uncovered pair. For \(s=3,4,5\), there are respectively 2, 3, and 5 types up to relabeling. At every marked vertex the free link sets are disjoint, so the envelope has excess zero. Exact evaluation at the central consecutive positions yields:

| Spanning linear vertices \(s\) | Edge bound \(m\) | Types | Largest failure bound |
|---:|---:|---:|---:|
| 3 | 33 | 2 | \(28845/29393\) |
| 4 | 34 | 3 | \(793/798\) |
| 5 | 35 | 5 | \(91877/92378\) |

The full trace vectors are in `linear_certificates.json`; all are regenerated before their probabilities are checked. For fewer edges, pad avoiding \(S\), preserving the spanning links. This proves Theorem C.

For a pair-covered 25-vertex hypergraph with exactly 34 edges, every degree is at least six and the degree sum is 170. Therefore at least \(25\cdot7-170=5\) vertices have degree six. Each such vertex is spanning and linear, since its 24 link incidences cover 24 distinct vertices. Theorem C with four of them proves colorability. Padding first handles at most 34 edges. Together with the 19-vertex forest calculation, this proves Theorem B.

## 6. Consequence for the next endpoint and verification scope

Contracting any pair of vertices sharing no edge preserves noncolorability and uniformity; duplicate edges can be coalesced. Thus a hypothetical 33-edge obstruction has a pair-covered quotient with at most 33 edges. Padding on its vertex set gives exactly 33 edges. Pair coverage implies
\(33\ge\lceil(v/5)\lceil(v-1)/4\rceil\rceil\), excluding \(v\ge26\). Theorem A forces minimum degree at least seven, while Theorem B excludes 19 vertices and smaller vertex counts are covered by balanced colorings. Since its degree sum is 165, minimum degree seven implies \(7v\le165\). Consequently any obstruction has a pair-covered representative with

\[
20\le v\le23,\qquad \delta\ge7.
\]

This is a whole-endpoint structural reduction. The remaining high-degree cases are **not** decided here. The unrestricted bound remains \(33\le m(5)\le51\).

Run `python3 verify.py` with Python 3.11+, without `-O`. Only the standard library is needed. It enumerates the whole low-degree scope and all spanning-link types, checks the three residual traces and the 17-versus-12 contradiction, and evaluates the forest ranges. `audit.py` checks 64 envelope maxima against independent enumeration of labeled free sets and subsets, 2,240 actual tail-event families, and 5,986 covering links for the pivot bound. The controls are not substitutes for the completeness arguments above.

This is a computer-assisted theorem, not a proof-assistant formalization or independent peer review. Its computational trust boundary is the published source, Python interpreter, and hardware. The broad high-degree exploratory search is not needed for any theorem and is not part of the public certificate.

## References and attribution

[1] K. Grill and D. Linzmayer, *Improved Lower Bounds for Property B*, arXiv:2403.05674v3 (2024), [primary full text](https://arxiv.org/html/2403.05674v3). Greedy critical pairs, fixed marked vertices, and the standard finite reductions are prior art. The present contribution replaces pair sums at marked vertices by complete link-union envelopes and supplies quantified applications and a global degree barrier.

[2] D. Hunter, *An upper bound for the probability of a union*, Journal of Applied Probability 13(3) (1976), 597–603, [publisher record](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/S0021900200104164), DOI 10.2307/3212481. The forest union inequality is classical; it is re-proved above. The contributions here are the packing-sensitive tail formula, the link-event forest specialization, and their applications to this Property B endpoint. No novelty is claimed for Hunter's inequality, Kruskal's algorithm, or elementary packing inequalities.

The [preceding unrestricted theorem](../proof.md) and its source are preserved. The located external primary frontier remains 32–51 before that result. Numerical tables in the 2026 overview were inaccessible; priority statements remain limited to the searched primary literature.
