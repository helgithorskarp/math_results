# Incidence realizability proves m(5) ≥ 35

11 September 2026. Exact computer-assisted mathematics.

**Theorem.** Every finite simple 5-uniform hypergraph with at most 34 edges has Property B (a vertex coloring with no monochromatic edge). Hence

\[
35\le m(5)\le51,
\]

where \(m(5)\) is the smallest edge count of a non-two-colorable finite simple 5-uniform hypergraph. The upper bound is from the primary literature [3]. The exact value, and existence at 35 edges, remain unresolved here.

The new ingredients are necessary incidence-realizability conditions, complete integer-box certification of link bounds, and exact counting by inclusion–exclusion over incident rows. They close the **entire 34-edge endpoint**. The [preceding 33-edge proof](../incidence_forests/proof.md) and all earlier source remain unchanged. The present proof reuses their general lemmas and implementations, but does not assume their numerical lower bounds.

## 1. Probability bounds used by the certificate

Start all vertices red, process an ordering, and turn a vertex blue if it is last in an otherwise red edge. No red edge survives. If a blue edge survives, its first vertex was turned blue by an edge whose last vertex it is. These two edges intersect only there. Thus failure requires a *critical vertex*: last in one edge and first in another. This is the established greedy mechanism used by Grill–Linzmayer [1].

Fix \(s\le4\) marked vertices consecutively in the center, and uniformly permute the other \(N=v-s\) vertices. Exactly \(L=\lfloor N/2\rfloor\) free vertices are before the block; their set \(C\) is a uniform \(L\)-subset. Let \(x_A\) count edges whose intersection with the marked set is \(A\). At a marked vertex each incident edge has a free row \(F_i\) of size \(a_i=5-|A_i|>0\). Flag bit 1 says all its other marks precede this vertex; bit 2 says they all follow it. A mark is critical precisely when

\[
\exists i,j:\quad f_i\mathbin\&1\ne0,\quad f_j\mathbin\&2\ne0,
\quad F_i\subseteq C,\quad F_j\cap C=\varnothing. \tag{1}
\]

Pair coverage guarantees that these rows cover every free vertex, including for rows with flag zero. A critical free vertex before the block requires an edge avoiding all marks entirely on the left; after the block, entirely on the right. There are \(x_\varnothing\) such edges. Consequently

\[
\Pr(\text{some critical vertex})\le
 T(N,L,5,x_\varnothing)+\sum_{u\text{ marked}} B_u, \tag{2}
\]

where \(B_u\) bounds (1), and \(T\) bounds the union of the monochromatic-side events for the edges avoiding the block. A strict bound below one proves colorability.

The packing-sensitive forest formula \(T\) and its proof are in [the link-envelope proof, Section 2](../link_envelopes/proof.md). Explicitly, for \(m\) distinct \(r\)-sets,

\[
 T=mp-(m-1)q_0-\sum_{t=1}^{r-1}\max(0,m-K_t)(q_t-q_{t-1}),
\]

where \(p=(\binom Lr+\binom{N-L}r)/\binom Nr\),

\[
 p_i=\frac{\binom{N-2r+i}{L-2r+i}+\binom{N-2r+i}L
 +2\mathbf1_{i=0}\binom{N-2r}{L-r}}{\binom NL},\quad
 q_0=\min_{0\le i<r}p_i,\quad q_t=\min_{t\le i<r}p_i.
\]

The integer \(K_t\) is the largest positive \(c\) satisfying
\(c\binom rt\le\binom Nt\) and
\(N\binom a2+ba\le(t-1)\binom c2\), where \(cr=Na+b\), \(0\le b<N\).
These bounds limit the components of successive edge-intersection graphs. Hunter's forest union inequality [2] gives the displayed formula. Impossible binomial coefficients are zero; \(T=0\) for \(m=0\).

