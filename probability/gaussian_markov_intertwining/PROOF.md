# A fixed-covariance obstruction to positive Gaussian intertwiners

26 September 2026. Complete author argument; independent mathematical review
and formalization are pending. This closes a proposed **prior-independent
Markov factorization** of the Gaussian-majorisation problem. It does not
prove or disprove the majorisation conjecture, and does not prove the
remaining ordered-contact flux inequality.

Gaussian-preserving channel classifications have substantial prior
literature. In particular, De Palma--Mari--Giovannetti--Holevo, Theorem
III.2, classify Feller operators preserving all Gaussian measures. The
argument here tests only translates of **one fixed covariance**, even on
a bounded open set of means, with no Feller assumption. We give the
elementary proof and a finite quantitative obstruction needed for this
campaign; we make no priority claim for Gaussian-channel rigidity.
See [SOURCES.md](SOURCES.md).

## 1. The proposed factorization and its exact boundary

A Markov kernel K from R^m to R^n sends a probability law P to

    (KP)(B) = integral K(z,B) dP(z).

It may use auxiliary randomness and may depend on the map and the chosen
noise variance. The proposed identity, in the dimension-three application,
is

    K(mu * gamma_t) = (F#mu) * gamma_t
                 for every bounded probability law mu.             (1)

Here K must be the same for all those priors. Testing Dirac laws shows
that (1) is equivalent to

    K N(x,t I_3) = N(F(x),t I_3) for every x.                         (2)

This is a possible additional device for a semigroup argument, not a
known equivalent description of majorisation. Positivity of K alone
would not establish the desired majorisation direction.

**Theorem 1 (local fixed-covariance rigidity).** Let Sigma be positive
definite on R^m, let Gamma be positive semidefinite on R^n, and let C be
a convex subset of R^m with nonempty interior. Suppose a Markov kernel K
and a map F:C->R^n satisfy

    K N(x,Sigma) = N(F(x),Gamma)                 for every x in C.   (3)

Then there are a matrix A and a vector b such that

    F(x)=Ax+b on C,             D=Gamma-A Sigma A^T >= 0,             (4)
    K(z,.)=N(Az+b,D)            for Lebesgue-almost every z.         (5)

Conversely, (4)--(5) imply (3). The kernel is determined only up to a
Lebesgue null set, which no input in (3) can detect. No continuity of
the kernel, smoothness of F, or assumption about other input covariances
is needed. Singular output and conditional Gaussian laws are allowed.

For equal isotropic covariances in equal dimensions, (4) is precisely
that A is a linear contraction. Thus (1) is available exactly for affine
contractions. Allowing K to depend on t, or adding any fixed finite
amount of output Gaussian noise, does not admit a nonlinear F.

### Positive Gaussian transforms force affine means

Write p_x for the density of N(x,Sigma). For x_0=(1-theta)x_1+theta x_2,
0<theta<1, the exact identity is

    p_x0(z)=C_theta p_x1(z)^(1-theta) p_x2(z)^theta,
    log C_theta=theta(1-theta)|x_1-x_2|_(Sigma^-1)^2/2.                (6)

Consequently, for every nonnegative measurable h on the output space,
Holder's inequality gives

    integral h d(KP_x0)
       <= C_theta [integral h d(KP_x1)]^(1-theta)
                    [integral h d(KP_x2)]^theta.                    (7)

Indeed, apply Holder to (Kh)(z) times (6), assigning powers 1-theta and
theta also to Kh. Nonnegative integrals justify the kernel interchange
by Tonelli. In the following application every displayed integral is
finite.

Take h(y)=exp(lambda.y), with arbitrary lambda in R^n. Substitution of
(3) in (7) cancels the common output covariance term and yields

    lambda.[F(x_0)-(1-theta)F(x_1)-theta F(x_2)] <= log C_theta.      (8)

Since lambda is arbitrary, the bracket must vanish. F preserves every
two-point convex combination in C. The elementary affine-extension
property on a convex set with nonempty interior gives F(x)=Ax+b on C.
For example, use an affine basis in an interior simplex and then extend
along segments from that simplex to every point of C. This argument also
shows the following finite obstruction, without any interior assumption:

**Every tested barycentric relation must be preserved.** If x_0 is a
specified convex combination of finitely many tested means x_i, exact
fixed-covariance Gaussian outputs require F(x_0) to be the same convex
combination of the F(x_i). The proof uses the corresponding finite
Holder inequality. A nonlinear midpoint triple already prevents exact
intertwining, even on a three-point parameter set.

### Identification and covariance of the kernel

For u in R^n put h_u(z)=integral exp(iu.y) K(z,dy), so |h_u|<=1. On C,

    P_Sigma h_u(x)=exp(iu.(Ax+b)-u^T Gamma u/2).                     (9)

A Gaussian convolution of a bounded measurable function is real analytic
on all R^m. Its complex Gaussian extension is locally dominated, which
also proves the required analyticity directly. Equality on the interior
of C therefore extends (9) to every real x.

The bounded function

    h_u^*(z)=exp(iu.(Az+b)-u^T D u/2)                               (10)

has the same Gaussian convolution, even before the sign of D is known:
for each fixed u its absolute value is just a finite constant.
Gaussian convolution is injective on bounded measurable functions up to
Lebesgue null sets. For completeness, if P_Sigma h=0, form the finite
complex measure h(z)p_0(z)dz. Its bilateral Laplace transform is entire,
and vanishes on all real arguments by the convolution identity. Its
Fourier transform therefore vanishes as well, so uniqueness of Fourier
transforms of finite measures gives h=0 almost everywhere.

It follows that h_u=h_u^* almost everywhere. The bound |h_u|<=1 gives
u^T D u>=0 for every u. Take a countable dense set of u's to obtain a
single exceptional null set. Outside it, continuity of characteristic
functions in u identifies the whole conditional law as (5). Finally a
Gaussian calculation proves the converse: applying Az+b and then adding
independent N(0,D) noise to N(x,Sigma) gives N(Ax+b,Gamma).

## 2. A strict injective three-site contraction defeats even approximation

The preceding obstruction is not confined to an infinite set of means,
colliding target labels, nonsmooth density levels, or exact arithmetic
equalities with no positive separation.

In R^3 take

    x_-=(-1,0,0), x_0=(0,0,0), x_+=(1,0,0),
    y_-=(1/2,0,0), y_0=(0,0,0), y_+=(3/4,0,0),                      (11)
    P_i=N(x_i,I_3),             Q_i=N(y_i,I_3).

All three targets are distinct. The distance ratios for the pairs
(-,0), (0,+), (-,+) are respectively 1/2, 3/4, 1/8. The global map

    F(x)=((5/8)|x_1|+(1/8)x_1,0,0)                                 (12)

is 3/4-Lipschitz and has the prescribed images. Thus every distinct
tested pair strictly contracts.

**Theorem 2 (positive error for every channel).** For every Markov kernel
K:R^3->R^3,

    max_i TV(KP_i,Q_i) > 1/648,                                    (13)

where TV(P,Q)=sup_B |P(B)-Q(B)|, one half of L1 for densities. In
particular, no sequence of positive channels approximates these three
labelled Gaussian outputs arbitrarily well. The constant is a
conservative exact bound, not the optimal deficiency.

### A bounded-event certificate

Let C_0=exp(1/2). The source Gaussian densities obey

    C_0(p_-+p_+)/2 = cosh(z_1) p_0 >= p_0.                          (14)

Positivity of K propagates this domination to every measurable event B:

    (KP_0)(B) <= C_0[(KP_-)(B)+(KP_+)(B)]/2.                        (15)

Set delta=max_i TV(KP_i,Q_i) and use (15) to obtain

    delta >= [Q_0(B)-C_0(Q_-(B)+Q_+(B))/2]/(1+C_0).                 (16)

Choose the slab B={z:-2<=z_1<=-1}. For each target displacement
m in {1/2,3/4}, its density q_m satisfies on this slab

    log(C_0 q_m/q_0)=1/2+m z_1-m^2/2 <= -1/8.                     (17)

Hence the numerator in (16) is at least
(1-exp(-1/8)) Q_0(B). The following intentionally simple bounds suffice:

    1-exp(-1/8) >= 1/9,
    Q_0(B) > (2 pi)^(-1/2) exp(-2) > 1/24,
    1+C_0 < 3.                                                    (18)

The first uses exp(1/8)>=1+1/8. For the second, integrate over an
interval of length one and use pi<4 and exp(2)<8. The latter follows
from exp(1)<11/4, since 121/16<8. Also exp(1/2)<2. All exponential
upper bounds follow from the rational Taylor-tail bound recorded in
audit.py. Substitution in (16) proves (13). No Gaussian quadrature or
uncertified floating-point sign is used.

### Why this is not a counterexample to the campaign's conjecture

For **every** prior supported on the three sites (11), Gaussian
majorisation nevertheless holds at every positive variance. Apply
the already established dimension-one contraction theorem of
Aishwarya--Li to (12) on the first coordinate. The other two coordinates
are a common independent Gaussian factor. Tensoring preserves the
comparison: for every fixed transverse z, apply the one-dimensional
convex-energy inequality to u -> U(gamma_t^(2)(z) u), then integrate z.
Equivalently one can use positive-part energies and Tonelli.

This is a positive control from existing theory, not a new positive
class. It separates a common channel for all priors from the actual
majorisation obligation. The positive majorisation statement also allows
a prescribed origin mass. Bound (13) concerns the three labelled Gaussian
channels; it is not an error bound for the smaller experiment obtained
by fixing the origin mass and removing the Dirac tests.

## 3. Reversing the universal channel is even more restrictive

A prior-independent kernel R with

    R((F#mu)*gamma_t)=mu*gamma_t for every tested prior mu            (19)

must, on Dirac tests, send N(F(x),tI) to N(x,tI). Total variation
contracts under every Markov kernel, whereas

    TV(N(x,tI),N(x',tI))=2 Phi(|x-x'|/(2 sqrt(t)))-1.                (20)

The likelihood-ratio halfspace proves (20) directly. Its strict
monotonicity implies |x-x'|<=|F(x)-F(x')|. For a 1-Lipschitz F all
tested distances must therefore be equal. A single strictly contracted
pair rules out (19). On a convex full-dimensional domain in R^3 this
leaves only restrictions of affine isometries.

Thus a universal reverse spatial channel cannot supply the desired
Jensen proof for a genuine strict contraction either. This does not
exclude a spatial channel depending on the prior.

## 4. What the obstruction closes, and what remains

The result excludes a specific attempt to transfer heat evolution:
factor the convolved pushforward through the already convolved input by
one positive linear, prior-independent operator. It holds at one fixed
positive variance; no semigroup law in t was assumed. Composing any
number of such Markov operations, or using extra randomness whose law
is independent of the prior, is still one Markov kernel and cannot
avoid the obstruction. Retaining an unobserved input label is a
different model and is not ruled out.

This is not the previous obstruction for orthogonally aligned common
noise. That result concerns a **prior-dependent reverse** posterior
kernel and its failure to preserve Lebesgue measure. Here the forward
kernel is completely arbitrary but must work for every tested prior;
the reverse statement uses that same universal quantifier.

The [global endpoint criterion](../gaussian_majorisation_global_criterion/PROOF.md)
permits its density-value coupling to depend on the law, map and variance.
The [common-set dual](../gaussian_prior_localization/PROOF.md) allows a
target set depending on the source test set, with no demand that those
choices constitute a positive linear operator. Neither is contradicted.
The [fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md)
also remains an exact open criterion; this three-site example cannot
supply a negative majorisation witness for it.

The concurrent [three-cap reflection proof](../gaussian_disjoint_cap_reflections/PROOF.md)
gives a broader positive benchmark by a motion in two auxiliary dimensions.
For a nonaffine cap map on a full-dimensional convex domain, Theorem 1
rules out a universal forward channel on that domain. This is compatible
with the geometric argument, which never requires such a channel. Its
positive theorem remains the geometric lane's author result, awaiting
independent correctness and priority review.

For the PDE lane the remaining exact obligation is unchanged:

    J_f(v) >= J_g(v) at globally ordered concentration-profile contacts,

with the regularized strict-contraction hypotheses of
[CONTACT_REDUCTION.md](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md).
The source and target thresholds agree there; the equivalent posterior
condition uses unweighted covariance integrals on different superlevel
sets. Neither a universal noise channel nor profile order alone supplies
that sign. This pass closes the channel route, and records no advance
on the sign itself or on the full dimension-three theorem.

The audit checks the finite contraction, the slab exponent margins,
and the rational constants in (18). It does not formalize Holder's
inequality, analytic continuation, Gaussian injectivity, or the contact
reduction. Independent acceptance remains pending.
