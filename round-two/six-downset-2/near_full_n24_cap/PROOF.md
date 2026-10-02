# A capped n24 near-cube with support cutoff seven

Actual author **six-downset-2**, role **researcher**, 2026-10-02.
Status: exact rational author certificate with an ordinary whole-space
proof. The real PSD, harmonic completeness, kernel and convexity arguments
are unformalized. Independent review of this extension is pending.

## Quantified result

Fix n=24 and the original downset

```
D = {A subset[24]: |A|<=22},  F=D\{empty},
N=16777191, m=N-1=16777190, s=8388584, h=N-s=8388607.
```

Every point star has size s. The empty set is an actual vertex with its
permitted loop. The rational table in [seed.json](seed.json) and the exact
completion below define matrices M_t for **every real**

```
0<=t<=1/86856.
```

They satisfy the original conditions of Spectral Chvatal H, and the
additional cap:

```
M_t is symmetric, M_t*1=1,
(M_t)[A,B]=0 whenever A intersection B is nonempty,
0 <= h*M_t+s*I <= N*I.
```

Every proper disjoint nonempty pair with both sizes at least8 has entry0.
Thus all proper disjoint couplings touch a set of size at most7;
complementary pairs are allowed at every size. At t=0 the centered lower
matrix L_t=h*M_t+s*I has greatest centered rank **16777166=N-25**.
At every real 0<t<=1/86856, it has greatest possible H rank
**16777167=N-24**. In the whole original space,

```
N*I-L_t >= (1/8)*(I-J_N/N).
```

Consequently the unit eigenvalue of M_t is simple throughout the interval,
and every other eigenvalue is at most1-1/(8h). The cap rank is N-1.

Define the support architecture S_k by requiring entry0 on every proper
disjoint nonempty pair A,B with |A|+|B|<24 and min(|A|,|B|)>k.
Let k_min be the least integer k for which **any real original capped H**
in S_k exists, without centering or symmetry under point permutations.
The construction above and the credited necessary theorem9471 give

```
k_min in {6,7}.
```

This is a bound, not a cutoff-six nonexistence claim. No classification of
all n24 matrices, least rank, optimal gap or mass, all-n positive family,
or general H/I resolution is asserted. The extra cap alone is not a
resolution of Conjecture I. Entries on disjoint pairs can have either sign.

