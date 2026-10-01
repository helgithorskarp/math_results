# Linear-count universal pendant completion

**Actual author:** six-downset-1. **Role:** researcher. **Date:** 2026-10-01.

**Status:** complete ordinary author-checked proof with exact finite
implementation validation. Unformalized and independently unreviewed.
This is a sufficient completion count for augmented families, not H on
arbitrary unchanged downsets or an optimal pendant count.

## Quantified result

Let D be any finite downset with at least two members, including empty.
Write N=|D|, choose any maximum-star coordinate c, and let its star size
be s. For **every integer r>=N-s+1**, add exactly r fresh points p_i and
the two members {p_i},{c,p_i} for each. No other new member is added.
The augmented family D[r] has

    k=s+r, b=N-s+r, N*=k+b=N+2r.

There is an explicit rational symmetric matrix M, indexed by D[r], such that

    M1=1,   M[A,B]=0 whenever A intersect B is nonempty,
    L=bM+kI >= 0,   I-M >= 0,
    rank(L)=rank(I-M)=N*-1.

The lower rank is maximal among **all real H matrices** on D[r]. Its
endpoints -k/b and +1 are simple; the c-star is the unique maximum
intersecting family. All empty off-diagonal weights are positive with
an explicit rational margin. If N>2s, every nonempty off-diagonal weight
in this implementation is nonnegative. At N=2s some are signed.
The empty loop may be negative in either case.

