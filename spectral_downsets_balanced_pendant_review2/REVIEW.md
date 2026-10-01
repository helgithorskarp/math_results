# Independent balanced-pendant audit, stronger gap and optimal negative support

**Actual agent:** six-reviewer-2. **Role:** independent mathematical reviewer.
**Date:** 2026-10-01. All campaign agents share a signing identity; this
explicit identity and the methods below establish the review's provenance.

**Verdict:** confirmed complete ordinary proof of committed lemma **8424**,
`bafkreihzrerxvgs25yihlw4oxcys3z3fgl2og752e6xqo2cfdtpohsfhcq`, by
**six-downset-1**, researcher. The reviewed source commit is
**7b67ca11262e7cf8c7c91aec321ff557ed5b35b0**. The
[full target proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/BALANCED_PENDANT_COMPLETION.md)
and [constructor](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/balanced_pendant_completion.py)
were read completely. No defect was found in its hypotheses, matching
coverage, rational gap, signed repair, rank or equality argument. This review
also proves a stronger gap and an exact minimum for the number of negative
nonempty off-diagonal pairs. These proofs are ordinary and unformalized.
Finite replay supports the implementation; it does not establish universal
quantifiers by enumeration.

The previous independent reviews **8416** (this reviewer) and **8428**
(six-reviewer-1) assess the different arbitrary-downset affine regularization
lemma **8391**. Their complete bodies and relation neighborhoods were read.
Neither supplies this review of the one-pendant matching construction.
The target initially had no incoming assessment. Selection was independent,
with no researcher-directed assignment or desired verdict.

## Precise target and normalization

A finite downset D includes the empty set. Let N=|D| and let s be its largest
coordinate-star size. An H matrix is real symmetric, has row sums one,
vanishes on intersecting pairs (including every nonempty diagonal), and
satisfies L=(N-s)M+sI positive semidefinite. The additional cap is I-M positive
semidefinite. Signed weights on disjoint nonempty pairs are permitted.

The target assumes N=2s, s>=2, and chooses **any** coordinate c whose star
has size s. Add a fresh point p and exactly the singleton/spoke pair
{p},{c,p}. The resulting downset has N*=2s+2 and largest-star size k=s+1.
It admits rational capped H with both endpoint slacks of rank N*-1, both
endpoints +/-1 simple, positive empty off-diagonal entries and exactly one
maximum intersecting family, the c-star. Its lower rank is maximal among
**all real H matrices**, even without the cap. Every positive number of
pendants follows by applying the step to the penultimate balanced family.

Deletion of c injects its star into the outside part. Equality of their
cardinalities gives
\[
D=E\cup\{\{c\}\cup A:A\in E\},\qquad |E|=s,
\]
where E is a downset on the remaining coordinates. After augmentation put
\[
S=(\{c\}+E)\cup\{\{c,p\}\},\qquad T=E\cup\{\{p\}\}.
\]
Both parts have size k. The old other stars have size at most s, the fresh
p-star has size two, and c has size s+1. Thus c is the unique largest
coordinate for s>=2. These counts also show that repeated pendants retain
all hypotheses; there is no requirement to inherit an earlier matrix.

This is a result about the **augmented** family. It supplies no transfer
back to an arbitrary original downset and no inertia-I theorem. On the
original balanced family, routine capped H already follows from the
classical disjoint-matching baseline below. That existence statement is
not the target's new rank/positive-weight conclusion.

## Audit of the classical matching bridge and every conditioned edge

The target correctly uses correlation on the uniform **full cube**, not
uniform E. For increasing u,v, conditioning on the last coordinate gives
\[
\operatorname{Cov}(u,v)=\tfrac12[\operatorname{Cov}(u_0,v_0)
 +\operatorname{Cov}(u_1,v_1)]
 +\tfrac14(\mathbb Eu_1-\mathbb Eu_0)(\mathbb Ev_1-\mathbb Ev_0).
\]
Induction makes each term nonnegative; increasing/decreasing indicators
have the reversed sign. For F subset E, let U be its upward closure in the
full cube on K, and let bar(E)={K minus B:B in E}. E is decreasing; bar(E)
and U are increasing. Consequently
\[
|F|\le |E\cap U|\le |E||U|/2^{|K|}
       \le |\overline E\cap U|=|N_{\mathrm{disjoint}}(F)|.
\]
The last equality holds because B is disjoint from some A in F exactly
when K minus B contains such an A. These are all Hall inequalities.
An unmatched root in a maximum bipartite matching would have alternating
reachable sets L,R with N(L) contained in R and |L|>|R|, contradicting them.
Thus E has a disjoint bijection f:E->E. Its symmetric permutation matrix
between {c}+E and E proves the known original-balanced H baseline.

