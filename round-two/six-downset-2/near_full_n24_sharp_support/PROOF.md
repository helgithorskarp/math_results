# Least proper support cutoff six for the n24 capped near-cube

Actual author **six-downset-2**, role **researcher**, 2026-10-02.
Status: exact rational author certificate and an ordinary proof. The real
congruence, harmonic completeness and kernel arguments are unformalized.
Independent review of this new construction is pending.

## Quantified claim

Fix the ORIGINAL downset, including its actual empty vertex and loop,

```
D={A subset[24]: |A|<=22}, F=D\{empty},
N=16777191, m=N-1=16777190, s=8388584, h=N-s=8388607.
```

Every point star has size s. There is an explicit rational real symmetric
matrix M, defined by [seed.json](seed.json) and the decoding below, with

```
M*1=1, M[A,B]=0 if A intersection B is nonempty,
0 <= L=h*M+s*I <= N*I,
N*I-L >= (1/64)*(I-J_N/N).
```

Its lower rank is the greatest possible H rank **N-24=16777167**.
Its cap rank is N-1, and the unit eigenvalue of M is simple. Every other
eigenvalue is at most1-1/(64h). The core is noncentered.

For integer k>=0, define S_k to require M[A,B]=0 on every PROPER disjoint
nonempty pair with |A|+|B|<24 and min(|A|,|B|)>k. Complementary pairs are
allowed at every size. The least k for which ANY REAL ORIGINAL capped H
in S_k exists is

```
k_min=6.
```

The minimization has no centering, point-permutation invariance,
rationality, sign, rank or quantitative-gap hypothesis. Our positive
witness is invariant and rational; the lower bound imported from9471
already applies to every real original capped H. This closes the earlier
6<=k_min<=7 bracket in [the n24 S7 packet](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_n24_cap/PROOF.md).
Its S7 matrix and continuum of repairs remain valid.

This is a finite n24 architectural optimum under the extra cap. It does
not classify centered S6 feasibility, optimize the cap gap or positive
mass, give an all-n positive family, or resolve general H/I. Disjoint
entries can have either sign. Tight H follows because L has nonzero
kernel and hence lambda_min(M)=-s/h; the weighted Hoffman expression is
N*(s/h)/(1+s/h)=s.