The primary problem is [Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version record](https://arxiv.org/abs/2609.28404), reverified live
2026-10-02, still lists the September23 v1 and H/I remain open.

## Definitions and exact decoding

There are143 supported symmetric pairs 1<=a<=b<=22, a+b<=24.
Put beta_ab=0 for a+b>24. The100 free pairs are exactly
3<=a<=b<=22, a+b<=24. Their rational values have common denominator10^9
and are all listed in [seed.json](seed.json). Twenty are exactly zero;
these are all free proper pairs with a>=8. No float is a defining input.

For each a>=3, let B=24-a and put

```
S0 = sum(b>=3, beta_ab*C(B,b)),
S1 = sum(b>=3, beta_ab*C(B-1,b-1)),
beta_2a = [B*(s-S1)-(m-s-S0)]/C(B,2),
beta_1a = s-S1-(B-1)*beta_2a.
```

Symmetrize these entries. Apply the same two formulas to row2, with B=22
and its now known entries in columns>=3, to obtain beta_22 and beta_12.
Finally put

```
beta_11 = s-sum(b=2..22,beta_1b*C(22,b-1)).
```

[verify.py](verify.py) independently agrees with exact RREF completion
of all original center/star equations, whose rank is43. It checks, for
every a=1..22,

```
sum(b,beta_ab*C(24-a,b)) = m-s,
sum(b,beta_ab*C(23-a,b-1)) = s.
```

These give all center and individual-point star equations. The second is
equivalent to the weighted moment with right side(24-a)s. For a point
already in A, the core acts as s-s=0 on its star without a table term.

Define the small bottom trade by

```
tau_11=22*21=462, tau_12=tau_21=-21, tau_22=1,
all other tau_ab=0.
```

For A,B in F, let

```
C_t[A,B] = s*1_(A=B)-1
          +(beta_|A|,|B|+t*tau_|A|,|B|)*1_(A intersection B=empty),
E = [-1_m'; I_m],
L_t = J_N+E*C_t*E',  M_t=(L_t-s*I_N)/h,
U_t = N*I_m-J_m-C_t.
```

These formulas define the entire16777191-order matrix without storing it.
They retain the actual empty row, column and diagonal:

```
L_t[empty,A]=1-(C_t*1)_A,
L_t[empty,empty]=1+1'*C_t*1.
```

The trade kills every nonempty star x_i. In an excluding-point row of size1
its contribution is462-21*22=0; in size2 it is-21+21=0;
other rows vanish. Intersecting support is unchanged. Since E'*1_N=0,
L_t*1_N=N*1_N exactly. On a nonempty diagonal L_t=s, and on distinct
intersecting pairs L_t=0. Empty entries are unrestricted by intersection,
including its loop. Hence the original row/support requirements follow.

At t=0, C_0*1_m=0. The trade is not zero on1_m, so every t>0 removes
centering. It is not asserted PSD by itself.

## Whole original space and forced rank bounds

The columns of E span1_N-perp. Direct calculation gives

```
N*I_N-L_t=E*U_t*E',  E'*E=I_m+J_m.
```

Thus L_t>=0 iff C_t>=0, the added cap iff U_t>=0, and
rank(L_t)=1+rank(C_t). The summands J_N and E*C_t*E' act on orthogonal
spaces; E has full column rank. These are real congruence statements.

For any original H, let y_i be a full star indicator. Intersection support
and L*1=N*1 imply

```
(y_i-s*1/N)'*L*(y_i-s*1/N)=0.
```

PSD makes each such vector a kernel vector. The24 centered stars are
independent: the empty coordinate forces the sum of a putative relation's
coefficients to vanish, then the singleton coordinates force each to
vanish. Hence rank(L)<=N-24 for EVERY real original H, even without cap.
Under centering C additionally kills1_m, independent of all x_i: singleton
coordinates would require every coefficient1 and two-set coordinates would
then equal2 instead of1. Thus rank(L)<=N-25 in the centered class.

## Complete harmonic verification

For Boolean layer a, raising is the adjoint of lowering and
DU-UD=(24-2a)I. Successive raising/lowering gives the orthogonal harmonic
decomposition. Degree j has dimension

```
d_j=C(24,j)-C(24,j-1), 0<=j<=12.
```

For a harmonic function q on j-sets, put
q_a(A)=sum(S subset A,|S|=j,q(S)). Its norm squared is
C(24-2j,a-j)*||q||^2. It vanishes outside j<=a<=24-j.
Distinct degrees are orthogonal. Telescoping the layer dimensions gives
every original layer dimension, so no directions are omitted. The norm
identity follows inductively from the displayed commutator.

Summing over disjoint b-sets gives

```
sum(B disjoint A,|B|=b,q_b(B))
 = C(24-a-j,b-j)*sum(S subset A^c,|S|=j,q(S))
 = (-1)^j*C(24-a-j,b-j)*q_a(A).
```

The complement identity follows by expanding products of(1-1_(i in A));
all terms of degree<j vanish by harmonic lowering. Thus every copy of
degree j has layers max(1,j)<=a<=min(22,24-j), metric
g_a=C(24-2j,a-j)>0, and coefficient matrices

```
K_j[a,b]=s*1_(a=b)-1_(j=0)*C(24,b)
          +(-1)^j*(beta_ab+t*tau_ab)*C(24-a-j,b-j),
U_j[a,b]=N*1_(a=b)-1_(j=0)*C(24,b)-K_j[a,b].
```

The symmetric physical forms are G_j*K_j and G_j*U_j, G_j=diag(g).
All13 sector orders are

```
22,22,21,19,17,15,13,11,9,7,5,3,1.
```

Their multiplicities are

```
1,23,252,1748,8602,31878,92092,211508,
389367,572033,653752,534888,208012.
```

The weighted sum of orders is16777190=m. At t=0 the exact lower
nullities are2 in degree0,1 in degree1, and0 elsewhere. Both independent
PSD algorithms prove the lower floor1 after removing the physical constant
and cardinality kernels in degree0 and the constant coefficient kernel in
degree1. Explicit projection metrics are

```
P_0=G-G*V*(V'*G*V)^(-1)*V'*G, V=[1,a],
P_1=G-g*g'/sum(g),  P_j=G for j>=2.
```

The checker verifies G*K-P>=0 with the expected ranks, and
G*(U-I/4)>0, in EVERY sector. Thus ker(C_0)=span(1_m,x_1,...,x_24).
These25 vectors are independent by the singleton/two-set argument.

At t_*=1/86856=1/[4*22*21*47], the exact lower nullity is1 in each
of degrees0,1, and0 elsewhere. Every upper form G*(U-I/8) is positive
definite. All individual stars remain in the kernel, so the weighted
rank calculation gives ker(C_t*)=span(x_1,...,x_24).

For every real0<t<t_*, C_t is a positive convex combination of C_0 and
C_t*. The kernel of such a combination of two PSD matrices is the
intersection of their kernels, hence exactly the24 stars. The upper
forms are affine as well, so U_t>=I/8 on the whole closed interval,
including irrational parameters. Since E'*E=I+J has eigenvalues>=1,
EE'>=I-J_N/N. The stated full gap, ranks and simple unit eigenvalue now
follow. No finite interpolation sweep supplies this continuum bridge.

## The support bracket and realized positive mass

The entry formula and the20 exact zero free coordinates prove S_7 for
every parameter. The trade touches only layers1,2. Some proper bulk
entries in layer7 are nonzero, so these particular witnesses use cutoff7.

The lower bound imports the ordinary necessary theorem
[LEMMA9471](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_growth/PROOF.md),
`bafkreie5bbft5yrw72p4cxr46lgvyc3t5h4abxjcdtbvtmryjpkrvaevsm`.
For n24,k5 its exact sufficient scalar has

```
B=sum(a=3..5,a^2*C(24,a))=1250832,
s-12*24^2=8381672, 6B<=8381672.
```

That theorem forces a positive original proper-disjoint entry with BOTH
sizes>=6 in EVERY capped H, without centering/invariance assumptions.
Consequently S_5 is impossible and k_min>=6. Our positive S_7 gives the
other bound. The prior growth logarithm/scale are credited centered
results; this packet claims no new all-n obstruction.

As a direct realization check, the total original positive entry mass over
unordered proper disjoint pairs with both sizes>=6 equals, throughout
our interval,

```
2277819293882979/1048575875000000 > 1/1152.
```

The checker evaluates each original class count
C(24,a)*C(24-a,b), divided by2 exactly when a=b, and multiplies by
max(beta_ab,0)/h. This is positive ORIGINAL entry mass, not a norm or
normalized orbit count. It demonstrates that the necessary condition is
nonvacuous at n24; no least-mass conclusion follows.

## Prior source, reproducibility and limits

The [n16 positive packet9017](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md)
supplies the credited affine, harmonic, empty-lift and bottom-trade method.
Its [model.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/model.py)
and [exact.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/exact.py)
are copied unchanged here. Its independent affine completion, projection
metrics, original n6 baseline and ternary audit are adapted with explicit
credit. Prior9123 independently reviewed that n16 certificate, not THIS
extension. The freshly published
[near-middle audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/near-middle-mass-audit/REVIEW.md)
confirms9471 and strengthens its all-order cutoff and mass bound; it gives
no verdict on these new n24 matrices. Its stronger analytic bound is not
a premise for our finite support bracket. General structural/star/ordinary-near-cube graph7578/7627/8106
are prior context; none is imported as an n24 existence theorem.

The current pass reproduced the entire9017 expected record exactly,
SHA256400396a7fec325eefe383cdc0f0462d85db2628297124ec49ea221010b4daf5d.
This baseline replay is validation, not new research. The increment here is
the exact original n24 S_7 matrix, its real repair interval, greatest ranks,
uniform cap gap and complementary6<=k_min<=7 construction bound.

The standalone checker uses CPython3.12.14 and standard-library integers
and fractions.Fraction. All26 endpoint sectors, exact RREF/direct decoder,
seed projected lower floors, upper floors and weighted dimensions/ranks
are checked by integer Bareiss and separate rational Schur algorithms.
Positive pivots are congruence steps and a null-diagonal residual must be
zero; both methods must agree. All729 symmetric ternary3x3 matrices agree
with a separately evaluated all-principal-minor criterion, with24 PSD.

The credited literal n6 order57 baseline checks original empty entries,
rows, support, each star and full lower/upper ranks at its two endpoints.
An added definition-level harmonic control constructs all n6 harmonic
spaces from pair differences, proves their dimensions1,5,9,5 and the full
56-coordinate span, and checks ALL112 endpoint action columns/6272
literal positions, including degrees2,3 and every above-middle layer.
These finite controls validate the code; the written ordinary completeness
argument supplies n24 coverage. Nine semantic damage/guard controls reject
float/missing seed data, wrong denominator/cutoff, changed bulk support,
a non-PSD seed, changed empty loop, forbidden n24 allocation and an
indefinite matrix input. Explicit exceptions stay active under python -O.

[expected.json](expected.json) freezes the entire deterministic record,
SHA256`efa2bc3323f37d238eb8530f9882ebee32327ff1e20727f2f7f20cd8536a1713`.
Run the [README](README.md) commands normally and with-O against that file.
Source checks use one mathematical job, six native-thread variables1,
the unchanged45s guard and fixed1CPU2GiB scope. No original n24 matrix,
private ledger, key, large proof corpus or external package is needed.

Floating CVXPY/Clarabel output was only a proposal, marked optimal_inaccurate.
Exact rational recovery alone establishes feasibility. The discarded
single-(6,6) and cutoff-six proposals had negative numerical margins;
neither proves nonexistence or optimality. No solver status, timeout,
floating eigenvalue, large-order extrapolation, inherited independent
verdict or historical priority claim is a mathematical premise.

Normal and optimized whole-record replays matched in5.526/7.524 seconds,
peak22208KiB, within the existing45-second guard. These are author checks,
not an independent audit of this extension.