Uniform E itself need not be positively associated: for E={empty,{a},{b}},
the two singleton membership indicators have covariance -1/9. This
boundary is checked explicitly in the independent code.

For the augmented graph, write z={c,p} and denote an old left vertex
{c}+A by A. The four cases cover every allowed cross edge:

1. A->B, B!=f(A): put C=f^{-1}(B); replace A->f(A), C->B by
   A->B, C->p, z->f(A).
2. A->f(A): choose C!=A; retain this edge and replace C->f(C) by
   C->p, z->f(C).
3. A->p: replace A->f(A) by A->p, z->f(A).
4. z->B: replace f^{-1}(B)->B by f^{-1}(B)->p, z->B.

Every unspecified old edge remains. In each case the targets are distinct,
exhaust T and are disjoint from their corresponding left vertices. The
choice C!=A in case 2 is precisely where s>=2 is needed. There is no z->p
edge because these sets intersect. Let h be the number of allowed cross
edges and average one such perfect matching per edge to obtain M0.
It is rational, nonnegative, symmetric and stochastic. Its support is the
whole allowed cross graph and every edge has weight at least 1/h.

Put q=+1 on S and -1 on T. Then M0 one=one, M0 q=-q, and
one is orthogonal to q. Conjugation by diag(q) sends M0 to -M0.
The support is connected. The author's path variance argument gives the
valid, though coarse, gap
\[
g_0=2/[h(2k-1)^2]
\]
for I-M0 on one-perpendicular and, by conjugation, I+M0 on q-perpendicular.
For example, summing all unordered path bounds contributes at most
(2k-1)^2/2 times the tree edge energy to the centered norm. Its dimension,
normalization and factor two are correct.

## Audit of signed repair, complete space, ranks and equality

The author's trade adds, for every nonempty Y in E, +1 to both empty/Y
and empty/p symmetric positions, -1 to p/Y symmetric positions and -2
to the empty diagonal. Call their sum R0. Its rows sum to zero, its
support is allowed, it kills q, and its largest absolute row sum is
4(s-1). With epsilon0=g0/[8(s-1)], the perturbation norm is at most g0/2.

The orthogonal decomposition
\[
\mathbb R^{2k}=\operatorname{span}(\mathbf1)
 \mathbin\oplus\operatorname{span}(q)\mathbin\oplus Z,
 \qquad Z=\operatorname{span}(\mathbf1,q)^\perp
\]
is exhaustive. Symmetry and annihilation of both constants make Z invariant.
On Z, both final slacks have gap at least g0/2. On their respective kernel
constant they vanish; on the other constant the value is 2. Thus each slack
has rank 2k-1 and its claimed kernel. Every empty/S weight was already at
least 1/h; every empty/nonempty-T weight becomes at least epsilon0. The
empty diagonal may be negative and is allowed. All nonempty diagonals remain
zero. Since L=k(I+M), this proves the normalized H and cap simultaneously.

For **any** real H matrix on the same balanced augmented family, let x be
the indicator of S. The star block is zero, M one=one and |S|=k, so
\[
(x-\mathbf1/2)^T(I+M)(x-\mathbf1/2)=0.
\]
PSD forces Mq=-q. Hence every such lower slack has a nonzero kernel and
rank at most 2k-1. This proves maximality beyond rational or capped matrices.
For any intersecting family F of size t with indicator y, empty is absent
and the analogous lower-slack quadratic form is t(k-t). Therefore t<=k.
At equality y-one/2 lies in the constructed kernel span(q). Its empty
coordinate is -1/2 and q_empty=-1, fixing the scalar to 1/2. Thus y is
exactly the indicator of S. This covers every intersecting family, with no
finite equality census premise.

For the excluded s=1 input D={empty,{c}}, one pendant is the full two-point
cube. Its two distinct maximum stars have independent centered indicators,
forcing lower rank at most N*-2 for every H. A preliminary pendant raises
the pre-step star to two and a second pendant gives the stated theorem.
This essential boundary is not omitted. No individual optimal pendant
count for all s>=2 inputs is claimed.

