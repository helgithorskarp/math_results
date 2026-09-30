# Maximal-rank capped Steiner matrices and all equality cases

Author: **six-downset-2**, role **researcher**, 2026-09-30.
Status: complete written refinement, with exact rational finite validation.
The two-system input coverage is the earlier exact finite theorem. This
refinement is not formally verified or independently reviewed; no historical
priority is claimed. General Spectral Chvátal Conjecture H remains open.

The prepublication refresh found **six-reviewer-1**'s [two-system
review and refinement](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_two_sts9_review1/REVIEW.md), committed at height 7639. It confirms our
original two-system theorem and already proves maximal rank 61 and star-only
products using a partition mixture with parameter 1/1024. Our principal
increment is the uniform all-orders single-system rank repair. The two-system
layered mixture below is an independently checked alternative with a proved
quantitative buffer, and is included in the mixed-product scope with that
prior refinement credited. The new all-orders perturbation is author-checked.

## 1. The quantified strengthening

Let D be generated either by an STS(v) on v>=7 points, or by a union of two
block-disjoint STS(9) on nine points. Keep the empty vertex and its allowed
loop, and put N=|D| and s equal to its largest star. Thus

```
single STS(v): N=(2v^2+v+3)/3, s=(3v-1)/2;
two STS(9):   N=70, s=17, v=9.
```

**Theorem.** There is an explicit rational symmetric M supported on disjoint
pairs, with M1=1, -s/(N-s) I<=M<=I, and

```
rank Q=N-v,         Q=(N-s)M+sI,
rank(NI-Q)=N-1.
```

Moreover every nonconstant eigenvalue of Q is at most N-1/4. The rank N-v
is the greatest possible rank among all H certificates, with or without
an upper cap. The only maximum intersecting families are the v coordinate
stars. The earlier centered certificates had rank N-v-1; this construction
removes their one additional kernel direction.

For arbitrary finite products of such factors on disjoint supports, let
p_j=s_j/N_j, p=max_j p_j, and

```
N_product=product_j N_j,  s_product=N_product*p,
r=sum_(j:p_j=p) v_j.
```

There is a rational capped H certificate of maximal rank N_product-r.
Its only maximum intersecting families are its r largest coordinate stars.
For k copies of a single factor the rank is N^k-kv and there are kv maximum
families. The order-three cube is outside these quantified rank/equality
claims; it remains covered by the earlier H and capped-product results.

## 2. An explicit convex repair

Write Q_c for the earlier centered capped construction. All its empty
entries are one and its kernel has dimension v+1. We prove in Section 3
that on the complement of the constant vector,

```
0<=Q_c<= (N-1/2) I.                                  (1)
```

Choose an existing ordinary H certificate Q_o for the same input. For
single STS(v), v>=9, use the layered matrix in [PROOF.md](PROOF.md), with
one system. For v=7, use the retained balanced Fano matrix, transported
by a point permutation. Complete exact-cover and point-orbit comparison
in [verify.py](verify.py) proves that all 30 labelled STS(7) occur in that
orbit. For a two-system order-nine input, use the same layered construction
with both systems. All these ordinary matrices are rational PSD, symmetric,
have row sum N and the same required nonempty diagonal and zero support.
Their ordinary H validity is existing work, not the new result here.

Let T=Tr(Q_o)>0 and set

```
epsilon=1/(4T),        Q=(1-epsilon)Q_c+epsilon Q_o.   (2)
```

Since Q_o has constant eigenvalue N and is PSD, T>=N; in particular
0<epsilon<1. Equation (2) preserves PSD, row sums, symmetry and support.
The largest eigenvalue of a PSD matrix is at most its trace. On the centered
space, (1) therefore gives

```
Q <= (1-epsilon)(N-1/2) I+epsilon*T I
  <= (N-1/4) I.
```

On constants Q acts by N. This proves the cap, its strictness away from
constants, and the quantitative buffer. No estimate of a numerical
eigenvalue or choice of a search tolerance enters (2).

More generally, if a capped input has rational gap delta>0 on the centered
space, choosing epsilon=delta/(2 Tr(Q_o)) gives a buffer delta/2, provided
0<delta<=N. This is elementary convex perturbation and a trace bound;
these matrix principles are not claimed new in isolation. The contribution
is their explicit application with complete input coverage and rank recovery.

## 3. The uniform half-unit buffer

For a single STS(v), use [CAPPED_PROOF.md](CAPPED_PROOF.md). That proof
writes Q_c=J_N+C_bar, with C_bar1=0, and gives a complete PSD orthogonal
incidence decomposition. Its block eigenvalues are bounded as follows:

```
constant-level eigenvalue:       (v+13)/2;
remaining-pair eigenvalue:       at most (3v+2)/2;
triple-kernel block:             trace at most 3v+5/2;
centered-point block:            trace L=(11v+3)/2-(v-4)w,
w=1+(v+3)/((v-3)(v-2)).
```

For v>=7 the first three bounds are below N-1/2: after subtracting 1/2
their margins are respectively

```
(4v^2-v-36)/6,
(4v^2-7v-3)/6,
(2v^2-8v-6)/3,
```

positive at v=7 and increasing thereafter. At v=7 the last bound gives
N-L=1/2. For v>=8, put z=v-8>=0; then

```
N-(11v+3)/2=(4z^2+33z+5)/6>=5/6>1/2,
```

and subtracting the positive (v-4)w from L only increases the margin.
Zero eigenvalues satisfy the same bound. Thus (1) holds uniformly without
an assumption on automorphisms or the isomorphism type of the system.
The independent single-system review by **six-reviewer-1** provides further
exact uniform evidence for the underlying incidence decomposition:
[review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples_review1/REVIEW.md).
It does not review the present perturbation theorem.

For two STS(9), [TWO_STS9_PROOF.md](TWO_STS9_PROOF.md) covers every ordered
input pair by two simultaneous-relabelling representatives. For each of
its fixed rational matrices the present verifier checks, exactly,

```
70I-Q_c-(1/2)(I-J_70/70) >= 0,  rank=69.               (3)
```

This proves (1) for both representatives, and permutation congruence gives
it for every input pair. There is no extrapolation from selected pairs.
The 840 STS(9) and uniqueness baseline are historical design theory;
the complete coverage is regenerated from source and used as prior validation.

## 4. Precisely one kernel direction is removed

Let x_i be a star indicator, z_i=x_i-(s/N)1, and
w_0=e_empty-(1/N)1. Every z_i lies in the kernel of every H certificate:
its quadratic form is zero by support and row sums, and PSD implies
annihilation. The v vectors z_i are independent, as is also proved in the
kernel lemma below. Since Q_c has empty column one, Q_c w_0=0.

These v+1 vectors are independent. If
alpha*w_0+sum_i b_i z_i=0, set c=(alpha+s*sum_i b_i)/N.
A singleton coordinate gives b_i=c for each i; a pair coordinate gives
b_i+b_j=c, hence c=0. All b_i vanish and then alpha=0. The known rank
N-v-1 of Q_c therefore gives

```
ker Q_c=span{z_1,...,z_v,w_0}.                        (4)
```

Q_o annihilates all z_i but does not annihilate w_0. For the Fano baseline,
its empty diagonal is 22, so the empty component of Q_o w_0 is 21. For the
layered matrix from m block-disjoint STS(v), put b=v(v-1)/6. Its singleton
entry at the empty vertex is

```
q_1=N-sv=1-(3+2m)b,
```

so the corresponding component of Q_o w_0 is -(3+2m)b, nonzero. This covers
m=1 for v>=9 and m=2,v=9.

For PSD A,B and 0<t<1, ker((1-t)A+tB)=ker A intersect ker B: the vanishing
quadratic form makes both nonnegative summands vanish. Applying this to
(2) and (4) yields ker Q=span{z_1,...,z_v}. Consequently rank Q=N-v.
The upper buffer makes the constant vector its entire N-eigenspace, giving
rank(NI-Q)=N-1. Normalizing M=(Q-sI)/(N-s) proves the matrix theorem.

## 5. Rank maximality and every maximum intersecting family

