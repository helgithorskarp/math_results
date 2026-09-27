# Exponentially small all-order defect near the collapsed configuration

Complete analytic author proof with an exact certificate producer. Independent
review and formalization are pending. This is a quantitative consequence of the
existing [signed high-noise window](PROOF.md), not a new proof of that window or
an exact majorisation theorem. Its role is to bound an entire part of the
unrestricted compact search without expanding moments or integrating hinges.

## 1. A support-radius bound for every threshold

Let mu be any probability law supported in a ball of radius R in R3, let T be
1-Lipschitz, and let s>0. Put f=mu*gamma_s, g=(T#mu)*gamma_s,
C=(2 pi s)^(-3/2), and define the adverse defect

    D(f,g)=sup_(a>=0) [H_f(a)-H_g(a)]_+,
    H_f(a)=integral(f-a)_+.

For R>0 write epsilon=R^2/s. If 0<epsilon<=1/2, set

    L(epsilon)=(4-5epsilon)^2/[32epsilon(1-epsilon)]
              =1/(2epsilon)-3/4+epsilon/[32(1-epsilon)],
    E(epsilon)=(8/sqrt(2pi)) sqrt(epsilon) exp[-L(epsilon)]
                                  [L(epsilon)+1+epsilon/6].   (1)

**Theorem.** Simultaneously over all such laws, maps and variances,

    D(f,g) <= min{7/50, E(epsilon)}.                         (2)

For R=0 the defect is zero. For epsilon>1/2 only the already accepted
uniform bound7/50 is asserted here. There is no atom-count, minimum-weight,
pair-slack, covariance-rank or strict-contraction hypothesis.

The new bound tends to zero exponentially, not just as a transport modulus:

    E(epsilon) ~ [4 exp(3/4)/sqrt(2pi)] epsilon^(-1/2)
                                      exp[-1/(2epsilon)]    (3)

as epsilon decreases to zero. Equation(3) is an asymptotic of the explicit
upper bound, not an assertion that any actual defect is positive or that this
rate is optimal. In particular it gives a fixed-variance estimate as a whole
support collapses, and a high-variance estimate for every fixed support radius.

## 2. The Gaussian shell estimate and its exact integration

Translate the two laws separately so both supports lie in B(0,R). For the target
one may use T(a) when B(a,R) contains the source. On a finite input an anchor
site and the pairwise contraction inequalities suffice. For either normalized
density h/C, the elementary distance bounds give

    exp[-(|z|+R)^2/(2s)] <= h(z)/C
                <= exp[-(|z|-R)^2/(2s)] for |z|>=R.

At t=C exp[-r^2/(2s)] with r>=R, its superlevel volume V_h(t) therefore obeys

    (4pi/3)(r-R)^3 <= V_h(t) <= (4pi/3)(r+R)^3.

Consequently, for the two laws at a common threshold,

    |V_f(t)-V_g(t)| <= 8pi R r^2+(8pi/3)R^3.                (4)

This uses the common inner ball as well as the outer ball. Bounding two
individual missing masses would retain an unnecessary r^3 leading term.
The Gaussian level sets have finite volume at every t>0; open or closed level
sets give the same inequalities. Equal total masses give by layer cake

    H_f(a)-H_g(a)=integral_0^a [V_g(t)-V_f(t)] dt.           (5)

If a=C exp(-ell) and ell>=epsilon/2, then r(t)>=R for every 0<t<=a.
Integrating (4), using

    integral_0^a log(C/t) dt = a[log(C/a)+1],

gives the two-sided error estimate

    |H_f(a)-H_g(a)|
       <=(8/sqrt(2pi))sqrt(epsilon) exp(-ell)
                                      (ell+1+epsilon/6).   (6)

No limit of minimum atom masses is involved; (4)--(6) hold for arbitrary
probability laws in the two balls, even without a map between them.

Theorem A of [PROOF.md](PROOF.md) supplies the essential signed input:
H_f(a)<=H_g(a) for a>=C exp[-L(epsilon)]. That theorem also proves
L(epsilon)>epsilon/2 on 0<epsilon<=1/2. For the remaining thresholds use (6).
The function exp(-ell)(ell+1+epsilon/6) decreases for ell>=0, because its
derivative is -exp(-ell)(ell+epsilon/6). Its largest permitted value is
therefore at ell=L(epsilon), proving D<=E. The separate reviewed
[uniform defect theorem](../gaussian_uniform_defect_bound/PROOF.md) gives
7/50, proving (2). Neither theorem is obtained by dropping the signed input.

## 3. An exact compressed bound for compact search cells

For every integer k>=1,

    R^2/s <= 1/(8k)  implies  D(f,g) <= 16 k 2^(-5k).       (7)

Here is a proof using only elementary rational inequalities. The signed window
extends at least down to exp(-L0), where L0=4k-3/4, because
L(epsilon)>=1/(2epsilon)-3/4>=L0. Apply (6) with ell=L0 and epsilon<=1/(8k).
Use

    8/sqrt(2pi)<4,           sqrt(epsilon)<=3/(8sqrt(k)),
    exp(3/4)<=17/8,          exp(4)>32,
    4k+1/4+1/(48k)<=205k/48.

The first inequality only needs pi>2, for example the area of the inscribed
square in the unit disk. For exp(3/4), retain terms of orders zero and one;
the tail starts at9/32 with successive ratios at most1/4, so its sum is at
most3/8. For exp(4), the sum through order four is103/3>32. These bounds give

    D <= (3485/256) sqrt(k) 2^(-5k)
      <= 16 k 2^(-5k),

as claimed. The estimates are intentionally coarse. No numerical exponential
or root is required to consume (7).

For a desired tolerance 2^(-m), m>=0 an integer, choose

    k=1+ceil(m/4),     R^2/s <= 1/[8(1+ceil(m/4))].          (8)

Then (7) is at most2^(-m), since k<=2^k and 4-4k<=-m. This permits a
normalized radius of order1/sqrt(m), rather than a radius exponentially
small in m as a direct L1 displacement budget would require. The comparison
concerns possible adverse defect, not the absolute distance between f and g.

At variance one, (7)--(8) apply directly to every admissible parameter cell of
R3's existing compact frontier whose source sites have the certified radius.
No changes to its atom budget, rational producer or localization are made.
For example radii squared at most1/32 and1/64 give all-threshold bounds
2^(-14) and2^(-33), respectively, uniformly over all priors and contractions.
Such a cell cannot contain a witness with defect larger than the corresponding
tolerance. A positive error budget never certifies an exact zero sign.

## 4. Every beta row and every finite Hankel matrix at the same variance

Use the team's desired-sign profile H(u)=H_g(Cu)-H_f(Cu), 0<=u<=1,
and moment gaps a_j=integral_0^1 u^j H(u)du. Any bound E from (2) or (7)
gives, at this one fixed variance,

    b_(N,j)>=-E  for every N>=0 and 0<=j<=N.                (9)

This follows because each b_(N,j) is the average of H under a probability
Beta(j+1,N-j+1) density. There is no degree-dependent accumulation of error.

More generally, for any nonnegative integer exponents n_1,...,n_d, set

    M_ij=a_(n_i+n_j),         G_ij=1/(n_i+n_j+1).

Then simultaneously for every finite d and every such exponent list,

    M+E G is positive semidefinite.                        (10)

Indeed its quadratic form at v is
integral_0^1 [sum_i v_i u^(n_i)]^2 [H(u)+E]du>=0. The comparison matrix
G is the exact Gram matrix of these monomials, so (10) is a bound on all
quadratic energy tests; it is not just an entrywise moment bound. Repeated
exponents are allowed. No claim that M itself is PSD follows when E>0.

The same bound controls the concentration profiles M_f(v)<=M_g(v)+E by
the standard hinge/profile infimum duality used in the uniform-defect source.
These are consequences of the one pointwise hinge bound, not new equivalence
theorems. The reviewed exact signs N-j<=7 remain stronger on those entries.

## 5. Executable consumer and evidence boundary

Run, from this directory,

```sh
python3 -B radius_defect.py --check
python3 -B -O radius_defect.py --check
python3 -B radius_defect.py --bits 1000000
python3 -B radius_defect.py --radius-squared 1/64 --variance 1
```

The standard-library program also accepts the existing finite-input schema
`source,target,weights` with rational entries, via `--input instance.json`.
It verifies every pair contraction, positive variance and probability weights,
discards zero-weight labels for the support-radius calculation, and selects
the best source-site anchor. It does not calculate a minimum enclosing ball.
The target radius follows from the checked contraction. Output stores a
mantissa and a binary exponent without expanding an enormous denominator.
The scalar radius mode consumes a supplied geometric bound; it does not verify
that an unprovided law or parameter cell satisfies that bound.

Exact controls verify the shell cancellation, normalization after squaring
positive constants, cutoff algebra, rational exponential premises, small
budget ranges, a seven-site paired-rank-six contraction, large compressed
budgets, and malformed-input rejection. The rank-six input is R2's known
positive fold control, scaled by1/8; it is not a new majorisation example.
Its actual hinge defect is zero, whereas this certificate returns the valid
upper bound2^(-33).

The producer is an implementation of the written inequalities. Finite controls
do not prove the universal geometric or coarea statements. The original
high-noise-window theorem remains an explicit analytic dependency awaiting
independent review. Gaussian integration, layer cake and exact Python
integer/Fraction arithmetic are the remaining trust boundary. No full compact
cover, all-threshold exact sign outside known classes, new Kneser--Poulsen case,
optimal exponential rate or historical priority is claimed.
