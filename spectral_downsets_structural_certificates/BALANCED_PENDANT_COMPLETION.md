# One-pendant completion of every balanced downset

**Actual author:** six-downset-1. **Role:** researcher. **Date:** 2026-10-01.

**Status:** complete ordinary author-checked proof, supported by exact finite
validation. The all-order argument is not formalized or independently reviewed.
The Harris correlation inequality and Hall matching theorem used below are
classical baselines; their reproduction is not a new research claim. The
contribution is the one-pendant connected matching construction and explicit
signed perturbation, giving both maximal endpoint ranks and positive weights
from the empty set for arbitrary balanced downsets.

Let D be a finite downset, including the empty set, with N=|D| and largest
coordinate-star size s. A matrix certifies H when it is real symmetric,
has row sums one, vanishes whenever its indexing sets intersect, and
L=(N-s)M+sI is positive semidefinite. Only the empty diagonal may be nonzero.
Here a **cap** means I-M is positive semidefinite. These are the conventions
in [Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
Their September 23 v1 remained the latest listed version when checked on
October 1, 2026; general H and the distinct inertia conjecture I remain open
in that source.

## Quantified lemma

Suppose N=2s, s>=2, and c is a coordinate with a star of size s. For a fresh
point p put

    D[1] = D union {{p},{c,p}},   N* = 2s+2,   s* = s+1.

There is an explicit rational matrix M on D[1] certifying H and the cap,
with

    rank((N*-s*)M+s*I) = rank(I-M) = N*-1.

Both endpoints -1 and +1 are simple. Every empty off-diagonal entry is
strictly positive. The lower rank is maximal among **all real H matrices**
on this augmented family, and its unique largest intersecting family is
the c-star. Negative nonempty weights are allowed.

More explicitly, write E={A in D:c not in A}, |E|=s, and set

    S = {{c} union A:A in E} union {{c,p}},
    T = E union {{p}},
    h = |{(X,Y) in S x T:X intersect Y is empty}|,
    g = 2/[h(N*-1)^2],
    epsilon = 1/[4h(s-1)(N*-1)^2].

The construction below has empty off-diagonal margin at least epsilon and
both I-M and I+M at least g/2 on the orthogonal complement of their two
endpoint vectors. No seed H matrix, PSD hypothesis or symmetry assumption
on E is required.

The same conclusion holds after **every positive number r of pendants**:
apply the lemma to D[r-1] and add the last pendant. Indeed D[r-1] is still
balanced, with chosen star size s+r-1. The displayed constants then use
s+r-1 as the pre-extension star size. The constructor in this package
implements the single-pendant step; iterating it needs no inherited matrix.

This certifies the augmented family. Existence of a routine capped H matrix
for the original balanced D already follows from the classical matching
baseline below, without the asserted ranks or empty weights. Neither this
baseline nor the lemma resolves H on arbitrary original downsets.

## Balanced deletion structure

The map A -> A\{c} injects the c-star into E. Their equal cardinalities
make it a bijection, so

    D = E union {{c} union A:A in E}.

E is a downset on the remaining ground set K. Every coordinate star of any
downset has size at most half its cardinality, by the same deletion injection.
After one pendant the c-star has size s+1, each old other star has size at
most s, and the new p-star has size two. Thus s*=s+1 and c is the unique
largest coordinate when s>=2. S and T partition D[1] into equal parts.

## Classical disjoint matching baseline, with proof

Every finite nonempty downset E admits a bijection f:E->E with
A intersect f(A) empty. We supply the elementary bridge rather than assume
positive association for the uniform measure on E, which need not hold.

On the uniform full cube 2^K, increasing real functions u,v have
nonnegative covariance. Induct on |K|. Splitting the last coordinate into
sections u0,u1 and v0,v1 gives the identity

    Cov(u,v) = [Cov(u0,v0)+Cov(u1,v1)]/2
               + (Eu1-Eu0)(Ev1-Ev0)/4.

Both section covariances and both expectation differences are nonnegative.
The zero-coordinate case is immediate. Applying this to event indicators
also gives nonpositive covariance for an increasing and a decreasing event.
This is the uniform-cube Harris inequality. Its historical primary source
is [T. E. Harris, A lower bound for the critical probability in a certain
percolation process, 1960](https://doi.org/10.1017/S0305004100034241);
publisher metadata was checked, while the proof here is self-contained.

For F subset E let U be its upward closure in the full cube, and let
bar(E)={K\B:B in E}. E is decreasing; bar(E) and U are increasing.
The correlation inequalities give

    |E intersect U|/|E| <= |U|/2^|K|
                        <= |bar(E) intersect U|/|bar(E)|.

The disjoint neighbors of F in E are precisely those B for which
K\B lies in U. Since |bar(E)|=|E|,

    |F| <= |E intersect U| <= |bar(E) intersect U| = |N_disjoint(F)|.

These are Hall's inequalities. For completeness, choose a maximum matching
in the bipartite disjointness graph on two copies of E. If a left vertex is
unmatched, expose alternating paths from it. There can be no reachable
unmatched right vertex, since that would augment the matching. If L and R
are the reachable left and right sets, all neighbors of L lie in R and every
vertex of R is matched to a vertex of L. The unmatched root gives
|L|>|R|, contrary to the inequality. Thus the matching is perfect and yields f.
This is the standard matching criterion of [P. Hall, On Representatives of
Subsets, 1935, Theorem 1](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms/s1-10.37.26).

Applying f between old {c}+E and E gives a symmetric permutation matrix
on D with row sums one and spectrum contained in {-1,1}, so H and its
cap on balanced D are a known elementary consequence. Do not count this
baseline as the present closure result.

## One pendant makes every allowed cross edge usable

Start with f as above. An old left vertex is denoted A, meaning {c}+A,
and the new left vertex is denoted z={c,p}. The new right vertex is p.
For each allowed S/T edge produce a perfect matching containing it:

1. For A->B with A,B in E and B!=f(A), put C=f^{-1}(B), so C!=A.
   Replace A->f(A), C->B by A->B, C->p, z->f(A).
2. For A->f(A), choose any C in E other than A, possible because s>=2.
   Retain A->f(A) and replace C->f(C) by C->p, z->f(C).
3. For A->p replace A->f(A) by A->p, z->f(A).
4. For z->B put C=f^{-1}(B), replacing C->B by C->p, z->B.

In each case retain every unspecified old f-edge. The targets are all
distinct and exhaust T, and every new pair is disjoint: p is fresh, while
z is disjoint from every member of E. Thus these are complete matchings.
There are exactly h conditioned matchings, one for each allowed cross edge.

Let M0 be the average of their symmetric permutation matrices. It is
rational, nonnegative, symmetric, stochastic and supported precisely on
the allowed cross graph; every such edge has weight at least 1/h. This
graph is connected: {c} sees every member of E and p; every old left vertex
sees p; and z sees every member of E.

Let 1 be the global constant and q be +1 on S, -1 on T. Then M0 1=1,
M0 q=-q, and q is orthogonal to 1. The following exact gap proves that
these endpoint eigenspaces are one-dimensional without an irreducibility
or numerical spectral assumption.

## A quantitative complete spectral gap

For any vector v orthogonal to 1,

    ||v||^2 = (1/N*) sum_{i<j}(vi-vj)^2.

Choose any spanning tree of the connected support graph. The difference
along a tree path has square at most N*-1 times the sum of the squared
edge differences along that path, by Cauchy--Schwarz. Bounding each path
by the full tree gives

    ||v||^2 <= (N*-1)^2/2 sum_tree_edges(vi-vj)^2.

Symmetry and stochasticity give the exact weighted Laplacian identity

    v^T(I-M0)v = sum_{i<j}(M0)ij(vi-vj)^2 >= g ||v||^2.

The minimum edge weight 1/h gives the displayed g. Thus I-M0 is PSD,
with kernel exactly span(1) and gap at least g on its complement.
If R is diagonal with entries q, then R M0 R=-M0. Consequently I+M0
has kernel span(q) and the same gap on q's complement. The two constants
and

    Z = span(1,q)^perp

are an exhaustive orthogonal decomposition of the entire N*-dimensional
space. In particular both unperturbed slacks have rank N*-1.

## Positive empty weights from a signed row-zero trade

Within T, for each nonempty Y in E, add the symmetric unit trade

    T0[empty,Y] += 1,    T0[empty,p] += 1,
    T0[p,Y] -= 1,        T0[empty,empty] -= 2.

All unspecified entries are zero. This preserves disjoint support and
zero nonempty diagonal. Every row sum is zero. Since T0 is supported on T,
where q is constant, T0 annihilates both 1 and q. Its maximum absolute
row sum is exactly 4(s-1), attained at empty. Symmetry and
2|vi vj|<=vi^2+vj^2 therefore imply

    |v^T T0 v| <= 4(s-1)||v||^2.

Put M=M0+epsilon T0. Both endpoint eigenvectors survive. Symmetry makes
Z invariant; there both I-M and I+M are bounded below by

    [g-4(s-1)epsilon]I = (g/2)I > 0.

On the two constant lines the slack eigenvalues remain 0 and 2. This
exhausts the space and proves the cap, H, simplicity, and both claimed ranks.

The empty-to-S weights remain at least 1/h. The empty-to-Y weights for
nonempty Y in E are epsilon, and the empty-to-p weight is (s-1)epsilon.
Since epsilon<=1/h, all empty off-diagonals are at least epsilon. The only
negative nonempty weights introduced are the s-1 pairs p/Y, each -epsilon.
The empty diagonal becomes -2(s-1)epsilon and is allowed by H.

This trade differs from requiring a nonnegative H matrix. Its signed
outside weights are essential to the stated implementation; no
nonnegativity assertion is made for the final matrix.

## Maximal rank and the complete equality argument

For any real H matrix K on this same family let L_K=s*(I+K). For an
intersecting family F of t nonempty members, its indicator x satisfies
x^T Kx=0. Since L_K 1=N*1, the centered indicator obeys

    (x-(t/N*)1)^T L_K (x-(t/N*)1) = s*t-t^2.

PSD implies t<=s*. With F equal to the chosen c-star, t=s* and the
centered indicator is nonzero, so PSD forces a kernel vector. Hence
every real H slack has rank at most N*-1, as attained here. This is the
same standard forced-star kernel argument used in the earlier
[empty-coordinate/kernel result](PROOF.md); see graph 7578.

For the constructed M the lower kernel is exactly span(q). If t=s*,
the empty coordinate of x is zero and q_empty=-1, forcing

    x-(1/2)1 = (1/2)q.

Therefore F is exactly S. This argument covers every intersecting family,
not only coordinate stars or families found in the finite census.

At the excluded s=1 balanced input D={empty,{c}}, one pendant leaves two
distinct largest stars. Their centered indicators are independent (both
have the same nonzero empty coordinate and are unequal), forcing lower
rank at most N*-2. After a preliminary pendant the star size is two, so
the lemma provides a two-pendant completion of this boundary input. No
minimum-count assertion for individual inputs with s>=2 is required.

## Scope relative to previous committed work

The arbitrary-downset [affine pendant completion](AFFINE_PENDANT_COMPLETION.md),
graph 8391, guarantees maximal-rank capped H after a sufficient regularizing
count, with signed weights allowed. The present result restricts the input
to N=2s and removes that count threshold: **one pendant suffices**, and
therefore every positive count works. It uses a different proof with no
affine seed or orthogonal extension history. The earlier
[centered nonnegative-core pendant closure](PENDANT_EXTENSIONS.md), graph
8264, requires a seed core and covers different hypotheses; it is contextual
attribution rather than a prerequisite for this argument.

For the three-point full cube the validated affine recipe used 12 total
pendants and a final matrix of order 32. Here one pendant gives order 10,
with both slack ranks 9 and empty margin 1/16524. This is a comparison of
two sufficient constructions; neither number was claimed necessary.
The [independent arbitrary-downset audit by six-reviewer-2](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pendant_completion_review2/REVIEW.md),
committed as graph 8416 at source 48a230ab36aba56ee119e032f6ee596282b3c24d,
confirms the earlier affine completion and proves the smaller uniform bound
p>=2(N-1)^2+s+4. That review is credited context for 8391, and does **not**
review the present one-pendant lemma or its matching/row-zero-trade proof.
No generic tensor-product rank or endpoint-simplicity assertion is made
at density 1/2, and no historical priority or independent acceptance is
inferred from bounded searches or a shared signing identity.

## Reproduce the compact exact evidence

From this directory, with Python 3.11.2 and only its standard library:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  NUMEXPR_NUM_THREADS=1 python3 verify_balanced_pendant.py --check
```

[The constructor](balanced_pendant_completion.py) uses deterministic
augmenting paths for the classical f and the four explicit matching splices.
It stores O(s^2) integers and performs O(s^3) matching-count work, apart from
ground-set bit-operation costs. Its dense helper has an explicit order-64
validation limit. No floating arithmetic or external solver is used.
[The checker](verify_balanced_pendant.py) independently reconstructs literal
row-zero trades, checks every matching and every matrix entry, verifies
complete allowed-edge coverage and minimum weights, and uses exact rational
LDL for the full endpoint slacks and gap-buffered matrices. Definition-level
H and both endpoint vectors are checked. Small forced-edge matchings are
also replayed by direct backtracking, independent of the splice algorithm.

[The expected output](balanced_pendant_expected.json) contains the complete
18 labeled nontrivial downsets E on three ground points, with D={c}+E union E,
plus cube4, cube5, and a center relabeling with a hole in its bit positions.
This is **bounded E coverage**, not a census of arbitrary four-/five-point
downsets. Every record has full final and buffered LDL checks. Hall's
inequalities are checked on all subsets of each original E, up to |E|=16.
The cube5 fixture replays all 113 constructed matchings, but omits independent
forced-edge backtracking and an intersecting-family census at order 34.
Every fixture of order at most 20 has a complete nonempty-vertex intersecting
family census including the empty family. Thirteen malformed-input or
corrupted-certificate controls are rejected.

| Original D | Completed N* | Both ranks | h | Empty margin |
|---|---:|---:|---:|---:|
| cube2 | 6 | 5 | 7 | 1/700 |
| cube3 | 10 | 9 | 17 | 1/16524 |
| cube4 | 18 | 17 | 43 | 1/347956 |
| cube5 | 34 | 33 | 113 | 1/7383420 |

The ordinary all-order Harris/Hall bridge, connected-support gap and
invariant-complement argument are analytic proof steps outside the exact
finite replay. Finite counts and successful LDL checks alone do not prove
the quantified lemma. [The compact source manifest](balanced_source_manifest.json)
lists hashes and all existing transitive local checker imports.
