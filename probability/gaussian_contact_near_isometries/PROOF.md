# An inward first variation excludes Gaussian profile contacts near isometries

26 September 2026. Complete author proof; independent mathematical review
and formalization are pending. This is a quantitative, local sign estimate
for the **actual** concentration profiles. It supplies an exclusion region
for the team's ordered-contact problem, including critical density levels.
It does not establish the unrestricted dimension-three conjecture or a new
Kneser--Poulsen case. In particular, its bounded-input theorem must not be
applied directly to an input with Gaussian tails; Section 6 states the
additional tail budget needed there.

The proof uses the classical posterior-divergence first variation, followed
by a Taylor estimate on the source's actual optimizing set. A refinement of
the team's earlier Procrustes calculation absorbs the Taylor remainder by
pair-distance loss. No monotone path from the input to its contraction is
assumed or constructed. Attribution and the distinction from the R5/R8
reference-set mechanisms are in [SOURCES.md](SOURCES.md).

## 1. Statement

Let n>=1, let X have a probability law mu on R^n, and let T be 1-Lipschitz
on supp(mu). Assume, after centering X, that

    E X=0,          |X|<=R almost surely,          Cov(X)>=kappa I_n,
    R>0,            kappa>0.                                  (1)

Center T(X) and choose an orthogonal Procrustes alignment Q: put
Y=Q(T(X)-E T(X)), where Q minimizes E|Y-X|^2. Equivalently choose the
alignment so that E[X Y^T] is symmetric positive semidefinite. A singular
value decomposition supplies such an alignment even if the cross-covariance
is singular. Fix one such choice and define

    h=Y-X,       delta=ess sup |h|,       M=E|h|^2,
    Delta(X,X')=|X-X'|^2-|Y-Y'|^2 >=0,
    D=E Delta(X,X'),                                          (2)

where primes denote independent copies. The quantity delta is measured
AFTER this alignment; small unaligned displacement or small mean square
error alone is not the stated hypothesis. Orthogonal motions and
translations do not change any profile or flux below.

For t>0 set

    C_t=(2 pi t)^(-n/2),       gamma_t(z)=C_t exp(-|z|^2/(2t)),
    f_t=law(X)*gamma_t,        g_t=law(Y)*gamma_t,
    L_u(v)=sup_(|E|=v) integral_E u,
    omega_n=|B(0,1)|,         r=(v/omega_n)^(1/n),
    q=q(R,t,v)=exp(-[(r+R)^2/2+(r+3R)^2]/t).                 (3)

**Theorem 1 (signed profile estimate).** At every t>0 and 0<v<infinity,

    L_g_t(v)-L_f_t(v)
       >= [v C_t/(4t)] [q-8R delta/kappa] D.                  (4)

Consequently, if

    delta <= kappa q/(16R),                                  (5)

then

    L_g_t(v)-L_f_t(v) >= [v C_t q/(8t)] D.                    (6)

This is strictly positive unless T agrees almost surely with an affine
Euclidean isometry. There is no atom-count bound, lower atom-mass bound,
finite-support assumption, or regular-level hypothesis.

For fixed t0>0 and V>0, the single condition

    delta <= [kappa/(16R)]
       exp(-[(r_V+R)^2/2+(r_V+3R)^2]/t0),
    r_V=(V/omega_n)^(1/n),                                   (7)

gives (6) simultaneously for ALL t>=t0 and 0<v<=V. There is no positive
lower volume cutoff. It is also possible to cover a standardized volume
range r<=L sqrt(t), t>=t0: replace the exponential in (7) by

    exp(-[(L+R/sqrt(t0))^2/2+(L+3R/sqrt(t0))^2]).             (8)

Neither (7) nor (8) covers all positive volumes for a fixed nonzero delta.
The constants are conservative, not claimed optimal.

## 2. The local refinement of Procrustes rigidity

We need the following strengthening of the bounded-radius estimate in
[the earlier entropy-rigidity proof, Section 6](../gaussian_contraction_rigidity/PROOF.md):

    M <= [1/(2 kappa)] E Delta^2 <= [4R delta/kappa] D.        (9)

Here is the argument, recalled to keep the dependency checkable. Regard
the centered coordinate functions of X,Y as finite-rank operators
A,B:R^n->L^2(mu). Set H=AA*-BB*, and let J be orthogonal projection
off the constants in L^2(mu). Double centering of squared distances gives

    H=-(1/2) J Delta J,
    ||H||_HS^2 <= (1/4) E Delta^2.                           (10)

The kernel notation in (10) uses the integral operator with kernel Delta.
The chosen alignment makes A*B symmetric positive semidefinite. With
U=A+B and V=A-B, expansion gives

    ||H||_HS^2
      = (1/2) tr(U*U V*V)+(1/2) tr((U*V)^2)
      >= (kappa/2) ||A-B||_HS^2 = (kappa/2) M.               (11)

Indeed U*V=A*A-B*B is symmetric, while
U*U=A*A+B*B+2A*B >= A*A >= kappa I. Thus both terms used in the
inequality have the required sign. This proves the first inequality (9).

For the refinement, write a=X-X' and b=Y-Y'. Contraction and (1)--(2)
give |b|<=|a|<=2R and |a-b|<=2delta, so

    0<=Delta=(|a|-|b|)(|a|+|b|)<=8R delta.                  (12)

Hence E Delta^2<=8R delta D, proving (9). The refinement uses the
displacement-dependent upper bound (12), in place of the old 4R^2 bound.
It is valid for diffuse as well as atomic laws. No entropy comparison is
used in the argument.

## 3. An inward derivative on the actual source top set

Fix t,v and abbreviate f=f_t. Gaussian mixtures with bounded centers are
positive, real analytic, tend to zero at infinity, and have null positive
level sets. Thus there is a unique a in (0,max f) with

    E={z:f(z)>a},       |E|=v,       integral_E f=L_f(v).     (13)

Put f_theta=law(X+theta h)*gamma_t. We use only its derivative at theta=0,
not monotonicity of the whole straight interpolation. Differentiation gives

    dot f_0=-div(f b),
    b(z)=E[h | X+sqrt(t)Z=z].                              (14)

Denote this posterior law of X by pi_z. Differentiating its Gaussian
likelihood yields

    div b(z)=(1/t) tr Cov_pi_z(h,X)
             =(1/(2t)) E_(pi_z x pi_z) S,
    S=(X-X').(h-h').                                      (15)

All label functions are bounded, so these differentiations are justified
uniformly on bounded z-sets. The endpoint contraction gives the exact
identity and sign

    -2S=Delta+|h-h'|^2 >=0.                                (16)

At a regular level, the divergence theorem and f=a on the boundary give

    I:=integral_E dot f_0
      =-a integral_E div b
      =[a/(4t)] integral_E E_(pi_z x pi_z)
                           [Delta+|h-h'|^2] dz.            (17)

Equation (17) holds also at critical levels. Approximate a by regular
values, using Sard's theorem. Their superlevel sets lie in a common compact
set and converge almost everywhere to E, since {f=a} is null. Both
dot f_0 and div b are continuous and bounded there. Dominated convergence
therefore proves (17). This avoids differentiating the optimizing level or
dividing by |grad f|. It is also the first derivative of L_f_theta(v) by
the usual unique-top-set envelope argument, although that fact is not
needed for the finite Taylor estimate below.

The following elementary bounds make (17) uniform over source laws. On
the ball |z|<=r, f(z)>=C_t exp(-(r+R)^2/(2t)). Since that ball has volume v,

    a>=a0:=C_t exp(-(r+R)^2/(2t)).                          (18)

On the other hand f(z)<=C_t exp(-(|z|-R)_+^2/(2t)). It follows that

    E is contained in B(0,r+2R).                           (19)

For z in E and almost every center x, f(z)<=C_t and |z-x|<=r+3R.
The posterior density relative to mu therefore satisfies

    d pi_z/d mu(x)=gamma_t(z-x)/f(z)
       >= exp(-(r+3R)^2/(2t)).                             (20)

The integrand in (17) is nonnegative. Apply (20) to both labels, and note
E|h-h'|^2=2M because E h=0. Equations (17)--(20) give

    I >= [a v/(4t)] exp(-(r+3R)^2/t) (D+2M)
      >= [v C_t q/(4t)] D.                                (21)

This is an inward derivative with a positive, explicit pair-loss margin.
It concerns a deformation of centers, not the Gaussian-time derivative
whose sign is missing at a general ordered contact.

## 4. The finite remainder and proof of Theorem 1

For any unit e, the Gaussian directional Hessian obeys

    ||partial_ee gamma_t||_infinity <= C_t/t.               (22)

To verify the constant, write u=(e.z)^2/t. The absolute derivative is at
most (C_t/t)|u-1| exp(-u/2). This last scalar factor is at most 1:
on [0,1] it is at most 1, and on [1,infinity) its maximum is
2 exp(-3/2)<1. Orthogonal coordinates only decrease the Gaussian factor.

Taylor expansion in each label displacement h and (22) imply

    integral_E(g_t-f_t) >= I-[v C_t/(2t)] M.                (23)

One may first integrate the pointwise Taylor formula in theta and then in
the input label. All terms are dominated since h is bounded. This estimate
uses the actual source E; it introduces no reference-top-set error. Since
E is an admissible competitor for L_g_t(v),

    L_g_t(v)-L_f_t(v)
      >= integral_E(g_t-f_t)
      >= [v C_t/(4t)] [q D-2M]
      >= [v C_t/(4t)] [q-8R delta/kappa] D,                 (24)

by (9). This proves (4); (5) proves (6). Monotonicity of the explicit q in
its radius and time parameters proves (7)--(8).

If D=0, (9) gives M=0, so the aligned and centered Y equals X almost
surely. Restoring the alignment gives an affine isometry on supp(mu),
using continuity there. Conversely an affine isometry preserves all pair
distances. This proves the claimed strictness. In particular a nontrivial
contraction cannot have equality in (6).

The v factor in the pointwise Hessian bound (23) is essential for covering
volumes approaching zero. Using only an L1 Hessian bound would lose this
factor and give an artificial lower-volume restriction.

## 5. Consequence for ordered contacts

For a Gaussian convolution define the bulk heat flux

    J_u(v)=-integral_(u>a_u(v)) Laplacian u.                 (25)

The [first-contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md)
asks for J_f_t(v)>=J_g_t(v) when the full profiles are ordered and equal
at v. For bounded inputs satisfying (1) and (5), Theorem 1 proves more:
equality of the two profiles at this one volume forces D=0. The two
densities then agree up to a rigid motion at every variance, and

    J_f_t(v)=J_g_t(v).                                     (26)

Thus the ordered-contact flux condition is verified in this explicit
neighborhood of a full-rank isometry. Global profile order was not required
for this local exclusion. There is no inferred inequality between posterior
covariances at different top sets away from the exclusion region.

The sufficient contact class in the cited reduction instead starts with
rho=xi*gamma_epsilon and applies a globally strict contraction F AFTER
that regularization. Such rho is unbounded; moreover F with Lipschitz
constant c<1 cannot be uniformly close to an isometry on all of R^n.
Consequently (1)--(5) cannot simply be asserted for that class.

## 6. An explicit tail budget for the actual auxiliary class

Let mu now be any probability law, possibly unbounded, and let T be a
contraction. Choose a measurable bounded core of mass m in (0,1], and write

    mu=m mu_0+(1-m)mu_1.                                   (27)

Apply the centering and alignment above to mu_0. Suppose its parameters
R,kappa,delta satisfy (5) at the chosen t,v, and let D_0 be its conditional
pair-distance loss. Put

    B_0=[v C_t q(R,t,v)/(8t)] D_0.                          (28)

The full profiles satisfy the signed estimate

    L_(T#mu)*gamma_t(v)-L_mu*gamma_t(v) >= m B_0-(1-m).      (29)

Indeed for positive probability densities u=m u_0+(1-m)u_1,

    m L_u_0(v) <= L_u(v) <= m L_u_0(v)+(1-m).

Use the lower bound for the target and the upper bound for the source,
then apply (6) to the core. Rigid alignment of the whole target does not
change these profiles. The case m=1 is Theorem 1.

Thus any contact, ordered or otherwise, must satisfy

    1-m >= m B_0                                           (30)

for EVERY such certified core. Strict reversal of (30) excludes a contact
in the unbounded auxiliary class as well. The core covariance, aligned
displacement and tail mass must actually be bounded; no automatic control
relative to D_0 is assumed. This is a usable sufficient test, not a claim
that every Gaussian-tailed contraction passes it.

### Nonvacuity within the exact auxiliary class

Here is a deliberately simple check of the quantifiers in (29), not a new
positive map class. Take n=3, xi a point mass at zero,

    epsilon=10^(-6),    rho=gamma_epsilon,
    F(x)=(1-10^(-8))x, t=1, v=4 pi/3,
    core={|x|<=1/100}.                                    (31)

The full input is unbounded and F is globally strict. The conditional
core is centered and radial, so the identity is its Procrustes alignment.
For a standard three-dimensional Gaussian Z, integration by parts gives

    P(|Z|>10) <= 11 exp(-50),
    E[|Z|^2 1_(|Z|>10)] <= 1031 exp(-50).                 (32)

For example its radial density is sqrt(2/pi) u^2 exp(-u^2/2); use
integral_10^infinity exp(-u^2/2) du <= exp(-50)/10.
The elementary bounds 8/3<e<3 imply

    1-m < 11(3/8)^50 < 10^(-19),
    kappa=1/(2*10^6) is a valid covariance lower bound.     (33)

For the latter statement, spherical symmetry and the second bound (32)
give E[Z_i^2;|Z|<=10]>2/3, since 1031(3/8)^50<1.
Conditioning divides by m<=1, so the claimed kappa is conservative.
Also R=1/100, delta=10^(-10), and

    D_0 >= 3*10^(-14),
    [(1+R)^2/2+(1+3R)^2]=31419/20000<2,
    q>1/9,       delta<kappa/(144R).                       (34)

Here D_0=2[1-(1-10^(-8))^2] E|X|^2 and E|X|^2>=3kappa.
The usual bounds 3<pi<22/7 give v>4 and C_1>1/16; for the latter,
(44/7)^3<256. Therefore m>1/2 and

    m B_0 > (3*10^(-14))/576 > 10^(-19) > 1-m.            (35)

This supplies a strictly positive certified margin in (29) for an input
of exactly the auxiliary type. Homothety already has full majorisation;
(31)--(35) only verify that the new tail test is not vacuous on that type.
The rational comparisons in (33)--(35) are audited in [audit.py](audit.py).

## 7. What this resolves and what remains

The new sign control is (4)--(6): an endpoint profile gap, obtained from
an inward center variation, on a neighborhood with explicit radius and
covariance data. It rules out all nonisometric bounded contacts there,
including critical levels and arbitrarily small positive volumes. The
separate core budget (29) retains the exact cost for unbounded inputs.

It does not control covariance collapse, arbitrary large volumes, vanishing
heat time, large aligned displacement, or an unbounded input whose tail
exceeds the core margin. In particular it supplies neither a universal
tail-to-pair-loss estimate nor the general sign of the unweighted posterior
covariance integral in the contact reduction. These are actual remaining
obligations, not hypotheses to be inferred from global profile order.

The proof is analytic and uses Gaussian differentiation, the divergence
theorem, regular-value approximation, finite-rank operator identities and
Taylor's theorem. The exact audit checks algebraic identities and the
explicit example, not the universal analytic claims. No quadrature,
solver, exhaustive search, hidden corpus or independent acceptance is used.
