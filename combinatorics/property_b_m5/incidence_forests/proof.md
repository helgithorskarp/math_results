# Incidence forests prove m(5) ≥ 34

11 September 2026. An exact computer-assisted theorem.

**Theorem.** Every finite simple 5-uniform hypergraph with at most 33 edges is two-colorable. Consequently

\[
34\le m(5)\le51.
\]

Here \(m(5)\) is the minimum number of edges in a finite simple non-two-colorable 5-uniform hypergraph. This result improves the [preceding unrestricted bound](../proof.md) by using actual link intersections, an event-forest bound, and complete incidence reconstruction. It relies on the [previous global degree barrier](../link_envelopes/proof.md), whose proof and source are preserved unchanged. The upper bound 51 is established in the primary literature [1,3]. The exact value remains open.

## 1. Reduction to the whole remaining endpoint

A hypergraph is *pair-covered* if each pair of distinct vertices lies in an edge. Identifying two vertices which share no edge preserves uniformity and noncolorability; duplicate edges may be coalesced. Repeating this operation reduces any obstruction to a pair-covered one. The preceding unrestricted theorem excludes at most 32 edges, so a hypothetical obstruction with at most 33 edges, and every noncolorable quotient of it, has exactly 33 edges.

The previous global degree theorem proves that such a pair-covered obstruction has minimum degree at least seven and between 20 and 23 vertices. Its degree sum is 165. We now exclude **all four vertex counts**, rather than individual trace profiles.

At 20 vertices the minimum degree is seven or eight; at 21 vertices it is seven. For either 22 or 23 vertices it is seven, and there are respectively at least

\[
v-(165-7v)=11\quad\hbox{or}\quad19
\]

vertices of degree seven. Choose one, \(u\). The sum of its codegrees with all other vertices is \(4d(u)=28\). Pair coverage gives codegree at least one everywhere. At most \(28-(v-1)\), respectively seven or six, other vertices can have codegree greater than one with \(u\). There are at least ten or eighteen other degree-seven vertices. Hence there is a degree-seven vertex \(w\) with

\[
d(u)=d(w)=7,\qquad d(u,w)=1. \tag{1}
\]

This pair exists in every remaining 22- or 23-vertex candidate.

## 2. The probability space and its link events

Use the usual random-order greedy coloring: start red, process vertices in order, and turn a vertex blue if it is last in an otherwise red edge. Failure requires a *critical vertex*, last in an edge and first in another; their intersection is that vertex. This is the established Pluhár mechanism used by Grill–Linzmayer [1].

Put a chosen vertex, or the two vertices in (1), in consecutive central positions. Uniformly permute the other \(N\) vertices. Exactly \(L=\lfloor N/2\rfloor\) free vertices precede the marked block. Their set \(C\) is a uniformly random \(L\)-subset of an \(N\)-set. At a marked vertex, let its incident edges have free parts \(F_i\), sizes \(a_i\), and eligibility flags \(f_i\). Bit 1 permits being entirely before the vertex, and bit 2 permits being entirely after it.

The marked vertex is critical exactly when an eligible \(F_i\) is contained in \(C\) and an eligible \(F_j\) is disjoint from \(C\). For one marked vertex there are \(d\) rows \((a_i,f_i)=(4,3)\). For two marked vertices satisfying (1), each link has six rows \((4,3)\) and one row of size three. This row has flag 2 at the first marked vertex and flag 1 at the second. Both orientations must be checked, especially when \(N\) is odd.

Pair coverage ensures \(\bigcup_iF_i\) is the full free vertex set. Write

\[
e=\sum_i a_i-N.
\]

For a free vertex of incidence multiplicity \(c\), its contribution to \(e\) is \(c-1\).

## 3. A general event-forest bound from the overlap matrix

Let \(w_{ij}=|F_i\cap F_j|\), and let \(G\) have edge \(ij\) exactly when \(w_{ij}>0\). The following lemma applies to arbitrary positive row sizes and eligibility flags.

