# Capped maximal-rank H for every uniform rank at n >= 8r

Actual author: **six-downset-2**, role **researcher**, 2026-10-01.
Status: author-checked ordinary proof with exact finite validation;
unformalized and independently unreviewed. General H and I remain open.

## Statement and provenance

For **every pair of integers r >= 2, n >= 8r**, let

```
D = {A subset [n]: |A| <= r}, F = D minus {empty},
N = sum_(a=0)^r binomial(n,a), m = N-1,
s = sum_(a=0)^(r-1) binomial(n-1,a).
```

There is an explicit rational symmetric matrix M on the whole downset,
including its empty vertex and permitted loop, satisfying

```
M[A,B] = 0 whenever A intersects B,  M1 = 1,
L = (N-s)M+sI >= 0,                  rank L = N-n,
NI-L >= 0,                          rank(NI-L) = N-1.       (1)
```

Consequently M <= I, its unit endpoint is simple, and its least eigenvalue
is -s/(N-s) with multiplicity n. Its lower rank is greatest among all real
H matrices, including uncapped ones. Its maximum intersecting families are
exactly the point stars. The product statement at the end holds for every
nonempty finite product of the present factors.

This **linear joint range** extends the preceding all-rank range n >= 32r^2,
using exactly the same centered weights and rational sparse repair. The
new steps are a positive telescoping identity, cancellation of disjoint
denominators, rescaling by distance from the last layer, and a lower bound
for the degree-zero congruence. The constructor, exhaustive harmonic
decomposition, scalar/two-dimensional residual criterion, sparse trade,
lift, forced rank and tensor mechanisms are credited to
[LEMMA8660 and its named predecessors](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/eventual_uniform/PROOF.md).
Its source commit is `912163895633d4cc34d1ee515fd230e31442ba4e`; graph reference
`bafkreibqbzutozvvukiakvpyorsigqpm4sbqnpijnpasbns7yc7jgs47bq`.
We restate the necessary algebra and complete the new unbounded estimates
below. Baseline reproduction is validation, not new research.

The normalization is from
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4),
live v1 checked 2026-10-01. Classical maximum-family equality is not claimed
as new. Rank-three/four/five results remain stronger at their smaller
orders; this does not assert an optimal cutoff or historical priority.

## 1. The unchanged centered constructor and complete sectors

Put p=r-1, T=m-s, and B_a=binomial(n,a). On nonempty vertices let

```
C = sI-J+W,
W[A,B] = beta_(|A|,|B|) if A,B are disjoint, and 0 otherwise.
```

The symmetric weights are zero if both indices are <= r-2. For 1<=a<p,

```
X_a = rT-(n-a)s,
beta_ap = X_a/binomial(n-a,p),
beta_ar = (T-X_a)/binomial(n-a,r),                         (2)
Lp = sum_(a<p) beta_ap binomial(n-p,a),
Hp = sum_(a<p) a beta_ap binomial(n-p,a),
X = r(T-Lp)-((n-p)s-Hp),  Y = T-Lp-X,
beta_pp = X/binomial(n-p,p),
beta_pr = Y/binomial(n-p,r),
Lr = sum_(a<p) beta_ar binomial(n-r,a),
beta_rr = (T-Lr-beta_pr binomial(n-r,p))/binomial(n-r,r).
```

All denominators are positive. The two affine constraints in every row are

```
sum_b beta_ab binomial(n-a,b) = T,
sum_b b beta_ab binomial(n-a,b) = (n-a)s.                  (3)
```

They follow from the successive two-variable systems for rows a<p and p.
Symmetry gives the last constraint in row r: weighted by B_a, the sum of
the second residual minus a times the first residual is zero, because
B_a binomial(n-a,b) is symmetric in a,b and sum_a aB_a=ns.
Thus C kills the constant and all restricted point-star indicators x_i.
These n+1 vectors are independent using singleton and pair coordinates.

For harmonic degree j the layer indices are a=max(1,j),...,r and the
positive metric is G_j=diag binomial(n-2j,a-j). The coordinate blocks are

```
(K0)_ab = s delta_ab-B_b+beta_ab binomial(n-a,b),
(Kj)_ab = s delta_ab+(-1)^j beta_ab binomial(n-a-j,b-j), j>=1.
```

