# Strict Gaussian hinges and stability without additional damping

Complete author proof, 27 September 2026; independent review of this packet
is pending. The norm-preserving comparison and compact width rigidity used
below have independent campaign acceptance. The unrestricted R3 question
remains open. Historical priority is not asserted.

## 1. Statement and the new implication

Let mu be a bounded probability law in R3, let K=supp(mu), and let T:K->R3
be 1-Lipschitz. Suppose that anchors a,b satisfy

    |x-a|=|T(x)-b|                       for every x in K.       (1)

Write nu=T#mu, f=mu*gamma_s, g=nu*gamma_s, C_s=(2 pi s)^(-3/2),
M_g=||g||_infinity, and

    H_f(h)=integral (f-h)_+,
    D=integral_K integral_K (|x-x'|^2-|T(x)-T(x')|^2) dmu dmu.  (2)

D is the **ordered** mean squared-distance loss. The reviewed
[norm-preserving theorem](../gaussian_norm_preserving_majorisation/PROOF.md)
already proves H_g>=H_f at every variance and threshold, including diffuse
laws. The increment here is an explicit strict margin, equality rigidity
at a single hinge, and the resulting ambient stability with no homothety.

**Theorem 1 (loss-normalized margin).** Suppose s>0, R>=1 is an integer,
and |x-a|<=R sqrt(s). For any nonnegative integers j,k, set

    W=2R+2^(j+1),
    N=2W^2+W+8R+8k+33.                                      (3)

Throughout the entire, possibly empty, threshold interval

    C_s 2^(-j) <= h <= M_g-C_s 2^(-k),

one has

    H_g(h)-H_f(h) >= (D/s) 2^(-N).                            (4)

The coefficient does not depend on the loss, atom count, smallest weight,
or a covariance floor. In particular it remains valid as D decreases to
zero. A supplied radius and threshold separation are material hypotheses.

**Theorem 2 (single-hinge rigidity).** If T is nonisometric on K, then,
simultaneously for every s>0 and every 0<h<M_g,

    H_g(h)>H_f(h),                 ||g||_infinity>||f||_infinity. (5)

Equality at even one h strictly between zero and M_g forces T to preserve
all distances on K. In that case all hinges agree at every variance.

**Corollary 3 (ambient interior).** Fix a nonisometric pair satisfying (1)
and s>0. There is epsilon>0 such that every pair of bounded laws mu',nu'
with W_infinity(mu,mu')<epsilon and W_infinity(nu,nu')<epsilon still satisfies
full Gaussian majorisation at variance s. The perturbations are independent;
they need not retain (1) or even arise from a short map. A common positive
epsilon works over any specified compact interval of positive variances,
and small simultaneous variance perturbations are allowed.

Within the norm-preserving class, the ambient interior points are exactly
the nonisometric support maps. The isometric ones are boundary points.
There is no claimed uniform neighborhood over D->0 or s->0.