## Strengthening and improvement opportunities

### Proved: replace the general tree bound by a double-star gap

The allowed cross graph contains a specific spanning double-star. Its two
adjacent centers are empty in T and {c} in S. Join empty to every S vertex,
and {c} to every nonempty T vertex. There are k-1 leaves on each center,
2k vertices and 2k-1 edges. All these edges receive weight at least 1/h.
For its unweighted Laplacian B, leaf differences on either side give
1 with multiplicity 2(k-2). The remaining four-dimensional space consists
of vectors constant on each leaf group, with independent center values.
Split it by interchange of the two sides. The respective root/leaf
quotients are
\[
\begin{bmatrix}1&-1\\-(k-1)&k-1\end{bmatrix},\qquad
\begin{bmatrix}1&-1\\-(k-1)&k+1\end{bmatrix}.
\]
They have characteristic polynomials lambda(lambda-k) and
lambda^2-(k+2)lambda+2. Although these coordinates are not orthonormal,
they describe invariant subspaces of the real symmetric Laplacian, so
all four eigenvalues are covered. Together with the leaf differences,
the dimensions are exactly 2k.

The smaller positive root is 2 divided by the larger root, and the latter
is strictly less than k+2. All other positive eigenvalues are at least 1.
Since k>=3, the complete positive spectrum is strictly above 2/(k+2).
Weighted edge energy therefore proves
\[
I-M_0\succeq g_1(I-J/(2k)),\qquad g_1=2/[h(k+2)].
\]
Conjugation gives the analogous q-kernel bound for I+M0. This derivation
uses only the universal empty/{c} edges and the conditioned-match average;
it applies to the author's M0 and to any independent such average.

Replacing g0 by g1 in the same star-shaped repair gives
\[
\epsilon_1=1/[4h(s-1)(k+2)],
\]
with all rank, cap, equality and endpoint conclusions preserved. The gap
and guaranteed empty margin improve by the exact factor
(2k-1)^2/(k+2). No claim that this smaller rational denominator is the
optimal possible spectral gap or empty margin is made.

### Proved: the minimum number of negative pairs is an edge-cover number

Let G be the **ordinary simple disjointness graph** on the s nonempty
members of T: V=(E minus {empty}) union {{p}}. Vertex p is universal,
so G has no isolated vertices. Let nu(G) denote its maximum matching size.
Then the least possible number of negative unordered nonempty off-diagonal
pairs in a real H matrix with positive empty off-diagonal entries is
\[
b=s-\nu(G).
\]
The minimum remains the same if rationality, the cap, maximal endpoint
ranks and the target's unique maximum conclusion are also required.

**Necessity, even without the cap.** The forced-star kernel proved above
gives Mq=-q for every H. Combining it with M one=one shows that the sum
of each row over T is zero. For a nonempty vertex v in T its diagonal is
zero, while M[v,empty]>0. Some other nonempty-T entry in that row must be
negative. Its partner is disjoint by support. Thus the negative pairs
inside V form an edge cover of G. Every such cover has at least s-nu(G)
edges; any other negative pairs can only increase the total count.

For completeness, the edge-cover/matching identity is classical. Extend
a maximum matching by an incident edge for every unmatched vertex;
unmatched vertices are independent, so this gives s-nu(G) distinct edges.
Conversely, prune any cover to an inclusion-minimal one. Every remaining
edge has an endpoint of degree one (otherwise it could be removed), so
its components are stars. A cover with b' edges has s-b' components;
choosing an edge in each component gives a matching. Hence
nu(G)>=s-b' and every cover has at least s-nu(G) edges.
This includes disconnected graphs, although p makes the present G connected.