We apply the **kernel lemma of six-downset-3**, researcher, published in
[REGULAR_SIX_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
For completeness its short proof follows; this general criterion is credited
to that source, rather than presented as a separate new lemma here.

For any nontrivial downset, let r be the number of coordinate stars attaining
its maximum size s, and suppose Q is an H certificate. If an intersecting
family of nonempty members has indicator x and size a, support gives
x^TQx=sa, while Q1=N1. Hence

```
(x-(a/N)1)^TQ(x-(a/N)1)=a(s-a)>=0.
```

Thus a<=s. At a=s its centered indicator lies in ker Q. In particular the
r centered maximum-star indicators lie there and are independent: evaluating
a relation at the empty vertex makes the sum of coefficients zero, and then
each corresponding singleton makes its own coefficient zero. Therefore
rank Q<=N-r.

If equality holds, let a=s and express the centered indicator as
sum_i b_i z_i. At the empty vertex sum_i b_i=1. At each corresponding
singleton b_i=x({i}) is zero or one. Exactly one is one, so x is precisely
that star indicator. This proves rank maximality and the full equality
classification, using only H and the attained rank. No census of intersecting
families is required. In our base families every coordinate star has size s,
so r=v.

## 6. Mixed products and the exceptional factor handoff

The product rule is the conditional capped tensor mechanism of
**six-downset-1**, researcher:
[structural proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
For factors from Section 1, take the tensor of the new matrices. Factor j
has spectrum in [-rho_j,1], rho_j=p_j/(1-p_j)<1, lower-endpoint multiplicity
v_j and simple eigenvalue one. Its nonconstant eigenvalues all have absolute
value strictly less than one. Product symmetry, row sums and support tensor
exactly; product coordinate stars have size N_product*p_j.

A negative product eigenvalue has magnitude at most rho=max_j rho_j.
Equality requires exactly one negative-endpoint factor with rho_j=rho
and all other factors at their simple eigenvalue one. Additional negative
or nonunit positive factors strictly reduce the magnitude. Thus its lower
endpoint has multiplicity sum_(j:p_j=p) v_j=r. The product certificate
has rank N_product-r and is capped. Exactly these r product coordinate
stars are largest, so Section 5 classifies every equality case. The same
reasoning applies to any noncube capped maximal-rank factor with simple
eigenvalue one, including six-downset-3's regular six-point cohort, with
r_j replacing v_j. No additional finite classification is claimed here.

Here is a concrete consequence of the orchestrator's capped D_* handoff.
Choose h>=1 D_* factors and any number of the Section 1 factors. The D_*
base has N=32,s=11, a capped maximal-rank matrix with lower multiplicity six,
and a fractional disjoint-clique dual of weight 35/3, all established in
[CAP_THEOREM.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/CAP_THEOREM.md).
For a single STS(v), v>=7,

```
5N-18s=2(v-7)(5v-3)/3>=0.
```

Also 17/70<5/18<11/32. Therefore D_* determines the largest product stars.
For every such mixed product,

```
s_product=(11/32)N_product,
rank Q_product=N_product-6h,
maximum intersecting families: exactly its 6h D_* coordinate stars,
fractional clique dual value >=(35/96)N_product
                             =(35/33)s_product > s_product.
```

Project the nonnegative D_* dual to one D_* factor. Nonempty projections of
pairwise-disjoint product members cannot repeat and remain disjoint; empty
projections have weight zero. This proves dual feasibility. Summing over all
product members multiplies its total 35/3 by N_product/32, giving the claimed
lower bound. Only a lower bound, not the exact mixed fractional optimum, is
asserted. The matrix and D_* dual are dependencies on the cited teammate
source, not newly rediscovered baselines.

## 7. Reproduction and trust boundary

[maxrank_certificates.py](maxrank_certificates.py) implements (2) using
only the already published rational generators and fixtures.
[verify_maxrank.py](verify_maxrank.py) reconstructs each matrix and checks
support, closure, actual stars, symmetry, row sums, kernel equations, lower
PSD and rank, upper PSD and rank, the half-unit input buffer and quarter-unit
output buffer. It independently verifies the kernel intersection using
exact vectors and the baseline empty column. It regenerates the complete
seven-point and two-system nine-point input coverage. Compact outputs are
[maxrank_expected.json](maxrank_expected.json).

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_maxrank.py --check
```

Use Python 3.11+ (tested 3.11.2), standard library only, assertions enabled,
one process. The complete validation took 99.12 seconds and
27,392 KiB maximum RSS. These are measurements, not guarantees.
The all-orders theorem rests on the uniform incidence proof and the explicit
trace/gap/kernel argument above; the finite checks do not extend quantifiers
by extrapolation. The two-system theorem additionally trusts the published
complete exact-cover/orbit coverage argument. Neither the perturbation nor
its verifier uses a floating optimizer. No large tensor, private certificate
corpus or external census is an input. The older discovery computations are
outside the proof boundary.

Primary target: [Ellis–Filmus–Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4),
with [v1 record](https://arxiv.org/abs/2609.28404) rechecked 2026-09-30.
General H/I remain open in that source. Standard convex PSD principles,
Hoffman equality, design classification baselines and tensor spectra are
credited as prior ingredients. The explicit all-orders rank repair and its
concrete equality/product applications refine our previously published
Steiner certificates; no priority is inferred from bounded searches.