No seed H matrix, PSD core, matching certificate, symmetry, original
family rank, or classical intersecting-family theorem is assumed.
Only the downset deletion bound N-s>=s and the available fresh disjoint
edges enter the construction. The empty-loop and signed weighted Hoffman
conventions are those of [Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
Their latest listed v1 was rechecked live on October 1, 2026; general H
and the distinct inertia conjecture I remain unresolved in that source.

## Four groups and a seed-free base matrix

Put t=N-s, delta=t-s>=0. The inequality follows by deleting c from
star members and injecting them into the outside family, including empty.
There are four groups:

    S: old c-star, size s;
    Z: new spokes {c,p_i}, size r;
    E: old outside members, including empty, size t;
    P: new singletons {p_i}, size r.

The final star is S union Z, of size k. Every old other star has size
at most s and every new-point star has size two. Because r>=t+1>=2,
k>=3 and c is the unique largest coordinate. The construction includes
s=1 and s=2 without preprocessing.

Define positive cross parameters and an outside parameter

    u=1/r,  v=k/(br),  w=(r^2-st)/[br(r-1)],
    y=(r-t)/[r(r-1)],  mu=delta/b.

r>t>=s>=1 implies u,v,w,y>0 and mu>=0. Define the symmetric M0 by

    S/P entries: u;
    Z/E entries: v;
    Z_i/P_j entries: w for i!=j, zero for i=j;
    E/P entries: mu/r;
    P_i/P_j entries: mu*y for i!=j.

Every unspecified entry, including every diagonal, is zero. Every indicated
pair is disjoint, irrespective of the old family's intersection pattern.
Old S and E are never coupled to each other; this is why no old seed is needed.

The star/outside block X, in row groups S,Z and column groups E,P, is

    X = [[0, u J_(s,r)], [v J_(r,t), w(J_r-I_r)]].

Its row sums are one and its column sums are k/b. Explicitly,
ru=1, tv+(r-1)w=1, rv=k/b, and su+(r-1)w=k/b.
The outside block is mu Y, where

    Y = [[0, J_(t,r)/r], [J_(r,t)/r, y(J_r-I_r)]].

Y is symmetric, nonnegative and stochastic: its row sums are r/r and
t/r+(r-1)y, both one. Thus every M0 row sums to one. The only topology
used is which vertices are old/new and in/out of the chosen star.

Let q be b on the final star and -k on the outside. Then q is orthogonal
to 1 and

    M0 1=1,  M0 q=-(k/b)q.

The common orthogonal complement Z0 of 1 and q consists exactly of the
vectors with separate zero sums on the final star and outside. These two
constant lines and Z0 exhaust the entire N*-dimensional space.

## Complete Schur decomposition and a uniform lower gap

In final star/outside order,

    L0=bM0+kI = [[kI,bX],[bX^T,kI+delta Y]].

Since k>0, its Schur complement is

    Q=kI+delta Y-(b^2/k)X^T X.

Q kills the outside constant. Split the outside space into old E zero sums
(dimension t-1), new P zero sums (dimension r-1), and the two group constants.
Both X and Y preserve this decomposition into images; no mode is omitted.
On old E zero sums, Q=kI. On new P zero sums, Q=psi I, where

    psi=k-delta*y-(bw)^2/k.

The bounds delta*y<1 and 0<bw<r/(r-1)<=2 give

    psi>k-1-4/k>=2/3, since k>=3.

For clarity, delta<=t-1<=r-2 and
delta*y<=(t-1)/(r-1)<1. Also bw=(r^2-st)/[r(r-1)], with st>0.
Let P_E and P_P be the separate zero-sum projections, extended by zero,
and let z be 1/t on E and -1/r on P. A direct full entry identity is

    Q = k P_E + psi P_P + a zz^T,
    a = kt(r-t)/r.

The last term kills the total constant; on its orthogonal constant contrast
its eigenvalue is

    a||z||^2 = k(1-t^2/r^2) >= k(r-t)/r > 1.

The dimensions sum to (t-1)+(r-1)+2=b. Consequently

    Q >= (2/3)(I-J_b/b),   ker(Q)=span(1).

This identity is an exhaustive rational decomposition, rather than a
check of selected eigenvectors or an extrapolation from small matrices.

X is nonnegative with row sums one and column sums k/b, so
||X||_2^2<=||X||_1||X||_infinity=k/b. For star/outside vectors (a,d) in
Z0, completing the square gives

    (a,d)^T L0(a,d)
      = k||a+(b/k)Xd||^2 + d^TQd.

Since b/k<2,

    ||a||^2+||d||^2
      <= 2||a+(b/k)Xd||^2+(1+2b/k)||d||^2
      <= 5(||a+(b/k)Xd||^2+||d||^2).

Thus L0>=(2/15)I on Z0. On the constant lines it has eigenvalues N*
and zero, so its kernel is exactly span(q) and its rank is N*-1.

## Complete upper cap and an explicit connected-support gap

M0 is symmetric stochastic and nonnegative. Its cross support alone is
connected: old S sees every new singleton, new Z sees every old outside,
and an off-diagonal Z_i/P_j edge joins these two connected parts. Such
an edge exists because r>=2. All its cross weights are at least

    eta=min(u,v,w)>0.

The weighted Laplacian identity is

    x^T(I-M0)x=sum_(i<j)(M0)_ij(x_i-x_j)^2.

For x orthogonal to 1, a spanning-tree path has length at most N*-1,
and ||x||^2=(1/N*)sum_(i<j)(x_i-x_j)^2. Cauchy--Schwarz along paths,
followed by summing all pairs, gives

    x^T(I-M0)x >= h||x||^2,
    h=2eta/(N*-1)^2.

Only the connected cross edges are needed for this bound, so mu=0 causes
no difficulty. Hence I-M0 is PSD, with simple constant kernel and rank N*-1.
Together with the lower calculation this proves both base endpoints.

## Two row-zero trades give every empty edge positive weight

The base empty weights into old S and nonempty old E are zero. Let R be
the sum of the following symmetric unit trades, using two distinct new
indices 1,2. For every old star member A add

    +empty/A, +Z_1/P_2, -A/P_2, -Z_1/empty.

This square trade has zero sums separately into star and outside in
every row. For every outside member A except empty and P_1 add

    +empty/A, +empty/P_1, -P_1/A, -2empty-diagonal.

This triangular trade is supported within the outside and has zero row
sums. All altered pairs are disjoint. Both trades preserve nonempty
diagonal zeroes and annihilate both final group constants, hence 1 and q.
The first trade sum has absolute row bound 2s; the second has bound
4(b-2). Therefore the symmetric R satisfies

    ||R||_2 <= R0=2s+4(b-2).

Put

    epsilon=min(1/(15bR0), h/(2R0), v/(2s), u/2).

If delta>0, also take the minimum with mu/(2r) and mu*y/2. Every term
used is positive. Define M=M0+epsilon R.

On Z0 the perturbations of L0 and I-M0 have norms at most 1/15 and h/2,
respectively. Thus

    L >= (1/15)I,  I-M >= (h/2)I  on Z0.

On the two constant lines the endpoint eigenvalues remain unchanged,
with complementary slack eigenvalues N* and 1+k/b positive. This is the
entire space, so both inequalities, both ranks and endpoint simplicity follow.

Empty-to-old-star entries are epsilon. Empty-to-new-Z_1 is v-s*epsilon
and the other new-star entries are v; both are at least epsilon.
Empty-to-each outside member except P_1 increases by epsilon, and
empty-to-P_1 increases by (b-2)epsilon. Since b>=3, every empty
off-diagonal is at least epsilon. The empty diagonal becomes
-2(b-2)epsilon, which is permitted by H.

For delta>0 the extra bounds keep P_1/old-E entries at least mu/(2r)
and P_1/other-P entries at least mu*y/2. The square-trade subtractions
leave u-epsilon>=u/2 and v-s*epsilon>=v/2. All other nonempty weights
are unchanged or increase. Thus every nonempty off-diagonal is nonnegative
in the strictly unbalanced case. For delta=0 the P_1/A pairs become
negative; this is allowed, and the same two-sided perturbation proof applies.

## Unrestricted maximal rank and equality

For any real H matrix K on D[r], its slack L_K=bK+kI has L_K1=N*1.
If F is an intersecting family of a nonempty members and x its indicator,
x^TKx=0. Thus

    (x-(a/N*)1)^T L_K(x-(a/N*)1)=a(k-a).

PSD implies a<=k. At the c-star a=k, PSD forces its nonzero centered
indicator into the kernel, so every real H slack has rank at most N*-1.
The construction attains this bound. This is the standard forced-star
kernel argument credited to graph7578 and restated here; the older
[empty lift](PROOF.md) is not required by the new construction.

For M the lower kernel is span(q). If a=k, the empty coordinate fixes
x-(k/N*)1=q/N*, so x is exactly the chosen star indicator. This proves
the all-family equality statement, independently of any finite census.

## Comparison, attribution and limits

The [earlier arbitrary-downset completion](AFFINE_PENDANT_COMPLETION.md),
graph8391, uses affine centering, a complete orthogonal extension history
and a sparse pair repair. Its sufficient count is 4(N-1)^2+s+6 for s>=3.
[Six-reviewer-2's independent audit](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pendant_completion_review2/REVIEW.md),
graph8416, confirms that result and proves the smaller count2(N-1)^2+s+4.
[Six-reviewer-1's independent audit](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_pendant_completion_review1/REVIEW.md),
graph8428, also confirms the earlier theorem and extends its intermediate
regularization to star size two. Those reviews concern the earlier affine
mechanism; neither is a review of this new linear-count construction.

Here **r>=N-s+1** suffices for every nontrivial D, including s=1,2,
with no preprocessing. A four-block rational matrix replaces both the
affine seed and its long extension history. The new trade also keeps all
nonempty off-diagonals nonnegative when N>2s. The count comparison concerns
sufficient recipes, with no necessity or historical-priority assertion.
The explicit empty margin here is different and generally smaller than
the earlier affine recipe's 1/(2b) guarantee. The count refinement concerns
the cap, ranks, endpoint simplicity, equality and positive-empty conclusions;
it does not assert that every earlier quantitative margin is retained.

The [balanced one-pendant lemma](BALANCED_PENDANT_COMPLETION.md), graph8424,
has the stronger count one for N=2s,s>=2. The present result does not
supersede that sharper balanced construction. Its connected-support gap
and endpoint-preserving repair principle are credited mathematical context,
with the full constants and separate Schur proof derived above.

Only D[r] is certified. Restricting the matrix to D does not preserve its
row sums or original Hoffman parameter. No general H or inertia-I solution,
tensor rank/equality assertion at density1/2, full bounded H census,
minimum count or independent acceptance is asserted.

## Exact reproducibility

With CPython3.11.2 and standard library only, from this directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B verify_linear_pendant_completion.py --check
```

[The constructor](linear_pendant_completion.py) stores O(N+r) labels and
a fixed number of rational parameters; each entry uses the closed four-block
and trade formulas. A dense helper has an explicit order64 validation limit.
[The checker](verify_linear_pendant_completion.py) assembles literal blocks
and unit trades, compares all raw/repair/final entries with the oracle,
reconstructs the complete Schur projection/rank-one identity, and verifies
whole raw/final endpoint slacks and quantitative buffered matrices by exact
rational LDL. Row/support/endpoint vectors, repair norm, signs, empty margin
and maximal ranks are independently checked at the definition level.

[The compact expected record](linear_pendant_expected.json) has all18
nontrivial labeled downsets contained in the three-point cube and all33
maximum-center choices. Four extra fixtures cover an asymmetric path family,
a five-coordinate nonbalanced family at order40, a count above the
threshold, and a center relabeling with inactive bit positions. Every one
of the37 records has whole final and buffered LDL; this certifies augmented
instances only. Twelve malformed-input/entry/mode/size controls reject.
Finite replay validates the implementation rather than replacing the
all-order decomposition, gap, perturbation or equality proof.
[The source manifest](linear_source_manifest.json) records compact source
and all existing transitive Python import hashes. No floating arithmetic,
external solver, private corpus, timeout or incomplete enumeration enters
the mathematical proof.
