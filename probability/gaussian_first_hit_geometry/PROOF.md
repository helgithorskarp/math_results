# Actual equality contacts satisfy the Brownian witness event bounds

Complete author argument, 27 September 2026; independent review pending.
The full dimension-three Gaussian-convolution majorisation question remains
open. This is a limitation of an event-exclusion route, not a counterexample
to majorisation or to the prior-stationary contact reduction.

## 1. Exact statement and the hypotheses it does not satisfy

Let gamma_q be the centred Gaussian density with covariance q I_3. Put
delta=1/8, x_0=0, x_1=delta e_1, x_2=delta e_2, x_3=delta e_3, and

    rho_p = sum_(i=0)^3 p_i gamma_1(.-x_i),  p in Delta_4,
    F(x) = -x,       f_(t,p)=rho_p*gamma_t,
    g_(t,p)=(F#rho_p)*gamma_t.

These are Gaussian-regularized finite-site inputs of the contact route;
the underlying four-site measure is bounded and has full affine span.
The smoothed rho_p itself is unbounded in support. For every prior p and t>0,

    g_(t,p)(y)=f_(t,p)(-y).

Consequently every profile and hinge comparison is equality, including
all-prior ordering and prior/threshold stationarity. At p_i=1/4,t=1,
write f=f_(1,p), g=g_(1,p), and set

    a=(4 pi)^(-3/2) exp(-1/4),
    A_f={x: (1/4) sum_i exp(-|x-x_i|^2/4)>exp(-1/4)},
    A_g=-A_f.                                               (1)

These are the true top sets. Every active component has exactly equal
acceptance probabilities in the two experiments. The common-volume heat
fluxes J_f=-integral_A_f Delta f and J_g=-integral_A_g Delta g agree.

Let I be uniform on {0,1,2,3}, independent of independent standard Brownian
motions Z,W in R3. Define the actual common-noise terminal difference

    D_i(z,w)=1_A_g(-x_i-z+w)-1_A_f(x_i+z+w),
    M_s=E[D_I(Z_1,W_1)|I,(Z_r,W_r)_(r<=s)],
    N_s=|W_s|^2-3s,
    tau_theta=inf{s: |M_s|>=theta}.

The martingale starts at zero conditional on each label. For every
0<kappa<=1/256, put s_k=1-kappa^2/48 and theta_k=kappa/16. Then

    Pr{tau_theta_k<=s_k} >= kappa^2/96,                       (2)
    Pr{N_s_k M_s_k<=-kappa/4,
                         |(Z_s_k,W_s_k)|<2} >= kappa^2/96. (3)

In fact a fixed positive-volume box of states has N_s_k M_s_k<-1.
Its negative sign therefore persists on an open neighborhood. In contrast,

    E[N_s M_s]=0   for every 0<=s<=1,                        (4)
    J_f-J_g=0.

Here kappa is a parameter for testing the event bounds, not an adverse
flux margin: there is no positive adverse margin in this example.

An equally valid orthogonal noise coupling for these same densities gives
M_s identically zero, and therefore no first hit at a positive threshold.

The example has Lip(F)=1 and equality at all earlier times. It DOES NOT
meet the strict c<1 and transversely adverse first-contact hypotheses of
the reduction. In particular it cannot disprove that reduction. It proves
that its quantitative event conclusions, even with genuine top sets,
component balance and all-prior equality, do not by themselves recognize
an adverse contact. They can occur without the negative expected covariance
that was used to derive them. No impossibility claim is made for a proof
that also uses strict first-contact information quantitatively.

## 2. The top sets and the balanced martingale

The sites all have norm at most delta. At time one the component densities
are gamma_2(.-x_i). If |y|<1-delta then every |y-x_i|<1, so every
component exceeds a. If |y|>=1+delta then every |y-x_i|>=1, so no
component exceeds a. Thus, for every prior, each of its two top sets obeys

    B(0,7/8) subset A_f,A_g subset B(0,9/8).                (5)

The boundaries are regular. Indeed grad f(y)/f(y)=-(y-m(y))/2, where
m(y) is a convex combination of the sites and hence |m(y)|<=delta.
On f=a, |y|>=1-delta, so |grad f(y)|/f(y)>=(1-2delta)/2>0.
Reflection gives the same assertion for g. This also proves compactness
and smoothness of the positive level boundaries.

For each i the target component is the reflection of the source component,
and A_g=-A_f. Thus their acceptance probabilities agree and E[D|I=i]=0.
This argument holds for every prior, including boundary priors. The entire
prior/threshold hinge difference is identically zero.

For s<1 define

    h_i(s,z,w)=E[D_i(z+Z',w+W')],
    Z',W' independent with law gamma_(1-s).

Then M_s=h_I(s,Z_s,W_s). Gaussian convolution makes h_i smooth. Brownian
conditional expectations give a bounded continuous version of M up to
the terminal time, with M_1=D almost surely. Terminal boundary events
have probability zero. These are the same definitions and conventions as
the prior-stationary witness source; no surrogate top set is used.

## 3. A box exceeding the prescribed event probabilities

Let

    C=[3/4,1] x [-1/8,1/8] x [-1/8,1/8],
    E={Z_s in C, W_s in C}.

For z,w in C,

    |w|^2<=33/32,   |(z,w)|^2<=33/16<4,
    |w-z|^2<=3/16<1/4,   (z+w)_1>=3/2.

For every label this gives

    |-x_i-z+w|<5/8,       |x_i+z+w|>=11/8.                 (6)

At s=s_k, the remaining noise in either output has law gamma_q with
q=2(1-s_k)=kappa^2/24. If its norm is below 1/4, (5)--(6) place the
target output in A_g and the source output outside A_f. Markov's inequality
using E|G_q|^2=3q yields

    Pr{|G_q|>=1/4}<=48q=2 kappa^2,
    h_i(s_k,z,w)>=1-4 kappa^2.                             (7)

Equation (7) uses only the two marginal probabilities; it does not require
any assertion about independence between the two outputs.
Since s_k>=47/48,

    N_s_k <=33/32-3(47/48)=-61/32

on E. Equations (7) and kappa<=1/256 give N_s_k M_s_k<-1 and
M_s_k>theta_k there. Continuity from M_0=0 forces a first hit by s_k.

The six-dimensional Gaussian density of (Z_s,W_s) on C x C is at least

    (2 pi)^(-3) exp[-33/(32s)]
                  >= (2 pi)^(-3) exp[-99/94] > 1/1372.     (8)

Here s>=47/48, 2pi<7 and exp(99/94)<4. The last exponential inequality
also follows from the exact positive-series upper bound in the checker;
no floating-point integral is used. The six-dimensional volume of C x C
is 1/4096. Hence

    Pr(E)>1/5619712 > (1/256)^2/96 >= kappa^2/96.           (9)

This proves (2)--(3). The state bound 2 is smaller than the prior witness
radius R_k=sqrt(4 log(1536/kappa^2)). Thus its bounded-region condition
also cannot distinguish this example. Smoothness and the strict margin
give a robust adverse state, rather than an isolated zero or a terminal
boundary effect. The standard Gaussian gradient estimate in the prior
source also applies verbatim if its particular radius r_k is desired.

## 4. Exact cancellation and dependence on the noise coupling

Because A_g=-A_f, the same terminal difference can be written as

    D_i(z,w)=1_A_f(x_i+z-w)-1_A_f(x_i+z+w).

The Brownian law is invariant under W -> -W. This transformation changes
the signs of D and M, preserves N, and does not change the label. Hence
(4) holds even conditional on each label.

The transformation also preserves tau_theta, so the positive and negative
values of N_(tau_theta wedge s) M_(tau_theta wedge s) are paired exactly.
The expectations exist: the stopped M is bounded, and stopped Brownian
squared norm has finite expectation. The unfavorable state box is balanced
by its reflected favorable counterpart. There is no adverse expected flux.

Now change only the target noise to -W. Its marginal is still a standard
Brownian motion independent of I,Z, and its squared norm is unchanged.
The terminal difference becomes

    Dtilde_i(z,w)=1_A_g(-x_i-z-w)-1_A_f(x_i+z+w)=0.         (10)

Thus its conditional-expectation martingale is zero.
Both couplings represent the same densities and the same Gaussian
noise-energy formula for J_f-J_g. They differ in first-hit geometry.

This cancellation is not restricted to the four-site law.
For any input law and any isometry F(x)=Qx+b, Gaussian convolution gives
A_g=Q A_f+b at corresponding levels. Coupling the target noise as QW
then makes the two membership indicators equal pointwise. Since
|QW|=|W|, the flux formula remains valid. This observation does not
construct such an aligned coupling for a general nonlinear contraction.

## 5. Consequence for the research route

The prior witness result goes from a negative expected covariance to
first-hit and negative-state probability bounds. Reversing that step is
invalid even for the actual Gaussian top sets and all-prior equality
contacts exhibited here. Searching for those events or excluding their
local geometry without retaining signed cancellation cannot decide the
unrestricted question. An orthogonal noise choice can create or remove
the entire event geometry at an isometric equality case.

The strict first-contact requirement remains an essential, unused
distinction. This proof neither constructs one nor controls its signed
covariance. It closes the event-only branch of this lane, while preserving
the necessary-contact theorem and the accepted local near-isometry work.
There is no new sufficient comparison criterion, new Gaussian map class,
or Kneser--Poulsen conclusion.