The corollary uses the earlier [bounded-law openness theorem, Theorems A/B](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md) and the independently
accepted [compact width rigidity](../gaussian_compact_width_rigidity/PROOF.md).
It is a new application of that openness criterion, not a reproof of it.
For finite supports, the strict mean-width input is also classical; see
[Gorbovickis, Theorem 1.5](https://arxiv.org/html/1006.0531v2).

## 2. A quantitative peak lemma for arbitrary bounded contractions

This auxiliary estimate does not need (1). Work at s=1 and translate the
source so that |p|<=R. Write C=(2 pi)^(-3/2), M_f=||f||_infinity. Then

    log(M_g/M_f) >= (D/4) exp(-4R^2),
    M_g-M_f >= (C D/4) exp(-9R^2/2).                         (6)

Both convolutions vanish at infinity and attain their maxima. If z is a
mode of f, its posterior pi on source labels has density

    d pi/d mu(p) = C exp(-|z-p|^2/2)/f(z).

Differentiating f at z gives z=E_pi p, hence |z|<=R. Since f(z)<=C,
d pi/d mu>=exp(-2R^2), so the ordered posterior loss satisfies
D_pi>=exp(-4R^2)D. Boundedness makes all relative entropies here finite.
The exact posterior identity and Jensen's inequality give

    log(f(z)/C) = -Var_pi(p)/2-KL(pi||mu),
    log(g(E_pi T(p))/C) >= -Var_pi(T(p))/2-KL(pi||mu).

Here Var_pi(Y)=E_pi|Y-E_pi Y|^2 is scalar trace variance. For any label
law pi, D_pi=2[Var_pi(p)-Var_pi(T(p))]. Subtracting the two
displays proves the first bound in (6). Now M_f>=f(0)>=C exp(-R^2/2) and
exp(t)-1>=t prove the second. This is a direct variational calculation,
not an inference from entropy order of f and g. No novelty of qualitative
peak monotonicity is claimed.

The variance-s version replaces R by a source radius divided by sqrt(s),
C by C_s and D by D/s. Thus peak strictness is available for every
nonisometric bounded contraction, independently of the norm-preserving
hinge argument that follows.

## 3. The positive kernel and a uniform radial crossing

Normalize s=1 and translate the two anchors to zero. First let
mu=sum_i w_i delta_(p_i), with positive weights summing to one, and q_i=T(p_i).
Thus |p_i|=|q_i|<=R. Put delta_ij=|p_i-p_j|^2-|q_i-q_j|^2>=0.
For rho>=0, u in [0,1], and independent uniform theta,eta in S2, define

    v_i=C w_i exp[-rho^2/2-|p_i|^2/2
                  +rho((1-u)theta.p_i+u eta.q_i)],
    F=sum_i v_i.

The reviewed norm-preserving identity, its equation (11), integrated in
polar coordinates, is

    integral U(g)-integral U(f)
      =4 pi integral_0^infinity rho^4 integral_0^1 u(1-u)
         E_(theta,eta) [sum_(i<j) delta_ij v_i v_j U''(F)] du drho. (7)

For smooth convex U with U(0)=0 and 0<=U(v)<=v, all integrals are finite
and Tonelli applies to the nonnegative right side. This identity imports
R1's positive spherical operator difference through the reviewed theorem;
no new evolution or dimension-lifting assertion is needed here.

Since |(1-u)theta.p_i+u eta.q_i|<=|p_i|, the exponent of v_i/(C w_i)
is nonpositive. Consequently, including along any chord in the eta ball,

    F<=C,
    |partial_u F|<=2 rho R C,
    |partial_rho F|<=(rho+R) C,
    |F(rho,u,theta,eta)-F(rho,u,theta,eta')|
                                         <=rho R C |eta-eta'|. (8)

For rho>=R, also F<=C exp[-(rho-R)^2/2]. Each pair has the lower bound

    sum_(i<j) delta_ij v_i v_j
            >=(D/2) C^2 exp[-(rho+R)^2].                    (9)

We prove a real-parameter version first. Let 0<tau,epsilon<=1 and suppose

    C tau<=h<=M_g-C epsilon.

Set B=R+1, L=R+2/tau, W=L+R. Choose a mode z_* of g. The posterior
mode identity gives |z_*|<=R, and ||grad g||_infinity<=C. Move outward
from z_* by epsilon/4, choosing any direction if z_*=0, to obtain z_0.
With rho_0=|z_0| and eta_0=z_0/rho_0,

    epsilon/4<=rho_0<=R+epsilon/4<=B,
    g(z_0)>=M_g-C epsilon/4.

Define a_0=epsilon/(16BR), b_0=epsilon/(8BR). For every theta, restrict

    1-a_0 <= u <= 1-a_0/2,       |eta-eta_0|<=b_0.           (10)

The u integral of u(1-u) over this interval is at least a_0^2/8.
The cap in (10), expressed in chordal distance, has probability b_0^2/4.
Using (8), the losses from u=1 and eta=eta_0 are at most C epsilon/8
each. Hence

    F(rho_0,u,theta,eta)>=h+C epsilon/2.

At rho=L the opposite endpoint satisfies

    F(L,u,theta,eta)<=C exp(-2/tau^2)<=C tau/2<=h-C tau/2.   (11)

The middle inequality follows from exp(x)>=1+x and
tau^2/(tau^2+2)<=tau/2 for 0<tau<=1.

Take a nonnegative smooth density zeta_r supported in (h-r,h+r), where
0<r<min(C epsilon/4,C tau/4), and put

    U_r(v)=integral (v-t)_+ zeta_r(t) dt.

Then U_r''=zeta_r, U_r(0)=0 and 0<=U_r(v)<=v for v>=0. For every fixed
triple (u,theta,eta) in (10), U_r'(F(rho_0))=1 and U_r'(F(L))=0.
The fundamental theorem of calculus and (8) give

    1<=integral_(rho_0)^L U_r''(F)|partial_rho F| drho
      <=C W integral_(rho_0)^L U_r''(F) drho.               (12)

Neither monotonicity of F along the ray nor regularity of its level set
is required. This is the source of a uniform margin at critical thresholds.

Restrict the nonnegative integral (7) to (10) and rho in [rho_0,L].
Use rho^4>=(epsilon/4)^4, (9), and (12). This yields

    integral U_r(g)-integral U_r(f)
      >= [pi C epsilon^8 exp(-W^2)/(2^26 B^4 R^4 W)] D.      (13)

For clarity the product before simplification is

    4pi * (epsilon/4)^4 * (D/2)C^2 exp(-W^2)
        * (a_0^2/8) * (b_0^2/4) * 1/(CW).

As r decreases to zero, U_r tends to (v-h)_+. Dominated convergence
applies separately to each density using 0<=U_r(f)<=f and 0<=U_r(g)<=g.
Thus (13) is a hinge bound. There is no infinite-volume uniform smoothing
error to discard.

## 4. Diffuse laws, the dyadic coefficient, and equality

Choose finite quantizations on the original compact support, pushing each
atom by the original T. All pair and anchor conditions hold exactly.
Gaussian translation continuity gives uniform and L1 convergence of both
densities. The ordered losses converge to D, since the bounded continuous
pair-loss function is uniformly continuous; the target peaks converge too.

For a threshold on the closed upper edge h=M_g-C epsilon, apply (13) to
the quantization with

    epsilon_n=min(epsilon, (M_(g_n)-h)/C).

For large n this is positive and tends to epsilon. Keep tau fixed.
The coefficient in (13) is continuous in epsilon. Hinge convergence follows
from the L1 bound |H_f(h)-H_(f_n)(h)|<=||f-f_n||_1. This proves (13) for
all bounded laws with the same constant, including the closed band edge.

Now let tau=2^(-j), epsilon=2^(-k). For integer R>=1, W is an integer and

    pi C>1/8,      exp(-W^2)>=2^(-2W^2),
    B^4 R^4<=16 R^8<=2^(4+8R),       W<=2^W.

Here pi<4 and e<4 suffice. Substitution into (13) gives (3)--(4) at s=1.
At general s, scale coordinates by 1/sqrt(s) and replace h by s^(3/2)h.
Hinge values are invariant under this density/volume rescaling, while D
becomes D/s. This proves Theorem 1.

For any 0<h<M_g, choose j,k large enough to put h in its band. If D>0,
(4) is strict. A continuous nonnegative pair loss has zero integral under
mu x mu only if it is zero at every pair of support points. Thus D=0 is
equivalent to isometry on K. A distance-preserving map on a subset of R3
extends to an ambient rigid motion: choose an affine basis and use
polarization, then extend the resulting orthogonal map from its affine
span. Convolution with the isotropic Gaussian preserves that congruence,
so every hinge is equal. Equation (6) supplies the strict peak statement
when D>0. Theorem 2 follows.

## 5. The all-threshold join and the finite-certificate interface

For a nonisometric bounded contraction the independently accepted compact
width rigidity theorem gives

    m(K)>m(TK),       m(K)=integral_S2 sup_(x in K) theta.x d sigma(theta).

Together with (5), these are exactly the three hypotheses of the old
bounded-law openness theorem: a strict support mean-width gap, a strict
peak gap, and strictly positive hinges throughout 0<h<M_g. That theorem
uses positive-mass support nets for a uniform low-threshold sign, L1
continuity on a compact middle interval, and the strict peak gap above it.
Its compact-family clause supplies one neighborhood over each compact
positive variance interval. This proves Corollary 3 without a new tail
cutoff, covariance assumption, MGF comparison, or extra damping.

Conversely, an isometric pair is in the majorisation set but is not an
ambient interior point. If the source is nonpoint, contract the source
by a factor arbitrarily close to one while leaving the target fixed.
The general peak lemma (6) raises its peak strictly, violating order.
If both are point masses, split the target into two arbitrarily close
distinct points: its peak drops strictly below C_s. The majorisation
set is closed under product W_infinity convergence, by Gaussian L1
continuity, so these are boundary points.

**Minimal R2/R3 handoff.** Once a support-net low-threshold certificate and
a strict source-peak upper bound have supplied a compact middle band,
place that band inside [C_s 2^(-j),M_g-C_s 2^(-k)]. Theorem 1 supplies
its minimum hinge margin (D/s)2^(-N). Consequently the finite beta test in
[BOUNDED_LAWS.md, Theorem C](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md)
succeeds whenever its localization error E_n satisfies

    2 E_n < (D/s)2^(-N).

This replaces an unspecified positive middle minimum by an explicit
loss-normalized bound for the whole anchored class. The support-net and
peak inputs remain separate certified obligations; ordinary moment
matching does not verify them. The bound is conservative and is not a
claim of a practical degree for every input. A bare margin at sampled
thresholds would not provide this conclusion.

The rational checker can avoid a target-peak oracle on the explicit band

    2^(-j)<=h/C_s<=2^(-R^2)-2^(-k),                         (14)

whenever nonempty, since g(b)>=C_s exp(-R^2/2)>=C_s 2^(-R^2).
It also reports the stronger conditional band relative to the true peak.
Its finite checks neither compute that peak nor prove the analytic theorem.

This does not sign an arbitrary contraction outside all existing classes.
In particular it supplies no verified fixed-variance hypothesis for the
canonical proper screw. Unlike a domain-wide all-variance class theorem,
the ambient neighborhood depends on the law and variance band; it gives
no new Kneser--Poulsen limit as s tends to zero. The previous norm-preserving
ball/cap consequences remain unchanged.
