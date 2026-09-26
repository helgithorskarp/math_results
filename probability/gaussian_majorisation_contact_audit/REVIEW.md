# Functional-lane review of the Gaussian first-contact equivalence

26 September 2026. **Verdict: the reviewed argument establishes the stated
reduction. No proof gap requiring a correction was found.** This is a
second-lane analytic review of Theorem 1 in
[CONTACT_REDUCTION.md](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md),
at the revision and hash recorded in [INPUTS.json](INPUTS.json). It does not
prove its remaining contact inequality, produce a Gaussian contact, or
resolve the unrestricted R3 conjecture.

The review checks the proof rather than replaying its finite controls.
In particular, it rederives the sensitive posterior identities, the two
volume-end bounds, and the scalar-envelope transversality step. Section 6
below supplies an elementary justification of the critical-image fact used
in that last step. No formal verification or external human peer review is
claimed. The reviewer is the functional/stability lane and authored one
cited strict-homothety precursor; this is not independence from the entire
dependency tree. The reviewed contact reduction was authored by the
separate evolution lane.

## 1. The exact claim being accepted

Let gamma_t have covariance t I3. Choose a finite probability law xi,
epsilon>0 and a globally c-Lipschitz map F:R3->R3, c<1. Set

\[
 U\sim\rho=\xi*\gamma_\epsilon,\quad Y=F(U),\quad
 f_t=\rho*\gamma_t,\quad g_t=\mathcal L(Y)*\gamma_t.
\]

For a positive Gaussian convolution u, let

\[
 L_u(v)=\sup_{|E|=v}\int_Eu,\quad
 |\{u>a_u(v)\}|=v,\quad
 J_u(v)=-\int_{\{u>a_u(v)\}}\Delta u.
\]

The full bounded-law contraction conjecture is equivalent to the following
condition: at every positive time and positive finite volume where
L_g(w)>=L_f(w) for **all** w>0 and L_g(v)=L_f(v), one has J_f(v)>=J_g(v).
The source proves the stronger contrapositive: any bounded strict failure
can be changed into an auxiliary pair of the displayed form with an ordered
contact and J_f<J_g. Earlier positive times have strict order at every
positive finite volume. At the contact a_f(v)=a_g(v).

The target F must be applied **after** the input is Gaussian-regularized.
Its image may be singular before the final convolution. The auxiliary
input is unbounded; neither this construction nor its contact is claimed
to be a bounded finite mixture of centers. The reduction justifies both
directions between this auxiliary class and the original bounded problem.

The following obligations were checked independently of the source's
computer controls.

| Obligation | Review outcome |
|---|---|
| Differentiation through critical density levels | Valid by null level sets and the unique-threshold envelope; no inverse-level derivative is required. |
| Strict target dilation for the Gaussian-tailed law | Valid; posterior moments are finite and the covariance trace is strictly positive for a nonpoint target. |
| Large volumes, uniformly down to time zero | Valid by the source Gaussian component and strict global Lipschitz constant. |
| Small volumes, uniformly down to time zero | Valid by compact images initially and the posterior peak bound on later compact time intervals. |
| Failure-preserving finite approximation and regularization | Valid with the displayed L1 budget; global extension precedes input smoothing. |
| Transverse first contact, including multiple minimizing volumes | Valid through a Lipschitz scalar envelope and a one-dimensional exceptional-value argument. |
| Converse and posterior form of the remaining sign | Valid by truncation and bulk continuity; the unweighted covariance direction is K_f<=K_g. |

## 2. Critical levels do not obstruct the first derivatives

For the families in Section 1 and compact intervals of positive time and
dilation, Gaussian convolution is positive, analytic and vanishes at
infinity. Positive level sets are null: a nonconstant real analytic function
cannot have a positive-measure level set. The density cannot be constant
because it is positive and integrable. Superlevel sets of positive level
are bounded, uniformly on compact parameter families when the level is
bounded away from zero. Uniform tightness of the center laws and Gaussian
kernel bounds suffice for this assertion.