The verifier also uses the earlier exact permutation coefficient bound `model.bound`, which sums per-position minima of the left, right, and ordered-pair union bounds. It uses the covering-link signature enumeration for excess at most four in `star_envelope.envelope`, and its conditional per-position combination `bounds.envelope_bound`. These general lemmas and enumeration completeness arguments are proved in [the original proof](../proof.md) and [the link-envelope proof](../link_envelopes/proof.md). A projection to fewer marks or any ordering of the marks remains a valid certificate. No least-degree assumption is needed for a coloring bound itself.

## 2. Necessary conditions for actual incidence families

Write \(w_{ij}=|F_i\cap F_j|\), and let \(G\) have edge \(ij\) exactly when \(w_{ij}>0\). Put \(e=\sum_i a_i-N\). The rows here have sizes at most four. Size-four rows at one marked vertex have the same singleton trace and are distinct, so

\[
1\le w_{ij}\le\min(a_i,a_j,3). \tag{3}
\]

Smaller rows are allowed to coincide; (3) does not exclude this.

**Realizability lemma.** Every such covering family satisfies all of the following.

1. \(\sum w_{ij}\ge e\). For any independent subset \(S\) of the neighbors of \(i\), \(\sum_{j\in S}w_{ij}\le a_i\).
2. Within each component of \(G\), the union has size at least the sum of the sizes of any independent collection of rows, and at least \(a_i+a_j-\min(a_i,a_j,3)\) for an adjacent pair (or \(a_i+a_j\) for a nonadjacent pair). The sum of these component lower bounds is at most \(N\).
3. Every forest in \(G\) has total overlap weight at most \(e\), hence so does a maximum spanning forest.
4. The augmented matrix

\[
\Gamma=\begin{pmatrix}W&a\\a^T&N\end{pmatrix}\succeq0,
\qquad W_{ii}=a_i,\quad W_{ij}=w_{ij}. \tag{4}
\]

**Proof.** A point in \(c\) rows contributes \(c-1\) to \(e\) and \(\binom c2\) to the pair-weight sum. Independent neighboring rows have disjoint intersections within row \(i\). Rows from different components are disjoint, proving the component assertion. At each point, the forest induced on its incident rows has at most \(c-1\) edges; sum over points to prove assertion 3. Finally (4) is the Gram matrix of the row incidence vectors and the all-ones vector on the free vertex set. These are necessary conditions, not a claim that a surviving matrix is realizable. ∎

`realizability.py` tests (4) with exact symmetric Schur complements. A negative diagonal rejects; a zero diagonal requires its whole row to be zero. For a positive pivot \(p\), the remaining matrix is replaced by \(pA_{ij}-A_{i0}A_{0j}\). Removing a positive common integer factor preserves positive semidefiniteness. This avoids numerical tolerances.

## 3. Complete link-bound certification

For each eligible ordered disjoint pair of rows let \(A_{ij}\) be the event in (1). Its count, with denominator \(D=\binom NL\), is

\[
p_{ij}=\binom{N-a_i-a_j}{L-a_i}.
\]

The intersection of events \((i,j),(k,\ell)\) is empty unless each left row is disjoint from each right row. Otherwise its numerator is
\(\binom{N-a-b}{L-a}\), where \(a=|F_i\cup F_k|\), \(b=|F_j\cup F_\ell|\); repeated same-side rows count only once. These sizes are determined by the overlap matrix. Hunter's inequality gives

\[
 B\le (\sum p_{ij}-\text{maximum event-forest weight})/D. \tag{5}
\]

This is the incidence-forest lemma proved in [the preceding proof, Section 3](../incidence_forests/proof.md). Holding the positive support fixed, increasing overlap weights decreases the required same-side union sizes, so the event-intersection counts increase. The maximum forest weight increases. Thus (5) is **nonincreasing** in the positive overlap weights. A box's lower corner therefore bounds every assignment in the box.

`certificates.json` contains only row sizes, flags, \(N,L\), and the claimed bound \(B\). The production verifier reconstructs a complete proof of each bound as follows.

