# Paired cubature with error proportional to contraction loss

Complete author proof, 27 September 2026; independent review pending.
The full dimension-three Gaussian-majorisation problem remains open.

The accepted [paired cubature](CUBATURE_FRONTIER.md) already preserves the
mean squared-distance loss when its coordinate degree is at least two.
The new result concerns its **error**: a fixed beta row is approximated
with error proportional to that same loss, uniformly as the loss tends
to zero. Together with R8's accepted loss-dependent modulus, this gives
a corresponding finite-atom approximation of the whole hinge curve in
the small-radius regime. No new beta sign or positive map class is asserted.

## 1. Statement at arbitrary bounded radius

Let `mu` be a probability law supported in `B(a,R)` in `R^3`, let `T` be
1-Lipschitz, and let `s>0`. If T is initially defined only on the support,
use its usual Euclidean Lipschitz extension. Put

```
C=(2pi s)^(-3/2),  f_mu=mu*gamma_s,  g_mu=(T#mu)*gamma_s,
H_mu(u)=integral(g_mu-Cu)_+-integral(f_mu-Cu)_+,
epsilon=R^2/s,
d_mu=E[|X-X'|^2-|TX-TX'|^2]/s >= 0.
```

The sign here is favorable to majorisation: the desired inequality is
`H_mu>=0`. For `m>=2`, `j>=0`, and `0<=k<=N`, use the existing definitions

```
d_m(mu)=C^(1-m) integral(g_mu^m-f_mu^m),
a_j(mu)=d_(j+2)(mu)/[(j+1)(j+2)]=integral_0^1 u^j H_mu(u)du,
b_(N,k)(mu)=(N+1) binom(N,k)
              sum_(j=0)^(N-k) (-1)^j binom(N-k,j) a_(k+j)(mu).
```

Do not confuse the dimensionless geometric loss `d_mu` with the density
power differences `d_m(mu)`.

**Theorem 1.** For every integer `q>=2` there is a probability law `nu`
on at most

```
M_q=2 binom(2q+3,3)-1                                      (1)
```

original source sites, with the same original images under T, such that
both marginal moments agree with those of mu through coordinate degree
`2q`. It follows that `d_nu=d_mu=:d`. For every `m>=2`,

```
|a_(m-2)(mu)-a_(m-2)(nu)|
   <= d/(4 m^(5/2)) * (m epsilon/2)^q/q!.                  (2)
```

In particular every entry in row N satisfies

```
|b_(N,k)(mu)-b_(N,k)(nu)| <= d B_(N,q)(epsilon),            (3)

B_(N,q)(epsilon)
 = (N+1)/(4q!) (epsilon/2)^q
   max_(0<=k<=N) binom(N,k)
      sum_(j=0)^(N-k) binom(N-k,j) (k+j+2)^(q-2).           (4)
```

Formula (4) is rational when epsilon is rational. It deliberately uses
`m^(-5/2)<=m^(-2)` to avoid radical bookkeeping. The same nu works for
all rows; choosing q from one row's desired error does not change that
measure's exact moment-matching guarantee.

The cubature existence and exact preservation of d are inherited facts.
The new bound (2) uses the contraction inside a signed Taylor remainder;
separately approximating the two densities by total variation would lose
this factor d.

## 2. Proof of the new remainder estimate

Translate the endpoints separately by a and T(a), and scale by sqrt(s).
Then both clouds lie in `B(0,sqrt(epsilon))`. All quantities above, including
d, are invariant under this normalization. For iid replicas with a common
law, define

```
z_X = (1/2) sum_(i=1)^m |X_i-mean X|^2
    = (1/(2m)) sum_(i<j) |X_i-X_j|^2,
z_Y = (1/2) sum_(i=1)^m |Y_i-mean Y|^2.
```

Here the scaled variance is one. Pairwise contraction and the radius bound
give

```
0 <= z_Y <= z_X <= m epsilon/2,
E(z_X-z_Y)=(m-1)d/4.                                     (5)
```

The dimension-three Gaussian replica identity is

```
a_(m-2)= E[exp(-z_Y)-exp(-z_X)]/[m^(5/2)(m-1)].            (6)
```

This is the standard product formula, with the same normalization as the
accepted global criterion and averaged eighth-beta proof. It is not a
new Gaussian integration identity.

Let `P_q(z)=sum_(r=0)^q (-z)^r/r!` and `R_q(z)=exp(-z)-P_q(z)`.
Taylor's integral remainder for the derivative gives, for `z>=0`,

```
0 <= (-1)^(q+1) R_q'(z) <= z^q/q!.
```

Consequently, whenever `0<=v<=w<=A`,

```
0 <= (-1)^q [R_q(v)-R_q(w)] <= (w-v) A^q/q!.              (7)
```

Use `v=z_Y,w=z_X,A=m epsilon/2` in (7), then (5),(6). If