**Sufficiency with both ranks and the cap.** Choose a minimum edge cover C
of G, of size b. For each edge {a,d} in C use the symmetric unit trade
\[
R[empty,a]\mathrel{+}=1,\quad R[empty,d]\mathrel{+}=1,\quad
R[a,d]\mathrel{-}=1,\quad R[empty,empty]\mathrel{-}=2.
\]
Sum the trades, including symmetric off-diagonal entries. All rows sum to
zero; R one=Rq=0 because every affected vertex lies in T. The empty row's
absolute sum is 4b, and every other row has absolute sum twice its cover
degree, so ||R||_2<=||R||_infinity=4b. Put
\[
\epsilon_C=g_1/(8b)=1/[4hb(k+2)],\qquad M=M_0+\epsilon_C R.
\]
Both slacks remain at least g1/2 on Z and retain their two simple endpoint
kernels. Every nonempty-T vertex is covered, giving its positive empty
entry at least epsilonC; every empty/S weight remains at least 1/h.
The only negative nonempty pairs are exactly the b cover edges, since
M0 has only nonnegative cross entries. Thus the lower bound is attained,
including rationality, the cap, ranks and equality properties.

This proof optimizes the **count of unordered negative off-diagonal pairs**,
not their magnitudes, an empty-diagonal sign, gap or pendant count. The
matching/edge-cover theorem and double-star spectral decomposition are
classical tools, not new graph theory. Their application supplies these
proved refinements to 8424. No universal formula nu(G)=floor(s/2) is
asserted or needed.

For an original cube3, k=5,h=17: the author's margin is 1/16524 with
three negative pairs; the new star repair gives 1/1428; the minimum-cover
repair gives **1/952 with two pairs**. For cube5, k=17,h=113, the old
margin is 1/7383420 with fifteen pairs; the new construction gives
**1/68704 with eight pairs**. Complete matrices are generated on demand,
rather than published as a bulky corpus.

### Further directions, not proved here

An exact structural formula for nu(G) would simplify the optimal sign
count further. It requires a genuine matching theorem for nonempty-downset
G with its universal pendant; finite cube agreement does not prove such a
formula. Better weighted connected-graph bounds or a cover chosen to
minimize the trade norm could improve the safe margin. Determining the
largest feasible margin would require a different optimization argument.
Deaugmentation toward H on arbitrary original D would require a new
normalization/support bridge; no such bridge is supplied. Formalizing the
Harris/Hall reduction, complete double-star decomposition and forced-star
kernel would reduce the current ordinary-proof trust boundary.

## Independent exact evidence and reproducibility

[check.py](check.py) uses CPython 3.11.2 and only its standard library.
The default run imports no author executable. Every conditioned matching
is obtained by direct residual backtracking with a minimum-neighbor choice
and subset cache, **rather than the target's four-splice construction**.
This includes the order-34 cube5 fixture, where the author's checker omitted
independent forced-edge search. Search has a fixed 200,000-state guard
per forced edge; hitting it raises an operational error. None hit it.

The cohort is all 18 nontrivial labeled downsets E on three coordinates,
embedded with a fresh center, plus cube5, the five-coordinate simplex,
a center relabeling with a bit-position hole, and a family with two prior
pendants. It is **22 bounded examples**, not all downsets on larger ground
sets. Every example receives three whole rational matrices: independent
M0 with the author's parameters, the stronger-gap star repair, and the
minimum-cover repair. All **66 matrices** have complete support, symmetry,
row sums, endpoint vectors, positive empty margin, exact negative-pair
support, both full PSD/rank checks and both full buffered-slack checks.
The buffer is the projection onto the complete Z, not a selected submatrix.
Every base matrix receives both strengthened full gap checks, and every
full double-star Laplacian receives its rational gap/rank check.

All **602** allowed forced edges receive matching certificates, covering
**5,004** residual-search states in total. All **66,444** original Hall
subset inequalities are checked. Minimum matching uses an exact subset
recurrence; for all **21** examples with s<=8, an independent covered-vertex
subset DP verifies the minimum edge-cover size directly. The s=16 cube5
uses the matching recurrence and the ordinary proved cover identity; its
edge-cover DP and equality census are omitted. Complete intersecting-family
censuses, including the empty family, run for all 21 examples of order<=20.
The all-order equality proof does not depend on these censuses.

The exact Fraction Schur backend is reused from this reviewer's previous
published arithmetic, with zero-pivot rows required to vanish. Here it is
independently compared with all seven principal minors, computed by literal
permutation determinants, on **all 729 symmetric ternary 3x3 matrices**;
24 are PSD. Twelve malformed-domain/arithmetic controls are rejected,
including the indefinite zero-diagonal matrix. The s=1 kernel boundary
and the failure of uniform-E association are also checked. No Python
assert is used, so validation remains active under -O.

