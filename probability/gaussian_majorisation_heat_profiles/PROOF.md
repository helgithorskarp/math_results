# Concentration profiles under heat flow and a strict six-atom obstruction

Complete author proof of the statements below; independent review and
formalization are pending. The full Gaussian-majorisation problem is not
settled. Our heat-time parameter is the Gaussian **variance** s, so the
generator is one half of the Laplacian.

## 1. Exact evolution at regular levels

Let u_s=mu*gamma_s in R^n, where mu is a bounded probability law and
gamma_s has covariance s I. For a positive regular value a, write

\[
 V_s(a)=|\{u_s>a\}|,\quad
 H_s(a)=\int(u_s-a)_+,\quad
 J_s(a)=\int_{\{u_s=a\}}|\nabla u_s|\,dS,
\quad B_s(a)=\int_{\{u_s=a\}}\frac{dS}{|\nabla u_s|}.
\tag{1}
\]

All positive superlevel sets are bounded. On a compact space-time patch
of regular levels the implicit-function theorem, coarea, and smooth
Gaussian derivatives justify the identities

\[
 H_a=-V,\qquad V_a=-B<0,\qquad H_{aa}=B,
 \qquad H_s=-\frac12J.                         \tag{2}
\]

For the last identity differentiate the hinge, use u_s'=Delta u_s/2,
and apply the divergence theorem on {u_s>a}. Its outward unit normal is
-grad u_s/|grad u_s|, giving the minus sign. There is no moving-boundary
term because the hinge vanishes on the boundary.

The concentration profile is

\[
 L_u(s,v)=\sup_{|E|=v}\int_Eu_s
          =\int_0^v u_s^*(w)\,dw .               \tag{3}
\]

At v=V_s(a), it equals H_s(a)+av. The maximizing set is {u_s>a}.
Let a=a(s,v) be the inverse level function on the regular patch. Then

\[
 L_v=a,\qquad L_{vv}=-\frac1B<0,\qquad
 L_s=-\frac12J.
\tag{4}
\]

Consequently the exact coefficient is

\[
 \boxed{\quad L_s=\frac{\kappa_u(s,v)}2 L_{vv},
 \qquad \kappa_u(s,v)=J_s(a(s,v))B_s(a(s,v)).\quad}
\tag{5}
\]

This is an exact equation, not a closed equation for L alone: kappa retains
the geometry and gradient distribution of its level surface. In contrast,
writing the equation directly in the threshold variable gives
H_s=-(J/B)H_aa/2, with the opposite parabolic sign. Applying a forward
maximum principle in the threshold variable would therefore be incorrect.

For probability densities the desired majorisation is exactly
L_f(s,v)<=L_g(s,v) for all v, equivalently H_f(s,a)<=H_g(s,a) for all a.
One can see the equivalence from

\[
 H(a)=\sup_{v\ge0}(L(v)-av),\qquad
 L(v)=\inf_{a\ge0}(H(a)+av).                     \tag{6}
\]

These are standard rearrangement identities, and the scalar concentration
method is classical. They are derived here to fix the coefficient and
comparison signs precisely.

## 2. The comparison equation and the information it needs

For f_s=mu*gamma_s and g_s=nu*gamma_s, set W=L_g-L_f. On a rectangle
of common regular levels,

\[
 \boxed{\quad W_s-\frac{\kappa_g}2W_{vv}
       =F:=\frac{\kappa_g-\kappa_f}2(L_f)_{vv}.\quad}
\tag{7}
\]

Thus kappa_f>=kappa_g would give nonnegative forcing and, with nonnegative
parabolic-boundary values, a direct comparison principle. A contraction
of the labelled centres does **not** imply that coefficient inequality,
as Sections 4--6 show.

For precision, take a closed regular rectangle
[s_0,s_1] x [v_0,v_1], with s_0>0 and 0<v_0<v_1. Assume all relevant levels
remain regular in a neighborhood of the rectangle. The coefficients and
profiles are smooth there, and kappa_g is bounded above and away from zero.
Starting at v in (v_0,v_1), let

\[
 dZ_r=\sqrt{\kappa_g(s_1-r,Z_r)}\,dB_r,
\qquad Z_0=v,
\]

and stop at tau, the earlier of s_1-s_0 and the first exit from (v_0,v_1).
The coefficients may be extended smoothly outside the interval for this
construction; the stopped law does not depend on the extension. Ito's
formula and (7), followed by bounded stopping, give