First use a dense cutoff. Assuming all pairs disjoint gives a sum \(H=\sum h_{ij}\), where \(h_{ij}\) includes both eligible orientations. Every supported pair deletes its \(h_{ij}\). A support with at least \(K\) edges has pair sum at most \(H\) minus its \(K\) smallest summands. Choose the first \(K\) making this less than the requested threshold. Enumerate every support with fewer than \(K\) edges.

For completeness of the graph catalogue, append one vertex with every possible neighborhood, inductively from zero vertices. Canonicalization starts with degree colors and repeatedly refines them by the vector of neighbor counts in each color class. These classes and their order are invariant under isomorphism. Minimize the edge list over all orders within the final classes. Vertices with identical open neighborhoods, or identical closed neighborhoods, are twins; interchanging them is an automorphism. Keeping their relative order therefore omits no edge-list minimum. Deleting one vertex of an arbitrary graph proves that the construction covers every graph under the cutoff. Assign all distinct permutations of the row-type multiset to every support.

For a support and row assignment, use the component lower bounds first, then consider the complete integer box (3). Propagate the independent-neighbor capacity inequalities and the lower bound on total overlap. Reject a box if the maximum overlap-forest weight at its lower corner exceeds \(e\). If (5) at that corner is below threshold, the whole box closes. Otherwise split one nonconstant coordinate into every integer value. At a singleton box apply the exact Gram test and, if it passes, the incidence reconstruction below. No timeout, sampling, solver, or heuristic omission is present in the production verifier.

The stored bounds have integer numerators on denominator \(D\). Each is verified with strict threshold \(B+1/D\), which proves the asserted weak bound \(B\). The largest support catalogue used has eight rows and 2,481 graphs with at most eleven edges. Both the dense branch and every sparse branch are included.

## 4. Exact reconstruction and row inclusion–exclusion

Every nonsingleton incidence column is a clique of \(G\). Enumerate the nonnegative multiplicity of each clique of size at least three, subject to remaining row capacities and pair weights. The residual pair weights then determine all two-row columns; fill remaining row capacities with singleton columns. Retain precisely the nonnegative fillings satisfying

\[
\sum_Q n_Q(|Q|-1)=e. \tag{6}
\]

This gives exactly all covering incidence families with the prescribed data, up to relabeling free vertices. Every actual family gives one such multiplicity assignment, and each retained assignment is a realization. Repeated columns represent different vertices with identical incidences. This complete reconstruction is inherited from the preceding incidence-forest framework.

The new event counter works on rows instead of coloring every shared column. For nonempty eligible left-row subsets \(I\) and right-row subsets \(J\), put \(U_I=\bigcup_{i\in I}F_i\) and similarly \(U_J\). Inclusion–exclusion gives the exact numerator

\[
\sum_{\substack{\varnothing\ne I\subseteq\mathcal L,\ \varnothing\ne J\subseteq\mathcal R\\U_I\cap U_J=\varnothing}}
 (-1)^{|I|+|J|}\binom{N-|U_I|-|U_J|}{L-|U_I|}. \tag{7}
\]

Indeed multiply the two inclusion–exclusion expansions of the indicators that at least one left event and one right event occur. Terms requiring a point on both sides vanish. Precompute row-subset unions; for each \(I\), enumerate only right subsets disjoint from \(U_I\). Positive row sizes imply \(I\cap J=\varnothing\), giving at most \(3^d\) terms for \(d\) rows. This made the eight-row residual calculations practical.

For example, take eight four-sets. Two disjoint triples of rows each consist of pairwise unions of three disjoint two-element sets; the two remaining rows are private four-sets. The union has 20 vertices. Formula (7) gives exactly 29,972 critical 10-subsets out of 184,756. The verifier's audit compares this to the earlier column-color dynamic program, and compares 120 general families to that program and direct subset enumeration.

## 5. Reduction to a finite whole-endpoint decision