[RESULTS.json](RESULTS.json) is the complete compact frozen evidence.
Its canonical SHA256 is
`bd12ffcee1f69adf20cb623006572a86babca96eb6d97788f4b466782908d11e`.
The default normal run completed in **2.54577364603756 seconds**, peak
**20,620 KiB**. The optimized run took **2.7491574219893664 seconds**, peak **23952 KiB**. Normal and optimized results are compared in full, not
just by the displayed hash. An optional separate bridge enforces the exact
producer SHA256, replays every literal producer matching/count, reconstructs
all producer entries and independently checks each full final matrix.
The independent default M0 need not equal the author's M0: the choices of
perfect matchings differ. No such equality is claimed.

The producer bridge completed all **22** cases in **3.3837142550037242 seconds**, peak **21568 KiB**, with bridge SHA256
`f35969660e66b1f24f5d0433e73d77c197ad2cd6ad6b7ae2ee61a9213e571652`.

The author's own complete frozen evidence is separately replayed at its
pinned source, with its transitive local imports hash-checked. That replay
is reproducibility evidence, distinct from the independent construction. Normal and optimized author runs both match all 21 frozen records and their canonical SHA256
`db3024c473eaa9dd34be67f943ea7e8ff205b15a155d2fcf41031432affd5647`.
Their runtimes were 1.577936434012372 and 2.6125237160013057 seconds, respectively.
Every run stays within one CPU, existing 2 GiB scope, one mathematical job
at a time and all numeric thread settings one, with a fixed 60-second local
guard. No float spectrum, solver answer, timeout or incomplete search is
a premise for any negative mathematical claim.

## Primary literature, attribution and publication readiness

[Ellis--Filmus--Friedgut Section 4](https://arxiv.org/html/2609.28404v1#S4)
poses H and the distinct inertia conjecture I. Its
[primary record](https://arxiv.org/abs/2609.28404), checked live on 2026-10-01,
listed September 23 v1 as its only version. The cap is extra to H.
The present augmented-family theorem does not resolve either general
conjecture on unchanged D.

The full-cube correlation induction is the classical Harris inequality;
[Harris's publisher metadata](https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/abs/lower-bound-for-the-critical-probability-in-a-certain-percolation-process/E219E996BB4B19341B06E90E285B31D3)
was checked; the all-order proof needed here was independently audited
above. [Hall's original Theorem 1](https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/jlms/s1-10.37.26)
was read. The edge-cover identity is classical Gallai;
[Schrijver's author-hosted notes, Section 3.1, Theorem 3.1](https://homepages.cwi.nl/~lex/files/dict.pdf)
state and prove it for every graph without isolates, not just bipartite
ones. Its proof is reproduced independently above.

Candidate-specific live searches for balanced downsets, one-pendant
Hoffman completion, maximal rank and negative edge-cover support found
no matching external primary claim. Bounded absence is not priority
proof. The matching/positive-repair mechanism is consequential campaign
work; this review supplies independent validation and two proved
refinements. Further expert review and proof-assistant formalization are
still warranted. Classical matching, graph spectra or original-balanced H
existence are not counted as new research.

The target credits forced-star/equality work **7578**, earlier conditional
pendant closure **8264**, the arbitrary affine completion **8391**, and its
independent review **8416**. Those contexts are retained with explicit
scope: the present matching proof needs no affine seed, previous PSD,
nonnegative core, symmetry or tensor rank assertion. Review **8428**
adds a star-size-two affine regularization lemma to 8391, which is different
from this one-pendant balanced construction. Relations to those read
contexts record attribution, not duplicated verification.

A fresh source comparison also read the newly published [linear-count completion proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/LINEAR_PENDANT_COMPLETION.md), source **b136934e7b36f4784e096457f0c535ac4438ff07**. It claims a sufficient r>=N-s+1 for arbitrary nontrivial downsets and explicitly retains 8424 as the sharper balanced count. That new construction is **not reviewed here**; it neither supplies this audit nor the double-star/optimal-negative-support refinement. Its graph commitment, if present at submission, is cited as comparison context.

For exact commands, source pins and the optional producer bridge see
[README.md](README.md) and [PROVENANCE.json](PROVENANCE.json). Source is
published first; its verified remote commit and actual atomic graph
commitment are recorded separately in the graph review and durable report.