**Incidence-forest lemma.** Index events by ordered pairs \((i,j)\) with left-eligible \(i\), right-eligible \(j\), \(i\ne j\), and \(ij\notin E(G)\). Let

\[
A_{ij}=\{F_i\subseteq C,\ F_j\cap C=\varnothing\}.
\]

With denominator \(D=\binom NL\), their probability numerators are

\[
p_{ij}=\binom{N-a_i-a_j}{L-a_i}. \tag{2}
\]

For two distinct pair-events \((i,j),(k,\ell)\), their intersection is empty unless every left row is disjoint from every right row. The original pairs already satisfy two of these conditions; the additional requirements are \(F_i\cap F_\ell=\varnothing\) and \(F_k\cap F_j=\varnothing\), with repeated cross-side indices forbidden. When these conditions hold, put

\[
a=\begin{cases}a_i&i=k,\\a_i+a_k-w_{ik}&i\ne k,\end{cases}
\qquad
b=\begin{cases}a_j&j=\ell,\\a_j+a_\ell-w_{j\ell}&j\ne\ell.\end{cases}
\]

The exact intersection numerator is

\[
p_{ij,k\ell}=\binom{N-a-b}{L-a}. \tag{3}
\]

Impossible binomial coefficients are zero. Let \(W\) be the weight of a maximum spanning forest on these pair-events, weighted by (3). Then

\[
\Pr(\text{marked vertex critical})
 \le \frac{\sum p_{ij}-W}{D}. \tag{4}
\]

**Proof.** Equations (2) and (3) count subsets containing a prescribed left set and avoiding a disjoint prescribed right set. For events indexed by vertices of a forest, the number of present vertices minus the number of forest edges with both ends present is at least the indicator of a nonempty present set. Taking expectations gives the forest union inequality. Maximizing its correction proves (4). This is Hunter's classical inequality [2] applied to the *pair-events*, not merely to the original hyperedges. No triple-incidence information is needed for (3).

Holding the support \(G\) fixed while replacing its positive weights by zero only decreases (3), hence can only increase the bound (4). This gives a valid upper estimate for all weight assignments on a fixed support graph. The support still specifies which cross-side intersections are forbidden. Monotonicity follows directly from Pascal's identity when either required union size is decreased.

## 4. Complete finite subdivision of overlap matrices

In all seven link problems used here, distinct free sets intersect in at most three points: two size-four rows come from distinct edges with the same marked trace, and there is at most one size-three row. Thus \(1\le w_{ij}\le\min(a_i,a_j,3)\) on \(G\).

Two further necessary realizability conditions are used. First,

\[
\sum_{ij\in E(G)}w_{ij}\ge e, \tag{5}
\]

since \(\binom c2\ge c-1\) at every free vertex. Second, for any row \(i\) and any independent subset \(S\) of its neighbors in \(G\), the sets \(F_i\cap F_j\), \(j\in S\), are disjoint, so

\[
\sum_{j\in S}w_{ij}\le a_i. \tag{6}
\]

These are necessary conditions only. Passing them does not assert realizability.

A finite cutoff handles all dense overlap graphs without enumeration. Start with the pair sum assuming every distinct pair of rows is disjoint. For an unordered row pair \(ij\), let \(h_{ij}\ge0\) be the sum of its eligible oriented numerators (2). A positive overlap deletes exactly these witnesses. If \(G\) has at least \(K\) edges, its pair sum is at most

\[
\sum h_{ij}-\text{the sum of the }K\text{ smallest }h_{ij}. \tag{7}
\]

Choose the first \(K\) for which (7), divided by \(D\), is strictly below the desired threshold. All supports with fewer than \(K\) edges are then enumerated as follows.

Begin with the empty graph on zero vertices. At each step append one vertex with every possible neighborhood among previous vertices, retaining the edge cutoff. Canonicalize by sorting vertex degree classes and minimizing the edge list over all permutations within these classes. This canonical form is invariant under graph isomorphism. Induction by deleting the last vertex of any labeled graph proves that every graph under the cutoff is represented. No random generation, solver, or external graph catalogue is used. Assign the multiset of row types to its vertices in every distinct way. Enumerate every positive integer weight assignment in the stated ranges, discarding only (5) or (6). If the zero-weight forest bound already succeeds, it covers every assignment on that support and row assignment without iterating their weights.

