# Shift averaging does not cancel the Gaussian partition interaction

Complete author proof; independent review pending. This supplement closes
one proposed route from [defect localization](DEFECT_LOCALIZATION.md) to an
exact comparison. It is a counterexample to an interaction-order inequality,
**not** to Gaussian majorisation. Indeed its labelled sites admit a strict
contracting motion in dimension three, so their full Gaussian comparison
is already covered by Aishwarya--Li, Theorem 1.4.

## 1. The missing inequality and the example

For an integrable nonnegative function f, write

    H_f(a) = integral_R3 (f-a)_+,       a>=0.

For a finite family of subdensities f_i, let

    I(f_i;a) = H_(sum_i f_i)(a)-sum_i H_(f_i)(a) >= 0.       (1)

If f_i,g_i have matched masses p_i, then the exact decomposition is

    H_f(a)-H_g(a)
      = sum_i p_i[H_(f_i/p_i)(a/p_i)-H_(g_i/p_i)(a/p_i)]
        + I(f_i;a)-I(g_i;a).                               (2)

The localization proof bounds the last source interaction by a boundary
crossing error and discards the nonnegative target interaction. A possible
shortcut would remove that error by proving

                 E_U I(g_i;a) >= E_U I(f_i;a),             (3)

where U is the random shift of the source partition. The following theorem
disproves (3) for actual Gaussian data, even with injective strictly
contracting endpoints and maximal paired affine rank.

Let gamma(z)=C exp(-|z|^2/2), C=(2 pi)^(-3/2), and fix

    a=C/256,       ell>0.

Index eight equally weighted sites by sigma in {-1,1}^3, and put

    x_sigma = t sigma,
    Q(sigma) = (sigma_2 sigma_3, sigma_1 sigma_3, sigma_1 sigma_2),
    y_sigma = (t/2) sigma + t^4 Q(sigma).                   (4)

For U uniform on [0,ell)^3, group the source sites by the half-open cubes
U+ell(m+[0,1)^3), m in Z^3. Each nonempty group defines

    f_i(z) = (1/8) sum_(sigma in group i) gamma(z-x_sigma),
    g_i(z) = (1/8) sum_(sigma in group i) gamma(z-y_sigma).

The target retains the **source labels**; it is not repartitioned by its
own spatial cells. Write I_f(U)=I(f_i;a), I_g(U)=I(g_i;a), and define

    K(b) = (2 pi/3) b [2 log(C/b)]^(3/2),       0<b<C.

**Theorem.** For every fixed ell>0,

    lim_(t down to 0) (ell/t^3) E_U[I_g(U)-I_f(U)]
      = -(9/2) K(a) [4(7/8)^(3/2)-3]
      < -(9/8) K(a) < 0.                                 (5)

Consequently (3) is false for all sufficiently small positive t. The
sites in (4) have paired affine rank six for every t>0. For 0<t<1/2,
both endpoint sets have eight distinct sites, the endpoint map is strictly
contracting, and straight interpolation is a strict contracting motion.
Thus the full Gaussian majorisation holds for these endpoints at every
variance, with every choice of nonnegative weights of total one.

The proof supplies a sufficiently-small-t family, not an explicit numerical
cutoff for t. In particular the rational values used by the geometry audit
are not claimed to certify the sign of an integrated Gaussian quantity.

## 2. Hinge expansion for a small cube

Let h_(q,t) be gamma convolved with the uniform law on the 2^q sites
(t sigma_1,...,t sigma_q,0,...,0), for q=0,1,2,3. In particular h_(0,t)=gamma.
The Gaussian and all its derivatives are integrable. Taylor expansion of
translations in L1, followed by sign averaging, gives

    (h_(q,t)-gamma)/t^2 -> (1/2) sum_(j=1)^q partial_jj gamma
                           in L1 as t -> 0.               (6)

For completeness, the first derivatives cancel, and the average of
sigma_i sigma_j is zero for i!=j and one for i=j. The second-order Taylor
remainder is o(t^2) in L1 by L1 continuity of translated second derivatives.
There are only finitely many translated terms.

If v_epsilon -> v in L1 and |{gamma=b}|=0, then

    [H_(gamma+epsilon v_epsilon)(b)-H_gamma(b)]/epsilon
           -> integral_{gamma>b} v.                      (7)

To prove this, replace v_epsilon by v using the L1 Lipschitz bound for
H. For fixed v the pointwise difference quotient converges off the level
set and is dominated by |v|. Apply dominated convergence. For 0<b<C,
the level of gamma is a sphere and has zero volume.

Put r=sqrt(2 log(C/b)). The divergence theorem and spherical symmetry give

    (1/2) integral_{|z|<r} partial_jj gamma
       = -(b/(2r)) integral_{|z|=r} z_j^2 dS
       = -(2 pi/3) b r^3 = -K(b).

Equations (6)--(7) therefore imply

    H_(h_(q,t))(b) = H_gamma(b)-q K(b)t^2+o(t^2).

Define the normalized contraction gap

    G_q(t,b) = H_(h_(q,t/2))(b)-H_(h_(q,t))(b).

Then

    G_q(t,b) = (3/4)q K(b)t^2+o(t^2).                     (8)