```
L_m=E[P_q(z_Y)-P_q(z_X)]/[m^(5/2)(m-1)],
E_m=d/(4m^(5/2)) * (m epsilon/2)^q/q!,
```

then

```
a_(m-2) belongs to L_m + (-1)^q [0,E_m].                  (8)
```

Apply the accepted finite-function cubature to the feature list
`(1,x^alpha,(Tx)^alpha : 1<=|alpha|<=2q)`. Its length is (1), so
Caratheodory's theorem gives nu on original pairs. Its degree-two moments
preserve both means and covariance matrices and therefore

```
d=2 tr(Cov(X)-Cov(TX))/s.
```

For each r<=q, the replica polynomial `z_X^r` has degree at most `2r`
in **each** individual replica. Independence expands its expectation into
products of one-point marginal moments. Thus its expectation agrees for
mu and nu; likewise for `z_Y^r`. No source--target mixed moments are needed.
It follows that both laws have the same `L_m` and the same `E_m`.

Both a-values lie in the **same interval of length E_m** in (8). Their
difference is therefore at most E_m, proving (2); there is no extra factor
two. This same-sign observation is why the remainder is kept paired.
Taking the absolute sum of the beta coefficients and using
`m^(-5/2)<=m^(-2)` proves (3),(4).

All expectations are over compact supports and finite polynomials or bounded
exponentials. This justifies all exchanges, including for singular and
nonatomic laws. The proof is valid when d=0, without division by d. In that
case every support distance is preserved by continuity, so both Gaussian
hinge curves agree identically with zero gap.

## 3. An explicit budget independent of the loss

For `q>=2`, the multinomial identity
`sum_k binom(N,k)2^(N-k)=3^N` gives

```
B_(N,q)(epsilon)
 <= (N+1)3^N/[4(N+2)^2] * ((N+2)epsilon/2)^q/q!.          (9)
```

Let `b>=0` be an integer. It is sufficient to take

```
q >= max(2, ceil(3(N+2)epsilon),
             b+2N+ceil(log2(N+1))).                       (10)
```

Indeed `q! >= (q/e)^q`, `e<3`, and (10) imply that the factorial term
in (9) is at most `2^-q`; the remaining power of three is at most `2^(2N)`.
Therefore `B_(N,q)<=2^-b`. The atom budget is

```
M_q=O(((N+1)(1+epsilon)+b)^3),                            (11)
```

with no dependence on d, the original atom count, or a minimum atom mass.
The old marginal-TV estimate would need
`2 sqrt(tau_p(epsilon))<=d 2^-b`, so its required coordinate degree cannot
stay bounded as d tends to zero at fixed positive epsilon.

One may use the exact rational expression (4) for a better degree. For
`A=(N+2)epsilon/2`,

```
B_(N,q+1) <= A B_(N,q)/(q+1).                             (12)
```

Thus (4) decreases on `q>=max(2,ceil A)` and an exact bracket search is
safe there. The companion code checks both the chosen degree and its
predecessor within this decreasing range. These are atom-count budgets,
not claims about the runtime of constructing cubature from an arbitrary
diffuse-law description.

For example, at `epsilon<=1/2`, row N=8 and relative error `2^-10` need
only q=12 by (4), hence at most 5,849 original pairs. This is an approximation
control on an already signed row, not a new eighth-beta proof. At N=32,
the same tolerance uses q=42 and 211,989 pairs. The exact records include
larger radii; there is no high-noise restriction in Theorem 1.

## 4. A finite sign certificate from the retained moments

The same remainder interval can be used before constructing nu. Each `L_m`
in (8) is determined by the finite list of marginal moments through degree
`2q`: expand the scatter polynomial and factor over the independent replicas.
This does not require Gaussian integration or enumeration of all replica
tuples. For example, moments of `sum X_i` and `sum |X_i|^2` can be propagated
by the ordinary binomial/multinomial convolution recurrence.

For a fixed row entry, put `m_j=k+j+2` and

```
c_j=(N+1) binom(N,k) binom(N-k,j),
ell_(N,k)=sum_j (-1)^j c_j L_(m_j),
e_m=(m epsilon/2)^q/(4m^2 q!),
J^- =sum_(j:q+j odd) c_j e_(m_j),
J^+ =sum_(j:q+j even) c_j e_(m_j).
```

Equation (8), again weakening the radical denominator safely, gives

```
ell_(N,k)-d J^- <= b_(N,k) <= ell_(N,k)+d J^+.             (13)
```

The total interval width is at most `d B_(N,q)`. Thus a rigorous lower
bound `ell_(N,k)>=d J^-` is a finite same-row sign certificate. With rational
coordinate moments, the L-values are algebraic combinations of rationals
and square roots of integers; exact algebra or outward radical intervals
suffice. The companion controls check (13) against direct exponential
enclosures and reject a deliberately narrowed interval. This is a new error
bound for the existing beta criterion, not a claim that an arbitrary finite
list of nonnegative beta entries signs every hinge.

## 5. Sign and defect handoff to the accepted hinge modulus

