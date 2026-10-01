# Capped maximal-rank H at every uniform rank when n>=32r^2

Actual author: **six-downset-2**, role **researcher**, 2026-10-01.
Status: complete author-checked ordinary proof; exact finite validation;
unformalized and not independently reviewed. General H and I remain open.

## 1. Quantified result and credited inputs

For every pair of integers **r>=2, n>=32r^2**, let

```
D(n,r)={A subset[n]: |A|<=r}, F=D minus {empty},
N=sum_(a=0)^r binomial(n,a), m=N-1,
s=sum_(k=0)^(r-1) binomial(n-1,k).
```

There is an explicit rational symmetric matrix M on the **whole** downset,
including the empty vertex and its permitted loop, such that

```
M[A,B]=0 if A intersects B, M1=1,
L=(N-s)M+sI >=0, rank L=N-n,
NI-L >=0, rank(NI-L)=N-1.                         (1)
```

Thus M<=I, its unit endpoint is simple, and its least eigenvalue is
`-s/(N-s)` with multiplicity n. The lower rank is greatest among **all
real H matrices**, including uncapped matrices. Every finite nonempty
product of these factors on disjoint supports has the capped maximal-rank
and eligible-star consequences specified in Section 8.

There is a second exact structural result: at **every n>=2r**, the symmetric
centered core whose disjoint weights vanish whenever both layer sizes are
at most r-2 is unique, with the formulas below. Its full core/cap PSD tests
reduce to one degree-zero scalar and rational Schur residuals of size at
most two. This is a criterion for this ansatz, not an assertion that it
succeeds at every stable order. For example, it fails at (n,r)=(20,10).

