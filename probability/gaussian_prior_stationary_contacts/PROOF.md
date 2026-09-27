# Prior-stationary contacts have detectable Brownian witnesses

Complete author proof, 27 September 2026; independent review is pending.
The unrestricted three-dimensional Gaussian-majorisation question remains
open. This result strengthens the accepted first-contact reduction: one
may demand exact balance for each active input component, stability under
all changes of the prior, and a quantitative adverse Brownian event before
the terminal time. It neither constructs a contraction violating
majorisation nor proves the missing contact-flux sign.

## 1. Statement

Write gamma_q for N(0,q I_3), H_u(a)=integral(u-a)_+, and
L_u(v)=sup_{|E|=v} integral_E u. At a Gaussian convolution define

    J_u(v) = -integral_{u>a_u(v)} Delta u,
    |{u>a_u(v)}|=v.                                           (1)

This bulk definition includes critical levels. Our analytic input is the
accepted [global contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md)
and its strictification, volume-end control and dilation argument. Section
2 proves the additional uniformity needed here; a fixed-prior contact alone
does not imply our conclusion.

**Theorem 1 (prior-stationary reduction).** Any strict bounded-law failure
of Gaussian majorisation in R3 gives finite sites x_1,...,x_N, epsilon>0,
a global nonconstant c-Lipschitz map F with c<1, and t_*>0 such that, for
every w in the entire closed probability simplex Delta_N, putting

    rho_w = sum_i w_i gamma_epsilon(.-x_i),
    f_(t,w) = rho_w * gamma_t,
    g_(t,w) = (F#rho_w) * gamma_t,                            (2)

one has L_g(t,w)(v)>L_f(t,w)(v) for 0<t<t_* and every finite v>0.
At t=t_* all these comparisons are nonstrictly ordered. There are w_*
and v_* at which equality holds and

    J_f(v_*)-J_g(v_*) < 0.                                  (3)

Hereafter f=f_(t_*,w_*), g=g_(t_*,w_*). Their top sets
A_f={f>a}, A_g={g>a} have a common positive threshold a, equal volume
v_* and equal retained mass. Define the fixed component densities

    f_i = gamma_(epsilon+t_*)(.-x_i),
    g_i = (F#gamma_epsilon(.-x_i))*gamma_(t_*).

Then

    integral_A_g g_i = integral_A_f f_i       if w_*,i>0,
    integral_A_g g_i >= integral_A_f f_i      if w_*,i=0.      (4)

Moreover Psi(w,b)=H_(sum w_i g_i)(b)-H_(sum w_i f_i)(b) is
nonnegative for every w in Delta_N and b>=0, and Psi(w_*,a)=0.
Thus for any finitely supported random pair (W,B) in Delta_N x [0,infinity)
with mean (w_*,a),

    E H_(sum W_i g_i)(B) - H_g(a)
       >= E H_(sum W_i f_i)(B) - H_f(a) >= 0.                (5)

If a is a regular level of both densities, every u supported on the
active labels with sum u_i=0, and every beta in R, satisfy

    integral_{g=a} (sum u_i g_i-beta)^2/|grad g| dS
       >= integral_{f=a} (sum u_i f_i-beta)^2/|grad f| dS.     (6)

No assertion of regularity is needed for (1)--(5).

**Theorem 2 (quantitative stochastic witness).** At the contact of Theorem
1, write t=t_* and choose any 0<kappa<=1 with
t(J_f-J_g)<=-kappa. There is the explicit bounded martingale M below,
starting at zero conditional on every active label, such that, with

    s_k = 1-kappa^2/48,       theta_k = kappa/16,
    N_s = |W_s|^2-3s,
    tau_k = inf{0<=s<=1: |M_s|>=theta_k},

with the infimum of the empty set defined as infinity, one has

    E[N_(s_k) M_(s_k)] <= -kappa/2,
    Pr{tau_k<=s_k} >= kappa^2/96,                            (7)
    Pr{N_(s_k) M_(s_k)<=-kappa/4} >= kappa^2/96.             (8)

The event in (8) can also be restricted to
|(Z_(s_k),W_(s_k))|<=R_k, losing at most half the stated probability, where

    R_k = sqrt(4 log(1536/kappa^2)).                         (9)

In particular, some active label has a robust adverse state in a bounded
six-dimensional region at this specified preterminal time. Section 5 gives
an explicit radius of a neighborhood on which its sign persists.

The same F acts on the smoothed input throughout (2). In particular
F#(xi*gamma_epsilon) is not replaced by (F#xi)*gamma_epsilon. The Brownian
construction below retains the actual two top sets, with no replacement by
componentwise optimal sets or by pairwise terms.

## 2. Selecting the contact over a whole prior simplex

The existing reduction, Sections 2--6, first transfers a strict bounded-law
failure to finite sites with prior w_0, positive input smoothing epsilon,
and a nonconstant global strict contraction F. A constant target cannot
fail. Translate the target to arrange F(0)=0. There is a final heat time
S and a compact interval I=[lambda_-,lambda_+] of positive dilations
such that lambda_+ Lip(F)<1 and the failure at w_0 survives throughout I.
For now replace F in g by lambda F and set

    D(t,lambda,w,v)=L_g(t,lambda,w)(v)-L_f(t,w)(v).           (10)

We need bounds uniform also over w in the *closed* simplex, including its
vertices. Put R=max_i|x_i| and c=lambda_+ Lip(F). The large-volume
estimate of the existing reduction uses only R, c, epsilon and S. Its
strict comparison therefore holds uniformly over w and lambda for all
v>=v_+ and 0<=t<=S, for some finite v_+.

For completeness, the other compactness arguments remain uniform as
follows. Every rho_w is strictly positive, analytic and vanishes at
infinity, including at boundary priors. The family varies continuously
in L1 and uniformly. Its peaks are positive and continuous in w.
At time zero the volume contraction inequality gives

    L_(lambda F)#rho_w(v) >= L_rho_w(v/c^3)>L_rho_w(v).       (11)

For a fixed (w,lambda,v), choose v<u<v/c^3 and a compact optimal source
set E of volume u. Its image lambda F(E) has volume less than v.
A small open neighborhood of this image still has volume less than v.
Source mass on E, source profiles, and their strict gap vary continuously
with the prior. For nearby lambda, the image is contained in a slightly
larger neighborhood of the same compact image. Brownian noise lies in
that neighborhood with probability tending to one as t decreases to zero.
Consequently the strict comparison persists uniformly near the chosen
(w,lambda,v). A finite cover handles any compact interval of positive v.

The interval next to zero volume requires a separate argument. Fix
c^3<k<1. At each prior w choose a small u>0 and a compact optimal source
set E of volume u with rho_w(E)>k u max rho_w. The image volume is at
most c^3u<ku. The same compact-image argument gives, for small t,

    L_g(t,lambda,w')(ku)>ku max rho_w'

uniformly over w' near w and lambda in I. The strict inequality and
continuity of max rho_w' justify the neighborhood of w. Concavity of
L_g and max f_(t,w')<=max rho_w' extend this comparison to 0<v<=ku.
A finite cover of Delta_N gives a common small volume and small time.
Combine it with the previous compact-volume argument and the large-volume
bound to obtain strict order at all v for 0<t<=t_0, with t_0>0.

On [t_0,S], the strict posterior peak comparison used in the existing
reduction applies at every (t,lambda,w). It is strict since c<1 and
rho_w has a nonpoint posterior with full support. Peaks depend
continuously on these compact parameters, so their gap has a positive
minimum. The uniform spatial continuity of Gaussian convolutions then
gives strict order on a common interval 0<v<=v_-. We may take v_->0
smaller if necessary. A failure is therefore confined to

    t in [t_0,S],  lambda in I,  w in Delta_N,
    v in [v_-,v_+].                                        (12)

The C1 envelope identities from the existing reduction hold continuously
on this box, with weight derivatives understood along faces. Null
positive level sets justify the derivatives without excluding critical
levels. Every rho_w has full support and F is nonconstant; hence
F#rho_w is nonpoint for every w. The strict target-dilation identity
therefore gives D_lambda<0 everywhere in (12), bounded away from zero
by compactness.

For each (t,w,v) invert D=0 as a function of lambda, clipping the inverse
to the endpoints of I if there is no interior zero. Denote it b(t,w,v).
It is continuous and uniformly Lipschitz in t, because D_lambda is
uniformly negative and D_t uniformly bounded. Thus

    b_*(t)=min_{w in Delta_N, v in [v_-,v_+]} b(t,w,v)

is Lipschitz, with b_*(t_0)=lambda_+ and b_*(S)=lambda_-.
Choose an interior lambda outside the image under b_* of the
nondifferentiability set and of {t: b_*'(t)=0}. Both images have measure
zero: use the Lipschitz null-set property and the one-dimensional area
formula. At the first t_* with b_*(t_*)<=lambda, its derivative exists and
is strictly negative. Let (w_*,v_*) attain the minimum there.
The unclipped inverse for these fixed minimizing parameters is C1
in t near t_* and touches b_* from above, so their derivatives agree.
Implicit differentiation gives

    D_t(t_*,lambda,w_*,v_*)=-D_lambda b_*'(t_*)<0.           (13)

Every prior and volume is ordered at t_*, and every prior and volume is
strictly ordered at all earlier positive times. Since v_* is an interior
volume minimum, D_v=0 gives the common density level a. The heat identity
D_t=(J_f-J_g)/2 gives (3). Absorb lambda into F. This establishes the
strengthened selection, including zero weights and critical levels.

## 3. Balance and prior curvature

Profile ordering is equivalent to hinge ordering. At the selected time
it holds for every w, and the common threshold at the touching profiles
gives Psi(w_*,a)=0. Differentiation of the hinge in a prior direction is
valid by dominated convergence, since the positive density level sets
are null. Put

    alpha_i=integral_A_g g_i-integral_A_f f_i.               (14)

Directional minimality along e_i-e_j makes alpha_i constant on the active
labels. The equality of retained masses gives sum_i w_*,i alpha_i=0,
so that constant is zero. Variation from w_* toward an inactive vertex
e_i gives alpha_i>=0. This proves (4). Removing inactive labels preserves
the contact and the conclusions for the remaining simplex.

Each individual hinge is convex jointly in (w,b), since it is an integral
of the positive part of an affine function. Taking expectations of
Psi(W,B)>=0 and using equality at its mean proves the first inequality
in (5); Jensen gives the second. This finite-difference condition is
valid even at critical contact levels.

At a regular level the top boundaries are compact smooth hypersurfaces
with nonvanishing gradient. The second derivative at r=0 of
H_(f+r sum u_i f_i)(a+r beta) is

    integral_{f=a}(sum u_i f_i-beta)^2/|grad f| dS.

This follows by coarea differentiation; regularity persists for the
small perturbations in question. The analogous formula holds for g.
Their difference is nonnegative at a local minimum of Psi, proving (6).
Only active-prior tangent directions are used; extending arbitrary
signed perturbations through zero weights would be invalid.

## 4. The exact probability space and the flux

Let I have distribution w_*, independently of two independent standard
three-dimensional Brownian motions Z_s,W_s, 0<=s<=1. For a fixed active
label i define a bounded Borel function on R3 x R3 by

    D_i(z,w)=1_A_g(F(x_i+sqrt(epsilon)z)+sqrt(t)w)
                       -1_A_f(x_i+sqrt(epsilon)z+sqrt(t)w). (15)

The terminal variable D=D_I(Z_1,W_1) lies in [-1,1]. Equation (4) says
E[D|I=i]=0 for every active label. Sharing W_1 in the two indicators is
only a coupling for evaluating their difference; it imposes no ordering
of the individual events, radii or conditional densities.

Gaussian kernel differentiation gives, with A and B respectively the
source and target indicators in (15),

    J_f=(1/t) E[(3-|W_1|^2) A],
    J_g=(1/t) E[(3-|W_1|^2) B].

Fubini is justified by integrability of the Gaussian Laplacian and the
bounded indicators. No differentiation of F is involved. Hence

    t(J_f-J_g)=E[(|W_1|^2-3)D]=E[|W_1|^2 D].              (16)

In particular an adverse flux has an adverse conditional expectation for
at least one label even though each label is exactly mass-balanced.

Let F_s be the filtration generated by I and both Brownian histories up
to s. The input endpoint Z_1 is not revealed at time zero. Put

    M_s=E[D|F_s]=h_I(s,Z_s,W_s),
    h_i(s,z,w)=P^(6)_(1-s) D_i(z,w),                       (17)

where P^(6)_q is convolution by N(0,q I_6). Then M_0=0, |M_s|<=1,
and M has a continuous version on [0,1] with M_1=D. Gaussian smoothing
makes h_i smooth for s<1, irrespective of the regularity of F or of the
two top boundaries. Ito's formula yields

    dM_s=grad_z h_I . dZ_s + grad_w h_I . dW_s,
    dN_s=2 W_s . dW_s,        N_s=|W_s|^2-3s.

Both martingales are in L2. The resulting covariance identity is

    t(J_f-J_g)=E[N_1 M_1]
              =2 E integral_0^1 W_s . grad_w h_I(s,Z_s,W_s) ds. (18)

For example first stop at r<1 and then pass in L2. The absolute
integrability of the displayed expected integral follows from
Cauchy--Schwarz and the Ito energy bound
E integral_0^1 |grad h_I|^2 ds=E D^2<=1.
These are classical Brownian conditional-expectation identities. The new
content is their application to the *prior-stationary contact* and the
quantitative consequences below, not a new martingale representation.

## 5. A finite-time, bounded-region adverse event

For any 0<s<1, martingale orthogonality gives

    E[N_1 D]-E[N_s M_s]=E[(N_1-N_s)(D-M_s)].                (19)

Direct Gaussian moments give E N_s^2=6s^2 and
E(N_1-N_s)^2=6(1-s^2). Also E(D-M_s)^2<=1. Therefore

    |E[N_1 D]-E[N_s M_s]|<=sqrt(6(1-s^2))
                              <=sqrt(12(1-s)).             (20)

At s=s_k the last expression is kappa/2, proving the first part of (7).
Let p=Pr{tau_k<=s_k}. On its complement |M_(s_k)|<theta_k,
and everywhere |M_(s_k)|<=1. Cauchy--Schwarz gives

    kappa/2 <= |E[N_(s_k) M_(s_k)]|
             <=sqrt(6) s_k (theta_k+sqrt(p)).               (21)

Since sqrt(6)<4, the theta term is at most kappa/4. Thus
p>=kappa^2/(96 s_k^2)>=kappa^2/96, proving the first-hit bound.

To keep the adverse *sign* as well, let V=-N_(s_k) M_(s_k).
Then E V>=kappa/2 and E V^2<=6s_k^2<=6. If
p'=Pr{V>=kappa/4}, splitting the expectation at that event gives

    kappa/2 <= E V <= kappa/4 + sqrt(6p').                  (22)

Hence p'>=kappa^2/96, proving (8). The six-dimensional state has law
N(0,s_k I_6), independently of the label. Markov's inequality gives

    Pr{|(Z_(s_k),W_(s_k))|>R}
       <=8 exp(-R^2/4),                                  (23)

because its exponential squared-norm moment at parameter 1/4 is
(1-s_k/2)^(-3)<=8. For R=R_k in (9), (23) is kappa^2/192.
Intersecting with (8) proves the bounded-region probability claim.

Here is a deterministic robustness consequence. For every i and s<1,
Gaussian differentiation and |D_i|<=1 give the directional bound

    |grad h_i(s,z,w)| <= 1/sqrt(1-s).

At s_k this is less than 7/kappa. On the six-dimensional ball of radius
R_k+1 the function

    Q_i(z,w)=(|w|^2-3s_k)h_i(s_k,z,w)

has Lipschitz constant at most

    L_k=2(R_k+1)+(7/kappa)[(R_k+1)^2+3].                   (24)

Some active i has a point in the radius-R_k ball with Q_i<=-kappa/4.
On the entire ball about that point of radius

    r_k=min{1, kappa/(8L_k)},                              (25)

one consequently has Q_i<=-kappa/8. A finite r_k-net of the radius-R_k
ball must encounter such a negative value. This statement does not
assume an algorithm for evaluating h_i: validated evaluation of the
true contact top sets and of (15) remains a separate obligation.

## 6. Controls, gain and remaining boundary

An exact analytic control checks the orientation of (16)--(20). It is
*not* a contraction/contact example. For independent scalar standard
Gaussian coordinates z,w set

    D=1_{|z|>|w|}-1_{|w|>|z|}.

The two probabilities are 1/2. With A=(z+w)/sqrt(2), B=(z-w)/sqrt(2),
the variables A,B are independent standard Gaussians and D=sign(A B).
It follows that

    E[(|W_1|^2-3)D]=-E|A| E|B|=-2/pi,
    E[N_s M_s]=-(2/pi)s^2.                                (26)

The unused two W coordinates contribute zero. The second formula follows
from E[A_s sign(A_1)]=s sqrt(2/pi) and the corresponding B identity.
Equivalently the martingale is the product
[2 Phi(A_s/sqrt(1-s))-1][2 Phi(B_s/sqrt(1-s))-1]. Thus zero component
mass difference alone does not control the energy covariance; the common
contraction, actual top sets and global prior minimality must be retained.

The new restrictions are substantive but necessary, not sufficient:

* A putative global violation may be sought at a contact that is stable
  under every prior change on its selected support, with all active
  component acceptance differences exactly zero. Cancellations among
  nonzero component mass differences are no longer needed.
* At a prescribed adverse flux margin, the stochastic evidence cannot be
  confined to an arbitrarily thin terminal layer, an arbitrarily rare
  event, or arbitrarily large Brownian states. Equations (7)--(9) and
  (24)--(25) give explicit bounds independent of the support size and F.
* Neither the regular-level matrix inequality (6) nor component balance
  has yet been shown to force the sign E[N_1D]>=0. Excluding the specified
  adverse Brownian events using the contraction and top-set geometry is
  the remaining nonlocal task. There is no lower bound on the hypothetical
  margin kappa, and no constructed adverse contact.

The source includes a small exact checker of Gaussian moment identities,
constant inequalities and the control in (26). It is not a computer proof
of the analytic reduction or of the full conjecture. No numerical search,
unpublished external data, or omitted large certificate enters the proof.
Dependency and novelty boundaries are in [SOURCES.md](SOURCES.md).