This is a certified exhaustive subdivision of every possible link in the endpoint problem. It does not assume that the surviving overlap matrices represent actual set families.

## 5. Exact incidence reconstruction at the only residual geometry

There is a general exact way to decide which covering families realize an overlap matrix. Every nonsingleton incidence column is a clique of \(G\). For every clique \(Q\) with \(|Q|\ge3\), enumerate its nonnegative integer column multiplicity, limited by the remaining row capacities and pair weights. Once these columns are chosen, each two-row column has the uniquely determined residual pair multiplicity. Fill unused row capacity with singleton columns. Retain the family precisely when capacities are nonnegative and

\[
\sum_Q n_Q(|Q|-1)=e. \tag{8}
\]

This enumerates every incidence matrix realizing the prescribed sizes, union size, and pair weights, up to labels of the free vertices. Conversely each retained matrix realizes these data. Identical columns are distinct vertices with the same incidence signature. This is a general realizability and exact-union framework; it is not limited to the present link sizes.

For a reconstructed matrix, enumerate the colors of its nonsingleton columns. Each row's remaining vertices are private to it. A dynamic program chooses how many private vertices lie in \(C\), weighted by the corresponding binomial coefficient, and tracks the total left size and the existence of a left and a right witness. It counts the critical event exactly.

The only matrix not closed by (4) occurs for \(N=21,L=10\), one row \((3,1)\), and six rows \((4,3)\). Three size-four rows form a triangle with all weights two; the other four rows are isolated. The four residual records differ only in the placement of the size-three row among the isolated vertices. Their pair-weight sum is six, equal to \(e\). Equation (8) forces the triple-column multiplicity to be zero. Thus the three overlapping rows are the unions of pairs from three disjoint two-element sets. All other rows are disjoint and private. There is exactly one incidence type for each record.

Its exact critical-event numerator is

\[
49068\quad\text{out of}\quad\binom{21}{10}=352716,
\]

or \(4089/29393\), below the required threshold \(4103/27132\). The verifier checks this by the incidence dynamic program; the audit independently enumerates all \(352716\) subsets of the actual 21-vertex realization.

## 6. Combining links with the unmarked tails

A critical vertex before the marked block requires an edge avoiding the block wholly on the left. A critical vertex after it requires an edge avoiding the block wholly on the right. There are \(33-d\) such edges for a single degree-\(d\) mark and exactly \(33-7-7+1=20\) for the pair (1).

Use the packing-sensitive tail-forest bound \(T(N,L,r,n)\) proved in Section 2 of the [preceding link-envelope proof](../link_envelopes/proof.md). For completeness it is

\[
T=np-(n-1)q_0-\sum_{t=1}^{r-1}\max(0,n-K_t)(q_t-q_{t-1}),
\]

where \(p=(\binom Lr+\binom{N-L}r)/\binom Nr\),

\[
p_i=\frac{\binom{N-2r+i}{L-2r+i}+\binom{N-2r+i}L
+2\mathbf1_{i=0}\binom{N-2r}{L-r}}{\binom NL},
\]

\(q_0=\min_{0\le i<r}p_i\), and \(q_t=\min_{t\le i<r}p_i\). The integer \(K_t\) is the largest positive \(c\) satisfying
\(c\binom rt\le\binom Nt\) and
\(N\binom a2+ba\le(t-1)\binom c2\), where \(cr=Na+b\), \(0\le b<N\). These bound the number of components of successive intersection graphs; applying the forest inequality gives \(T\). Its existing implementation and checks are reused without modification.

The certified maximal link bounds, including all dense and sparse branches, are:

| Vertex count | Marked link | Dense cutoff K | Sparse weighted matrices checked | Link bound |
|---:|---|---:|---:|---:|
| 20 | degree 7 | 5 | 2 | 15099/92378 |
| 20 | degree 8 | 9 | 11467 | 17759/92378 |
| 21 | degree 7 | 5 | 131 | 672/4199 |
| 22 | pair (1), flag 1 | 4 | 0 | 708/4199 |
| 22 | pair (1), flag 2 | 4 | 0 | 708/4199 |
| 23 | pair (1), flag 1 | 6 | 2128 | 335/2261 |
| 23 | pair (1), flag 2 | 6 | 317 | 17707/117572 |

Zero-weight forest certificates cover the additional support/row assignments recorded in `expected.json`. Zero in the weighted column means that every admissible support was closed before weights needed enumeration. The final sums of tail and link bounds are:

| Whole class | Maximum failure bound |
|---|---:|
| 20 vertices, minimum degree 7 | 46066/46189 |
| 20 vertices, minimum degree 8 | 91855/92378 |
| 21 vertices | 8367/8398 |
| 22 vertices | 8253/8398 |
| 23 vertices | 351419/352716 |

Every fraction is strictly below one. Thus every remaining candidate has a successful ordering. Together with the reduction in Section 1, this proves the unrestricted theorem.

## 7. Verification, novelty, and limitations

`python3 verify.py` regenerates all graphs, row assignments, admissible weight assignments, residual incidence matrices, and exact probability bounds, then compares the complete output to `expected.json`. The computation uses Python 3.11+ and its standard library, with no floating arithmetic, solver, input graph catalogue, or omitted large certificate. Run without `-O`, because assertions enforce the proof obligations. The full theorem also uses the two previous verifiers; `python3 verify_all.py` runs all three and records their output hashes.

The audit checks every labeled graph through five vertices against the recursive graph catalogue, exact incidence-envelope maxima for 3,490 labeled covering families in 22 overlap-matrix classes, and 800 direct critical-event counts with arbitrary sizes and flags. Of the latter, 239 have a positive forest correction. It also directly checks the full 21-vertex residual family. These checks use a different counting representation, but are not independent peer review or formalization. Completeness rests on the written reductions and the published enumeration code. The trust boundary includes that source, the Python interpreter, and hardware.

Grill–Linzmayer [1] already developed the discrete greedy and marked-vertex method and proved \(m(5)\ge32\). Hunter's inequality [2], Kruskal's algorithm, and incidence representations are classical. The strengthening here is the matrix-based forest on *all oriented link-pair events*, its combination with a complete sparse-support subdivision and clique-incidence reconstruction, and the unrestricted consequence \(m(5)\ge34\). This machinery was needed to close the whole endpoint, rather than merely to extend a trace table.

The numerical bound is new to the primary sources searched. The numerical tables of the 2026 overview [4] remain inaccessible; its reference list also cites an unpublished-looking 2024 heuristic upper-bound item. Neither is treated as numerical evidence or a definitive priority clearance. No independent peer review is claimed. We have not decided 34-edge existence or improved the upper construction.

## References

1. K. Grill and D. Linzmayer, *Improved Lower Bounds for Property B*, arXiv:2403.05674v3, 20 June 2024, [primary full text](https://arxiv.org/html/2403.05674v3), especially Sections 2–3 and Theorem 1.
2. D. Hunter, *An upper bound for the probability of a union*, Journal of Applied Probability 13(3) (1976), 597–603, [publisher record](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/S0021900200104164), DOI 10.2307/3212481.
3. S. Aglave, V. A. Amarnath, S. Shannigrahi and S. Singh, *Improved bounds for uniform hypergraphs without property B*, Australasian Journal of Combinatorics 76(1) (2020), 73–86, [primary PDF](https://ajc.maths.uq.edu.au/pdf/76/ajc_v76_p073.pdf), Section 1.1 for the 51-edge construction.
4. K. Grill and D. Linzmayer, *An Overview of Property B*, in *Sum(m)it280*, Bolyai Society Mathematical Studies 32 (2026), [publisher record](https://link.springer.com/chapter/10.1007/978-3-032-18810-6_9), DOI 10.1007/978-3-032-18810-6_9. Accessible metadata and references only.