The problem normalization and distinction from the inertia conjecture I
are from [Ellis--Filmus--Friedgut Section 4](https://arxiv.org/html/2609.28404v1#S4).
The [live version record](https://arxiv.org/abs/2609.28404), checked October 1,
2026, still lists v1 and leaves H/I open. The cap is an extra condition.

Credited campaign ingredients are the
[core lift and conditional capped tensor theorem, lemma7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
[sparse trade, lemma7745](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
and [forced rank/equality mechanism, lemma7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
The finite-rank centered examples are
[rank three, lemma7930](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three/PROOF.md),
[rank four, lemma7980](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md),
and [rank five, lemma8583](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/uniform_rank_five/PROOF.md).
The last source is by this author. Its exact verifier and three generic
tables are reproduced before this extension; reproduction is validation.
At the final refresh, [independent review8648](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/rank-five-audit/REVIEW.md)
confirmed8583 and proved a larger closed repair interval. That review was
inspected and credited; its verdict applies to rank five, and its larger
interval is not used in the conservative repair below.

[Lemma8064](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling/PROOF.md)
already gives ordinary maximal-rank H for **all r>=2,n>=2r**, while proving
cap failure for its own proposed coupling. It does not establish a cap.
The [independent audit8104](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling_review3/REVIEW.md)
confirms that result, enlarges its coupling interval and retains its cap
obstruction. That verdict concerns8064, not the present construction.
The new increment here is an explicit all-rank **capped** construction in
a quantified quadratic range, the uniform estimates proving it, and the
general residual criterion. No claim is made for all n>=2r, a best cutoff,
or historical priority. The classical uniform intersecting-family maximum
and its star equality are prior results; their spectral deduction below
is a consequence of the new sharp-kernel matrices.

## 2. Closed affine formulas at every stable order

In this section only r>=2,n>=2r are needed. Set p=r-1 and T=m-s. Let D_ab
denote literal disjointness between nonempty layers a,b. Put

```
C=sI_m-J_m+(beta_ab D_ab).                       (2)
```

Choose symmetric weights with beta_ab=0 for a,b<=r-2. For each a<p define

```
X_a=rT-(n-a)s,
beta_(a,p)=X_a/binomial(n-a,p),
beta_(a,r)=(T-X_a)/binomial(n-a,r).               (3)
```

Reflect these entries. The last three weights are

```
Lp=sum_(a=1)^(p-1) beta_(a,p) binomial(n-p,a),
Hp=sum_(a=1)^(p-1) a beta_(a,p) binomial(n-p,a),
X=r(T-Lp)-[(n-p)s-Hp], Y=T-Lp-X,
beta_pp=X/binomial(n-p,p),
beta_pr=Y/binomial(n-p,r),
Lr=sum_(a=1)^(p-1) beta_(a,r) binomial(n-r,a),
beta_rr=[T-Lr-beta_pr binomial(n-r,p)]/binomial(n-r,r). (4)
```

All denominators are positive at n>=2r. Empty sums are zero, so r=2 is
included with no special constructor division. The exact implementation
is [matrices.py](matrices.py).

The equations required for stars and centering are

```
sum_b beta_ab binomial(n-a,b)=T,
sum_b b beta_ab binomial(n-a,b)=(n-a)s.           (5)
```

The second is equivalent to
`sum_b beta_ab binomial(n-a-1,b-1)=s`. For a<p, the two unknown weighted
entries have sum T and p/r-weighted sum (n-a)s; solving that two-variable
system gives (3). The same operation in row p gives (4), then row r's
first equation determines beta_rr. Its remaining equation is automatic:
if R_a and E_a are respectively the residuals in the second and first
equations of (5), symmetry of

```
binomial(n,a)binomial(n-a,b)=n!/[a!b!(n-a-b)!]
```

gives `sum_a binomial(n,a)(R_a-aE_a)=0`. The target terms cancel because
`sum_a a binomial(n,a)=ns` and `sum_a (n-a)binomial(n,a)=nT`.
All residuals but R_r have already vanished, and binomial(n,r)>0, so R_r=0.
This also proves uniqueness: every successive two-variable system has
determinant r-p=1, with positive binomial factors.

For the restricted star indicators x_i, counting the disjoint b-sets
containing i in a row outside that star proves Cx_i=0. Rows inside it
vanish directly from support. The first equation of (5) gives C1_m=0.
The n stars and constant vector are independent: singleton and pair rows
of any relation first determine all coefficients and then force them zero.

## 3. Complete harmonic sectors and the kernel quotients

For each a let V_a be real functions on a-subsets with the counting inner
product. Raising U_a and lowering T_(a+1)=U_a^T obey

```
T_(a+1)U_a-U_(a-1)T_a=(n-2a)I.
```

This follows by counting a one-point exchange, including diagonal terms.
It makes U_a injective for a<n/2. Consequently H_j=ker T_j has dimension
`binomial(n,j)-binomial(n,j-1)` for j<=r<=n/2, including j=r at n=2r;
take H_0=V_0. If

```
W_(a,j)h(A)=sum_(J subset A, |J|=j) h(J),
```

repeated adjointness gives
`<W_(a,j)h,W_(a,j)k>=binomial(n-2j,a-j)<h,k>`. Distinct degrees are
orthogonal by moving raising maps until lowering kills the higher degree.
The dimensions telescope to binomial(n,a) on every layer, so the lifts
exhaust it. All their norm factors are positive in j<=a<=r<=n/2.
This is the classical harmonic decomposition, e.g.
[Filmus--Mossel](https://arxiv.org/abs/1507.02713), with completeness justified
here rather than inferred from finite blocks.

Repeated lowering and inclusion-exclusion show that
`sum_(J subset A^c,|J|=j) h(J)=(-1)^j W_(a,j)h(A)`. Counting disjoint
B containing J gives `D_ab W_(b,j)=(-1)^j binomial(n-a-j,b-j)W_(a,j)`.
Thus, on A_j={max(1,j),...,r}, the core block and positive metric are

```
K0_ab=s delta_ab-binomial(n,b)+beta_ab binomial(n-a,b),
Kj_ab=s delta_ab+(-1)^j beta_ab binomial(n-a-j,b-j), j>=1,
Gj=diag binomial(n-2j,a-j).                       (6)
```

Gj Kj is symmetric, so every eigenvalue is real. K0 kills 1 and the layer
cardinality vector a, while K1 kills 1. These forced directions should be
removed before estimating a spectral error. Define quotient coordinates

```
(Q0 v)_a=v_a+(a-r)v_p+(p-a)v_r, a=1,...,r-2,
(Q1 v)_a=v_a-v_r, a=1,...,r-1.
```

Their kernels are exactly span(1,a) and span(1). Choose the first r-2 or
r-1 standard vectors as the respective sections W, so QW=I. The quotient
operators A0=Q0 K0 W and A1=Q1 K1 W satisfy

```
(A0)_ab=s delta_ab+(a-r)beta_(b,p)binomial(n-p,b)
                          +(p-a)beta_(b,r)binomial(n-r,b),
(A1)_ab=s delta_ab-beta_ab binomial(n-a-1,b-1)
                          +beta_(b,r)binomial(n-r-1,b-1). (7)
```

The full characteristic polynomials are respectively x^2 det(xI-A0) and
x det(xI-A1). Hence their quotient roots are real too. When r=2, A0 is
empty and contributes no positive eigenvalue. No singular-kernel
perturbation is estimated as though it were a positive definite matrix.

## 4. Exact criterion with residuals of size at most two

Still assume only n>=2r. In H0=G0 K0, the leading r-2 block is
`A=s diag(w)-w w^T`, w_a=binomial(n,a), a<=r-2. The forced kernels and
the invertible bottom 2-by-2 evaluation of (1,a) give the identity
`H0=Q0^T A Q0`. Thus its inertia is that of
`sI-sqrt(w)sqrt(w)^T`, plus two zero directions. In particular, for r>=3,

```
K0 PSD iff s>=m_low, m_low=sum_(a=1)^(r-2)binomial(n,a).
```

If the inequality is strict, the positive rank is r-2; at equality it is
r-3. For r=2, K0=0 identically. This is an inertia statement; the nonzero
eigenvalues of K0 are not asserted to equal those of the congruent block.

For j>=1, the leading layers a<=r-2 in H_j=G_j K_j form the diagonal
block sG_low. There are at most two remaining layers. Its PSD and rank
are therefore equivalent to those of the exact rational residual

```
S_j=H_top,top-H_low,top^T(sG_low)^(-1)H_low,top.  (8)
```

For the upper core U=NI_m-J_m-C, its degree-zero coordinates are
`(N-s)delta_ab-beta_ab binomial(n-a,b)`; other degrees are `NI-Kj`.
In every degree its leading block is (N-s)G_low, so the identical Schur
test gives a residual of size at most two. Positive leading diagonals
make the equivalence exact, with ranks adding. This proves the stated
criterion for both **centered, unrepaired** slacks. The later sparse trade
changes the low block and is not passed through (8).

At (n,r)=(20,10), s=262144 and m_low=263949. The vector equal to one on
the first eight layers and zero elsewhere has full-core quadratic form
`m_low(s-m_low)=-476427945`. Since s-m_low=-1805, it is negative.
This rules out this unique centered sparse ansatz at that pair, and says
nothing about other H or capped matrices.

## 5. Uniform estimates in the stated quadratic range

From now on assume n>=32r^2. Write B_k=binomial(n,k), and retain p=r-1.
Every backwards ratio in a binomial tail through degree r is at most
1/16. Consequently, with B=B_(r-2),

```
Z=sum_(k=0)^(r-2)B_k <=(9/8)B,
sum_(a=1)^(p-1)(p-a+1)B_a <=(9/4)B.             (9)
```

Indeed the two bounding geometric sums at q=1/16 are 16/15<=9/8 and
`sum_(k>=0)(k+2)q^k=496/225<=9/4`. This also covers the empty sum r=2.
The elementary ratio comparisons needed below are

```
B_(r-2)/s <=4r/n, s/B_r <=4r/n, B_p<=2s,
s<= (8/7)B_p, T<=2B_r,
binomial(n-a,k)>=(6/7)B_k, 1<=a<=r, k=p or r,
s/binomial(n-a,p) <=4/3.                        (10)
```

Here s>=binomial(n-1,p) and
`B_(r-2)/binomial(n-1,p)=n(r-1)/[(n-r+2)(n-r+1)]<=4r/n`.
Also `B_r/B_p=(n-r+1)/r`, and the upper tail bound for s gives the
stated s/B_r inequality. For displacement of a binomial coefficient,

```
binomial(n-a,k)/B_k=product_(i=0)^(k-1)(1-a/(n-i))
 >=1-ak/(n-k+1) >=6/7.
```

The last bound already holds at n>=8r^2, since n-r+1>=7r^2.
The s-tail ratio is at most1/8 there, so s<=(8/7)B_p; division gives
the last inequality of (10). T=sum_(k=1)^r binomial(n-1,k), so its
ordinary geometric tail gives T<=2B_r. All denominators are positive.

The leading cancellation in (3)-(4) must be retained. Set

```
U=sum_(k=1)^(r-2)binomial(n-1,k),
D=p s-(n-r)U-n,
X_a=(a-p)s+D.                                   (11)
```

The identity follows from `T=B_r+U` and
`r B_r=n binomial(n-1,p)`. For r=2, D=0. For r>=3, with
V=sum_(k=1)^(r-3)binomial(n-1,k), Pascal ratios give

```
D=r binomial(n-1,r-2)-(n-2r+1)V+p-n.
```

The ratios to s are bounded by
`binomial(n-1,r-2)/s<=2r/n`, `V/s<=8r^2/n^2`, and `n/s<=4/n`
(the last uses s>=binomial(n-1,2), n>=6). Therefore

```
|D|/s <=(2r^2+8r^2+4)/n <=12r^2/n <=3/8.       (12)
```

In particular |X_a|<=(p-a+1)s for a<p. Equations (3),(10) imply

```
|beta_(a,p)|<=(4/3)(p-a+1), |beta_(a,r)|<=3.     (13)
```

For the second bound, |T-X_a|<=2B_r+rs<=(5/2)B_r, while its denominator
is at least(6/7)B_r. The resulting bound35/12 is smaller than3.

Now (9),(13) imply

```
|Lp| <=3B <=(12r/n)s, |Hp|<=r sum_a |beta_(a,p)|binomial(n-p,a),
|X|=|D-rLp+Hp| <=(36r^2/n)s,
|beta_pp| <=48r^2/n <=3/2.                      (14)
```

For |X|, the absolute weighted sum controlling Lp and Hp is at most3B,
so |rLp-Hp|<=2r*3B<=24r^2 s/n; add (12).
Next |Y|<=T+|Lp|+|X|<=2B_r+2s, as
`(12r+36r^2)/n<=3/(8r)+9/8<=21/16<2`.
Thus |beta_pr|<=119/48<3 using (10). Similarly
`|Lr|<=3Z<=(27r/(2n))s<=s`, and
`|beta_pr|binomial(n-r,p)<=3B_p<=6s`.
The numerator of beta_rr has absolute value at most2B_r+7s, hence
`|beta_rr|<=91/32<3`. We have proved the uniform bound

```
|beta_ab|<=2r for every a,b.                     (15)
```

The zero entries and (13)-(14) are stronger than this bound; they matter
in the quotient estimates. For every row of A0 in (7), summing over b
and using (9),(13) gives

```
sum_b |(A0)_ab-s delta_ab|/s
 <=r(3B+3Z)/s <=(51/2)r^2/n <=51/64.            (16)
```

For A1, both binomial sums have degrees at most r-2. The first weight
has absolute value at most2r, and beta_(b,r) at most3. Hence

```
sum_b |(A1)_ab-s delta_ab|/s
 <=(2r+3)Z/s <=(63/4)r^2/n <=63/128.            (17)
```

For every j>=2, sum the binomials with index b-j<=r-2 and apply (15):

```
sum_b |(Kj)_ab-s delta_ab|/s <=2r Z/s <=9r^2/n <=9/32. (18)
```

These are bounds on the actual quotient or sector operators, not on an
unweighted block alleged to be symmetric. Their eigenvalues are real
by Section 3. The row norm bounds give |lambda/s-1|<=51/64: pick a
largest coordinate of an eigenvector, or use Gershgorin's theorem.
In particular all the quotient and higher-sector eigenvalues are in
**[s/8,15s/8]**, a deliberately weaker common window.

Thus the exact sector positive ranks are r-2 in degree zero, r-1 in
degree one, and r-j+1 in every degree j>=2. Harmonic exhaustion proves

```
ker C=span(1_m,x_1,...,x_n),
C >= the projector onto that kernel's perpendicular,
U=NI_m-J_m-C >= I_m.                            (19)
```

For the upper inequality, C kills1 and hence commutes with J. U has
eigenvalue1 on constants, N on the other core-kernel directions, and
N-lambda>=s/8+1 on the rest, since
`N-2s=binomial(n-1,r)>=1`. The lower positive gap s/8 is at least1
because s>=n>=32r^2. This proves an unbounded joint r,n claim by explicit
estimates, not by extrapolation from finite calculations.

## 6. Removing the one excess kernel direction

Use the credited sparse trade Delta on disjoint nonempty pairs: its layer
weights are (n-2)(n-3) on singleton/singleton, -(n-3) on singleton/pair,
1 on pair/pair, and zero otherwise. These weights have zero diagonal and
intersecting entries. A singleton row outside a point has one singleton
term cancelling n-2 pair terms; a pair row outside it has one singleton
term cancelling n-3 pair terms. Thus Delta x_i=0 at every r>=2.
Literal row counting gives

```
delta=1_m^T Delta 1_m=n(n-1)(n-2)(n-3)/4>0,
||Delta||_2<=B_trade=3(n-1)(n-2)(n-3)/2,
epsilon=delta/(8m B_trade^2)=n/[72m(n-1)(n-2)(n-3)],
epsilon B_trade=n/(48m)<=1/48.                  (20)
```

The bound is the maximum absolute row sum, and symmetry bounds the norm.
Let S=span(x_i) and h be the nonzero projection of1_m onto S-perpendicular.
On S-perpendicular=span(h) direct_sum R, where R=(S+span(1_m))-perpendicular,
the repaired core C'=C+epsilon Delta has blocks

```
[epsilon a       epsilon b^T;
 epsilon b       C_R+epsilon D_R],
a=delta/||h||^2>=delta/m, ||b||,||D_R||<=B_trade.
```

By (19)-(20), the bottom block is at least47I/48, with inverse norm less
than2. Its Schur complement is at least
`epsilon(delta/m-2 epsilon B_trade^2)>=3 epsilon delta/(4m)>0`.
Therefore C' is positive definite on S-perpendicular and kills exactly S.
Also U'=U-epsilon Delta>=47I/48>0. This proof controls the singular
constant direction explicitly; a small-norm assertion alone would not.

## 7. Full lift, maximal rank and classical equality

Set E=[-1_m^T;I_m], L=J_N+E C' E^T, M=(L-sI)/(N-s). Full column rank
of E and E^T1=0 give L1=N1 and

```
L>=0, rank L=1+rank C'=N-n,
NI-L=E U' E^T>=0, rank(NI-L)=m=N-1.
```

The identity uses `E(NI_m-J_m)E^T=NI_N-J_N`. Nonempty diagonal entries
of L are s, and its off-diagonal intersecting entries are zero. The empty
entries, implemented directly in matrices.py, are

```
L[empty,empty]=1+epsilon delta,
L[empty,A]=1-epsilon(n-1)(n-2)(n-3)/2 if |A|=1,
L[empty,A]=1+epsilon(n-2)(n-3)/2       if |A|=2,
L[empty,A]=1                         otherwise.
```

No vertex, loop or row equation is omitted. All these quantities are rational.

For any real H matrix, if y is an intersecting indicator of size q, support
and row sums imply
`(y-(q/N)1)^T L (y-(q/N)1)=q(s-q)`. PSD gives q<=s and puts the n
independent centered stars z_i in ker L. Independence follows from empty
and singleton coordinates, forcing rank L<=N-n even without a cap.
Our lift attains that bound. If q=s for its matrix, the kernel expression
for y has empty coordinate zero, so its star coefficients sum to1; singleton
coordinates make each coefficient0 or1. Exactly one is1, so y is its star.
This is the credited rank-to-equality argument reproducing classical equality.

## 8. Finite products

Let each factor have r_j>=2,n_j>=32r_j^2, with data N_j,s_j. Put

```
N_P=product_j N_j, p_*=max_j s_j/N_j, s_P=N_P p_*,
J_*={j:s_j/N_j=p_*}, d=sum_(j in J_*) n_j.
```

Tensoring the explicit matrices gives capped rational H on the product,
with lower rank N_P-d and upper rank N_P-1. Indeed each spectrum is in
[-rho_j,1], rho_j=s_j/(N_j-s_j)<1, with a simple unit endpoint and lower
multiplicity n_j. A negative product reaches -max rho_j only with exactly
one eligible negative endpoint and every other factor at1; three or more
negative factors give strictly smaller magnitude. Positive nonunit factors
also make the magnitude smaller. The unit endpoint is simple as well.
Thus the lower kernel consists exactly of the d eligible centered point-star
cylinders. These independent largest stars force the same rank upper bound
for every real H matrix on the product. Empty and singleton evaluations
again classify the maximum intersecting indicators as exactly those d stars.
This applies the credited capped tensor mechanism to the new factors.

## 9. Evidence, scope and trust boundary

The standalone checker uses only integers and fractions. It validates22
quantitative pairs r=2,...,12 at n=32r^2 and n=32r^2+1; every counting
identity, all complete harmonic-sector ranks, all stated numerical
inequalities, both kernel quotient intertwinings, the degree-zero
congruence, every size-at-most-two residual and the full repaired-sector
PSD/rank accounting. It separately validates six smaller generic examples
and full original-index matrices of orders11,42,163. All13 damaged/domain/
PSD controls reject under normal Python and Python -O. The (20,10)
negative witness is an exact ansatz obstruction, not a general cap verdict.
All expected values and exact finite radii are in [RESULTS.json](RESULTS.json).

The published rank-five verifier was reproduced; three generic tables at
n12,13,20 in [BASELINE.json](BASELINE.json) match the new formulas exactly.
These are credited input validation, not mathematical novelty or external
review. The constructor's affine domain n>=2r is larger than its default
certified domain n>=32r^2; smaller orders require their own exact checking.

The unbounded theorem rests on Sections 2-8: the weighted redundancy,
harmonic completeness, quotient spectrum, explicit uniform tail estimates,
Schur repair and lift/tensor/rank arguments. These ordinary bridges are
unformalized. Finite checks alone do not establish their quantifiers.
There is no solver, CAS, numerical eigenvalue, interpolation, search timeout,
private fixture or omitted enumeration in the proof. Published source is
compact; no large matrix corpus or credential is included. This does not
settle general H/I, every n>=2r, arbitrary bounded-rank downsets, or an
optimal threshold.
