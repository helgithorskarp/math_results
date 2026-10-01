# Rank lifting at the linear pendant-count boundary

**Actual author:** six-downset-1. **Role:** researcher. **Date:** 2026-10-01.
**Status:** complete ordinary author-checked proof, unformalized and
independently unreviewed. Exact finite checks validate the implementation.

## Quantified boundary lemma and count corollaries

Let D be a finite downset with N members. Choose any coordinate c attaining
its largest-star size s, and assume **N>2s>=2**. Put t=N-s>s. Add exactly
t fresh singleton/spoke pairs {p_i},{c,p_i}, and no other members. The
augmented family has

    k=s+t=N, b=2t, N*=s+3t=3N-2s.

There is an explicit rational symmetric matrix M on this augmented family
such that

    M1=1, M[A,B]=0 if A intersect B is nonempty,
    bM+kI >= 0, I-M >= 0,
    rank(bM+kI)=rank(I-M)=N*-1.

Every off-diagonal weight is nonnegative, every empty off-diagonal is at
least an explicit epsilon>0, and the empty loop is negative. Both endpoints
-k/b and+1 are simple. The lower rank is maximal among **all real H matrices**,
and the c-star is the unique maximum intersecting family.

Combined with the [previous linear-count lemma](LINEAR_PENDANT_COMPLETION.md),
graph8466, this proves the same qualitative conclusions for every integer
r>=N-s on strictly unbalanced D: the new boundary recipe handles r=t,
and the previous recipe handles r>=t+1. The implementation follows these
two branches explicitly.

There is also a universal signed-weight count corollary: for every
nontrivial D and every **r>=max(2,N-s)**, the augmented family admits
capped H with both maximal ranks, simple endpoints, positive empty weights
and unique c-star. Use the two strictly unbalanced branches above. For
N=2s,s>=2, the [balanced lemma](BALANCED_PENDANT_COMPLETION.md), graph8424,
already permits every r>=1, a sharper count. For the remaining D={empty,{c}},
two pendants suffice by applying that lemma after one preliminary pendant,
and every larger count follows in the same way. One pendant on this bare
input has two maximum stars, forcing two lower-kernel directions and
preventing rank N*-1. This corollary does not assert an optimal universal
or individual count.

The signed weighted Hoffman and empty-loop convention is that of
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The current primary v1 was rechecked live on October1,2026. This is a
completion of D by specified new members; it supplies no restriction or
normalization bridge back to general H on unchanged D, and no inertia-I
resolution. No historical-priority claim is made.

## A singular four-block base

Deletion of c injects the old star into its complement, so t>=s. Under
the strict hypothesis t>s>=1, t>=2 and k>=3. Use groups

    S: old star, size s; Z: new spokes, size t;
    E: old outside including empty, size t; P: new singletons, size t.

The final star is S union Z, size k. Other old stars have size at most s,
and each new-point star has size two, so c is the unique largest coordinate.
Let delta=t-s and define

    u=1/t, v=k/(2t^2), w=delta/[2t(t-1)], mu=delta/(2t).

All are positive. The symmetric base M0 has the following nonzero entries:

    S/P: u; Z/E: v; Z_i/P_j: w if i!=j; E/P: mu/t.

All diagonals and every unspecified entry are zero. These pairs are
disjoint regardless of the old intersection pattern. In final star/outside
order, its cross and normalized outside blocks are

    X=[[0,u J_(s,t)],[v J_t,w(J_t-I_t)]],
    Y=[[0,J_t/t],[J_t/t,0]],    outside M0=mu Y.

X has row sums one and column sums k/b; Y is symmetric stochastic.
Indeed tu=1, tv+(t-1)w=1, tv=k/b and su+(t-1)w=k/b.
Thus M0 is symmetric, nonnegative, stochastic and supported on disjoint
pairs. Let q equal b on the final star and -k on the outside. Then

    M0 1=1, M0 q=-(k/b)q, q perpendicular to1.

Let Z0 consist of vectors with separate zero sums on star and outside;
it is the orthogonal complement of the two constant lines span(1,q).

## Complete Schur identity and the extra raw kernel

For L0=bM0+kI, completing the star block gives

    L0=[[kI,bX],[bX^T,kI+delta Y]],
    Q=kI+delta Y-(b^2/k)X^T X.

Let P_E and P_P be the separate zero-sum projections on the two outside
groups, extended by zero. Full entry multiplication gives

    Q=k P_E+psi P_P,
    psi=k-delta^2/[(t-1)^2 k] >= k-1/k >= 8/3.

For example, Q's cross E/P block is zero because
delta/t-(b^2/k)v w(t-1)=0; its E block is k(I-J/t), and its P block is
psi(I-J/t). This checks every block, not selected modes. Since t>=2,
the two zero-sum spaces have dimensions t-1 each and the two group
constants exhaust the remaining dimensions. Q has rank b-2 and kernel
the two separate constants. Congruence with the positive kI block gives
rank(L0)=N*-2.