\[
 W(s_1,v)=\mathbb E W(s_1-\tau,Z_\tau)
       +\mathbb E\int_0^\tau F(s_1-r,Z_r)\,dr .     \tag{8}
\]

This records the actual remaining sign obligation: the boundary term and
the integrated signed forcing, not the forcing at each point separately.
It is a standard stopped parabolic representation, not an optimal coupling
criterion for the two endpoint laws. No passage through arbitrary critical
levels, to infinite v, or to atomic time zero is claimed in (8).

An isoperimetric control supplies only a common lower bound:

\[
 \kappa_u=JB\ge |\partial\{u_s>a\}|^2
       \ge n^2\omega_n^{2/n}v^{2-2/n},              \tag{9}
\]

where omega_n is the volume of the unit ball. The first step is
Cauchy--Schwarz, the second the Euclidean isoperimetric inequality.
Equality holds for a radially decreasing density with spherical level
surfaces. Two lower bounds of this kind do not order kappa_f and kappa_g.

### The geometric initial layer is not the flat atomic initial profile

There is also an exact global estimate, requiring no regular-level
assumption. Let mu have N distinct atoms K, all of positive weight, with
smallest weight p_*. Put

\[
 V_K(r)=|K+rB_3|,\qquad V_K(\rho_K(v))=v\quad(v>0),
\]

where the continuous strictly increasing tube volume has a unique inverse.
Let Q_3(z)=Pr{|G|>z} for a standard Gaussian G in R3. Then at every s,v>0,

\[
 \boxed{\quad
 p_*Q_3(\rho_K(v)/\sqrt{s})
 \le 1-L_\mu(s,v)
 \le N Q_3(\rho_K(v)/\sqrt{s}).\quad}             \tag{9a}
\]

Proof: with C_s=(2pi s)^(-3/2) and d(x,K)=min_{p in K}|x-p|,

\[
 p_*C_s e^{-d(x,K)^2/(2s)}\le u_s(x)
              \le C_s e^{-d(x,K)^2/(2s)}.
\]

The associated superlevel inclusions give the inverse-level bounds

\[
 p_*C_s e^{-\rho_K(v)^2/(2s)}
 \le a(s,v)\le C_s e^{-\rho_K(v)^2/(2s)}.          \tag{9b}
\]

Positive Gaussian mixtures have null positive level sets and continuous
strictly decreasing level volumes, so the inverse exists even at critical
values. Integrate (9b) from v to infinity, using
1-L(s,v)=integral_v^infinity a(s,w)dw, and set w=V_K(r).
The distance-function coarea formula gives V_K'(r) as the boundary area
of the union of balls for almost every r. The union contains one radius-r
ball, and its boundary is contained in the N sphere boundaries. Isoperimetry
therefore gives

\[
 4\pi r^2\le V_K'(r)\le4\pi N r^2\quad\text{a.e. }r>0.
\]

These bounds also justify the tube-volume properties used above. The radial
Gaussian integral is exactly Q_3, proving (9a). No derivative of an inverse
at a critical value is needed in this argument.
For one atom both bounds coincide, recovering the exact Gaussian radial
tail and checking the normalization.

For z>0, integration by parts and the elementary Gaussian tail bound give

\[
 \sqrt{2/\pi}\,z e^{-z^2/2}
 \le Q_3(z)
 \le\sqrt{2/\pi}\,(z+z^{-1})e^{-z^2/2}.
\]

Consequently,

\[
 \boxed{\quad
 -2s\log(1-L_\mu(s,v))\longrightarrow\rho_K(v)^2
 \quad(s\downarrow0).\quad}                     \tag{9c}
\]

The convergence is uniform on any compact positive v interval, with error
O(s|log s|); the constant can depend on K,N,p_* and the interval. This
follows directly from (9a) and the displayed tail bounds, since rho_K is
then bounded above and away from zero. In particular L_mu(s,v) tends to
one for every v>0 for **every finite atomic law**. The common flat limit
alone conceals the whole inverse tube-volume function in its exponential
rate. It is not adequate initial information for a geometric comparison.

For example, let the target law be a pushforward of a finite source law.
Suppose their supports have, at one volume, rho_f>rho_g>0, and set
delta=rho_f^2-rho_g^2. Let p_* be the minimum source
weight and N the source atom count; merged target weights are at least p_*.
For any

\[
 0<s<\min\left\{\rho_f^2,
 \frac{\delta}{2\log(2N\rho_f/(p_*\rho_g))}\right\},            \tag{9d}
\]