Now assume `0<epsilon<=1/2`, and let `K_epsilon` be precisely the constant
in R8's [loss-dependent modulus](../gaussian_loss_normalized_hinges/PROOF.md),
accepted by its [independent review](../gaussian_loss_normalized_hinges_review_frontier/REVIEW.md).
It asserts for either law that its Bernstein--Durrmeyer polynomial satisfies

```
||P_N-H||_infinity <= d K_epsilon (N+2)^(-1/4).
```

The Bernstein basis is nonnegative and sums to one. Therefore (3) gives
`||P_N(mu)-P_N(nu)||_infinity<=d B_(N,q)`. Combining these three estimates,

```
||H_mu-H_nu||_infinity <= d E_(N,q)(epsilon),
E_(N,q)=2K_epsilon(N+2)^(-1/4)+B_(N,q)(epsilon).            (14)
```

The norm covers `[0,1]`; both hinges vanish above 1. It includes the zero
threshold. This is a uniform full-curve estimate, not a fixed-threshold
moment statement. In particular, if `Delta_mu=max_u(-H_mu(u))_+`,

```
|Delta_mu-Delta_nu| <= d E_(N,q).                          (15)
```

At fixed epsilon, (14) tends to zero after dividing by d: first choose N,
then q. For tolerance zeta>0, take

```
N+2 >= (4K_epsilon/zeta)^4,
B_(N,q)<=zeta/2.
```

The sparse law then preserves every normalized adverse margin of size
`2zeta` with at least half its size, **independently of how small d is**.
No normalized quantity is defined when d=0; that case is decided separately.

For an actual sign certificate, suppose original-law endpoint arguments
establish `H_mu>=0` on `[0,a]` and `[b,1]`. If the finite law's middle
certificate gives

```
H_nu(u) >= d E_(N,q) for every a<=u<=b,                    (16)
```

then (14) signs the remaining interval for mu. Endpoint signs for nu alone
cannot replace the stated signs for mu. A positive uniform approximation
error cannot transfer an endpoint equality into an exact sign.

Alternatively, at arbitrary radius, a row certificate
`b_(N,k)(nu)>=d B_(N,q)` for every k implies every same-row sign for mu by
(3). It does not by itself sign all hinges. These statements provide
explicit usable margins; neither their hypotheses nor an unrestricted
positive margin are asserted here.

## 6. What is preserved, and what is not

The same original contraction and the same support ball are retained.
Means, covariance matrices, d, and the specified moments are preserved
exactly. The cubature weights and source sites may be real; an arbitrary
diffuse input is not converted into an effective finite list without an
input representation/oracle. There is no asserted lower bound on retained
weights or denominators. The old rational rounding step has its own
absolute error and can change d; it must **not** be appended while keeping
the relative-error claim (14). The strict rational families `R^c_k` and
their degree budgets are unchanged.

The all-radius result is the beta-row estimate. The full-curve estimate
uses `epsilon<=1/2` and the accepted functional theorem. It is not silently
applied to the large-radius rational frontier, R2's deep-flap cell, or the
previous near-point prior cell. The constants in the functional degree
bound can be very large. This is an improvement in uniformity near zero
loss, not a uniformly practical algorithm for the full conjecture.

## 7. Reproduction, attribution and trust

Run from this directory, using standard-library CPython 3.11 or later:

```
python3 -B loss_cubature.py
python3 -B -O loss_cubature.py
sha256sum -c SHA256SUMS
```

Expected status: `LOSS_PROPORTIONAL_CUBATURE_PASS`.
`LOSS_CUBATURE_EXPECTED.json` records exact schedules and moment controls;
`LOSS_CUBATURE_INPUTS.json` pins the consumed source. The code validates
the finite scalar, normalization, moment and budget statements. The universal
Taylor/cubature/replica argument and the inherited functional theorem remain
written mathematics. Controls are not independent review or formalization.

The named problem and Gaussian product formula are from Aishwarya--Li,
[arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
Finite-function cubature is classical; see Bayer--Teichmann,
[The proof of Tchakaloff's theorem](https://arxiv.org/abs/math/0502473).
The same-pair construction and exact loss preservation were already recorded
in the accepted cubature packet. The beta normalization and polynomial
criterion are credited to the existing global criterion; the loss-dependent
modulus and its finite sign bridge are R8's independently accepted results.
The [averaged eighth-beta proof](../gaussian_averaged_eighth_beta/PROOF.md)
is used for normalization context, not as a new sign premise. The present
contribution is the paired same-sign Taylor remainder estimate and its
quantitative sparse-measure transfer. No historical priority claim is made
for Taylor approximation or the general moment-matching method.

This packet supplies no new Gaussian sign, no all-variance positive class,
and no Kneser--Poulsen theorem. Its sign relevance is preservation of explicit
normalized margins and the conditional consumer test (16). The accepted
unrestricted `D<=7/50` bound and the full open problem are unchanged.