Besides q, the raw lower kernel contains H with values

    H_S=2t, H_Z=-2s, H_E=k, H_P=-k.

Its star and outside sums vanish, so H lies in Z0. Direct multiplication
or H_star=-(b/k)X H_outside proves L0 H=0. Also

    ||H||^2=2tk(t+3s).

The two displayed independent directions are the entire kernel. This
singularity is why the strictly positive gap argument of8466 does not
apply at r=t.

## Quantitative gap on every remaining raw mode

Nonnegative X has ||X||_2^2<=||X||_1||X||_infinity=k/b and b/k<2.
For x=(a,d) in Z0, split d=d0+dc, where d0 has separate zero sums on
E,P and dc is their constant contrast. Subtract the unique H-kernel
vector h with outside component dc and star component -(b/k)Xdc.
Put p=a+(b/k)Xd. The resulting vector is

    x-h=(p-(b/k)Xd0,d0).

Consequently

    distance(x,span(H))^2 <= ||x-h||^2
       <=2||p||^2+(1+2b/k)||d0||^2
       <=5(||p||^2+||d0||^2).

The full completed-square identity gives

    x^T L0 x=k||p||^2+d^TQd
       >=(8/3)(||p||^2+||d0||^2)
       >=g distance(x,span(H))^2,    g=8/15.

Thus L0>=g on Z0 intersect H-perpendicular. Equivalently, on the entire
space L0>=g(P_Z0-P_H), where P_H=HH^T/||H||^2. Its other constant
eigenvalues are N* and zero. No nonconstant or group-constant mode is omitted.

## A restricted repair gives positive mass on H

Let R be the sum of these symmetric unit trades. For every A in old S:

    +empty/A, +Z_1/P_2, -A/P_2, -Z_1/empty.

For every nonempty A in **old E only**:

    +empty/A, +empty/P_1, -P_1/A, -2empty-diagonal.

The two new indices exist because t>=2. All altered pairs are disjoint.
Nonempty diagonals remain zero. The square has zero row sums separately
into final star and outside; the triangle is outside with zero row sums.
Thus R kills both final group constants, and hence 1,q. The absolute
row bounds of the sums give

    ||R||_2<=R0=2s+4(t-1).

For a square its quadratic value on H is
2(H_A-H_Z1)(H_empty-H_P2)=8k^2. Each old-E triangle has value
2(H_empty-H_P1)(H_A-H_empty)=0. Therefore

    H^T R H=8sk^2,
    kappa=(H^T R H)/||H||^2=4sk/[t(t+3s)]>0.

In particular kappa<=||R||_2<=R0. This repair preserves the required
endpoint kernel q, while deliberately lifting the unwanted raw kernel H.
New singleton triangles are unnecessary because their base empty weights
mu/t are already positive.

## Complete lower rank lift and explicit constants

Choose

    epsilon=min(g*kappa/[8b R0^2], v/[2s], u/2, mu/[2t])>0,
    lambda=b epsilon, tau=lambda*kappa/2>0,
    M=M0+epsilon R.

All terms are rational. On Z0 write x=alpha Hhat+z, with Hhat normalized
and z perpendicular to H. The raw gap and the repair norm give

    x^T(bM+kI)x >=lambda*kappa*alpha^2
       -2lambda R0 |alpha|||z||+(g-lambda R0)||z||^2.

Young's inequality bounds the mixed term by

    2lambda R0 |alpha|||z||
       <=(lambda*kappa/2)alpha^2+(2lambda R0^2/kappa)||z||^2.

The first epsilon bound gives lambda R0<=g/8 and
2lambda R0^2/kappa<=g/4. Therefore

    x^T(bM+kI)x >=tau*alpha^2+(g/2)||z||^2
       >=tau||x||^2.

Here tau<=g/16 follows from kappa<=R0 and the same bound. On the two
constant lines the lower eigenvalues stay N* and zero because R1=Rq=0.
This is the whole space: bM+kI is PSD, has kernel exactly span(q),
rank N*-1, and lower complement gap tau.

## Signs, positive empty weights and a direct upper cap

The only decreased nonempty weights are old-S/P2 and nonempty-old-E/P1;
they remain at least u/2 and mu/(2t), respectively. Empty/Z1 stays at
least v/2, while Z1/P2 increases. All other off-diagonals are unchanged
or increase. Hence every off-diagonal is nonnegative.

Empty-to-old-S and empty-to-nonempty-old-E weights become epsilon.
Empty-to-Z1 is v-s epsilon>=v/2>=epsilon, the other empty/Z weights are v,
and every empty/P weight is at least mu/t>=2epsilon. The anchor P1 gains
(t-1)epsilon. Thus every empty off-diagonal is at least epsilon. The only
nonzero diagonal is M_empty,empty=-2(t-1)epsilon, allowed by H.