Identify two vertices sharing no edge and coalesce any duplicate edges. Uniformity and noncolorability are preserved: a coloring of the quotient lifts to the original. Iterate to a pair-covered quotient. On at most eight vertices a balanced coloring works immediately. On at least nine vertices there are enough distinct 5-sets to pad to exactly 34 edges, preserving pair coverage. A pair-covered vertex has degree at least \(\lceil(v-1)/4\rceil\). For \(v\ge26\), the degree sum is at least 182, exceeding 170. Only \(9\le v\le25\) remain.

For \(9\le v\le16\), the balanced-coloring union bound is strictly below one. The tail-forest formula at 17 and 18 vertices gives respectively \(12017/12155\) and \(12026/12155\). At 19 vertices, the earlier one-anchor forest bound, checked for every possible minimum degree 5 through 8, has maximum \(12047/12155\). All are recomputed here.

For \(20\le v\le24\), start with three least-degree vertices. If their degrees are \(a\le b\le c\), use the complete ranges

\[
\lceil(v-1)/4\rceil\le a\le\lfloor170/v\rfloor,\quad
 a\le b\le\lfloor(170-a)/(v-1)\rfloor,\quad
 b\le c\le\lfloor(170-a-b)/(v-2)\rfloor.
\]

Enumerate positive pair codegrees and every triple codegree between zero and their minimum. Möbius inversion determines all eight trace counts. Discard only a negative count or a marked vertex with insufficient free incidences to cover the free set. `model.profiles` implements exactly these ranges.

| Vertices | Initial three-mark traces | Treatment |
|---:|---:|---|
| 20 | 2,985 | All close by the coloring bounds |
| 21 | 2,496 | All close by the coloring bounds |
| 22 | 497 | All but three close; structural four-mark closure below |
| 23 | 350 | All close by the coloring bounds |
| 24, minimum degree 6 | 50 | Complete fourth-mark extensions close |
| 24, minimum degree 7 | 165 | Whole class closes structurally below |

The following single-vertex bounds are useful at 20 and 21 vertices; they hold for **any** vertex of the stated degree, irrespective of whether it has minimum degree.

| Vertices | Degree | Critical-vertex bound |
|---:|---:|---:|
| 20 | 7 | 12355/92378 |
| 20 | 8 | 7672/46189 |
| 21 | 7 | 553/4199 |
| 21 | 8 | 7560/46189 |

Each is added to \(T(v-1,\lfloor(v-1)/2\rfloor,5,34-d)\), with sum strictly below one. All other link certificates in the table are recomputed by the same complete procedure.

**The 22-vertex class.** The only unclosed three-mark traces, in binary-mask order, are

```
[19,3,3,2,3,2,2,0]
[18,4,4,1,4,1,1,1]
[17,5,5,0,5,0,0,2]
```

Each has three degrees seven and all three pair codegrees two. Minimum degree six is already excluded by the other traces. A minimum-degree-seven candidate has at least \(22-(170-7\cdot22)=6\) vertices of degree seven. Any three of them can be the least-degree marks, by tie choice. Hence **every pair** in this pool has codegree two. Choose four.

Let their quadruple codegree be \(q\in\{0,1,2\}\), and enumerate the four exact triple traces from 0 through 2. Each exact pair trace is 2 minus \(q\) and its incident exact triple traces. The singleton traces follow from degree seven; the empty trace follows from 34 edges. Exactly 26 labeled nonnegative vectors result. Every one closes by (2) or the inherited bounds. Thus the entire 22-vertex class closes.

**The 24-vertex class, minimum degree six.** If a three-mark trace fails the initial coloring tests, append the fourth least-degree vertex, with degree from the third degree through \(\lfloor(170-a-b-c)/21\rfloor\). Split every old trace count in all possible ways according to incidence with this mark. This yields 5,594 raw extensions. Discard only a trace of size greater than five, an uncovered marked pair, insufficient marked-to-free incidences, or insufficient free-pair capacity \(\sum_A x_A\binom{5-|A|}{2}<\binom{20}{2}\). Exactly 613 remain, all closed by a projection or the four-mark bound. Every actual candidate follows one of these branches.