The Gaussian-tailed U and Lipschitz Y have all polynomial moments.
Differentiating Gaussian kernels therefore gives parameter derivatives
continuous in L1 and locally uniformly. For
H(p,a)=integral(u_p-a)_+, a>0, the hinge's L1 Lipschitz property and null
level sets yield

\[
 H_a=-|\{u_p>a\}|,\qquad
 H_p=\int_{\{u_p>a\}}\partial_pu_p.
\]

These derivatives are continuous. One rigorous way to obtain H_p is to
replace the parameter increment by its fixed L1 derivative; the resulting
error is o of the parameter increment, and the fixed-direction hinge
derivative follows by dominated convergence. This avoids assuming that
the hinge is Frechet differentiable on all of L1.

The level-volume function is continuous and strictly decreasing from
infinity to zero. For strictness, any nonempty intermediate range of the
continuous density has a nonempty open inverse image. Hence its inverse
a(p,v) is continuous. In the identity

\[
 L(p,v)=\min_{a>0}[H(p,a)+av],
\]

the minimizer is unique. Comparing old and new minimizers bounds each
difference quotient between expressions with converging thresholds. Thus

\[
 L_v=a(p,v),\qquad L_p=\int_{\{u_p>a(p,v)\}}\partial_pu_p,
 \qquad \partial_tL=-J/2.                              \tag{R1}
\]

This proves exactly the C1 regularity the source uses. It does not assert
that a(p,v) is differentiable, that the inverse level derivative stays
finite, or that the second-order profile equation works at critical levels.
The bulk definition of J, with L1 continuity and null levels, is continuous
through those levels.

## 3. Posterior dilation and the strict peak bound

Write u_(t,lambda)=law(lambda Y)*gamma_t and m(x)=E[Y|lambda Y+sqrt(t)Z=x].
Gaussian differentiation gives

\[
 \partial_\lambda u=-\operatorname{div}(u m),\qquad
 \operatorname{div}m=\frac1{t\lambda}
          \operatorname{tr}\operatorname{Cov}(\lambda Y\mid x).
\]

At a regular level u=a, integrate the continuity equation over {u>a}.
The boundary density is a, so (R1) yields

\[
 \partial_\lambda L_u(v)
 =-\frac a{t\lambda}\int_{\{u>a\}}
              \operatorname{tr}\operatorname{Cov}(\lambda Y\mid x)\,dx.
                                                               \tag{R2}
\]

Approximate any positive critical level by regular values. Its superlevel
sets stay in one bounded region, the denominator u stays positive there,
and posterior moments and derivatives are continuous. Dominated convergence
extends (R2) to the critical level. Gaussian likelihoods are strictly
positive on the underlying law. Thus a posterior has zero covariance trace
only if Y is a point mass. Otherwise (R2) is strictly negative at every
positive finite volume.

This justifies the extension of the cited bounded-law homothety formula
to the unbounded auxiliary law actually used. On a compact positive
time/dilation/volume box, continuity makes the negative derivative bounded
away from zero. There is no lower-covariance assumption on the original law
and no inverse covariance matrix.

The peak argument also checks directly. At a source mode z of f_t, its
posterior P_z satisfies E_(P_z) U=z. Take m=E_(P_z) F(U). The Gaussian
likelihood ratio and Jensen give

\[
 \log\frac{g_t(m)}{f_t(z)}
 \ge\frac{\operatorname{Var}_{P_z}(U)
              -\operatorname{Var}_{P_z}(F(U))}{2t}
 \ge\frac{1-c^2}{2t}\operatorname{Var}_{P_z}(U)>0.       \tag{R3}
\]

Here Var means the trace, and the second inequality follows by using two
independent posterior samples. All moments involved are finite; the
posterior of the everywhere-positive rho is nonpoint. Since max g_t>=g_t(m),
this is precisely the previously published posterior peak estimate in the
case needed by the contact proof. It is not a new peak theorem.