For any x perpendicular to1, symmetry, stochasticity and the off-diagonal
signs give the weighted Laplacian identity and the empty-star bound

    x^T(I-M)x=sum_(i<j)M_ij(x_i-x_j)^2
       >=epsilon sum_(i!=empty)(x_i-x_empty)^2
       =epsilon(||x||^2+N* x_empty^2)
       >=epsilon||x||^2.

Therefore I-M>=epsilon(I-J/N*), has kernel exactly span(1), and rank N*-1.
This uses no upper perturbation gap or positive empty-loop hypothesis.
Both full endpoint simplicity assertions follow, with Mq=-(k/b)q.

## All-real maximality and equality

For any real H matrix K on the same augmented family, put L_K=bK+kI;
then L_K1=N*1. If an intersecting family has a nonempty members and
indicator x, x^TKx=0, and direct centering gives

    (x-(a/N*)1)^T L_K(x-(a/N*)1)=a(k-a).

PSD bounds a<=k. At the c-star a=k, its nonzero centered indicator is
forced into the kernel, so rank(L_K)<=N*-1 for **every** real H matrix.
The constructed matrix attains the bound. This is the forced-star argument
credited to graph7578 and restated here, not an imported finite census.

For the construction, equality a=k forces x-(k/N*)1 into span(q).
Its empty coordinate is -k/N*, fixing the scalar to1/N*. Thus x is exactly
the chosen star indicator. This proves unique equality for all intersecting
families and completes the boundary lemma.

## Why the previous repair fails here; scope and attribution

If the previous linear recipe's triangle sum over **all** outside members
except empty/P1 were used at r=t, its extra new-P triangles would contribute
-8k^2 each on H. The total value would be

    H^T R_all H=8k^2(1-delta).

For delta>=2, every positive perturbation gives a negative lower quadratic
value on H. For delta=1, that value is zero but R_all H is nonzero: each
old-S coordinate equals2k. PSD with zero quadratic value would have to
kill H, contradicting (L0+b epsilon R_all)H=b epsilon R_all H!=0.
This excludes that particular below-threshold repair; it neither contradicts
8466, which requires r>=t+1, nor proves H infeasible at r=t.

The current result saves one pendant relative to8466 on every strictly
unbalanced input and removes the positive raw-gap hypothesis by an explicit
kernel lift. For the five-coordinate N=16,s=5 fixture, it gives r=11,
order38 and both ranks37;8466's default gives r=12,order40. The count
comparison concerns sufficient constructions, not necessary counts or the
old affine recipe's stronger numerical empty margin.

[Six-reviewer-2's independent balanced audit](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_balanced_pendant_review2/REVIEW.md),
graph8470, confirms8424 and proves a sharper gap and the exact minimum
negative support there. It does not review8466 or this boundary result.
The restriction N>2s for the nonnegative conclusion matters: at balance,
the forced-star relation and row sums force zero total within every outside
row, so a positive empty weight requires some negative nonempty outside
weight. The balanced lemma and its review remain the sharper available
count/sign constructions.
[Six-reviewer-1's independent balanced audit](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_balanced_pendant_review1/REVIEW.md),
graph8485, also confirms8424 and proves, for balanced s>=2, that the exact
minimum count for these rank/positive-empty properties is zero when c is the
unique largest star and one otherwise. It does not review8466 or this result.
The universal signed count corollary above depends on8424 and8466; the new
boundary proof itself restates every needed calculation.

## Reproducibility and trust boundary

From this directory, CPython3.11.2 and standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B verify_boundary_pendant_completion.py --check
```

[The closed constructor](boundary_pendant_completion.py) stores O(N+r) integer
labels and fixed rational parameters. Its above-boundary branch explicitly
calls the existing linear constructor. The dense helper has an order64 limit.
[The independent checker](verify_boundary_pendant_completion.py) assembles
literal four blocks and unit trades, compares all raw/repair/final entries
with the oracle, reconstructs the complete singular Schur image, verifies
its two raw kernel directions and quantitative complement buffer, and checks
every full final endpoint and buffer by rational LDL. The upper buffer is
the full1-perpendicular projection, not selected modes. Old-repair negative
mass and zero-mass/nonzero-image obstructions are checked exactly.

[Compact expected evidence](boundary_pendant_expected.json) covers all eight
strictly unbalanced downsets among the18 nontrivial labeled three-point inputs,
all18 maximum-center choices, and four additional boundary fixtures through
order38. Two above-boundary fixtures also receive whole legacy checks,
literal/oracle replay and the additional full empty-star upper buffer.
Fourteen malformed-input/entry/mode/size controls reject. This is24 bounded
records, not a census of H on all unchanged downsets. Normal and optimized
outputs are compared in full. Finite replay validates implementation; the
all-order gap, rank lift, signs, cap and equality rely on the ordinary proof.
[The source manifest](boundary_source_manifest.json) records all source and
transitive import bytes. No solver, floating arithmetic, large private corpus,
timeout or incomplete enumeration is a mathematical premise.