(9a) and the tail bounds imply 1-L_g>1-L_f, hence L_f>L_g. Choosing the
target threshold a_g(s,v) gives H_f(a_g)-H_g(a_g)>=L_f-L_g>0 by (6).
Thus a reversal of the equal-radius tube comparison gives an explicit
small-variance range of actual hinge failures. No such geometric reversal
is supplied. This quantifies the known Gaussian-to-Kneser--Poulsen bridge
in heat-profile coordinates; it is not a new positive geometric theorem.
The weight dependence also prevents treating the dominant-atom reduction
as a uniform regular perturbation argument.

## 3. The small-volume coefficient detects anisotropy

Suppose a smooth positive density u has a unique global maximum m at zero,
with

\[
 -\nabla^2\log u(0)=A>0.                           \tag{10}
\]

Assume u tends to zero at infinity; local regularity near its nondegenerate
maximum then suffices for all small-volume levels. As v decreases to zero,

\[
 \boxed{\quad
 \frac{\kappa_u(v)}{n^2\omega_n^{2/n}v^{2-2/n}}
 \longrightarrow
 \frac{\operatorname{tr}A}{n(\det A)^{1/n}}.
 \quad}                                         \tag{11}
\]

Here kappa is the surface product in (5); no heat evolution is needed
for the asymptotic itself.

Proof: write a=m(1-epsilon). Rescaling x=sqrt(2 epsilon) A^(-1/2)y
makes the superlevel set converge in C^1 to the unit ball. Taylor expansion
and the implicit-function theorem justify this convergence, and give

\[
 v=\frac{\omega_n(2\epsilon)^{n/2}}{\sqrt{\det A}}(1+o(1)),
\quad
 B=\frac{n\omega_n(2\epsilon)^{n/2-1}}
           {m\sqrt{\det A}}(1+o(1)).               \tag{12}
\]

The second formula can be obtained directly by transforming the coarea
surface integral; it does not differentiate an uncontrolled little-o
remainder. Alternatively a smooth radial parametrization of the rescaled
level surface gives the same expression. Since Delta u(0)=-m tr A,
the divergence theorem gives

\[
 J=-\int_{\{u>a\}}\Delta u
   =m\operatorname{tr}A\,v(1+o(1)).               \tag{13}
\]

Multiplying (12)--(13) proves (11). The arithmetic-geometric mean inequality
shows that the limit is at least one, with equality precisely when A is
a scalar matrix. In particular, scalar curvature at the source peak and
nonscalar curvature at the target peak force kappa_g>kappa_f at all
sufficiently small common volumes. The volume, rather than the numerical
density threshold, is held equal in this comparison.

## 4. An exact strict, injective contraction

In R3 take the six atoms p_i in {+e_1,-e_1,+e_2,-e_2,+e_3,-e_3}, all of
mass 1/6. Let nu=T#mu with

\[
 r=99/100,\quad t=1/100,\qquad
 T=\operatorname{diag}(r,t,t).                    \tag{14}
\]

The map is globally r-Lipschitz and injective; all 15 distinct pair
distances strictly decrease. It has the explicit contracting motion

\[
 T_\theta=\operatorname{diag}(1-\theta/100,
                     1-99\theta/100,1-99\theta/100),
 \quad0\le\theta\le1.                            \tag{15}
\]

Every squared pair distance is a sum of nonnegative constants times
decreasing squared diagonal factors. Aishwarya--Li's continuous-contraction
theorem therefore proves full Gaussian majorisation for this example at
every variance. The counterexample below concerns only the stronger
coefficientwise comparison proposed in Section 2.

At variance one put C=(2pi)^(-3/2), a=exp(-r^2/2), b=exp(-t^2/2). Then

\[
 f(x)=\frac{C e^{-1/2}}3e^{-|x|^2/2}
                  (\cosh x_1+\cosh x_2+\cosh x_3),
\]
\[
 g(x)=\frac C3e^{-|x|^2/2}
                  (a\cosh(rx_1)+b\cosh(tx_2)+b\cosh(tx_3)).
\tag{16}
\]

Both are even, strictly log-concave, and have their unique maximum at zero.
Indeed for a Gaussian mixture at variance one,

\[
 \nabla^2\log u(x)=-I+\operatorname{Cov}(P\mid x),  \tag{17}
\]

where posterior weights are proportional to exp(-|x-p_i|^2/2).
To derive (17), first differentiate the mixture to get
grad log u=E[P|x]-x; differentiating the normalized posterior weights
then gives the covariance matrix.
All weights are positive. For the source, in any unit direction e,
E[(e.P)^2|x]<1: equality would require all six projections to have
absolute value one, which is impossible. Subtracting the squared mean
only improves the inequality. For the target, |P|<=r<1 gives the uniform
bound Cov(P|x)<=r^2 I. This proves the claimed strict log-concavity.
The same argument works at every variance s>=1, using
-I/s+Cov(P|x)/s^2. Thus no nonmaximal critical level occurs in this range.