The defining primary literature is [Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
Its [version record](https://arxiv.org/abs/2609.28404) was checked live
2026-10-02; it still lists the September23 v1 and H/I remain proposed
conjectures. The published proof of ordinary Chvatal is prior art.

## Exact table and the full star face

There are143 supported symmetric pairs 1<=a<=b<=22 with a+b<=24.
The121 free pairs are ALL those with a>=2. Their rational values are
listed in seed.json and share denominator10^9. No float defines a value.
Put beta_ab=0 when a+b>24, and symmetrize the free entries. For a=2..22,
and then for a=1, solve

```
beta_1a=[(24-a)*s-sum(b=2..22,b*beta_ab*C(24-a,b))]/(24-a),
beta_11=[23*s-sum(b=2..22,b*beta_1b*C(23,b))]/23.
```

[affine.py](affine.py) checks all22 equations

```
sum(b=1..22,b*beta_ab*C(24-a,b))=(24-a)*s.
```

For an excluding-point row, divide by24-a to obtain
sum_b beta_ab*C(23-a,b-1)=s. An including-point row contributes s-s=0
without any disjoint table term. Thus EVERY individual point star is
annihilated. All singleton coordinates are eliminated with nonzero
divisors, so these formulas cover the entire real star-only affine face;
no zeroth-moment/centering equation is included. Exact RREF of the143
coordinates independently has rank22 and the same121 free coordinates.
This algebraic coverage statement holds over R; finite audits are not a
proof by enumeration of real matrices.

Exactly30 free coordinates are the proper pairs with a>=7 and a+b<24;
every one is zero. Thus the table lies in S6, with91 active free
coordinates. The nonzero core row sums are recorded exactly in
[expected.json](expected.json). Noncentering follows also from the exact
degree-zero nullity1: cardinality is a kernel vector, and the constant
coefficient vector is independent of it.

## Whole original matrix and the empty row

For A,B in F, define

```
C[A,B]=s*1_(A=B)-1+beta_|A|,|B|*1_(A intersection B=empty),
E=[-1_m'; I_m], L=J_N+E*C*E', M=(L-s*I_N)/h,
U=N*I_m-J_m-C.
```

These formulas retain the actual empty entries:

```
L[empty,A]=1-(C*1)_A,
L[empty,empty]=1+1'*C*1.
```

The checker evaluates every layer's core row sum and these empty values
exactly, and confirms the entire layer-aggregated original row equations.
Since E'*1_N=0, L*1_N=N*1_N. On nonempty diagonals L=s and on distinct
intersecting pairs L=0. Empty entries, including the loop, are permitted
by intersection support. Hence M meets the original row/support conditions.

The columns of E span1_N-perp, E'*E=I_m+J_m, and

```
N*I_N-L=E*U*E', rank(L)=1+rank(C).
```

The added J_N acts on a space orthogonal to the image of E. Thus the
whole lower positivity is equivalent to C>=0, and the whole cap to U>=0.
These are ordinary real congruence statements, not numerical estimates.
If U>=I_m/64, then
E*U*E'>=EE'/64>=(I_N-J_N/N)/64 because the nonzero eigenvalues of EE'
are1 and N. This gives the full original cap gap and simple unit
eigenvalue, including the empty row. No mean corner is removed from U.

## Complete harmonic certificate

On Boolean layers, lowering D and its adjoint raising R satisfy
DR-RD=(24-2a)I on layer a. Successive raising/lowering decomposes each
layer orthogonally into harmonic degrees j. The harmonic space at j has
dimension d_j=C(24,j)-C(24,j-1), with C(24,-1)=0. Indeed,
raising below the middle is injective since the commutator gives
||R f||^2=||D f||^2+(24-2a)||f||^2>0. Its adjoint lowering is
surjective onto the preceding layer, giving this kernel dimension. For harmonic q on j-sets,
put q_a(A)=sum(S subset A, |S|=j, q(S)). Induction using the commutator
gives squared norm C(24-2j,a-j)*||q||^2, with support j<=a<=24-j.
The telescoping sum of harmonic dimensions equals every layer dimension.
Consequently these spaces span the WHOLE nonempty core, including all
above-middle layers and degree12; there is no truncation of directions.

Summation over disjoint b-sets gives

```
sum(B disjoint A, |B|=b,q_b(B))
 = C(24-a-j,b-j)*sum(S subset A^c, |S|=j,q(S))
 = (-1)^j*C(24-a-j,b-j)*q_a(A).
```

For the complement identity, expand products of(1-1_(i in A)). Terms
of degree less than j vanish by harmonic lowering. Thus on each copy
of degree j=0..12, layers max(1,j)<=a<=min(22,24-j) have metric
g_a=C(24-2j,a-j)>0 and coefficient matrices

```
K_j[a,b]=s*1_(a=b)-1_(j=0)*C(24,b)
          +(-1)^j*beta_ab*C(24-a-j,b-j),
U_j[a,b]=N*1_(a=b)-1_(j=0)*C(24,b)-K_j[a,b].
```

The physical symmetric forms are G_j*K_j and G_j*U_j, G_j=diag(g).
Every degree has order

```
22,22,21,19,17,15,13,11,9,7,5,3,1
```

and multiplicity

```
1,23,252,1748,8602,31878,92092,211508,
389367,572033,653752,534888,208012.
```

Their weighted order sum is m=16777190. Both integer Bareiss and
independent rational Schur checking establish, in EVERY degree,

```
G_j*K_j >=0, rank=d-1 for j=0,1 and rank=d for j>=2,
G_j*(U_j-I/64)>0, rank=d.
```

The exact lower kernels are the cardinality coefficient vector(a) in
degree0 and the constant coefficient vector in degree1. In particular
the degree-zero lower block has only ONE required kernel, and the FULL
22-order upper block is checked. A centered two-kernel compression would
be invalid here. The weighted core nullity is1+23=24, precisely the
independent point stars, so rank(C)=N-25 and rank(L)=N-24.

For completeness, N-24 is an absolute H rank bound on this downset.
For any real original H, its L=hM+sI is PSD and L1=N1. A full star
indicator y_i has y_i'Ly_i=s^2 by intersection support. Therefore
(y_i-s1/N)'L(y_i-s1/N)=0, and PSD makes each such centered star a kernel
vector. They are independent: the empty coordinate first forces the sum
of coefficients zero, and the singleton coordinates then force each
coefficient zero. Hence rank(L)<=N-24 even without the upper cap. Our
certificate attains this bound, not just a favorable sampled rank.

## Sharp cutoff and prior evidence

[LEMMA9471](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_growth/PROOF.md),
artifact `bafkreie5bbft5yrw72p4cxr46lgvyc3t5h4abxjcdtbvtmryjpkrvaevsm`,
forces a POSITIVE original proper disjoint entry with both sizes>=6 in
EVERY real original capped H at n24. Its finite sufficient scalar is

```
B=sum(a=3..5,a^2*C(24,a))=1250832,
s-12*24^2=8381672, 6B<=8381672.
```

Thus S5, and every S_k contained in it, are impossible, without a
centering or invariance assumption. Our S6 gives the matching upper
bound. The necessary theorem was independently confirmed and strengthened
by [REVIEW9513](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/near-middle-mass-audit/REVIEW.md).
That review gives no verdict on THIS new matrix; its stronger all-n mass
bound is not a premise for our finite optimum.

As an original-entry check, the packet sums positive beta_ab/h over ALL
unordered proper disjoint pairs with both sizes>=6. Each class has count
C(24,a)*C(24-a,b), halved exactly when a=b. The exact total and every
positive class appear in expected.json and exceed the credited1/1152
lower bound. Every such class now touches layer6. This is original entry
mass, not a normalized coefficient or harmonic norm. No least-mass claim
is asserted.

Specifically beta_66=780391/250000000>0 and the exact total positive
original mass is166653712846621/131071984375000. The actual empty scaled
diagonal is L[empty,empty]=195179316200979/25000000.

The [9365 star-only packet](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_pair_separation/PROOF.md)
supplies the direct/RREF affine decoder; here only its imported parameter
tuple adapter changes. The [9521 packet](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_n24_cap/PROOF.md)
supplies model.py and exact.py copied unchanged and the selected literal,
harmonic and arithmetic controls copied verbatim into baseline.py. Its
prior [9017 n16 construction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md)
supplies the underlying harmonic, empty-lift and exact-PSD method.
Prior independent n16 review9123 is context, not a new n24 verdict.
Structural/star/ordinary-near-cube graph7578/7627/8106 remain credited
context. No separate mathematical premise from a different downset
family is imported.

## Reproduction and trust boundary

The current pass reproduced the whole9521 record exactly, hash
`efa2bc3323f37d238eb8530f9882ebee32327ff1e20727f2f7f20cd8536a1713`.
That replay is validation. The increment is the rational S6 witness and
sharp least cutoff, greatest H rank and whole cap gap1/64.

The standalone checker uses CPython3.12.14, standard-library integers
and fractions.Fraction. All26 sector forms, all22 star equations,
both exact affine decoders, full dimensions/ranks, empty rows and
original positive entry classes are checked. Positive elimination pivots
are exact congruence steps; a zero-diagonal residual must be identically
zero. Both PSD algorithms must agree. All729 symmetric ternary3x3
matrices match a separate all-principal-minor criterion, with24 PSD.

Credited literal n6 controls check BOTH original57-order endpoints,
including a noncentered repair, every entry's row/support/star behavior,
the actual empty loop and lower/upper ranks. The harmonic control proves
literal harmonic dimensions1,5,9,5, full56-coordinate span, ALL112 action columns and
6272 positions, including degrees2,3 and above-middle layers. These are
definition-level code controls; the ordinary harmonic argument above
supplies n24 completeness. Twelve semantic damage controls remain active
under python-O and reject bad rational data, domain/census/support,
damaged lower PSD, wrong empty loop and forbidden original n24 allocation.

The entire deterministic record is frozen in expected.json. Reproduction
commands and its exact hash appear in the [README](README.md). Ordinary
mathematical bridges remain unformalized and this extension is independently
unreviewed. Matching same-author algorithms is not an independent-person
verdict.

Optional CVXPY1.7.4/Clarabel0.11.1 floating optimization proposed the seed.
An unconditioned negative objective FAILED dual stationarity. Invertible
congruences, referenced to the known S7 sectors, and free-variable scaling
then found a positive proposal, still marked optimal_inaccurate. The
published certificate is rational and every defining claim is rechecked
exactly without those packages. No negative solver status, floating
eigenvalue, timeout, incomplete search or large-order extrapolation proves
nonexistence. Fixed1CPU2GiB/native1/one mathematical job and the existing
45s guard suffice; no original16777191-order matrix is materialized.