Only q=0,1,2,3 and b in {a,2a,4a,8a} will occur, all with b<C, so
these finitely many remainders can be taken simultaneously. G_0 is zero.

## 3. Average the source grid before perturbing the targets

First use the homothetic targets ybar_sigma=(t/2)sigma. Suppose 0<2t<ell.
In each coordinate the random grid separates -t and t with probability
p=2t/ell. The three events are independent. If J coordinates split, there
are 2^J components, each with mass 2^(-J). After translation each normalized
source component has density h_(3-J,t), and each normalized target
component has density h_(3-J,t/2). Hinge integrals are translation invariant.

The scaling identity H_(p h)(a)=p H_h(a/p) thus gives the exact formula

    I_gbar(U)-I_f(U) = G_3(t,a)-G_(3-J)(t,2^J a).          (9)

There is no contribution when J=0. Since J has the Binomial(3,2t/ell)
law, the J=1 probability is 6t/ell+O(t^2). The probabilities for J>=2
are O(t^2), while their gaps in (9) are O(t^2). Applying (8) yields

    E_U[I_gbar(U)-I_f(U)]
      = (9/(2ell)) [3K(a)-2K(2a)]t^3+o(t^3).              (10)

At the selected threshold, K(2a)/K(a)=2(7/8)^(3/2). The sign in (5)
needs no numerical logarithm, Gaussian integral or approximation of pi:

    (7/8)^3-(13/16)^2 = 5/512 > 0,
    4(7/8)^(3/2)-3 > 1/4.                                (11)

Thus even shift averaging of the fixed-axis cubic grid leaves a negative
target-minus-source interaction. Averaging rotations of the grid, or
choosing a different adaptive partition, is not covered by this argument.

## 4. Restore full paired rank without changing the limit

The perturbation from ybar_sigma to y_sigma has length sqrt(3)t^4.
For equal-mass nonnegative densities u,v,

    |H_u(a)-H_v(a)| <= (1/2)||u-v||_1.

This follows from the variational expression for H and the equality of
the masses. The variance-one Gaussian translation estimate is

    (1/2)||gamma(. -z)-gamma(. -z')||_1
           <= |z-z'|/sqrt(2 pi).

It follows by integrating the directional Gaussian derivative along the
translation. Averaging over the centers proves the same bound for mixtures.
Apply it to the full target mixture and separately to each labelled
component. The component masses sum to one, so uniformly over U,

    |I_g(U)-I_gbar(U)| <= sqrt(6/pi)t^4.                   (12)

For fixed ell this is o(t^3/ell), proving (5) for the final targets (4).

The seven functions

    1, sigma_1, sigma_2, sigma_3,
       sigma_2 sigma_3, sigma_1 sigma_3, sigma_1 sigma_2

are nonzero mutually orthogonal Walsh characters on the eight cube vertices.
For t>0 their span is exactly the span of 1 and the six coordinates
of (x_sigma,y_sigma). Hence its dimension is seven and the paired affine
rank is six. In particular neither endpoint support lies in a proper
affine subspace of R3.

For distinct sigma,tau write

    u=x_sigma-x_tau,    e=t^4[Q(sigma)-Q(tau)],
    v=y_sigma-y_tau=u/2+e.

If the two sign vectors differ in h=1,2,3 coordinates, their Q vectors
differ in respectively k=2,2,0 coordinates. Thus

    |e|^2/|u|^2 = t^6 k/h <= 2t^6 < 1/4,    0<t<1/2.    (13)

The triangle and reverse triangle inequalities give 0<|v|<|u|. Moreover

    v.(u-v) = |u|^2/4-|e|^2 > 0.

Along the linear path u_s=(1-s)u+s v, the derivative of |u_s|^2 is
nondecreasing in s, and its value at s=1 is -2v.(u-v)<0. It is therefore
negative throughout [0,1]. This proves the strict contracting motion
claim. Theorem 1.4 of the [primary paper](https://arxiv.org/html/2609.07041v2)
then gives full Gaussian majorisation for every law on these eight labels.

## 5. Consequence for localization, and the remaining obligation

An exact decomposition must retain both the conditional comparison gaps
and the interaction difference in (2). The latter does not acquire the
desired sign simply by averaging shifted grids, even on a full-rank strict
contraction with a known positive full comparison. Conditional positive
gaps compensate the adverse interaction in this example.

This does **not** disprove a possible zero-error inequality for the
*positive defects* Delta(mu,T): here the global and every conditional
defect are zero. Nor does it refute the existing localization theorem,
which charged a nonnegative source error and never asserted (3).
The uniform finite frontier and its error bound remain unchanged.
Any further exact localization argument needs a stronger relation that
retains conditional gaps, or a different sign mechanism. No new positive
Kneser--Poulsen class, full-question resolution, or independent acceptance
is obtained from this obstruction.

The [exact audit](interaction_audit.py) checks the cube partitions, Walsh
rank, all 28 pair types, straight-motion geometry at rational parameters,
the shift-probability polynomial and the rational sign margin (11).
[INTERACTION_EXPECTED.json](INTERACTION_EXPECTED.json) is its compact output.
It uses standard-library exact fractions, not quadrature. The asymptotic
hinge expansion and its strict sign are established by the written proof;
finite geometry checks do not replace that analytic argument.
