# A global first-contact reduction for Gaussian majorisation

Complete author proof; independent review and formalization are pending.
The unrestricted dimension-three conjecture remains open. The result below
reduces it to a heat-flux inequality at ordered contacts. It does not prove
that inequality, find a contact, or give a new Kneser--Poulsen theorem.

The previous [coefficient obstruction](PROOF.md) rules out an unconditional
ordering of the two diffusion coefficients. Here the flux is tested only
where the *entire* concentration profiles are ordered and touch. Smoothing
the input before applying a strict contraction supplies genuine initial
order and uniform control at both volume ends. An additional scalar
dilation removes a possible tangential first crossing in time.

## 1. Statement and the remaining inequality

Let gamma_t be the Gaussian of covariance t I_3. For a positive density u,
put

    L_u(v) = sup_{|E|=v} integral_E u.

If u is a Gaussian convolution and 0<v<infinity, there is a unique a_u(v)
with |{u>a_u(v)}|=v. Define the **bulk flux**

    J_u(v) = - integral_{u>a_u(v)} Delta u.                 (1)

At a regular level this is the familiar surface integral of |grad u|.
Definition (1) also makes sense at critical levels; no division by a
vanishing gradient is used.

Consider the following test class. Let xi be a finite positive probability
law on R3, epsilon>0, and let F:R3->R3 have Lipschitz constant c<1. Set

    rho = xi * gamma_epsilon,
    f_t = rho * gamma_t,
    g_t = (F#rho) * gamma_t,                 t>0.           (2)

**Contact condition C.** For every choice (2), every t>0 and v>0, if

    L_g_t(w) >= L_f_t(w) for all w>0,
    L_g_t(v) = L_f_t(v),

then

    J_f_t(v) >= J_g_t(v).                                 (3)

**Theorem 1.** The full Gaussian-majorisation conjecture for bounded
probability laws and 1-Lipschitz maps in R3 is equivalent to C.

More precisely, any strict violation for bounded data gives data (2),
a time t_*>0 and a finite v_*>0 such that the two profiles are ordered
at t_*, touch at v_*, and

    J_f_t_*(v_*) < J_g_t_*(v_*).                           (4)

The profiles are strictly ordered for every positive volume at every
earlier positive time. At the contact their density thresholds also agree:
a_f_t_*(v_*)=a_g_t_*(v_*). The contact levels need not be regular.

Thus a *weak* inequality (3), including critical levels via (1), would
settle the full question. A merely regular-level version is not proved
sufficient here. None of the arguments below establishes (3).

The auxiliary input rho has Gaussian tails and unbounded support. This is
intentional. A violation for it transfers to a bounded input by truncation;
conversely a bounded violation survives the regularization in (2). One
must apply F to the regularized input: F#(xi*gamma_epsilon) is generally
different from (F#xi)*gamma_epsilon.

## 2. Profiles are C1 through critical levels

For the Gaussian convolutions used here, including compact families of
positive variances and positive dilation parameters, the following hold:

* the densities are strictly positive, real analytic, vanish at infinity,
  and have null positive level sets;
* every positive superlevel set is bounded, uniformly on compact parameter
  families when its level is bounded away from zero;
* the density and the parameter derivatives used below vary continuously
  in L1 and locally uniformly.

These facts follow from differentiation of the Gaussian kernel, boundedness
of its derivatives, and the finite moments of F(X+sqrt(epsilon)Z).
Uniform tightness and Gaussian decay give the uniform superlevel bound.
Real analyticity follows by the locally dominated complex Gaussian
extension; a nonconstant real analytic function has null level sets.

Write H(p,a)=integral (u_p-a)_+, with p the time and dilation parameters.
Dominated differentiation, using null level sets, gives

    H_a = -|{u_p>a}|,       H_p = integral_{u_p>a} partial_p u_p. (5)

These derivatives are continuous. The level volume decreases continuously
and strictly from infinity to zero as a increases from zero to max u_p.
Strict decrease follows because every intermediate density interval has
a nonempty open inverse image. Its inverse a(p,v) is continuous.

The identity L(p,v)=min_a[H(p,a)+av] and its unique minimizing level give,
by the two elementary envelope inequalities,

    L_v=a(p,v),             L_p=integral_{u_p>a(p,v)} partial_p u_p. (6)

For example bound a difference quotient of the minimum by using its old
and new minimizers and then use their continuity. This proves C1 without
differentiating a(p,v). In particular, at *every* positive finite volume,

    partial_t L_u(t,v) = -J_u(t,v)/2.                      (7)

The function J in (1) is continuous in these parameters and v. Critical
levels do not prevent (6)--(7). We do not assert a globally smooth second
volume derivative or a bounded diffusion coefficient JB.

We also need strictness under target dilation. If Y has the law F#rho
and u_{t,lambda}=law(lambda Y)*gamma_t, then for lambda>0,

    partial_lambda L_u(t,lambda,v)
      = - a/(t lambda) integral_{u>a} tr Cov(lambda Y | lambda Y+sqrt(t)Z=x) dx.
                                                               (8)

This is negative whenever Y is not a point mass. To check it, the density
satisfies the continuity equation with velocity E[Y|x]. The divergence of
that velocity is tr Cov(lambda Y|x)/(t lambda). At a regular level,
integration by parts gives (8). Both sides are continuous in the level,
so regular-value approximation proves it at every level. The covariance
trace is everywhere positive for a nonpoint law because all Gaussian
posterior likelihoods are positive. The bounded moments justify these
steps even though Y need not be bounded.

Formula (8) is the concentration-profile version of the already published
strict homothety identity in
[the stability proof, Section 4](../gaussian_majorisation_open_stability/PROOF.md).
It is an input here, not a new strictness theorem.

## 3. A uniform tail bound from the regularized input

This is the estimate that prevents a first failure from escaping to
infinite volume at time zero. It uses the strict Lipschitz constant and
the Gaussian component of the *input*, not a Kneser--Poulsen assumption.

Let |X|<=R, rho=law(X+sqrt(epsilon)Z), F(0)=0, and Lip(F)<=c with
0<c<1. Fix 0<S<infinity. For 0<=t<=S, define f_t and g_t as in (2),
interpreting g_0 as a measure if necessary. For measures use
L_nu(v)=sup_{|E|<=v} nu(E). Put v=4 pi r^3/3.

Since f_t is a mixture of translates of gamma_{epsilon+t}, maximization
over E and then averaging give

    1-L_f_t(v) >= Q_3(r/sqrt(epsilon+t)),                  (9)

where Q_3 is the standard three-dimensional Gaussian radial tail. Also,
with independent standard three-dimensional Gaussians Z,Z',

    |F(X+sqrt(epsilon)Z)+sqrt(t)Z'|
       <= cR + sqrt(c^2 epsilon+t) sqrt(|Z|^2+|Z'|^2).     (10)

Taking the ball of volume v as a competitor for L_g and applying the
six-dimensional Gaussian squared-norm moment-generating function gives,
for 0<theta<1/2 and r>=cR,

    1-L_g_t(v)
      <= (1-2theta)^(-3)
         exp[-theta (r-cR)^2/(c^2 epsilon+t)].            (11)

This applies at t=0 even if the pushforward is singular.

Here is one explicit uniform cutoff. Set

    eta = epsilon(1-c^2)/(2(epsilon+S)),
    theta = (1-eta)/2,
    A = eta/[2(c^2 epsilon+S)],
    B = (1-eta)R/(c epsilon),

and take

    r >= r_+ := max{
       cR, 2B/A,
       sqrt(2[3 log(1/eta)+1]/A),
       sqrt(pi(epsilon+S)/2)}.                            (12)

Indeed (c^2 epsilon+t)/(epsilon+t)<=1-2eta, whence

    theta/(c^2 epsilon+t) - 1/[2(epsilon+t)] >= A.

One can check this without an estimate: writing q=c^2, the difference
between the left side and A is exactly

    eta (S-t)[epsilon(1+2q)+2S+t]
      / [2(q epsilon+t)(epsilon+t)(q epsilon+S)] >= 0.

Consequently

    theta(r-cR)^2/(c^2 epsilon+t) - r^2/[2(epsilon+t)]
       >= A r^2-Br >= A r^2/2 >= 3 log(1/eta)+1.          (13)

The elementary bound Q_3(z)>=sqrt(2/pi) z exp(-z^2/2) and the last
condition in (12) make its prefactor at least one. Equations (9)--(13)
therefore prove the stronger uniform conclusion

    1-L_g_t(v) <= exp(-1) [1-L_f_t(v)],
    L_g_t(v)>L_f_t(v)                  (r>=r_+, 0<=t<=S). (14)

The constants are deliberately conservative. They deteriorate as
epsilon decreases to zero or c increases to one. Thus (14) does not
remove the atomic geometric initial layer or give uniform control of
arbitrary tiny distant packets. It does not contradict the team's
obstruction to a general relative-deficit perturbation estimate.

For target dilations lambda in a compact interval with
lambda_max Lip(F)<1, use c=lambda_max Lip(F) throughout. All these tail
estimates are then uniform in lambda.

## 4. Strict initial order and the small-volume boundary

The density rho=xi*gamma_epsilon is bounded, positive everywhere, analytic,
and vanishes at infinity. Write L_0=L_rho and m_0=max rho. A c-Lipschitz
map sends a compact set E to a set of volume at most c^3|E|. Therefore

    L_F#rho(v) >= L_0(v/c^3)>L_0(v),             v>0,     (15)

where strictness uses positivity of rho everywhere. This argument permits
a singular pushforward and does not differentiate F.

For clarity about persistence as t decreases to zero, choose u with
v<u<v/c^3 and a compact optimal source superlevel set E of volume u.
The compact image A=F(E) has volume strictly below v. For a sufficiently
small spatial neighborhood A^h, its volume is still below v. Hence

    L_g_t(v) >= rho(E) Pr{|sqrt(t)Z|<h} -> L_0(u)>L_0(v). (16)

Meanwhile L_f_t(v)<=L_0(v), since convolution cannot increase a
concentration profile. Slightly shrinking the volume budget and enlarging
the volume at which L_0 is evaluated makes (16) uniform on a neighborhood
of any fixed v. A finite cover makes it uniform on a compact interval of
positive volumes.

These statements are uniform over a compact target-dilation interval
with maximal Lipschitz constant c<1. The source set E can stay fixed.
If A=F(E), then (lambda A)^h=lambda(A^(h/lambda)); outer continuity
of volume and lambda bounded away from zero give the required uniform
neighborhood-volume bound.

There is also a uniform interval next to zero volume. Choose k with
c^3<k<1 and then u>0 small enough that

    L_0(u)>m_0 k u.

Use the same compact-image argument with volume budget v_0=ku to get
L_g_t(v_0)>m_0 v_0 for all sufficiently small t, uniformly in lambda.
For t>0 the profile is concave and vanishes at zero, so
L_g_t(v)/v>=L_g_t(v_0)/v_0 for 0<v<=v_0. Since max f_t<=m_0, this
proves strict order throughout that small-volume interval.

To extend the small-volume bound to a fixed compact interval of positive
times, use the established sharp posterior peak inequality:

    log(max g_t/max f_t)
      >= E_{posterior at a source mode}^{tensor 2}
          [|U-U'|^2-|F(U)-F(U')|^2]/(4t) > 0.            (17)

This is Theorem C and Section 5 of
[the existing rigidity proof](../gaussian_contraction_rigidity/PROOF.md),
including its allowance for unbounded input. It is not new here. The
strict sign follows from c<1 and the nonpoint posterior of rho.

The short reason is worth recalling. At a source mode z the source
posterior has mean z. Evaluate g at the mean of F(U) under that same
posterior and apply Jensen to the Gaussian likelihood ratio. The log
ratio is at least [Var(U)-Var(F(U))]/(2t), which is the right side of
(17). The posterior has finite moments; no differentiability of F enters.

Both peak values are continuous in positive time and lambda. On a compact
parameter set their positive difference thus has a positive minimum.
Gaussian derivative bounds give a uniform spatial Lipschitz bound for
g_t. A small ball around a target maximizer then has density above the
source maximum. Taking subsets of this ball proves strict order for all
sufficiently small volumes, uniformly on the compact parameter set.

Combining this fact, (14), and (16) gives the needed boundary statement:

**Lemma 2.** For fixed data (2), a fixed horizon S, and a compact positive
dilation interval whose maps all have Lipschitz constant less than one,
there exist t_0>0 and 0<v_-<v_+<infinity such that

* every positive volume is strictly ordered for 0<t<=t_0;
* for every 0<t<=S, volumes v<=v_- and v>=v_+ are strictly ordered;
* all statements hold uniformly over the dilation interval.

Take v_+ from (12), obtain v_- from the two small-volume arguments, and
then apply the finite-cover argument (16) on [v_-,v_+]. Decrease t_0 if
necessary. No regularity of the contact levels is used.

## 5. Every bounded failure survives this normalization

A strict bounded-law hinge failure first has a finite witness: finite
approximation of the input and its exact mapped labels changes the
convolved densities in L1 by arbitrarily little. A slight common target
homothety preserves the failure and makes the finite map strictly
contracting. Kirszbraun extension supplies a globally c-Lipschitz map
with c<1. These are the existing strict finite-witness reductions; the
Gaussian translate estimate below also verifies their continuity step.

Suppose the resulting finite pair has a hinge gap -d<0 at variance S.
For X with that finite law, put U=X+sqrt(epsilon)Z and Y=F(U).
The L1 translation estimate

    ||gamma_S(. -x)-gamma_S(. -y)||_1
       <= sqrt(2/(pi S)) |x-y|

and the 1-Lipschitz property of the hinge functional give a change in
the two-endpoint hinge gap at most

    sqrt(2/(pi S))(1+c)sqrt(epsilon) E|Z|
       = 4(1+c)sqrt(epsilon)/(pi sqrt(S)).                (18)

In particular epsilon<pi^2 S d^2/[64(1+c)^2] retains a gap below -d/2.
We now have (2) with a strict failure at time S.

The target cannot be a point mass. A point target gives gamma_S, whereas
f_S is a mixture of translates of gamma_{epsilon+S} and is strictly less
concentrated than gamma_S at every positive finite volume.

Translate the target to have F(0)=0. Choose a closed dilation interval
I=[lambda_-,lambda_+] around 1, with lambda_->0 and lambda_+ c<1,
small enough that every lambda in I still has the same strict hinge
failure at time S. L1 continuity in lambda justifies this choice.
At the source optimizing volume for that hinge, every one of these
profiles has a strict concentration failure as well. Lemma 2 applies
uniformly over I.

## 6. A transverse first contact

Put

    W(t,lambda,v)=L_{law(lambda Y)*gamma_t}(v)-L_f_t(v).

It is C1 on positive times, dilations, and volumes. By Lemma 2 all possible
zeros before S lie in one compact interval V=[v_-,v_+], and at a small
time t_0 every profile is strictly positive. At time S each lambda has
a negative value in V. Equation (8) gives W_lambda<0; on the compact
box [t_0,S] x I x V it is bounded above by a strictly negative number.

For fixed (t,v), define b(t,v) as the zero of W in I if there is one,
clipped to lambda_- when W(t,lambda_-,v)<=0 and to lambda_+ when
W(t,lambda_+,v)>=0. The uniform negative lambda derivative and the
bounded time derivative show directly by the mean-value theorem that
b is Lipschitz in time with one common constant. It is continuous in v.
Consequently

    b_*(t)=min_{v in V} b(t,v)                            (19)

is Lipschitz, equals lambda_+ at t_0, and equals lambda_- at S.

For a Lipschitz function of one real variable, the image of its
nondifferentiability set and of the set where its derivative is zero
has one-dimensional measure zero. This follows from Rademacher's theorem,
the null-set property of Lipschitz maps, and the one-dimensional area
formula on the zero-derivative set. Thus choose lambda strictly between
the two endpoints outside that exceptional image.

Let t_* be the first time b_*(t)<=lambda. Then t_*>t_0,
b_*(t_*)=lambda, and b_*'(t_*)<0: earlier values are strictly larger,
and the derivative exists and is nonzero by the choice of lambda.
Choose v_* attaining (19). Since its clipped value is interior to I,
it is an actual zero and the implicit-function theorem applies to
b(t,v_*) near t_*.

The functions b(t,v_*) and b_*(t) agree at t_*, and the former is always
at least the latter. Their derivatives at that time therefore agree.
Differentiating its zero equation gives

    W_t(t_*,lambda,v_*) = -W_lambda(t_*,lambda,v_*) b_*'(t_*) < 0. (20)

All volumes have W(t_*,lambda,v)>=0, and all earlier positive times have
strict order. Also W(t_*,lambda,v_*)=0. The volume derivative is zero at
this interior minimum, so (6) gives equality of the two density levels.
Finally (7) turns (20) into (4). Replace F by lambda F to obtain exactly
the test class in Theorem 1.

This step is essential. At an arbitrary first contact, a zero time
derivative would not rule out a later sign change. The scalar perturbation
and (19) produce a genuinely transverse contact, so a weak inequality
in C is sufficient. No assumption of a unique minimizing volume, a
nondegenerate contact, or a regular density level is made.

## 7. Completion of the equivalence and checks on its scope

If C holds, Sections 5--6 contradict any bounded-law failure, proving
the full conjecture. Conversely, suppose that conjecture holds for bounded
laws. Truncate and renormalize rho in (2); total-variation convergence of
the input and its pushforward gives L1 convergence of both convolutions,
and hence uniform convergence of their concentration profiles. Thus
the conjecture also holds for (2) at every positive time.

At any contact, the nonnegative C1 function t->L_g_t(v)-L_f_t(v) has an
interior minimum. Its derivative is zero. By (7) the two bulk fluxes are
equal, which implies C. This proves Theorem 1.

There is a precise posterior form of the remaining inequality. For
u=law(U)*gamma_t, Gaussian differentiation gives

    Delta log u(x) = -3/t + tr Cov(U | U+sqrt(t)Z=x)/t^2.

At a regular level, the divergence theorem also gives
J_u=-a integral_{u>a} Delta log u. Both bulk integrals are continuous
in a, so this identity extends to every positive level below the peak.
Thus, with |{u>a}|=v,

    J_u = 3av/t - (a/t^2) K_u,
    K_u = integral_{u>a} tr Cov(U | U+sqrt(t)Z=x) dx.       (21)

At an ordered contact, a and v are common to both densities. Condition C
is therefore exactly **K_f<=K_g at those contacts**. The covariance
integrals use Lebesgue measure on two different superlevel sets, not
density-weighted whole-space MMSE. No pointwise posterior-covariance
ordering is assumed, and the direction in (21) must not be reversed.

Some controls clarify what has and has not changed:

* If xi is a point and F(x)=cx, then f_t=gamma_{epsilon+t} and
  g_t=gamma_{c^2 epsilon+t}. Their profiles are strictly ordered. For
  gamma_q, formula (1) gives J=3av/q, checking the heat normalization.
* A constant target is excluded in Section 5 because it cannot fail;
  its dilation derivative is zero, so it must not enter the transversality
  argument as a nonpoint law.
* At c=1 the tail parameter eta vanishes and strict initial order may
  disappear. The proof uses strictification of an actual failure and
  does not silently apply these bounds to an isometry.
* The original six-atom coefficient reversal does not refute C: its
  profiles have a positive gap in the region where the coefficients
  reverse. Ordering diffusion coefficients everywhere remains unnecessary.
* The regularized input is unbounded, its image may be singular before
  adding gamma_t, and the volume cutoffs depend on the particular data.
  There is no uniform atom count, contact time, volume, or support bound.

The remaining research task is now the specific inequality (3), with
global profile order and equal level volumes and masses as hypotheses.
At a regular contact it is an inequality between two boundary fluxes;
at a critical contact (1) is the exact continuous replacement. The
reduction supplies no sign for those fluxes. It complements the endpoint
coupling and stability criteria rather than establishing their missing
global comparison.