**The 24-vertex class, minimum degree seven.** At least \(24-(170-7\cdot24)=22\) vertices have degree seven. On this pool join pairs with codegree greater than one. At a degree-seven vertex the sum of codegrees is 28, while all 23 other vertices require at least one. Thus this graph has maximum degree at most five. Greedy independent-set selection gives four degree-seven vertices all of whose pair codegrees are one, because \(22>3(5+1)\).

The traces of size at least two on these four vertices partition the pairs of \(K_4\) into cliques. There are exactly three types: six pairs; one triple and its three remaining cross pairs; one quadruple. Singleton counts are seven minus the number of incident blocks. All three close. Their pilot central-block bounds were \(91565/92378\), \(91109/92378\), and \(6685/7106\); the production verifier is free to find an earlier successful projection.

**The 25-vertex class.** Minimum degree is six, and at least \(25\cdot7-170=5\) vertices have degree six. Each is spanning and linear: its 24 free incidences cover all 24 other vertices once. Select four of them. Their pair codegrees are one, giving the same three clique-partition types, now with singleton degree six. The existing exact conditional envelope closes every type, with maximum \(793/798\), as already proved in the [spanning-link theorem](../link_envelopes/proof.md). This check is repeated here.

Every possible quotient vertex count has now been excluded. This proves the theorem.

## 6. Reproduction, attribution, and limits

Run `python3 verify.py` in this directory, with Python 3.11+ and its standard library, without `-O`. It recomputes all stored link bounds, every trace and structural closure, and the controls, then compares the complete deterministic output to `expected.json`. The output is not accepted merely because it matches a hash: all inequalities, enumeration branches, and structural conditions are asserted during its production. No solver, external graph catalogue, omitted proof trace, or large artifact is required. Prior numerical theorem outputs are not premises.

Controls compare 400 symmetric-matrix PSD decisions with all principal minors; check all necessary conditions on 426 actual covering families; compare 120 event counts in three representations; compare the recursive graph catalogue against the preceding exhaustive canonicalizer for 347 graph types through seven vertices; and check the 20-vertex two-triangle family. These are implementation controls, not independent peer review or formalization. The trust boundary is the written arguments, published Python source including the inherited general-bound modules, interpreter, and hardware.

The greedy method and fixed-vertex framework are prior art [1]. Hunter's inequality, Gram positivity, Schur complements, incidence columns, inclusion–exclusion, and graph refinement are classical. The contribution is their incidence-sensitive combination with a complete finite proof system and the unrestricted consequence \(m(5)\ge35\). In particular, realization tests and row counting were needed to close complete vertex classes; this is more than a trace inventory.

The strongest accessible external primary lower bound located was 32 [1], with upper bound 51 [3], before this campaign's results. The bound here is new to the primary sources searched. Numerical tables in the 2026 overview [4] were inaccessible; its references also include an unpublished-looking heuristic upper-bound item. These are limitations of priority clearance, not numerical evidence. No independent review or final settlement of \(m(5)\) is claimed.

## References

1. K. Grill and D. Linzmayer, *Improved Lower Bounds for Property B*, arXiv:2403.05674v3 (2024), [primary full text](https://arxiv.org/html/2403.05674v3).
2. D. Hunter, *An upper bound for the probability of a union*, Journal of Applied Probability 13(3) (1976), 597–603, [publisher record](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/S0021900200104164), DOI 10.2307/3212481.
3. S. Aglave, V. A. Amarnath, S. Shannigrahi and S. Singh, *Improved bounds for uniform hypergraphs without property B*, Australasian Journal of Combinatorics 76(1) (2020), 73–86, [primary PDF](https://ajc.maths.uq.edu.au/pdf/76/ajc_v76_p073.pdf), Section 1.1 for the 51-edge construction.
4. K. Grill and D. Linzmayer, *An Overview of Property B*, in *Sum(m)it280*, Bolyai Society Mathematical Studies 32 (2026), [publisher record](https://link.springer.com/chapter/10.1007/978-3-032-18810-6_9). Accessible metadata and references only.