Peak values vary continuously in positive time and target dilation because
the densities vary uniformly. Their strict difference has a positive
minimum on each compact parameter box. Uniform Gaussian gradient bounds
then give a ball around a target mode where its density exceeds the source
peak. Taking subsets of that ball proves the asserted uniform small-volume
comparison away from time zero.

## 4. Both volume boundaries really are uniform in time and dilation

For the initial boundary, let L_0=L_rho and m_0=max rho. A c-Lipschitz map
reduces the volume of a compact set by at least the factor c^3, so
L_(F#rho)(v)>=L_0(v/c^3)>L_0(v). Use a **closed** top set of rho when a
compact optimizer is needed; it has the same volume and mass as the open
top set because the intervening level is null. This is a clarification of
the source's compact-set wording, not a change in its hypothesis.

If v<u<v/c^3, the image A of a compact source top set of volume u has
|A|<v. A sufficiently small neighborhood A^h still has volume below v.
After convolution, its mass is at least L_0(u) Pr{|sqrt(t)Z|<h}, which
exceeds L_0(v) for small t. Since convolution cannot increase L_f, the
strict comparison persists. For a compact positive dilation interval,
|(lambda A)^h|=lambda^3|A^(h/lambda)| supplies a uniform h using the
maximal Lipschitz constant less than one. A finite cover gives uniformity
over compact positive volume intervals.

To include volumes tending to zero, choose c^3<q<1 and u small enough
that L_0(u)>m_0 q u. The same argument at v_0=q u gives L_g(v_0)>m_0v_0
uniformly for small t. Concavity of L_g then yields L_g(v)>m_0v>=L_f(v)
for every 0<v<=v_0. Combine this with (R3) on later compact time intervals.

For the opposite boundary, suppose |X|<=R, rho=law(X+sqrt(epsilon)Z),
F(0)=0 and 0<c<1. Put v=4 pi r^3/3 and fix a horizon S. Averaging the
Gaussian maximal mass in a set of volume v gives

\[
 1-L_f(t,v)\ge Q_3(r/\sqrt{\epsilon+t}).
\]

The pointwise estimate

\[
 |F(X+\sqrt\epsilon Z)+\sqrt t Z'|
 \le cR+\sqrt{c^2\epsilon+t}\sqrt{|Z|^2+|Z'|^2}
\]

and a six-dimensional Gaussian Chernoff bound give

\[
 1-L_g(t,v)\le(1-2\theta)^{-3}
      \exp[-\theta(r-cR)^2/(c^2\epsilon+t)]
\]

for r>=cR and 0<theta<1/2. This remains valid at t=0 for a singular
pushforward. The source's constants can be verified without its polynomial
computer check. Put

\[
 \eta=\frac{\epsilon(1-c^2)}{2(\epsilon+S)},\quad
 \theta=(1-\eta)/2,\quad
 A=\frac\eta{2(c^2\epsilon+S)},\quad
 B=\frac{(1-\eta)R}{c\epsilon}.
\]

For 0<=t<=S, (c^2 epsilon+t)/(epsilon+t)<=1-2 eta, so directly

\[
 \frac\theta{c^2\epsilon+t}-\frac1{2(\epsilon+t)}
 \ge\frac\eta{2(c^2\epsilon+t)}\ge A.
\]

Expansion of the square therefore bounds the exponent difference below
by Ar^2-Br. For

\[
 r\ge\max\left\{cR,\frac{2B}{A},
     \sqrt{\frac{2[3\log(1/\eta)+1]}A},
     \sqrt{\frac{\pi(\epsilon+S)}2}\right\},
\]

this is at least 3 log(1/eta)+1. The radial tail inequality
Q_3(z)>=sqrt(2/pi) z exp(-z^2/2) has prefactor at least one here.
Consequently

\[
 1-L_g(t,v)\le e^{-1}[1-L_f(t,v)]<1-L_f(t,v).            \tag{R4}
\]

Choosing c as an upper bound for the whole dilation interval makes (R4)
uniform in that interval. The zero-Lipschitz map can also be bounded by
any positive c<1; it is later excluded as a possible failing target.
Thus division by c creates no missing case.

The combination of the initial, small-volume and large-volume arguments
gives the compact time-volume box needed by the source. Its constants
depend on the particular regularized input and its strict Lipschitz
reserve. They are not uniform as epsilon tends to zero or c tends to one.
The known atomic initial layer and relative-tail obstruction are untouched.

## 5. A bounded strict failure survives the required normalization

Finite approximation selects actual input sites and their mapped images;
it preserves the contraction constraints. Multiplying the finite targets
by a factor just below one preserves a strict negative hinge and makes
the finite map strictly contracting. Kirszbraun's theorem supplies a
globally c-Lipschitz extension. Crucially, this extension is taken before
Gaussian input regularization.

For the resulting finite law X and U=X+sqrt(epsilon)Z, the Gaussian
translation bound gives the two-endpoint L1 error at variance S as at most

\[
 \sqrt{\frac2{\pi S}}(1+c)\sqrt\epsilon\,\mathbb E|Z|
 =\frac{4(1+c)\sqrt\epsilon}{\pi\sqrt S}.               \tag{R5}
\]

A negative hinge -d is therefore below -d/2 after regularization whenever
epsilon<pi^2 S d^2/[64(1+c)^2]. Each hinge is 1-Lipschitz in density L1,
so no threshold approximation is hidden in this estimate.

The target cannot be a point: a point target gives gamma_S, while f_S is
a mixture of translates of gamma_(epsilon+S), strictly less concentrated
than gamma_S at every finite positive volume. Thus (R2) applies with a
strict derivative to the target used in the crossing argument.

Translate F so F(0)=0 and choose a compact dilation interval I about one,
with lambda_min>0 and lambda_max c<1, small enough that the same hinge
is still negative at S throughout I. L1 continuity follows from E|Y|<infinity.
At the source top-set volume v corresponding to that hinge threshold a,

\[
 L_g(v)-L_f(v)\le[H_g(a)+av]-[H_f(a)+av]<0.
\]

Thus all dilations have a concentration failure at S. The uniform boundary
arguments in Section 4 give a common compact volume interval V and an
initial positive time t_0<S on which all profiles are strictly ordered.

## 6. The scalar-envelope step is valid without a smooth Sard assumption

This is the delicate quantifier in the argument. On the compact box put
W(t,lambda,v)=L_(lambda Y*gamma_t)(v)-L_f_t(v). The notation means the
law of lambda Y convolved with gamma_t. We have W in C1 and W_lambda<=-kappa<0.
Let b(t,v) be its zero as a function of lambda, clipped to the endpoints
of I when the zero is outside I. It is continuous, and

\[
 |b(t,v)-b(t',v)|\le\frac{\|W_t\|_\infty}{\kappa}|t-t'|.
\]

The bound follows by monotonicity and the mean-value inequality even in
the clipped cases. Hence b_*(t)=min_(v in V)b(t,v) is Lipschitz, starts at
lambda_max and ends at lambda_min.

For a Lipschitz scalar function h on an interval, the image of its
nondifferentiability set is null: differentiability holds almost everywhere
and a Lipschitz map sends null subsets of the line to null subsets. Also
the image of {h'=0} is null. Here is an elementary check of the latter
fact, avoiding an assumption that h is C1 or that the minimizer is unique.

Fix alpha>0. Let E_m consist of x in the interval such that
|h(y)-h(x)|<=alpha|y-x| whenever |y-x|<=1/m and y is in the interval.
These are closed increasing sets; closedness follows by passing to limits,
first for strict |y-x|<1/m and then by continuity at equality. Every
interior point with h'=0 belongs to some E_m. Partition the interval into
finitely many pieces of length at most 1/m. On any piece meeting E_m,
choose x in that intersection; its image portion lies in an interval of
length at most twice alpha times the piece length. Thus

\[
 |h(E_m)|\le2\alpha\,|\text{time interval}|.
\]

The images h(E_m) are compact and increasing. The same bound holds for
their union. Letting alpha decrease to zero proves the null critical image;
the two time endpoints do not matter. This is the one-dimensional fact
used by the source's area-formula argument, not a new Sard theorem.

Choose lambda strictly between the endpoints of I outside both exceptional
images for b_*. At the first t_* with b_*(t_*)<=lambda, continuity gives
b_*(t_*)=lambda. Earlier values are larger; the derivative exists and is
nonzero by the choice of lambda, so b_*'(t_*)<0.

Choose a minimizing v_*. Since its clipped value is interior to I,
b(t,v_*) is a genuine C1 zero near t_*. The difference b(t,v_*)-b_*(t)
is nonnegative and vanishes at t_*, so their derivatives there agree.
Differentiating the zero equation yields

\[
 W_t(t_*,\lambda,v_*)
 =-W_\lambda(t_*,\lambda,v_*)b_*'(t_*)<0.               \tag{R6}
\]

Every volume in V has W>=0 then; all volumes outside V have strict order
by Section 4. Earlier positive times have strict order. The contact lies
in the interior of V because the boundary volumes remain strictly ordered.
Therefore W_v=0 and (R1) gives equal density levels. Also (R1) changes
(R6) into J_f<J_g. The map lambda F remains globally strictly contracting.

This verifies the needed strict crossing even if the original failure
crossed a flat zero, several volumes minimize simultaneously, or the
contact density levels are critical. Those possibilities were not excluded
by assuming generic smoothness of the profiles or their volume derivatives.

## 7. Converse, remaining covariance sign, and use by other lanes

If the bounded-law conjecture holds, truncate and renormalize rho on balls.
The input and its pushforward converge in total variation. Their Gaussian
convolutions converge in L1, and their concentration profiles converge
uniformly in volume. Thus the conjecture applies to the auxiliary unbounded
pair at all positive times. At a contact the C1 time profile has a local
minimum zero, so W_t=0 and J_f=J_g. This proves the converse.

Finally, Gaussian differentiation gives

\[
 \Delta\log u=-3/t+
       \operatorname{tr}\operatorname{Cov}(U\mid U+\sqrt tZ=x)/t^2.
\]

At a regular level u=a, the boundary relation
partial_n log u=(partial_n u)/a implies
J_u=-a integral_(u>a) Delta log u. The same bounded-region/null-level
argument as in Section 3 extends this identity to critical levels. Hence

\[
 J_u=\frac{3av}{t}-\frac a{t^2}K_u,\qquad
 K_u=\int_{\{u>a\}}
       \operatorname{tr}\operatorname{Cov}(U\mid U+\sqrt tZ=x)\,dx.
                                                               \tag{R7}
\]

The levels and volumes agree at a globally ordered contact. The outstanding
sign is therefore exactly **K_f<=K_g**. These are Lebesgue integrals over
two different superlevel sets. Whole-space density-weighted MMSE, entropy
monotonicity and a finite positive moment list do not state this inequality.
This review supplies no new implication from those quantities to (R7).

For finite-atomic and stability work, the useful trust boundary is precise:
the reduction establishes the existence of a transverse contact if a
failure exists, but gives no uniform atom count, extension algorithm,
contact time, volume, level or covariance margin. Its auxiliary laws are
unbounded, so the [support-uniform moment bound](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md)
cannot be applied directly with a finite support radius. Truncation with an
absolute error preserves a strict failure; it does not by itself certify
an exact ordered contact or its flux. The original bounded-law exact
certificate and the contact condition remain complementary obligations.

The first-contact reduction is accepted at the stated scope. The remaining
research target is its globally ordered-contact sign, with critical levels
included, or another route to the same unrestricted conjecture. This audit
adds no positive class or Kneser--Poulsen consequence and changes none of
the source proof's claims or files.