At zero, the negative logarithmic Hessians are

\[
 A_f=\frac23 I,\qquad A_g=\operatorname{diag}(x,y,y),
\quad x=1-\frac{r^2a}{a+2b},\quad
 y=1-\frac{t^2b}{a+2b}.                           \tag{18}
\]

Since z exp(-z/2) strictly increases on [0,1] and r^2>t^2, x<y.
Both are positive. Applying (11),

\[
 \lim_{v\downarrow0}\frac{\kappa_g(1,v)}{\kappa_f(1,v)}
       =R:=\frac{x+2y}{3(xy^2)^{1/3}}>1.           \tag{19}
\]

This argument also shows reversal near zero volume at every fixed s>=1:
the source curvature remains scalar, while the target's two curvatures
remain unequal, because z exp(-z/(2s)) increases on [0,1]. The volume
interval may depend on s. There is no claim of a uniform gap as s grows.

## 5. Rational certification of a gap greater than 0.007

For 0<=q<=1/2, the alternating Taylor sum S_16(q) for exp(-q) gives

\[
 S_{16}(q)-\frac{q^{17}}{17!}\le e^{-q}\le S_{16}(q).
\tag{20}
\]

The terms decrease; the alternating-series remainder proves (20).
Use q=9801/20000 and q=1/20000. All interval operations below are rational.
Monotonicity of the fractions in (18) gives the following outward bounds:

\[
 \frac{77017949}{10^8}<x<\frac{77017950}{10^8},\qquad
 \frac{99996172}{10^8}<y<\frac{99996173}{10^8}.       \tag{21}
\]

The exact audit verifies these strict inequalities and then bounds

\[
 R^3=\frac{(x+2y)^3}{27xy^2}
 \ge\frac{(x_-+2y_-)^3}{27x_+y_+^2}
 >\frac{511}{500}
 >\left(\frac{1007}{1000}\right)^3.               \tag{22}
\]

All quantities are positive. The final difference is the exact fraction
852657/10^9. No floating-point root extraction is used. It follows from
(19) that there exists v_0>0 such that

\[
 \boxed{\ \kappa_g(1,v)>\frac{1007}{1000}\kappa_f(1,v)
               \quad(0<v<v_0).\ }                \tag{23}
\]

An explicit numerical value of v_0 is neither computed nor needed to
refute the universal coefficient ordering. Its existence follows from
the proved strict limit. The code verifies the constants in this analytic
argument, not a sampled family of volume levels.

## 6. Robustness and the remaining route

This is not a merging or equality artifact. The source and target each
have six distinct atoms of positive mass; all pairwise losses are strict.
The maxima are nondegenerate. Under sufficiently small changes of the
finite positive weights and source/target coordinates, the strict distance
inequalities and the strict ratio gap persist. Gaussian derivatives depend
continuously on those parameters. The unique peak remains the unique global
peak: use its negative definite Hessian locally, a compact-away-from-peak
gap, and a uniform Gaussian tail bound. The implicit-function theorem then
gives continuous peak locations and Hessians. This proves an open family
of failures of coefficient ordering; no radius for that neighborhood is
claimed.

The negative forcing in (7) is compatible with W>=0. Here majorisation is
already known from (15); earlier positive profile gap and the rest of the
signed evolution compensate it. A future semigroup proof must retain such
integrated or boundary information. In particular, common isoperimetric
lower bounds, eventual strict log-concavity, strict contraction, injectivity,
and nondegenerate peaks do not imply the missing pointwise coefficient sign.

A more focused unresolved question concerns only a regular first contact:
when W first reaches zero from a nonnegative time history at an interior
volume, must J_f>=J_g at that contact? Equation (4) then has the correct
sign, without requiring coefficient ordering everywhere. This is a proposed
sign lemma, not a proved assertion; boundary behavior and critical levels
would still have to be handled. The present example has a positive profile
gap and does not refute this contact condition.

The dominant fixed-atom reduction does not remove this remaining task:
its bounded remainder has no common support-radius bound. Nor may a
regular-level identity silently be extended across all its critical levels
or down to atomic initial time. Those are explicit analytic obligations,
not conclusions of this note. No new sufficient geometric class or
Kneser--Poulsen consequence is asserted.