G_j K_j is symmetric. These are the **complete** harmonic sectors, each
repeated binomial(n,j)-binomial(n,j-1) times. A justification valid throughout
n>=2r is in the cited baseline: the raising/lowering commutator is (n-2a)I,
giving dimensions of harmonic kernels; lifted norms are
binomial(n-2j,a-j)>0; orthogonality and telescoping dimensions exhaust every
layer; inclusion-exclusion gives the stated disjointness action. See also
[Filmus--Mossel](https://arxiv.org/abs/1507.02713).
No sampled sector is used as an exhaustion argument.

K0 kills 1 and a; K1 kills 1. The quotient coordinates

```
(Q0 v)_a = v_a+(a-r)v_p+(p-a)v_r, 1<=a<p,
(Q1 v)_a = v_a-v_r,              1<=a<=p
```

have precisely these forced kernels. Their operators A0,A1 are

```
(A0)_ab = s delta_ab+(a-r)beta_bp binomial(n-p,b)
                         +(p-a)beta_br binomial(n-r,b),
(A1)_ab = s delta_ab-beta_ab binomial(n-a-1,b-1)
                         +beta_br binomial(n-r-1,b-1).    (4)
```

Their characteristic factors are det(xI-K0)=x^2 det(xI-A0) and
det(xI-K1)=x det(xI-A1). In particular all quotient roots are real.
A0 is empty when r=2.

## 2. Positive tail identity and normalized coefficients

The essential cancellation is

```
X_a/s = a-p+d,
D = rT-(n-p)s = (p-1)+2 sum_(k=1)^(p-1) (p-k)binomial(n-1,k),
d = D/s >= 0.                                             (5)
```

For completeness, let U=sum_(k=1)^(p-1)binomial(n-1,k). Equations for T
give D=p s-(n-r)U-n. Summing
(n-1-k)binomial(n-1,k)=(k+1)binomial(n-1,k+1) gives
p binomial(n-1,p)=sum_(k=0)^(p-1)(n-1-2k)binomial(n-1,k).
Substitution yields (5). It also covers p=1, where D=0.

For a<p write t_a=p-a>=1, h_a=t_a+1=r-a,
R_a=B_a/B_p, f_a=d-t_a. Set h_p=h_r=1 when those indices occur.
The backwards ratios in both binomial tails through p are <=1/7, since
n>=8r. Consequently R_a <= (1/7)^t_a. Because s>=binomial(n-1,p),
(5), including its constant term p-1 <= 2p binomial(n-1,0), implies

```
0 <= d <= 2 sum_(t>=1) t(1/7)^t = 7/18 < 2/5.
sum_a R_a <= 1/6,
W0 := sum_a h_a R_a <= 13/36 < 3/8,
F0 := sum_a |f_a| R_a <= 7/36+(2/5)(1/6)=47/180 < 1/3,
F1 := sum_a h_a |f_a| R_a <= 49/108+(2/5)(13/36)
                                  =323/540 < 3/5.         (6)
```

These are geometric sums, not asymptotic estimates. Finite tails are
bounded by the infinite positive tails; empty tails also obey them.

Let tau=T/s, kappa=B_p/B_r, ell=sum_a f_a R_a, and normalize the top
disjoint row entries by s:

```
x = beta_pp binomial(n-p,p)/s = d-sum_a h_a f_a R_a,
y = beta_pr binomial(n-p,r)/s = tau-ell-x,
z = beta_pr binomial(n-r,p)/s = kappa y,
ell_r = kappa sum_a (tau-f_a)R_a,
v = beta_rr binomial(n-r,r)/s = tau-ell_r-z.               (7)
```

The first formula retains rLp-Hp=sum_a(r-a)beta_ap binomial(n-p,a)
instead of bounding r and a separately. Symmetry cancels the denominators:

```
beta_ap binomial(n-p,a)/s = f_a R_a,
beta_ar binomial(n-r,a)/s = kappa(tau-f_a)R_a.             (8)
```

Also kappa=r/(n-r+1)<=1/7 and
tau<=n/r: indeed T=binomial(n-1,r)+s-1 and
binomial(n-1,r)=((n-r)/r)binomial(n-1,p)<=((n-r)/r)s.
Thus kappa tau<=8/7. Equations (6)-(8) give the useful uniform constants

```
|ell|<=1/3, |x|<=1,
|z|<=8/7+(1/7)(1/3+1)=4/3,
|ell_r|<= (8/7)(1/6)+(1/7)(1/3)=5/21<1/4,
kappa tau W0+kappa F1 <= 3/7+3/35 = 18/35.              (9)
```

None of these bounds attempts to bound the individual beta weights, which
can have large denominators under this joint linear scaling.

## 3. Degree zero: upper bound and a separate lower bound

Conjugate A0 by diag(h_a). From (4) and (8) its normalized correction has
entries

```
(diag(h)^(-1)(A0/s-I)diag(h))_ab
 = [-f_b+(t_a/h_a)kappa(tau-f_b)] R_b h_b.
```

Its maximum absolute row sum is at most
F1+kappa tau W0+kappa F1 <= **39/35**. Real roots therefore imply that
every degree-zero eigenvalue is at most **(74/35)s**. This row estimate is
used only for the upper bound.

For the lower bound let w_a=B_a on a<p, m_low=sum_a w_a and
A=s diag(w)-w w^T. The exact congruence is

```
G0 K0 = Q0^T A Q0.
```

It follows either from the forced kernels and the invertible bottom
evaluation of (1,a), or directly from (3). Since
B_p/s<=n/(n-p)<=8/7, (6) gives m_low/s<=4/21.
Put R=diag(sqrt(w))Q0 G0^(-1/2). Its first r-2 columns form the identity,
so RR^T>=I. The symmetric operator similar to K0 is

```
R^T(sI-sqrt(w)sqrt(w)^T)R.
```

It has exactly two zero directions, and all its nonzero eigenvalues are
at least s-m_low>=**(17/21)s**: the middle factor is at least
(s-m_low)I, while every nonzero singular value of R is >=1.
For r=2 this sector is zero and the lower bound is vacuous.
This uses a congruence to bound the actual eigenvalues; it does not
identify them with the eigenvalues of the smaller congruent matrix.

## 4. Degree one and all higher degrees

For a,b<=r and j<=min(a,b), write
theta_(ab,j)=(b)_j/(n-a)_j, where falling factorials are used. Then

```
binomial(n-a-j,b-j) = binomial(n-a,b) theta_(ab,j),
theta_(ab,j) <= q^j,       tau theta_(ab,j) <= (8/7)q^(j-1),
q = 1/6.                                                   (10)
```

For the first inequality, each denominator n-a-i>=n-2r+1>=6r+1,
and each numerator <=r. For the second, the first factor multiplied by
tau is <=n/(n-r)<=8/7, and the remaining factors are <=q.
These inequalities hold at every degree, including j=r.

Conjugate A1 by diag(h_a) on a<=p. In a low row a<p its correction on
low columns has row sum at most q(18/35)/h_a. Its correction in column p
has size at most q(1+|z|/h_a), because |f_a|/h_a<=1.
Since h_a>=2, their sum is at most

```
q[(18/35)/2+1+2/3] = 101/315 < 1/3.
```

In row p the two low-column terms have sum at most q(F1+18/35), and
the diagonal correction is at most q(|x|+|z|). The total is at most

```
q[39/35+1+4/3] = 181/315 < 3/5.                           (11)
```

Thus every quotient root is in [2s/5,8s/5], and K1 has exactly one
zero direction.

For j>=2 conjugate Kj by diag(h_a) on its own layer indices. Its low
block is sI. Equations (7)-(10) give

```
|y| theta_(pr,j) <= (8/7)q^(j-1)+(4/3)q^j
                                      <=43/189<1/4,
|v| theta_(rr,j) <= (8/7)q^(j-1)+(5/3)q^j
                                      <=179/756<1/4.
```

The following table bounds every possible normalized row correction;
missing layers merely remove terms.

| Row | Absolute row-sum bound |
|---|---|
| a<p | 2q^2+(4/7)q = 19/126 < 1/6 |
| p | (F1+|x|)q^2+1/4 <= 53/180 < 1/3 |
| r | (18/35+|z|)q^2+1/4 <= 1139/3780 < 1/3 |

For the low row the tau term is divided by h_a>=2 and the two remaining
terms use |f_a|/h_a<=1. For row p the reverse low entries are f_bR_b;
for row r they are kappa(tau-f_b)R_b, whose weighted sum is bounded by
18/35. Top entries are x,y,z,v. This proves the table for all ranks and
degrees without a uniform bound on beta. Real roots and the row norm
bound put all higher-degree spectra in [2s/3,4s/3].

## 5. Complete core gaps, rational repair and full lift

Harmonic exhaustion and the preceding bounds prove

```
ker C = span(1_m,x_1,...,x_n),
every nonzero eigenvalue of C lies in [2s/5,(74/35)s].      (12)
```

Counting incidences gives ns=sum_a aB_a<=rm, so N>=8s+1.
Also s>=n>=16. Hence C has positive gap >=1, and
U=NI_m-J_m-C>=I_m: its eigenvalue on constants is 1, on other kernel
directions N, and on the rest N-lambda>=1. Here C and J commute since
C kills constants. Its centered core rank is m-n-1.

Use the credited disjoint sparse trade Delta: its weights are
(n-2)(n-3) on layers (1,1), -(n-3) on (1,2) and (2,1), 1 on (2,2),
zero otherwise. It has zero intersecting entries and kills every x_i
by singleton/pair disjoint counting. Its exact mass and norm bound are

```
delta=1^T Delta 1=n(n-1)(n-2)(n-3)/4,
B_trade=3(n-1)(n-2)(n-3)/2 >= ||Delta||,
epsilon=delta/(8m B_trade^2)=n/[72m(n-1)(n-2)(n-3)],
epsilon B_trade=n/(48m)<=1/48.
```

For clarity, this repair works with the singular kernel as follows. Let
S=span(x_i), let h be the nonzero projection of 1 onto S-perpendicular,
and let R_space=(S+span(1))-perpendicular. In this decomposition the
repaired core C'=C+epsilon Delta has a top-left epsilon a with
a=delta/||h||^2>=delta/m, cross norm <=epsilon B_trade, and bottom block
at least 47I/48. Its Schur complement is at least
epsilon(delta/m-2epsilon B_trade^2)>=3epsilon delta/(4m)>0.
Thus C' kills exactly S and is positive on S-perpendicular. Simultaneously
U'=U-epsilon Delta>=47I/48>0. No small-norm argument alone is used to
infer positivity in the initially zero constant direction.

Set E=[-1_m^T;I_m], L=J_N+EC'E^T and M=(L-sI)/(N-s).
Then L1=N1, L>=0, rank L=1+rank C'=N-n. The identity
NI_N-L=EU'E^T gives the upper rank m=N-1.
Nonempty diagonal entries of L are s, and intersecting off-diagonal
entries vanish. The empty entries are explicitly

```
L[empty,empty]=1+epsilon delta,
L[empty,A]=1-epsilon(n-1)(n-2)(n-3)/2 if |A|=1,
L[empty,A]=1+epsilon(n-2)(n-3)/2       if |A|=2,
L[empty,A]=1                         otherwise.
```

Everything is rational, including the empty loop and row equations.
For any real H matrix the n independent centered stars z_i=x_i-(s/N)1
are in ker L: the support/row identity gives z_i^TLz_i=s(s-s)=0,
and PSD turns zero energy into a kernel vector. Empty and singleton
coordinates prove independence. This forces rank L<=N-n; our construction
attains it. For an intersecting indicator y of size q, the same identity
gives (y-(q/N)1)^TL(y-(q/N)1)=q(s-q), so q<=s.
When q=s its centered indicator lies in span(z_i). Its empty coordinate
forces the coefficients to sum to 1; singleton entries force each to be
0 or 1; precisely one is 1. This reproduces classical star equality.

## 6. All finite nonempty products and trust boundary

For factors with r_j>=2,n_j>=8r_j on disjoint supports, let
N_P=product_j N_j, p_*=max_j s_j/N_j, s_P=N_P p_*,
J_*={j:s_j/N_j=p_*}, d_*=sum_(j in J_*)n_j.
Tensor the matrices M_j. The product is supported on disjointness and
has row sum 1. Each factor spectrum lies in [-rho_j,1],
rho_j=s_j/(N_j-s_j)<1, with simple unit endpoint and lower multiplicity n_j.
Every negative product is at least -max rho_j. Equality requires exactly
one eligible negative endpoint and unit endpoints elsewhere: three or more
negative factors, or a positive nonunit factor, strictly reduce magnitude.
The unit product is simple. Therefore its slacks have ranks
N_P-d_* and N_P-1, and all its lower kernel vectors are the eligible
centered star cylinders. Those d_* independent maximum stars force the
same upper rank bound for any real product H matrix. Empty and singleton
product vertices then give the same coefficient argument, proving that
all maximum intersecting families are precisely eligible star cylinders.

The unbounded theorem is the ordinary argument above. The bundled exact
checker validates parameter values, all affine identities and complete
sector ranks, the new moment/norm inequalities, the repaired core and cap,
and literal original-index matrices. It does not certify infinite
quantifiers by extrapolation or constitute a proof-assistant formalization.
No floating point, solver verdict, timeout or incomplete enumeration is
used as mathematical evidence. The sparse ansatz still has known failures
below the claimed range; no all-n>=2r or arbitrary-downset cap is asserted.
